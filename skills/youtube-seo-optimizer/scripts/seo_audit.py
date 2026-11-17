#!/usr/bin/env python3
"""YouTube SEO Optimizer — audit title, description, tags, hashtags, chapters.

Local only, no API key, no network. Scores pasted metadata 0-100 and prints
fixes plus tag suggestions built from the video's own words.

Usage:
  python3 seo_audit.py --title "..." --description "..." --tags "a, b, c" \
      --topic "biryani calories" [--chapters "0:00 Intro\n0:08 Calories"] \
      [--out report.csv]
"""
import argparse
import csv
import re
import sys
from collections import Counter

HOOK_WORDS = {
    "how", "why", "what", "best", "worst", "secret", "free", "new", "top",
    "mistake", "truth", "hack", "easy", "fast", "stop", "never", "always",
    "kaise", "kyun", "kya", "sach", "asli",
}


def words(text):
    return re.findall(r"[a-zA-Z0-9\u0600-\u06FF]+", text.lower())


def check_title(title, keyword):
    pts, notes = 0, []
    t = title.strip()
    kw = keyword.lower().strip()
    if not t:
        return 0, [("FAIL", "Title is empty.")]
    if len(t) <= 100:
        pts += 6
    else:
        notes.append(("FAIL", f"Title is {len(t)} chars — YouTube cuts it at 100."))
    if len(t) <= 60:
        pts += 4
        notes.append(("PASS", "Title shows fully in search (60 chars or under)."))
    elif len(t) <= 100:
        notes.append(("WARN", "Title is over 60 chars — it will be cut off in search."))
    if kw and kw in t.lower():
        pts += 7
        notes.append(("PASS", "Main keyword is in the title."))
    else:
        notes.append(("FAIL", "Main keyword is NOT in the title."))
    ws = set(words(t))
    has_number = bool(re.search(r"\d", t))
    has_question = "?" in t
    has_hook_word = bool(ws & HOOK_WORDS)
    if has_number or has_question or has_hook_word:
        pts += 5
        notes.append(("PASS", "Title has a hook (number, question, or strong word)."))
    else:
        notes.append(("WARN", "Title has no hook — add a number or a question."))
    letters = [c for c in t if c.isalpha()]
    if letters and sum(1 for c in letters if c.isupper()) / len(letters) > 0.7:
        notes.append(("WARN", "Title is mostly ALL CAPS — YouTube may treat it as spam."))
    else:
        pts += 3
    return pts, notes


def check_description(desc, keyword):
    pts, notes = 0, []
    d = desc.strip()
    kw = keyword.lower().strip()
    if not d:
        return 0, [("FAIL", "Description is empty.")]
    if len(d) >= 125:
        pts += 7
        notes.append(("PASS", f"Description is {len(d)} chars."))
    else:
        notes.append(("WARN", f"Description is only {len(d)} chars — write at least 125."))
    first = d[:150].lower()
    if kw and kw in first:
        pts += 8
        notes.append(("PASS", "Main keyword is in the first 2 lines (seen before 'more')."))
    else:
        notes.append(("FAIL", "Main keyword is NOT in the first 2 lines of the description."))
    if re.search(r"https?://|www\.|link in|bio mein|follow karo|subscribe", d, re.I):
        pts += 5
        notes.append(("PASS", "Description has a link or call to action."))
    else:
        notes.append(("WARN", "No link or call to action in the description."))
    w = words(d)
    if w and kw:
        kw_count = d.lower().count(kw)
        dens = kw_count / max(len(w), 1) * 100
        if dens > 5:
            notes.append(("WARN", f"Keyword used {kw_count} times — looks stuffed, use it less."))
        else:
            pts += 5
    return pts, notes


def check_tags(tags, keyword):
    pts, notes = 0, []
    tag_list = [t.strip() for t in tags.split(",") if t.strip()]
    total_chars = sum(len(t) for t in tag_list)
    if 5 <= len(tag_list) <= 15:
        pts += 8
        notes.append(("PASS", f"{len(tag_list)} tags — good count."))
    elif not tag_list:
        return 0, [("FAIL", "No tags at all.")], []
    else:
        notes.append(("WARN", f"{len(tag_list)} tags — aim for 5-15."))
    if total_chars <= 500:
        pts += 4
    else:
        notes.append(("FAIL", f"Tags total {total_chars} chars — YouTube allows 500 max."))
    if len(tag_list) != len(set(t.lower() for t in tag_list)):
        notes.append(("WARN", "Duplicate tags found — remove the repeats."))
    else:
        pts += 3
    kw = keyword.lower().strip()
    joined = " ".join(tag_list).lower()
    if kw and kw in joined:
        pts += 5
        notes.append(("PASS", "Main keyword is in the tags."))
    else:
        notes.append(("FAIL", "Main keyword is NOT in the tags."))
    return pts, notes, tag_list


def check_hashtags(desc, tags):
    pts, notes = 0, []
    tags_text = (desc or "") + " " + (tags or "")
    found = re.findall(r"#\w+", tags_text)
    if not found:
        pts += 5
        notes.append(("PASS", "No hashtags — fine, they are optional."))
    elif len(found) <= 3:
        pts += 5
        notes.append(("PASS", f"{len(found)} hashtags — YouTube shows the first 3."))
    elif len(found) <= 15:
        pts += 2
        notes.append(("WARN", f"{len(found)} hashtags — only the first 3 show, keep 3-5."))
    else:
        notes.append(("FAIL", f"{len(found)} hashtags — over 15 means YouTube ignores all of them."))
    return pts, notes


def parse_chapters(text):
    out = []
    for line in (text or "").splitlines():
        m = re.match(r"\s*(\d+):(\d{2})(?::(\d{2}))?\s+(.+)", line)
        if not m:
            continue
        if m.group(3):  # h:mm:ss
            total = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
        else:  # m:ss
            total = int(m.group(1)) * 60 + int(m.group(2))
        out.append((total, m.group(4).strip()))
    return out


def check_chapters(text):
    pts, notes = 0, []
    ch = parse_chapters(text)
    if not ch:
        notes.append(("INFO", "No chapters given — add timestamps to help viewers jump."))
        return 0, notes
    if ch[0][0] == 0:
        pts += 5
        notes.append(("PASS", "First chapter starts at 0:00."))
    else:
        notes.append(("FAIL", "First chapter must start at 0:00."))
    times = [t for t, _ in ch]
    if times == sorted(times) and len(times) == len(set(times)):
        pts += 5
    else:
        notes.append(("FAIL", "Chapters are not in ascending order."))
    gaps = [b - a for a, b in zip(times, times[1:])]
    if gaps and min(gaps) < 10:
        notes.append(("FAIL", "A chapter is shorter than 10 seconds — YouTube needs 10s minimum."))
    else:
        pts += 3
    if len(ch) >= 3:
        pts += 2
        notes.append(("PASS", f"{len(ch)} chapters."))
    else:
        notes.append(("WARN", f"Only {len(ch)} chapter(s) — aim for at least 3."))
    return pts, notes


def suggest_tags(topic, title, desc, existing):
    stopwords = {
        "hain", "hai", "mein", "me", "ki", "ka", "ke", "se", "aur", "ya",
        "ko", "per", "par", "ye", "wo", "yeh", "woh", "kitni", "kitna",
        "hoti", "hota", "aaj", "hum", "the", "and", "for", "with", "from",
        "this", "that", "how", "what", "your", "you", "http", "https",
        "www", "com", "app",
    }
    pool = Counter()
    for text in (topic, title, desc):
        for w in words(text):
            if len(w) > 2 and w not in stopwords:
                pool[w] += 1
    topic_words = words(topic)
    suggestions = []
    if topic:
        suggestions.append(topic.strip().lower())
    for w in topic_words:
        if w not in suggestions:
            suggestions.append(w)
    for w, _ in pool.most_common(12):
        if w not in suggestions:
            suggestions.append(w)
    existing_low = {t.lower() for t in existing}
    return [s for s in suggestions if s.lower() not in existing_low][:8]


def grade(score):
    if score >= 90:
        return "Excellent — ready to publish."
    if score >= 70:
        return "Good — fix the FAIL items first."
    if score >= 50:
        return "Needs work — fix before publishing."
    return "Weak — fix the FAIL items before publishing."


def main():
    ap = argparse.ArgumentParser(description="Audit YouTube video metadata (0-100 SEO score).")
    ap.add_argument("--title", default="", help="Video title")
    ap.add_argument("--description", default="", help="Video description")
    ap.add_argument("--tags", default="", help="Comma-separated tags")
    ap.add_argument("--topic", default="", help="Main keyword/topic, e.g. 'biryani calories'")
    ap.add_argument("--chapters", default="", help="Chapters, one per line: '0:00 Intro'")
    ap.add_argument("--out", default="", help="Optional CSV file to save the report")
    args = ap.parse_args()

    kw = args.topic or (args.title.split()[0] if args.title else "")
    total = 0
    all_notes = []

    p, n = check_title(args.title, kw)
    total += p
    all_notes += [("Title", s, m) for s, m in n]
    p, n = check_description(args.description, kw)
    total += p
    all_notes += [("Description", s, m) for s, m in n]
    p, n, tag_list = check_tags(args.tags, kw)
    total += p
    all_notes += [("Tags", s, m) for s, m in n]
    p, n = check_hashtags(args.description, args.tags)
    total += p
    all_notes += [("Hashtags", s, m) for s, m in n]
    p, n = check_chapters(args.chapters)
    total += p
    all_notes += [("Chapters", s, m) for s, m in n]
    if kw and kw.lower() in args.title.lower() and kw.lower() in args.description.lower():
        total += 10
        all_notes.append(("Keyword", "PASS", "Main keyword is in title AND description."))
    elif kw:
        all_notes.append(("Keyword", "WARN", "Main keyword should be in title, description AND tags."))
    total = min(total, 100)

    print(f"\nYouTube SEO score: {total}/100 — {grade(total)}\n")
    for area, status, msg in all_notes:
        print(f"[{status:4}] {area}: {msg}")
    fixes = [m for _, s, m in all_notes if s == "FAIL"]
    warns = [m for _, s, m in all_notes if s == "WARN"]
    print("\nFix first:")
    for i, f in enumerate(fixes + warns, 1):
        print(f"  {i}. {f}")
    sugg = suggest_tags(args.topic, args.title, args.description, tag_list)
    if sugg:
        print("\nSuggested extra tags (from your own words):")
        print("  " + ", ".join(sugg))
    if args.out:
        with open(args.out, "w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["area", "status", "note"])
            for area, status, msg in all_notes:
                w.writerow([area, status, msg])
            w.writerow(["SCORE", total, grade(total)])
        print(f"\nSaved CSV report to {args.out}")
    return 0 if total >= 50 else 1


if __name__ == "__main__":
    sys.exit(main())
