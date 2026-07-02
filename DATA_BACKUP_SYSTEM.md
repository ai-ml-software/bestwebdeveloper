# GitHub Issues as Database + JSON Backup System

Complete data persistence and backup solution for your Static Website CMS.

## 🎯 What This Does

Your website data is now backed up in **3 locations** simultaneously:

1. **Browser Local Storage** - Fast, instant access (primary)
2. **Google Sheets** - Via Apps Script API
3. **GitHub Issues** - As individual issues with labels
4. **JSON Files** - Versioned in your repo (`/data/` folder)

This ensures your data **never gets lost** and can be restored from any backup source.

---

## 🚀 Setup Instructions

### Step 1: Add GitHub Token to Repository Secrets

1. Go to your GitHub repository settings: **Settings → Secrets and variables → Actions**
2. Click **New repository secret**
3. Name: `GITHUB_TOKEN` (it's pre-created, but ensure it exists)
4. Value: Will use the default `secrets.GITHUB_TOKEN` automatically

### Step 2: Add Apps Script URL Secret (Optional but Recommended)

1. In **Repository Secrets**, click **New repository secret**
2. Name: `APPS_SCRIPT_URL`
3. Value: Your Apps Script Web App URL (same as in `cms-config.js`)

This allows the GitHub Actions workflow to automatically sync from Google Sheets to GitHub Issues daily.

### Step 3: Check GitHub Actions Workflow

The workflow is automatically set up at `.github/workflows/sync-data.yml`

It runs:
- **Every day at 2 AM UTC** (scheduled)
- **On demand** (manual trigger)
- **On workflow file changes**

To manually trigger:
1. Go to **Actions** tab in your GitHub repository
2. Select **"Sync Data to GitHub Issues & JSON"**
3. Click **Run workflow**

---

## 💾 Using the Admin Interface

In your CMS admin pages (add-blog.html, add-services.html, etc.), you'll see **3 sync buttons**:

```
[Google Sheets] [GitHub Issues] [JSON Backup]
```

### Load Data From:

- **Google Sheets**: Syncs from your configured Apps Script endpoint
- **GitHub Issues**: Reads issues as data (public API, no token needed)
- **JSON Backup**: Loads from `/data/{type}.json` files

### Save Data To:

Your data automatically saves to:
1. **Browser storage** (instant)
2. **Google Sheets** (if Apps Script configured)
3. **GitHub Issues** (if you publish changes via Actions)
4. **JSON backup** (via GitHub Actions daily)

---

## 📊 Data Structure

### GitHub Issues Format

Each record is stored as a GitHub Issue with:

- **Title**: Record title
- **Labels**: Content type (e.g., `content:blog`, `status:published`)
- **Body**: Key-value metadata + content

Example issue:
```
Title: "How to Build a Website"

Labels: content:blog, status:published

Body:
slug: how-to-build-website
category: Web Development
tags: tutorial, web design
publishDate: 2026-07-02
author: Best Web Developer
excerpt: Complete guide to building websites
metaTitle: How to Build a Website | Best Web Developer
metaDescription: Learn web design and development from scratch

contentHtml: >>>
<h2>Introduction</h2>
<p>Building a website involves...</p>
<<<

---
Auto-synced from Google Sheets: 2026-07-02T12:34:56.000Z
```

### JSON Backup Format

Files in `/data/` directory:

```json
// data/blogs.json
[
  {
    "id": "1",
    "title": "How to Build a Website",
    "slug": "how-to-build-website",
    "status": "published",
    "category": "Web Development",
    "tags": "tutorial, web design",
    "publishDate": "2026-07-02",
    "author": "Best Web Developer",
    "metaTitle": "How to Build a Website | Best Web Developer",
    "metaDescription": "Learn web design and development from scratch",
    "contentHtml": "<h2>Introduction</h2><p>...</p>"
  }
]
```

And a combined `backup.json`:
```json
{
  "blogs": [...],
  "services": [...],
  "pages": [...],
  "categories": [...],
  "tags": [...],
  "seo": [...],
  "geo": [...],
  "aeo": [...],
  "_metadata": {
    "synced_at": "2026-07-02T12:34:56.000Z",
    "sync_source": "Google Sheets + GitHub Issues"
  }
}
```

---

## 🔄 Sync Flow

```
┌─────────────────────────────────────────────────────────┐
│ Admin Interface (CMS)                                    │
│ - Create/Edit records                                   │
│ - Choose sync source (Google Sheets/GitHub/JSON)       │
└──────────────┬──────────────────────────────────────────┘
               │
     ┌─────────┴─────────┬──────────────┬──────────────┐
     │                   │              │              │
     ▼                   ▼              ▼              ▼
┌──────────┐    ┌──────────────┐  ┌──────────┐  ┌─────────┐
│ Browser  │    │ Google       │  │ GitHub   │  │ JSON    │
│ Storage  │    │ Sheets       │  │ Issues   │  │ Files   │
└──────────┘    └──────────────┘  └──────────┘  └─────────┘
     │                   │              │              │
     │  ◀─ Manual Sync ─ │              │              │
     │  ◀───── Auto ─────┼──────────────┼──────────────┘
     │       Backup      │
     │     (Daily)       │
     └─────────┬─────────┘
               │
┌──────────────▼──────────────┐
│ GitHub Actions Workflow     │
│ (Runs Daily 2 AM UTC)       │
│ - Fetches from Google Sheets
│ - Syncs to GitHub Issues    │
│ - Saves JSON backups        │
└─────────────────────────────┘
```

---

## 🛟 Data Recovery

If your primary data is lost:

### Option 1: Restore from JSON Backup
1. Click **"JSON Backup"** button in CMS
2. Records load from `/data/{type}.json`

### Option 2: Restore from GitHub Issues
1. Click **"GitHub Issues"** button in CMS
2. Records load from GitHub API (public, no auth needed)

### Option 3: Restore from Google Sheets
1. Click **"Google Sheets"** button in CMS
2. Records load from your Apps Script endpoint

### Option 4: Manual Recovery from Backup
```bash
# Get the latest version from GitHub repo history
git log --oneline data/backup.json
git show COMMIT_HASH:data/backup.json

# Or download from GitHub web interface:
# https://github.com/ai-ml-software/bestwebdeveloper/tree/main/data
```

---

## 🔐 Security Notes

### Public Data
- **GitHub Issues**: Public by default (good for transparency)
- **JSON Files**: Public in repository
- **Google Sheets**: Depends on your sharing settings

### Private Data
- **Browser Storage**: Private to your device
- **GitHub Token**: Keep secret, use repository secrets

### Sensitive Content
If you have sensitive data:
1. Keep Apps Script endpoint private (requires authentication)
2. Don't expose GitHub Issues publicly (make repo private)
3. Encrypt sensitive fields before saving

---

## 📝 API Reference

### Load from GitHub (JavaScript)
```javascript
// In your CMS, these functions are available:

// Load from GitHub Issues
await loadFromGitHub();

// Load from JSON backup
await loadFromJsonBackup();

// Load from Google Sheets
await loadFromSheet();
```

### Manual GitHub Sync (Node.js)
```bash
# Run the sync script
GITHUB_TOKEN=your_token APPS_SCRIPT_URL=your_url node scripts/sync-to-github-issues.js

# Or in GitHub Actions (automatic)
# The workflow at .github/workflows/sync-data.yml handles this
```

---

## 🐛 Troubleshooting

### "GitHub API error: 403"
- Check that `GITHUB_TOKEN` is set in repository secrets
- Token needs `repo` scope for private repos

### "No records found from GitHub"
- Make sure sync has run at least once (check Actions tab)
- Verify labels are correct (e.g., `content:blog`, `status:published`)

### JSON files are empty
- Sync script hasn't run yet
- Check GitHub Actions workflow logs for errors

### Apps Script sync fails
- Verify `APPS_SCRIPT_URL` in `cms-config.js` or repository secret
- Check Apps Script deployment is still active
- Ensure webhook authentication matches

---

## ✨ Features

✅ **Multi-source sync** - Load from Google Sheets, GitHub Issues, or JSON  
✅ **Automatic daily backup** - GitHub Actions syncs at 2 AM UTC  
✅ **Public data resilience** - GitHub Issues can't be deleted by mistake  
✅ **Version control** - All changes tracked in Git  
✅ **No API keys needed** - GitHub API works for public data  
✅ **Simple structure** - Issues as key-value metadata  
✅ **Search-friendly** - GitHub Issues are searchable  
✅ **One-click recovery** - Restore from any backup source  

---

## 📚 Related Files

- **GitHub API Integration**: [`assets/js/github-api.js`](../assets/js/github-api.js)
- **Sync Script**: [`scripts/sync-to-github-issues.js`](../scripts/sync-to-github-issues.js)
- **Workflow**: [`.github/workflows/sync-data.yml`](../.github/workflows/sync-data.yml)
- **Admin CMS**: [`assets/js/admin-cms.js`](../assets/js/admin-cms.js)
- **Data Backups**: [`data/`](../data/)

---

**Last Updated**: 2026-07-02  
**Sync Schedule**: Daily at 2 AM UTC  
**Backup Type**: Google Sheets + GitHub Issues + JSON Files
