#!/usr/bin/env python3
"""
Comprehensive SEO, AEO, and GEO Optimization Implementation
- Deploy 16-block enterprise schema
- Add Open Graph + Twitter metadata
- Add blog post dates
- Enhance all pages for search engines and AI
"""

import os
import re
from datetime import datetime

# Schema mappings for each page
PAGE_SCHEMAS = {
    'index.html': 'Home Page — WebPage',
    'about.html': 'About Page — AboutPage',
    'services.html': 'Services Page — CollectionPage + ItemList',
    'portfolio.html': 'Portfolio Page — CollectionPage',
    'blog.html': 'Blog Page — Blog',
    'pricing.html': 'Pricing Page — WebPage',
    'contact.html': 'Contact Page — ContactPage',
    'faq.html': 'FAQ Page — FAQPage',
    'testimonials.html': 'Testimonials Page — WebPage',
    'sitemap.html': 'Sitemap Page — WebPage',
    'privacy-policy.html': 'Privacy Policy — WebPage',
    'cookie-policy.html': 'Cookie Policy — WebPage',
    'terms-conditions.html': 'Terms and Conditions — WebPage',
}

# Blog post metadata
BLOG_POSTS = {
    'blog/bootstrap-corporate-websites.html': {
        'title': 'Bootstrap Corporate Websites',
        'description': 'How Bootstrap powers fast, responsive, and professional corporate websites for modern businesses.',
        'published': '2026-05-15',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/bootstrap-corporate-websites.webp',
    },
    'blog/brand-identity-online-trust.html': {
        'title': 'Brand Identity and Online Trust',
        'description': 'Why consistent branding builds credibility and drives conversions in digital environments.',
        'published': '2026-05-10',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/brand-identity-design.webp',
    },
    'blog/email-automation-funnels.html': {
        'title': 'Email Automation Funnels',
        'description': 'How to build email automation funnels that nurture leads, reduce churn, and drive revenue.',
        'published': '2026-05-05',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/email-automation.webp',
    },
    'blog/geo-optimization-for-ai-search.html': {
        'title': 'GEO Optimization for AI Search',
        'description': 'Strategies for optimizing your content for generative AI engines and answer-based search results.',
        'published': '2026-05-01',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/ai-search-optimization.webp',
    },
    'blog/responsive-web-design-conversions.html': {
        'title': 'Responsive Web Design and Conversions',
        'description': 'How responsive web design directly impacts user experience, bounce rates, and conversion metrics.',
        'published': '2026-04-25',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/responsive-design.webp',
    },
    'blog/seo-ready-website-checklist.html': {
        'title': 'SEO-Ready Website Checklist',
        'description': 'A complete checklist for building or auditing a website with strong technical and on-page SEO foundations.',
        'published': '2026-04-20',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/seo-checklist.webp',
    },
    'blog/shopify-product-page-seo.html': {
        'title': 'Shopify Product Page SEO',
        'description': 'Best practices for optimising Shopify product pages for Google rankings and organic traffic growth.',
        'published': '2026-04-15',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/shopify-seo.webp',
    },
    'blog/social-media-content-calendar.html': {
        'title': 'Social Media Content Calendar',
        'description': 'How to plan and execute a social media content calendar that maintains consistency and drives engagement.',
        'published': '2026-04-10',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/social-calendar.webp',
    },
    'blog/technical-seo-site-health.html': {
        'title': 'Technical SEO and Site Health',
        'description': 'A guide to monitoring and improving technical SEO metrics including crawlability, indexation, and Core Web Vitals.',
        'published': '2026-04-05',
        'modified': '2026-06-20',
        'image': 'https://bestwebdeveloper.org/assets/images/technical-seo.webp',
    },
}

# Open Graph & Twitter metadata for pages
PAGE_METADATA = {
    'index.html': {
        'og_title': 'Best Web Developer for Web Design, Development and Marketing',
        'og_description': 'Modern Bootstrap web design, development, SEO, branding, app development, and digital marketing services with SEO and GEO optimized pages.',
        'og_type': 'website',
        'og_image': 'https://bestwebdeveloper.org/assets/images/digital-marketing-services-partner.webp',
    },
    'about.html': {
        'og_title': 'About Best Web Developer',
        'og_description': 'Learn about Best Web Developer — a UK-based digital agency offering premium web design, development, SEO, and marketing services globally.',
        'og_type': 'website',
        'og_image': 'https://bestwebdeveloper.org/assets/images/best-web-developer-logo.png',
    },
    'services.html': {
        'og_title': 'Digital Services | Best Web Developer',
        'og_description': 'Explore SEO optimized web design, development, branding, ecommerce, app development, and digital marketing services.',
        'og_type': 'website',
        'og_image': 'https://bestwebdeveloper.org/assets/images/digital-marketing-services-partner.webp',
    },
    'blog.html': {
        'og_title': 'Best Web Developer Blog',
        'og_description': 'Guides, tips, and insights on web design, SEO, digital marketing, ecommerce, and business growth.',
        'og_type': 'website',
        'og_image': 'https://bestwebdeveloper.org/assets/images/content-marketing-services-strategy.webp',
    },
}

def add_og_metadata(content, filepath):
    """Add Open Graph and Twitter metadata to page head."""
    filename = os.path.basename(filepath)
    
    # Determine metadata based on file
    if filename in PAGE_METADATA:
        meta = PAGE_METADATA[filename]
        og_title = meta['og_title']
        og_desc = meta['og_description']
        og_type = meta['og_type']
        og_image = meta['og_image']
    elif filename.startswith('blog/') and filename in BLOG_POSTS:
        blog_meta = BLOG_POSTS[filename]
        og_title = blog_meta['title']
        og_desc = blog_meta['description']
        og_type = 'article'
        og_image = blog_meta['image']
    else:
        # Skip if not in mapping
        return content
    
    # Check if already has OG tags
    if 'property="og:title"' in content:
        return content
    
    # Create OG metadata block
    og_block = f'''<meta property="og:title" content="{og_title}"/>
<meta property="og:description" content="{og_desc}"/>
<meta property="og:image" content="{og_image}"/>
<meta property="og:type" content="{og_type}"/>
<meta property="og:url" content="https://bestwebdeveloper.org/"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{og_title}"/>
<meta name="twitter:description" content="{og_desc}"/>
<meta name="twitter:image" content="{og_image}"/>
'''
    
    # Insert before </head>
    content = re.sub(r'(</head>)', og_block + r'\1', content)
    return content

def add_blog_dates_to_schema(content, filepath):
    """Add datePublished and dateModified to BlogPosting schemas."""
    filename = os.path.basename(filepath)
    
    if filename not in BLOG_POSTS:
        return content
    
    blog_meta = BLOG_POSTS[filename]
    pub_date = blog_meta['published']
    mod_date = blog_meta['modified']
    image_url = blog_meta['image']
    title = blog_meta['title']
    desc = blog_meta['description']
    
    # Add to BlogPosting schema
    date_block = f',\n      "datePublished": "{pub_date}",\n      "dateModified": "{mod_date}",\n      "image": {{\n        "@type": "ImageObject",\n        "url": "{image_url}",\n        "width": 1200,\n        "height": 630\n      }}'
    
    # Find BlogPosting and inject dates before closing }
    content = re.sub(
        r'("@type": "BlogPosting"[^}]*"breadcrumb":[^}]*})\n      }',
        r'\1' + date_block + '\n      }',
        content
    )
    
    return content

def add_article_schema_to_blog(content, filepath):
    """Add Article mainEntity reference to blog posts."""
    filename = os.path.basename(filepath)
    
    if filename not in BLOG_POSTS:
        return content
    
    # Check if BlogPosting block already has mainEntityOfPage
    if 'mainEntityOfPage' in content:
        return content
    
    blog_url = f"https://bestwebdeveloper.org/{filename.replace('.html', '')}"
    
    # Add mainEntityOfPage to BlogPosting
    main_entity = f',\n      "mainEntityOfPage": {{\n        "@type": "WebPage",\n        "@id": "{blog_url}"\n      }}'
    
    content = re.sub(
        r'("@type": "BlogPosting"[^}]*"author":[^}]*}),\n      "publisher"',
        r'\1' + main_entity + ',\n      "publisher"',
        content
    )
    
    return content

def enhance_page(filepath):
    """Enhance a single page with metadata and schema."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        
        # Add Open Graph metadata
        content = add_og_metadata(content, filepath)
        
        # Add blog dates if applicable
        filename = os.path.basename(filepath)
        if 'blog/' in filepath and filename in BLOG_POSTS:
            content = add_blog_dates_to_schema(content, filepath)
            content = add_article_schema_to_blog(content, filepath)
        
        # Write if changed
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return True
        return False
    except Exception as e:
        print(f"Error: {filepath}: {e}")
        return False

def main():
    """Process all HTML files."""
    print("=" * 70)
    print("COMPREHENSIVE SEO/AEO/GEO OPTIMIZATION - METADATA & SCHEMA ENHANCEMENT")
    print("=" * 70)
    print()
    
    html_files = []
    
    for root, dirs, files in os.walk('/workspaces/bestwebdeveloper'):
        if 'backup' in dirs:
            dirs.remove('backup')
        if '.git' in dirs:
            dirs.remove('.git')
        
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                html_files.append(filepath)
    
    print(f"Found {len(html_files)} HTML files\n")
    
    updated = 0
    for filepath in sorted(html_files):
        # Skip admin/CMS files
        if any(skip in filepath for skip in ['add-', 'admin-', 'gemini-', 'deepseek-', 'seo-score-', 'bestwebdeveloper-seo-report']):
            continue
        
        if enhance_page(filepath):
            rel_path = filepath.replace('/workspaces/bestwebdeveloper/', '')
            print(f"✓ Enhanced: {rel_path}")
            updated += 1
    
    print()
    print("=" * 70)
    print(f"✓ Successfully enhanced {updated} pages with metadata and schema")
    print("=" * 70)
    print()
    print("Next Steps:")
    print("1. Create comprehensive schema blocks from provided file")
    print("2. Create XML sitemaps")
    print("3. Create robots.txt and llms.txt")
    print("4. Verify in Google Search Console")
    print("5. Test in Rich Results Test")

if __name__ == '__main__':
    main()
