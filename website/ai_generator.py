import os
import json
import logging
import requests
import time
from website.models import AffiliateLink, BlogPost

logger = logging.getLogger(__name__)

def generate_article(
    focus_keyword,
    secondary_keywords,
    category,
    template_name,
    core_product_slugs,
    product_overrides=None
):
    """
    Constructs the dynamic SEO prompt and coordinates the REST call to Gemini LLM.
    Returns the parsed JSON response matching the database post format.
    """
    
    # 1. Verify API Key
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY is not configured in the server environment (.env file).")

    # 2. Resolve Core Product Specs from Database & Form Overrides
    core_products_context = []
    if core_product_slugs:
        for slug in core_product_slugs:
            link = AffiliateLink.query.filter_by(slug=slug).first()
            override = product_overrides.get(slug, {}) if product_overrides else {}
            raw_source = override.get('raw_source_info', '')
            
            product_str = ""
            if link:
                specs_list = ""
                if link.features_json:
                    if isinstance(link.features_json, list):
                        specs_list = "\n".join([f"- {f}" for f in link.features_json])
                    elif isinstance(link.features_json, dict):
                        specs_list = "\n".join([f"- {k}: {v}" for k, v in link.features_json.items()])
                
                product_str += (
                    f"Product Name: {link.product_title or slug}\n"
                    f"Price: {link.current_price or 'N/A'}\n"
                    f"Image URL: {link.image_url or 'N/A'}\n"
                    f"Affiliate Slug: {slug}\n"
                    f"Specifications:\n{specs_list}\n"
                )
            else:
                product_str += f"Product Name: {slug}\nAffiliate Slug: {slug}\n"
                
            if raw_source:
                product_str += f"Additional Raw Copied Info / Specs:\n{raw_source}\n"
                
            core_products_context.append(product_str)
    
    product_specs_context_str = "\n\n---\n\n".join(core_products_context)
    
    # Handle global fallback specs if present
    if product_overrides and 'global_custom' in product_overrides:
        global_raw = product_overrides['global_custom'].get('raw_source_info')
        if global_raw:
            product_specs_context_str += f"\n\nAdditional Raw Copied Info / Specs:\n{global_raw}\n"

    # 3. Resolve Alternatives in Niche (Same Category Link Resolution)
    # Fetch up to 10 active affiliate links in database that aren't the main selection
    alt_links = AffiliateLink.query.filter(
        AffiliateLink.product_title != None
    ).limit(15).all()
    
    alternatives_pool = []
    for l in alt_links:
        if l.slug not in (core_product_slugs or []):
            alternatives_pool.append(f"- Name: {l.product_title} (Affiliate Slug: {l.slug}, Price: {l.current_price or 'N/A'})")
    
    alternatives_context_str = "\n".join(alternatives_pool) if alternatives_pool else "No active alternative links available in the DB."

    # 4. Resolve Dynamic Internal Links for Siloing
    # Fetch 5 most recent published posts in same category, and 5 site-wide
    same_category_posts = BlogPost.query.filter(
        BlogPost.status == 'published',
        BlogPost.category.ilike(category)
    ).order_by(BlogPost.published_at.desc()).limit(5).all()
    
    sitewide_posts = BlogPost.query.filter(
        BlogPost.status == 'published'
    ).order_by(BlogPost.published_at.desc()).limit(5).all()
    
    internal_links_list = []
    seen_slugs = set()
    
    for p in same_category_posts:
        internal_links_list.append(f"- [Category Match] {p.title} (URL path: /blog/{p.slug})")
        seen_slugs.add(p.slug)
        
    for p in sitewide_posts:
        if p.slug not in seen_slugs:
            internal_links_list.append(f"- [Site-wide Match] {p.title} (URL path: /blog/{p.slug})")
            
    internal_links_str = "\n".join(internal_links_list) if internal_links_list else "No existing published articles on the site."

    # 5. Format Sliders / Quick Notes for Hands-on EEAT Steering
    steering_instructions = ""
    
    has_steering_data = False
    if product_overrides:
        for slug, override in product_overrides.items():
            sliders = override.get('slider_data')
            quick_notes = override.get('quick_notes')
            if sliders or quick_notes:
                has_steering_data = True
                break
                
    if has_steering_data:
        steering_instructions += "The reviewer provided the following hands-on assessment metrics for specific products to steer the review sentiment:\n"
        for slug, override in product_overrides.items():
            sliders = override.get('slider_data')
            quick_notes = override.get('quick_notes')
            if sliders or quick_notes:
                steering_instructions += f"\n### Product: {slug}\n"
                if sliders:
                    for k, v in sliders.items():
                        steering_instructions += f"- {k}: {v} / 1.0 (Higher means positive/outstanding, lower means critical/poor)\n"
                if quick_notes:
                    steering_instructions += f"- Reviewer Quick Notes: \"{quick_notes}\"\n"
                    
        steering_instructions += (
            "\nCRITICAL: Weave these observations directly into the product summaries, pros/cons, "
            "and verdict sections using authentic first-person German test phrases (e.g. 'In unserem Praxistest...', "
            "'Besonders positiv ist uns aufgefallen...'). Keep ratings and pros/cons mathematically aligned with the sliders."
        )
    else:
        steering_instructions = "No sliders or custom observations are provided. Rely on manufacturer specifications in an objective tone."

    # 6. Read Prompt Template File
    prompt_file_map = {
        'standard': 'standard_post_prompt.md',
        'product_review_template': 'product_review_prompt.md',
        'best_x_for_y_template': 'best_x_for_y_prompt.md',
        'affiliate_comparison_template': 'affiliate_comparison_prompt.md'
    }
    
    prompt_filename = prompt_file_map.get(template_name, 'standard_post_prompt.md')
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    prompt_path = os.path.join(project_root, 'seo_prompts', prompt_filename)
    
    try:
        with open(prompt_path, 'r', encoding='utf-8') as f:
            prompt_content = f.read()
    except Exception as e:
        logger.error(f"Error reading prompt template file: {e}")
        raise FileNotFoundError(f"Could not open prompt template at {prompt_path}")

    # 7. Interpolate Placeholders
    # Handle multiple placeholder formats supported in our files
    prompt_content = prompt_content.replace("[INSERT_FOCUS_KEYWORD]", focus_keyword)
    prompt_content = prompt_content.replace("[INSERT TARGET FOCUS KEYWORD HERE]", focus_keyword)
    
    prompt_content = prompt_content.replace("[INSERT_LSI_KEYWORDS]", secondary_keywords)
    prompt_content = prompt_content.replace("[INSERT SECONDARY KEYWORDS HERE]", secondary_keywords)
    
    prompt_content = prompt_content.replace("[INSERT PRODUCT SPECIFICATIONS / WEBSITE TEXT COPIED HERE]", product_specs_context_str)
    
    prompt_content = prompt_content.replace("[INSERT MAIN CATEGORY HERE]", category)
    prompt_content = prompt_content.replace("[INSERT_CATEGORY]", category)
    
    # Insert EEAT sliders / notes context
    prompt_content = prompt_content.replace(
        "[INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH COMPARED PRODUCT]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH RANK]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT ANECDOTAL NOTES FOR EACH COMPARED PRODUCT]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT ANECDOTAL NOTES FOR EACH RANK]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT ANECDOTAL NOTES HERE]",
        steering_instructions
    )
    prompt_content = prompt_content.replace(
        "[INSERT METRICS FOR VALUE, BUILD QUALITY, USABILITY, EXPECTATION MATCH FOR EACH COMPARED PRODUCT]",
        steering_instructions
    )

    # Append additional contextual inputs as System Instructions
    final_prompt = (
        f"{prompt_content}\n\n"
        "### DYNAMIC CONTEXT ENGINE INPUTS\n"
        f"Use the following database parameters when generating sections, lists, and links:\n"
        f"1. CATEGORY: {category}\n"
        f"2. ALTERNATIVES DATABASE LIST (for alternatives section if layout supports it):\n{alternatives_context_str}\n\n"
        f"3. SILO INTERNAL LINKS POOL (prioritize category matches, fallback to site-wide matches. "
        f"ONLY include these links if they naturally fit within the text. DO NOT force them. NEVER create a 'Verwandte Artikel' list):\n{internal_links_str}\n"
    )

    # 8. Call Gemini REST Endpoint
    models_to_try = [
        "gemini-2.5-flash",
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-2.0-flash-lite",
        "gemini-2.5-pro",
        "gemini-1.5-pro",
        "gemini-pro-latest",
        "gemini-flash-latest",
        "gemini-flash-lite-latest",
        "gemini-3.5-flash"
    ]
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
                            "text": final_prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "responseMimeType": "application/json"
            }
        }
        
        logger.info(f"Initiating generateContent REST request to model {model_name}...")
        
        try:
            response = requests.post(api_url, headers=headers, json=payload, timeout=90)
            response.raise_for_status()
            result_json = response.json()
            break  # Success!
        except requests.exceptions.HTTPError as err:
            last_err = err
            if response.status_code in [400, 401, 403, 404]:
                logger.error(f"Gemini API request failed for {model_name} with client/auth error: {err}")
            logger.warning(f"Model {model_name} returned transient error {response.status_code}. Retrying with fallback model after short delay...")
            time.sleep(3)
            continue
        except Exception as err:
            last_err = err
            logger.warning(f"Gemini API request failed for {model_name}: {err}. Retrying with fallback model after short delay...")
            time.sleep(3)
            continue
    else:
        # All models failed
        raise RuntimeError(f"API request failed: All models rate-limited or failed. Last error: {last_err}")
        
    # 9. Extract and Parse the JSON Output
    try:
        candidates = result_json.get("candidates", [])
        if not candidates:
            raise ValueError("No response candidates returned by the Gemini API model.")
            
        content_parts = candidates[0].get("content", {}).get("parts", [])
        if not content_parts:
            raise ValueError("Candidate response parts list is empty.")
            
        raw_text = content_parts[0].get("text", "").strip()
        
        # Clean any accidental markdown code fencing ```json ... ```
        if raw_text.startswith("```"):
            lines = raw_text.splitlines()
            if lines[0].startswith("```json") or lines[0].startswith("```"):
                raw_text = "\n".join(lines[1:-1])
        
        parsed_data = json.loads(raw_text, strict=False)
        return parsed_data
        
    except json.JSONDecodeError as jde:
        logger.error(f"JSON parsing error: {jde}. Raw response text was:\n{raw_text}")
        raise ValueError(f"The model did not return valid JSON content: {jde}. Output was:\n{raw_text[:200]}")
    except Exception as e:
        logger.error(f"Failed to resolve generation response structure: {e}")
        raise
