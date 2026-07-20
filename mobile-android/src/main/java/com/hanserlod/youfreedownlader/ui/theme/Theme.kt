package com.hanserlod.youfreedownlader.ui.theme

import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.darkColorScheme
import androidx.compose.material3.lightColorScheme
import androidx.compose.runtime.Composable
import androidx.compose.ui.graphics.Color

private val DarkColorScheme = darkColorScheme(
    primary = Color(0xFF7C4DFF),
    primaryContainer = Color(0xFF651FFF),
    secondary = Color(0xFF03DAC6),
    secondaryContainer = Color(0xFF018786),
    tertiary = Color(0xFFFF0187),
    tertiaryContainer = Color(0xFF880E4F),
    surface = Color(0xFF121212),
    surfaceContainerHighest = Color(0xFF1E1E1E),
    onSurface = Color(0xFFFFFFFF),
    onSurfaceVariant = Color(0xFFB0B0B0),
    outline = Color(0xFF757575),
    error = Color(0xFFCF6679),
    errorContainer = Color(0xFFB00020),
    background = Color(0xFF121212),
    onBackground = Color(0xFFFFFFFF),
)

private val LightColorScheme = lightColorScheme(
    primary = Color(0xFF651FFF),
    primaryContainer = Color(0xFFE8D0FF),
    secondary = Color(0xFF018786),
    secondaryContainer = Color(0xFFB2F0EF),
    tertiary = Color(0xFF880E4F),
    tertiaryContainer = Color(0xFFFFD8E4),
    surface = Color(0xFFFFFFFF),
    surfaceContainerHighest = Color(0xFFF5F5F5),
    onSurface = Color(0xFF121212),
    onSurfaceVariant = Color(0xFF424242),
    outline = Color(0xFF757575),
    error = Color(0xFFB00020),
    errorContainer = Color(0xFFFFEBEE),
    background = Color(0xFFF5F5F5),
    onBackground = Color(0xFF121212),
)

@Composable
fun YourFreeDownloaderTheme(
    darkTheme: Boolean = false,
    content: @Composable () -> Unit
) {
    val colorScheme = if (darkTheme) DarkColorScheme else LightColorScheme

    MaterialTheme(
        colorScheme = colorScheme,
        typography = Typography,
        content = content
    )
}