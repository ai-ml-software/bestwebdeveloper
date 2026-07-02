# Best Web Developer - Static CMS with Triple-Redundant Backups

**A complete static website CMS with Google Sheets integration, GitHub Issues database, and automatic JSON backups.**

---

## 📋 Quick Navigation

- [Data Storage System](#-data-storage-system)
- [File Structure](#-file-structure)
- [Important URLs](#-important-urls)
- [How to Save Data](#-how-to-save-data)
- [Publishing Steps](#-publishing-steps)
- [GitHub Backup System](#-github-backup-system)
- [Data Recovery](#-data-recovery)

---

## 🗂️ Data Storage System

Your data is stored in **3 locations simultaneously** for maximum security:

```
┌─────────────────────────────────────────────────────────┐
│                   Your Website Data                     │
└─────────────────────────────────────────────────────────┘
           │                    │                    │
           ▼                    ▼                    ▼
    ┌────────────┐      ┌──────────────┐    ┌─────────────┐
    │  Browser   │      │   Google     │    │   GitHub    │
    │  Storage   │◀────▶│   Sheets     │◀──▶│   Issues    │
    │  (Primary) │      │ (Backup #1)  │    │ (Backup #2) │
    └────────────┘      └──────────────┘    └─────────────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                                ▼
                         ┌─────────────┐
                         │    JSON     │
                         │    Files    │
                         │ (Backup #3) │
                         │   /data/    │
                         └─────────────┘
```

---

## 📁 File Structure

### **Root Level Files**
```
bestwebdeveloper/
├── README.md                          ← You are here
├── index.html                         ← Home page
├── blog.html                          ← Blog listing
├── portfolio.html                     ← Portfolio listing
├── services.html                      ← Services listing
├── contact.html                       ← Contact page
├── admin-dashboard.html               ← CMS admin dashboard
├── add-blog.html                      ← Blog CMS editor
├── add-services.html                  ← Services CMS editor
├── add-pages.html                     ← Pages CMS editor
├── add-categories.html                ← Categories CMS editor
├── add-tags.html                      ← Tags CMS editor
├── add-seo.html                       ← SEO CMS editor
├── add-geo.html                       ← GEO CMS editor
├── add-aeo.html                       ← AEO/FAQ CMS editor
├── seo-score-checker.html             ← SEO scoring tool
└── CNAME                              ← GitHub Pages domain config
```

### **Content Folders**
```
blog/                                  ← Published blog posts
├── index.html                         ← Blog index/listing
├── post-title.html                    ← Individual blog post
└── ...

services/                              ← Published services
├── service-name.html                  ← Service detail page
└── ...

portfolio/                             ← Portfolio projects
├── project-name.html                  ← Project detail page
└── ...

locations/                             ← Location-specific pages
└── ...
```

### **Assets Folder**
```
assets/
├── css/
│   ├── styles.css                     ← Main styles
│   └── admin-cms.css                  ← Admin CMS styles
├── js/
│   ├── cms-config.js                  ← CMS configuration
│   ├── cms-seed-data.js               ← Initial/seed data
│   ├── admin-cms.js                   ← Main CMS logic
│   ├── github-api.js                  ← GitHub Issues API
│   └── main.js                        ← Frontend JS
├── images/                            ← Images & logos
└── data/
    └── [JSON files]                   ← Backup location
```

### **GitHub Files**
```
.github/
└── workflows/
    └── sync-data.yml                  ← Auto-sync workflow (runs daily)

scripts/
└── sync-to-github-issues.js           ← Manual sync script (Node.js)
```

### **Backup & Documentation**
```
data/
├── backup.json                        ← Complete data backup
├── blogs.json                         ← Blog posts only
├── services.json                      ← Services only
├── pages.json                         ← Pages only
├── categories.json                    ← Categories only
├── tags.json                          ← Tags only
├── seo.json                           ← SEO records only
├── geo.json                           ← GEO records only
└── aeo.json                           ← AEO/FAQ records only

DATA_BACKUP_SYSTEM.md                  ← Full backup documentation
GITHUB_ISSUES_QUICK_START.md           ← Quick start guide
SETUP_COMPLETE.md                      ← System overview
```

---

## 🔗 Important URLs

### **CMS Admin Pages**

| Page | URL | Purpose |
|------|-----|---------|
| Admin Dashboard | `/admin-dashboard.html` | Main control center |
| Blog Manager | `/add-blog.html` | Create/edit blog posts |
| Services Manager | `/add-services.html` | Create/edit services |
| Pages Manager | `/add-pages.html` | Create/edit pages |
| Categories Manager | `/add-categories.html` | Manage categories |
| Tags Manager | `/add-tags.html` | Manage tags |
| SEO Manager | `/add-seo.html` | Manage SEO meta data |
| GEO Manager | `/add-geo.html` | Manage geo targeting |
| AEO Manager | `/add-aeo.html` | Manage FAQs |
| SEO Score | `/seo-score-checker.html` | Check SEO scores |

### **Public Pages**

| Page | URL | Purpose |
|------|-----|---------|
| Home | `/index.html` or `/` | Website home |
| Blog | `/blog.html` | Blog listing |
| Services | `/services.html` | Services listing |
| Portfolio | `/portfolio.html` | Portfolio listing |
| Contact | `/contact.html` | Contact form |
| About | `/about.html` | About page |

### **Data Source URLs**

| Service | URL |
|---------|-----|
| GitHub Repository | `https://github.com/ai-ml-software/bestwebdeveloper` |
| GitHub Issues API | `https://api.github.com/repos/ai-ml-software/bestwebdeveloper/issues` |
| Google Sheets | See `cms-config.js` for Spreadsheet ID |
| Google Apps Script | See `APPS_SCRIPT_URL` in repo secrets |
| Website | `https://bestwebdeveloper.org` |

---

## 💾 How to Save Data

### **Method 1: Browser Local Storage (Fastest)**

When you create/edit content in any CMS page:

1. Fill in form fields (title, description, content, etc.)
2. Click **"Save to table"** button
3. Data saves to **browser local storage** instantly ✅

**Location**: Browser's localStorage under key `bwd-cms:{type}`

**Lasts**: Until browser cache is cleared

---

### **Method 2: Google Sheets (Recommended)**

To sync to Google Sheets:

1. **Setup** (One time):
   - Update `assets/js/cms-config.js`:
     ```javascript
     appsScriptUrl: 'https://script.google.com/macros/d/YOUR_ID/userweb'
     ```
   - Deploy Apps Script as Web App (see `apps-script/README_APPS_SCRIPT_SETUP.md`)

2. **Save Data**:
   - Create/edit record in CMS
   - Click **"Save to table"**
   - If Apps Script configured, syncs automatically to Google Sheets ✅

**Location**: Google Sheets (Spreadsheet ID in `cms-config.js`)

**Lasts**: Permanently (unless you delete from Sheets)

---

### **Method 3: GitHub Issues (Automatic)**

To enable GitHub Issues backup:

1. **Setup** (One time):
   - Go to repo **Settings → Secrets and variables → Actions**
   - Add secret: `GITHUB_TOKEN` (already exists by default)
   - Add secret: `APPS_SCRIPT_URL` (paste your Apps Script URL)

2. **Automatic Sync**:
   - GitHub Actions runs **daily at 2 AM UTC**
   - Syncs Google Sheets → GitHub Issues → JSON Files
   - Or manually trigger: **Actions tab → Run workflow**

**Location**: GitHub Issues (with labels like `content:blog`, `status:published`)

**Lasts**: Permanently (version-controlled in Git)

---

### **Method 4: JSON File Backups (Automatic)**

1. **Automatic**: Same as GitHub Issues, runs daily
2. **Manual**: Run this command:
   ```bash
   GITHUB_TOKEN=your_token APPS_SCRIPT_URL=your_url node scripts/sync-to-github-issues.js
   ```

**Location**: `/data/{type}.json` files in repo

**Lasts**: Permanently (versioned in Git)

---

### **Data Storage Summary**

| Storage | When | How | Persistence | Access |
|---------|------|-----|-------------|--------|
| **Browser** | Instant | Auto on save | Until cleared | Fast (local) |
| **Google Sheets** | On save | Via Apps Script | Permanent | API (Sheets) |
| **GitHub Issues** | Daily | Via GitHub Actions | Permanent | API (GitHub) |
| **JSON Files** | Daily | Via GitHub Actions | Permanent | Git (versioned) |

---

## 📝 Publishing Steps

### **Step 1: Access CMS**

1. Go to `/admin-dashboard.html` (or specific editor like `/add-blog.html`)
2. Enter password: `BWD@2026` (change in `cms-config.js`)
3. You're authenticated ✅

### **Step 2: Create New Content**

#### **For Blog Posts** (`/add-blog.html`):
1. Click **"New"** button
2. Fill in:
   - **Title** (H1 heading)
   - **URL Slug** (auto-generated from title)
   - **Category** (e.g., "Web Development")
   - **Tags** (comma-separated: "tutorial, web design")
   - **Published Date** (auto-filled with today)
   - **Author** (auto-filled)
   - **Read Time** (e.g., "6 min read")
   - **Excerpt** (preview text)
   - **Image URL** & **Alt Text**
   - **Meta Title** (35-60 chars, for Google)
   - **Meta Description** (120-160 chars, for Google)
   - **Focus Keyword** (main SEO keyword)
   - **Content** (main HTML body)
   - **Status** (Draft, Published, Archived)
   - Optional: GEO, AEO, Schema, etc.

3. Click **"Save to table"** ✅

#### **For Services** (`/add-services.html`):
1. Click **"New"** button
2. Fill in:
   - **Title** (Service name)
   - **URL Slug** (auto-generated)
   - **Category** (e.g., "Web Services")
   - **Price Range** (e.g., "$500-$2000")
   - **Description** (short description)
   - **Meta Title** & **Description**
   - **Content** (detailed service info)
   - **Status** (Draft or Published)

3. Click **"Save to table"** ✅

#### **For Pages** (`/add-pages.html`):
1. Click **"New"** button
2. Fill in:
   - **Title** (page title)
   - **URL Slug** (auto-generated)
   - **Page Type** (e.g., "About", "FAQ")
   - **Meta Title** & **Description**
   - **Content** (page HTML)
   - **Status** (Draft or Published)

3. Click **"Save to table"** ✅

#### **For Categories** (`/add-categories.html`):
1. Click **"New"** button
2. Fill in:
   - **Title** (category name)
   - **URL Slug** (auto-generated)
   - **Description** (category description)
   - **Parent** (optional, for nested categories)

3. Click **"Save to table"** ✅

#### **For Tags** (`/add-tags.html`):
1. Click **"New"** button
2. Fill in:
   - **Title** (tag name)
   - **URL Slug** (auto-generated)
   - **Description** (tag description)

3. Click **"Save to table"** ✅

### **Step 3: Publish to Website**

#### **Option A: Direct Publishing (Quick)**

In the Data Table (bottom of page):

1. Find your record in the table
2. Click **"Publish"** button (green, only shows for drafts)
3. Status changes from "Draft" to "Published" ✅
4. **File appears on website immediately**

#### **Option B: Via Status Field (Full Edit)**

1. Click **"Edit"** on the record
2. Change **Status** dropdown from "Draft" to "Published"
3. Click **"Save to table"**
4. **File appears on website immediately** ✅

#### **Option C: Bulk Management**

In Data Table:
1. Filter by **Status** dropdown
2. See all drafts, published, or archived items
3. Click **Publish** button for any draft ✅

### **Step 4: Website Sync**

#### **Auto-generated URLs**

Once published, content appears at:

- **Blog**: `https://bestwebdeveloper.org/blog/{slug}`
  - Example: `/blog/how-to-build-website`
  
- **Services**: `https://bestwebdeveloper.org/services/{slug}`
  - Example: `/services/web-design`
  
- **Pages**: `https://bestwebdeveloper.org/{slug}`
  - Example: `/about` or `/contact`

#### **Data Syncs To**:
1. ✅ Browser storage (instant)
2. ✅ Google Sheets (if configured, instant)
3. ✅ GitHub Issues (daily at 2 AM UTC)
4. ✅ JSON files (daily at 2 AM UTC)

---

## 🔄 GitHub Backup System

### **What Gets Backed Up**

Every time you publish:
1. **Browser Storage**: Instant
2. **Google Sheets**: If Apps Script configured
3. **GitHub Issues**: Daily via Actions
4. **JSON Files**: Daily via Actions

### **How to Trigger Manual Sync**

1. Go to **Actions** tab in GitHub
2. Select **"Sync Data to GitHub Issues & JSON"**
3. Click **"Run workflow"** button
4. Monitor progress in the logs

### **View Your Backups**

**GitHub Issues** (Searchable):
- Go to **Issues** tab
- Filter by labels: `content:blog`, `status:published`, etc.
- Each record = one issue

**JSON Files** (Versioned):
- Browse: `https://github.com/ai-ml-software/bestwebdeveloper/tree/main/data`
- Download: Click any `.json` file
- History: Click "History" button on any file

**Git History**:
```bash
# View all backup changes
git log data/backup.json

# See specific version
git show HASH:data/backup.json

# Restore old version
git checkout HASH -- data/
```

---

## 🛟 Data Recovery

### **If Data is Lost**

#### **Option 1: Restore from JSON Backup** (Fastest)

1. Go to any CMS page (e.g., `/add-blog.html`)
2. Click **"JSON Backup"** button
3. **All data loads instantly** ✅

#### **Option 2: Restore from GitHub Issues**

1. Go to any CMS page
2. Click **"GitHub Issues"** button
3. **All data loads from GitHub** ✅

#### **Option 3: Restore from Google Sheets**

1. Go to any CMS page
2. Click **"Google Sheets"** button
3. **All data loads from Sheets** ✅

#### **Option 4: Restore from Git**

```bash
# View previous version
git log data/backup.json

# Restore specific commit
git show COMMIT_HASH:data/backup.json > restored.json

# Or restore entire directory
git checkout COMMIT_HASH -- data/
git commit -m "Restore data from backup"
```

---

## ⚙️ Configuration Files

### **`assets/js/cms-config.js`** (Main Configuration)

```javascript
window.BWD_CMS_CONFIG = {
  // Google Sheets
  appsScriptUrl: 'https://script.google.com/macros/d/YOUR_ID/userweb',
  adminPassword: 'BWD@2026',  // Change this!
  
  // Website
  siteBaseUrl: 'https://bestwebdeveloper.org',
  siteName: 'Best Web Developer',
  
  // Defaults
  defaultAuthor: 'Best Web Developer',
  defaultCountry: 'United States',
  defaultRobots: 'index, follow, max-image-preview:large',
  
  // GitHub
  githubRepo: 'ai-ml-software/bestwebdeveloper'
};
```

### **`assets/js/github-api.js`** (GitHub Integration)

- Handles reading from GitHub Issues API
- No auth needed for public repos
- Labels used for filtering:
  - `content:blog`, `content:service`, `content:page`, etc.
  - `status:published`, `status:draft`, `status:archived`

### **`scripts/sync-to-github-issues.js`** (Data Sync Script)

- Node.js script that syncs Sheets → GitHub Issues → JSON
- Runs automatically via GitHub Actions
- Can run manually:
  ```bash
  node scripts/sync-to-github-issues.js
  ```

### **`.github/workflows/sync-data.yml`** (GitHub Actions)

- Scheduled: Daily at 2 AM UTC
- Syncs Google Sheets → GitHub Issues → JSON Files
- Can trigger manually via GitHub UI

---

## 🚀 Quickstart Checklist

- [ ] 1. Read this README ✓
- [ ] 2. Go to `/admin-dashboard.html`
- [ ] 3. Login with `BWD@2026`
- [ ] 4. Create first blog post in `/add-blog.html`
- [ ] 5. Click **"Save to table"**
- [ ] 6. Click **"Publish"** button
- [ ] 7. View at `/blog/your-slug`
- [ ] 8. Add `APPS_SCRIPT_URL` secret if using Sheets
- [ ] 9. Check `Actions` tab for auto-sync status
- [ ] 10. Done! Data auto-syncs daily 🎉

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| [GITHUB_ISSUES_QUICK_START.md](GITHUB_ISSUES_QUICK_START.md) | 5-minute setup guide |
| [DATA_BACKUP_SYSTEM.md](DATA_BACKUP_SYSTEM.md) | Complete backup documentation |
| [SETUP_COMPLETE.md](SETUP_COMPLETE.md) | System overview |
| [BLOG_POST_QUICK_REFERENCE.md](BLOG_POST_QUICK_REFERENCE.md) | Blog template/reference |

---

## 🔐 Security

**Password**: Change `adminPassword` in `assets/js/cms-config.js`

**Secrets to Add** (GitHub Settings → Secrets):
- `GITHUB_TOKEN` - For publishing to GitHub
- `APPS_SCRIPT_URL` - For syncing Google Sheets

**Data Privacy**:
- Public repo = GitHub Issues visible
- Private repo = GitHub Issues hidden
- Google Sheets = Depends on sharing settings
- Browser = Private to your device

---

## 🐛 Troubleshooting

### Data Not Syncing?
- Check GitHub Actions logs: **Actions** tab
- Verify `APPS_SCRIPT_URL` is set in repo secrets
- Ensure Apps Script is deployed and active

### Can't Access CMS?
- Check password is correct (`BWD@2026`)
- Clear browser cache
- Try incognito/private window

### Changes Not Appearing?
- Click **"Save to table"** (not just form submit)
- Click **"Publish"** to make draft → published
- Check status is "Published" not "Draft"

### Can't Load from GitHub?
- Check repo is public (or token is valid)
- Labels should be: `content:blog`, `status:published`, etc.
- Run manual sync: **Actions** → **Run workflow**

---

## 📞 Support

**CMS Issues**: Check browser console (F12) for errors

**Data Backup**: See [DATA_BACKUP_SYSTEM.md](DATA_BACKUP_SYSTEM.md)

**Quick Setup**: See [GITHUB_ISSUES_QUICK_START.md](GITHUB_ISSUES_QUICK_START.md)

**Apps Script**: See `apps-script/README_APPS_SCRIPT_SETUP.md`

---

## ✨ Summary

```
Save Data Flow:
CMS Form → Browser Storage → Google Sheets → GitHub Issues (daily) → JSON (daily)

Publish Flow:
Create Record → Save to Table → Click Publish → Website Updated (instant)

Backup Flow:
Daily Auto-Sync → GitHub Issues + JSON Files → Git History (version controlled)

Recovery Flow:
Lost Data → Click [JSON Backup] or [GitHub Issues] → Restore (instant)
```

---

**Last Updated**: 2026-07-02  
**System**: Static CMS with Triple-Redundant Backups  
**Status**: ✅ Production Ready
