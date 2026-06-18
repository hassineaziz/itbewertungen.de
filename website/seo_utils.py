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
    
    for i, post in enumerate(top_picks):
        product_name = post.title
        author_name = "Redaktion"
        image_url = post.cover_image_url
        price_val = post.price_from
        rating_val = post.rating

        if post.structured_content and isinstance(post.structured_content, dict):
            sc = post.structured_content
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

