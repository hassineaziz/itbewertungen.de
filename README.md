# Affiliate Blog CMS — Flask Template

A production-ready, self-hosted affiliate marketing site built with Flask. Write and publish SEO-optimised blog posts, manage affiliate links with live Amazon price syncing, and generate AI-assisted content — all from a single lightweight CMS with no external dependency.

---

## Features

### Public Site (`/blog`)
- Full-text search across title, excerpt, and content
- Tag filtering via JSON array queries (GIN-indexed for speed)
- Reading time estimation on every post
- RSS feed at `/blog/feed.xml`
- Hreflang-ready bilingual routing (`/` for German, `/en/` for English)
- Auto-generated XML sitemap

### Admin CMS (`/admin-cms`)
- Rich HTML editor (TinyMCE) for standard posts
- Schema-driven post templates for affiliate content (see below)
- Cover image upload directly to S3
- `draft` / `published` status with `published_at` timestamp
- SEO fields: `meta_title`, `meta_description`, `focus_keyword`
- Export newsletter subscribers as CSV
- One-click sitemap regeneration after publishing

### Schema-Driven Post Templates
Rather than a blank editor, each post type follows a structured schema stored in `schemas/templates.json`:

| Template | Use Case |
|---|---|
| `product_review` | Single product deep-dive with pros/cons, rating, and structured data |
| `affiliate_comparison` | Head-to-head comparison table (2+ products) |
| `best_x_for_y` | "Best X for Y" listicle with ranked picks |
| `affiliate_top_3` | Top-3 curated list with CTA buttons |
| `expanded_definition` | Informational / SEO foundation post |
| `standard` | Free-form rich text HTML |

### Affiliate Link Engine
- Central `AffiliateLink` table — one record per product, one `/go/<slug>` redirect
- Click tracking on every redirect
- Amazon PA-API integration: syncs live price, discount %, availability, and product images on demand
- `sync_prices.py` script for scheduled bulk price refreshes
- Price history stored as JSON for trend display

### AI Post Generator
- Gemini-powered article generator seeded with your affiliate product data
- Dynamic prompt templates per post type (`seo_prompts/`)
- Generates fully structured JSON matching the database schema — no manual copy-paste
- AI revision endpoint for refining existing drafts

### SEO & Structured Data
- JSON-LD schemas: `Product`, `Review`, `ItemList`, `BlogPosting`, `BreadcrumbList`
- Aggregate rating and price pulled live from the `AffiliateLink` table
- Canonical tags, Open Graph, and Twitter Card meta on every page
- `robots.txt` and sitemap auto-updated on publish

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12 / Flask |
| Database | SQLite (dev) · PostgreSQL (prod) |
| ORM / Migrations | SQLAlchemy + Alembic |
| Frontend | Jinja2 templates + Tailwind CSS |
| Rich Editor | TinyMCE (self-hosted) |
| AI Generation | Google Gemini API |
| Storage | AWS S3 (cover images) |
| Price Sync | Amazon Product Advertising API |
| i18n | Flask-Babel |
| WSGI | Gunicorn + Nginx |

---

## Getting Started

### 1. Clone and install

```bash
git clone https://github.com/your-username/affiliate-blog-cms.git
cd affiliate-blog-cms
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
npm install   # Tailwind build tooling
```

### 2. Configure

```bash
cp .env.example .env
cp config.example.yaml config.yaml
```

Key `.env` values:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask session secret |
| `ADMIN_PASSWORD` | Password for `/admin-cms` |
| `SQLALCHEMY_DATABASE_URI` | SQLite or PostgreSQL connection string |
| `GEMINI_API_KEY` | Google Gemini for AI post generation |
| `AMAZON_CLIENT_ID` / `AMAZON_CLIENT_SECRET` | Amazon PA-API credentials |
| `AMAZON_PARTNER_TAG` | Your Amazon Associates tag |
| `AWS_ACCESS_KEY_ID` / `AWS_SECRET_ACCESS_KEY` | S3 for cover image uploads |

Key `config.yaml` values (see `config.example.yaml` for full reference):

```yaml
brand:
  name: "YourSite"
  primary_color: "#2563eb"

niche:
  category: "External SSDs"
  home_title: "Best External SSDs 2026 — Lab Tested & Ranked"

seo:
  domain: "https://yourdomain.com"
  lang: "en"
```

### 3. Initialise the database

```bash
flask db upgrade
python seed_db.py        # optional: seed sample affiliate links
```

### 4. Run locally

```bash
python main.py
# → http://localhost:5001
# → http://localhost:5001/admin-cms  (enter ADMIN_PASSWORD)
```

### 5. Build Tailwind CSS

```bash
npx tailwindcss -i website/static/css/app.css -o website/static/css/app.build.css --watch
```

---

## Project Structure

```
├── main.py                  # App entry point
├── wsgi.py                  # Gunicorn entry point
├── config.example.yaml      # Site config template
├── schemas/templates.json   # Post template schemas
├── seo_prompts/             # Per-template AI prompt files
├── migrations/              # Alembic migrations
├── sync_prices.py           # Amazon price sync script
├── seed_db.py               # Dev seed script
└── website/
    ├── __init__.py          # App factory
    ├── models.py            # SQLAlchemy models
    ├── views.py             # All routes (public + admin)
    ├── ai_generator.py      # Gemini AI article generator
    ├── seo_utils.py         # Structured data + meta helpers
    ├── auto_sitemap.py      # Sitemap generation
    ├── templates/
    │   ├── base.html
    │   ├── landing.html
    │   ├── blog_index.html
    │   ├── blog_admin_*.html
    │   └── post-templates/  # One template per content type
    └── static/
        ├── css/
        └── js/tinymce/      # Self-hosted TinyMCE
```

---

## Deployment (Production)

```bash
# Set environment
export FLASK_ENV=production
export SESSION_COOKIE_SECURE=true

# Run with Gunicorn
gunicorn wsgi:app -w 4 -b 0.0.0.0:8000
```

Serve behind Nginx with SSL. The app includes `ProxyFix` middleware for correct IP and HTTPS detection behind a reverse proxy.

For scheduled price syncs, add a cron job:

```cron
0 */6 * * * /path/to/venv/bin/python /path/to/sync_prices.py
```

---

## License

MIT
