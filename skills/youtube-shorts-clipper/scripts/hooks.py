#!/usr/bin/env python3
"""Step 3: find the best moments (hooks) in the transcript.

Usage:
    python3 hooks.py <transcript.json> --outdir work/<id> [--clips 3]
               [--min 15] [--max 60] [--llm none|gemini]

How it works (no AI key needed):
  - Splits the transcript into sentences, then scores every window of
    1-4 sentences that lasts 15-60 seconds.
  - A window scores high when its FIRST line (the hook) has a question,
    a number, a superlative ("best", "sabse"), a warning ("never",
    "mistake"), direct address ("you", "tum"), or an emotion word,
    when the speech is dense and fast, and when it ends cleanly.
  - Picks the top windows that do not overlap each other.
  - If --llm gemini and GEMINI_API_KEY is set, a Gemini model re-ranks
    the top candidates; any failure falls back to the rule scores.

Writes outdir/clips.json:
  [{rank, start, end, duration, score, hook_line, title,
    description, hashtags, text}]

If the transcript is empty (no speech), falls back to even slices
of the video so the pipeline still produces clips.
"""
import argparse
import json
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env, read_json, write_json  # noqa: E402

QUESTION_WORDS = {"what", "why", "how", "when", "where", "which", "who",
                  "kya", "kyun", "kaise", "kab", "kahan", "kaun", "kis"}
SUPERLATIVES = {"best", "top", "first", "biggest", "greatest", "only",
                "secret", "secrets", "shocking", "amazing", "unbelievable",
                "insane", "crazy", "free", "new", "sabse", "behtreen",
                "number one", "no 1", "no. 1"}
WARNING_WORDS = {"never", "don't", "dont", "stop", "mistake", "wrong",
                 "fail", "danger", "truth", "real", "lie", "fake",
                 "mat", "kabhi", "ghalti", "dhoka"}
DIRECT_WORDS = {"you", "your", "tum", "tumhara", "aap", "apko", "tu"}
EMOTION_WORDS = {"love", "hate", "wow", "oh", "god", "amazing", "incredible",
                 "kamaal", "zabardast", "wah", "haha", "lol"}
VALUE_WORDS = {"money", "price", "free", "worth", "profit", "loss",
              "paisa", "muft", "sasta", "mehnga"}
STORY_WORDS = {"story", "remember", "once", "when i", "kahani", "yaad",
               "ek dafa", "ek din"}

ALL_HOOK_WORDS = (QUESTION_WORDS | SUPERLATIVES | WARNING_WORDS |
                  DIRECT_WORDS | EMOTION_WORDS | VALUE_WORDS | STORY_WORDS)

# Virality framework, adapted from SamurAIGPT/AI-Youtube-Shorts-Generator
# (MIT) — 8 criteria. Each maps to word signals the rule scorer checks.
# The LLM re-rank (--llm gemini) uses the same 8 criteria by name.
VIRALITY_LABELS = {
    "hook": "strong opening line",
    "emotional_peak": "emotional peak",
    "opinion_bomb": "spicy / contrarian take",
    "revelation": "revelation moment",
    "conflict": "conflict / tension",
    "quotable": "quotable line",
    "story_peak": "story peak",
    "practical_value": "practical value",
}
OPINION_WORDS = {"best", "worst", "overrated", "underrated", "truth",
                 "actually", "nobody", "everyone", "sabse", "behtreen"}
REVELATION_WORDS = {"secret", "secrets", "hidden", "revealed", "wait",
                    "nobody knows", "raaz", "chhupa"}
CONFLICT_WORDS = {"vs", "versus", "fight", "wrong", "better than",
                  "worse", "disagree", "mukabla"}
QUOTABLE_STRONG = {"never", "always", "every", "nobody", "secret", "best",
                   "worst", "truth", "free"}
STORY_MARKERS = {"then", "suddenly", "finally", "ek din", "phir",
                 "remember", "story", "kahani", "yaad", "ek dafa"}
PRACTICAL_WORDS = {"how to", "kaise", "step", "tip", "trick", "free",
                   "save", "easy", "tarika", "asaan"}


def tokenize(text):
    return re.findall(r"[a-z0-9']+", text.lower())


def sentences_from(transcript):
    """Build sentences from word timestamps, snapping to . ! ? boundaries."""
    words = transcript.get("words", [])
    if not words:
        return []
    sentences = []
    current = []
    for word in words:
        current.append(word)
        if re.search(r"[.!?]", word["word"]):
            sentences.append(current)
            current = []
    if current:
        sentences.append(current)
    out = []
    for group in sentences:
        text = " ".join(w["word"].strip() for w in group).strip()
        if text:
            out.append({"start": group[0]["start"], "end": group[-1]["end"],
                        "text": text})
    return out


def score_window(window):
    """Score one candidate clip. Returns (raw_score, [reasons]).

    The FIRST sentence counts double (it is the hook — the first 1-2
    seconds a viewer hears). Each fired virality category adds a
    human-readable reason, like the reference implementation's
    `virality_reason` field.
    """
    first = window[0]["text"]
    rest = " ".join(s["text"] for s in window[1:])
    full = " ".join(s["text"] for s in window)
    first_tokens = set(tokenize(first))
    all_tokens = tokenize(full)
    all_set = set(all_tokens)
    first_lower = first.lower()
    full_lower = full.lower()
    duration = window[-1]["end"] - window[0]["start"]
    if duration <= 0:
        return 0.0, []

    score = 0.0
    fired = set()

    def hit(category, points):
        nonlocal score
        score += points
        fired.add(category)

    # Hook line (first sentence) matters most.
    if first_tokens & QUESTION_WORDS:
        hit("hook", 3.0)
    if first_tokens & SUPERLATIVES:
        hit("hook", 2.0)
    if first_tokens & WARNING_WORDS:
        hit("hook", 2.0)
    if first_tokens & DIRECT_WORDS:
        hit("hook", 1.5)
    if first_tokens & EMOTION_WORDS:
        hit("emotional_peak", 1.5)
    if re.search(r"\d", first):
        hit("hook", 2.0)  # number in the hook line
    if first.strip().endswith("?"):
        hit("hook", 2.0)
    # Rest of the clip, by virality category.
    if all_set & EMOTION_WORDS:
        hit("emotional_peak", 1.0)
    if all_set & OPINION_WORDS:
        hit("opinion_bomb", 1.5)
    if any(p in full_lower for p in REVELATION_WORDS):
        hit("revelation", 1.5)
    if any(p in full_lower for p in CONFLICT_WORDS):
        hit("conflict", 1.5)
    if len(tokenize(first)) <= 12 and (first_tokens & QUOTABLE_STRONG):
        hit("quotable", 1.5)
    if any(p in full_lower for p in STORY_MARKERS):
        hit("story_peak", 1.0)
    if any(p in full_lower for p in PRACTICAL_WORDS):
        hit("practical_value", 1.5)
    score += 0.5 * len(all_set & ALL_HOOK_WORDS)
    if re.search(r"\d", rest):
        score += 1.0
    # Speech density: natural fast speech (2.2-3.8 words/sec) keeps viewers.
    wps = len(all_tokens) / duration
    if 2.2 <= wps <= 3.8:
        score += 2.0
    elif 1.5 <= wps < 2.2:
        score += 0.5
    # Sweet-spot length for Shorts.
    if 25 <= duration <= 50:
        score += 1.5
    elif duration < 15 or duration > 60:
        score -= 2.0

    order = ["hook", "emotional_peak", "opinion_bomb", "revelation",
             "conflict", "quotable", "story_peak", "practical_value"]
    reasons = [VIRALITY_LABELS[c] for c in order if c in fired]
    return round(score, 2), reasons


def to_100(raw_score):
    """Map a raw rule score onto the familiar 0-100 scale."""
    return max(1, min(100, round(raw_score * 10)))


def make_title(hook_line, source_title=""):
    title = hook_line.strip().rstrip(".!?").strip()
    title = title[:1].upper() + title[1:] if title else "Watch this"
    if len(title) > 90:
        title = title[:87].rsplit(" ", 1)[0] + "..."
    return title


def make_hashtags(source_title):
    tags = ["Shorts"]
    words = [w for w in re.findall(r"[A-Za-z0-9]+", source_title or "")
             if len(w) > 3]
    seen = set()
    for word in words:
        tag = word[:1].upper() + word[1:]
        if tag.lower() not in seen and tag.lower() != "shorts":
            tags.append(tag)
            seen.add(tag.lower())
        if len(tags) >= 6:
            break
    return ["#" + t for t in tags]


def build_clip(window, rank, source_title):
    hook = window[0]["text"]
    raw_score, reasons = score_window(window)
    title = make_title(hook, source_title)
    tags = make_hashtags(source_title)
    description = "%s\n\n%s\n\n%s" % (
        hook, "Source: %s" % source_title if source_title else "", " ".join(tags))
    return {
        "rank": rank,
        "start": round(window[0]["start"], 2),
        "end": round(window[-1]["end"], 2),
        "duration": round(window[-1]["end"] - window[0]["start"], 2),
        "score": to_100(raw_score),
        "raw_score": raw_score,
        "reason": "; ".join(reasons) if reasons else "steady moment, clear speech",
        "hook_line": hook,
        "title": title,
        "description": description.strip(),
        "hashtags": tags,
        "text": " ".join(s["text"] for s in window),
    }


def overlaps(a_start, a_end, b_start, b_end):
    """True when two windows overlap by >50% of the shorter one
    (the reference implementation's dedupe rule)."""
    overlap = max(0.0, min(a_end, b_end) - max(a_start, b_start))
    shorter = min(a_end - a_start, b_end - b_start)
    return shorter > 0 and overlap > 0.5 * shorter


def rule_based_clips(sentences, source_title, count, min_len, max_len):
    candidates = []
    for size in range(1, 5):
        for i in range(len(sentences) - size + 1):
            window = sentences[i:i + size]
            duration = window[-1]["end"] - window[0]["start"]
            if min_len <= duration <= max_len:
                raw, _reasons = score_window(window)
                candidates.append((raw, window))
    candidates.sort(key=lambda item: item[0], reverse=True)
    picked = []
    for raw, window in candidates:
        if raw <= 0:
            continue
        start, end = window[0]["start"], window[-1]["end"]
        if any(overlaps(start, end, p["start"], p["end"]) for p in picked):
            continue
        picked.append({"start": start, "end": end, "window": window})
        if len(picked) >= count:
            break
    picked.sort(key=lambda p: p["start"])
    return [build_clip(p["window"], i + 1, source_title)
            for i, p in enumerate(picked)]


def even_slices(duration, count, min_len, max_len):
    """Fallback when there is no speech: even slices of the video."""
    if duration <= 0:
        return []
    length = max(min_len, min(max_len, duration / max(count, 1)))
    clips = []
    start = 0.0
    while len(clips) < count and start + min_len <= duration:
        end = min(start + length, duration)
        clips.append({
            "rank": len(clips) + 1,
            "start": round(start, 2), "end": round(end, 2),
            "duration": round(end - start, 2), "score": 0.0,
            "hook_line": "Clip %d" % (len(clips) + 1),
            "title": "Clip %d" % (len(clips) + 1),
            "description": "#Shorts", "hashtags": ["#Shorts"], "text": "",
        })
        start = end
    return clips


def llm_rerank(clips, transcript, source_title):
    """Optional: ask Gemini to re-rank the rule-based candidates."""
    import requests

    key = os.environ.get("GEMINI_API_KEY", "")
    if not key or not clips:
        return clips
    text = "\n".join(
        "[%d] %.1f-%.1fs: %s" % (c["rank"], c["start"], c["end"], c["text"])
        for c in clips)
    prompt = (
        "You rank short-video clips for YouTube Shorts. Score each clip "
        "0-100 for viral potential using these 8 criteria: hook (strong "
        "opening line), emotional peak, opinion bomb (spicy/contrarian "
        "take), revelation moment, conflict, quotable line, story peak, "
        "practical value. Reply ONLY with JSON:\n"
        '[{"rank": 1, "score": 85, "title": "short punchy title", '
        '"reason": "Opens with a number + regret, peaks on a contrarian lesson"}]\n\n'
        "Source video: %s\n\nClips:\n%s" % (source_title, text))
    try:
        resp = requests.post(
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent?key=" + key,
            json={"contents": [{"parts": [{"text": prompt}]}]}, timeout=60)
        resp.raise_for_status()
        raw = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        raw = raw.strip().removeprefix("```json").removeprefix("```").removesuffix("```")
        ranked = json.loads(raw)
        by_rank = {r["rank"]: r for r in ranked if "rank" in r}
        for clip in clips:
            update = by_rank.get(clip["rank"])
            if update:
                clip["score"] = float(update.get("score", clip["score"]))
                if update.get("title"):
                    clip["title"] = str(update["title"])[:90]
                if update.get("reason"):
                    clip["reason"] = str(update["reason"])
        clips.sort(key=lambda c: c["score"], reverse=True)
        for i, clip in enumerate(clips, 1):
            clip["rank"] = i
        print("LLM re-rank done (Gemini).")
    except Exception as exc:  # noqa: BLE001 - any LLM failure = keep rule scores
        print("LLM re-rank failed (%s) - keeping rule-based scores." % exc)
    return clips


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Find the best Shorts moments in a transcript.")
    parser.add_argument("transcript", help="transcript.json from transcribe.py")
    parser.add_argument("--outdir", required=True, help="Work folder for this video")
    parser.add_argument("--clips", type=int, default=3, help="How many clips (default: 3)")
    parser.add_argument("--min", type=float, default=15, help="Min clip seconds (default: 15)")
    parser.add_argument("--max", type=float, default=60, help="Max clip seconds (default: 60)")
    parser.add_argument("--llm", default="none", choices=["none", "gemini"],
                        help="Optional LLM re-rank (needs GEMINI_API_KEY)")
    parser.add_argument("--source-title", default="", help="Original video title (for titles/tags)")
    parser.add_argument("--duration", type=float, default=0,
                        help="Source video duration (for the no-speech fallback)")
    args = parser.parse_args()

    transcript = read_json(args.transcript)
    sentences = sentences_from(transcript)
    if sentences:
        clips = rule_based_clips(sentences, args.source_title, args.clips,
                                 args.min, args.max)
        if args.llm == "gemini":
            clips = llm_rerank(clips, transcript, args.source_title)
    else:
        print("No speech found - falling back to even slices.")
        clips = even_slices(args.duration or transcript.get("duration", 0),
                            args.clips, args.min, args.max)

    out = os.path.join(args.outdir, "clips.json")
    write_json(out, clips)
    print("Found %d clip(s):" % len(clips))
    for clip in clips:
        print("  #%d  %.1fs-%.1fs (%.0fs) score %.1f  |  %s" % (
            clip["rank"], clip["start"], clip["end"], clip["duration"],
            clip["score"], clip["title"]))
    print("Saved: %s" % out)


if __name__ == "__main__":
    main()
