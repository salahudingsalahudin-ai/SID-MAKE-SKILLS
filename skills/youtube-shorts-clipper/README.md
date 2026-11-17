# youtube-shorts-clipper

Turn a long YouTube video into vertical Shorts, automatically.
Paste a link → download → transcribe → find hooks → cut 9:16 clips
with captions → upload to YouTube Shorts (private by default).

Every clip is transformative by default: 9:16 reframe, dynamic
zoom/pan that jumps every 3 seconds (no shot stays static), burned
captions, plus optional brand text, speed tweak, or your own
voiceover. Short clips (15–60s) from a small slice of the source.
These cut the copyright risk a lot, but there is no 100% guarantee —
Content ID can still claim recognised audio/video, so the safest use
is your own video, gameplay, or commentary.

See `SKILL.md` for the full pipeline and `SETUP.md` for the
step-by-step setup on your PC.

## Sources & licences

Design references (ideas credited, code is original, MIT):

| Source | Licence | What it contributed |
|---|---|---|
| OpenShorts — github.com/mutonby/openshorts | MIT | Pipeline shape: ingest → transcribe → analyze → reframe → captions → export; hook overlays; MCP/REST automation idea |
| AI YouTube Shorts Generator — github.com/SamurAIGPT/AI-Youtube-Shorts-Generator | MIT | LLM virality framework (8 criteria: hook, emotional peak, opinion bomb, revelation, conflict, quotable, story peak, practical value); score + hook + reason per clip; ready-made `.claude/skills/youtube-shorts-generator` skill folder studied (chunking, >50% dedupe). Note: it uses MuAPI (cloud, paid); this skill uses free local tools instead |
| Clipper — github.com/Satish-Thapa/Clipper | MIT | Most-replayed heatmap signal; sentence-boundary snapping; title/description/hashtag writing |
| Podcast Clipper — github.com/marcuth/podcast-clipper | MIT | Gemini hook detection; word-level caption re-transcription for final cuts |
| yt-dlp — github.com/yt-dlp/yt-dlp | Unlicense | YouTube downloading |
| faster-whisper — github.com/SYSTRAN/faster-whisper | MIT | Local speech-to-text with word timestamps |
| OpenAI Whisper — github.com/openai/whisper | MIT | Transcription model family |
| google-api-python-client | Apache-2.0 | YouTube Data API v3 uploads |
| FFmpeg — ffmpeg.org | LGPL/GPL | Cutting, cropping, caption burning |

This skill's own code (`scripts/`, docs) is MIT licensed — see `LICENSE`.
