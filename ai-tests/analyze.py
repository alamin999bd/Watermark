import json, subprocess, sys
import numpy as np

W, H = 640, 360

def probe(path):
    out = subprocess.check_output(["ffprobe", "-v", "error", "-count_frames", "-show_entries",
        "stream=codec_type,codec_name,width,height,nb_read_frames,duration", "-of", "json", path])
    return json.loads(out)["streams"]

def frames(path):
    raw = subprocess.check_output(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"])
    return np.frombuffer(raw, np.uint8).reshape(-1, H, W, 3).astype(float)

clean, marked, output = (frames(p) for p in sys.argv[1:4])
print("VIDEOCHECK input streams ", probe(sys.argv[2]))
print("VIDEOCHECK output streams", probe(sys.argv[3]))
n = min(len(clean), len(marked), len(output))
# Same rectangle as VideoAiRemovalEngine.createMask(center=0.5, width=0.30)
bw = W * 0.30; bh = bw * 0.40
mask = np.zeros((H, W), bool)
mask[int(H/2 - bh/2):int(H/2 + bh/2), int(W/2 - bw/2):int(W/2 + bw/2)] = True
print("VIDEOCHECK frames compared=%d maskErrorBefore=%.2f maskErrorAfter=%.2f outsideMaskChange=%.2f" % (
    n, np.abs(marked[:n] - clean[:n])[:, mask].mean(), np.abs(output[:n] - clean[:n])[:, mask].mean(),
    np.abs(output[:n] - marked[:n])[:, ~mask].mean()))
