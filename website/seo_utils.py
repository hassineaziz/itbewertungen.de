import re
from flask import url_for

def clean_price_str(price_str):
    if not price_str:
        return "0.00"
    price_str = str(price_str)
    p = price_str.replace('$', '').replace('€', '').replace('£', '').replace(',', '.').strip()
    match = re.search(r'\d+(?:\.\d+)?', p)
    if match:
        return match.group(0)
    return p

def itemlist_schema(top_picks, config):
    if not top_picks:
        return {}
    items = []
    domain = config.get('seo', {}).get('domain', '').rstrip('/')
    brand_name = config.get('brand', {}).get('name', 'Brand')
    
    from website.views import resolve_affiliate_details_in_data
    import copy
    
    for i, post in enumerate(top_picks):
        product_name = post.title
        author_name = "Redaktion"
        image_url = post.cover_image_url
        price_val = post.price_from
        rating_val = post.rating

        if post.structured_content and isinstance(post.structured_content, dict):
            sc = resolve_affiliate_details_in_data(copy.deepcopy(post.structured_content))
            product_name = sc.get('product_name', product_name)
            author_name = sc.get('author_name', author_name)
            
            # Extract first product details if list is present
            for list_key in ['products', 'picks']:
                if list_key in sc and isinstance(sc[list_key], list) and len(sc[list_key]) > 0:
                    first_p = sc[list_key][0]
                    if isinstance(first_p, dict):
                        if product_name == post.title:
                            product_name = first_p.get('name', product_name)
                        if not image_url:
                            image_url = first_p.get('image_url')
                        if not price_val:
                            price_val = first_p.get('price')
                        if not rating_val:
                            rating_val = first_p.get('rating')
                    break

        price_cleaned = clean_price_str(price_val)
        rating_str = str(rating_val) if rating_val else "10"
        final_image = image_url if image_url else f"{domain}/static/favicon.png"

        items.append({
            "@type": "ListItem",
            "position": i + 1,
            "item": {
                "@type": "Review",
                "url": f"{domain}{url_for('views.blog_post', slug=post.slug)}",
                "name": post.title,
                "author": {
                    "@type": "Person",
                    "name": author_name
                },
                "itemReviewed": {
                    "@type": "Product",
                    "name": product_name,
                    "image": final_image,
                    "description": post.excerpt or post.meta_description or f"Ausführlicher Testbericht und Bewertung für {product_name}.",
                    "brand": {
                        "@type": "Brand",
                        "name": brand_name
                    },
                    "aggregateRating": {
                        "@type": "AggregateRating",
                        "ratingValue": rating_str,
                        "bestRating": "10",
                        "ratingCount": 1
                    },
                    "offers": {
                        "@type": "Offer",
                        "price": price_cleaned,
                        "priceCurrency": "EUR",
                        "availability": "https://schema.org/InStock",
                        "shippingDetails": {
                            "@type": "OfferShippingDetails",
                            "shippingRate": {
                                "@type": "MonetaryAmount",
                                "value": 0,
                                "currency": "EUR"
                            },
                            "shippingDestination": {
                                "@type": "DefinedRegion",
                                "addressCountry": "DE"
                            },
                            "deliveryTime": {
                                "@type": "ShippingDeliveryTime",
                                "handlingTime": {
                                    "@type": "QuantitativeValue",
                                    "minValue": 0,
                                    "maxValue": 2,
                                    "unitCode": "DAY"
                                },
                                "transitTime": {
                                    "@type": "QuantitativeValue",
                                    "minValue": 1,
                                    "maxValue": 5,
                                    "unitCode": "DAY"
                                }
                            }
                        },
                        "hasMerchantReturnPolicy": {
                            "@type": "MerchantReturnPolicy",
                            "applicableCountry": "DE",
                            "returnPolicyCategory": "https://schema.org/MerchantReturnFiniteReturnWindow",
                            "merchantReturnDays": 14,
                            "returnMethod": "https://schema.org/ReturnByMail",
                            "returnFees": "https://schema.org/FreeReturn"
                        }
                    }
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": rating_str,
                    "bestRating": "10"
                }
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items
    }


def download_and_cache_image(url, keyword=None):
    """
    Downloads an image from an external URL, saves it locally under website/static/uploads/
    with a name based on the slugified keyword (if provided) or url hash, and returns the local URL path.
    If the URL is already local or empty, it is returned unchanged.
    """
    if not url:
        return url
    if not url.startswith('http'):
        return url

    import os
    import re
    import hashlib
    import requests
    from flask import current_app

    try:
        # Determine the root path to the static folder
        try:
            root_path = current_app.root_path
        except RuntimeError:
            # Fallback for scripts running outside Flask context (e.g. sync_prices.py)
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website')
            if not os.path.exists(root_path):
                # if current folder is website/
                root_path = os.path.dirname(os.path.abspath(__file__))

        upload_folder = os.path.join(root_path, 'static', 'uploads')
        os.makedirs(upload_folder, exist_ok=True)

        # Parse filename to get extension or fall back to .jpg
        path_part = url.split('?')[0].split('#')[0]
        _, url_ext = os.path.splitext(path_part)
        ext = url_ext.lower()
        if ext not in ['.jpg', '.jpeg', '.png', '.gif', '.webp', '.svg']:
            ext = '.jpg'

        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        
        # Build keyword-based filename if keyword is provided
        if keyword:
            # Slugify the keyword
            safe_keyword = re.sub(r'[^\w\s-]', '', keyword.lower())
            safe_keyword = re.sub(r'[-\s]+', '-', safe_keyword).strip('-')
            # E.g. to translate German umlauts
            safe_keyword = safe_keyword.replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
            # Clean again in case umlaut replacement introduced non-alphanumerics
            safe_keyword = re.sub(r'[^a-z0-9-]', '', safe_keyword)
            # Append short 8-char hash of the URL to ensure uniqueness
            filename = f"{safe_keyword}_{url_hash[:8]}{ext}"
        else:
            filename = f"cached_{url_hash}{ext}"
            
        filepath = os.path.join(upload_folder, filename)

        # Check if the file already exists locally to avoid duplicate requests
        if os.path.exists(filepath):
            return f"/static/uploads/{filename}"

        # Download the image
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        # Update extension based on the actual Content-Type if necessary
        content_type = response.headers.get('content-type', '')
        new_ext = ext
        if 'image/png' in content_type:
            new_ext = '.png'
        elif 'image/gif' in content_type:
            new_ext = '.gif'
        elif 'image/webp' in content_type:
            new_ext = '.webp'
        elif 'image/svg' in content_type:
            new_ext = '.svg'
        elif 'image/jpeg' in content_type or 'image/jpg' in content_type:
            new_ext = '.jpg'

        if new_ext != ext:
            if keyword:
                filename = f"{safe_keyword}_{url_hash[:8]}{new_ext}"
            else:
                filename = f"cached_{url_hash}{new_ext}"
            filepath = os.path.join(upload_folder, filename)
            if os.path.exists(filepath):
                return f"/static/uploads/{filename}"

        with open(filepath, 'wb') as f:
            f.write(response.content)

        return f"/static/uploads/{filename}"
    except Exception as e:
        try:
            current_app.logger.warning(f"Failed to download image {url}: {e}")
        except RuntimeError:
            print(f"Failed to download image {url}: {e}")
        return url


def download_images_in_structured_content(data, keyword=None):
    """
    Recursively searches structured data (dict or list) for 'image_url' keys,
    downloads the external images, and updates them to the locally cached URLs using the keyword.
    """
    if isinstance(data, dict):
        new_dict = {}
        for k, v in data.items():
            if k == 'image_url' and isinstance(v, str) and v.startswith('http'):
                new_dict[k] = download_and_cache_image(v, keyword=keyword)
            else:
                new_dict[k] = download_images_in_structured_content(v, keyword=keyword)
        return new_dict
    elif isinstance(data, list):
        return [download_images_in_structured_content(item, keyword=keyword) for item in data]
    else:
        return data



