package com.hanserlod.youfreedownlader.ui.viewmodel

import android.app.Application
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.hanserlod.youfreedownlader.domain.model.DownloadProgress
import com.hanserlod.youfreedownlader.domain.model.DownloadStatus
import com.hanserlod.youfreedownlader.domain.model.MediaType
import com.hanserlod.youfreedownlader.domain.model.VideoFormat
import com.hanserlod.youfreedownlader.domain.model.VideoInfo
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.channels.Channel
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext

class DownloadViewModel(application: Application) : ViewModel() {

    // Python integration
    private var python: com.chaquo.python.Python? = null
    private var hanserlodModule: com.chaquo.python.PyObject? = null

    // State
    private val _url = androidx.lifecycle.MutableLiveData<String>("")
    val url: androidx.lifecycle.LiveData<String> = _url

    private val _videoInfo = androidx.lifecycle.MutableLiveData<VideoInfo?>()
    val videoInfo: androidx.lifecycle.LiveData<VideoInfo?> = _videoInfo

    private val _mediaType = androidx.lifecycle.MutableLiveData<MediaType>(MediaType.VIDEO)
    val mediaType: androidx.lifecycle.LiveData<MediaType> = _mediaType

    private val _selectedFormat = androidx.lifecycle.MutableLiveData<VideoFormat?>()
    val selectedFormat: androidx.lifecycle.LiveData<VideoFormat?> = _selectedFormat

    private val _availableFormats = androidx.lifecycle.MutableLiveData<List<VideoFormat>>(emptyList())
    val availableFormats: androidx.lifecycle.LiveData<List<VideoFormat>> = _availableFormats

    private val _downloadProgress = androidx.lifecycle.MutableLiveData<DownloadProgress>(DownloadProgress())
    val downloadProgress: androidx.lifecycle.LiveData<DownloadProgress> = _downloadProgress

    private val _isLoading = androidx.lifecycle.MutableLiveData<Boolean>(false)
    val isLoading: androidx.lifecycle.LiveData<Boolean> = _isLoading

    private val _error = androidx.lifecycle.MutableLiveData<String?>()
    val error: androidx.lifecycle.LiveData<String?> = _error

    private val _downloadPath = androidx.lifecycle.MutableLiveData<String?>()
    val downloadPath: androidx.lifecycle.LiveData<String?> = _downloadPath

    private var currentDownloadJob: kotlinx.coroutines.Job? = null

    init {
        initializePython()
    }

    private fun initializePython() {
        viewModelScope.launch(Dispatchers.IO) {
            try {
                if (!com.chaquo.python.Python.isStarted()) {
                    com.chaquo.python.Python.start(com.chaquo.python.android.AndroidPlatform(application))
                }
                python = com.chaquo.python.Python.getInstance()
                hanserlodModule = python?.getModule("hanserlod")
                _isLoading.postValue(false)
            } catch (e: Exception) {
                _error.postValue("Failed to initialize Python: ${e.message}")
            }
        }
    }

    fun setUrl(newUrl: String) {
        _url.value = newUrl
    }

    fun fetchVideoInfo() {
        val url = _url.value?.trim()
        if (url.isNullOrEmpty()) {
            _error.value = "Please enter a URL"
            return
        }

        if (!isValidYouTubeUrl(url)) {
            _error.value = "Invalid YouTube URL"
            return
        }

        _isLoading.value = true
        _error.value = null

        viewModelScope.launch(Dispatchers.IO) {
            try {
                val pyFormatos = hanserlodModule?.callAttr("obtener_formatos", url)?.asList()
                val videoInfo = parseVideoInfo(url, pyFormatos)
                _videoInfo.postValue(videoInfo)
                _isLoading.postValue(false)
            } catch (e: Exception) {
                _error.postValue("Failed to fetch video info: ${e.message}")
                _isLoading.postValue(false)
            }
        }
    }

    private fun isValidYouTubeUrl(url: String): Boolean {
        val patterns = listOf(
            "youtube\\.com/watch\\?v=",
            "youtu\\.be/",
            "youtube\\.com/shorts/",
            "youtube\\.com/embed/"
        )
        return patterns.any { url.contains(it) }
    }

    private fun parseVideoInfo(url: String, pyFormatos: com.chaquo.python.PyObject?): VideoInfo? {
        val formatList = mutableListOf<VideoFormat>()
        pyFormatos?.let { pyList ->
            for (i in 0 until pyList.length()) {
                val item = pyList[i].asList()
                if (item.length() >= 2) {
                    val formatId = item[0].toString()
                    val desc = item[1].toString()
                    // Parse description to extract format info
                    val format = parseFormatDescription(formatId, desc)
                    formatList.add(format)
                }
            }
        }

        return VideoInfo(
            id = extractVideoId(url) ?: "",
            title = "Loading...",
            formats = formatList
        )
    }

    private fun parseFormatDescription(formatId: String, description: String): VideoFormat {
        // description format: "itag - 720p - mp4" or similar
        val parts = description.split(" - ")
        return VideoFormat(
            formatId = formatId,
            ext = parts.lastOrNull()?.split(".")?.last() ?: "mp4",
            resolution = parts.find { it.endsWith("p") }?.removeSuffix("p"),
            formatNote = parts.find { it.contains("kbps") || it.contains("fps") }
        )
    }

    private fun extractVideoId(url: String): String? {
        val patterns = listOf(
            "v=([^&]+)".toRegex(),
            "youtu\\.be/([^?&]+)".toRegex(),
            "shorts/([^?&]+)".toRegex()
        )
        for (pattern in patterns) {
            val match = pattern.matchEntire(url) ?: pattern.find(url)
            match?.groupValues?.get(1)?.let { return it }
        }
        return null
    }

    fun setMediaType(type: MediaType) {
        _mediaType.value = type
        updateAvailableFormats()
    }

    fun selectFormat(format: VideoFormat) {
        _selectedFormat.value = format
    }

    private fun updateAvailableFormats() {
        val info = _videoInfo.value
        if (info == null) return

        val formats = when (_mediaType.value) {
            MediaType.VIDEO -> info.videoFormats
            MediaType.AUDIO_ONLY -> info.audioFormats
        }
        _availableFormats.value = formats
        _selectedFormat.value = formats.firstOrNull()
    }

    fun startDownload(outputDir: String) {
        val url = _url.value?.trim()
        val format = _selectedFormat.value
        val type = _mediaType.value

        if (url.isNullOrEmpty() || format == null) {
            _error.value = "Missing URL or format"
            return
        }

        _downloadProgress.value = DownloadProgress(status = DownloadStatus.DOWNLOADING)
        _error.value = null

        currentDownloadJob?.cancel()
        currentDownloadJob = viewModelScope.launch(Dispatchers.IO) {
            try {
                val progressChannel = Channel<DownloadProgress>(10)

                // Start progress listener
                val progressJob = viewModelScope.launch {
                    for (progress in progressChannel) {
                        _downloadProgress.postValue(progress)
                    }
                }

                // Run download
                val outputPath = "$outputDir/%(title)s.%(ext)s"
                val soloAudio = type == MediaType.AUDIO_ONLY

                hanserlodModule?.callAttr(
                    "descargar_video",
                    url,
                    outputPath,
                    format.formatId,
                    soloAudio
                )

                progressChannel.close()
                progressJob.join()

                _downloadProgress.postValue(DownloadProgress(status = DownloadStatus.COMPLETED))
                _downloadPath.postValue(outputDir)
            } catch (e: Exception) {
                if (e !is kotlinx.coroutines.CancellationException) {
                    _downloadProgress.postValue(DownloadProgress(
                        status = DownloadStatus.FAILED,
                        error = e.message
                    ))
                    _error.postValue("Download failed: ${e.message}")
                }
            }
        }
    }

    fun cancelDownload() {
        currentDownloadJob?.cancel()
        _downloadProgress.value = DownloadProgress(status = DownloadStatus.CANCELLED)
    }

    override fun onCleared() {
        currentDownloadJob?.cancel()
        super.onCleared()
    }
}