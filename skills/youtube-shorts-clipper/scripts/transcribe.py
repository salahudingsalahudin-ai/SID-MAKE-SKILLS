#!/usr/bin/env python3
"""Step 2: speech -> text with word timestamps (faster-whisper, local, free).

Usage:
    python3 transcribe.py <video-or-audio> --outdir work/<id> [--model tiny]

- Extracts audio to 16 kHz mono WAV, runs faster-whisper (tiny model
  by default: fast on CPU, no GPU needed), writes:
    transcript.json  - segments + every word with start/end times
    transcript.srt   - caption lines for the whole video
- If the video has no audio, writes an empty transcript and exits 0
  (the hook finder then falls back to even time slices).
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, probe, run, words_to_srt, write_json  # noqa: E402


def extract_audio(video, wav):
    run(["ffmpeg", "-y", "-v", "error", "-i", video,
         "-vn", "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", wav])


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Transcribe a video's speech to text.")
    parser.add_argument("input", help="Video or audio file")
    parser.add_argument("--outdir", required=True, help="Work folder for this video")
    parser.add_argument("--model", default="tiny",
                        help="Whisper model size: tiny (fastest), base, small (default: tiny)")
    parser.add_argument("--language", default=None,
                        help="Spoken language code, e.g. en, ur (default: auto-detect)")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)
    info = probe(args.input)
    transcript_path = os.path.join(args.outdir, "transcript.json")
    srt_path = os.path.join(args.outdir, "transcript.srt")

    if not info["has_audio"]:
        print("No audio track - writing an empty transcript.")
        write_json(transcript_path, {"language": "", "duration": info["duration"],
                                     "segments": [], "words": []})
        open(srt_path, "w", encoding="utf-8").close()
        print("Saved: %s (empty)" % transcript_path)
        return

    wav = os.path.join(args.outdir, "audio.wav")
    print("Extracting audio...")
    extract_audio(args.input, wav)

    # Decode the WAV ourselves (stdlib wave + numpy) and pass raw samples
    # to Whisper. This avoids faster-whisper's av-based decoder, which
    # breaks with newer PyAV versions.
    import wave

    import numpy as np

    with wave.open(wav, "rb") as handle:
        channels = handle.getnchannels()
        rate = handle.getframerate()
        frames = handle.readframes(handle.getnframes())
    audio = np.frombuffer(frames, dtype=np.int16).astype(np.float32) / 32768.0
    if channels == 2:
        audio = audio.reshape(-1, 2).mean(axis=1)
    if rate != 16000:
        print("Warning: audio is %d Hz, expected 16000 - results may suffer." % rate)

    from faster_whisper import WhisperModel

    print("Transcribing with faster-whisper (%s, CPU int8)..." % args.model)
    print("First run downloads the model (~75 MB for tiny) - one time only.")
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    segments, detected = model.transcribe(
        audio, word_timestamps=True, vad_filter=True, language=args.language)
    language = detected.language if hasattr(detected, "language") else ""
    all_segments = []
    all_words = []
    for seg in segments:
        words = [{"start": w.start, "end": w.end, "word": w.word}
                 for w in (seg.words or [])]
        all_segments.append({"start": seg.start, "end": seg.end,
                             "text": seg.text.strip()})
        all_words.extend(words)

    write_json(transcript_path, {"language": language, "duration": info["duration"],
                                 "segments": all_segments, "words": all_words})
    count = words_to_srt(all_words, srt_path)
    print("Language: %s | Segments: %d | Words: %d | Caption lines: %d" % (
        language, len(all_segments), len(all_words), count))
    print("Saved: %s" % transcript_path)
    print("Saved: %s" % srt_path)


if __name__ == "__main__":
    main()
