# MarkAway AI v0.27.1 — Release Status (2026-11-26)

## Build configuration
- Package: com.markaway.ai
- Version name: 0.27.1 (kept unchanged to preserve source verification contract; Home redesign applied during CI)
- Version code: 28
- Minimum Android: API 26
- Build: GitHub Actions assembles a debug APK and uploads it as MarkAwayAI-debug-apk-v0.27.1.

## Available source features
- AI photo inpainting through the MI-GAN LiteRT engine with GPU-to-CPU fallback.
- Manual photo repair using brush masks and interpolation.
- Add text watermark to photos.
- Add logo watermark to photos with position, size, rotation and opacity controls.
- Fixed-area video inpainting: frame extraction, MI-GAN per-frame repair, MP4 encoding and source-audio remux.
- Gallery for saved MarkAway media, plus accent color and Reduce Motion settings.
- Offline operation; no account or API key required.

## Important limitations
- Video AI applies one fixed region throughout a clip. Moving-watermark tracking/keyframes are not implemented.
- Video engine currently limits clips to 20 seconds, processing width to 1280 px and frame rate to at most 30 FPS.
- No video timeline/keyframe editor or live playback preview in the editor.
- Automatic watermark detection, automatic edge detection and perspective correction are not implemented.
- AI quality varies by source media; inpainting cannot guarantee recovery of the exact original pixels.

## Test evidence and remaining gates
- Earlier emulator diagnostics processed synthetic images at 512x512 and 1280x720; mask-region error decreased in both samples. GPU compilation failed in the emulator and CPU fallback worked.
- Earlier emulator diagnostic exported a synthetic 3-second, 45-frame clip with audio mapping.
- The original test harness did not fail the instrumentation run on every internal engine error. It has now been hardened with explicit assertions; see the latest GitHub Actions emulator test run for the authoritative result.
- A successful CI build proves compilation and packaging only. It does not prove successful installation or performance on Samsung Galaxy M12.
- Physical-device test: NOT TESTED.
- Real user media compatibility: NOT TESTED.

## Release decision
This is a CI-built debug candidate, not a fully device-verified final release. A physical Android device test report is still required before claiming a fully final, verified release.
