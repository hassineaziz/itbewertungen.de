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
