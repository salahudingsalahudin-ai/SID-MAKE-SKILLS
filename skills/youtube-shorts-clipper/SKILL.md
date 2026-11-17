---
name: youtube-shorts-clipper
description: >-
  Turn a long YouTube video into vertical Shorts automatically: paste a link
  (or a local video), the agent downloads it, transcribes the speech,
  finds the strongest hook moments, cuts 15-60 second 9:16 clips with
  burned-in captions, writes titles/descriptions/hashtags, and uploads
  them to YouTube Shorts (private by default, you publish after review).
  Use when: making Shorts/TikTok/Reels from a long video, podcast,
  gameplay or livestream; finding viral moments in a video.
license: MIT
compatibility: "Python 3.10+, FFmpeg 5+, Linux/macOS"
metadata:
  author: Sid's agent (original work, 2026)
  version: "1.0.0"
  category: video
  tags: "youtube-shorts, video-clipping, yt-dlp, whisper, ffmpeg, hooks, captions, upload"
  use-cases: "Paste a GTA 6 video link and get 3 Shorts with hooks, Make Shorts from your own long videos or livestreams, Auto-caption and reframe a video to vertical 9:16"
  agents: "claude-code, gemini-cli, cursor"
---

# YouTube Shorts Clipper — Long Video → Shorts

One command turns a long video into Shorts. Link paste karo, Shorts mil jayen ge.

## The pipeline (5 steps)

1. **Download** — `scripts/download.py` gets the video with `yt-dlp`
   (max 1080p) or uses your local file. Also grabs any English captions
   YouTube already has.
2. **Transcribe** — `scripts/transcribe.py` turns speech into text with
   word-level timestamps using `faster-whisper` (runs on your own PC,
   free, no API key).
3. **Find hooks** — `scripts/hooks.py` scores every 15–60 second window
   of the transcript: question in the first line, numbers, superlatives
   ("best", "sabse"), warnings ("never", "mistake"), direct address
   ("you", "tum"), fast dense speech. Picks the top non-overlapping
   moments and writes a title, description and hashtags for each.
   Optional: `--llm gemini` (needs `GEMINI_API_KEY`) asks Gemini to
   re-rank the candidates.
4. **Cut** — `scripts/cutter.py` cuts vertical 9:16 clips with ffmpeg.
   `blur` mode (default) keeps the whole frame over a blurred background
   — best for gameplay like GTA 6. `crop` mode cuts the middle slice —
   best for talking-head videos. Captions are burned into the video.
   **Transformative by default:** every 3 seconds the frame jumps to a
   new zoom level and pan position (`--transform on`), so no shot ever
   stays static. Add your brand (`--brand "RotiAI"`), a speed tweak
   (`--speed 1.1`) or your own commentary (`--voiceover commentary.mp3`)
   to make the clip clearly yours.
5. **Upload** — `scripts/upload.py` uploads to YouTube as a Short with
   the YouTube Data API. Privacy is **private by default** — you watch
   the Short in YouTube Studio and make it Public yourself.

Run it all at once with `scripts/clip.py`, or run each step by hand.

## Quick start

```bash
cd skills/youtube-shorts-clipper
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# One command: 3 Shorts from a video (no upload yet)
python3 scripts/clip.py "https://www.youtube.com/watch?v=VIDEO_ID" --clips 3

# With upload (needs client_secrets.json, see SETUP.md)
python3 scripts/clip.py "https://www.youtube.com/watch?v=VIDEO_ID" --clips 3 --upload

# From a local file instead of a link
python3 scripts/clip.py ~/Videos/my-video.mp4 --clips 5 --mode crop

# Apna brand + halki speed — clip aur zyada tumhara lage
python3 scripts/clip.py ~/Videos/my-video.mp4 --clips 3 --brand "RotiAI" --speed 1.1

# Apni commentary mila kar (pehle se record ki hui mp3)
python3 scripts/clip.py ~/Videos/my-video.mp4 --clips 3 --voiceover ~/commentary.mp3
```

Full step-by-step setup (including the Google Cloud part for upload)
is in `SETUP.md`. Read it once before the first upload.

## How the hook finder works

No AI key needed. It reads the transcript, splits it into sentences,
and scores every window of 1–4 sentences (15–60 seconds):

- **First line counts double** — that is the hook, the first 1–2 seconds
  a viewer hears. Questions, numbers, "best/sabse", "never/mistake",
  "you/tum" and emotion words score high.
- **Dense, fast speech** (2.2–3.8 words/second) scores higher — slow
  rambling scores low.
- **Sweet spot length** 25–50 seconds gets a bonus.
- The top windows that do not overlap are picked, earliest first.

Example hooks it loves: "What if I told you the map is twice as big?",
"Never do this mistake in GTA 6", "Ye sab se bara secret hai".

## Safe rules — clip transformative kaise bane (zaroori)

Ye skill clips ko **transformative** banata hai — matlab naya edit,
sirf copy nahi. Har clip mein ye sab hota hai:

1. **3-second rule:** koi bhi aik frame/shot 3 second se zyada same
   nahi rehta. Har 3 sec ke andar zoom ya pan badal jata hai (auto
   jump-cuts + zoom/pan, `--transform on` default hai).
2. **Transformative changes:** 9:16 reframe/crop, dynamic zoom,
   burned captions, apna brand text (`--brand`), apni commentary
   (`--voiceover`), speed tweak (`--speed 1.1`).
3. **Short clips, chhota hissa:** clip 15–60 second ka hota hai, aur
   source ka sirf chhota hissa use hota hai. Agar clips source ka 15%
   se zyada ban jayen to system warning deta hai — kam clips banao.

**No 100% guarantee:** ye tareeqe copyright ka risk BOHT kam karte
hain, lekin poori guarantee nahi hai — YouTube Content ID phir bhi
claim kar sakta hai, khas tor par pehchana jane wala audio/video.
Is liye sab se safe ye hai: **apni video, apni gameplay, apni
commentary** par use karo. Doosron ki video sirf tab jab ijazat ho.

## Rules (important)

- **Only clip videos you own or have permission to use.** Cutting
  someone else's GTA 6 video and uploading it as your Short can get a
  copyright strike or a Content ID claim on your channel. This system
  is safe for YOUR videos, YOUR gameplay, YOUR commentary. For other
  people's videos, only use clips you have rights to.
- **Review before publishing.** Uploads default to private. Watch each
  Short, check the hook and captions, then publish it yourself.
- **Never put API keys or client_secrets.json in chat, in the repo, or
  in a screenshot.** They live in your `.env` file and in
  `~/.config/youtube-shorts-clipper/` on your own PC only.
- **Titles stay honest.** The hook line comes from what is actually
  said in the clip — never invent a claim the video does not make.
- If a step fails twice, stop retrying the same way and read the error
  message — it usually says exactly what is missing.

## Files

- `scripts/clip.py` — whole pipeline in one command
- `scripts/download.py` — step 1: download (yt-dlp) or local file
- `scripts/transcribe.py` — step 2: speech to text (faster-whisper)
- `scripts/hooks.py` — step 3: find hook moments, write titles/tags
- `scripts/cutter.py` — step 4: cut 9:16 clips, burn captions
- `scripts/upload.py` — step 5: upload to YouTube Shorts
- `scripts/common.py` — shared helpers (env, ffprobe, SRT)
- `requirements.txt` — Python packages to install
- `.env.example` — copy to `.env`, fill in your own keys
- `SETUP.md` — step-by-step setup for Sid's PC
- `README.md` — where the ideas came from, with licences

## Sources (design references, all openly licensed)

- OpenShorts (MIT) — github.com/mutonby/openshorts — pipeline shape:
  ingest → transcribe → analyze → reframe → captions → export.
- AI YouTube Shorts Generator (MIT) — github.com/SamurAIGPT/AI-Youtube-Shorts-Generator —
  LLM virality framework: 8 criteria (hook, emotional peak, opinion bomb,
  revelation, conflict, quotable, story peak, practical value), each clip
  with score 0–100 + hook line + reason. Its ready-made skill folder
  `.claude/skills/youtube-shorts-generator` was also studied: long-video
  chunking (1200s windows, 60s overlap), >50% overlap dedupe,
  content-type classification. NOTE: that project uses MuAPI (cloud,
  paid per minute) for download/transcribe/ranking; this skill uses
  free local tools (yt-dlp, faster-whisper, rule scoring) instead —
  same framework idea, different engine.
- Clipper (MIT) — github.com/Satish-Thapa/Clipper — most-replayed
  heatmap idea + DeepSeek ranking + sentence-boundary snapping.
- Podcast Clipper (MIT) — github.com/marcuth/podcast-clipper — Gemini
  hook detection + word-level caption re-transcription.
- Tools used: yt-dlp (Unlicense), faster-whisper (MIT), OpenAI Whisper
  (MIT), google-api-python-client (Apache-2.0), FFmpeg (LGPL/GPL).

All code in `scripts/` is original work written for this skill, MIT
licensed (see `LICENSE`). Ideas above are credited, not copied.
