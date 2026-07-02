/**
 * GitHub Issues as a Database (Data Backup & Sync)
 * Syncs blog posts, services, pages, categories, tags, SEO, GEO, AEO to GitHub Issues
 */
(function(){
  'use strict';
  
  window.GitHubDataAPI = {
    repo: 'ai-ml-software/bestwebdeveloper', // Update with your repo
    apiUrl: 'https://api.github.com/repos',
    
    // Label mapping for content types
    labels: {
      blogs: 'content:blog',
      services: 'content:service',
      pages: 'content:page',
      categories: 'content:category',
      tags: 'content:tag',
      seo: 'content:seo',
      geo: 'content:geo',
      aeo: 'content:aeo'
    },
    
    /**
     * Fetch all issues for a content type from GitHub
     * @param {string} type - Content type (blogs, services, etc.)
     * @param {string} token - Optional GitHub token for higher rate limits
     */
    async fetchData(type, token = null) {
      try {
        const label = this.labels[type];
        if (!label) throw new Error(`Unknown content type: ${type}`);
        
        const url = `${this.apiUrl}/${this.repo}/issues?labels=${encodeURIComponent(label)}&state=all&per_page=100`;
        const headers = { 'Accept': 'application/vnd.github.v3+json' };
        if (token) headers['Authorization'] = `token ${token}`;
        
        const res = await fetch(url, { headers });
        if (!res.ok) throw new Error(`GitHub API error: ${res.status} ${res.statusText}`);
        
        const issues = await res.json();
        
        // Convert GitHub Issues to data records
        return issues
          .filter(issue => !issue.pull_request) // Exclude PRs
          .map(issue => this.issueToRecord(type, issue));
      } catch (error) {
        console.error(`Failed to fetch ${type} from GitHub:`, error);
        return [];
      }
    },
    
    /**
     * Convert a GitHub Issue to a data record
     */
    issueToRecord(type, issue) {
      let record = {
        id: issue.number.toString(),
        title: issue.title,
        slug: (issue.body.match(/slug:\s*([^\n]+)/i) || ['', ''])[1].trim() || 
               issue.title.toLowerCase().replace(/[^a-z0-9]+/g, '-'),
        status: issue.state === 'closed' ? 'archived' : 
                issue.labels.some(l => l.name === 'status:published') ? 'published' : 'draft',
      };
      
      // Parse body as JSON metadata or key:value pairs
      try {
        const bodyLines = issue.body.split('\n');
        bodyLines.forEach(line => {
          const match = line.match(/^([a-zA-Z0-9_]+):\s*(.+)$/);
          if (match) {
            const key = match[1];
            let value = match[2].trim();
            // Handle multiline values (marked with >>>)
            if (value.endsWith('>>>')) {
              // Find the closing marker
              const closeIdx = bodyLines.findIndex(l => l.includes('<<<'));
              if (closeIdx > -1) {
                const multiline = bodyLines
                  .slice(bodyLines.indexOf(line), closeIdx + 1)
                  .map(l => l.replace(/^(>>>|<<<)/, '').trim())
                  .filter(l => l)
                  .join('\n');
                record[key] = multiline;
              }
            } else {
              record[key] = value;
            }
          }
        });
      } catch (e) {
        console.error('Failed to parse issue body:', e);
      }
      
      // Add GitHub-specific metadata
      record._githubIssue = issue.number;
      record._githubUrl = issue.html_url;
      record._lastUpdated = issue.updated_at;
      
      return record;
    },
    
    /**
     * Create or update a GitHub Issue for a record
     * @param {string} type - Content type
     * @param {object} record - Data record
     * @param {string} token - GitHub token (required for write)
     */
    async saveData(type, record, token) {
      if (!token) throw new Error('GitHub token required for saving data');
      
      try {
        const label = this.labels[type];
        const title = record.title || record.metaTitle || 'Untitled';
        const body = this.recordToIssueBody(type, record);
        const labels = [label, record.status === 'published' ? 'status:published' : 'status:draft'];
        
        // Check if issue exists (by searching in body)
        let issueNumber = record._githubIssue;
        
        if (issueNumber) {
          // Update existing issue
          const url = `${this.apiUrl}/${this.repo}/issues/${issueNumber}`;
          const res = await fetch(url, {
            method: 'PATCH',
            headers: {
              'Authorization': `token ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, body, labels, state: record.status === 'archived' ? 'closed' : 'open' })
          });
          
          if (!res.ok) throw new Error(`Failed to update issue: ${res.status}`);
          return await res.json();
        } else {
          // Create new issue
          const url = `${this.apiUrl}/${this.repo}/issues`;
          const res = await fetch(url, {
            method: 'POST',
            headers: {
              'Authorization': `token ${token}`,
              'Content-Type': 'application/json'
            },
            body: JSON.stringify({ title, body, labels })
          });
          
          if (!res.ok) throw new Error(`Failed to create issue: ${res.status}`);
          return await res.json();
        }
      } catch (error) {
        console.error(`Failed to save ${type} to GitHub:`, error);
        throw error;
      }
    },
    
    /**
     * Convert a record to GitHub Issue body format
     */
    recordToIssueBody(type, record) {
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
          if (value.includes('\n')) {
            lines.push(`${field}: >>>`);
            lines.push(value);
            lines.push('<<<');
          } else {
            lines.push(`${field}: ${value}`);
          }
        }
      });
      
      // Add main content
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
      
      lines.push(`\n---\n*Synced: ${new Date().toISOString()}*`);
      
      return lines.join('\n');
    },
    
    /**
     * Delete a GitHub Issue
     */
    async deleteData(type, id, token) {
      if (!token) throw new Error('GitHub token required for deleting data');
      
      try {
        const url = `${this.apiUrl}/${this.repo}/issues/${id}`;
        const res = await fetch(url, {
          method: 'PATCH',
          headers: {
            'Authorization': `token ${token}`,
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ state: 'closed' })
        });
        
        if (!res.ok) throw new Error(`Failed to delete issue: ${res.status}`);
        return true;
      } catch (error) {
        console.error(`Failed to delete ${type} from GitHub:`, error);
        throw error;
      }
    }
  };
})();
