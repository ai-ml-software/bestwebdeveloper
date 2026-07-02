Best Web Developer Bootstrap Corporate Modern Website

Upload the contents of this folder to Cloudflare Pages, Netlify, or any static host. The index.html file must be at the first level of the upload. Contact and newsletter forms are front-end validated placeholders and need a backend/form endpoint before production.


CMS UPDATE INCLUDED
-------------------
New password-gated admin pages were added:
- admin-dashboard.html
- add-blog.html
- add-services.html
- add-pages.html
- add-categories.html
- add-tags.html
- add-seo.html
- add-geo.html
- add-aeo.html
- seo-score-checker.html

Default front-end password: BWD@2026
Change it in assets/js/cms-config.js before upload.

Google Sheets / Apps Script:
1. Open the spreadsheet with ID 1zlupdxEyaOhuurdvYi5DhRduXVszY5plN7UFqEfO0X4.
2. Paste apps-script/Code.gs into Extensions > Apps Script.
3. Run setupSheets().
4. Deploy as Web App.
5. Paste the deployment URL into assets/js/cms-config.js.

Important: Static HTML password pages are not strong security. Apps Script validates the password before write actions, but for private business data use a real authenticated backend.

HOW TO POST A BLOG
------------------
1. Open /admin-dashboard and click Blogs, or go directly to /add-blog.
2. Unlock the CMS with the same admin password from assets/js/cms-config.js (default: BWD@2026).
3. Fill in the blog record:
   - Title
   - URL slug (for example: right-tech-stack-business-website)
   - Category, tags, excerpt, main content HTML
   - SEO fields: meta title, meta description, focus keyword, canonical URL
   - Status: published or draft
4. Click Save to table.
5. If you want the post to sync to Google Sheets, click Sync Google Sheet after the Apps Script Web App URL is configured.
6. Publish the actual page file in the /blog folder using the same slug, for example /blog/right-tech-stack-business-website.html.
7. Make sure the blog card and internal links on /blog.html point to the same slug so the post appears in the public site flow.
8. For new posts, also add the matching entry to assets/data/cms-seed-data.js if you want it to appear in the admin UI immediately on a fresh local load.
