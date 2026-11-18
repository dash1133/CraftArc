# CraftArc VSL

The video sales letter for CraftArc: 2:13, 1920x1080, 30 fps, burned-in captions, AI voiceover. Built entirely from code, so any change to a line re-times the voice, captions and visuals together.

```
vsl/
├── CraftArc_VSL_1080p.mp4        the final video
├── CraftArc_VSL.vtt / .srt       caption files for YouTube, LinkedIn and the website
├── VSL_Script.md                 script and storyboard with timings and claim IDs (generated)
├── contact_sheet.png             one frame per sentence
├── src/
│   ├── script.py                 THE source: every line, visual and claim ID
│   ├── clean_screens.py          relabels test data in the app screens
│   ├── make_voiceover.py         offline voice (Kokoro), timeline, captions
│   ├── render_vsl.py             draws every frame and encodes the MP4
│   └── export_script.py          writes VSL_Script.md
└── assets/screens/{raw,clean}/   the six app frames, before and after cleaning
```

## Rebuild

Needs Python 3.10+, `pip install pillow numpy soundfile kokoro-onnx`, and ffmpeg. The voice model files `kokoro-v1.0.onnx` and `voices-v1.0.bin` come from the [kokoro-onnx model release](https://github.com/thewh1teagle/kokoro-onnx/releases/tag/model-files-v1.0). The voice runs offline, so the script is never sent to an outside service.

```bash
python3 vsl/src/clean_screens.py
```

```bash
KOKORO_DIR=/path/to/kokoro-models python3 vsl/src/make_voiceover.py
```

```bash
python3 vsl/src/export_script.py
```

```bash
python3 vsl/src/render_vsl.py --stills
```

```bash
python3 vsl/src/render_vsl.py --web
```

`--stills` writes one frame per sentence and a contact sheet in about 5 seconds, so you can check a change before the full render. The full render takes about 10 minutes and writes `build/CraftArc_VSL_1080p.mp4`, the 720p web cut and the poster.

## Common changes

- **Change a line.** Edit `cap` (and `say`, if the voice needs a spelling such as "Craft Arc" or "C.O.O.") in `src/script.py`. Delete `build/vo/` so the voice is regenerated, then run the steps above. Run `python3 website/tests/copy_lint.py` afterwards. It checks the VSL text too.
- **Use Dash's own voice.** Record each sentence as `build/vo/sNN_MM.wav` (24 kHz mono, numbered as in `VSL_Script.md`) and run `make_voiceover.py` and the render. Existing files are reused, not regenerated. Then remove the AI-disclosure line.
- **Change the voice.** Set `VOICE` in `src/script.py`. Kokoro voices include `af_heart` (current), `bf_emma` (British female) and `bm_george` (British male).
- **Real screens.** Replace the PNGs in `assets/screens/raw/` and re-run `clean_screens.py`. If the layout changed, update the coordinates in that script and the `focus` and `hl` boxes in `script.py`.
