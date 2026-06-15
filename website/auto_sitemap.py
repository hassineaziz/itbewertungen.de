from flask import current_app
from .models import BlogPost
from datetime import datetime, timezone

def generate_auto_sitemap():
    # Home
    yield ('views.home', {}, datetime.now(timezone.utc).isoformat(), 'daily', 1.0)
    
    # Blog Index
    yield ('views.blog_index', {}, datetime.now(timezone.utc).isoformat(), 'daily', 0.9)
    
    # Blog Posts
    try:
        posts = BlogPost.query.filter_by(status='published').all()
        for post in posts:
            lastmod = post.updated_at.isoformat() if post.updated_at else post.published_at.isoformat() if post.published_at else None
            yield ('views.blog_post', {'slug': post.slug}, lastmod, 'monthly', 0.8)
    except:
        pass
        
    # Legal
    yield ('views.privacy_policy', {}, None, 'yearly', 0.1)
    yield ('views.terms_of_service', {}, None, 'yearly', 0.1)
