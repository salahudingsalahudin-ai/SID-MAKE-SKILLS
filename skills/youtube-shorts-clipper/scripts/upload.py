#!/usr/bin/env python3
"""Step 5: upload a clip to YouTube as a Short.

Usage:
    python3 upload.py <clip.mp4> --title "..." --description "..."
               [--tags a,b,c] [--category 22] [--privacy private]
               [--dry-run]

- First run opens your browser once (Google sign-in) and saves a
  token to ~/.config/youtube-shorts-clipper/token.json, so later
  uploads need no browser.
- Default privacy is PRIVATE: you review the Short in YouTube Studio
  and make it Public yourself. Pass --privacy public to publish at once.
- Needs a client_secrets.json from YOUR OWN Google Cloud project
  (YouTube Data API v3 enabled). Path: YT_CLIENT_SECRETS env var,
  ./client_secrets.json, or ~/.config/youtube-shorts-clipper/.
  NEVER put secrets in this repo or in chat.
- --dry-run checks everything (file, title length, secrets present)
  without uploading anything.
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import load_env  # noqa: E402

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
TOKEN_DIR = os.path.expanduser("~/.config/youtube-shorts-clipper")
TOKEN_FILE = os.path.join(TOKEN_DIR, "token.json")


def find_secrets():
    candidates = [
        os.environ.get("YT_CLIENT_SECRETS", ""),
        os.path.join(os.getcwd(), "client_secrets.json"),
        os.path.join(TOKEN_DIR, "client_secrets.json"),
    ]
    for path in candidates:
        if path and os.path.exists(path):
            return path
    return ""


def get_service():
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    secrets = find_secrets()
    if not secrets:
        print("client_secrets.json not found.")
        print("Get one from your Google Cloud project (YouTube Data API v3")
        print("enabled, OAuth client ID for a Desktop app), then put it in")
        print("this folder or set YT_CLIENT_SECRETS=/path/to/client_secrets.json")
        raise SystemExit(1)
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            print("Opening your browser for Google sign-in (first run only)...")
            flow = InstalledAppFlow.from_client_secrets_file(secrets, SCOPES)
            creds = flow.run_local_server(port=0)
        os.makedirs(TOKEN_DIR, exist_ok=True)
        with open(TOKEN_FILE, "w", encoding="utf-8") as handle:
            handle.write(creds.to_json())
        print("Login saved to %s" % TOKEN_FILE)
    return build("youtube", "v3", credentials=creds)


def main():
    load_env()
    parser = argparse.ArgumentParser(description="Upload a clip as a YouTube Short.")
    parser.add_argument("video", help="Clip file, e.g. clips/clip_01.mp4")
    parser.add_argument("--title", required=True, help="Short title (max 100 chars)")
    parser.add_argument("--description", default="", help="Description (max 5000 chars)")
    parser.add_argument("--tags", default="Shorts",
                        help="Comma-separated tags (default: Shorts)")
    parser.add_argument("--category", default="22",
                        help="YouTube category id (22 People & Blogs, 20 Gaming, 24 Entertainment)")
    parser.add_argument("--privacy", default="private",
                        choices=["private", "unlisted", "public"],
                        help="Default: private - you publish it yourself after review")
    parser.add_argument("--dry-run", action="store_true",
                        help="Check everything, upload nothing")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        print("File not found: %s" % args.video)
        raise SystemExit(2)
    if len(args.title) > 100:
        print("Title too long (%d chars, max 100): %s" % (len(args.title), args.title))
        raise SystemExit(2)
    if len(args.description) > 5000:
        print("Description too long (max 5000 chars).")
        raise SystemExit(2)

    if args.dry_run:
        print("DRY RUN - everything checks out, nothing uploaded:")
        print("  File: %s" % args.video)
        print("  Title: %s" % args.title)
        print("  Tags: %s | Category: %s | Privacy: %s" % (
            args.tags, args.category, args.privacy))
        print("  Secrets file: %s" % (find_secrets() or "NOT FOUND (needed for real upload)"))
        return

    from googleapiclient.http import MediaFileUpload

    service = get_service()
    body = {
        "snippet": {
            "title": args.title,
            "description": args.description,
            "tags": [t.strip() for t in args.tags.split(",") if t.strip()],
            "categoryId": args.category,
        },
        "status": {"privacyStatus": args.privacy},
    }
    print("Uploading: %s" % args.video)
    request = service.videos().insert(
        part="snippet,status", body=body,
        media_body=MediaFileUpload(args.video, chunksize=-1, resumable=True))
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print("  Uploaded %d%%" % int(status.progress() * 100))
    video_id = response["id"]
    url = "https://www.youtube.com/shorts/" + video_id
    print("Uploaded! %s (privacy: %s)" % (url, args.privacy))
    print("Video ID: %s" % video_id)


if __name__ == "__main__":
    main()
