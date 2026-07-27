I have a static website hosted on GitHub Pages (custom domain bestwebdeveloper.org) behind Cloudflare. I want to add a blog admin panel at https://bestwebdeveloper.org/admin that allows me to:

- Log in securely with my GitHub account (GitHub OAuth).
- Write and edit blog posts in a rich-text/markdown editor.
- Upload images.
- When I click “Publish”, it creates a Markdown file in the /posts/ folder of my repository and commits it to GitHub.
- A GitHub Action then builds the site and generates clean HTML pages (e.g., https://bestwebdeveloper.org/blog/my-post-slug), never exposing the .md file.

Tech constraints and preferences:
- The main site is purely static HTML/CSS/JS (no backend).
- I use Cloudflare, so a lightweight Cloudflare Worker is acceptable to handle the OAuth callback (no full backend).
- I want to use Decap CMS (formerly Netlify CMS) for the admin interface because it integrates directly with GitHub and runs entirely in the browser.
- The OAuth flow must use a Cloudflare Worker to securely exchange the GitHub auth code for a token (since the static site can’t do this alone).
- The GitHub Action should build the blog posts into clean URLs like /blog/{slug}/index.html using a simple script (or Jekyll/Astro if that’s simpler).
- The whole system must work with my existing site structure, where the main site is in the root and the blog is a sub-section.

Please provide:
1. The exact file structure I need to add to my repository (admin/index.html, admin/config.yml, posts/ example, .github/workflows/deploy.yml, and the Cloudflare Worker code).
2. The fully working Cloudflare Worker script (JavaScript) that handles the GitHub OAuth callback, generates an access token, and returns it to Decap CMS.
3. The admin/index.html that loads Decap CMS from CDN and points to the Worker for authentication.
4. The admin/config.yml for Decap CMS configured for my GitHub repository (owner/repo) with the blog collection, image upload, and editorial workflow if applicable.
5. A GitHub Action workflow that, on push to the main branch, converts Markdown files in /posts/ into HTML pages at /blog/{slug}/index.html (using a simple Node script or a static site generator) and deploys to GitHub Pages.
6. Instructions on how to register the GitHub OAuth App (callback URL pointing to the Worker) and set the necessary environment variables/secrets in Cloudflare and GitHub.

Make sure the final public URLs are clean (no .md extensions) and that the admin panel feels like a real CMS (title, slug, featured image, tags, body with rich editing). The whole setup should be free under Cloudflare’s free tier and GitHub’s limits.
