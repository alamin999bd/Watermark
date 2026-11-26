from pathlib import Path
import xml.etree.ElementTree as ET

root = Path("source/MarkAwayAI")
manifest = root / "app/src/main/AndroidManifest.xml"
gradle = root / "app/build.gradle.kts"
main = root / "app/src/main/java/com/markaway/ai/MainActivity.kt"

# Give Android's launcher and app info the requested product name.
m = manifest.read_text(encoding="utf-8")
m = m.replace('android:label="MarkAway AI"', 'android:label="Watermark Remove" android:icon="@mipmap/ic_launcher" android:roundIcon="@mipmap/ic_launcher_round"')
manifest.write_text(m, encoding="utf-8")

# Retain application ID and version; only align the version label with the product release.
g = gradle.read_text(encoding="utf-8")
# No applicationId change: this is an update to the existing app, not a separate app.
gradle.write_text(g, encoding="utf-8")

# Update visible in-app brand title while retaining existing layout and features.
s = main.read_text(encoding="utf-8")
if s.count('Text("MarkAway", fontSize = 25.sp') != 1:
    raise SystemExit("Could not find the unique home header brand title")
s = s.replace('Text("MarkAway", fontSize = 25.sp', 'Text("Watermark Remove", fontSize = 22.sp')
s = s.replace('Text("AI WATERMARK STUDIO", fontSize = 10.sp', 'Text("PHOTO & VIDEO CLEANUP", fontSize = 9.sp')
main.write_text(s, encoding="utf-8")

# A crisp vector brand mark: magic-cleanup wand with sparkle, readable at launcher size.
res = root / "app/src/main/res"
(res / "drawable").mkdir(parents=True, exist_ok=True)
(res / "values").mkdir(parents=True, exist_ok=True)
(res / "mipmap-anydpi-v26").mkdir(parents=True, exist_ok=True)
brand = """<vector xmlns:android="http://schemas.android.com/apk/res/android"
    android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">
    <path android:fillColor="#22D3EE" android:pathData="M24,72 L65,31 Q68,28 71,31 L77,37 Q80,40 77,43 L36,84 Q33,87 30,84 L24,78 Q21,75 24,72 Z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M72,13 L76,24 L87,28 L76,32 L72,43 L68,32 L57,28 L68,24 Z"/>
    <path android:fillColor="#A78BFA" android:pathData="M35,17 L38,25 L46,28 L38,31 L35,39 L32,31 L24,28 L32,25 Z"/>
    <path android:fillColor="#FFFFFF" android:pathData="M86,54 L89,62 L97,65 L89,68 L86,76 L83,68 L75,65 L83,62 Z"/>
    <path android:fillColor="#0B1020" android:pathData="M18,91 L90,91 L90,96 L18,96 Z"/>
</vector>
"""
(res / "drawable" / "ic_brand_mark.xml").write_text(brand, encoding="utf-8")
(res / "values" / "ic_launcher_background.xml").write_text(
    '<resources><color name="ic_launcher_background">#0B1020</color></resources>', encoding="utf-8")
adaptive = """<adaptive-icon xmlns:android="http://schemas.android.com/apk/res/android">
    <background android:drawable="@color/ic_launcher_background"/>
    <foreground android:drawable="@drawable/ic_brand_mark"/>
</adaptive-icon>
"""
(res / "mipmap-anydpi-v26" / "ic_launcher.xml").write_text(adaptive, encoding="utf-8")
(res / "mipmap-anydpi-v26" / "ic_launcher_round.xml").write_text(adaptive, encoding="utf-8")
print("Watermark Remove app label, in-app brand title, and adaptive launcher logo added.")
