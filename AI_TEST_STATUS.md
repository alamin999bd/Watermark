# AI Removal Test Status — 2026-11-25

## Image AI (MI-GAN)
- Model card contract checked against the Kotlin adapter.
- Expected input: NCHW [1,4,512,512], channels = mask-0.5, R*mask, G*mask, B*mask.
- Expected output: NCHW [1,3,512,512], normalized [-1,1].
- Kotlin preprocessing and compositing follow this contract.
- Model binary is not present in the supplied source ZIP; CI downloads it at build time.
- Actual LiteRT inference has NOT been executed in this environment. No Android SDK/device runtime is available here.
- Therefore image removal is NOT yet verified as working.

## Video AI
- Existing video implementation exports a fixed-area mosaic cover.
- It does not run MI-GAN on video frames, track moving marks, or reconstruct the original background.
- Video AI is NOT implemented or tested.

## Required validation before claiming completion
1. Build with the licensed model asset bundled.
2. Run image inference on an Android device; save before/after test outputs and verify untouched areas remain unchanged.
3. Implement frame decode -> mask propagation/manual tracking -> MI-GAN inference per frame -> audio-preserving video encode.
4. Test short clips at multiple resolutions and frame rates; verify audio sync, memory use, export completion, and output playback.
5. Only then mark either feature complete.

No APK build or real-device test is claimed by this report.
