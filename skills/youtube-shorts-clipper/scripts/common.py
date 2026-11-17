"""Shared helpers for youtube-shorts-clipper.

Kept dependency-free (only the standard library) so every script
can import this file without extra installs.
"""
import json
import os
import subprocess


def load_env(path=".env"):
    """Tiny .env reader (KEY=VALUE lines). No dependency needed."""
    if not os.path.exists(path):
        return
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


def run(cmd, check=True):
    """Run a command, print it, fail loudly on error."""
    print("  $ " + " ".join(str(c) for c in cmd))
    result = subprocess.run(cmd)
    if check and result.returncode != 0:
        raise SystemExit("Command failed (%s): %s" % (result.returncode, " ".join(str(c) for c in cmd)))
    return result


def probe(path):
    """ffprobe: return width, height, duration (seconds), has_audio."""
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height",
         "-show_entries", "format=duration",
         "-of", "json", path],
        capture_output=True, text=True)
    data = json.loads(out.stdout or "{}")
    streams = data.get("streams", [{}])
    fmt = data.get("format", {})
    audio = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "a",
         "-show_entries", "stream=index", "-of", "csv=p=0", path],
        capture_output=True, text=True)
    return {
        "width": streams[0].get("width", 0),
        "height": streams[0].get("height", 0),
        "duration": float(fmt.get("duration", 0) or 0),
        "has_audio": bool(audio.stdout.strip()),
    }


def write_json(path, data):
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as handle:
        json.dump(data, handle, ensure_ascii=False, indent=2)


def read_json(path):
    with open(path, encoding="utf-8") as handle:
        return json.load(handle)


def seconds_to_srt(t):
    """Seconds (float) -> SRT timestamp 'HH:MM:SS,mmm'."""
    ms = int(round(t * 1000))
    hours, ms = divmod(ms, 3600000)
    minutes, ms = divmod(ms, 60000)
    seconds, ms = divmod(ms, 1000)
    return "%02d:%02d:%02d,%03d" % (hours, minutes, seconds, ms)


def words_to_srt(words, path, max_words=6, max_gap=0.6, max_span=2.0):
    """Group word timestamps into short caption lines and write an SRT file.

    words: list of {"start": float, "end": float, "word": str}.
    Returns the number of caption lines written.
    """
    lines = []
    current = []
    for word in words:
        text = word["word"].strip()
        if not text:
            continue
        if current:
            gap = word["start"] - current[-1]["end"]
            span = word["end"] - current[0]["start"]
            if gap > max_gap or len(current) >= max_words or span > max_span:
                lines.append(current)
                current = []
        current.append(word)
    if current:
        lines.append(current)
    with open(path, "w", encoding="utf-8") as handle:
        for i, line in enumerate(lines, 1):
            handle.write("%d\n%s --> %s\n%s\n\n" % (
                i,
                seconds_to_srt(line[0]["start"]),
                seconds_to_srt(line[-1]["end"]),
                " ".join(w["word"].strip() for w in line),
            ))
    return len(lines)
