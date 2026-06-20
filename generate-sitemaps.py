#!/usr/bin/env python3
"""
Generate comprehensive XML sitemaps for Best Web Developer
- sitemap.xml (index)
- sitemap-pages.xml
- sitemap-services.xml
- sitemap-blog.xml
- sitemap-portfolio.xml
- sitemap-locations.xml
- sitemap-images.xml
"""

import os
from datetime import datetime

DOMAIN = "https://bestwebdeveloper.org"
LAST_MODIFIED = "2026-06-20"

def get_pages():
    """Get all main pages."""
    return [
        ("", 1.0, "daily"),  # Home
        ("about", 0.9, "monthly"),
        ("services", 0.95, "weekly"),
        ("blog", 0.9, "weekly"),
        ("portfolio", 0.9, "monthly"),
        ("pricing", 0.8, "monthly"),
        ("contact", 0.8, "monthly"),
        ("faq", 0.8, "monthly"),
        ("testimonials", 0.8, "monthly"),
        ("sitemap", 0.7, "yearly"),
        ("privacy-policy", 0.5, "yearly"),
        ("cookie-policy", 0.5, "yearly"),
        ("terms-conditions", 0.5, "yearly"),
    ]

def get_services():
    """Get all service pages."""
    services = [
        "web-design-development",
        "ui-ux-design",
        "web-development",
        "wordpress-development",
        "ecommerce-development",
        "search-engine-optimization-services",
        "digital-marketing-services",
        "email-marketing-near-me",
        "content-marketing-services",
        "social-media-agency",
        "brand-designs-services",
        "android-app-development",
        "illustration-services",
        "on-page-seo-services",
        "off-page-seo-services",
        "technical-seo-services",
        "local-seo-services",
        "ppc-google-ads",
        "youtube-marketing",
        "youtube-ads",
        "streaming-platforms",
        "spotify-streaming",
        "soundcloud-streaming",
        "music-marketing",
        "music-website",
        "artist-development-services",
        "non-profit-services",
        "video-production-services",
    ]
    return [(f"services/{s}", 0.85, "monthly") for s in services]

def get_blogs():
    """Get all blog posts."""
    blogs = [
        "bootstrap-corporate-websites",
        "brand-identity-online-trust",
        "email-automation-funnels",
        "geo-optimization-for-ai-search",
        "responsive-web-design-conversions",
        "seo-ready-website-checklist",
        "shopify-product-page-seo",
        "social-media-content-calendar",
        "technical-seo-site-health",
    ]
    return [(f"blog/{b}", 0.8, "weekly") for b in blogs]

def get_portfolio():
    """Get all portfolio pages."""
    portfolio = [
        "corporate-website-redesign",
        "shopify-growth-store",
        "seo-authority-buildout",
        "mobile-app-launch",
        "brand-identity-system",
        "digital-campaign-engine",
    ]
    return [(f"portfolio/{p}", 0.85, "monthly") for p in portfolio]

def get_locations():
    """Get all location pages."""
    locations = [
        "uk-digital-marketing-services",
        "usa-digital-marketing-services",
        "phoenix-digital-marketing",
        "scottsdale-digital-marketing",
        "tempe-digital-marketing",
    ]
    return [(f"locations/{l}", 0.8, "monthly") for l in locations]

def generate_page_entry(url, priority, changefreq, lastmod=LAST_MODIFIED):
    """Generate a single URL entry for sitemap."""
    return f"""  <url>
    <loc>{DOMAIN}/{url}</loc>
    <lastmod>{lastmod}</lastmod>
    <changefreq>{changefreq}</changefreq>
    <priority>{priority}</priority>
  </url>"""

def generate_sitemap_xml(pages):
    """Generate sitemap XML content."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for url, priority, changefreq in pages:
        if url == "":
            # Home page
            xml += generate_page_entry("", priority, changefreq) + "\n"
        else:
            xml += generate_page_entry(url, priority, changefreq) + "\n"
    
    xml += '</urlset>'
    return xml

def generate_image_sitemap(image_paths):
    """Generate image sitemap XML."""
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\n'
    xml += '           xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'
    
    # Add images from key pages
    images = [
        ("", ["digital-marketing-services-partner.webp"]),
        ("services/web-design-development", ["web-design-development-agency-team.webp"]),
        ("services/ui-ux-design", ["ui-ux-design-interface.webp"]),
        ("portfolio/corporate-website-redesign", ["web-design-development-agency-team.webp"]),
        ("portfolio/shopify-growth-store", ["shopify-website-development-services.webp"]),
        ("portfolio/seo-authority-buildout", ["seo-digital-marketing-rocket.webp"]),
        ("blog/bootstrap-corporate-websites", ["bootstrap-corporate-websites.webp"]),
        ("blog/seo-ready-website-checklist", ["seo-checklist.webp"]),
        ("blog/technical-seo-site-health", ["technical-seo.webp"]),
    ]
    
    for page, img_files in images:
        url = page if page else ""
        xml += f'\n  <url>\n    <loc>{DOMAIN}/{url}</loc>\n'
        
        for img in img_files:
            xml += f'    <image:image>\n'
            xml += f'      <image:loc>{DOMAIN}/assets/images/{img}</image:loc>\n'
            xml += f'      <image:title>{img.replace("-", " ").replace(".webp", "")}</image:title>\n'
            xml += f'    </image:image>\n'
        
        xml += '  </url>\n'
    
    xml += '</urlset>'
    return xml

def generate_sitemap_index():
    """Generate the main sitemap index."""
    sitemaps = [
        "sitemap-pages.xml",
        "sitemap-services.xml",
        "sitemap-blog.xml",
        "sitemap-portfolio.xml",
        "sitemap-locations.xml",
        "sitemap-images.xml",
    ]
    
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for sitemap in sitemaps:
        xml += f'''  <sitemap>
    <loc>{DOMAIN}/{sitemap}</loc>
    <lastmod>{LAST_MODIFIED}</lastmod>
  </sitemap>
'''
    
    xml += '</sitemapindex>'
    return xml

def main():
    """Generate all sitemaps."""
    print("=" * 70)
    print("GENERATING COMPREHENSIVE XML SITEMAPS")
    print("=" * 70)
    print()
    
    base_dir = "/workspaces/bestwebdeveloper"
    
    # Generate individual sitemaps
    sitemaps = {
        "sitemap-pages.xml": get_pages(),
        "sitemap-services.xml": get_services(),
        "sitemap-blog.xml": get_blogs(),
        "sitemap-portfolio.xml": get_portfolio(),
        "sitemap-locations.xml": get_locations(),
    }
    
    for filename, pages in sitemaps.items():
        xml_content = generate_sitemap_xml(pages)
        filepath = os.path.join(base_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(xml_content)
        
        print(f"✓ Created {filename} ({len(pages)} URLs)")
    
    # Generate image sitemap
    image_sitemap = generate_image_sitemap([])
    with open(os.path.join(base_dir, "sitemap-images.xml"), 'w', encoding='utf-8') as f:
        f.write(image_sitemap)
    print(f"✓ Created sitemap-images.xml")
    
    # Generate main sitemap index
    index_xml = generate_sitemap_index()
    with open(os.path.join(base_dir, "sitemap.xml"), 'w', encoding='utf-8') as f:
        f.write(index_xml)
    print(f"✓ Created sitemap.xml (index)")
    
    print()
    print("=" * 70)
    print("✓ All sitemaps generated successfully!")
    print("=" * 70)
    print()
    print("Sitemap Summary:")
    total_urls = sum(len(pages) for pages in sitemaps.values())
    print(f"- Total URLs in sitemaps: {total_urls}")
    print(f"- Service pages: {len(get_services())}")
    print(f"- Blog posts: {len(get_blogs())}")
    print(f"- Portfolio pages: {len(get_portfolio())}")
    print(f"- Location pages: {len(get_locations())}")
    print(f"- Main pages: {len(get_pages())}")
    print()
    print("Submit to Google Search Console:")
    print("https://search.google.com/search-console")
    print()
    print("Verify sitemaps at:")
    print("https://bestwebdeveloper.org/sitemap.xml")

if __name__ == '__main__':
    main()
