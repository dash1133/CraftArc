"""Generate the VSL voiceover offline with Kokoro (no text leaves the machine).

Writes build/vo/sNN_MM.wav per sentence, build/vo.wav (the full track) and
build/timeline.json (start and end of every sentence and scene), then the
captions as build/craftarc_vsl.vtt and build/craftarc_vsl.srt.

Model files (kokoro-v1.0.onnx, voices-v1.0.bin) come from
https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0.
Point KOKORO_DIR at the folder that holds them.
Run:  KOKORO_DIR=/path/to/models python vsl/src/make_voiceover.py
"""
import json
import os
import re
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

sys.path.insert(0, str(Path(__file__).parent))
from script import SCENES, TIMING, VOICE, caption_chunks, spoken  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "build"
SR = 24000


def trim_silence(x, thresh=0.004, pad=0.04):
    idx = np.where(np.abs(x) > thresh)[0]
    if len(idx) == 0:
        return x
    a = max(idx[0] - int(pad * SR), 0)
    b = min(idx[-1] + int(pad * SR), len(x))
    return x[a:b]


def ts(t, sep="."):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}".replace(".", sep)


def main():
    kokoro = None

    def tts(text):
        nonlocal kokoro
        if kokoro is None:  # loaded only when a sentence has no recording yet
            from kokoro_onnx import Kokoro
            kdir = Path(os.environ.get("KOKORO_DIR", "."))
            kokoro = Kokoro(str(kdir / "kokoro-v1.0.onnx"), str(kdir / "voices-v1.0.bin"))
        return kokoro.create(text, voice=VOICE["voice"], speed=VOICE["speed"], lang=VOICE["lang"])

    (BUILD / "vo").mkdir(parents=True, exist_ok=True)

    track, t, timeline = [], 0.0, {"scenes": [], "sentences": []}

    def silence(sec):
        nonlocal t
        track.append(np.zeros(int(round(sec * SR)), dtype=np.float32))
        t += sec

    for si, sc in enumerate(SCENES):
        scene_start = t
        silence(TIMING["scene_lead"])
        for ti, s in enumerate(sc["sentences"]):
            if ti:
                silence(TIMING["gap"])
            wav_path = BUILD / "vo" / f"s{si:02d}_{ti:02d}.wav"
            if not wav_path.exists():
                audio, sr = tts(spoken(s))
                assert sr == SR, sr
                sf.write(wav_path, trim_silence(audio.astype(np.float32)), SR)
            audio, file_sr = sf.read(wav_path, dtype="float32")
            if audio.ndim > 1:
                audio = audio.mean(axis=1)
            if file_sr != SR:
                raise SystemExit(f"{wav_path.name} is {file_sr} Hz; record or convert it to {SR} Hz mono")
            start = t
            track.append(audio)
            t += len(audio) / SR
            timeline["sentences"].append({"scene": si, "idx": ti, "start": round(start, 3), "end": round(t, 3),
                                          "cap": s["cap"], "words": len(spoken(s).split())})
        silence(TIMING["scene_tail"])
        timeline["scenes"].append({"id": sc["id"], "start": round(scene_start, 3), "end": round(t, 3)})

    full = np.concatenate(track)
    peak = np.abs(full).max()
    full = full / peak * 0.89  # headroom; final loudness is set in the ffmpeg mux
    sf.write(BUILD / "vo.wav", full, SR)
    timeline["duration"] = round(t, 3)
    (BUILD / "timeline.json").write_text(json.dumps(timeline, indent=1))

    # Captions: split long sentences into chunks timed by character share.
    vtt, srt, n = ["WEBVTT", ""], [], 0
    for s in timeline["sentences"]:
        chunks = ["\n".join(c) for c in caption_chunks(s["cap"])]
        total = sum(len(c) for c in chunks)
        c0 = s["start"]
        for c in chunks:
            c1 = c0 + (s["end"] - s["start"]) * len(c) / total
            n += 1
            vtt += [f"{ts(c0)} --> {ts(c1)}", c, ""]
            srt += [str(n), f"{ts(c0, ',')} --> {ts(c1, ',')}", c, ""]
            c0 = c1
    (BUILD / "craftarc_vsl.vtt").write_text("\n".join(vtt))
    (BUILD / "craftarc_vsl.srt").write_text("\n".join(srt))
    words = sum(s["words"] for s in timeline["sentences"])
    print(f"voiceover {t:.1f}s, {words} words, {words / t * 60:.0f} wpm overall, {n} caption cues")


if __name__ == "__main__":
    main()
