package com.markaway.ai

import android.graphics.*
import android.net.Uri
import android.util.Log
import androidx.test.ext.junit.runners.AndroidJUnit4
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import java.io.File
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit
import kotlin.math.abs

/** Exercises the real MI-GAN image and fixed-area video engines on an emulator. */
@RunWith(AndroidJUnit4::class)
class AiRemovalTest {
    private val inst = InstrumentationRegistry.getInstrumentation()
    private val app = inst.targetContext
    private fun report(s: String) { Log.i("AITEST", s) }

    private fun clean(w: Int, h: Int): Bitmap {
        val b = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
        val c = Canvas(b)
        val p = Paint()
        p.shader = LinearGradient(0f, 0f, w.toFloat(), h.toFloat(), Color.rgb(40, 110, 160), Color.rgb(210, 170, 90), Shader.TileMode.CLAMP)
        c.drawRect(0f, 0f, w.toFloat(), h.toFloat(), p)
        p.shader = null
        p.color = Color.argb(90, 20, 60, 30)
        p.strokeWidth = 6f
        var x = -h
        while (x < w) { c.drawLine(x.toFloat(), 0f, (x + h).toFloat(), h.toFloat(), p); x += 32 }
        return b
    }

    private fun save(b: Bitmap, name: String) =
        File(app.filesDir, name).outputStream().use { b.compress(Bitmap.CompressFormat.PNG, 100, it) }

    @Test fun image() {
        for ((w, h) in listOf(512 to 512, 1280 to 720)) {
            var truth: Bitmap? = null
            var marked: Bitmap? = null
            var mask: Bitmap? = null
            var output: Bitmap? = null
            try {
                truth = clean(w, h)
                marked = truth.copy(Bitmap.Config.ARGB_8888, true)
                val box = Rect(w * 3 / 8, h * 7 / 16, w * 5 / 8, h * 9 / 16)
                val text = Paint(Paint.ANTI_ALIAS_FLAG).apply {
                    color = Color.WHITE; textSize = box.height() * 0.7f; textAlign = Paint.Align.CENTER; isFakeBoldText = true
                }
                Canvas(marked).drawText("SAMPLE", box.exactCenterX(), box.exactCenterY() + text.textSize / 3, text)
                mask = Bitmap.createBitmap(w, h, Bitmap.Config.ARGB_8888)
                Canvas(mask).apply { drawColor(Color.BLACK); drawRect(box, Paint().apply { color = Color.WHITE }) }
                val start = System.currentTimeMillis()
                output = LiteRtMiganInpaintingEngine.repair(app, marked, mask)
                val elapsed = System.currentTimeMillis() - start
                assertEquals("Output width changed", w, output.width)
                assertEquals("Output height changed", h, output.height)
                var before = 0.0; var after = 0.0; var inN = 0; var outside = 0.0; var outN = 0
                fun diff(a: Int, b: Int) = (abs(Color.red(a) - Color.red(b)) + abs(Color.green(a) - Color.green(b)) + abs(Color.blue(a) - Color.blue(b))) / 3.0
                for (y in 0 until h) for (x in 0 until w) {
                    val expected = truth.getPixel(x, y)
                    if (box.contains(x, y)) { before += diff(marked.getPixel(x, y), expected); after += diff(output.getPixel(x, y), expected); inN++ }
                    else { outside += diff(output.getPixel(x, y), marked.getPixel(x, y)); outN++ }
                }
                val beforeMean = before / inN
                val afterMean = after / inN
                val outsideMean = outside / outN
                save(marked, "image_${w}_input.png")
                save(output, "image_${w}_output.png")
                save(truth, "image_${w}_truth.png")
                report("IMAGE ${w}x${h} ms=$elapsed maskErrorBefore=%.2f maskErrorAfter=%.2f outsideMaskChange=%.2f".format(beforeMean, afterMean, outsideMean))
                assertTrue("MI-GAN did not improve the marked region at ${w}x${h}", afterMean < beforeMean)
                assertTrue("Pixels outside the mask changed excessively at ${w}x${h}: $outsideMean", outsideMean <= 3.0)
            } catch (e: Throwable) {
                report("IMAGE ${w}x${h} FAILED ${e.javaClass.name}: ${e.message}")
                throw AssertionError("Image AI validation failed for ${w}x${h}", e)
            } finally {
                listOfNotNull(output, mask, marked, truth).forEach { if (!it.isRecycled) it.recycle() }
            }
        }
    }

    @Test fun video() {
        val input = File(app.filesDir, "input.mp4")
        inst.context.assets.open("input.mp4").use { s -> input.outputStream().use { s.copyTo(it) } }
        val latch = CountDownLatch(1)
        var succeeded = false
        var completionMessage = "No completion callback received"
        val start = System.currentTimeMillis()
        VideoAiRemovalEngine.start(app, Uri.fromFile(input), 0.5f, 0.5f, 0.30f,
            onProgress = { report("VIDEO progress $it") },
            onDone = { ok, msg ->
                succeeded = ok
                completionMessage = msg
                report("VIDEO done ok=$ok ms=${System.currentTimeMillis() - start} $msg")
                latch.countDown()
            })
        assertTrue("Video AI timed out after 15 minutes", latch.await(15, TimeUnit.MINUTES))
        assertTrue("Video AI export failed: $completionMessage", succeeded)
        assertTrue("Video AI completion message did not confirm saved output", completionMessage.contains("saved", ignoreCase = true))
    }
}
