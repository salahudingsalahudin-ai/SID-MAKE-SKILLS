#!/usr/bin/env python3
"""Step 1: get the video.

Usage:
    python3 download.py <youtube-url-or-local-file> --outdir work/<id>

- YouTube URL -> downloads with yt-dlp (max 1080p, mp4) + info JSON
  + any English captions YouTube already has (saves transcription time).
- Local file -> just checks it with ffprobe and uses it as-is.

Writes outdir/meta.json and prints its path.

Only use videos you own or have permission to clip. Re-uploading
someone else's video can get a copyright strike on your channel.
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, probe, write_json  # noqa: E402


def download_url(url, outdir):
    import yt_dlp

    os.makedirs(outdir, exist_ok=True)
    opts = {
        "format": ("bestvideo[height<=1080][ext=mp4]+bestaudio[ext=m4a]/"
                   "best[height<=1080][ext=mp4]/best"),
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(outdir, "source.%(ext)s"),
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["en.*"],
        "subtitlesformat": "vtt",
        "writeinfojson": True,
        "quiet": True,
        "no_warnings": True,
        # YouTube now needs a JS runtime to solve its challenges:
        # Node (already on Sid's PC) + the EJS solver from GitHub.
        # Without these, yt-dlp reports "Requested format is not available".
        "js_runtimes": {"node": {}},
        "remote_components": ["ejs:github"],
    }
    print("Downloading (yt-dlp, max 1080p)...")
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
    except Exception as exc:  # noqa: BLE001 - show the real yt-dlp error
        print("Download failed: %s" % exc)
        if "CERTIFICATE_VERIFY_FAILED" in str(exc):
            print("Tip: your network is intercepting HTTPS (office/school")
            print("proxy or antivirus). Try another network, or download")
            print("the video yourself and pass the local file.")
        else:
            print("Tip: YouTube sometimes blocks downloads. Try again later,")
            print("or download the video yourself and pass the local file.")
        raise SystemExit(1)
    video = os.path.join(outdir, "source.mp4")
    if not os.path.exists(video):
        found = sorted(glob.glob(os.path.join(outdir, "source.*")))
        found = [f for f in found if not f.endswith((".info.json", ".vtt"))]
        video = found[0] if found else ""
    subs = sorted(glob.glob(os.path.join(outdir, "source.*.vtt")))
    return {
        "source": url,
        "video_id": info.get("id", ""),
        "title": info.get("title", ""),
        "uploader": info.get("uploader", ""),
        "duration": info.get("duration", 0),
        "video_path": video,
        "subtitles": subs[0] if subs else None,
    }


def use_local_file(path, outdir):
    os.makedirs(outdir, exist_ok=True)
    info = probe(path)
    return {
        "source": path,
        "video_id": "",
        "title": os.path.splitext(os.path.basename(path))[0],
        "uploader": "",
        "duration": info["duration"],
        "video_path": os.path.abspath(path),
        "subtitles": None,
        "width": info["width"],
        "height": info["height"],
        "has_audio": info["has_audio"],
    }


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Download a YouTube video or use a local file.")
    parser.add_argument("input", help="YouTube URL or path to a local video file")
    parser.add_argument("--outdir", required=True, help="Work folder for this video")
    args = parser.parse_args()

    if os.path.isfile(args.input):
        meta = use_local_file(args.input, args.outdir)
    elif args.input.startswith("http"):
        meta = download_url(args.input, args.outdir)
    else:
        print("Not a file and not a URL: %s" % args.input)
        raise SystemExit(2)

    if meta.get("video_path") and os.path.exists(meta["video_path"]):
        info = probe(meta["video_path"])
        meta["width"] = info["width"]
        meta["height"] = info["height"]
        meta["has_audio"] = info["has_audio"]
        if not meta.get("duration"):
            meta["duration"] = info["duration"]
    else:
        print("Video file not found after download.")
        raise SystemExit(1)

    meta_path = os.path.join(args.outdir, "meta.json")
    write_json(meta_path, meta)
    print("Saved: %s" % meta_path)
    print("Title: %s" % meta["title"])
    print("Duration: %.1f s | Size: %sx%s | Audio: %s" % (
        meta["duration"], meta["width"], meta["height"], meta["has_audio"]))
    if meta.get("subtitles"):
        print("YouTube captions found: %s" % meta["subtitles"])


if __name__ == "__main__":
    main()
