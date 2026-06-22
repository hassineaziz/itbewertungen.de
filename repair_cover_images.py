#!/usr/bin/env python3
"""
repair_cover_images.py
----------------------
Fixes blog posts whose cover_image_url references a local /static/uploads/ file
that does NOT exist on this machine.

Run this on the VPS (or any machine) where the database lives:
    python3 repair_cover_images.py

What it does:
  1. Scans all BlogPost rows for cover_image_url = /static/uploads/xxx that are missing on disk.
  2. For each broken post, looks up the first product's AffiliateLink image_url.
  3. Updates cover_image_url to the affiliate link's image (which is always authoritative).
  4. Saves the fix to the database.
"""

import os
import sys

# ── Bootstrap Flask app ────────────────────────────────────────────────────────
# Make sure we're in the project root
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from dotenv import load_dotenv
load_dotenv()

from website import create_app, db
from website.models import BlogPost, AffiliateLink

app = create_app()

def file_exists_for_url(root_path, url):
    """Return True if a /static/... URL maps to an existing file on disk."""
    if not url:
        return False
    if not url.startswith('/static/'):
        return True  # external URL — treat as OK
    file_path = os.path.join(root_path, url.lstrip('/'))
    return os.path.exists(file_path)


def get_first_affiliate_image(post):
    """
    Find the first product's AffiliateLink and return its image_url.
    Falls back to image_url stored in structured_content.
    """
    if not post.structured_content:
        return None

    for list_key in ['products', 'picks']:
        products = post.structured_content.get(list_key)
        if not (products and isinstance(products, list) and len(products) > 0):
            continue
        first = products[0]
        if not isinstance(first, dict):
            continue

        # Try affiliate link first
        aff_slug = first.get('affiliate_slug', '')
        if aff_slug:
            clean_slug = aff_slug.strip('/').replace('go/', '')
            link = AffiliateLink.query.filter(
                db.func.lower(AffiliateLink.slug) == db.func.lower(clean_slug)
            ).first()
            if link and link.image_url:
                return link.image_url

        # Fallback: image stored in structured_content
        img = first.get('image_url', '')
        if img:
            return img
        break

    return None


with app.app_context():
    root_path = app.root_path  # = .../website/

    posts = BlogPost.query.all()
    fixed = 0
    broken = 0

    print(f"Checking {len(posts)} posts...\n")

    for post in posts:
        url = post.cover_image_url or ''
        if not url.startswith('/static/'):
            continue  # external URL or empty — skip

        if file_exists_for_url(root_path, url):
            continue  # file exists — OK

        broken += 1
        print(f"  ❌  [{post.id}] \"{post.title[:50]}\"")
        print(f"       broken cover: {url}")

        new_img = get_first_affiliate_image(post)
        if new_img:
            print(f"       → fixing with: {new_img}")
            post.cover_image_url = new_img
            fixed += 1
        else:
            print(f"       ⚠️  No affiliate image found — cover cleared")
            post.cover_image_url = ''

        print()

    if fixed or broken:
        db.session.commit()
        print(f"Done. {broken} broken posts found, {fixed} fixed.")
    else:
        print("✅  All cover images are OK — nothing to fix.")
