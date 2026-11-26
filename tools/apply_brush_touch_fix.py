from pathlib import Path

path = Path("source/MarkAwayAI/app/src/main/java/com/markaway/ai/MainActivity.kt")
text = path.read_text(encoding="utf-8")

old_import = "import androidx.compose.foundation.gestures.detectDragGestures\n"
new_import = (
    "import androidx.compose.foundation.gestures.awaitEachGesture\n"
    "import androidx.compose.foundation.gestures.awaitFirstDown\n"
    "import androidx.compose.ui.input.pointer.PointerEventPass\n"
)
if text.count(old_import) != 1:
    raise SystemExit("Expected detectDragGestures import exactly once")
text = text.replace(old_import, new_import, 1)

old = """                Modifier.fillMaxSize().pointerInput(sourceBitmap) {
                    val imageScale = minOf(size.width / sourceBitmap.width.toFloat(), size.height / sourceBitmap.height.toFloat())
                    val drawnWidth = sourceBitmap.width * imageScale
                    val drawnHeight = sourceBitmap.height * imageScale
                    val offsetX = (size.width - drawnWidth) / 2f
                    val offsetY = (size.height - drawnHeight) / 2f
                    fun isInsideImage(position: Offset) =
                        position.x >= offsetX && position.x <= offsetX + drawnWidth &&
                        position.y >= offsetY && position.y <= offsetY + drawnHeight
                    fun imagePoint(position: Offset) = Offset(
                        ((position.x - offsetX) / drawnWidth).coerceIn(0f, 1f),
                        ((position.y - offsetY) / drawnHeight).coerceIn(0f, 1f)
                    )
                    var drawingOnImage = false
                    detectDragGestures(
                        onDragStart = { start ->
                            drawingOnImage = isInsideImage(start)
                            if (drawingOnImage) {
                                latestOnStrokesChange(latestStrokes + listOf(listOf(imagePoint(start))))
                            }
                        },
                        onDrag = { change, _ ->
                            change.consume()
                            if (drawingOnImage) {
                                val p = imagePoint(change.position)
                                val updated = latestStrokes.toMutableList()
                                if (updated.isNotEmpty()) updated[updated.lastIndex] = updated.last() + p
                                latestOnStrokesChange(updated)
                            }
                        },
                        onDragEnd = { drawingOnImage = false },
                        onDragCancel = { drawingOnImage = false }
                    )
                }"""
new = """                Modifier.fillMaxSize().pointerInput(sourceBitmap) {
                    val imageScale = minOf(size.width / sourceBitmap.width.toFloat(), size.height / sourceBitmap.height.toFloat())
                    val drawnWidth = sourceBitmap.width * imageScale
                    val drawnHeight = sourceBitmap.height * imageScale
                    val offsetX = (size.width - drawnWidth) / 2f
                    val offsetY = (size.height - drawnHeight) / 2f
                    fun isInsideImage(position: Offset) =
                        position.x >= offsetX && position.x <= offsetX + drawnWidth &&
                        position.y >= offsetY && position.y <= offsetY + drawnHeight
                    fun imagePoint(position: Offset) = Offset(
                        ((position.x - offsetX) / drawnWidth).coerceIn(0f, 1f),
                        ((position.y - offsetY) / drawnHeight).coerceIn(0f, 1f)
                    )

                    // Observe touch events in the Initial pass so the parent verticalScroll
                    // cannot steal a brush stroke. Start immediately (no drag-slop delay).
                    awaitEachGesture {
                        val down = awaitFirstDown(
                            requireUnconsumed = false,
                            pass = PointerEventPass.Initial
                        )
                        val drawingOnImage = isInsideImage(down.position)
                        down.consume()
                        val baseStrokes = latestStrokes
                        var activeStroke = emptyList<Offset>()
                        if (drawingOnImage) {
                            activeStroke = listOf(imagePoint(down.position))
                            latestOnStrokesChange(baseStrokes + listOf(activeStroke))
                        }
                        do {
                            val event = awaitPointerEvent(PointerEventPass.Initial)
                            val change = event.changes.firstOrNull { it.id == down.id } ?: break
                            if (change.pressed) {
                                change.consume()
                                if (drawingOnImage) {
                                    activeStroke = activeStroke + imagePoint(change.position)
                                    latestOnStrokesChange(baseStrokes + listOf(activeStroke))
                                }
                            }
                        } while (change.pressed)
                    }
                }"""
if text.count(old) != 1:
    raise SystemExit("Expected unique old brush gesture block; source left unchanged")
text = text.replace(old, new, 1)
path.write_text(text, encoding="utf-8")
print("Brush touch fix applied")
