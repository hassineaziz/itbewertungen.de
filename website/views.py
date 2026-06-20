from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for, current_app, make_response, session, abort
from .models import BlogPost
from . import db, csrf
from .seo_utils import download_and_cache_image, download_images_in_structured_content
import os
import re
import json
from datetime import datetime, timezone

views = Blueprint('views', __name__)

# ── Schema helpers ─────────────────────────────────────────────────────────────

def _schema_path():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schemas', 'templates.json')

def load_schemas():
    try:
        with open(_schema_path(), 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        current_app.logger.error(f"Failed to load schema: {e}")
        return {}

def get_template_names():
    schemas = load_schemas()
    return {k: v.get('label', k) for k, v in schemas.items()}

# ── Auth helpers ───────────────────────────────────────────────────────────────

def generate_unique_slug(base_title: str) -> str:
    slug = re.sub(r'[^\w\s-]', '', base_title.lower())
    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
    base_slug = slug
    counter = 1
    while BlogPost.query.filter_by(slug=slug).first() is not None:
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('views.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# ── Auth routes ────────────────────────────────────────────────────────────────

@views.route('/admin-cms', methods=['GET', 'POST'])
def admin_login():
    if session.get('admin_logged_in'):
        return redirect(url_for('views.blog_dashboard'))
    if request.method == 'POST':
        password = request.form.get('password')
        correct_password = os.getenv('ADMIN_PASSWORD', 'admin123')
        if password == correct_password:
            session['admin_logged_in'] = True
            flash('Logged in successfully!', 'success')
            return redirect(url_for('views.blog_dashboard'))
        else:
            flash('Incorrect password.', 'error')
    return render_template('admin_login.html')

@views.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    flash('Logged out.', 'success')
    return redirect(url_for('views.home'))

# ── Public pages ───────────────────────────────────────────────────────────────

def resolve_post_price_from_affiliate(post):
    if not post:
        return
    from .models import AffiliateLink
    slug_clean = post.affiliate_slug or (post.structured_content.get('affiliate_slug') if post.structured_content else None)
    
    # If not set directly, check first pick's slug for listicles
    if not slug_clean and post.structured_content:
        for list_key in ['products', 'picks']:
            if list_key in post.structured_content and isinstance(post.structured_content[list_key], list):
                if len(post.structured_content[list_key]) > 0:
                    first_item = post.structured_content[list_key][0]
                    if isinstance(first_item, dict):
                        slug_clean = first_item.get('affiliate_slug')
                    break
                    
    if slug_clean:
        if slug_clean.startswith('/go/'): slug_clean = slug_clean[4:]
        elif slug_clean.startswith('go/'): slug_clean = slug_clean[3:]
        link = AffiliateLink.query.filter(db.func.lower(AffiliateLink.slug) == db.func.lower(slug_clean)).first()
        if link:
            if link.current_price is not None:
                post.price_from = f"{link.current_price:.2f} €".replace('.', ',').replace(',00', '')
            if not post.cover_image_url and link.image_url:
                post.cover_image_url = link.image_url

@views.route('/')
def home():
    from .models import Category
    featured_post   = BlogPost.query.filter_by(featured_rank=1, status='published').first()
    top_picks       = BlogPost.query.filter(BlogPost.featured_rank.between(1, 3), BlogPost.status=='published').order_by(BlogPost.featured_rank.asc()).all()
    runner_up_posts = BlogPost.query.filter(BlogPost.featured_rank.between(2, 5), BlogPost.status=='published').order_by(BlogPost.featured_rank.asc()).all()
    latest_posts    = BlogPost.query.filter_by(status='published').order_by(BlogPost.updated_at.desc()).limit(4).all()
    categories      = Category.query.limit(4).all()
    
    resolve_post_price_from_affiliate(featured_post)
    for p in top_picks:
        resolve_post_price_from_affiliate(p)
    for p in runner_up_posts:
        resolve_post_price_from_affiliate(p)
    for p in latest_posts:
        resolve_post_price_from_affiliate(p)
        
    return render_template("landing.html",
                           featured_post=featured_post,
                           top_picks=top_picks,
                           runner_up_posts=runner_up_posts,
                           latest_posts=latest_posts,
                           categories=categories)

@views.route('/blog')
def blog_index():
    page     = request.args.get('page', 1, type=int)
    tag      = request.args.get('tag')
    category = request.args.get('category')
    q        = request.args.get('q')
    query    = BlogPost.query.filter_by(status='published')
    if tag:
        query = query.filter(BlogPost.tags.contains([tag.lower()]))
    if category:
        query = query.filter(BlogPost.category == category)
    if q:
        query = query.filter(
            BlogPost.title.ilike(f'%{q}%') |
            BlogPost.excerpt.ilike(f'%{q}%') |
            BlogPost.content_html.ilike(f'%{q}%') |
            db.cast(BlogPost.structured_content, db.String).ilike(f'%{q}%')
        )
    posts = query.order_by(BlogPost.published_at.desc()).paginate(page=page, per_page=12)
    
    for p in posts.items:
        resolve_post_price_from_affiliate(p)
        
    return render_template('blog_index.html', posts=posts, current_tag=tag, current_category=category, q=q)

def resolve_affiliate_details_in_data(data):
    if not isinstance(data, dict):
        return data

    from .models import AffiliateLink
    
    # 1. Resolve root level affiliate slug if present (e.g. for Single Product Review)
    affiliate_slug = data.get('affiliate_slug')
    if affiliate_slug:
        if affiliate_slug.startswith('/go/'): affiliate_slug = affiliate_slug[4:]
        elif affiliate_slug.startswith('go/'): affiliate_slug = affiliate_slug[3:]
        link = AffiliateLink.query.filter(db.func.lower(AffiliateLink.slug) == db.func.lower(affiliate_slug)).first()
        if link:
            if link.product_title:
                data['product_name'] = link.product_title
                data['name'] = link.product_title
            if link.current_price is not None:
                data['price'] = f"{link.current_price:.2f} €".replace('.', ',').replace(',00', '')
            if link.image_url:
                data['image_url'] = link.image_url
            if link.features_json:
                data['specs'] = link.features_json

    # We want to collect resolving info for all products in listicles
    resolved_info_by_original_name = {}
    resolved_info_by_index = {} # key: (list_key, index)

    # 2. Resolve lists of products / picks (e.g. for comparison or best-of listicles)
    for list_key in ['products', 'picks']:
        if list_key in data and isinstance(data[list_key], list):
            for idx, item in enumerate(data[list_key]):
                if isinstance(item, dict):
                    orig_name = item.get('name') or item.get('product_name')
                    item_slug = item.get('affiliate_slug')
                    
                    info = {}
                    if item_slug:
                        clean_slug = item_slug
                        if clean_slug.startswith('/go/'): clean_slug = clean_slug[4:]
                        elif clean_slug.startswith('go/'): clean_slug = clean_slug[3:]
                        link = AffiliateLink.query.filter(db.func.lower(AffiliateLink.slug) == db.func.lower(clean_slug)).first()
                        if link:
                            if link.product_title:
                                item['name'] = link.product_title
                                item['product_name'] = link.product_title
                                info['name'] = link.product_title
                            if link.current_price is not None:
                                formatted_price = f"{link.current_price:.2f} €".replace('.', ',').replace(',00', '')
                                item['price'] = formatted_price
                                info['price'] = formatted_price
                            if link.image_url:
                                item['image_url'] = link.image_url
                                info['image_url'] = link.image_url
                            if link.features_json:
                                item['specs'] = link.features_json
                                info['specs'] = link.features_json
                            info['link'] = link
                    
                    if info:
                        if orig_name:
                            resolved_info_by_original_name[orig_name.strip().lower()] = info
                        resolved_info_by_index[(list_key, idx)] = info

    # Helper to extract spec value from an array of key-value spec strings, matching getSpecValue JS logic
    def get_spec_value_py(specs, header):
        if not specs or not isinstance(specs, list):
            return ""
        header_lower = ''.join(c for c in header.lower() if c.isalnum())
        keywords = [header_lower]
        if "lesegeschwindigkeit" in header_lower:
            keywords.extend(["leserate", "lesegeschwindigkeit", "readspeed", "speed", "lese"])
        if "schnittstelle" in header_lower:
            keywords.extend(["interface", "anschluss", "schnittstelle"])
        if "schutzklasse" in header_lower:
            keywords.extend(["ip", "schutzklasse", "waterproof", "staub", "wasser"])
        if "verschlüsselung" in header_lower:
            keywords.extend(["verschlüsselung", "encryption", "sicherheit", "aes"])
            
        for spec in specs:
            if not isinstance(spec, str):
                continue
            colon_idx = spec.find(':')
            if colon_idx == -1:
                continue
            spec_key = spec[:colon_idx].strip()
            spec_val = spec[colon_idx + 1:].strip()
            spec_key_lower = ''.join(c for c in spec_key.lower() if c.isalnum())
            if (spec_key_lower == header_lower or 
                spec_key_lower in header_lower or 
                header_lower in spec_key_lower or
                any(kw in spec_key_lower for kw in keywords)):
                return spec_val
        return ""

    # 3. Resolve comparison table if present
    comp_table = data.get('comparison_table')
    if comp_table and isinstance(comp_table, dict) and 'rows' in comp_table and isinstance(comp_table['rows'], list):
        headers = comp_table.get('headers', [])
        model_col_idx = -1
        price_col_idx = -1
        
        for col_idx, h in enumerate(headers):
            h_lower = str(h).lower()
            if any(w in h_lower for w in ['modell', 'product', 'name', 'geraet', 'gerät', 'computer', 'monitore', 'festplatte']):
                model_col_idx = col_idx
            elif 'preis' in h_lower or 'price' in h_lower:
                price_col_idx = col_idx
                
        if model_col_idx == -1 and len(headers) > 0:
            model_col_idx = 0
        if price_col_idx == -1 and len(headers) > 0:
            price_col_idx = len(headers) - 1

        for row_idx, row in enumerate(comp_table['rows']):
            if isinstance(row, list):
                matched_info = None
                
                # Try to match by index first
                for list_key in ['products', 'picks']:
                    if list_key in data and isinstance(data[list_key], list):
                        if len(data[list_key]) == len(comp_table['rows']):
                            matched_info = resolved_info_by_index.get((list_key, row_idx))
                            if matched_info:
                                break
                                
                # Try to match by model name in model cell
                if not matched_info and model_col_idx < len(row):
                    row_model_name = str(row[model_col_idx]).strip().lower()
                    matched_info = resolved_info_by_original_name.get(row_model_name)
                    
                if matched_info:
                    if 'name' in matched_info and model_col_idx < len(row):
                        row[model_col_idx] = matched_info['name']
                    if 'price' in matched_info and price_col_idx < len(row):
                        row[price_col_idx] = matched_info['price']
                    
                    specs = matched_info.get('specs')
                    if specs:
                        for col_idx, h in enumerate(headers):
                            if col_idx == model_col_idx or col_idx == price_col_idx:
                                continue
                            spec_val = get_spec_value_py(specs, str(h))
                            if spec_val and col_idx < len(row):
                                row[col_idx] = spec_val

    return data

@views.route('/<slug>')
def blog_post(slug):
    post = BlogPost.query.filter_by(slug=slug, status='published').first()
    if not post:
        abort(404)

    resolve_post_price_from_affiliate(post)
    tmpl = post.template or 'standard'
    
    import copy
    data = copy.deepcopy(post.structured_content or {})
    if 'affiliate_slug' not in data and post.affiliate_slug:
        data['affiliate_slug'] = post.affiliate_slug
    data = resolve_affiliate_details_in_data(data)

    if tmpl == 'standard':
        return render_template('post-templates/blog_post.html', post=post)
    else:
        template_file = f'post-templates/{tmpl}.html'
        try:
            return render_template(template_file, post=post, data=data,
                                   current_date=datetime.now().strftime('%d. %B %Y'))
        except Exception as e:
            current_app.logger.error(f"Failed to render template {template_file}: {e}")
            abort(404)

# ── Admin dashboard ────────────────────────────────────────────────────────────

@views.route('/admin/blog')
@admin_required
def blog_dashboard():
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog_admin_dashboard.html', posts=posts)

@views.route('/admin-cms/update-ranks', methods=['POST'])
@admin_required
def blog_update_ranks():
    for key, value in request.form.items():
        if key.startswith('rank_'):
            try:
                post_id = int(key.split('_')[1])
                post    = BlogPost.query.get(post_id)
                if post:
                    post.featured_rank = int(value) if value and value.strip() else None
            except ValueError:
                pass
    db.session.commit()
    flash('Featured rankings updated successfully.', 'success')
    return redirect(url_for('views.blog_dashboard'))

# ── Schema API ─────────────────────────────────────────────────────────────────

@views.route('/admin/api/schema/<template_name>')
@admin_required
def api_schema(template_name):
    """Return the JSON schema for a given template. Used by the JS form builder."""
    schemas = load_schemas()
    schema  = schemas.get(template_name)
    if not schema:
        return jsonify({'error': 'Unknown template'}), 404
    return jsonify(schema)

@views.route('/admin/api/schemas')
@admin_required
def api_schemas_list():
    """Return list of available templates."""
    schemas = load_schemas()
    result  = [{'key': k, 'label': v.get('label', k), 'description': v.get('description', '')}
               for k, v in schemas.items()]
    return jsonify(result)

@views.route('/admin/api/blog/revise', methods=['POST'])
def api_blog_revise():
    if not session.get('admin_logged_in'):
        return jsonify({'error': 'Unauthorized'}), 403

    req_data = request.get_json() or {}
    template_name = req_data.get('template_name')
    structured_content = req_data.get('structured_content')
    instruction = req_data.get('instruction', '').strip()

    if not template_name or not isinstance(structured_content, dict):
        return jsonify({'error': 'Missing template_name or structured_content'}), 400

    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        return jsonify({'error': 'GEMINI_API_KEY is not configured in the server environment.'}), 500

    instruction_section = ""
    if instruction:
        instruction_section = f"\nUser Instruction:\nApply the following custom editing or formatting instructions: \"{instruction}\"\n"
    else:
        instruction_section = "\nAuto-Align mode:\nReview all copy fields and make sure they match the new order/specs/names of the products. Ensure the verdict/conclusion summarizes the actual winner correctly.\n"

    structured_content_json = json.dumps(structured_content, ensure_ascii=False, indent=2)
    
    prompt = (
        "You are an expert SEO copywriter editing a structured blog post in German.\n"
        f"The post is built using the template: '{template_name}'.\n\n"
        "Here is the current structured content of the blog post in JSON format:\n"
        f"{structured_content_json}\n\n"
        "The user has updated the structured properties (such as product rankings, prices, specifications, scores, or product listings).\n"
        "Your task is to:\n"
        "1. Review the content of all text-heavy copywriting fields (e.g., 'buying_guide', 'conclusion', 'verdict', product summaries/reviews, listicle descriptions, or verdict cells) and revise them so they are completely consistent with the updated product names, order, prices, and specifications.\n"
        "2. Reorder reviews, lists, or comparison table rows if the rankings or products list have changed, to maintain perfect consistency.\n"
        "3. Revise the copy to sound professional, engaging, and authoritative.\n"
        f"{instruction_section}\n"
        "OUTPUT FORMAT:\n"
        "Return the updated structured content matching the EXACT same JSON keys and structure as the input JSON.\n"
        "Do NOT include any extra keys.\n"
        "Do NOT wrap the response in markdown code blocks like ```json ... ```. Just return the raw JSON object.\n"
    )

    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-pro",
        "gemini-1.5-pro",
        "gemini-pro-latest",
        "gemini-flash-latest"
    ]
    
    import requests
    import time
    
    result_json = None
    last_err = None
    
    for model_name in models_to_try:
        api_url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            result_json = response.json()
            break
        except Exception as err:
            last_err = err
            time.sleep(1)
            continue
    else:
        return jsonify({'error': f'Failed to contact Gemini API. Last error: {str(last_err)}'}), 502

    try:
        candidates = result_json.get("candidates", [])
        if not candidates:
            raise ValueError("No response candidates returned by the Gemini API model.")
            
        content_parts = candidates[0].get("content", {}).get("parts", [])
        if not content_parts:
            raise ValueError("Candidate response parts list is empty.")
            
        raw_text = content_parts[0].get("text", "").strip()
        
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                raw_text = "\n".join(lines[1:-1])
        
        parsed_data = json.loads(raw_text, strict=False)
        return jsonify(parsed_data)
    except Exception as e:
        return jsonify({'error': f'Failed to parse LLM response as JSON: {str(e)}'}), 500

def populate_derived_post_fields(post):
    # Cache the cover image if it's an external URL
    if post.cover_image_url:
        post.cover_image_url = download_and_cache_image(post.cover_image_url, keyword=post.focus_keyword)

    # Process and cache images in structured_content in-place
    if post.structured_content:
        post.structured_content = download_images_in_structured_content(post.structured_content, keyword=post.focus_keyword)

    if not post.template or post.template == 'standard':
        return

    import copy
    sc_resolved = resolve_affiliate_details_in_data(copy.deepcopy(post.structured_content or {}))

    rating = None
    price_from = None
    best_for_label = None
    affiliate_slug = None

    if post.template == 'best_x_for_y_template':
        products = sc_resolved.get('products') or sc_resolved.get('picks') or []
        if products and isinstance(products, list):
            first = products[0]
            if isinstance(first, dict):
                rating = first.get('rating')
                price_from = first.get('price')
                best_for_label = first.get('badge')
                affiliate_slug = first.get('affiliate_slug')

    elif post.template == 'affiliate_comparison_template':
        products = sc_resolved.get('products', [])
        if products and isinstance(products, list):
            first = products[0]
            if isinstance(first, dict):
                rating = first.get('rating')
                price_from = first.get('price')
                best_for_label = first.get('badge')
                affiliate_slug = first.get('affiliate_slug')

    elif post.template == 'product_review_template':
        rating = sc_resolved.get('rating')
        price_from = sc_resolved.get('price')
        best_for_label = sc_resolved.get('badge')
        affiliate_slug = sc_resolved.get('affiliate_slug')

    if affiliate_slug:
        if affiliate_slug.startswith('/go/'):
            affiliate_slug = affiliate_slug[4:]
        elif affiliate_slug.startswith('go/'):
            affiliate_slug = affiliate_slug[3:]

    if rating is not None:
        try:
            post.rating = float(rating)
        except (ValueError, TypeError):
            post.rating = None
    else:
        post.rating = None

    post.price_from = str(price_from) if price_from is not None else None
    post.best_for_label = str(best_for_label) if best_for_label is not None else None
    post.affiliate_slug = str(affiliate_slug) if affiliate_slug is not None else None

# ── Admin: Generate with AI ───────────────────────────────────────────────────

@views.route('/admin/blog/generate-ai', methods=['GET', 'POST'])
@admin_required
def admin_generate_ai():
    from .models import AffiliateLink, Category
    from .ai_generator import generate_article
    
    template_names = get_template_names()
    categories = Category.query.all()
    affiliate_links = AffiliateLink.query.all()
    
    if request.method == 'POST':
        focus_keyword = request.form.get('focus_keyword', '').strip()
        secondary_keywords = request.form.get('secondary_keywords', '').strip()
        category = request.form.get('category', '').strip()
        template_name = request.form.get('template', 'standard')
        core_product_slugs = request.form.getlist('core_product_slugs')
        
        # Collect per-product overrides (EEAT & Specs)
        product_overrides = {}
        for slug in core_product_slugs:
            enable_eeat = request.form.get(f'enable_eeat_{slug}') == 'on'
            
            slider_data = None
            if enable_eeat:
                slider_data = {
                    'Preis-Leistung': float(request.form.get(f'score_value_{slug}', '0.5')),
                    'Verarbeitung & Material': float(request.form.get(f'score_build_{slug}', '0.5')),
                    'Handhabung & Installation': float(request.form.get(f'score_usability_{slug}', '0.5')),
                    'Alltagstauglichkeit': float(request.form.get(f'score_expectation_{slug}', '0.5'))
                }
                
            product_overrides[slug] = {
                'slider_data': slider_data,
                'quick_notes': request.form.get(f'quick_notes_{slug}', '').strip(),
                'raw_source_info': request.form.get(f'raw_source_info_{slug}', '').strip()
            }
            
        # Global fallback if no products are checked
        if not core_product_slugs:
            global_quick_notes = request.form.get('global_quick_notes', '').strip()
            global_raw_source = request.form.get('global_raw_source_info', '').strip()
            if global_quick_notes or global_raw_source:
                product_overrides['global_custom'] = {
                    'slider_data': None,
                    'quick_notes': global_quick_notes,
                    'raw_source_info': global_raw_source
                }
        
        if not focus_keyword:
            flash("Fokus-Keyword ist erforderlich.", "danger")
            return redirect(url_for('views.admin_generate_ai'))
            
        try:
            # 1. Generate via our LLM client
            generated_data = generate_article(
                focus_keyword=focus_keyword,
                secondary_keywords=secondary_keywords,
                category=category,
                template_name=template_name,
                core_product_slugs=core_product_slugs,
                product_overrides=product_overrides
            )
            
            # 2. Check and fallback if model generated JSON has missing or misnamed fields
            title = generated_data.get("title") or f"{focus_keyword} Test & Vergleich"
            slug = generated_data.get("slug") or generate_unique_slug(title)
            slug = generate_unique_slug(slug) # Make sure it's unique
            
            excerpt = generated_data.get("excerpt") or f"Detaillierter Testbericht für {focus_keyword}."
            meta_title = generated_data.get("meta_title") or title[:60]
            meta_description = generated_data.get("meta_description") or excerpt[:160]
            cover_image_url = generated_data.get("cover_image_url") or ""
            
            # Resolve category_id by name
            category_id = None
            if category:
                cat_obj = Category.query.filter_by(name=category).first()
                if cat_obj:
                    category_id = cat_obj.id

            # Create the post in DB
            post = BlogPost(
                title=title,
                slug=slug,
                excerpt=excerpt,
                template=template_name,
                status="draft", # default to draft for review
                category=category,
                category_id=category_id,
                content_html="", # satisfy NOT NULL constraint
                cover_image_url=cover_image_url,
                meta_title=meta_title,
                meta_description=meta_description,
                focus_keyword=focus_keyword,
                read_time=int(generated_data.get("read_time", 5))
            )
            post.set_tags_list(generated_data.get("tags", []))
            
            # 3. Populate specific template fields
            if template_name == 'standard':
                post.content_html = generated_data.get("content_html") or ""
                post.rating = float(generated_data.get("rating")) if generated_data.get("rating") else None
                post.price_from = generated_data.get("price")
            else:
                post.structured_content = generated_data.get("structured_content")
                post.content_html = ""
                
            # 4. Save and auto-extract derived fields
            db.session.add(post)
            db.session.commit()
            
            populate_derived_post_fields(post)
            db.session.commit()
            
            flash(f"Artikel erfolgreich mit KI generiert! (Entwurf: '{post.title}')", "success")
            return redirect(url_for('views.blog_edit', post_id=post.id))
            
        except Exception as e:
            current_app.logger.error(f"KI Generierung fehlgeschlagen: {e}")
            flash(f"Generierungsfehler: {str(e)}", "danger")
            return redirect(url_for('views.admin_generate_ai'))
            
    return render_template(
        'blog_admin_generate_ai.html',
        template_names=template_names,
        categories=categories,
        affiliate_links=affiliate_links,
        has_api_key=bool(os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY"))
    )

# ── Admin: New post ────────────────────────────────────────────────────────────

@views.route('/admin/blog/new', methods=['GET', 'POST'])
@admin_required
def blog_new():
    template_names = get_template_names()

    if request.method == 'POST':
        title    = request.form.get('title', '').strip()
        tmpl     = request.form.get('template', 'standard')
        status   = request.form.get('status', 'draft')
        excerpt  = request.form.get('excerpt', '')
        category = request.form.get('category', '')
        tags_str = request.form.get('tags', '')
        tags_list = [t.strip().lower() for t in tags_str.split(',') if t.strip()]

        meta_title       = request.form.get('meta_title', '')
        meta_description = request.form.get('meta_description', '')
        focus_keyword    = request.form.get('focus_keyword', '')
        cover_image_url  = request.form.get('cover_image_url', '')
        featured_rank    = request.form.get('featured_rank', '')
        rating           = request.form.get('rating', '')
        read_time        = request.form.get('read_time', '5')
        price_from       = request.form.get('price_from', '')
        price_drop       = request.form.get('price_drop', '')
        best_for_label   = request.form.get('best_for_label', '')
        affiliate_slug   = request.form.get('affiliate_slug', '')

        structured_json = request.form.get('structured_content_json', '{}')
        try:
            structured_content = json.loads(structured_json)
        except Exception:
            structured_content = {}

        content_html = request.form.get('content', '') if tmpl == 'standard' else ""
        
        # Use submitted slug if provided, otherwise auto-generate from title
        custom_slug = request.form.get('slug', '').strip()
        if custom_slug:
            # Sanitise: lowercase, hyphens only
            custom_slug = re.sub(r'[^\w\s-]', '', custom_slug.lower())
            custom_slug = re.sub(r'[-\s]+', '-', custom_slug).strip('-')
            slug = generate_unique_slug(custom_slug) if BlogPost.query.filter_by(slug=custom_slug).first() else custom_slug
        else:
            slug = generate_unique_slug(title)

        # Resolve category_id by name
        category_id = None
        if category:
            from .models import Category
            cat_obj = Category.query.filter_by(name=category).first()
            if cat_obj:
                category_id = cat_obj.id

        post = BlogPost(
            title=title, slug=slug, excerpt=excerpt,
            content_html=content_html, cover_image_url=cover_image_url,
            status=status, category=category, category_id=category_id,
            meta_title=meta_title, meta_description=meta_description,
            focus_keyword=focus_keyword, tags=tags_list,
            featured_rank=int(featured_rank) if featured_rank and featured_rank.strip() else None,
            rating=float(rating) if rating and rating.strip() else None,
            price_drop=int(price_drop) if price_drop and price_drop.strip() else None,
            read_time=int(read_time) if read_time and read_time.strip() else 5,
            price_from=price_from or None, best_for_label=best_for_label or None,
            affiliate_slug=affiliate_slug or None,
            template=tmpl, structured_content=structured_content,
        )
        if status == 'published':
            post.published_at = datetime.now(timezone.utc)

        populate_derived_post_fields(post)
        db.session.add(post)
        db.session.commit()
        flash('Blog post created!', 'success')
        return redirect(url_for('views.blog_dashboard'))

    from .models import AffiliateLink, Category
    all_links = AffiliateLink.query.all()
    categories = Category.query.order_by(Category.name.asc()).all()
    links_json = json.dumps([{
        "slug": l.slug,
        "product_title": l.product_title or l.slug,
        "current_price": f"{l.current_price:.2f} €".replace('.', ',').replace(',00', '') if l.current_price else '',
        "image_url": l.image_url or '',
        "features": l.features_json or []
    } for l in all_links])

    return render_template('blog_admin_edit.html', post=None,
                           template_names=template_names,
                           schemas_json=json.dumps(load_schemas()),
                           links_json=links_json,
                           categories=categories,
                           has_api_key=bool(os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")))

# ── Admin: Edit post ───────────────────────────────────────────────────────────

@views.route('/admin/blog/edit/<int:post_id>', methods=['GET', 'POST'])
@admin_required
def blog_edit(post_id):
    post = BlogPost.query.get_or_404(post_id)
    template_names = get_template_names()

    if request.method == 'POST':
        post.title            = request.form.get('title', post.title)
        post.excerpt          = request.form.get('excerpt', '')
        post.meta_title       = request.form.get('meta_title', '')
        post.meta_description = request.form.get('meta_description', '')
        post.focus_keyword    = request.form.get('focus_keyword', '')
        post.category         = request.form.get('category', '')
        if post.category:
            from .models import Category
            cat_obj = Category.query.filter_by(name=post.category).first()
            post.category_id = cat_obj.id if cat_obj else None
        else:
            post.category_id = None
        post.cover_image_url  = request.form.get('cover_image_url', '')
        post.price_from       = request.form.get('price_from', '')
        post.best_for_label   = request.form.get('best_for_label', '')
        post.affiliate_slug   = request.form.get('affiliate_slug', '')

        tags_str   = request.form.get('tags', '')
        post.tags  = [t.strip().lower() for t in tags_str.split(',') if t.strip()]

        fr = request.form.get('featured_rank', '')
        post.featured_rank = int(fr) if fr and fr.strip() else None

        r = request.form.get('rating', '')
        post.rating = float(r) if r and r.strip() else None

        pd = request.form.get('price_drop', '')
        post.price_drop = int(pd) if pd and pd.strip() else None

        rt = request.form.get('read_time', '5')
        post.read_time = int(rt) if rt and rt.strip() else 5

        tmpl = request.form.get('template', post.template)
        post.template = tmpl

        structured_json = request.form.get('structured_content_json', '{}')
        try:
            post.structured_content = json.loads(structured_json)
        except Exception:
            post.structured_content = {}

        if tmpl == 'standard':
            post.content_html = request.form.get('content', '')

        # Update slug if a new one was submitted
        new_slug = request.form.get('slug', '').strip()
        if new_slug and new_slug != post.slug:
            new_slug = re.sub(r'[^\w\s-]', '', new_slug.lower())
            new_slug = re.sub(r'[-\s]+', '-', new_slug).strip('-')
            if not BlogPost.query.filter(BlogPost.slug == new_slug, BlogPost.id != post.id).first():
                post.slug = new_slug
            else:
                flash(f'Slug "{new_slug}" ist bereits vergeben – alter Slug beibehalten.', 'warning')

        new_status = request.form.get('status', 'draft')
        if new_status == 'published' and post.status != 'published':
            post.published_at = datetime.now(timezone.utc)
        post.status = new_status

        populate_derived_post_fields(post)
        db.session.commit()
        flash('Blog post updated!', 'success')
        return redirect(url_for('views.blog_dashboard'))

    from .models import AffiliateLink, Category
    all_links = AffiliateLink.query.all()
    categories = Category.query.order_by(Category.name.asc()).all()
    links_json = json.dumps([{
        "slug": l.slug,
        "product_title": l.product_title or l.slug,
        "current_price": f"{l.current_price:.2f} €".replace('.', ',').replace(',00', '') if l.current_price else '',
        "image_url": l.image_url or '',
        "features": l.features_json or []
    } for l in all_links])

    return render_template('blog_admin_edit.html', post=post,
                           template_names=template_names,
                           schemas_json=json.dumps(load_schemas()),
                           links_json=links_json,
                           categories=categories,
                           has_api_key=bool(os.getenv("GEMINI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")))

# ── Admin: Delete ──────────────────────────────────────────────────────────────

@views.route('/admin/blog/delete/<int:post_id>', methods=['POST'])
@admin_required
def blog_delete(post_id):
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog post deleted.', 'success')
    return redirect(url_for('views.blog_dashboard'))

# ── Affiliate links ────────────────────────────────────────────────────────────

@views.route('/admin-cms/links', methods=['GET', 'POST'])
@admin_required
def admin_links():
    from .models import AffiliateLink
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            slug = request.form.get('slug', '').strip()
            if slug.startswith('/go/'): slug = slug[4:]
            elif slug.startswith('go/'): slug = slug[3:]
            slug = re.sub(r'[^\w\s-]', '', slug.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            dest = request.form.get('destination_url', '').strip()
            asin = request.form.get('asin', '').strip()
            if not dest.startswith(('http://', 'https://')):
                flash('Invalid Destination URL. Must start with http:// or https://', 'error')
            elif '/go/' in dest:
                flash('Destination URL cannot point back to a /go/ route (Redirect Loop).', 'error')
            else:
                existing = AffiliateLink.query.filter_by(slug=slug).first()
                if existing:
                    flash(f'Slug "/go/{slug}" already exists!', 'error')
                elif slug and dest:
                    try:
                        title = request.form.get('product_title', '').strip()
                        price_str = request.form.get('current_price', '').strip()
                        image = request.form.get('image_url', '').strip()
                        specs_text = request.form.get('specs_raw', '').strip()
                        
                        price = None
                        if price_str:
                            try:
                                price = float(price_str.replace('€', '').replace('$', '').replace(',', '.').strip())
                            except ValueError:
                                pass
                        
                        new_link = AffiliateLink(
                            slug=slug, 
                            destination_url=dest, 
                            asin=asin if asin else None,
                            product_title=title if title else None,
                            current_price=price,
                            image_url=download_and_cache_image(image, keyword=title) if image else None,
                            features_json=[s.strip() for s in specs_text.split('\n') if s.strip()] if specs_text else None,
                            last_synced_at=datetime.now(timezone.utc) if (title or price_str or image or specs_text) else None
                        )
                        db.session.add(new_link)
                        db.session.commit()
                        flash(f'Redirect /go/{slug} created successfully!', 'success')
                    except Exception:
                        db.session.rollback()
                        flash('Database error (likely a concurrent duplicate slug).', 'error')
        elif action == 'edit':
            link_id = request.form.get('link_id')
            slug    = request.form.get('slug', '').strip()
            if slug.startswith('/go/'): slug = slug[4:]
            elif slug.startswith('go/'): slug = slug[3:]
            slug = re.sub(r'[^\w\s-]', '', slug.lower())
            slug = re.sub(r'[-\s]+', '-', slug).strip('-')
            dest = request.form.get('destination_url', '').strip()
            asin = request.form.get('asin', '').strip()
            if not dest.startswith(('http://', 'https://')):
                flash('Invalid Destination URL. Must start with http:// or https://', 'error')
            elif '/go/' in dest:
                flash('Destination URL cannot point back to a /go/ route (Redirect Loop).', 'error')
            else:
                link = db.session.get(AffiliateLink, int(link_id))
                if link and slug and dest:
                    conflict = AffiliateLink.query.filter_by(slug=slug).first()
                    if conflict and conflict.id != link.id:
                        flash(f'Slug "/go/{slug}" is already used by another link.', 'error')
                    else:
                        try:
                            title = request.form.get('product_title', '').strip()
                            price_str = request.form.get('current_price', '').strip()
                            image = request.form.get('image_url', '').strip()
                            specs_text = request.form.get('specs_raw', '').strip()
                            
                            price = None
                            if price_str:
                                try:
                                    price = float(price_str.replace('€', '').replace('$', '').replace(',', '.').strip())
                                except ValueError:
                                    price = link.current_price
                            
                            link.slug = slug
                            link.destination_url = dest
                            link.asin = asin if asin else None
                            link.product_title = title if title else None
                            link.current_price = price
                            link.image_url = download_and_cache_image(image, keyword=title) if image else None
                            link.features_json = [s.strip() for s in specs_text.split('\n') if s.strip()] if specs_text else None
                            
                            if title or price_str or image or specs_text:
                                link.last_synced_at = datetime.now(timezone.utc)
                            
                            db.session.commit()
                            flash(f'Redirect /go/{slug} updated!', 'success')
                        except Exception:
                            db.session.rollback()
                            flash('Database error occurred.', 'error')
        elif action == 'sync':
            try:
                import sys
                sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
                from sync_prices import sync_all_links
                sync_all_links()
                flash('Live sync complete. Prices and availability updated!', 'success')
            except Exception as e:
                flash(f'Failed to sync: {str(e)}', 'error')
        elif action == 'delete':
            link_id = request.form.get('link_id')
            link    = db.session.get(AffiliateLink, int(link_id))
            if link:
                db.session.delete(link)
                db.session.commit()
                flash('Redirect link deleted.', 'success')
        return redirect(url_for('views.admin_links'))
    links = AffiliateLink.query.order_by(AffiliateLink.id.desc()).all()
    return render_template('blog_admin_links.html', links=links)

# ── Admin: Category Manager ────────────────────────────────────────────────────

@views.route('/admin-cms/categories', methods=['GET', 'POST'])
@admin_required
def admin_categories():
    from .models import Category, BlogPost
    import re
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'add':
            name = request.form.get('name', '').strip()
            slug = request.form.get('slug', '').strip()
            icon = request.form.get('icon', '').strip()
            
            if not name:
                flash('Kategorie-Name ist erforderlich.', 'error')
            else:
                if not slug:
                    slug = re.sub(r'[^\w\s-]', '', name.lower())
                    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
                else:
                    slug = re.sub(r'[^\w\s-]', '', slug.lower())
                    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
                
                existing = Category.query.filter_by(slug=slug).first()
                if existing:
                    flash(f'Slug "{slug}" existiert bereits!', 'error')
                else:
                    try:
                        new_cat = Category(name=name, slug=slug, icon=icon if icon else None)
                        db.session.add(new_cat)
                        db.session.commit()
                        flash(f'Kategorie "{name}" wurde erfolgreich erstellt!', 'success')
                    except Exception:
                        db.session.rollback()
                        flash('Datenbank-Fehler beim Erstellen der Kategorie.', 'error')
                        
        elif action == 'edit':
            cat_id = request.form.get('category_id')
            name = request.form.get('name', '').strip()
            slug = request.form.get('slug', '').strip()
            icon = request.form.get('icon', '').strip()
            
            if not name or not cat_id:
                flash('Ungültige Kategorie-Daten.', 'error')
            else:
                if not slug:
                    slug = re.sub(r'[^\w\s-]', '', name.lower())
                    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
                else:
                    slug = re.sub(r'[^\w\s-]', '', slug.lower())
                    slug = re.sub(r'[-\s]+', '-', slug).strip('-')
                
                category = db.session.get(Category, int(cat_id))
                if category:
                    conflict = Category.query.filter_by(slug=slug).first()
                    if conflict and conflict.id != category.id:
                        flash(f'Slug "{slug}" wird bereits von einer anderen Kategorie verwendet.', 'error')
                    else:
                        try:
                            old_name = category.name
                            category.name = name
                            category.slug = slug
                            category.icon = icon if icon else None
                            
                            if old_name != name:
                                BlogPost.query.filter_by(category_id=category.id).update({BlogPost.category: name})
                                
                            db.session.commit()
                            flash(f'Kategorie "{name}" wurde aktualisiert!', 'success')
                        except Exception:
                            db.session.rollback()
                            flash('Datenbank-Fehler beim Aktualisieren der Kategorie.', 'error')
                            
        elif action == 'delete':
            cat_id = request.form.get('category_id')
            category = db.session.get(Category, int(cat_id))
            if category:
                try:
                    BlogPost.query.filter_by(category_id=category.id).update({
                        BlogPost.category: None,
                        BlogPost.category_id: None
                    })
                    db.session.delete(category)
                    db.session.commit()
                    flash(f'Kategorie "{category.name}" gelöscht und alle Blog-Beiträge aktualisiert.', 'success')
                except Exception:
                    db.session.rollback()
                    flash('Datenbank-Fehler beim Löschen der Kategorie.', 'error')
        return redirect(url_for('views.admin_categories'))
        
    categories = Category.query.order_by(Category.name.asc()).all()
    return render_template('blog_admin_categories.html', categories=categories)

# ── Misc routes ────────────────────────────────────────────────────────────────

@views.route('/demo/comparison')
def comparison_demo():
    return render_template('affiliate_comparison_template.html',
                           post=None, data={},
                           current_date=datetime.now().strftime('%d. %B %Y'))

@views.route('/blog/feed.xml')
def blog_feed():
    posts    = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc()).limit(20).all()
    template = render_template('blog_feed.xml', posts=posts)
    response = make_response(template)
    response.headers['Content-Type'] = 'application/xml'
    return response

@views.route('/go/<slug>')
def affiliate_redirect(slug):
    from .models import AffiliateLink
    link = AffiliateLink.query.filter_by(slug=slug).first()
    if link:
        link.clicks += 1
        db.session.commit()
        return redirect(link.destination_url)
    abort(404)

@views.route('/datenschutz')
def privacy_policy():
    return render_template("privacy.html")

@views.route('/terms')
def terms_of_service():
    return render_template("terms.html")

@views.route('/ueber-uns')
def about():
    return render_template("about.html")

@views.route('/how-we-test')
def how_we_test():
    return render_template("how_we_test.html")

@views.route('/subscribe', methods=['POST'])
def subscribe():
    flash('Thanks for subscribing!', 'success')
    return redirect(url_for('views.home'))

@views.route('/admin/api/upload', methods=['POST'])
@admin_required
@csrf.exempt
def api_upload():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        from werkzeug.utils import secure_filename
        filename = secure_filename(file.filename)
        name, ext = os.path.splitext(filename)
        timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
        unique_filename = f"{name}_{timestamp}{ext}"
        
        upload_folder = os.path.join(current_app.root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)
        
        filepath = os.path.join(upload_folder, unique_filename)
        file.save(filepath)
        
        url = url_for('static', filename=f'uploads/{unique_filename}')
        return jsonify({'url': url})
    return jsonify({'error': 'Unknown upload error'}), 500

@views.route('/admin/api/amazon-fetch/<asin>')
@admin_required
def admin_amazon_fetch(asin):
    import sys
    import os
    # Ensure root is in sys.path
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if root_path not in sys.path:
        sys.path.append(root_path)
        
    try:
        from sync_prices import fetch_amazon_data
        
        # Check if API keys are configured in environment
        client_id = os.getenv('AMAZON_CLIENT_ID')
        client_secret = os.getenv('AMAZON_CLIENT_SECRET')
        partner_tag = os.getenv('AMAZON_PARTNER_TAG')
        
        if (not all([client_id, client_secret, partner_tag]) or 
            any(k.startswith('your-') for k in [client_id, client_secret, partner_tag] if k)):
            # Return MOCK data for testing if credentials are missing
            mock_data = {
                "is_available": True,
                "current_price": 149.99,
                "original_price": 199.99,
                "discount_percentage": 25,
                "product_title": f"[DEMO] Premium Product for ASIN {asin}",
                "image_url": "https://images.unsplash.com/photo-1597571063304-81f08190f3e1?auto=format&fit=crop&w=400&q=80",
                "features": [
                    "Kapazität: 2 TB",
                    "Anschluss: USB-C 3.2 Gen 2x2",
                    "Leserate: Bis zu 2.000 MB/s",
                    "Gewicht: 122g",
                    "Schutzklasse: IP65 robust"
                ],
                "demo_mode": True
            }
            return jsonify(mock_data)
            
        data = fetch_amazon_data(asin)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@views.route('/admin/api/affiliate-link/<path:slug>')
@admin_required
def admin_affiliate_link_fetch(slug):
    from .models import AffiliateLink
    if slug.startswith('/go/'): slug = slug[4:]
    elif slug.startswith('go/'): slug = slug[3:]
    
    link = AffiliateLink.query.filter_by(slug=slug).first()
    if not link:
        return jsonify({"error": f"Affiliate-Link mit dem Slug '/go/{slug}' wurde nicht gefunden."}), 404
        
    return jsonify({
        "product_title": link.product_title,
        "current_price": f"{link.current_price} €" if link.current_price else None,
        "image_url": link.image_url,
        "features": link.features_json if isinstance(link.features_json, list) else []
    })
