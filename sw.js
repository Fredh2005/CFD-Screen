// Cache the last build so opening the icon offline still shows the screen.
// The page is rebuilt server-side on a schedule, so the network copy always
// wins when there is a network.
const CACHE = 'cfd-screen-v3';
const ASSETS = ['./', './index.html', './manifest.webmanifest', './icon-192.png', './apple-touch-icon.png'];
self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting()));
});
self.addEventListener('activate', (event) => {
  event.waitUntil(caches.keys().then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  // no-cache: always revalidate with the server, so a push shows on the next open
  // instead of after GitHub Pages' 10-minute max-age.
  event.respondWith(fetch(event.request, { cache: 'no-cache' }).then((response) => {
    const copy = response.clone();
    caches.open(CACHE).then((c) => c.put(event.request, copy)).catch(() => {});
    return response;
  }).catch(() => caches.match(event.request).then((hit) => hit || caches.match('./index.html'))));
});
