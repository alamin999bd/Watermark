# AI Removal Test Status — 2026-11-26

## Image AI (MI-GAN)
- The GitHub Actions Android emulator ran the real LiteRT MI-GAN inference engine with the pinned model asset.
- Synthetic 512x512 sample: mask-region mean error improved from 30.09 to 22.41; mean change outside the mask was 0.00.
- Synthetic 1280x720 sample: mask-region mean error improved from 23.24 to 15.28; mean change outside the mask was 1.68.
- The emulator log confirms GPU model compilation failed and the engine fell back to the XNNPACK CPU delegate.
- These results demonstrate inference on synthetic emulator test images only. They do not guarantee clean results on arbitrary user photos.

## Video AI
- The emulator processed a synthetic 3-second, 45-frame clip.
- Frame decoding, fixed-area MI-GAN frame repair, MP4 encoding and audio remux completed successfully in about 24 seconds on the emulator.
- The engine currently applies one stationary normalized rectangle to every frame. Moving-watermark tracking/keyframes and timeline editing are not implemented.
- The 20-second maximum clip duration and 1280-pixel maximum processing width are enforced by the current engine.

## Test hardening
- Earlier test logs showed the engine could report an individual test failure while the instrumentation test itself still ended with OK. The emulator test was updated on 2026-11-26 to fail the test run on image inference/quality assertions, timeout, or video export failure.
- The hardened test run is pending. Do not treat earlier test pass markers as proof that the new assertions passed.

## Not tested
- Samsung Galaxy M12 / Android 13 physical-device installation, runtime, performance, memory, heat and battery.
- Real user photos/videos and a range of codecs, resolutions, frame rates and audio tracks.
- Moving-watermark tracking, automatic edge detection and perspective correction.
- Full editor navigation, gallery workflows and all export UI paths.

## Release gate
Do not label the app a final release until the hardened emulator tests and build pass, the app's supported features and limitations are clearly disclosed, and a physical-device test report is recorded. Any unavailable feature must remain marked unavailable rather than being implied to work.
