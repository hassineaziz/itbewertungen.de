import os
import json
from datetime import datetime, timezone, timedelta
from sqlalchemy.exc import OperationalError
from website import create_app, db
from website.models import BlogPost, AffiliateLink

app = create_app()

def seed():
    with app.app_context():
        # Ensure tables are created
        db.create_all()
        
        # Check if we already seeded links to avoid duplicates
        from sqlalchemy import text
        try:
            link_count = AffiliateLink.query.count()
        except OperationalError:
            # Columns might be missing – add them
            with db.engine.begin() as conn:
                for col, col_type in [("image_url", "VARCHAR(500)"), ("features_json", "JSON"), ("price_history", "JSON")]:
                    try:
                        conn.execute(text(f"ALTER TABLE affiliate_link ADD COLUMN {col} {col_type}"))
                    except Exception:
                        pass
            link_count = 0
        if link_count == 0:
            print("Seeding dummy Affiliate Links...")
            links_data = [
                {"slug": "samsung-t9", "destination_url": "https://amazon.com/dp/samsung-t9-fake-link?tag=ssdlab", "clicks": 142},
                {"slug": "crucial-x10", "destination_url": "https://amazon.com/dp/crucial-x10-fake-link?tag=ssdlab", "clicks": 89},
                {"slug": "sandisk-extreme", "destination_url": "https://amazon.com/dp/sandisk-extreme-fake-link?tag=ssdlab", "clicks": 312},
                {"slug": "wd-black-p40", "destination_url": "https://amazon.com/dp/wd-black-p40-fake-link?tag=ssdlab", "clicks": 45},
                {"slug": "samsung-t7-shield", "destination_url": "https://amazon.com/dp/samsung-t7-shield-fake-link?tag=ssdlab", "clicks": 18}
            ]
            for l_data in links_data:
                db.session.add(AffiliateLink(**l_data))
            db.session.commit()
            print("Affiliate Links seeded successfully!")

        # Check if we already seeded posts to avoid duplicates (seeding is now idempotent)
        print("Seeding dummy blog posts...")

        posts_data = [
            {
                "title": "Samsung T9 Portable SSD Review (2026)",
                "slug": "samsung-t9-portable-ssd-review",
                "excerpt": "We transferred 2TB of mixed files, ran synthetic benchmarks on Mac and Windows, and dropped the Samsung T9 from 6 feet onto concrete.",
                "category": "Storage",
                "tags": ["ssd", "storage", "featured", "tech"],
                "cover_image_url": "https://images.unsplash.com/photo-1597571063304-81f08190f3e1?auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>Why the T9 is Our Top Pick</h2>
                <p>The Samsung T9 offers the best balance of speed, durability, and price.</p>
                """,
                "featured_rank": 1,
                "rating": 9.8,
                "price_from": "$129.99",
                "price_drop": 12,
                "best_for_label": "Best Overall",
                "affiliate_slug": "samsung-t9",
                "pros": ["Sustained 1,950 MB/s read", "Rubberized drop protection", "Great thermals"],
                "read_time": 8
            },
            {
                "title": "Crucial X10 Pro Review: The Tiny Powerhouse",
                "slug": "crucial-x10-pro-review",
                "excerpt": "This drive is incredibly small, but packs a serious punch for video editors and creators on the go.",
                "category": "Storage",
                "tags": ["ssd", "storage", "tech", "featured"],
                "cover_image_url": "https://images.unsplash.com/photo-1621252179027-94459d278660?auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>Great Performance on a Budget</h2>
                <p>Don't let the size fool you. This drive can sustain 4K video editing effortlessly.</p>
                """,
                "featured_rank": 2,
                "rating": 9.2,
                "price_from": "$109.99",
                "price_drop": 5,
                "best_for_label": "Best for Creators",
                "affiliate_slug": "crucial-x10",
                "pros": ["Ultra compact", "Aluminum build", "Hardware encryption"],
                "read_time": 6
            },
            {
                "title": "SanDisk Extreme Portable V2 Review",
                "slug": "sandisk-extreme-portable-v2",
                "excerpt": "The old reliable. Is it still worth buying in 2026? We put it to the test.",
                "category": "Storage",
                "tags": ["ssd", "storage", "budget"],
                "cover_image_url": "https://images.unsplash.com/photo-1544866092-1935c5ef2a8f?auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>The Old Reliable</h2>
                <p>It's been around for years, but the price drops make it an incredible value.</p>
                """,
                "featured_rank": 3,
                "rating": 8.8,
                "price_from": "$79.99",
                "price_drop": 20,
                "best_for_label": "Best Budget",
                "affiliate_slug": "sandisk-extreme",
                "pros": ["Carabiner loop", "IP65 water resistance", "Incredible value"],
                "read_time": 5
            },
            {
                "title": "Best Espresso Machines for Home Baristas",
                "slug": "best-home-espresso-machines",
                "excerpt": "Skip the coffee shop queue. We review the top espresso machines that bring cafe-quality coffee right to your kitchen counter.",
                "category": "Home",
                "tags": ["coffee", "kitchen", "espresso"],
                "cover_image_url": "https://images.unsplash.com/photo-1520209268518-aec60b8bb5ca?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>Pulling the Perfect Shot at Home</h2>
                <p>Investing in a home espresso machine pays for itself within a year if you buy coffee daily. But which machine is actually worth your money?</p>
                <h3>Breville Barista Express</h3>
                <p>This is the ultimate beginner-friendly machine. It has a built-in grinder and intuitive controls to help you dial in the perfect shot.</p>
                <p><a href="#" class="btn-affiliate">Check Price on Amazon</a></p>
                """
            },
            {
                "title": "Are Noise-Canceling Headphones Worth It?",
                "slug": "noise-canceling-headphones-review",
                "excerpt": "We dive deep into the technology behind ANC (Active Noise Canceling) to see if paying the premium is truly worth it for travelers and remote workers.",
                "category": "Tech",
                "tags": ["audio", "travel", "headphones"],
                "cover_image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>The Magic of Active Noise Canceling</h2>
                <p>ANC uses microphones to listen to outside noise and plays the exact opposite frequency into your ears, effectively erasing the background hum of airplanes and coffee shops.</p>
                <h3>Sony WH-1000XM5</h3>
                <p>Currently the king of the hill, these headphones offer unbelievable silence.</p>
                """
            },
            {
                "title": "How to Choose the Right Dumbbells for a Home Gym",
                "slug": "choose-right-dumbbells-home-gym",
                "excerpt": "Building a home gym? Here is everything you need to know about adjustable vs fixed dumbbells and what weight ranges to start with.",
                "category": "Sports",
                "tags": ["fitness", "home gym", "weights"],
                "cover_image_url": "https://images.unsplash.com/photo-1581009146145-b5ef050c2e1e?ixlib=rb-4.0.3&auto=format&fit=crop&w=1600&q=80",
                "content_html": """
                <h2>Adjustable vs Fixed Dumbbells</h2>
                <p>If you have limited space, adjustable dumbbells are the clear winner. They replace a whole rack of weights.</p>
                <h3>Bowflex SelectTech 552</h3>
                <p>The industry standard for adjustable dumbbells. They adjust from 5 to 52.5 lbs with the turn of a dial.</p>
                <p><a href="#" class="btn-affiliate">Buy on Amazon</a></p>
                """
            }
        ]

        # Offset the dates to make them look naturally spaced out
        base_date = datetime.now(timezone.utc)

        for i, data in enumerate(posts_data):
            if BlogPost.query.filter_by(slug=data['slug']).first():
                continue
            post = BlogPost(
                title=data['title'],
                slug=data['slug'],
                excerpt=data['excerpt'],
                content_html=data['content_html'],
                category=data['category'],
                tags=data['tags'],
                cover_image_url=data['cover_image_url'],
                status='published',
                published_at=base_date - timedelta(days=i*2),  # staggered dates
                meta_title=data['title'],
                meta_description=data['excerpt'],
                focus_keyword=data.get('category'),
                featured_rank=data.get('featured_rank'),
                rating=data.get('rating'),
                price_from=data.get('price_from'),
                price_drop=data.get('price_drop'),
                best_for_label=data.get('best_for_label'),
                affiliate_slug=data.get('affiliate_slug'),
                pros=data.get('pros'),
                read_time=data.get('read_time', 5)
            )
            db.session.add(post)
            
        from website.models import Category
        cats = [
            Category(name='Storage', slug='storage', icon='hard_drive_2'),
            Category(name='Accessories', slug='accessories', icon='cable'),
            Category(name='Laptops', slug='laptops', icon='laptop_mac'),
            Category(name='Cameras', slug='cameras', icon='photo_camera')
        ]
        for c in cats:
            if Category.query.filter_by(slug=c.slug).first():
                continue
            db.session.add(c)

        db.session.commit()
        print("Successfully seeded baseline blog posts!")

        # Seed mockup posts from mockup_posts.json if it exists
        mockup_path = os.path.join(os.path.dirname(__file__), "schemas", "mockup_posts.json")
        if os.path.exists(mockup_path):
            with open(mockup_path, "r", encoding="utf-8") as f:
                mockup_data = json.load(f)

            def slugify(text):
                return text.lower().replace(" ", "-").replace("_", "-").replace("?", "")

            for tmpl_key, tmpl in mockup_data.items():
                title = tmpl.get("title") or tmpl.get("headline")
                slug = slugify(title)
                if BlogPost.query.filter_by(slug=slug).first():
                    continue
                
                content_html = tmpl.get("content") or tmpl.get("verdict") or ""
                excerpt = tmpl.get("sub_head") or tmpl.get("excerpt") or ""
                template_name = "standard" if tmpl_key == "standard_html" else tmpl_key
                structured_content = None if tmpl_key == "standard_html" else tmpl

                db.session.add(BlogPost(
                    title=title,
                    slug=slug,
                    excerpt=excerpt,
                    content_html=content_html,
                    category="Mockup",
                    tags=[tmpl_key],
                    cover_image_url=tmpl.get("image_url", ""),
                    status="published",
                    published_at=datetime.now(timezone.utc),
                    meta_title=title,
                    meta_description=excerpt,
                    read_time=tmpl.get("read_time", 5),
                    template=template_name,
                    structured_content=structured_content
                ))

            db.session.commit()
            print("Successfully seeded mockup posts!")

if __name__ == "__main__":
    seed()
