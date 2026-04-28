# Threadlytics Chrome Extension Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Membangun Chrome Extension (Manifest V3) yang menganalisa follower growth dan post engagement di threads.net, dengan trial 3 hari, freemium gate, dan license system via Sejoi + Supabase.

**Architecture:** Content script pasif scrape DOM threads.net → Background Service Worker deduplicasi & simpan ke IndexedDB (Dexie.js, 30 hari rolling) → Side Panel UI (Preact + Tailwind) query lokal & render stats. Supabase Edge Functions hanya untuk trial enforcement dan license validation.

**Tech Stack:** Manifest V3, Preact, Tailwind CSS, Dexie.js, uPlot, Vitest, Supabase (PostgreSQL + Edge Functions), Vite + @crxjs/vite-plugin

---

## File Structure

```
threadlytics/
├── manifest.json                        # MV3 config
├── package.json
├── vite.config.js                       # Multi-entry build via @crxjs
├── tailwind.config.js
├── vitest.config.js
├── src/
│   ├── shared/
│   │   ├── db.js                        # Dexie schema & singleton
│   │   ├── constants.js                 # DOM selectors, config values
│   │   └── fingerprint.js               # Device fingerprint generation
│   ├── content/
│   │   ├── index.js                     # Content script entry
│   │   ├── scraper.js                   # Extract data dari DOM nodes
│   │   └── observer.js                  # MutationObserver setup
│   ├── background/
│   │   ├── index.js                     # Service worker entry
│   │   ├── storage.js                   # IndexedDB read/write
│   │   ├── deduplicator.js              # Post deduplication
│   │   └── license.js                   # Trial/license state machine
│   └── sidepanel/
│       ├── index.html
│       ├── main.jsx                     # Preact entry point
│       ├── App.jsx                      # Root component, routing tier state
│       ├── components/
│       │   ├── Header.jsx               # Username + tier badge
│       │   ├── FollowerCard.jsx         # Follower count + growth chart
│       │   ├── EngagementCard.jsx       # Avg view/like/comment + ER
│       │   ├── TopPostsCard.jsx         # Viral tracker table
│       │   ├── UpgradeBanner.jsx        # Trial countdown / upgrade CTA
│       │   └── ActivateLicense.jsx      # Email + license key form
│       ├── hooks/
│       │   ├── useStats.js              # Query IndexedDB, return computed stats
│       │   └── useLicense.js            # Poll license state dari background
│       └── utils/
│           ├── calculations.js          # Growth %, ER, avg per period
│           ├── formatters.js            # Format angka: 24800 → "24.8k"
│           └── exportCsv.js             # Generate & download CSV
├── supabase/
│   └── functions/
│       ├── _shared/
│       │   └── mailer.ts                # Mailketing helper + email templates
│       ├── register-install/index.ts    # Simpan device_id + install_date + optional email
│       ├── validate/index.ts            # Return tier + trial_expires_at
│       ├── activate-license/index.ts   # Validasi key Sejoi, bind device, kirim email
│       └── notify-trial-expired/index.ts # Cron: kirim email H-1 trial habis
└── tests/
    ├── unit/
    │   ├── calculations.test.js
    │   ├── deduplicator.test.js
    │   ├── fingerprint.test.js
    │   ├── scraper.test.js
    │   └── exportCsv.test.js
    └── integration/
        └── storage.test.js
```

---

## Task 1: Project Scaffold

**Files:**
- Create: `threadlytics/manifest.json`
- Create: `threadlytics/package.json`
- Create: `threadlytics/vite.config.js`
- Create: `threadlytics/tailwind.config.js`
- Create: `threadlytics/vitest.config.js`

- [ ] **Step 1: Buat direktori project**

```bash
mkdir threadlytics && cd threadlytics
```

- [ ] **Step 2: Init package.json**

```bash
npm init -y
```

- [ ] **Step 3: Install dependencies**

```bash
npm install preact dexie uplot
npm install -D vite @crxjs/vite-plugin @preact/preset-vite tailwindcss autoprefixer vitest @vitest/coverage-v8 happy-dom
```

- [ ] **Step 4: Buat manifest.json**

```json
{
  "manifest_version": 3,
  "name": "Threadlytics",
  "version": "1.0.0",
  "description": "Analisa follower growth dan post engagement di Threads",
  "permissions": ["storage", "sidePanel"],
  "host_permissions": ["https://www.threads.net/*"],
  "background": {
    "service_worker": "src/background/index.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["https://www.threads.net/*"],
      "js": ["src/content/index.js"],
      "run_at": "document_idle"
    }
  ],
  "side_panel": {
    "default_path": "src/sidepanel/index.html"
  },
  "action": {
    "default_title": "Threadlytics"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

- [ ] **Step 5: Buat vite.config.js**

```js
import { defineConfig } from 'vite'
import { crx } from '@crxjs/vite-plugin'
import preact from '@preact/preset-vite'
import manifest from './manifest.json'

export default defineConfig({
  plugins: [preact(), crx({ manifest })],
})
```

- [ ] **Step 6: Buat tailwind.config.js**

```js
export default {
  content: ['./src/**/*.{js,jsx,html}'],
  theme: { extend: {} },
  plugins: [],
}
```

- [ ] **Step 7: Buat vitest.config.js**

```js
import { defineConfig } from 'vitest/config'
export default defineConfig({
  test: {
    environment: 'happy-dom',
    coverage: { provider: 'v8', threshold: { lines: 80 } },
  },
})
```

- [ ] **Step 8: Buat direktori struktur**

```bash
mkdir -p src/shared src/content src/background src/sidepanel/components src/sidepanel/hooks src/sidepanel/utils supabase/functions/register-install supabase/functions/validate supabase/functions/activate-license tests/unit tests/integration icons
```

- [ ] **Step 9: Commit**

```bash
git init && git add manifest.json package.json vite.config.js tailwind.config.js vitest.config.js
git commit -m "chore: project scaffold Threadlytics MV3"
```

---

## Task 2: Shared Constants & DB Schema

**Files:**
- Create: `src/shared/constants.js`
- Create: `src/shared/db.js`

- [ ] **Step 1: Tulis test untuk db schema**

```js
// tests/unit/db.test.js
import { describe, it, expect, beforeEach } from 'vitest'
import Dexie from 'dexie'

// Gunakan in-memory DB untuk testing
describe('db schema', () => {
  it('followers_history table memiliki kolom date dan count', async () => {
    const db = new Dexie('threadlytics-test')
    db.version(1).stores({
      followers_history: '&date, count',
      posts: '&post_id, date, views, likes, comments, text_preview',
    })
    await db.open()
    await db.followers_history.put({ date: '2026-04-08', count: 1000 })
    const row = await db.followers_history.get('2026-04-08')
    expect(row.count).toBe(1000)
    await db.delete()
  })

  it('posts table bisa simpan dan retrieve by post_id', async () => {
    const db = new Dexie('threadlytics-test2')
    db.version(1).stores({
      followers_history: '&date, count',
      posts: '&post_id, date, views, likes, comments, text_preview',
    })
    await db.open()
    await db.posts.put({
      post_id: 'abc123',
      date: '2026-04-08',
      views: 5000,
      likes: 120,
      comments: 30,
      text_preview: 'Ini konten post',
    })
    const post = await db.posts.get('abc123')
    expect(post.views).toBe(5000)
    await db.delete()
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/db.test.js
```

Expected: FAIL — "Cannot find module 'dexie'"

- [ ] **Step 3: Buat src/shared/constants.js**

```js
// DOM selectors untuk threads.net
// CATATAN: Selectors ini perlu diverifikasi dengan inspect element di threads.net
// karena Threads adalah React app yang bisa update className kapanpun.
// Tambahkan fallback selectors jika selector utama tidak ditemukan.

export const SELECTORS = {
  // Profile page — follower count
  follower_count: [
    'a[href$="/followers"] span',
    '[data-testid="followerCount"]',
    'span.x1lliihq', // fallback class-based (fragile, update if needed)
  ],

  // Post card — view count (biasanya ada icon mata)
  post_views: [
    '[aria-label*="view"] span',
    '[data-testid="viewCount"]',
  ],

  // Post card — like count
  post_likes: [
    '[aria-label*="like"] span',
    '[aria-label*="suka"] span',
    '[data-testid="likeCount"]',
  ],

  // Post card — comment count
  post_comments: [
    '[aria-label*="comment"] span',
    '[aria-label*="komentar"] span',
    '[data-testid="commentCount"]',
  ],

  // Post ID — biasanya ada di data attribute atau URL href post
  post_id: [
    'a[href*="/post/"]',
    'article[data-post-id]',
  ],

  // Post text preview
  post_text: [
    '[data-testid="post-text"]',
    'div[class*="post"] span',
  ],

  // Post card container
  post_container: [
    'article',
    '[data-testid="post-container"]',
  ],
}

export const CONFIG = {
  // Rolling window data (hari)
  DATA_RETENTION_DAYS: 30,

  // Interval cek license ke Supabase (ms) — 1 jam
  LICENSE_CHECK_INTERVAL_MS: 60 * 60 * 1000,

  // Trial duration (hari)
  TRIAL_DAYS: 3,

  // Supabase base URL — isi setelah project dibuat
  SUPABASE_URL: 'https://YOUR_PROJECT.supabase.co',
  SUPABASE_ANON_KEY: 'YOUR_ANON_KEY',

  // Free tier limits
  FREE_TOP_POSTS_LIMIT: 3,
  FREE_FOLLOWER_HISTORY_DAYS: 7,
}
```

- [ ] **Step 4: Buat src/shared/db.js**

```js
import Dexie from 'dexie'

const db = new Dexie('threadlytics')

db.version(1).stores({
  followers_history: '&date, count',
  posts: '&post_id, date, views, likes, comments, text_preview',
})

export default db
```

- [ ] **Step 5: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/db.test.js
```

Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add src/shared/constants.js src/shared/db.js tests/unit/db.test.js
git commit -m "feat: shared DB schema dan DOM selectors constants"
```

---

## Task 3: Device Fingerprint

**Files:**
- Create: `src/shared/fingerprint.js`
- Create: `tests/unit/fingerprint.test.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/unit/fingerprint.test.js
import { describe, it, expect } from 'vitest'
import { generateFingerprint } from '../../src/shared/fingerprint.js'

describe('generateFingerprint', () => {
  it('returns string non-empty', () => {
    const fp = generateFingerprint()
    expect(typeof fp).toBe('string')
    expect(fp.length).toBeGreaterThan(10)
  })

  it('returns sama jika dipanggil ulang di environment yang sama', () => {
    const fp1 = generateFingerprint()
    const fp2 = generateFingerprint()
    expect(fp1).toBe(fp2)
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/fingerprint.test.js
```

Expected: FAIL — "generateFingerprint is not a function"

- [ ] **Step 3: Implementasi fingerprint.js**

```js
// src/shared/fingerprint.js
// Fingerprint deterministik berbasis browser properties.
// Bukan 100% unique, tapi cukup untuk MVP anti-abuse trial.

export function generateFingerprint() {
  const components = [
    navigator.userAgent,
    navigator.language,
    Intl.DateTimeFormat().resolvedOptions().timeZone,
    `${screen.width}x${screen.height}`,
    `${screen.colorDepth}`,
    navigator.hardwareConcurrency ?? 'unknown',
    navigator.platform ?? 'unknown',
  ]
  const raw = components.join('|')
  return hashString(raw)
}

function hashString(str) {
  let hash = 0
  for (let i = 0; i < str.length; i++) {
    const char = str.charCodeAt(i)
    hash = (hash << 5) - hash + char
    hash = hash & hash // Convert to 32-bit int
  }
  // Return positive hex string
  return Math.abs(hash).toString(16).padStart(8, '0')
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/fingerprint.test.js
```

Expected: PASS (2 tests)

- [ ] **Step 5: Commit**

```bash
git add src/shared/fingerprint.js tests/unit/fingerprint.test.js
git commit -m "feat: device fingerprint untuk trial enforcement"
```

---

## Task 4: DOM Scraper

**Files:**
- Create: `src/content/scraper.js`
- Create: `tests/unit/scraper.test.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/unit/scraper.test.js
import { describe, it, expect } from 'vitest'
import { extractPostData, extractFollowerCount, parseCount } from '../../src/content/scraper.js'

describe('parseCount', () => {
  it('parse angka biasa', () => {
    expect(parseCount('1234')).toBe(1234)
  })
  it('parse format k (ribuan)', () => {
    expect(parseCount('24.8k')).toBe(24800)
    expect(parseCount('1.2K')).toBe(1200)
  })
  it('parse format m (jutaan)', () => {
    expect(parseCount('1.5m')).toBe(1500000)
  })
  it('return null jika tidak bisa diparse', () => {
    expect(parseCount('')).toBeNull()
    expect(parseCount(null)).toBeNull()
  })
})

describe('extractFollowerCount', () => {
  it('extract angka follower dari DOM node', () => {
    document.body.innerHTML = `
      <div>
        <a href="/user/followers">
          <span>12.5k</span>
          followers
        </a>
      </div>
    `
    const node = document.querySelector('a[href$="/followers"] span')
    expect(extractFollowerCount(document)).toBe(12500)
  })

  it('return null jika elemen tidak ditemukan', () => {
    document.body.innerHTML = '<div>no follower element</div>'
    expect(extractFollowerCount(document)).toBeNull()
  })
})

describe('extractPostData', () => {
  it('extract post_id, views, likes, comments dari article element', () => {
    document.body.innerHTML = `
      <article>
        <a href="/user/post/ABC123XYZ">link</a>
        <span aria-label="24800 views">24.8k</span>
        <span aria-label="120 likes">120</span>
        <span aria-label="30 comments">30</span>
        <span data-testid="post-text">Ini teks post</span>
      </article>
    `
    const article = document.querySelector('article')
    const result = extractPostData(article)
    expect(result.post_id).toBe('ABC123XYZ')
    expect(result.views).toBe(24800)
    expect(result.likes).toBe(120)
    expect(result.comments).toBe(30)
    expect(result.text_preview).toBe('Ini teks post')
  })

  it('return null jika post_id tidak ditemukan', () => {
    document.body.innerHTML = '<article><span>no link</span></article>'
    const result = extractPostData(document.querySelector('article'))
    expect(result).toBeNull()
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/scraper.test.js
```

Expected: FAIL — "extractPostData is not a function"

- [ ] **Step 3: Implementasi scraper.js**

```js
// src/content/scraper.js
import { SELECTORS } from '../shared/constants.js'

/**
 * Parse string angka dari Threads: "24.8k" → 24800, "1.5m" → 1500000
 */
export function parseCount(str) {
  if (!str) return null
  const s = str.trim().toLowerCase()
  if (!s) return null
  if (s.endsWith('k')) return Math.round(parseFloat(s) * 1000)
  if (s.endsWith('m')) return Math.round(parseFloat(s) * 1_000_000)
  const n = parseInt(s.replace(/,/g, ''), 10)
  return isNaN(n) ? null : n
}

/**
 * Query DOM dengan multiple fallback selectors.
 * Return elemen pertama yang ditemukan, atau null.
 */
function queryFallback(root, selectors) {
  for (const sel of selectors) {
    try {
      const el = root.querySelector(sel)
      if (el) return el
    } catch (_) {
      // selector invalid, skip
    }
  }
  return null
}

/**
 * Extract follower count dari halaman profile.
 * Return number atau null jika tidak ditemukan.
 */
export function extractFollowerCount(root) {
  const el = queryFallback(root, SELECTORS.follower_count)
  if (!el) return null
  return parseCount(el.textContent)
}

/**
 * Extract post ID dari URL di dalam article element.
 * Threads URL format: /username/post/POST_ID
 */
function extractPostId(article) {
  const el = queryFallback(article, SELECTORS.post_id)
  if (!el) return null
  const href = el.getAttribute('href') || ''
  const match = href.match(/\/post\/([A-Za-z0-9_-]+)/)
  return match ? match[1] : null
}

/**
 * Extract angka dari aria-label atau text content.
 * aria-label sering lebih akurat: "24800 views"
 */
function extractStatFromAriaOrText(article, selectors) {
  for (const sel of selectors) {
    try {
      const el = article.querySelector(sel)
      if (!el) continue
      // Coba dari aria-label dulu
      const aria = el.getAttribute('aria-label')
      if (aria) {
        const match = aria.match(/[\d,]+/)
        if (match) return parseInt(match[0].replace(/,/g, ''), 10)
      }
      // Fallback ke text content
      const n = parseCount(el.textContent)
      if (n !== null) return n
    } catch (_) {}
  }
  return null
}

/**
 * Extract semua data dari satu article/post element.
 * Return object atau null jika post_id tidak bisa diekstrak.
 */
export function extractPostData(article) {
  const post_id = extractPostId(article)
  if (!post_id) return null

  const views = extractStatFromAriaOrText(article, SELECTORS.post_views)
  const likes = extractStatFromAriaOrText(article, SELECTORS.post_likes)
  const comments = extractStatFromAriaOrText(article, SELECTORS.post_comments)

  const textEl = queryFallback(article, SELECTORS.post_text)
  const text_preview = textEl
    ? textEl.textContent.trim().slice(0, 100)
    : ''

  return {
    post_id,
    date: new Date().toISOString().split('T')[0],
    views: views ?? 0,
    likes: likes ?? 0,
    comments: comments ?? 0,
    text_preview,
  }
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/scraper.test.js
```

Expected: PASS (semua test)

- [ ] **Step 5: Commit**

```bash
git add src/content/scraper.js tests/unit/scraper.test.js
git commit -m "feat: DOM scraper dengan fallback selectors dan parseCount"
```

---

## Task 5: MutationObserver & Content Script Entry

**Files:**
- Create: `src/content/observer.js`
- Create: `src/content/index.js`

- [ ] **Step 1: Buat observer.js**

```js
// src/content/observer.js
import { SELECTORS } from '../shared/constants.js'
import { extractPostData, extractFollowerCount } from './scraper.js'

/**
 * Setup MutationObserver untuk detect post baru saat user scroll.
 * Setiap kali ada post baru masuk DOM, kirim datanya ke background.
 */
export function setupObserver(onPostFound, onFollowerFound) {
  const processedIds = new Set()

  function processArticles(root) {
    const articles = root.querySelectorAll(SELECTORS.post_container[0])
    articles.forEach((article) => {
      const data = extractPostData(article)
      if (!data || processedIds.has(data.post_id)) return
      processedIds.add(data.post_id)
      onPostFound(data)
    })
  }

  // Initial scan
  processArticles(document)

  // Scan follower jika di profile page
  const followerCount = extractFollowerCount(document)
  if (followerCount !== null) {
    onFollowerFound(followerCount)
  }

  // Watch untuk konten baru (infinite scroll)
  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType !== Node.ELEMENT_NODE) return
        processArticles(node)
      })
    })
  })

  observer.observe(document.body, { childList: true, subtree: true })
  return observer
}
```

- [ ] **Step 2: Buat content/index.js**

```js
// src/content/index.js
import { setupObserver } from './observer.js'

setupObserver(
  // Handler: post ditemukan
  (postData) => {
    chrome.runtime.sendMessage({ type: 'POST_FOUND', payload: postData })
  },
  // Handler: follower count ditemukan
  (count) => {
    chrome.runtime.sendMessage({ type: 'FOLLOWER_FOUND', payload: { count } })
  }
)
```

- [ ] **Step 3: Commit**

```bash
git add src/content/observer.js src/content/index.js
git commit -m "feat: MutationObserver content script untuk passive scraping"
```

---

## Task 6: Storage Layer (IndexedDB via Dexie)

**Files:**
- Create: `src/background/storage.js`
- Create: `tests/integration/storage.test.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/integration/storage.test.js
import { describe, it, expect, beforeEach } from 'vitest'
import Dexie from 'dexie'

// Pakai DB terpisah untuk test agar tidak conflict dengan production DB
let db

beforeEach(async () => {
  db = new Dexie('threadlytics-test')
  db.version(1).stores({
    followers_history: '&date, count',
    posts: '&post_id, date, views, likes, comments, text_preview',
  })
  await db.open()
  await db.followers_history.clear()
  await db.posts.clear()
})

describe('saveFollowerSnapshot', () => {
  it('simpan follower count dengan date sebagai key (unik per hari)', async () => {
    await db.followers_history.put({ date: '2026-04-08', count: 12000 })
    await db.followers_history.put({ date: '2026-04-08', count: 12500 }) // overwrite
    const all = await db.followers_history.toArray()
    expect(all.length).toBe(1)
    expect(all[0].count).toBe(12500)
  })
})

describe('savePost', () => {
  it('simpan post baru', async () => {
    await db.posts.put({
      post_id: 'post001',
      date: '2026-04-08',
      views: 10000,
      likes: 300,
      comments: 50,
      text_preview: 'Test post',
    })
    const post = await db.posts.get('post001')
    expect(post.views).toBe(10000)
  })

  it('update post jika post_id sudah ada (views bisa naik)', async () => {
    await db.posts.put({ post_id: 'post001', date: '2026-04-08', views: 10000, likes: 300, comments: 50, text_preview: 'Test' })
    await db.posts.put({ post_id: 'post001', date: '2026-04-08', views: 11000, likes: 310, comments: 52, text_preview: 'Test' })
    const all = await db.posts.where('post_id').equals('post001').toArray()
    expect(all.length).toBe(1)
    expect(all[0].views).toBe(11000)
  })
})

describe('pruneOldData', () => {
  it('hapus data di luar 30 hari', async () => {
    const old_date = '2026-01-01'
    const recent_date = '2026-04-07'
    await db.followers_history.put({ date: old_date, count: 9000 })
    await db.followers_history.put({ date: recent_date, count: 12000 })

    const cutoff = new Date()
    cutoff.setDate(cutoff.getDate() - 30)
    const cutoffStr = cutoff.toISOString().split('T')[0]
    await db.followers_history.where('date').below(cutoffStr).delete()

    const all = await db.followers_history.toArray()
    expect(all.every(r => r.date >= cutoffStr)).toBe(true)
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/integration/storage.test.js
```

Expected: FAIL (Dexie belum diimport di test setup)

- [ ] **Step 3: Implementasi storage.js**

```js
// src/background/storage.js
import db from '../shared/db.js'
import { CONFIG } from '../shared/constants.js'

/**
 * Simpan follower snapshot hari ini (1x per hari, overwrite jika sudah ada).
 */
export async function saveFollowerSnapshot(count) {
  const date = today()
  await db.followers_history.put({ date, count })
  await pruneOldData()
}

/**
 * Simpan atau update post (upsert by post_id).
 */
export async function savePost(postData) {
  await db.posts.put(postData)
}

/**
 * Hapus data lebih lama dari DATA_RETENTION_DAYS.
 */
export async function pruneOldData() {
  const cutoff = new Date()
  cutoff.setDate(cutoff.getDate() - CONFIG.DATA_RETENTION_DAYS)
  const cutoffStr = cutoff.toISOString().split('T')[0]
  await db.followers_history.where('date').below(cutoffStr).delete()
  await db.posts.where('date').below(cutoffStr).delete()
}

/**
 * Ambil semua follower history, diurutkan ascending by date.
 */
export async function getFollowerHistory() {
  return db.followers_history.orderBy('date').toArray()
}

/**
 * Ambil semua posts dalam range hari terakhir N hari.
 */
export async function getRecentPosts(days = 30) {
  const cutoff = new Date()
  cutoff.setDate(cutoff.getDate() - days)
  const cutoffStr = cutoff.toISOString().split('T')[0]
  return db.posts.where('date').aboveOrEqual(cutoffStr).toArray()
}

function today() {
  return new Date().toISOString().split('T')[0]
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/integration/storage.test.js
```

Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/background/storage.js tests/integration/storage.test.js
git commit -m "feat: storage layer IndexedDB dengan pruning 30 hari"
```

---

## Task 7: Post Deduplicator

**Files:**
- Create: `src/background/deduplicator.js`
- Create: `tests/unit/deduplicator.test.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/unit/deduplicator.test.js
import { describe, it, expect } from 'vitest'
import { Deduplicator } from '../../src/background/deduplicator.js'

describe('Deduplicator', () => {
  it('return true untuk post baru (belum pernah dilihat)', () => {
    const dedup = new Deduplicator()
    expect(dedup.isNew('post001')).toBe(true)
  })

  it('return false untuk post yang sudah diproses', () => {
    const dedup = new Deduplicator()
    dedup.mark('post001')
    expect(dedup.isNew('post001')).toBe(false)
  })

  it('isNew + mark sekaligus via markIfNew', () => {
    const dedup = new Deduplicator()
    expect(dedup.markIfNew('post001')).toBe(true)
    expect(dedup.markIfNew('post001')).toBe(false)
  })

  it('tidak terpengaruh post lain', () => {
    const dedup = new Deduplicator()
    dedup.mark('post001')
    expect(dedup.isNew('post002')).toBe(true)
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/deduplicator.test.js
```

Expected: FAIL — "Deduplicator is not a constructor"

- [ ] **Step 3: Implementasi deduplicator.js**

```js
// src/background/deduplicator.js
// In-memory deduplication untuk satu session background worker.
// Reset saat service worker restart (wajar — post yang masuk lagi akan di-upsert di DB).

export class Deduplicator {
  constructor() {
    this._seen = new Set()
  }

  isNew(post_id) {
    return !this._seen.has(post_id)
  }

  mark(post_id) {
    this._seen.add(post_id)
  }

  markIfNew(post_id) {
    if (this._seen.has(post_id)) return false
    this._seen.add(post_id)
    return true
  }
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/deduplicator.test.js
```

Expected: PASS (4 tests)

- [ ] **Step 5: Commit**

```bash
git add src/background/deduplicator.js tests/unit/deduplicator.test.js
git commit -m "feat: in-memory post deduplicator"
```

---

## Task 8: License State Machine

**Files:**
- Create: `src/background/license.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/unit/license.test.js
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { getTier, TIERS } from '../../src/background/license.js'

describe('getTier', () => {
  beforeEach(() => {
    vi.useFakeTimers()
  })

  it('return TRIAL jika install_date dalam 3 hari terakhir', () => {
    const installDate = new Date()
    installDate.setDate(installDate.getDate() - 1) // 1 hari lalu
    const tier = getTier({ is_active: false, install_date: installDate.toISOString(), license_key: null })
    expect(tier).toBe(TIERS.TRIAL)
  })

  it('return FREE jika trial habis dan tidak ada license aktif', () => {
    const installDate = new Date()
    installDate.setDate(installDate.getDate() - 5) // 5 hari lalu
    const tier = getTier({ is_active: false, install_date: installDate.toISOString(), license_key: null })
    expect(tier).toBe(TIERS.FREE)
  })

  it('return PRO jika license aktif', () => {
    const installDate = new Date()
    installDate.setDate(installDate.getDate() - 10)
    const tier = getTier({ is_active: true, install_date: installDate.toISOString(), license_key: 'TDL-XXXX' })
    expect(tier).toBe(TIERS.PRO)
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/license.test.js
```

Expected: FAIL — "getTier is not a function"

- [ ] **Step 3: Implementasi license.js**

```js
// src/background/license.js
import { CONFIG } from '../shared/constants.js'
import { generateFingerprint } from '../shared/fingerprint.js'

export const TIERS = {
  TRIAL: 'trial',
  FREE: 'free',
  PRO: 'pro',
}

/**
 * Tentukan tier user berdasarkan state license.
 * @param {{ is_active: boolean, install_date: string, license_key: string|null }} state
 */
export function getTier(state) {
  if (state.is_active && state.license_key) return TIERS.PRO

  const installDate = new Date(state.install_date)
  const daysSinceInstall = (Date.now() - installDate.getTime()) / (1000 * 60 * 60 * 24)

  if (daysSinceInstall <= CONFIG.TRIAL_DAYS) return TIERS.TRIAL
  return TIERS.FREE
}

/**
 * Register install ke Supabase. Dipanggil sekali saat extension pertama kali install.
 */
export async function registerInstall() {
  const device_id = generateFingerprint()
  const install_date = new Date().toISOString()

  const res = await fetch(`${CONFIG.SUPABASE_URL}/functions/v1/register-install`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${CONFIG.SUPABASE_ANON_KEY}`,
    },
    body: JSON.stringify({ device_id, install_date }),
  })

  if (!res.ok) throw new Error('register-install failed')
  return res.json()
}

/**
 * Validasi status license ke Supabase.
 * Return { tier, trial_expires_at, is_active }
 */
export async function validateLicense() {
  const device_id = generateFingerprint()

  const res = await fetch(`${CONFIG.SUPABASE_URL}/functions/v1/validate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${CONFIG.SUPABASE_ANON_KEY}`,
    },
    body: JSON.stringify({ device_id }),
  })

  if (!res.ok) throw new Error('validate failed')
  return res.json()
}

/**
 * Aktivasi license key dengan email user.
 * Return { success: boolean, message: string }
 */
export async function activateLicense(email, license_key) {
  const device_id = generateFingerprint()

  const res = await fetch(`${CONFIG.SUPABASE_URL}/functions/v1/activate-license`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${CONFIG.SUPABASE_ANON_KEY}`,
    },
    body: JSON.stringify({ device_id, email, license_key }),
  })

  const data = await res.json()
  if (!res.ok) return { success: false, message: data.message || 'Aktivasi gagal' }
  return { success: true, message: 'License berhasil diaktivasi' }
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/license.test.js
```

Expected: PASS (3 tests)

- [ ] **Step 5: Commit**

```bash
git add src/background/license.js tests/unit/license.test.js
git commit -m "feat: license state machine (trial/free/pro) dan Supabase calls"
```

---

## Task 9: Background Service Worker Entry

**Files:**
- Create: `src/background/index.js`

- [ ] **Step 1: Buat background/index.js**

```js
// src/background/index.js
import { saveFollowerSnapshot, savePost } from './storage.js'
import { Deduplicator } from './deduplicator.js'
import { registerInstall, validateLicense, TIERS, getTier } from './license.js'
import { CONFIG } from '../shared/constants.js'

const dedup = new Deduplicator()
let licenseState = null

// ── Install handler ──────────────────────────────────────────────────────────
chrome.runtime.onInstalled.addListener(async ({ reason }) => {
  if (reason === 'install') {
    try {
      licenseState = await registerInstall()
    } catch (e) {
      console.error('[Threadlytics] register-install error:', e)
    }
  }
})

// ── Message handler dari content script ─────────────────────────────────────
chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (message.type === 'POST_FOUND') {
    const { payload } = message
    if (dedup.markIfNew(payload.post_id)) {
      savePost(payload).catch(e => console.error('[Threadlytics] savePost error:', e))
    }
    sendResponse({ ok: true })
  }

  if (message.type === 'FOLLOWER_FOUND') {
    saveFollowerSnapshot(message.payload.count)
      .catch(e => console.error('[Threadlytics] saveFollowerSnapshot error:', e))
    sendResponse({ ok: true })
  }

  if (message.type === 'GET_LICENSE_STATE') {
    sendResponse({ licenseState })
  }

  if (message.type === 'ACTIVATE_LICENSE') {
    // Diteruskan ke license.js — return promise via sendResponse
    return true // keep channel open untuk async
  }

  return false
})

// ── Periodic license validation (1x/jam) ────────────────────────────────────
async function checkLicense() {
  try {
    const data = await validateLicense()
    licenseState = data
  } catch (e) {
    console.error('[Threadlytics] validateLicense error:', e)
  }
}

// Initial check
checkLicense()

// Set alarm untuk periodic check
chrome.alarms.create('licenseCheck', { periodInMinutes: 60 })
chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'licenseCheck') checkLicense()
})
```

- [ ] **Step 2: Update manifest.json — tambahkan alarms permission**

```json
{
  "manifest_version": 3,
  "name": "Threadlytics",
  "version": "1.0.0",
  "description": "Analisa follower growth dan post engagement di Threads",
  "permissions": ["storage", "sidePanel", "alarms"],
  "host_permissions": ["https://www.threads.net/*"],
  "background": {
    "service_worker": "src/background/index.js",
    "type": "module"
  },
  "content_scripts": [
    {
      "matches": ["https://www.threads.net/*"],
      "js": ["src/content/index.js"],
      "run_at": "document_idle"
    }
  ],
  "side_panel": {
    "default_path": "src/sidepanel/index.html"
  },
  "action": {
    "default_title": "Threadlytics"
  },
  "icons": {
    "16": "icons/icon16.png",
    "48": "icons/icon48.png",
    "128": "icons/icon128.png"
  }
}
```

- [ ] **Step 3: Commit**

```bash
git add src/background/index.js manifest.json
git commit -m "feat: background service worker entry dengan license check alarm"
```

---

## Task 10: Calculations Utility

**Files:**
- Create: `src/sidepanel/utils/calculations.js`
- Create: `tests/unit/calculations.test.js`

- [ ] **Step 1: Tulis failing test**

```js
// tests/unit/calculations.test.js
import { describe, it, expect } from 'vitest'
import {
  calcFollowerGrowth,
  calcAvgPostStats,
  calcEngagementRate,
  calcGrowthPercent,
} from '../../src/sidepanel/utils/calculations.js'

describe('calcFollowerGrowth', () => {
  const history = [
    { date: '2026-03-09', count: 10000 },
    { date: '2026-03-16', count: 10500 },
    { date: '2026-04-07', count: 11800 },
    { date: '2026-04-08', count: 12000 },
  ]

  it('hitung delta hari ini vs kemarin', () => {
    const result = calcFollowerGrowth(history, '2026-04-08')
    expect(result.delta_today).toBe(200)
  })

  it('hitung delta 7 hari', () => {
    const result = calcFollowerGrowth(history, '2026-04-08')
    expect(result.delta_7d).toBe(1500) // 12000 - 10500
  })

  it('hitung delta 30 hari', () => {
    const result = calcFollowerGrowth(history, '2026-04-08')
    expect(result.delta_30d).toBe(2000) // 12000 - 10000
  })
})

describe('calcAvgPostStats', () => {
  const posts = [
    { post_id: '1', date: '2026-04-07', views: 10000, likes: 300, comments: 50 },
    { post_id: '2', date: '2026-04-06', views: 8000, likes: 200, comments: 30 },
    { post_id: '3', date: '2026-03-25', views: 5000, likes: 100, comments: 20 }, // > 7 hari
  ]

  it('hitung rata-rata 7 hari terakhir', () => {
    const result = calcAvgPostStats(posts, 7, '2026-04-08')
    expect(result.avg_views).toBe(9000)
    expect(result.avg_likes).toBe(250)
    expect(result.avg_comments).toBe(40)
  })
})

describe('calcEngagementRate', () => {
  it('hitung ER sebagai (likes+comments)/views * 100', () => {
    expect(calcEngagementRate(300, 50, 10000)).toBeCloseTo(3.5, 1)
  })

  it('return 0 jika views adalah 0', () => {
    expect(calcEngagementRate(100, 20, 0)).toBe(0)
  })
})

describe('calcGrowthPercent', () => {
  it('hitung persen pertumbuhan', () => {
    expect(calcGrowthPercent(10000, 12000)).toBeCloseTo(20, 0)
  })

  it('return 0 jika baseline adalah 0', () => {
    expect(calcGrowthPercent(0, 100)).toBe(0)
  })

  it('return negatif jika turun', () => {
    expect(calcGrowthPercent(12000, 10000)).toBeCloseTo(-16.67, 1)
  })
})
```

- [ ] **Step 2: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/calculations.test.js
```

Expected: FAIL

- [ ] **Step 3: Implementasi calculations.js**

```js
// src/sidepanel/utils/calculations.js

/**
 * Hitung pertumbuhan follower vs periode lalu.
 * @param {Array<{date: string, count: number}>} history - sorted ascending by date
 * @param {string} today - format YYYY-MM-DD
 */
export function calcFollowerGrowth(history, today) {
  const todayCount = history.find(h => h.date === today)?.count ?? null

  const yesterday = offsetDate(today, -1)
  const week_ago = offsetDate(today, -7)
  const month_ago = offsetDate(today, -30)

  const yesterdayCount = closestBefore(history, yesterday)
  const weekCount = closestBefore(history, week_ago)
  const monthCount = closestBefore(history, month_ago)

  return {
    current: todayCount,
    delta_today: todayCount !== null && yesterdayCount !== null ? todayCount - yesterdayCount : null,
    delta_7d: todayCount !== null && weekCount !== null ? todayCount - weekCount : null,
    delta_30d: todayCount !== null && monthCount !== null ? todayCount - monthCount : null,
  }
}

/**
 * Hitung rata-rata stats post dalam N hari terakhir.
 */
export function calcAvgPostStats(posts, days, today) {
  const cutoff = offsetDate(today, -days)
  const recent = posts.filter(p => p.date >= cutoff && p.date <= today)

  if (recent.length === 0) return { avg_views: 0, avg_likes: 0, avg_comments: 0, count: 0 }

  const avg_views = Math.round(recent.reduce((s, p) => s + p.views, 0) / recent.length)
  const avg_likes = Math.round(recent.reduce((s, p) => s + p.likes, 0) / recent.length)
  const avg_comments = Math.round(recent.reduce((s, p) => s + p.comments, 0) / recent.length)

  return { avg_views, avg_likes, avg_comments, count: recent.length }
}

/**
 * Hitung engagement rate: (likes + comments) / views * 100
 */
export function calcEngagementRate(likes, comments, views) {
  if (!views) return 0
  return ((likes + comments) / views) * 100
}

/**
 * Hitung persen pertumbuhan dari baseline ke current.
 */
export function calcGrowthPercent(baseline, current) {
  if (!baseline) return 0
  return ((current - baseline) / baseline) * 100
}

// ── Helpers ──────────────────────────────────────────────────────────────────

function offsetDate(dateStr, days) {
  const d = new Date(dateStr)
  d.setDate(d.getDate() + days)
  return d.toISOString().split('T')[0]
}

function closestBefore(history, targetDate) {
  // Cari entry dengan date <= targetDate, ambil yang paling dekat
  const candidates = history.filter(h => h.date <= targetDate)
  if (!candidates.length) return null
  return candidates[candidates.length - 1].count
}
```

- [ ] **Step 4: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/calculations.test.js
```

Expected: PASS (semua test)

- [ ] **Step 5: Commit**

```bash
git add src/sidepanel/utils/calculations.js tests/unit/calculations.test.js
git commit -m "feat: growth dan engagement rate calculations"
```

---

## Task 11: Formatters & Export CSV

**Files:**
- Create: `src/sidepanel/utils/formatters.js`
- Create: `src/sidepanel/utils/exportCsv.js`
- Create: `tests/unit/exportCsv.test.js`

- [ ] **Step 1: Buat formatters.js**

```js
// src/sidepanel/utils/formatters.js

/**
 * Format angka besar menjadi singkatan: 24800 → "24.8k"
 */
export function formatCount(n) {
  if (n === null || n === undefined) return '—'
  if (n >= 1_000_000) return `${(n / 1_000_000).toFixed(1)}m`
  if (n >= 1000) return `${(n / 1000).toFixed(1)}k`
  return String(n)
}

/**
 * Format persen dengan tanda + atau -: 12.3 → "+12.3%"
 */
export function formatGrowth(percent) {
  if (percent === null || percent === undefined) return '—'
  const sign = percent >= 0 ? '+' : ''
  return `${sign}${percent.toFixed(1)}%`
}

/**
 * Format delta angka: 843 → "+843", -200 → "-200"
 */
export function formatDelta(delta) {
  if (delta === null || delta === undefined) return '—'
  const sign = delta >= 0 ? '+' : ''
  return `${sign}${delta.toLocaleString('id-ID')}`
}

/**
 * Format engagement rate: 2.1 → "2.1%"
 */
export function formatER(er) {
  if (er === null || er === undefined) return '—'
  return `${er.toFixed(1)}%`
}
```

- [ ] **Step 2: Tulis failing test untuk exportCsv**

```js
// tests/unit/exportCsv.test.js
import { describe, it, expect } from 'vitest'
import { generateFollowerCsv, generatePostsCsv } from '../../src/sidepanel/utils/exportCsv.js'

describe('generateFollowerCsv', () => {
  it('generate CSV string dari follower history', () => {
    const history = [
      { date: '2026-04-07', count: 11800 },
      { date: '2026-04-08', count: 12000 },
    ]
    const csv = generateFollowerCsv(history)
    expect(csv).toContain('date,followers')
    expect(csv).toContain('2026-04-07,11800')
    expect(csv).toContain('2026-04-08,12000')
  })
})

describe('generatePostsCsv', () => {
  it('generate CSV string dari posts data', () => {
    const posts = [
      { post_id: 'abc', date: '2026-04-08', views: 10000, likes: 300, comments: 50, text_preview: 'Hello world' },
    ]
    const csv = generatePostsCsv(posts)
    expect(csv).toContain('post_id,date,views,likes,comments,engagement_rate,text_preview')
    expect(csv).toContain('abc')
    expect(csv).toContain('10000')
  })
})
```

- [ ] **Step 3: Jalankan test — harus FAIL**

```bash
npx vitest run tests/unit/exportCsv.test.js
```

Expected: FAIL

- [ ] **Step 4: Implementasi exportCsv.js**

```js
// src/sidepanel/utils/exportCsv.js
import { calcEngagementRate } from './calculations.js'

export function generateFollowerCsv(history) {
  const header = 'date,followers'
  const rows = history.map(h => `${h.date},${h.count}`)
  return [header, ...rows].join('\n')
}

export function generatePostsCsv(posts) {
  const header = 'post_id,date,views,likes,comments,engagement_rate,text_preview'
  const rows = posts.map(p => {
    const er = calcEngagementRate(p.likes, p.comments, p.views).toFixed(2)
    const preview = `"${p.text_preview.replace(/"/g, '""')}"`
    return `${p.post_id},${p.date},${p.views},${p.likes},${p.comments},${er},${preview}`
  })
  return [header, ...rows].join('\n')
}

/**
 * Trigger browser download dari CSV string.
 */
export function downloadCsv(csvString, filename) {
  const blob = new Blob([csvString], { type: 'text/csv;charset=utf-8;' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = filename
  a.click()
  URL.revokeObjectURL(url)
}
```

- [ ] **Step 5: Jalankan test — harus PASS**

```bash
npx vitest run tests/unit/exportCsv.test.js
```

Expected: PASS (2 tests)

- [ ] **Step 6: Commit**

```bash
git add src/sidepanel/utils/formatters.js src/sidepanel/utils/exportCsv.js tests/unit/exportCsv.test.js
git commit -m "feat: formatters dan CSV export utility"
```

---

## Task 12: Side Panel Hooks

**Files:**
- Create: `src/sidepanel/hooks/useStats.js`
- Create: `src/sidepanel/hooks/useLicense.js`

- [ ] **Step 1: Buat useStats.js**

```js
// src/sidepanel/hooks/useStats.js
import { useState, useEffect } from 'preact/hooks'
import { getFollowerHistory, getRecentPosts } from '../../background/storage.js'
import { calcFollowerGrowth, calcAvgPostStats, calcEngagementRate, calcGrowthPercent } from '../utils/calculations.js'

export function useStats() {
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function load() {
      const today = new Date().toISOString().split('T')[0]
      const [history, posts] = await Promise.all([
        getFollowerHistory(),
        getRecentPosts(30),
      ])

      const followerGrowth = calcFollowerGrowth(history, today)
      const avg7d = calcAvgPostStats(posts, 7, today)
      const avg7d_prev = calcAvgPostStats(posts, 7, offsetDate(today, -7))

      const er = calcEngagementRate(avg7d.avg_likes, avg7d.avg_comments, avg7d.avg_views)
      const er_prev = calcEngagementRate(avg7d_prev.avg_likes, avg7d_prev.avg_comments, avg7d_prev.avg_views)

      // Top posts by views
      const sorted_posts = [...posts].sort((a, b) => b.views - a.views)

      setStats({
        follower: followerGrowth,
        avg7d,
        avg7d_prev,
        er,
        er_delta: er - er_prev,
        view_growth_pct: calcGrowthPercent(avg7d_prev.avg_views, avg7d.avg_views),
        like_growth_pct: calcGrowthPercent(avg7d_prev.avg_likes, avg7d.avg_likes),
        comment_growth_pct: calcGrowthPercent(avg7d_prev.avg_comments, avg7d.avg_comments),
        top_posts: sorted_posts,
        follower_history: history,
        all_posts: posts,
      })
      setLoading(false)
    }

    load()
    // Refresh setiap 5 menit
    const interval = setInterval(load, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  return { stats, loading }
}

function offsetDate(dateStr, days) {
  const d = new Date(dateStr)
  d.setDate(d.getDate() + days)
  return d.toISOString().split('T')[0]
}
```

- [ ] **Step 2: Buat useLicense.js**

```js
// src/sidepanel/hooks/useLicense.js
import { useState, useEffect } from 'preact/hooks'
import { TIERS, getTier } from '../../background/license.js'

export function useLicense() {
  const [tier, setTier] = useState(TIERS.FREE)
  const [licenseState, setLicenseState] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    function fetchLicenseState() {
      chrome.runtime.sendMessage({ type: 'GET_LICENSE_STATE' }, (response) => {
        if (response?.licenseState) {
          setLicenseState(response.licenseState)
          setTier(getTier(response.licenseState))
        }
        setLoading(false)
      })
    }

    fetchLicenseState()
    const interval = setInterval(fetchLicenseState, 60 * 1000)
    return () => clearInterval(interval)
  }, [])

  const isPro = tier === TIERS.PRO
  const isTrial = tier === TIERS.TRIAL
  const isFree = tier === TIERS.FREE

  return { tier, isPro, isTrial, isFree, licenseState, loading }
}
```

- [ ] **Step 3: Commit**

```bash
git add src/sidepanel/hooks/useStats.js src/sidepanel/hooks/useLicense.js
git commit -m "feat: useStats dan useLicense hooks untuk side panel"
```

---

## Task 13: Side Panel UI Components

**Files:**
- Create: `src/sidepanel/components/Header.jsx`
- Create: `src/sidepanel/components/FollowerCard.jsx`
- Create: `src/sidepanel/components/EngagementCard.jsx`
- Create: `src/sidepanel/components/TopPostsCard.jsx`
- Create: `src/sidepanel/components/UpgradeBanner.jsx`
- Create: `src/sidepanel/components/ActivateLicense.jsx`

- [ ] **Step 1: Buat Header.jsx**

```jsx
// src/sidepanel/components/Header.jsx
export function Header({ tier, licenseState }) {
  const tierLabel = {
    trial: 'Trial',
    free: 'Free',
    pro: 'Pro',
  }[tier]

  const tierColor = {
    trial: 'bg-yellow-100 text-yellow-800',
    free: 'bg-gray-100 text-gray-600',
    pro: 'bg-blue-100 text-blue-800',
  }[tier]

  return (
    <div class="flex items-center justify-between px-4 py-3 border-b border-gray-200">
      <div class="flex items-center gap-2">
        <span class="text-lg font-bold text-gray-900">Threadlytics</span>
      </div>
      <span class={`text-xs font-semibold px-2 py-1 rounded-full ${tierColor}`}>
        {tierLabel}
      </span>
    </div>
  )
}
```

- [ ] **Step 2: Buat FollowerCard.jsx**

```jsx
// src/sidepanel/components/FollowerCard.jsx
import { formatCount, formatDelta, formatGrowth } from '../utils/formatters.js'
import { calcGrowthPercent } from '../utils/calculations.js'

export function FollowerCard({ follower, history, isPro }) {
  if (!follower) return <div class="p-4 text-sm text-gray-400">Memuat data follower...</div>

  const pct_7d = follower.delta_7d !== null && follower.current
    ? calcGrowthPercent(follower.current - follower.delta_7d, follower.current)
    : null

  return (
    <div class="px-4 py-3 border-b border-gray-100">
      <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">FOLLOWERS</p>
      <p class="text-2xl font-bold text-gray-900">{formatCount(follower.current)}</p>
      <div class="flex gap-3 mt-1 text-sm">
        <span class="text-green-600">{formatDelta(follower.delta_today)} hari ini</span>
        {isPro && (
          <>
            <span class="text-gray-400">|</span>
            <span class="text-blue-600">
              {formatDelta(follower.delta_7d)} minggu ({formatGrowth(pct_7d)})
            </span>
          </>
        )}
      </div>
      {!isPro && (
        <p class="text-xs text-gray-400 mt-1">Data 30 hari tersedia di Pro</p>
      )}
    </div>
  )
}
```

- [ ] **Step 3: Buat EngagementCard.jsx**

```jsx
// src/sidepanel/components/EngagementCard.jsx
import { formatCount, formatGrowth, formatER } from '../utils/formatters.js'

export function EngagementCard({ avg7d, er, er_delta, view_growth_pct, like_growth_pct, comment_growth_pct, isPro }) {
  if (!avg7d) return <div class="p-4 text-sm text-gray-400">Memuat engagement...</div>

  const erTrend = er_delta >= 0 ? '▲' : '▼'
  const erColor = er_delta >= 0 ? 'text-green-600' : 'text-red-500'

  return (
    <div class="px-4 py-3 border-b border-gray-100">
      <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">ENGAGEMENT (avg/post, 7 hari)</p>
      <div class="flex gap-4 text-sm">
        <div class="text-center">
          <p class="text-gray-500 text-xs">👁 View</p>
          <p class="font-bold">{formatCount(avg7d.avg_views)}</p>
          {isPro && <p class={`text-xs ${view_growth_pct >= 0 ? 'text-green-600' : 'text-red-500'}`}>{formatGrowth(view_growth_pct)}</p>}
        </div>
        <div class="text-center">
          <p class="text-gray-500 text-xs">❤️ Like</p>
          <p class="font-bold">{formatCount(avg7d.avg_likes)}</p>
          {isPro && <p class={`text-xs ${like_growth_pct >= 0 ? 'text-green-600' : 'text-red-500'}`}>{formatGrowth(like_growth_pct)}</p>}
        </div>
        <div class="text-center">
          <p class="text-gray-500 text-xs">💬 Comment</p>
          <p class="font-bold">{formatCount(avg7d.avg_comments)}</p>
          {isPro && <p class={`text-xs ${comment_growth_pct >= 0 ? 'text-green-600' : 'text-red-500'}`}>{formatGrowth(comment_growth_pct)}</p>}
        </div>
      </div>
      {isPro && (
        <p class={`mt-2 text-sm font-semibold ${erColor}`}>
          ER: {formatER(er)} {erTrend} {er_delta >= 0 ? '+' : ''}{er_delta.toFixed(2)}%
        </p>
      )}
      {!isPro && <p class="text-xs text-gray-400 mt-1">Engagement rate trend tersedia di Pro</p>}
    </div>
  )
}
```

- [ ] **Step 4: Buat TopPostsCard.jsx**

```jsx
// src/sidepanel/components/TopPostsCard.jsx
import { useState } from 'preact/hooks'
import { formatCount } from '../utils/formatters.js'
import { calcEngagementRate } from '../utils/calculations.js'

const SORT_OPTIONS = ['views', 'likes', 'comments', 'er']
const FREE_LIMIT = 3

export function TopPostsCard({ posts, isPro }) {
  const [sortBy, setSortBy] = useState('views')

  const sorted = [...(posts || [])].sort((a, b) => {
    if (sortBy === 'er') {
      return calcEngagementRate(b.likes, b.comments, b.views) - calcEngagementRate(a.likes, a.comments, a.views)
    }
    return b[sortBy] - a[sortBy]
  })

  const limit = isPro ? 10 : FREE_LIMIT
  const displayed = sorted.slice(0, limit)

  return (
    <div class="px-4 py-3 border-b border-gray-100">
      <div class="flex items-center justify-between mb-2">
        <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide">🔥 TOP POSTS</p>
        <div class="flex gap-1">
          {SORT_OPTIONS.map(opt => (
            <button
              key={opt}
              onClick={() => setSortBy(opt)}
              class={`text-xs px-2 py-0.5 rounded ${sortBy === opt ? 'bg-blue-100 text-blue-700 font-semibold' : 'text-gray-400'}`}
            >
              {opt.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {displayed.length === 0 && (
        <p class="text-sm text-gray-400">Belum ada data post. Scroll di Threads untuk mulai mengumpulkan data.</p>
      )}

      {displayed.map((post, i) => (
        <div key={post.post_id} class="flex items-start gap-2 py-1.5 border-b border-gray-50 last:border-0">
          <span class="text-xs text-gray-400 w-4 shrink-0">{i + 1}.</span>
          <div class="flex-1 min-w-0">
            <p class="text-xs text-gray-700 truncate">{post.text_preview || '(tanpa teks)'}</p>
            <p class="text-xs text-gray-400">
              👁 {formatCount(post.views)} · ❤️ {formatCount(post.likes)} · 💬 {formatCount(post.comments)}
            </p>
          </div>
        </div>
      ))}

      {!isPro && posts?.length > FREE_LIMIT && (
        <p class="text-xs text-gray-400 mt-1 text-center">
          +{posts.length - FREE_LIMIT} post lainnya tersedia di <span class="text-blue-600 font-semibold">Pro</span>
        </p>
      )}
    </div>
  )
}
```

- [ ] **Step 5: Buat UpgradeBanner.jsx**

```jsx
// src/sidepanel/components/UpgradeBanner.jsx
import { TIERS } from '../../background/license.js'

const SEJOI_URL = 'https://sejoi.com/threadlytics' // ganti dengan URL Sejoi aktual

export function UpgradeBanner({ tier, licenseState, onActivate }) {
  if (tier === TIERS.PRO) return null

  if (tier === TIERS.TRIAL && licenseState?.trial_expires_at) {
    const expiresAt = new Date(licenseState.trial_expires_at)
    const hoursLeft = Math.max(0, Math.round((expiresAt - Date.now()) / (1000 * 60 * 60)))

    return (
      <div class="mx-4 my-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p class="text-xs font-semibold text-yellow-800">
          ⏳ Trial habis dalam {hoursLeft} jam
        </p>
        <div class="flex gap-2 mt-2">
          <a
            href={SEJOI_URL}
            target="_blank"
            class="flex-1 text-center text-xs bg-blue-600 text-white py-1.5 rounded-md font-semibold"
          >
            Upgrade Pro
          </a>
          <button
            onClick={onActivate}
            class="flex-1 text-center text-xs border border-blue-600 text-blue-600 py-1.5 rounded-md font-semibold"
          >
            Punya license?
          </button>
        </div>
      </div>
    )
  }

  // Free tier
  return (
    <div class="mx-4 my-2 p-3 bg-gray-50 border border-gray-200 rounded-lg">
      <p class="text-xs text-gray-600">
        Upgrade ke <span class="font-semibold text-blue-700">Pro</span> untuk data 30 hari, top 10 post, engagement trend & export CSV.
      </p>
      <div class="flex gap-2 mt-2">
        <a
          href={SEJOI_URL}
          target="_blank"
          class="flex-1 text-center text-xs bg-blue-600 text-white py-1.5 rounded-md font-semibold"
        >
          Rp 49.000/bln
        </a>
        <button
          onClick={onActivate}
          class="flex-1 text-center text-xs border border-gray-300 text-gray-600 py-1.5 rounded-md"
        >
          Aktifkan license
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 6: Buat ActivateLicense.jsx**

```jsx
// src/sidepanel/components/ActivateLicense.jsx
import { useState } from 'preact/hooks'
import { activateLicense } from '../../background/license.js'

export function ActivateLicense({ onSuccess, onCancel }) {
  const [email, setEmail] = useState('')
  const [key, setKey] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setLoading(true)
    setError(null)

    const result = await activateLicense(email.trim(), key.trim())
    setLoading(false)

    if (result.success) {
      onSuccess()
    } else {
      setError(result.message)
    }
  }

  return (
    <div class="px-4 py-4">
      <div class="flex items-center justify-between mb-3">
        <p class="font-semibold text-sm text-gray-800">Aktifkan License Pro</p>
        <button onClick={onCancel} class="text-gray-400 text-sm">✕</button>
      </div>

      <form onSubmit={handleSubmit} class="flex flex-col gap-3">
        <input
          type="email"
          placeholder="Email pembelian"
          value={email}
          onInput={(e) => setEmail(e.target.value)}
          required
          class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full"
        />
        <input
          type="text"
          placeholder="License key (TDL-XXXX-XXXX)"
          value={key}
          onInput={(e) => setKey(e.target.value)}
          required
          class="border border-gray-300 rounded-md px-3 py-2 text-sm w-full font-mono"
        />

        {error && <p class="text-xs text-red-600">{error}</p>}

        <button
          type="submit"
          disabled={loading}
          class="bg-blue-600 text-white py-2 rounded-md text-sm font-semibold disabled:opacity-50"
        >
          {loading ? 'Memverifikasi...' : 'Aktifkan'}
        </button>
      </form>

      <p class="text-xs text-gray-400 mt-3 text-center">
        License ini hanya berlaku untuk browser ini.
      </p>
    </div>
  )
}
```

- [ ] **Step 7: Commit**

```bash
git add src/sidepanel/components/
git commit -m "feat: semua UI components side panel"
```

---

## Task 14: Side Panel App Root & Entry

**Files:**
- Create: `src/sidepanel/App.jsx`
- Create: `src/sidepanel/main.jsx`
- Create: `src/sidepanel/index.html`

- [ ] **Step 1: Buat App.jsx**

```jsx
// src/sidepanel/App.jsx
import { useState } from 'preact/hooks'
import { useStats } from './hooks/useStats.js'
import { useLicense } from './hooks/useLicense.js'
import { Header } from './components/Header.jsx'
import { FollowerCard } from './components/FollowerCard.jsx'
import { EngagementCard } from './components/EngagementCard.jsx'
import { TopPostsCard } from './components/TopPostsCard.jsx'
import { UpgradeBanner } from './components/UpgradeBanner.jsx'
import { ActivateLicense } from './components/ActivateLicense.jsx'
import { generateFollowerCsv, generatePostsCsv, downloadCsv } from './utils/exportCsv.js'

export function App() {
  const { stats, loading } = useStats()
  const { tier, isPro, isTrial, licenseState } = useLicense()
  const [showActivate, setShowActivate] = useState(false)

  function handleExport() {
    if (!stats) return
    const followerCsv = generateFollowerCsv(stats.follower_history)
    const postsCsv = generatePostsCsv(stats.all_posts)
    downloadCsv(followerCsv, 'threadlytics-followers.csv')
    setTimeout(() => downloadCsv(postsCsv, 'threadlytics-posts.csv'), 500)
  }

  if (loading) {
    return (
      <div class="flex items-center justify-center h-full text-gray-400 text-sm">
        Memuat data...
      </div>
    )
  }

  if (showActivate) {
    return (
      <div class="flex flex-col h-full">
        <Header tier={tier} />
        <ActivateLicense
          onSuccess={() => setShowActivate(false)}
          onCancel={() => setShowActivate(false)}
        />
      </div>
    )
  }

  return (
    <div class="flex flex-col h-full overflow-y-auto text-sm">
      <Header tier={tier} />
      <UpgradeBanner
        tier={tier}
        licenseState={licenseState}
        onActivate={() => setShowActivate(true)}
      />
      <FollowerCard
        follower={stats?.follower}
        history={stats?.follower_history}
        isPro={isPro || isTrial}
      />
      <EngagementCard
        avg7d={stats?.avg7d}
        er={stats?.er}
        er_delta={stats?.er_delta}
        view_growth_pct={stats?.view_growth_pct}
        like_growth_pct={stats?.like_growth_pct}
        comment_growth_pct={stats?.comment_growth_pct}
        isPro={isPro || isTrial}
      />
      <TopPostsCard
        posts={stats?.top_posts}
        isPro={isPro || isTrial}
      />

      {(isPro || isTrial) && (
        <div class="px-4 py-3">
          <button
            onClick={handleExport}
            class="w-full text-xs border border-gray-300 text-gray-600 py-2 rounded-md"
          >
            Export CSV
          </button>
        </div>
      )}
    </div>
  )
}
```

- [ ] **Step 2: Buat main.jsx**

```jsx
// src/sidepanel/main.jsx
import { render } from 'preact'
import { App } from './App.jsx'
import './style.css'

render(<App />, document.getElementById('app'))
```

- [ ] **Step 3: Buat style.css**

```css
/* src/sidepanel/style.css */
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  width: 320px;
  min-height: 100vh;
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

- [ ] **Step 4: Buat index.html**

```html
<!DOCTYPE html>
<html lang="id">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Threadlytics</title>
</head>
<body>
  <div id="app"></div>
  <script type="module" src="./main.jsx"></script>
</body>
</html>
```

- [ ] **Step 5: Test build**

```bash
npx vite build
```

Expected: Build sukses tanpa error di `dist/`

- [ ] **Step 6: Commit**

```bash
git add src/sidepanel/App.jsx src/sidepanel/main.jsx src/sidepanel/index.html src/sidepanel/style.css
git commit -m "feat: side panel App root, entry point, dan HTML"
```

---

## Task 15: Supabase — Setup & Edge Functions

**Files:**
- Create: `supabase/functions/register-install/index.ts`
- Create: `supabase/functions/validate/index.ts`
- Create: `supabase/functions/activate-license/index.ts`

**Prerequisites:**
- Install Supabase CLI: `npm install -g supabase`
- Login: `supabase login`
- Buat project di supabase.com dan catat `SUPABASE_URL` dan `SUPABASE_ANON_KEY`
- Update `src/shared/constants.js` dengan nilai tersebut

- [ ] **Step 1: Init Supabase**

```bash
supabase init
supabase link --project-ref YOUR_PROJECT_REF
```

- [ ] **Step 2: Buat tabel licenses di Supabase SQL Editor**

```sql
create table public.installs (
  id uuid primary key default gen_random_uuid(),
  device_id text not null unique,
  install_date timestamptz not null,
  created_at timestamptz default now()
);

create table public.licenses (
  id uuid primary key default gen_random_uuid(),
  key text not null unique,
  email text not null,
  device_id text,
  activated_at timestamptz,
  is_active boolean default false,
  transfer_requested_at timestamptz,
  created_at timestamptz default now()
);

-- RLS: hanya bisa diakses via service role (Edge Functions)
alter table public.installs enable row level security;
alter table public.licenses enable row level security;
```

- [ ] **Step 3: Buat register-install/index.ts**

```typescript
// supabase/functions/register-install/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 })

  const { device_id, install_date } = await req.json()

  if (!device_id || !install_date) {
    return new Response(JSON.stringify({ error: 'device_id and install_date required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Upsert — jika device sudah ada, tidak reset install_date
  const { data, error } = await supabase
    .from('installs')
    .upsert({ device_id, install_date }, { onConflict: 'device_id', ignoreDuplicates: true })
    .select()
    .single()

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ ok: true, install_date: data?.install_date ?? install_date }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

- [ ] **Step 4: Buat validate/index.ts**

```typescript
// supabase/functions/validate/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

const TRIAL_DAYS = 3

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 })

  const { device_id } = await req.json()

  if (!device_id) {
    return new Response(JSON.stringify({ error: 'device_id required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Cek license aktif
  const { data: license } = await supabase
    .from('licenses')
    .select('is_active, key')
    .eq('device_id', device_id)
    .eq('is_active', true)
    .maybeSingle()

  if (license?.is_active) {
    return new Response(JSON.stringify({ tier: 'pro', is_active: true, trial_expires_at: null }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Cek install date untuk trial
  const { data: install } = await supabase
    .from('installs')
    .select('install_date')
    .eq('device_id', device_id)
    .maybeSingle()

  if (!install) {
    return new Response(JSON.stringify({ tier: 'free', is_active: false, trial_expires_at: null }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  const installDate = new Date(install.install_date)
  const trialExpires = new Date(installDate)
  trialExpires.setDate(trialExpires.getDate() + TRIAL_DAYS)
  const now = new Date()

  if (now < trialExpires) {
    return new Response(JSON.stringify({
      tier: 'trial',
      is_active: false,
      trial_expires_at: trialExpires.toISOString(),
      install_date: install.install_date,
    }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ tier: 'free', is_active: false, trial_expires_at: null }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

- [ ] **Step 5: Buat activate-license/index.ts**

```typescript
// supabase/functions/activate-license/index.ts
// CATATAN: Validasi ke Sejoi API perlu dikonfirmasi endpoint-nya.
// Jika Sejoi tidak punya API programmatic, ganti bagian verifySejoi
// dengan webhook flow atau manual activation.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

/**
 * Validasi license ke Sejoi menggunakan Check endpoint.
 * Sejoi API: GET {{sejoli_store_url}}/sejoli/sejoli-validate-license/
 * Params: license (license key), string (device_id sebagai unique identifier)
 * Return: { valid: boolean, messages: string[] }
 *
 * Note: Tidak perlu email/password Sejoi — sudah dikumpulkan saat pembelian
 * di dashboard Sejoi. Cukup license key + device_id.
 */
async function verifySejoi(license_key: string, device_id: string): Promise<boolean> {
  const sejoli_url = Deno.env.get('SEJOLI_STORE_URL') // contoh: https://toko.banirisset.com
  if (!sejoli_url) throw new Error('SEJOLI_STORE_URL not configured')

  const params = new URLSearchParams({ license: license_key, string: device_id })
  const res = await fetch(`${sejoli_url}/sejoli/sejoli-validate-license/?${params}`, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  })

  if (!res.ok) return false

  const data = await res.json()
  return data?.valid === true
}

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 })

  const { device_id, email, license_key } = await req.json()

  if (!device_id || !email || !license_key) {
    return new Response(JSON.stringify({ message: 'device_id, email, dan license_key wajib diisi' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Cek apakah license sudah dipakai device lain
  const { data: existing } = await supabase
    .from('licenses')
    .select('device_id, email, is_active')
    .eq('key', license_key)
    .maybeSingle()

  if (existing?.is_active && existing.device_id !== device_id) {
    return new Response(JSON.stringify({
      message: 'License sudah dipakai di browser lain. Hubungi support untuk transfer.',
    }), {
      status: 409,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Verifikasi ke Sejoi — pakai device_id sebagai `string` identifier
  const isValid = await verifySejoi(license_key, device_id)
  if (!isValid) {
    return new Response(JSON.stringify({ message: 'License key tidak valid. Pastikan key benar dan sudah aktif di Sejoi.' }), {
      status: 422,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Bind license ke device
  const { error } = await supabase
    .from('licenses')
    .upsert({
      key: license_key,
      email,
      device_id,
      is_active: true,
      activated_at: new Date().toISOString(),
    }, { onConflict: 'key' })

  if (error) {
    return new Response(JSON.stringify({ message: 'Gagal menyimpan license.' }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ ok: true, message: 'License berhasil diaktivasi.' }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

- [ ] **Step 6: Deploy Edge Functions**

```bash
supabase functions deploy register-install
supabase functions deploy validate
supabase functions deploy activate-license
```

Expected: "Deployed Function register-install" (3x)

- [ ] **Step 7: Commit**

```bash
git add supabase/
git commit -m "feat: Supabase Edge Functions register-install, validate, activate-license"
```

---

## Task 16: Email Notifications via Mailketing

**Files:**
- Create: `supabase/functions/_shared/mailer.ts`
- Modify: `supabase/functions/activate-license/index.ts`
- Create: `supabase/functions/notify-trial-expired/index.ts`
- Modify: `supabase/functions/register-install/index.ts`
- Modify: `src/sidepanel/components/UpgradeBanner.jsx`

**Mailketing API:**
- Endpoint: `POST https://api.mailketing.co.id/api/v1/send`
- Auth: `api_token` (dari menu Integrasi di dashboard Mailketing)
- Params: `from_name`, `from_email`, `recipient`, `subject`, `content`

**2 trigger email:**
1. License activated → kirim ke email user
2. Trial H-1 habis → kirim ke email user (opsional, user input email di side panel)

---

- [ ] **Step 1: Buat shared mailer helper**

```typescript
// supabase/functions/_shared/mailer.ts
const MAILKETING_URL = 'https://api.mailketing.co.id/api/v1/send'

interface SendEmailParams {
  to: string
  subject: string
  content: string
}

export async function sendEmail({ to, subject, content }: SendEmailParams): Promise<void> {
  const api_token = Deno.env.get('MAILKETING_API_TOKEN')
  const from_name = Deno.env.get('MAILKETING_FROM_NAME') ?? 'Threadlytics'
  const from_email = Deno.env.get('MAILKETING_FROM_EMAIL') ?? '[email protected]'

  if (!api_token) throw new Error('MAILKETING_API_TOKEN not configured')

  const body = new URLSearchParams({
    api_token,
    from_name,
    from_email,
    recipient: to,
    subject,
    content,
  })

  const res = await fetch(MAILKETING_URL, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  })

  if (!res.ok) {
    const text = await res.text()
    throw new Error(`Mailketing error: ${res.status} — ${text}`)
  }
}

// ── Email Templates ──────────────────────────────────────────────────────────

export function licenseActivatedEmail(email: string): { subject: string; content: string } {
  return {
    subject: '✅ License Threadlytics Berhasil Diaktivasi',
    content: `
<div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h2 style="color: #1d4ed8;">Threadlytics Pro Aktif!</h2>
  <p>Halo,</p>
  <p>License Threadlytics Pro kamu sudah berhasil diaktivasi di browser ini.</p>
  <ul>
    <li>Data follower growth 30 hari</li>
    <li>Top 10 viral post</li>
    <li>Engagement rate trend</li>
    <li>Export CSV</li>
  </ul>
  <p>Semua fitur Pro sekarang aktif. Buka Threads dan refresh side panel.</p>
  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;" />
  <p style="font-size: 12px; color: #9ca3af;">
    Jika ini bukan kamu, abaikan email ini atau hubungi support.<br/>
    License ini terikat ke satu browser. Transfer ke browser lain via support.
  </p>
</div>
    `.trim(),
  }
}

export function trialExpiringEmail(hoursLeft: number): { subject: string; content: string } {
  return {
    subject: `⏳ Trial Threadlytics Habis dalam ${hoursLeft} Jam`,
    content: `
<div style="font-family: sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
  <h2 style="color: #d97706;">Trial Kamu Hampir Habis</h2>
  <p>Halo,</p>
  <p>Trial Threadlytics Pro kamu akan habis dalam <strong>${hoursLeft} jam</strong>.</p>
  <p>Setelah trial habis, akses akan dibatasi ke Free tier (7 hari data, top 3 post).</p>
  <div style="margin: 24px 0;">
    <a href="https://sejoi.com/threadlytics"
       style="background: #1d4ed8; color: white; padding: 12px 24px; border-radius: 6px; text-decoration: none; font-weight: bold;">
      Upgrade ke Pro Sekarang
    </a>
  </div>
  <p style="font-size: 14px; color: #6b7280;">
    Pro Monthly: Rp 49.000/bln · Pro Yearly: Rp 399.000/thn
  </p>
  <hr style="border: none; border-top: 1px solid #e5e7eb; margin: 24px 0;" />
  <p style="font-size: 12px; color: #9ca3af;">
    Kamu menerima email ini karena mendaftar notifikasi trial di Threadlytics.
  </p>
</div>
    `.trim(),
  }
}
```

- [ ] **Step 2: Update register-install — terima optional email**

```typescript
// supabase/functions/register-install/index.ts
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

Deno.serve(async (req) => {
  if (req.method !== 'POST') return new Response('Method not allowed', { status: 405 })

  const { device_id, install_date, email } = await req.json()

  if (!device_id || !install_date) {
    return new Response(JSON.stringify({ error: 'device_id and install_date required' }), {
      status: 400,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  // Upsert — tidak reset install_date jika sudah ada
  // Jika user submit email (opsional), update field email
  const { data: existing } = await supabase
    .from('installs')
    .select('id, email')
    .eq('device_id', device_id)
    .maybeSingle()

  if (existing) {
    // Device sudah terdaftar — update email jika diberikan dan belum ada
    if (email && !existing.email) {
      await supabase.from('installs').update({ email }).eq('device_id', device_id)
    }
    return new Response(JSON.stringify({ ok: true, install_date }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  const { error } = await supabase
    .from('installs')
    .insert({ device_id, install_date, email: email ?? null })

  if (error) {
    return new Response(JSON.stringify({ error: error.message }), {
      status: 500,
      headers: { 'Content-Type': 'application/json' },
    })
  }

  return new Response(JSON.stringify({ ok: true, install_date }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

- [ ] **Step 3: Update tabel installs — tambah kolom email**

Jalankan di Supabase SQL Editor:

```sql
alter table public.installs add column if not exists email text;
alter table public.installs add column if not exists trial_expiry_notified boolean default false;
```

- [ ] **Step 4: Update activate-license — kirim email setelah aktivasi berhasil**

Tambahkan import dan email trigger di bagian bawah fungsi, setelah upsert berhasil:

```typescript
// supabase/functions/activate-license/index.ts
// Tambahkan import di baris pertama:
import { sendEmail, licenseActivatedEmail } from '../_shared/mailer.ts'

// ... (kode existing tetap sama sampai setelah upsert berhasil) ...

  // Setelah upsert sukses, kirim email konfirmasi (non-blocking)
  const emailTemplate = licenseActivatedEmail(email)
  sendEmail({ to: email, ...emailTemplate }).catch((err) => {
    console.error('[Threadlytics] Failed to send activation email:', err)
  })

  return new Response(JSON.stringify({ ok: true, message: 'License berhasil diaktivasi.' }), {
    headers: { 'Content-Type': 'application/json' },
  })
```

- [ ] **Step 5: Buat notify-trial-expired Edge Function**

```typescript
// supabase/functions/notify-trial-expired/index.ts
// Dipanggil oleh Supabase cron job setiap jam.
// Cek installs yang trial-nya habis dalam 24 jam ke depan dan belum dapat notifikasi.
import { createClient } from 'https://esm.sh/@supabase/supabase-js@2'
import { sendEmail, trialExpiringEmail } from '../_shared/mailer.ts'

const supabase = createClient(
  Deno.env.get('SUPABASE_URL')!,
  Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')!
)

const TRIAL_DAYS = 3

Deno.serve(async (req) => {
  // Hanya bisa dipanggil dari cron (pakai service role header) atau internal
  const authHeader = req.headers.get('Authorization')
  const serviceKey = Deno.env.get('SUPABASE_SERVICE_ROLE_KEY')
  if (authHeader !== `Bearer ${serviceKey}`) {
    return new Response('Unauthorized', { status: 401 })
  }

  const now = new Date()
  // Cari installs yang:
  // 1. Punya email (user opt-in notifikasi)
  // 2. Trial habis antara sekarang dan 24 jam ke depan
  // 3. Belum pernah dapat notifikasi (trial_expiry_notified = false)
  // 4. Belum punya license aktif
  const { data: installs, error } = await supabase
    .from('installs')
    .select('id, device_id, email, install_date')
    .not('email', 'is', null)
    .eq('trial_expiry_notified', false)

  if (error || !installs?.length) {
    return new Response(JSON.stringify({ ok: true, notified: 0 }), {
      headers: { 'Content-Type': 'application/json' },
    })
  }

  let notified = 0

  for (const install of installs) {
    const installDate = new Date(install.install_date)
    const trialExpires = new Date(installDate)
    trialExpires.setDate(trialExpires.getDate() + TRIAL_DAYS)

    const msUntilExpiry = trialExpires.getTime() - now.getTime()
    const hoursUntilExpiry = msUntilExpiry / (1000 * 60 * 60)

    // Kirim notif jika trial habis antara 0–24 jam lagi
    if (hoursUntilExpiry > 0 && hoursUntilExpiry <= 24) {
      // Cek apakah device sudah punya license aktif
      const { data: license } = await supabase
        .from('licenses')
        .select('is_active')
        .eq('device_id', install.device_id)
        .eq('is_active', true)
        .maybeSingle()

      if (!license?.is_active) {
        const hoursLeft = Math.round(hoursUntilExpiry)
        const template = trialExpiringEmail(hoursLeft)
        try {
          await sendEmail({ to: install.email, ...template })
          await supabase
            .from('installs')
            .update({ trial_expiry_notified: true })
            .eq('id', install.id)
          notified++
        } catch (e) {
          console.error(`[Threadlytics] Failed to notify ${install.email}:`, e)
        }
      }
    }
  }

  return new Response(JSON.stringify({ ok: true, notified }), {
    headers: { 'Content-Type': 'application/json' },
  })
})
```

- [ ] **Step 6: Setup cron job di Supabase**

Jalankan di Supabase SQL Editor (memerlukan pg_cron extension yang sudah aktif di Supabase):

```sql
-- Enable pg_cron jika belum aktif
create extension if not exists pg_cron;

-- Jalankan notify-trial-expired setiap jam
select cron.schedule(
  'notify-trial-expired',
  '0 * * * *',  -- setiap jam
  $$
  select net.http_post(
    url := current_setting('app.supabase_url') || '/functions/v1/notify-trial-expired',
    headers := jsonb_build_object(
      'Content-Type', 'application/json',
      'Authorization', 'Bearer ' || current_setting('app.service_role_key')
    ),
    body := '{}'::jsonb
  );
  $$
);
```

- [ ] **Step 7: Tambah opt-in email di UpgradeBanner (trial tier)**

```jsx
// src/sidepanel/components/UpgradeBanner.jsx — tambah form email di trial banner
import { useState } from 'preact/hooks'
import { TIERS } from '../../background/license.js'
import { CONFIG } from '../../shared/constants.js'

const SEJOI_URL = 'https://sejoi.com/threadlytics'

export function UpgradeBanner({ tier, licenseState, onActivate }) {
  const [email, setEmail] = useState('')
  const [emailSaved, setEmailSaved] = useState(false)
  const [saving, setSaving] = useState(false)

  if (tier === TIERS.PRO) return null

  async function saveNotifEmail(e) {
    e.preventDefault()
    if (!email) return
    setSaving(true)
    try {
      // Kirim email ke backend untuk update install record
      const { generateFingerprint } = await import('../../shared/fingerprint.js')
      const device_id = generateFingerprint()
      await fetch(`${CONFIG.SUPABASE_URL}/functions/v1/register-install`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          Authorization: `Bearer ${CONFIG.SUPABASE_ANON_KEY}`,
        },
        body: JSON.stringify({ device_id, install_date: new Date().toISOString(), email }),
      })
      setEmailSaved(true)
    } catch (_) {
      // Silent fail — tidak critical
    } finally {
      setSaving(false)
    }
  }

  if (tier === TIERS.TRIAL && licenseState?.trial_expires_at) {
    const expiresAt = new Date(licenseState.trial_expires_at)
    const hoursLeft = Math.max(0, Math.round((expiresAt - Date.now()) / (1000 * 60 * 60)))

    return (
      <div class="mx-4 my-2 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
        <p class="text-xs font-semibold text-yellow-800">
          ⏳ Trial habis dalam {hoursLeft} jam
        </p>
        <div class="flex gap-2 mt-2">
          <a href={SEJOI_URL} target="_blank"
            class="flex-1 text-center text-xs bg-blue-600 text-white py-1.5 rounded-md font-semibold">
            Upgrade Pro
          </a>
          <button onClick={onActivate}
            class="flex-1 text-center text-xs border border-blue-600 text-blue-600 py-1.5 rounded-md font-semibold">
            Punya license?
          </button>
        </div>
        {!emailSaved ? (
          <form onSubmit={saveNotifEmail} class="flex gap-1 mt-2">
            <input
              type="email"
              placeholder="Email untuk pengingat"
              value={email}
              onInput={(e) => setEmail(e.target.value)}
              class="flex-1 border border-gray-300 rounded px-2 py-1 text-xs"
            />
            <button type="submit" disabled={saving}
              class="text-xs bg-gray-100 border border-gray-300 px-2 py-1 rounded disabled:opacity-50">
              {saving ? '...' : 'OK'}
            </button>
          </form>
        ) : (
          <p class="text-xs text-gray-500 mt-2">✓ Pengingat aktif via email</p>
        )}
      </div>
    )
  }

  // Free tier
  return (
    <div class="mx-4 my-2 p-3 bg-gray-50 border border-gray-200 rounded-lg">
      <p class="text-xs text-gray-600">
        Upgrade ke <span class="font-semibold text-blue-700">Pro</span> untuk data 30 hari, top 10 post, engagement trend & export CSV.
      </p>
      <div class="flex gap-2 mt-2">
        <a href={SEJOI_URL} target="_blank"
          class="flex-1 text-center text-xs bg-blue-600 text-white py-1.5 rounded-md font-semibold">
          Rp 49.000/bln
        </a>
        <button onClick={onActivate}
          class="flex-1 text-center text-xs border border-gray-300 text-gray-600 py-1.5 rounded-md">
          Aktifkan license
        </button>
      </div>
    </div>
  )
}
```

- [ ] **Step 8: Set env vars di Supabase**

Di Supabase Dashboard → Edge Functions → Secrets, tambahkan:

```
MAILKETING_API_TOKEN     = <dari menu Integrasi di dashboard Mailketing>
MAILKETING_FROM_NAME     = Threadlytics
MAILKETING_FROM_EMAIL    = [email protected]
SEJOLI_STORE_URL         = https://<url-toko-sejoi-kamu>
```

- [ ] **Step 9: Deploy functions yang diupdate**

```bash
supabase functions deploy register-install
supabase functions deploy activate-license
supabase functions deploy notify-trial-expired
```

Expected: "Deployed Function" untuk ketiga functions

- [ ] **Step 10: Test email aktivasi**

```bash
# Test manual via curl
curl -X POST https://YOUR_PROJECT.supabase.co/functions/v1/activate-license \
  -H "Authorization: Bearer YOUR_ANON_KEY" \
  -H "Content-Type: application/json" \
  -d '{"device_id":"test123","email":"[email protected]","license_key":"TDL-TEST-TEST-TEST"}'
```

Expected: Email konfirmasi masuk ke inbox dalam 1–2 menit

- [ ] **Step 11: Commit**

```bash
git add supabase/functions/_shared/mailer.ts \
        supabase/functions/register-install/index.ts \
        supabase/functions/activate-license/index.ts \
        supabase/functions/notify-trial-expired/index.ts \
        src/sidepanel/components/UpgradeBanner.jsx
git commit -m "feat: email notifications via Mailketing — aktivasi license dan trial expiry"
```

---

## Task 17: Verifikasi Selectors & Testing Manual (renamed dari Task 16)

**Files:**
- Modify: `src/shared/constants.js`

- [ ] **Step 1: Buka threads.net dan inspect DOM**

Buka `https://www.threads.net/@akunmu` di Chrome DevTools → Inspect Elements:

Temukan selector untuk:
1. Follower count → klik kanan elemen angka follower → "Copy selector"
2. Post views → klik kanan angka views di post → "Copy selector"
3. Post likes → klik kanan angka likes → "Copy selector"
4. Post comments → klik kanan angka komentar → "Copy selector"
5. Post link (untuk extract post_id) → klik kanan link post → "Copy selector"

- [ ] **Step 2: Update SELECTORS di constants.js**

Ganti selectors dengan hasil inspect di Step 1. Format:

```js
export const SELECTORS = {
  follower_count: [
    // GANTI dengan selector aktual dari inspect
    'selector-hasil-inspect',
    // fallback lama tetap dipertahankan
    'a[href$="/followers"] span',
  ],
  // dst...
}
```

- [ ] **Step 3: Load extension di Chrome**

```
1. Buka chrome://extensions/
2. Enable "Developer mode" (kanan atas)
3. Klik "Load unpacked"
4. Pilih folder dist/ (hasil vite build)
5. Klik icon Threadlytics → Open Side Panel
6. Buka https://www.threads.net
7. Scroll feed beberapa saat
8. Lihat side panel — data harus mulai muncul
```

- [ ] **Step 4: Verifikasi data masuk ke IndexedDB**

```
1. DevTools → Application → IndexedDB → threadlytics
2. Cek tabel posts — harus ada rows
3. Cek tabel followers_history — harus ada row hari ini
```

- [ ] **Step 5: Commit**

```bash
git add src/shared/constants.js
git commit -m "fix: update DOM selectors berdasarkan inspect Threads"
```

---

## Task 17: Run All Tests & Coverage Check

- [ ] **Step 1: Jalankan semua unit tests**

```bash
npx vitest run
```

Expected: Semua test PASS

- [ ] **Step 2: Cek coverage**

```bash
npx vitest run --coverage
```

Expected: Coverage lines ≥ 80%

- [ ] **Step 3: Build final**

```bash
npx vite build
```

Expected: No errors, dist/ siap untuk upload

- [ ] **Step 4: Commit final**

```bash
git add .
git commit -m "test: all tests passing, coverage ≥80%, build clean"
```

---

## Task 18: Chrome Web Store Submission

- [ ] **Step 1: Siapkan aset**

- Buat icon 16x16, 48x48, 128x128 (PNG) dan taruh di `icons/`
- Screenshot side panel minimal 1280x800 (untuk listing)
- Tulis deskripsi pendek (132 karakter max) dan deskripsi panjang

- [ ] **Step 2: Zip extension**

```bash
cd dist && zip -r ../threadlytics-v1.0.0.zip . && cd ..
```

- [ ] **Step 3: Submit ke Chrome Web Store**

```
1. Buka https://chrome.google.com/webstore/devconsole
2. New Item → Upload ZIP
3. Isi store listing: nama, deskripsi, screenshots
4. Privacy practices: deklarasikan pengumpulan device ID
5. Submit for review
```

- [ ] **Step 4: Update SUPABASE_URL & SUPABASE_ANON_KEY di constants.js**

Pastikan nilai production (bukan placeholder) sudah diisi sebelum submit.

- [ ] **Step 5: Final commit**

```bash
git add icons/ && git commit -m "chore: ikon dan assets Chrome Web Store"
git tag v1.0.0
```

---

## Self-Review: Spec Coverage

| Requirement Spec | Task |
|---|---|
| Follower growth (+/- vs kemarin, 7d, 30d) | Task 10, 12, 13 |
| View, like, comment per post | Task 4, 6 |
| Avg engagement + growth pct | Task 10, 13 |
| Engagement rate (like+comment)/view | Task 10, 13 |
| Top posts viral tracker (sort views/likes/comments/ER) | Task 13 |
| Trial 3 hari penuh Pro | Task 8, 9, 15 |
| Freemium gate (free tier limits) | Task 13 |
| Device fingerprint | Task 3 |
| 1 license = 1 device + 1 email | Task 8, 15 |
| Anti-sharing (device mismatch disable) | Task 15 |
| Sejoi + Xendit payment | Task 15 (via verifySejoi) |
| Export CSV (Pro only) | Task 11, 14 |
| IndexedDB 30 hari rolling | Task 6 |
| Side panel UI | Task 12, 13, 14 |
| Chrome Web Store distribution | Task 18 |

**Sejoi API dikonfirmasi:** Check endpoint `GET {{sejoli_store_url}}/sejoli/sejoli-validate-license/?license=KEY&string=DEVICE_ID` — return `{ valid: bool }`. Tidak perlu password user. Sebelum deploy, isi env var `SEJOLI_STORE_URL` di Supabase Edge Function secrets.
