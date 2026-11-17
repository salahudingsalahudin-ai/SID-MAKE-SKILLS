#!/usr/bin/env python3
"""YouTube long video -> Shorts. One command, whole pipeline.

Usage:
    python3 clip.py <youtube-url-or-local-file> [--clips 3]
               [--model tiny] [--mode blur|crop] [--captions on|off]
               [--llm none|gemini] [--upload] [--privacy private]
               [--category 22] [--outdir work/<name>]

What it does, step by step:
  1. download.py  - gets the video (yt-dlp) or uses your local file
  2. transcribe.py - speech to text with word timestamps (faster-whisper)
  3. hooks.py     - finds the best 15-60s moments (hook scoring)
  4. cutter.py    - cuts vertical 9:16 clips with burned captions,
                    dynamic zoom/pan every 3s (transformative by default)
  5. upload.py    - (only with --upload) uploads to YouTube as Shorts,
                    PRIVATE by default so you review first

Without --upload it stops after cutting and prints the clip list.
Run from this skill's scripts/ folder, or pass full paths.

Only clip videos you own or have permission to use. Re-uploading
someone else's video can get a copyright strike on your channel.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, read_json  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))


def step(name, cmd):
    print("\n=== %s ===" % name)
    result = subprocess.run([sys.executable] + cmd)
    if result.returncode != 0:
        print("FAILED at step: %s" % name)
        raise SystemExit(result.returncode)


def main():
    load_env()
    parser = argparse.ArgumentParser(
        description="Turn a long YouTube video into vertical Shorts.")
    parser.add_argument("input", help="YouTube URL or local video file")
    parser.add_argument("--clips", type=int, default=3, help="How many Shorts (default: 3)")
    parser.add_argument("--model", default="tiny", help="Whisper model: tiny, base, small")
    parser.add_argument("--mode", default="blur", choices=["blur", "crop"],
                        help="blur keeps the whole frame (gameplay), crop cuts the middle")
    parser.add_argument("--captions", default="on", choices=["on", "off"])
    parser.add_argument("--transform", default="on", choices=["on", "off"],
                        help="Jump zoom/pan every 3s so no shot stays static (default: on)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speed tweak, e.g. 1.1 = 10%% faster (default: 1.0)")
    parser.add_argument("--brand", default="",
                        help="Your brand text burned on top, e.g. 'RotiAI'")
    parser.add_argument("--voiceover", default="",
                        help="Your own commentary audio file, mixed over the original")
    parser.add_argument("--llm", default="none", choices=["none", "gemini"],
                        help="Optional Gemini re-rank (needs GEMINI_API_KEY)")
    parser.add_argument("--min", type=float, default=15, help="Min clip seconds (default: 15)")
    parser.add_argument("--max", type=float, default=60, help="Max clip seconds (default: 60)")
    parser.add_argument("--upload", action="store_true", help="Upload the finished clips")
    parser.add_argument("--privacy", default="private",
                        choices=["private", "unlisted", "public"])
    parser.add_argument("--category", default="22",
                        help="YouTube category (22 People & Blogs, 20 Gaming)")
    parser.add_argument("--outdir", default="",
                        help="Work folder (default: work/<video name>)")
    args = parser.parse_args()

    base = os.path.splitext(os.path.basename(args.input.rstrip("/")))[0]
    base = "".join(c if c.isalnum() or c in "-_" else "_" for c in base) or "video"
    outdir = args.outdir or os.path.join("work", base[:40])
    clips_dir = os.path.join(outdir, "clips")
    os.makedirs(outdir, exist_ok=True)

    step("1/5 Download", [os.path.join(HERE, "download.py"), args.input,
                          "--outdir", outdir])
    meta = read_json(os.path.join(outdir, "meta.json"))

    step("2/5 Transcribe", [os.path.join(HERE, "transcribe.py"), meta["video_path"],
                            "--outdir", outdir, "--model", args.model])

    step("3/5 Find hooks", [os.path.join(HERE, "hooks.py"),
                            os.path.join(outdir, "transcript.json"),
                            "--outdir", outdir, "--clips", str(args.clips),
                            "--min", str(args.min), "--max", str(args.max),
                            "--llm", args.llm,
                            "--source-title", meta.get("title", ""),
                            "--duration", str(meta.get("duration", 0))])

    step("4/5 Cut clips", [os.path.join(HERE, "cutter.py"), meta["video_path"],
                           os.path.join(outdir, "clips.json"),
                           "--outdir", clips_dir, "--mode", args.mode,
                           "--captions", args.captions,
                           "--transform", args.transform,
                           "--speed", str(args.speed),
                           "--brand", args.brand,
                           "--voiceover", args.voiceover])

    clips = read_json(os.path.join(clips_dir, "clips_meta.json"))
    total_used = sum(c["duration"] for c in clips)
    source_len = meta.get("duration", 0) or 0
    if source_len > 0:
        pct = 100.0 * total_used / source_len
        print("\nSource used: %.0fs of %.0fs (%.0f%%) - keep it a small slice." % (
            total_used, source_len, pct))
        if pct > 15:
            print("Warning: clips use more than 15%% of the source. Use fewer")
            print("clips (--clips 2) or shorter ones to stay clearly transformative.")
    report = ["# Shorts report: %s" % meta.get("title", base), ""]
    for clip in clips:
        report.append("## Clip #%d - %s" % (clip["rank"], clip["title"]))
        report.append("- File: %s" % clip["file"])
        report.append("- Duration: %.1fs, Size: %sx%s" % (
            clip["duration"], clip["width"], clip["height"]))
        report.append("")

    if args.upload:
        print("\n=== 5/5 Upload (%d clip(s)) ===" % len(clips))
        for clip in clips:
            print("\nUploading clip #%d: %s" % (clip["rank"], clip["title"]))
            result = subprocess.run([
                sys.executable, os.path.join(HERE, "upload.py"), clip["file"],
                "--title", clip["title"],
                "--description", clip["description"],
                "--tags", ",".join(t.lstrip("#") for t in clip["hashtags"]),
                "--category", args.category, "--privacy", args.privacy])
            if result.returncode != 0:
                print("Upload failed for clip #%d - the finished file is still in %s"
                      % (clip["rank"], clips_dir))
    else:
        print("\nDone! %d clip(s) ready in %s" % (len(clips), clips_dir))
        print("Review them, then upload with --upload, or upload by hand")
        print("from YouTube Studio. Default upload privacy is private.")

    report_path = os.path.join(outdir, "report.md")
    with open(report_path, "w", encoding="utf-8") as handle:
        handle.write("\n".join(report))
    print("Report: %s" % report_path)


if __name__ == "__main__":
    main()
