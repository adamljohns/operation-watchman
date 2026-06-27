// Operation Watchman — Service Worker
// Provides offline support via cache-first strategy

const CACHE_NAME = 'watchman-v6';
const PRECACHE_URLS = [
  '/',
  '/index.html',
  '/manifest.json',
  '/content/plans/index.json',
  '/content/plans/watchman-90.json',
  '/content/plans/proverbs-31.json'
];

// ── Install: pre-cache core assets ──
self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(PRECACHE_URLS))
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

// ── Fetch: network-first for HTML & plan content, cache-first for the rest ──
self.addEventListener('fetch', event => {
  const url = new URL(event.request.url);

  // Skip non-GET requests
  if (event.request.method !== 'GET') return;

  // Network-first for navigations and plan JSON so deployed updates reach
  // users on next load. Cache-first here would pin the old index.html
  // forever unless CACHE_NAME were manually bumped with every deploy.
  const isNavigation = event.request.mode === 'navigate';
  const isContent    = url.origin === self.location.origin && url.pathname.startsWith('/content/');
  if (isNavigation || isContent) {
    event.respondWith(
      fetch(event.request)
        .then(response => {
          if (response && response.status === 200) {
            const cloned = response.clone();
            caches.open(CACHE_NAME).then(cache => cache.put(event.request, cloned));
          }
          return response;
        })
        .catch(() =>
          caches.match(event.request).then(cached =>
            cached || (isNavigation ? caches.match('/index.html') : Response.error())
          )
        )
    );
    return;
  }

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
          // Offline fallback for navigation when no cached match exists
          if (event.request.mode === 'navigate') {
            return caches.match('/index.html');
          }
          return Response.error();
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
