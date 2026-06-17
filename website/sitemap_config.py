import os
from flask import Blueprint, request
from datetime import datetime, timezone

seo_bp = Blueprint('seo', __name__)

def sitemap_generator():
    from .auto_sitemap import generate_auto_sitemap
    for entry in generate_auto_sitemap():
        yield entry

@seo_bp.route('/robots.txt')
def robots_txt():
    base_url = os.getenv('SITE_DOMAIN', request.url_root.rstrip('/'))
    if not base_url.startswith('https://'):
        base_url = base_url.replace('http://', 'https://')
    
    robots_content = f"""User-agent: *
Allow: /

Disallow: /admin/
Disallow: /auth/

Sitemap: {base_url}/sitemap.xml
Sitemap: {base_url}/blog/feed.xml
"""
    return robots_content, 200, {'Content-Type': 'text/plain'}

@seo_bp.route('/sitemap.xml')
def sitemap_xml():
    from flask import Response, url_for
    import xml.etree.ElementTree as ET
    
    try:
        urlset = ET.Element('urlset')
        urlset.set('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9')
        
        entries = list(sitemap_generator())
        
        for entry in entries:
            url_elem = ET.SubElement(urlset, 'url')
            if os.getenv('SITE_DOMAIN'):
                base_domain = os.getenv('SITE_DOMAIN').rstrip('/')
                path = url_for(entry[0], **entry[1])
                url = f"{base_domain}{path}"
            else:
                url = url_for(entry[0], **entry[1], _external=True)
                if url.startswith('http://'):
                    url = url.replace('http://', 'https://')
            
            loc_elem = ET.SubElement(url_elem, 'loc')
            loc_elem.text = url
            
            if entry[2]:
                lastmod_elem = ET.SubElement(url_elem, 'lastmod')
                lastmod_elem.text = entry[2]
            
            if entry[3]:
                changefreq_elem = ET.SubElement(url_elem, 'changefreq')
                changefreq_elem.text = entry[3]
            
            if entry[4]:
                priority_elem = ET.SubElement(url_elem, 'priority')
                priority_elem.text = str(entry[4])
                
        xml_str = ET.tostring(urlset, encoding='unicode', method='xml')
        xml_str = '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_str
        
        return Response(xml_str, mimetype='application/xml')
    except Exception as e:
        return f"Error generating sitemap: {str(e)}", 500

@seo_bp.route('/llms.txt')
def llms_txt():
    from .models import BlogPost
    from flask import url_for, current_app
    
    base_url = os.getenv('SITE_DOMAIN', request.url_root.rstrip('/'))
    if not base_url.startswith('https://'):
        base_url = base_url.replace('http://', 'https://')
        
    site_config = current_app.config.get('SITE_CONFIG', {})
    site_name = site_config.get('brand', {}).get('name', 'ITBewertungen.de')
    site_desc = site_config.get('niche', {}).get('home_description', '')
    
    markdown = []
    markdown.append(f"# {site_name}")
    markdown.append("")
    if site_desc:
        markdown.append(f"> {site_desc}")
        markdown.append("")
        
    markdown.append("## Core Pages")
    markdown.append("")
    markdown.append(f"- [Home]({base_url}/): Hauptseite mit aktuellen Testsiegern und Empfehlungen.")
    markdown.append(f"- [Reviews & Guides]({base_url}/blog): Alle Testberichte, Vergleiche und Ratgeber.")
    markdown.append(f"- [Über Uns]({base_url}/ueber-uns): Informationen über unsere Testkriterien und Redaktion.")
    markdown.append(f"- [Wie wir testen]({base_url}/how-we-test): Details über unsere standardisierten Labor- und Praxistests.")
    markdown.append("")
    
    markdown.append("## Testberichte & Kaufberatung")
    markdown.append("")
    
    try:
        posts = BlogPost.query.filter_by(status='published').order_by(BlogPost.published_at.desc()).all()
        for post in posts:
            path = url_for('views.blog_post', slug=post.slug)
            url = f"{base_url}{path}"
            excerpt = post.excerpt or post.meta_description or ""
            markdown.append(f"- [{post.title}]({url}): {excerpt}")
    except Exception as e:
        markdown.append(f"Error loading posts: {str(e)}")
        
    content = "\n".join(markdown)
    return content, 200, {'Content-Type': 'text/plain; charset=utf-8'}
