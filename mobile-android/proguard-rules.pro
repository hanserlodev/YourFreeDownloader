# ProGuard rules for YourFreeDownloader

# Keep Chaquopy Python integration
-keep class com.chaquo.python.** { *; }
-keep class com.chaquo.python.android.** { *; }

# Keep yt-dlp classes
-keep class yt_dlp.** { *; }
-keep class yt_dlp.version { *; }

# Keep ffmpeg-python classes
-keep class ffmpeg.** { *; }

# Keep application classes
-keep class com.hanserlod.youfreedownlader.** { *; }

# Keep Kotlin coroutines
-keep class kotlinx.coroutines.** { *; }

# Keep Compose runtime
-keep class androidx.compose.** { *; }

# Keep lifecycle
-keep class androidx.lifecycle.** { *; }

# Keep activity result
-keep class androidx.activity.result.** { *; }

# Keep Coil
-keep class coil.** { *; }