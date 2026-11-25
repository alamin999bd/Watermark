# MarkAway AI — source review

Reviewed on 2026-11-25 from the supplied v0.26.0 source ZIP.

- Static verification script: passed.
- AndroidManifest.xml: valid XML.
- Gradle compilation and APK build: not run; this environment has no Gradle executable or Android SDK.
- Image AI: LiteRT MI-GAN engine is wired in source, but the model is fetched by CI and inference has not been verified.
- Video feature: fixed-area mosaic masking only; no AI background reconstruction or moving-watermark tracking.
- Physical Android device test: not run.

The full reviewed source archive is not uploaded to this repository yet. This note does not represent an APK build.
