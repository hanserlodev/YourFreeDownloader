package com.hanserlod.youfreedownlader.domain.model

import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.setValue

/**
 * Media type for download
 */
enum class MediaType {
    VIDEO,
    AUDIO_ONLY
}

/**
 * Video format information
 */
data class VideoFormat(
    val formatId: String,
    val ext: String,
    val resolution: String? = null,
    val fps: Float? = null,
    val vcodec: String? = null,
    val acodec: String? = null,
    val abr: Int? = null, // audio bitrate in kbps
    val filesize: Long? = null,
    val filesizeApprox: Long? = null,
    val formatNote: String? = null
) {
    val isVideo: Boolean
        get() = vcodec != null && vcodec != "none"

    val isAudioOnly: Boolean
        get() = acodec != null && acodec != "none" && (vcodec == null || vcodec == "none")

    val displayName: String
        get() {
            val parts = mutableListOf<String>()
            resolution?.let { parts.add("$it p") }
            fps?.let { parts.add("${it}fps") }
            if (isVideo) parts.add("video: ${vcodec ?: "unknown"}")
            if (isAudioOnly) parts.add("audio: ${acodec ?: "unknown"}")
            abr?.let { parts.add("${it}kbps") }
            filesize?.let { parts.add("${(it / (1024 * 1024)).toString()}MB") }
            filesizeApprox?.let { parts.add("~${(it / (1024 * 1024)).toString()}MB") }
            formatNote?.let { parts.add(it) }
            return if (parts.isNotEmpty()) parts.joinToString(" | ") else formatId
        }
}

/**
 * Video metadata
 */
data class VideoInfo(
    val id: String,
    val title: String,
    val duration: Int? = null,
    val uploader: String? = null,
    val viewCount: Long? = null,
    val thumbnail: String? = null,
    val formats: List<VideoFormat> = emptyList(),
    val isLive: Boolean = false
) {
    val videoFormats: List<VideoFormat>
        get() = formats.filter { it.isVideo }

    val audioFormats: List<VideoFormat>
        get() = formats.filter { it.isAudioOnly }

    val bestVideoFormat: VideoFormat?
        get() = videoFormats.maxByOrNull { it.resolution?.replace("p", "")?.toIntOrNull() ?: 0 }

    val bestAudioFormat: VideoFormat?
        get() = audioFormats.maxByOrNull { it.abr ?: 0 }
}

/**
 * Download progress
 */
data class DownloadProgress(
    val status: DownloadStatus = DownloadStatus.PENDING,
    val downloadedBytes: Long = 0,
    val totalBytes: Long? = null,
    val speed: Double? = null, // bytes/sec
    val eta: Int? = null, // seconds
    val percent: Double = 0.0,
    val error: String? = null
) {
    val speedMbps: Double?
        get() = speed?.let { it / (1024 * 1024) }

    val etaFormatted: String
        get() = eta?.let { "${it / 60}:${"%02d".format(it % 60)}" } ?: "--:--"

    val progressText: String
        get() {
            return when (status) {
                DownloadStatus.DOWNLOADING -> {
                    val downloaded = (downloadedBytes / (1024 * 1024)).toString()
                    val total = totalBytes?.let { (it / (1024 * 1024)).toString() } ?: "?"
                    "$downloaded / $total MB (${"%.1f".format(percent)}%)"
                }
                DownloadStatus.COMPLETED -> "Completed"
                DownloadStatus.FAILED -> "Failed: ${error ?: "Unknown"}"
                DownloadStatus.CANCELLED -> "Cancelled"
                else -> "Pending"
            }
        }
}

enum class DownloadStatus {
    PENDING,
    DOWNLOADING,
    COMPLETED,
    FAILED,
    CANCELLED
}

/**
 * Download task state
 */
data class DownloadTask(
    val url: String,
    val videoInfo: VideoInfo? = null,
    val selectedFormat: VideoFormat? = null,
    val mediaType: MediaType = MediaType.VIDEO,
    val outputDir: String = "",
    var progress: DownloadProgress = DownloadProgress(),
    var isDownloading: Boolean = false
)