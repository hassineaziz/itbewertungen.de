from flask import url_for

def itemlist_schema(top_picks, config):
    if not top_picks:
        return {}
    items = []
    domain = config.get('seo', {}).get('domain', '').rstrip('/')
    for i, post in enumerate(top_picks):
        product_name = post.title
        author_name = "Redaktion"
        if post.structured_content and isinstance(post.structured_content, dict):
            product_name = post.structured_content.get('product_name', post.title)
            author_name = post.structured_content.get('author_name', 'Redaktion')

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
                    "name": product_name
                },
                "reviewRating": {
                    "@type": "Rating",
                    "ratingValue": post.rating if post.rating else "0",
                    "bestRating": "10"
                }
            }
        })
    return {
        "@context": "https://schema.org",
        "@type": "ItemList",
        "itemListElement": items
    }
