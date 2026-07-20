package com.hanserlod.youfreedownlader.ui.screen

import android.content.Context
import android.net.Uri
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.lifecycle.viewmodel.compose.viewModel
import com.hanserlod.youfreedownlader.domain.model.DownloadProgress
import com.hanserlod.youfreedownlader.domain.model.DownloadStatus
import com.hanserlod.youfreedownlader.domain.model.MediaType
import com.hanserlod.youfreedownlader.domain.model.VideoFormat
import com.hanserlod.youfreedownlader.domain.model.VideoInfo
import com.hanserlod.youfreedownlader.ui.viewmodel.DownloadViewModel

@OptIn(androidx.lifecycle.viewmodel.compose.ExperimentalViewModelComposeApi::class)
@Composable
fun DownloadScreen(viewModel: DownloadViewModel = viewModel()) {
    val url by viewModel.url.collectAsStateWithLifecycle("")
    val videoInfo by viewModel.videoInfo.collectAsStateWithLifecycle()
    val mediaType by viewModel.mediaType.collectAsStateWithLifecycle(MediaType.VIDEO)
    val availableFormats by viewModel.availableFormats.collectAsStateWithLifecycle(emptyList())
    val selectedFormat by viewModel.selectedFormat.collectAsStateWithLifecycle()
    val downloadProgress by viewModel.downloadProgress.collectAsStateWithLifecycle(DownloadProgress())
    val isLoading by viewModel.isLoading.collectAsStateWithLifecycle(false)
    val error by viewModel.error.collectAsStateWithLifecycle()
    val downloadPath by viewModel.downloadPath.collectAsStateWithLifecycle()

    var urlText by remember { mutableStateOf(url) }
    var showFormatDropdown by remember { mutableStateOf(false) }

    val context = LocalContext.current
    val scrollState = rememberScrollState()

    Scaffold(
        topBar = {
            TopAppBar(
                title = { Text("YourFreeDownloader") },
                colors = TopAppBarDefaults.topAppBarColors(
                    containerColor = MaterialTheme.colorScheme.surfaceContainer
                )
            )
        }
    ) { padding ->
        Box(
            modifier = Modifier
                .fillMaxSize()
                .padding(padding)
                .verticalScroll(scrollState)
        ) {
            Column(
                modifier = Modifier.fillMaxWidth(),
                verticalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                // URL Input Section
                UrlInputSection(
                    urlText = urlText,
                    onUrlChange = { newUrl ->
                        urlText = newUrl
                        viewModel.setUrl(newUrl)
                    },
                    onGetInfoClick = { viewModel.fetchVideoInfo() },
                    isLoading = isLoading,
                    enabled = urlText.isNotBlank()
                )

                // Error Message
                error?.let {
                    ErrorCard(message = it, onDismiss = { viewModel._error.value = null })
                }

                // Video Info Section
                videoInfo?.let { info ->
                    VideoInfoSection(info = info)
                }

                // Media Type Selection
                MediaTypeSection(
                    mediaType = mediaType,
                    onMediaTypeChange = { viewModel.setMediaType(it) }
                )

                // Quality Selection
                if (videoInfo != null && availableFormats.isNotEmpty()) {
                    QualitySelectionSection(
                        formats = availableFormats,
                        selectedFormat = selectedFormat,
                        onFormatSelect = { viewModel.selectFormat(it) },
                        showDropdown = showFormatDropdown,
                        onDropdownToggle = { showFormatDropdown = it }
                    )
                }

                // Download Section
                DownloadSection(
                    videoInfo = videoInfo,
                    selectedFormat = selectedFormat,
                    downloadProgress = downloadProgress,
                    onDownloadClick = {
                        requestStoragePermissionAndDownload(context, viewModel)
                    },
                    onCancelClick = { viewModel.cancelDownload() },
                    isDownloading = downloadProgress.status == DownloadStatus.DOWNLOADING
                )

                // Download Complete
                downloadPath?.let { path ->
                    DownloadCompleteCard(path = path)
                }
            }
        }
    }
}

// URL Input Section
@Composable
fun UrlInputSection(
    urlText: String,
    onUrlChange: (String) -> Unit,
    onGetInfoClick: () -> Unit,
    isLoading: Boolean,
    enabled: Boolean
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("YouTube URL", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(8.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                verticalAlignment = Alignment.CenterVertically
            ) {
                OutlinedTextField(
                    value = urlText,
                    onValueChange = onUrlChange,
                    modifier = Modifier
                        .fillMaxWidth()
                        .weight(1f),
                    placeholder = { Text("https://www.youtube.com/watch?v=...") },
                    singleLine = true,
                    keyboardOptions = androidx.compose.ui.text.input.KeyboardOptions(
                        keyboardType = androidx.compose.ui.text.input.KeyboardType.Url
                    ),
                    enabled = enabled
                )
                Spacer(modifier = Modifier.width(8.dp))
                Button(
                    onClick = onGetInfoClick,
                    enabled = enabled && !isLoading,
                    modifier = Modifier.height(48.dp)
                ) {
                    if (isLoading) {
                        CircularProgressIndicator(modifier = Modifier.size(24.dp))
                    } else {
                        Text("Get Info")
                    }
                }
            }
        }
    }
}

// Error Card
@Composable
fun ErrorCard(message: String, onDismiss: () -> Unit) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.errorContainer
        )
    ) {
        Row(
            modifier = Modifier.padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Text(message, color = MaterialTheme.colorScheme.onErrorContainer)
            IconButton(onClick = onDismiss) {
                Icon(
                    imageVector = androidx.compose.material.icons.Icons.Filled.Close,
                    contentDescription = "Dismiss"
                )
            }
        }
    }
}

// Video Info Section
@Composable
fun VideoInfoSection(info: VideoInfo) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(info.title, style = MaterialTheme.typography.titleLarge, maxLines = 2, overflow = TextOverflow.Ellipsis)
            Spacer(modifier = Modifier.height(8.dp))
            Row(horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                info.duration?.let { dur ->
                    InfoChip(icon = androidx.compose.material.icons.Icons.Filled.AccessTime, text = formatDuration(dur))
                }
                info.uploader?.let { uploader ->
                    InfoChip(icon = androidx.compose.material.icons.Icons.Filled.Person, text = uploader)
                }
                info.viewCount?.let { views ->
                    InfoChip(icon = androidx.compose.material.icons.Icons.Filled.Visibility, text = formatViews(views))
                }
            }
        }
    }
}

@Composable
fun InfoChip(icon: androidx.compose.ui.graphics.vector.ImageVector, text: String) {
    Row(
        modifier = Modifier
            .padding(vertical = 4.dp)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest, shape = MaterialTheme.shapes.small)
            .padding(horizontal = 12.dp, vertical = 6.dp),
        horizontalArrangement = Arrangement.spacedBy(4.dp)
    ) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Text(text, style = MaterialTheme.typography.bodySmall)
    }
}

// Media Type Section
@Composable
fun MediaTypeSection(
    mediaType: MediaType,
    onMediaTypeChange: (MediaType) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Download Type", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(12.dp))
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                MediaTypeChip(
                    label = "Video",
                    icon = androidx.compose.material.icons.Icons.Filled.Videocam,
                    isSelected = mediaType == MediaType.VIDEO,
                    onClick = { onMediaTypeChange(MediaType.VIDEO) }
                )
                MediaTypeChip(
                    label = "Audio (MP3)",
                    icon = androidx.compose.material.icons.Icons.Filled.AudioFile,
                    isSelected = mediaType == MediaType.AUDIO_ONLY,
                    onClick = { onMediaTypeChange(MediaType.AUDIO_ONLY) }
                )
            }
        }
    }
}

@Composable
fun MediaTypeChip(
    label: String,
    icon: androidx.compose.ui.graphics.vector.ImageVector,
    isSelected: Boolean,
    onClick: () -> Unit
) {
    val colors = if (isSelected) {
        MaterialTheme.colorScheme.primary to MaterialTheme.colorScheme.onPrimary
    } else {
        MaterialTheme.colorScheme.surfaceContainerHighest to MaterialTheme.colorScheme.onSurface
    }

    OutlinedButton(
        onClick = onClick,
        modifier = Modifier.fillMaxWidth(),
        colors = ButtonDefaults.buttonColors(
            containerColor = colors.first,
            contentColor = colors.second
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(vertical = 12.dp),
            horizontalArrangement = Arrangement.Center,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Icon(icon, contentDescription = null)
            Spacer(modifier = Modifier.width(8.dp))
            Text(label, fontWeight = FontWeight.Medium)
        }
    }
}

// Quality Selection Section
@Composable
fun QualitySelectionSection(
    formats: List<VideoFormat>,
    selectedFormat: VideoFormat?,
    onFormatSelect: (VideoFormat) -> Unit,
    showDropdown: Boolean,
    onDropdownToggle: (Boolean) -> Unit
) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 2.dp)
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text("Quality", style = MaterialTheme.typography.titleMedium)
            Spacer(modifier = Modifier.height(8.dp))

            DropdownMenu(
                expanded = showDropdown,
                onDismissRequest = { onDropdownToggle(false) }
            ) {
                formats.forEach { format ->
                    DropdownMenuItem(
                        text = { Text(format.displayName, maxLines = 1, overflow = TextOverflow.Ellipsis) },
                        onClick = {
                            onFormatSelect(format)
                            onDropdownToggle(false)
                        }
                    )
                }
            }

            OutlinedButton(
                onClick = { onDropdownToggle(!showDropdown) },
                modifier = Modifier.fillMaxWidth(),
                trailingIcon = {
                    Icon(
                        imageVector = if (showDropdown)
                            androidx.compose.material.icons.Icons.Filled.ExpandLess
                        else
                            androidx.compose.material.icons.Icons.Filled.ExpandMore,
                        contentDescription = null
                    )
                }
            ) {
                Text(
                    selectedFormat?.displayName ?: "Select quality",
                    maxLines = 1,
                    overflow = TextOverflow.Ellipsis
                )
            }
        }
    }
}

// Download Section
@Composable
fun DownloadSection(
    videoInfo: VideoInfo?,
    selectedFormat: VideoFormat?,
    downloadProgress: DownloadProgress,
    onDownloadClick: () -> Unit,
    onCancelClick: () -> Unit,
    isDownloading: Boolean
) {
    val canDownload = videoInfo != null && selectedFormat != null && !isDownloading

    Card(
        modifier = Modifier.fillMaxWidth(),
        elevation = CardDefaults.cardElevation(defaultElevation = 4.dp),
        colors = CardDefaults.cardColors(
            containerColor = if (isDownloading) MaterialTheme.colorScheme.primaryContainer else MaterialTheme.colorScheme.surface
        )
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            if (isDownloading) {
                DownloadProgressView(progress = downloadProgress)
            }

            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(8.dp)
            ) {
                Button(
                    onClick = if (canDownload) onDownloadClick else null,
                    enabled = canDownload,
                    modifier = Modifier.fillMaxWidth().weight(1f).height(56.dp),
                    colors = ButtonDefaults.buttonColors(
                        containerColor = MaterialTheme.colorScheme.primary
                    )
                ) {
                    if (isDownloading) {
                        Row(
                            horizontalArrangement = Arrangement.Center,
                            verticalAlignment = Alignment.CenterVertically
                        ) {
                            CircularProgressIndicator(color = MaterialTheme.colorScheme.onPrimary, modifier = Modifier.size(24.dp))
                            Spacer(modifier = Modifier.width(12.dp))
                            Text("Downloading...", color = MaterialTheme.colorScheme.onPrimary, fontWeight = FontWeight.Bold)
                        }
                    } else {
                        Text("Download", fontWeight = FontWeight.Bold, fontSize = 18.sp)
                    }
                }

                if (isDownloading) {
                    Button(
                        onClick = onCancelClick,
                        modifier = Modifier.width(56.dp).height(56.dp),
                        colors = ButtonDefaults.buttonColors(
                            containerColor = MaterialTheme.colorScheme.errorContainer
                        )
                    ) {
                        Icon(
                            androidx.compose.material.icons.Icons.Filled.Close,
                            contentDescription = "Cancel",
                            tint = MaterialTheme.colorScheme.onErrorContainer
                        )
                    }
                }
            }
        }
    }
}

@Composable
fun DownloadProgressView(progress: DownloadProgress) {
    Column(modifier = Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(8.dp)) {
        // Progress bar
        Column(Modifier.fillMaxWidth(), verticalArrangement = Arrangement.spacedBy(4.dp)) {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.SpaceBetween
            ) {
                Text(progress.progressText, style = MaterialTheme.typography.bodyMedium)
                Text("${"%.1f".format(progress.percent)}%", style = MaterialTheme.typography.bodyMedium)
            }
            LinearProgressIndicator(progress = progress.percent / 100f)
        }

        // Details
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            DetailChip(
                icon = androidx.compose.material.icons.Icons.Filled.Speed,
                label = "Speed",
                value = progress.speedMbps?.let { "${"%.1f".format(it)} MB/s" } ?: "--"
            )
            DetailChip(
                icon = androidx.compose.material.icons.Icons.Filled.Timer,
                label = "ETA",
                value = progress.etaFormatted
            )
        }
    }
}

@Composable
fun DetailChip(icon: androidx.compose.ui.graphics.vector.ImageVector, label: String, value: String) {
    Row(
        modifier = Modifier
            .weight(1f)
            .padding(12.dp)
            .background(MaterialTheme.colorScheme.surfaceContainerHighest, shape = MaterialTheme.shapes.small),
        horizontalArrangement = Arrangement.spacedBy(8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Icon(icon, contentDescription = null, tint = MaterialTheme.colorScheme.primary)
        Column {
            Text(label, style = MaterialTheme.typography.labelSmall, color = MaterialTheme.colorScheme.onSurfaceVariant)
            Text(value, style = MaterialTheme.typography.bodyMedium, fontWeight = FontWeight.Medium)
        }
    }
}

// Download Complete Card
@Composable
fun DownloadCompleteCard(path: String) {
    Card(
        modifier = Modifier.fillMaxWidth(),
        colors = CardDefaults.cardColors(
            containerColor = MaterialTheme.colorScheme.tertiaryContainer
        )
    ) {
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically
        ) {
            Column {
                Text("Download Complete!", style = MaterialTheme.typography.titleMedium, color = MaterialTheme.colorScheme.onTertiaryContainer)
                Text(path, style = MaterialTheme.typography.bodySmall, color = MaterialTheme.colorScheme.onTertiaryContainer, maxLines = 1, overflow = TextOverflow.Ellipsis)
            }
            IconButton(onClick = { /* open folder */ }) {
                Icon(
                    androidx.compose.material.icons.Icons.Filled.FolderOpen,
                    contentDescription = "Open folder",
                    tint = MaterialTheme.colorScheme.onTertiaryContainer
                )
            }
        }
    }
}

// Storage Permission
fun requestStoragePermissionAndDownload(context: Context, viewModel: DownloadViewModel) {
    // For API 29+, use MediaStore
    // For API 33+, use READ_MEDIA_VIDEO/AUDIO
    // For now, just use Downloads folder
    val outputDir = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
        Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS).absolutePath
    } else {
        Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS).absolutePath
    }
    viewModel.startDownload(outputDir)
}

private fun formatDuration(seconds: Int): String {
    val hours = seconds / 3600
    val minutes = (seconds % 3600) / 60
    val secs = seconds % 60
    return if (hours > 0) "%d:%02d:%02d".format(hours, minutes, secs) else "%d:%02d".format(minutes, secs)
}

private fun formatViews(views: Long): String {
    return when {
        views >= 1_000_000 -> "%.1fM".format(views / 1_000_000.0)
        views >= 1_000 -> "%.1fK".format(views / 1000.0)
        else -> views.toString()
    }
}