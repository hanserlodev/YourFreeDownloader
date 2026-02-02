package com.hanserlod.youfreedownlader

import android.os.Bundle
import android.widget.*
import android.widget.AdapterView.OnItemSelectedListener
import androidx.appcompat.app.AppCompatActivity
import com.chaquo.python.Python
import com.chaquo.python.android.AndroidPlatform
import kotlin.concurrent.thread

class MainActivity : AppCompatActivity() {

    private lateinit var urlInput: EditText
    private lateinit var downloadButton: Button
    private lateinit var progressBar: ProgressBar
    private lateinit var logTextView: TextView
    private lateinit var formatSpinner: Spinner
    private lateinit var python: Python
    private var formatList: List<Pair<String, String>> = listOf() // Pair(format_id, display_text)

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        supportActionBar?.hide()
        setContentView(R.layout.activity_main)

        urlInput = findViewById(R.id.urlInput)
        downloadButton = findViewById(R.id.downloadButton)
        progressBar = findViewById(R.id.progressBar)
        logTextView = findViewById(R.id.logTextView)
        formatSpinner = findViewById(R.id.formatSpinner)

        if (!Python.isStarted()) {
            Python.start(AndroidPlatform(this))
        }
        python = Python.getInstance()

        downloadButton.setOnClickListener {
            val url = urlInput.text.toString().trim()
            if (url.isNotEmpty()) {
                obtenerFormatos(url)
            } else {
                Toast.makeText(this, "Por favor ingresa una URL válida", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun obtenerFormatos(url: String) {
        progressBar.visibility = ProgressBar.VISIBLE
        progressBar.progress = 0
        logTextView.text = "Obteniendo formatos...\n"

        thread {
            try {
                val pyModule = python.getModule("hanserlod")
                val pyFormatos = pyModule.callAttr("obtener_formatos", url).asList()

                // Convertir PyObject tupla -> Pair<String, String>
                formatList = pyFormatos.map { pyObj ->
                    val tuple = pyObj.asList()
                    Pair(tuple[0].toString(), tuple[1].toString()) // format_id, display_text
                }

                runOnUiThread {
                    logTextView.append("Formatos disponibles:\n")
                    val adapter = ArrayAdapter(
                        this,
                        android.R.layout.simple_spinner_item,
                        formatList.map { it.second } // Mostrar solo la descripción
                    )
                    adapter.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item)
                    formatSpinner.adapter = adapter
                }

                // Configurar el Spinner
                formatSpinner.onItemSelectedListener = object : OnItemSelectedListener {
                    override fun onItemSelected(parent: AdapterView<*>, view: android.view.View?, position: Int, id: Long) {
                        val selectedFormatId = formatList[position].first
                        // Llamar a descargarVideo con el formato seleccionado
                        descargarVideo(url, selectedFormatId, soloAudio = false)
                    }

                    override fun onNothingSelected(parent: AdapterView<*>) {}
                }

            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                    logTextView.append("Error: ${e.message}\n")
                    progressBar.progress = 0
                    progressBar.visibility = ProgressBar.GONE
                }
            }
        }
    }

    private fun descargarVideo(url: String, formatId: String, soloAudio: Boolean = false) {
        thread {
            try {
                val pyModule = python.getModule("hanserlod")
                val outputPath = "/sdcard/Download/%(title)s.%(ext)s"
                pyModule.callAttr("descargar_video", url, outputPath, formatId, soloAudio)

                runOnUiThread {
                    progressBar.progress = 100
                    logTextView.append("¡Descarga completada!\n")
                }

            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Error: ${e.message}", Toast.LENGTH_LONG).show()
                    logTextView.append("Error: ${e.message}\n")
                    progressBar.progress = 0
                    progressBar.visibility = ProgressBar.GONE
                }
            }
        }
    }
}
