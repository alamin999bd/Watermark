# MarkAway AI — UI/UX ও Feature Repair Plan (v0.28.0)

এই নথি v0.27.1 source, emulator test artifacts এবং 61.16 সেকেন্ডের user screen recording পর্যালোচনা করে তৈরি। এটি implementation plan; নিচের কাজগুলো সম্পন্ন হয়েছে বলে দাবি করা হচ্ছে না।

## 1. বর্তমান সমস্যার প্রমাণ

- Home screen-এ সব প্রধান কাজের card আছে, কিন্তু কোনো bottom navigation, quick action hierarchy বা পরিষ্কার workflow নেই।
- Image picker থেকে ফিরে আসার পরে Remove screen-এ preview, brush-size control, Undo/Clear এবং Repair action আছে; কিন্তু selection/repair state ও progress feedback আরও স্পষ্ট করা দরকার।
- Video screen-এ video preview, time-range selection, keyframe/motion tracking, frame scrubber এবং export-quality options দেখা যায় না।
- Video screen-এ “AI Remove” লেখা থাকলেও current UI-তে stationary mask warning আছে; moving watermark tracking নেই।
- Gallery এবং Settings screen আছে, কিন্তু empty-state guidance ও workflow polish দুর্বল।
- Source audit অনুযায়ী auto edge detection/perspective correction নেই।
- Emulator log-এ LiteRT GPU delegate initialization ব্যর্থ হয়ে CPU fallback হয়েছে; CPU inference সফল হয়েছে। Samsung Galaxy M12-এ performance/thermal/memory test হয়নি।

## 2. Design direction

- Material 3 ভিত্তিক polished dark UI; consistent spacing, typography, accessible contrast এবং clear icon+label।
- Home: prominent “Remove from Photo” ও “Remove from Video” actions; secondary “Add Text”, “Add Logo”, “My Gallery”; bottom navigation: Home, Projects, Settings।
- প্রতিটি feature screen-এ top app bar, back navigation, clear selected-file state, help text এবং disabled/enabled button state।
- সব screen-এ loading/progress, success/error, cancel এবং retry feedback।
- Reduce Motion preference সব animated component-এ সম্মান করতে হবে।

## 3. Photo watermark removal workflow

1. Select Photo — Android Photo Picker; selected image-এর filename, dimensions এবং preview।
2. Mark Area — Brush, Eraser, Lasso/Rectangle selection, brush size, zoom/pan, Undo, Redo, Clear, Reset।
3. Preview — Original/Result comparison slider বা side-by-side toggle।
4. Repair — “Manual Repair” এবং “AI Repair” আলাদা label; model unavailable হলে স্পষ্ট error, silent fallback নয়।
5. Save — output format/quality, Save Copy, Share, Open Gallery।
6. Export failure হলে incomplete MediaStore item delete করতে হবে।

## 4. Video removal workflow

- Video preview with playback controls, timeline scrubber, current time/duration।
- Mask drawing with rectangle/brush, position/size controls এবং start/end time range।
- প্রথম release-এ fixed-area processing-কে স্পষ্টভাবে “Fixed Area AI Repair” বলতে হবে।
- Motion tracking/keyframes implement না হওয়া পর্যন্ত moving watermark support দাবি করা যাবে না।
- Export options: resolution (source/720p/1080p subject to device), FPS (source/30), quality preset, audio preserve toggle।
- Long processing-এ progress, cancel, memory/duration limit, background/foreground behavior এবং safe temporary-file cleanup।
- Source audio sync এবং output duration যাচাই করতে হবে।

## 5. Gallery & Settings

- Gallery tabs: All, Photos, Videos; search, sort newest/oldest, preview, share, delete confirmation, refresh।
- Empty state-এ “Create your first edit” action।
- Settings: theme/accent, Reduce Motion, export defaults, storage info, app version, licenses, privacy/about।

## 6. Required verification gates

- Static source validation এবং Gradle assembleDebug pass।
- Emulator UI tests: navigation, picker, brush gestures, undo/redo, save, gallery open/share/delete, video export।
- AI inference test: input/output dimensions, mask-region error improvement, outside-mask preservation, failure handling।
- Video test: fixed-mask output quality, audio sync, duration/FPS, corrupt-file check।
- Samsung Galaxy M12 Android 13: install/launch, photo import/edit/save, video import/preview/export, memory/thermal/crash checks।
- Any test not actually run must be reported as NOT TESTED.

## 7. Release rule

Do not publish a “final” APK until all P0 navigation/editor/export bugs are fixed, CI build succeeds, emulator checks pass, and physical-device test results are recorded. Moving watermark tracking, automatic edge detection and perspective correction must remain marked unavailable until implemented and tested.
