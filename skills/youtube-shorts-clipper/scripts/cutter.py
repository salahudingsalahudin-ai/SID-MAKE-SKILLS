#!/usr/bin/env python3
"""Step 4: cut the clips - vertical 9:16 + burned-in captions.

Usage:
    python3 cutter.py <source-video> <clips.json> --outdir clips/
               [--mode blur|crop] [--captions on|off]
               [--transform on|off] [--speed 1.0]
               [--brand "RotiAI"] [--voiceover commentary.mp3]

Transformative safety (why these exist):
  - --transform on (default): every 3 seconds the frame jumps - a new
    zoom level and a new pan position. No single shot stays unchanged
    for more than 3 seconds, so the clip never looks like a plain copy.
  - --mode blur|crop: reframes everything to vertical 9:16.
  - --brand TEXT: your own name/logo text burned on top, every frame.
  - --speed: slight speed tweak (e.g. 1.1 = 10% faster).
  - --voiceover FILE: your own commentary mixed over the original
    audio (original ducked to 35%).
  - Captions are burned in by default.

These changes make a clip transformative - a new edit, not a re-upload.
They cut the copyright risk a lot, but they are NOT a 100% guarantee:
YouTube Content ID can still claim audio/video it recognises. The
safest use is your own video, your own gameplay, your own commentary.
"""
import argparse
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, probe, read_json, words_to_srt, write_json  # noqa: E402

CAPTION_STYLE = ("FontName=DejaVu Sans,FontSize=28,PrimaryColour=&HFFFFFF&,"
                 "OutlineColour=&H000000&,BorderStyle=1,Outline=2,Shadow=0,"
                 "Alignment=2,MarginV=120")

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
]


def find_font():
    for path in FONT_CANDIDATES:
        if os.path.exists(path):
            return path
    return ""


def ffmpeg_escape(path):
    """Escape a file path for the ffmpeg subtitles filter."""
    return os.path.abspath(path).replace(":", "\\:").replace("'", "\\'")


def transform_filter():
    """Dynamic zoom + pan: the crop window moves every 3 seconds.

    ffmpeg evaluates crop w/h only once, so zoom is a fixed 1.15x
    crop-in; the motion comes from x/y, which ARE evaluated per frame:
    the pan position jumps every 3 seconds (left / center / right,
    different phase for y) with a slow drift inside each segment.
    Result: the frame is always moving and jumps every <=3s, so no
    single static shot ever lasts longer than 3 seconds.
    """
    seg = "floor(t/3)"
    x = "min(max((iw-ow)*(mod(%s,3)/2+0.08*sin(t*2)),0),iw-ow)" % seg
    y = "min(max((ih-oh)*(mod(%s+1,3)/2+0.08*cos(t*1.7)),0),ih-oh)" % seg
    return ("crop=w='iw/1.15':h='ih/1.15':x='%s':y='%s',scale=720:1280"
            % (x, y))


def build_video_filter(mode, width, height, srt_path, transform=True, brand=None,
                       speed=1.0):
    """Return a filter_complex video chain ending in [vout]."""
    if width == 720 and height == 1280:
        chain = "[0:v]scale=720:1280[v0]"
    elif mode == "crop":
        chain = "[0:v]crop=ih*9/16:ih,scale=720:1280[v0]"
    else:  # blur: full frame over a blurred background
        chain = ("[0:v]split[a][b];"
                 "[a]scale=720:1280:force_original_aspect_ratio=increase,"
                 "crop=720:1280,gblur=sigma=40[bg];"
                 "[b]scale=720:1280:force_original_aspect_ratio=decrease[fg];"
                 "[bg][fg]overlay=(W-w)/2:(H-h)/2[v0]")
    label = "v0"
    step = 0
    if transform:
        step += 1
        chain += ";[v%d]%s[v%d]" % (step - 1, transform_filter(), step)
        label = "v%d" % step
    if brand:
        font = find_font()
        if font:
            step += 1
            safe = brand.replace("'", "").replace(":", "\\:")
            chain += (";[v%d]drawtext=fontfile='%s':text='%s':fontsize=32:"
                      "fontcolor=white:borderw=2:bordercolor=black:"
                      "box=1:boxcolor=black@0.5:boxborderw=12:"
                      "x=(w-text_w)/2:y=48[v%d]" % (step - 1, font, safe, step))
            label = "v%d" % step
        else:
            print("Warning: no font found, --brand overlay skipped.")
    if speed != 1.0:
        # Speed up (or slow down) the video to match the audio atempo.
        # Must come after the crop (which uses input timestamps) and
        # before subtitles, so captions stay in sync.
        step += 1
        chain += ";[%s]setpts=PTS/%s[v%d]" % (label, speed, step)
        label = "v%d" % step
    if srt_path:
        chain += ";[%s]subtitles='%s':force_style='%s'[vout]" % (
            label, ffmpeg_escape(srt_path), CAPTION_STYLE)
    else:
        chain += ";[%s]null[vout]" % label
    return chain


def cut_clip(source, clip, out_path, mode, srt_path, has_audio,
             transform=True, speed=1.0, brand=None, voiceover=None):
    info = probe(source)
    vf = build_video_filter(mode, info["width"], info["height"], srt_path,
                            transform=transform, brand=brand, speed=speed)
    # -ss and -t are INPUT options (before -i): they must come before
    # the filter graph. An output -t breaks setpts/atempo speed changes
    # (ffmpeg stops on output timestamps, so the speedup never shows).
    inputs = ["-ss", str(clip["start"]), "-t", str(clip["duration"]), "-i", source]
    if voiceover:
        inputs += ["-i", voiceover]

    audio_filter = ""
    audio_map = []
    if voiceover:
        parts = []
        if has_audio:
            a0 = "[0:a]volume=0.35"
            if speed != 1.0:
                a0 += ",atempo=%s" % speed
            parts.append(a0 + "[a0]")
        parts.append("[1:a]volume=1.0[a1]")
        if has_audio:
            parts.append("[a0][a1]amix=inputs=2:duration=first[aout]")
            audio_map = ["-map", "[aout]"]
        else:
            parts.append("[a1]anull[aout]")
            audio_map = ["-map", "[aout]"]
        audio_filter = ";" + ";".join(parts)
    elif has_audio and speed != 1.0:
        audio_filter = ";[0:a]atempo=%s[aout]" % speed
        audio_map = ["-map", "[aout]"]
    elif has_audio:
        audio_map = ["-map", "0:a"]

    cmd = (["ffmpeg", "-y", "-v", "error"] + inputs +
           ["-filter_complex", vf + audio_filter,
            "-map", "[vout]"] + audio_map +
           ["-c:v", "libx264", "-crf", "23", "-preset", "veryfast",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart"])
    if audio_map:
        cmd += ["-c:a", "aac", "-b:a", "128k"]
    cmd += [out_path]
    print("  $ " + " ".join(cmd))
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise SystemExit("ffmpeg failed for clip #%d" % clip["rank"])
    return out_path


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Cut vertical captioned Shorts from a video.")
    parser.add_argument("source", help="Source video file")
    parser.add_argument("clips", help="clips.json from hooks.py")
    parser.add_argument("--outdir", required=True, help="Folder for finished clips")
    parser.add_argument("--mode", default="blur", choices=["blur", "crop"],
                        help="blur keeps the whole frame (gameplay), crop cuts the middle (talking head)")
    parser.add_argument("--captions", default="on", choices=["on", "off"],
                        help="Burn captions into the clips (needs transcript.json next to clips.json)")
    parser.add_argument("--transform", default="on", choices=["on", "off"],
                        help="Jump zoom/pan every 3s so no shot stays static (default: on)")
    parser.add_argument("--speed", type=float, default=1.0,
                        help="Speed tweak, e.g. 1.1 = 10%% faster (default: 1.0)")
    parser.add_argument("--brand", default="",
                        help="Your brand text burned on top, e.g. 'RotiAI'")
    parser.add_argument("--voiceover", default="",
                        help="Your own commentary audio file, mixed over the original")
    args = parser.parse_args()

    if args.speed < 0.5 or args.speed > 2.0:
        print("Speed must be between 0.5 and 2.0.")
        raise SystemExit(2)
    if args.voiceover and not os.path.isfile(args.voiceover):
        print("Voiceover file not found: %s" % args.voiceover)
        raise SystemExit(2)

    os.makedirs(args.outdir, exist_ok=True)
    clips = read_json(args.clips)
    info = probe(args.source)
    transcript = None
    transcript_path = os.path.join(os.path.dirname(os.path.abspath(args.clips)),
                                   "transcript.json")
    if args.captions == "on" and os.path.exists(transcript_path):
        transcript = read_json(transcript_path)

    done = []
    for clip in clips:
        name = "clip_%02d.mp4" % clip["rank"]
        out_path = os.path.join(args.outdir, name)
        srt_path = None
        if transcript:
            words = [w for w in transcript.get("words", [])
                     if clip["start"] <= w["start"] < clip["end"]]
            shifted = []
            for w in words:
                item = dict(w)
                # Clip-relative time, scaled by speed so captions stay
                # in sync with the sped-up/slowed video.
                item["start"] = (w["start"] - clip["start"]) / args.speed
                item["end"] = (w["end"] - clip["start"]) / args.speed
                shifted.append(item)
            srt_path = os.path.join(args.outdir, "clip_%02d.srt" % clip["rank"])
            words_to_srt(shifted, srt_path)
        print("Cutting clip #%d (%.1fs-%.1fs, transform=%s)..." % (
            clip["rank"], clip["start"], clip["end"], args.transform))
        cut_clip(args.source, clip, out_path, args.mode, srt_path, info["has_audio"],
                 transform=(args.transform == "on"), speed=args.speed,
                 brand=(args.brand or None),
                 voiceover=(args.voiceover or None))
        check = probe(out_path)
        done.append({"rank": clip["rank"], "file": out_path,
                     "title": clip["title"], "description": clip["description"],
                     "hashtags": clip["hashtags"],
                     "duration": check["duration"],
                     "width": check["width"], "height": check["height"]})
        print("  Saved: %s (%.1fs, %sx%s)" % (
            out_path, check["duration"], check["width"], check["height"]))

    meta_path = os.path.join(args.outdir, "clips_meta.json")
    write_json(meta_path, done)
    print("Saved: %s" % meta_path)


if __name__ == "__main__":
    main()
