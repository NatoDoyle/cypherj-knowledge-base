"""
Substack Scraper → Markdown Knowledge Base
===========================================
Scrapes all public posts from cypherj.substack.com (Justin Scott)
and saves each one as a clean Markdown file.

Usage:
    pip install requests beautifulsoup4 markdownify
    python scrape_substack.py

Output:
    ./knowledge_base/
        2026-03-24_the-mechanism-of-terror.md
        2026-03-17_boundaries-dont-protect-you.md
        ...
"""

import os
import re
import time
import json
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from datetime import datetime

# ── Config ──────────────────────────────────────────────────────────
SUBSTACK_SLUG = "cypherj"
BASE_URL = f"https://{SUBSTACK_SLUG}.substack.com"
OUTPUT_DIR = "./knowledge_base"
BATCH_SIZE = 12          # posts per API call
DELAY_BETWEEN = 1.0      # seconds between requests (be polite)
# ────────────────────────────────────────────────────────────────────

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "application/json",
}


def get_all_post_metadata() -> list[dict]:
    """Fetch metadata for all posts via the archive API."""
    all_posts = []
    offset = 0

    print("📡 Fetching post list...")
    while True:
        url = f"{BASE_URL}/api/v1/archive?sort=new&limit={BATCH_SIZE}&offset={offset}"
        resp = requests.get(url, headers=HEADERS)

        if resp.status_code != 200:
            print(f"  ⚠️  Got status {resp.status_code} at offset {offset}, stopping.")
            break

        batch = resp.json()
        if not batch:
            break

        all_posts.extend(batch)
        print(f"  ✓ Fetched {len(all_posts)} posts so far...")
        offset += BATCH_SIZE
        time.sleep(DELAY_BETWEEN)

    print(f"📋 Total posts found: {len(all_posts)}\n")
    return all_posts


def fetch_post_content(post: dict) -> str | None:
    """Fetch the full HTML body of a single post."""
    slug = post.get("slug", "")
    canonical_url = post.get("canonical_url", f"{BASE_URL}/p/{slug}")

    try:
        resp = requests.get(canonical_url, headers={
            **HEADERS,
            "Accept": "text/html",
        })
        if resp.status_code != 200:
            return None

        soup = BeautifulSoup(resp.text, "html.parser")

        # Substack wraps post body in a div with class "body markup"
        body = soup.find("div", class_="body")
        if not body:
            # Fallback: try finding the available-content div
            body = soup.find("div", class_="available-content")
        if not body:
            return None

        # Remove subscription CTAs, share buttons, etc.
        for unwanted in body.find_all(["div", "section"], class_=lambda c: c and any(
            x in (c if isinstance(c, str) else " ".join(c))
            for x in ["subscription-widget", "share", "footer", "button-wrapper",
                       "paywall", "subscribe-widget", "post-footer"]
        )):
            unwanted.decompose()

        return str(body)

    except Exception as e:
        print(f"  ⚠️  Error fetching {slug}: {e}")
        return None


def html_to_markdown(html: str) -> str:
    """Convert HTML to clean Markdown."""
    markdown = md(html, heading_style="ATX", bullets="-", strip=["img"])

    # Clean up excessive whitespace
    markdown = re.sub(r"\n{3,}", "\n\n", markdown)
    markdown = markdown.strip()

    return markdown


def sanitize_filename(text: str) -> str:
    """Create a safe filename from a string."""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text[:80].strip("-")


def save_post(post: dict, content_md: str):
    """Save a single post as a Markdown file with frontmatter."""
    title = post.get("title", "Untitled")
    subtitle = post.get("subtitle", "")
    date_str = post.get("post_date", post.get("published_at", ""))
    slug = post.get("slug", "untitled")
    url = post.get("canonical_url", f"{BASE_URL}/p/{slug}")
    word_count = post.get("wordcount", len(content_md.split()))

    # Parse date for filename
    try:
        dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
        date_prefix = dt.strftime("%Y-%m-%d")
        date_display = dt.strftime("%B %d, %Y")
    except (ValueError, AttributeError):
        date_prefix = "undated"
        date_display = "Unknown date"

    filename = f"{date_prefix}_{sanitize_filename(slug)}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    # Build the markdown file
    lines = [
        f"# {title}",
        "",
    ]
    if subtitle:
        lines += [f"*{subtitle}*", ""]

    lines += [
        f"**Author:** Justin Scott",
        f"**Date:** {date_display}",
        f"**Source:** [{url}]({url})",
        f"**Word count:** ~{word_count}",
        "",
        "---",
        "",
        content_md,
    ]

    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    return filename


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Step 1: Get all post metadata
    posts = get_all_post_metadata()

    if not posts:
        print("❌ No posts found. The API structure may have changed.")
        print("   Try the RSS fallback: curl https://cypherj.substack.com/feed")
        return

    # Build set of existing files to skip duplicates — scan themed folders + staging
    existing_files = set()
    scan_dirs = [OUTPUT_DIR, "Psychology", "Relationships", "Politics",
                 "Spirituality", "Frameworks", "Race & Culture"]
    for d in scan_dirs:
        if os.path.isdir(d):
            for f in os.listdir(d):
                if f.endswith(".md"):
                    existing_files.add(f)
    print(f"📂 Found {len(existing_files)} existing files\n")

    # Step 2: Fetch and save each post
    saved = 0
    skipped = 0
    already_existed = 0

    for i, post in enumerate(posts, 1):
        title = post.get("title", "Untitled")
        slug = post.get("slug", "")
        is_paid = post.get("audience", "") == "only_paid"

        # Skip paid-only posts (can't access full content)
        if is_paid:
            print(f"  [{i}/{len(posts)}] 🔒 Skipping paid post: {title}")
            skipped += 1
            continue

        # Check if this post already exists
        date_str = post.get("post_date", post.get("published_at", ""))
        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_prefix = dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            date_prefix = "undated"
        expected_filename = f"{date_prefix}_{sanitize_filename(slug)}.md"

        if expected_filename in existing_files:
            print(f"  [{i}/{len(posts)}] ⏭️  Already exists: {title}")
            already_existed += 1
            continue

        print(f"  [{i}/{len(posts)}] 📥 Downloading: {title}")

        html_content = fetch_post_content(post)
        if not html_content:
            print(f"           ⚠️  Could not fetch content, skipping.")
            skipped += 1
            continue

        content_md = html_to_markdown(html_content)
        if not content_md or len(content_md) < 50:
            print(f"           ⚠️  Content too short/empty, skipping.")
            skipped += 1
            continue

        filename = save_post(post, content_md)
        print(f"           ✅ Saved: {filename}")
        saved += 1

        time.sleep(DELAY_BETWEEN)

    # Step 3: Create an index file
    create_index(posts, saved)

    print(f"\n{'='*50}")
    print(f"✅ Done! {saved} new posts saved to ./{OUTPUT_DIR}/")
    print(f"📂 {already_existed} posts already existed (skipped)")
    print(f"⏭️  {skipped} posts skipped (paid/empty)")
    print(f"📁 Index file: {OUTPUT_DIR}/INDEX.md")


def create_index(posts: list[dict], total_saved: int):
    """Create an index/table of contents file."""
    lines = [
        "# Knowledge Base Index",
        f"**Source:** Justin Scott — cypherj.substack.com",
        f"**Total posts:** {total_saved}",
        f"**Scraped on:** {datetime.now().strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
        "## Posts",
        "",
    ]

    for post in posts:
        title = post.get("title", "Untitled")
        slug = post.get("slug", "untitled")
        date_str = post.get("post_date", post.get("published_at", ""))
        is_paid = post.get("audience", "") == "only_paid"

        try:
            dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
            date_prefix = dt.strftime("%Y-%m-%d")
        except (ValueError, AttributeError):
            date_prefix = "undated"

        if is_paid:
            lines.append(f"- 🔒 **{title}** ({date_prefix}) — *paid only*")
        else:
            filename = f"{date_prefix}_{sanitize_filename(slug)}.md"
            lines.append(f"- [{title}](./{filename}) ({date_prefix})")

    filepath = os.path.join(OUTPUT_DIR, "INDEX.md")
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


if __name__ == "__main__":
    main()
