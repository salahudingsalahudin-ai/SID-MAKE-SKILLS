---
name: youtube-seo-optimizer
description: >-
  Audit a YouTube video's title, description, tags, hashtags and chapters and
  get a 0-100 SEO score with concrete fixes and tag suggestions. Use for "check
  my title/description/tags", "why is nobody finding my video", "suggest tags",
  "SEO score", "fix my metadata", or before publishing a video or Short.
---

# YouTube SEO Optimizer

Audit video metadata locally and get a score plus fixes. No API key needed,
nothing is uploaded, no download from anywhere.

## How to use

Run the script with the video's real metadata pasted in:

```bash
python3 scripts/seo_audit.py \
  --title "Biryani = 380 calories?!" \
  --description "Daal chawal mein kitni calories hoti hain? ... rotiai.app" \
  --tags "biryani calories, desi food, weight loss pakistan" \
  --topic "biryani calories" \
  --chapters "0:00 Intro
0:08 Calories
0:20 Outro"
```

Add `--out report.csv` to also save the result as a CSV row.

## What it checks (score 0-100)

| Area | Points | Rules |
|---|---|---|
| Title | 25 | Under 100 chars (YouTube max); 60 or under shows fully; contains the main keyword; has a hook (number, question, or strong word); not ALL CAPS; not empty or vague |
| Description | 25 | At least 125 characters; main keyword in the first 150 characters (what viewers see before "more"); contains a link or call to action; keyword not stuffed (density under 5%) |
| Tags | 20 | 5-15 tags; total under 500 characters; no duplicates; covers the main keyword and topic words |
| Chapters | 15 | Timestamps in `m:ss` or `h:mm:ss` format; first chapter at 0:00; ascending order; at least 3 chapters; each at least 10 seconds long |
| Hashtags | 5 | 0-3 hashtags is best (YouTube shows the first 3 above the title); more than 15 means YouTube ignores all of them |
| Keyword use | 10 | Main keyword appears in title AND description AND tags |

## Output

- A 0-100 score plus a grade: 90+ excellent, 70-89 good, 50-69 needs work, under 50 fix before publishing.
- Each check as PASS / WARN / FAIL with one line explaining why.
- A short fix list, most important first.
- Tag suggestions built only from the video's own topic, title and
  description words — never invented tags.

## Rules

- Never invent numbers, views, or rankings. The score is about the metadata
  you pasted, not about how YouTube will rank the video — no tool can promise
  a ranking.
- Tags and keywords must come from the video's real topic. Do not add
  unrelated popular tags to chase views.
- For RotiAI videos, the main keyword is the dish + "calories" (for example
  "biryani calories"), and the description must carry the rotiai.app link.

## Note on the upstream repo

The upstream repo this skill is named after
(BankerInterface/youtube-seo-optimizer, MIT) ships only stub files and its
README points at an external "Core Update Pack" .exe download. Do not
download or run that. This skill is a clean-room implementation of the
features the README describes (SEO audit, tag suggestions, chapter check,
CSV export), written from scratch, running locally with no downloads and no
API key.
