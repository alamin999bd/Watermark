#!/usr/bin/env bash
# Runs inside the emulator job from source/MarkAwayAI. $1 = label (as-shipped | cpu-diagnostic)
set -uo pipefail
label="$1"; out="$GITHUB_WORKSPACE/results/$label"; mkdir -p "$out"
gradle --no-daemon -q assembleDebug assembleDebugAndroidTest || exit 1
adb install -r -g app/build/outputs/apk/debug/app-debug.apk || exit 1
adb install -r -g app/build/outputs/apk/androidTest/debug/app-debug-androidTest.apk || exit 1
for t in image video; do
  adb logcat -c
  adb shell am instrument -w -e class "com.markaway.ai.AiRemovalTest#$t" \
    com.markaway.ai.test/androidx.test.runner.AndroidJUnitRunner | tee "$out/$t-instrument.txt"
  adb logcat -d > "$out/$t-logcat.txt"
  echo "===== $label $t ====="
  grep -E "AITEST" "$out/$t-logcat.txt" | cut -c1-600 || echo "NO RESULT LINE"
  grep -E "FATAL EXCEPTION|Fatal signal|AndroidRuntime|UnsatisfiedLinkError" "$out/$t-logcat.txt" | head -20
done
for f in $(adb shell run-as com.markaway.ai ls files | tr -d '\r' | grep png); do
  adb exec-out run-as com.markaway.ai cat "files/$f" > "$out/$f"
done
video=$(adb shell ls /sdcard/Movies/MarkAway/ 2>/dev/null | tr -d '\r' | grep MarkAway_AI | tail -1)
if [ -n "$video" ]; then
  adb pull "/sdcard/Movies/MarkAway/$video" "$out/output.mp4"
  adb shell rm "/sdcard/Movies/MarkAway/$video"
  python3 "$GITHUB_WORKSPACE/ai-tests/analyze.py" "$GITHUB_WORKSPACE/clean.mp4" "$GITHUB_WORKSPACE/input.mp4" "$out/output.mp4"
else
  echo "VIDEOCHECK no output video was produced"
fi
adb uninstall com.markaway.ai.test >/dev/null; adb uninstall com.markaway.ai >/dev/null
