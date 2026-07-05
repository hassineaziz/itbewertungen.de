from . import db
from sqlalchemy.sql import func
import json

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    icon = db.Column(db.String(50), nullable=True)
    
class AffiliateLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(100), unique=True, nullable=False) # e.g. /go/samsung-t9
    destination_url = db.Column(db.String(1000), nullable=False)
    clicks = db.Column(db.Integer, default=0)
    
    # Auto-Sync Data Fields
    asin = db.Column(db.String(20), nullable=True)
    product_title = db.Column(db.String(255), nullable=True)
    current_price = db.Column(db.Float, nullable=True)
    original_price = db.Column(db.Float, nullable=True)
    discount_percentage = db.Column(db.Integer, nullable=True)
    is_available = db.Column(db.Boolean, default=True)
    image_url = db.Column(db.String(500), nullable=True)
    features_json = db.Column(db.JSON, nullable=True)
    price_history = db.Column(db.JSON, nullable=True)
    last_synced_at = db.Column(db.DateTime(timezone=True), nullable=True)

    # Persisted E-E-A-T review data — set once per product, reused by every
    # AI-generated article that references this affiliate link.
    eeat_enabled = db.Column(db.Boolean, default=False)
    eeat_value_score = db.Column(db.Float, nullable=True)
    eeat_build_score = db.Column(db.Float, nullable=True)
    eeat_usability_score = db.Column(db.Float, nullable=True)
    eeat_expectation_score = db.Column(db.Float, nullable=True)
    review_notes = db.Column(db.Text, nullable=True)
    raw_source_info = db.Column(db.Text, nullable=True)

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    slug = db.Column(db.String(200), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    excerpt = db.Column(db.String(300), nullable=True)
    content_html = db.Column(db.Text, nullable=True)   # used by 'standard' template only
    cover_image_url = db.Column(db.String(500), nullable=True)
    status = db.Column(db.String(20), default='draft')  # draft, published
    category = db.Column(db.String(100), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    published_at = db.Column(db.DateTime(timezone=True), nullable=True)
    tags = db.Column(db.JSON, nullable=True)
    meta_title = db.Column(db.String(255), nullable=True)
    meta_description = db.Column(db.String(255), nullable=True)
    focus_keyword = db.Column(db.String(100), nullable=True)
    
    # Review schema fields
    rating = db.Column(db.Float, nullable=True)
    rating_count = db.Column(db.Integer, default=0)
    price_from = db.Column(db.String(20), nullable=True)
    price_drop = db.Column(db.Integer, nullable=True)
    pros = db.Column(db.JSON, nullable=True)
    cons = db.Column(db.JSON, nullable=True)
    
    # Featured
    is_featured = db.Column(db.Boolean, default=False)
    featured_rank = db.Column(db.Integer, nullable=True)
    best_for_label = db.Column(db.String(100), nullable=True)
    affiliate_slug = db.Column(db.String(100), nullable=True)
    read_time = db.Column(db.Integer, default=5)

    # ── Schema-driven CMS ──────────────────────────────────────────────
    # Which template drives this post. 'standard' = legacy free-text HTML.
    template = db.Column(db.String(80), nullable=False, default='standard')
    # Stores the structured JSON filled by the admin form.
    structured_content = db.Column(db.JSON, nullable=True)
    # ───────────────────────────────────────────────────────────────────

    created_at = db.Column(db.DateTime(timezone=True), default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), default=func.now(), onupdate=func.now())
    
    def get_tags_list(self):
        if self.tags:
            return self.tags if isinstance(self.tags, list) else []
        return []
    
    def set_tags_list(self, tags_list):
        if tags_list:
            clean_tags = [tag.strip().lower() for tag in tags_list if tag.strip()]
            self.tags = list(set(clean_tags))
        else:
            self.tags = []

    @property
    def pros_list(self):
        if not self.pros:
            return []
        if isinstance(self.pros, list):
            return self.pros
        if isinstance(self.pros, str):
            import json
            try:
                return json.loads(self.pros)
            except:
                return [p.strip() for p in self.pros.split(',') if p.strip()]
        return []
