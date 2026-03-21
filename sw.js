// Operation Watchman — Service Worker
// Provides offline support via cache-first strategy

const CACHE_NAME = 'watchman-v1';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  'https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Open+Sans:wght@400;600&display=swap'
];

// ── Install: pre-cache core assets ──
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS.filter(u => !u.startsWith('http'))))
      .then(() => self.skipWaiting())
  );
});

// ── Activate: clean old caches ──
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys
          .filter(key => key !== CACHE_NAME)
          .map(key => caches.delete(key))
      )
    ).then(() => self.clients.claim())
  );
});

// ── Fetch: cache-first for local, network-first for external ──
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Cache-first for same-origin
  if (url.origin === self.location.origin) {
    event.respondWith(
      caches.match(event.request).then(cached => {
        if (cached) return cached;
        return fetch(event.request).then(response => {
          if (!response || response.status !== 200 || response.type === 'opaque') {
            return response;
          }
          const cloned = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
          return response;
        }).catch(() => {
          // Offline fallback for navigation
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html');
          }
        });
      })
    );
    return;
  }

  // Network-first for Google Fonts (graceful degradation)
  if (url.hostname.includes('fonts.googleapis.com') || url.hostname.includes('fonts.gstatic.com')) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          const cloned = response.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
          return response;
        })
        .catch(() => caches.match(event.request))
    );
  }
});
