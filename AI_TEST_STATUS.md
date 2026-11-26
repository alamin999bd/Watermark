# AI Removal Test Status — 2026-11-26

## Hardened Android emulator test: PASS
GitHub Actions run #3 completed successfully:
https://github.com/alamin999bd/Watermark/actions/runs/45771847781

The test harness now fails the instrumentation test when image inference/quality assertions fail, when video export times out, or when the video engine reports failure.

### Image AI (MI-GAN)
- Synthetic 512x512 sample: mask-region mean error improved from 30.09 to 22.41; mean change outside the mask was 0.00.
- Synthetic 1280x720 sample: mask-region mean error improved from 23.24 to 15.28; mean change outside the mask was 1.68.
- Both sizes passed the explicit assertions: mask-region error improved and outside-mask change stayed at or below 3.0.
- GPU model compilation failed in the emulator; the XNNPACK CPU fallback completed inference.
- These are synthetic emulator samples, not guarantees for arbitrary user photos.

### Video AI
- A synthetic 3-second, 45-frame clip completed fixed-area per-frame MI-GAN repair, MP4 encoding and audio remux in approximately 30.2 seconds on the emulator.
- Both as-shipped and CPU-diagnostic runs passed the explicit success and timeout assertions.
- The engine applies one fixed rectangle to every frame. Moving-watermark tracking/keyframes are not implemented.
- Current engine limits: 20-second clips, processing width up to 1280 pixels, and frame rate up to 30 FPS.

## Not tested
- Samsung Galaxy M12 / Android 13 physical-device installation, runtime, performance, memory, heat and battery.
- Real user photos/videos and a broad range of codecs, resolutions, frame rates and audio tracks.
- Moving-watermark tracking, automatic edge detection and perspective correction.
- Full manual UI walkthrough across every navigation, gallery and export path.

## Release gate
CI build and hardened emulator AI tests pass, but physical-device testing remains NOT TESTED. Do not describe the app as fully device-verified until a Samsung Galaxy M12 test report is recorded. Keep unavailable features clearly labelled.
