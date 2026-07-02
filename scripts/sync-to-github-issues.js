#!/usr/bin/env node
/**
 * Sync Data from Google Sheets to GitHub Issues
 * Usage: node scripts/sync-to-github-issues.js
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// Configuration
const CONFIG = {
  GITHUB_REPO: 'ai-ml-software/bestwebdeveloper',
  GITHUB_TOKEN: process.env.GITHUB_TOKEN || '',
  APPS_SCRIPT_URL: process.env.APPS_SCRIPT_URL || '',
  DATA_TYPES: ['blogs', 'services', 'pages', 'categories', 'tags', 'seo', 'geo', 'aeo']
};

const LABELS_MAP = {
  blogs: 'content:blog',
  services: 'content:service',
  pages: 'content:page',
  categories: 'content:category',
  tags: 'content:tag',
  seo: 'content:seo',
  geo: 'content:geo',
  aeo: 'content:aeo'
};

/**
 * Fetch data from Google Sheets via Apps Script
 */
async function fetchFromGoogleSheets(type) {
  return new Promise((resolve, reject) => {
    if (!CONFIG.APPS_SCRIPT_URL) {
      console.warn(`⚠️  APPS_SCRIPT_URL not set. Skipping ${type} sync from Google Sheets.`);
      resolve([]);
      return;
    }

    const payload = JSON.stringify({ action: 'list', type });
    const url = new URL(CONFIG.APPS_SCRIPT_URL);
    url.searchParams.set('action', 'list');
    url.searchParams.set('type', type);

    https.get(url.toString(), (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const parsed = JSON.parse(data);
          resolve(parsed.records || []);
        } catch (e) {
          console.error(`Failed to parse Google Sheets response for ${type}:`, e.message);
          resolve([]);
        }
      });
    }).on('error', (err) => {
      console.error(`Failed to fetch ${type} from Google Sheets:`, err.message);
      resolve([]);
    });
  });
}

/**
 * Fetch existing GitHub Issues for a type
 */
async function fetchGitHubIssues(type) {
  return new Promise((resolve, reject) => {
    if (!CONFIG.GITHUB_TOKEN) {
      console.warn('⚠️  GITHUB_TOKEN not set. Cannot fetch existing issues.');
      resolve([]);
      return;
    }

    const label = LABELS_MAP[type];
    const options = {
      hostname: 'api.github.com',
      path: `/repos/${CONFIG.GITHUB_REPO}/issues?labels=${encodeURIComponent(label)}&state=all&per_page=100`,
      method: 'GET',
      headers: {
        'Authorization': `token ${CONFIG.GITHUB_TOKEN}`,
        'User-Agent': 'DataSync'
      }
    };

    https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve(JSON.parse(data) || []);
        } catch (e) {
          console.error(`Failed to parse GitHub issues for ${type}:`, e.message);
          resolve([]);
        }
      });
    }).on('error', (err) => {
      console.error(`Failed to fetch GitHub issues for ${type}:`, err.message);
      resolve([]);
    });
  });
}

/**
 * Create or update a GitHub Issue
 */
async function upsertGitHubIssue(type, record, existingIssues) {
  return new Promise((resolve, reject) => {
    if (!CONFIG.GITHUB_TOKEN) {
      console.warn('⚠️  GITHUB_TOKEN not set. Skipping GitHub write.');
      resolve(null);
      return;
    }

    const label = LABELS_MAP[type];
    const title = record.title || record.metaTitle || 'Untitled';
    const body = recordToIssueBody(type, record);
    const labels = [label, record.status === 'published' ? 'status:published' : 'status:draft'];

    // Find existing issue by ID or slug
    let existingIssue = null;
    if (record.id && !isNaN(record.id)) {
      existingIssue = existingIssues.find(i => i.number === parseInt(record.id));
    }
    if (!existingIssue) {
      existingIssue = existingIssues.find(i => 
        i.body.includes(`slug: ${record.slug || record.id}`)
      );
    }

    const isUpdate = !!existingIssue;
    const path = isUpdate 
      ? `/repos/${CONFIG.GITHUB_REPO}/issues/${existingIssue.number}`
      : `/repos/${CONFIG.GITHUB_REPO}/issues`;
    
    const method = isUpdate ? 'PATCH' : 'POST';
    const payload = JSON.stringify({
      title,
      body,
      labels,
      state: record.status === 'archived' ? 'closed' : 'open'
    });

    const options = {
      hostname: 'api.github.com',
      path,
      method,
      headers: {
        'Authorization': `token ${CONFIG.GITHUB_TOKEN}`,
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
        'User-Agent': 'DataSync'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          console.log(`  ${isUpdate ? '✏️  Updated' : '✅ Created'} issue #${result.number}: ${title.slice(0, 50)}...`);
          resolve(result);
        } catch (e) {
          console.error(`Failed to parse response:`, e.message);
          resolve(null);
        }
      });
    });

    req.on('error', (err) => {
      console.error(`Failed to ${isUpdate ? 'update' : 'create'} GitHub issue:`, err.message);
      resolve(null);
    });

    req.write(payload);
    req.end();
  });
}

/**
 * Convert record to GitHub Issue body
 */
function recordToIssueBody(type, record) {
  const lines = [];
  const fieldMap = {
    blogs: ['slug', 'category', 'tags', 'publishDate', 'author', 'readTime', 'excerpt', 'metaTitle', 'metaDescription', 'focusKeyword', 'targetCountry', 'targetCity', 'geoServiceArea', 'aeoQuestion', 'aeoAnswer'],
    services: ['slug', 'category', 'tags', 'priceRange', 'excerpt', 'metaTitle', 'metaDescription', 'focusKeyword', 'targetCountry', 'targetCity', 'geoServiceArea', 'aeoQuestion', 'aeoAnswer'],
    pages: ['slug', 'category', 'tags', 'excerpt', 'metaTitle', 'metaDescription', 'focusKeyword', 'targetCountry', 'targetCity', 'geoServiceArea', 'aeoQuestion', 'aeoAnswer'],
    categories: ['slug', 'parent', 'description'],
    tags: ['slug', 'description'],
    seo: ['slug', 'pageType', 'metaTitle', 'metaDescription', 'focusKeyword', 'targetCountry', 'targetCity'],
    geo: ['slug', 'targetCountry', 'targetCity', 'geoServiceArea', 'address', 'latitude', 'longitude'],
    aeo: ['slug', 'aeoQuestion', 'aeoAnswer', 'faqGroup']
  };

  const fields = fieldMap[type] || [];
  fields.forEach(field => {
    if (record[field]) {
      const value = String(record[field] || '');
      if (value.length > 100 || value.includes('\n')) {
        lines.push(`${field}: >>>`);
        lines.push(value);
        lines.push('<<<');
      } else {
        lines.push(`${field}: ${value}`);
      }
    }
  });

  if (record.contentHtml) {
    lines.push('contentHtml: >>>');
    lines.push(record.contentHtml);
    lines.push('<<<');
  }

  if (record.schemaJson) {
    lines.push('schemaJson: >>>');
    lines.push(record.schemaJson);
    lines.push('<<<');
  }

  lines.push(`\n---\n*Auto-synced from Google Sheets: ${new Date().toISOString()}*`);
  return lines.join('\n');
}

/**
 * Save data to local JSON backup
 */
function saveJsonBackup(type, records) {
  const backupDir = path.join(__dirname, '..', 'data');
  if (!fs.existsSync(backupDir)) {
    fs.mkdirSync(backupDir, { recursive: true });
  }

  const filePath = path.join(backupDir, `${type}.json`);
  fs.writeFileSync(filePath, JSON.stringify(records, null, 2));
  console.log(`💾 Saved ${records.length} ${type} to ${filePath}`);
}

/**
 * Main sync function
 */
async function main() {
  console.log('🔄 Starting data sync: Google Sheets → GitHub Issues + JSON Backup\n');

  let totalSynced = 0;
  const allData = {};

  for (const type of CONFIG.DATA_TYPES) {
    console.log(`📝 Syncing ${type}...`);
    
    // Fetch from Google Sheets
    const sheetsData = await fetchFromGoogleSheets(type);
    console.log(`  📊 Found ${sheetsData.length} records in Google Sheets`);
    
    // Fetch existing GitHub issues
    const existingIssues = await fetchGitHubIssues(type);
    console.log(`  🐙 Found ${existingIssues.length} existing GitHub issues`);

    // Sync each record to GitHub
    let synced = 0;
    for (const record of sheetsData) {
      await upsertGitHubIssue(type, record, existingIssues);
      synced++;
      totalSynced++;
    }

    // Save JSON backup
    saveJsonBackup(type, sheetsData);
    
    allData[type] = sheetsData;
    console.log(`✅ ${type} sync complete\n`);
  }

  // Save combined backup
  const backupPath = path.join(__dirname, '..', 'data', 'backup.json');
  fs.writeFileSync(backupPath, JSON.stringify(allData, null, 2));
  console.log(`\n✨ Sync complete! Total records synced: ${totalSynced}`);
  console.log(`💾 Full backup saved to: ${backupPath}`);
}

// Run
main().catch(err => {
  console.error('❌ Sync failed:', err);
  process.exit(1);
});
