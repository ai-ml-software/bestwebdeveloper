# Quick Start: GitHub Issues + JSON Backup

## ⚡ 60-Second Setup

### 1. GitHub Actions is Ready ✅
The workflow `.github/workflows/sync-data.yml` is already created.
- Runs **daily at 2 AM UTC**
- Syncs Google Sheets → GitHub Issues → JSON Files

### 2. Add Your Apps Script URL to Secrets
```
Go to: Settings → Secrets and variables → Actions
Click: New repository secret

Name: APPS_SCRIPT_URL
Value: (Paste your Apps Script Web App URL from cms-config.js)
```

### 3. First Manual Sync
Go to **Actions** tab → **"Sync Data to GitHub Issues & JSON"** → **Run workflow**

This will:
- Fetch all data from Google Sheets
- Create GitHub Issues for each record
- Save JSON backups to `/data/` folder

### 4. Start Using the CMS Backup Buttons
In your admin pages (add-blog.html, add-services.html, etc.):

```
[Save]  [New]  [Google Sheets]  [GitHub Issues]  [JSON Backup]  ...
```

---

## 📊 What's Happening Behind the Scenes

```
Your CMS (Browser)
    ↓
Google Sheets ← Syncs to ← GitHub Issues
    ↓
   JSON Files (Versioned in Git)
    ↓
Automatic Daily Backup via GitHub Actions
```

Every piece of data is automatically backed up in **3 places**. Even if one fails, 2 others have your data.

---

## 🎯 Three Ways to Load Data

In your CMS, click any sync button:

| Button | Source | Speed | When to Use |
|--------|--------|-------|------------|
| **Google Sheets** | Apps Script API | Medium | Primary data source |
| **GitHub Issues** | GitHub API | Fast | Quick recovery, testing |
| **JSON Backup** | Local files | Fastest | Offline, instant restore |

---

## 🔄 Automatic Daily Sync

GitHub Actions automatically runs every day at 2 AM UTC:

1. **Fetch from Google Sheets** (via Apps Script)
2. **Create/Update GitHub Issues** (one issue per record)
3. **Save JSON backups** (versioned in Git)
4. **Commit changes** (recorded in Git history)

Check status: **Actions** tab → **"Sync Data to GitHub Issues & JSON"**

---

## 💾 Backup Files Created

After first sync, you'll have:

```
data/
  ├── backup.json          ← Combined all data
  ├── blogs.json           ← Blog posts only
  ├── services.json        ← Services only
  ├── pages.json           ← Pages only
  ├── categories.json      ← Categories only
  ├── tags.json            ← Tags only
  ├── seo.json             ← SEO records only
  ├── geo.json             ← GEO records only
  └── aeo.json             ← AEO FAQs only
```

All versioned in Git, so you can restore any previous version:
```bash
git log data/blogs.json           # See history
git show HASH:data/blogs.json     # View old version
```

---

## 🐙 GitHub Issues Database

After sync, your GitHub repo will have Issues like:

```
✅ "How to Build a Website"
   Labels: content:blog, status:published
   Body: slug: how-to-build-website, category: Web Development, ...

✅ "Web Design Service"
   Labels: content:service, status:published
   Body: slug: web-design, priceRange: $500-$2000, ...

✅ "Blog Post Template"
   Labels: content:blog, status:draft
   Body: slug: blog-post-template, ...
```

**Benefits:**
- ✅ Searchable with GitHub's Issue search
- ✅ Can comment/discuss on each issue
- ✅ Issues can't be accidentally deleted (archive instead)
- ✅ Full version history via GitHub
- ✅ Public backup (if repo is public)

---

## 🆘 If Something Goes Wrong

### Data Lost?
1. Click **[JSON Backup]** button → Data loads instantly
2. Or click **[GitHub Issues]** button → Syncs from GitHub
3. Or use **[Google Sheets]** → Syncs from Sheets

### Sync Failed?
- Check **Actions** tab for error logs
- Verify `APPS_SCRIPT_URL` secret is set correctly
- Manually run: **Actions → Run workflow**

### Want to Reset?
Delete from browser:
```javascript
// In browser console:
localStorage.clear()
// Then reload page and click [JSON Backup] or [GitHub Issues]
```

---

## 📖 Full Documentation

See [`DATA_BACKUP_SYSTEM.md`](DATA_BACKUP_SYSTEM.md) for:
- Complete setup instructions
- Data format details
- API reference
- Security notes
- Advanced configuration

---

## ✨ That's It!

Your data is now backed up in 3 places with automatic daily syncing. 🎉

**No data loss. No migration pain. Just security.**
