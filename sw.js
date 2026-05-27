// 범퍼 수정일지 Service Worker
const CACHE = 'bumper-v3';

self.addEventListener('install', () => self.skipWaiting());

// 구버전 캐시 전체 삭제 후 클라이언트 즉시 인계
self.addEventListener('activate', e => e.waitUntil(
  caches.keys().then(keys =>
    Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
  ).then(() => clients.claim())
));

// 네트워크 우선 — 오프라인 시 캐시 폴백
self.addEventListener('fetch', e => {
  if (e.request.method !== 'GET') return;
  e.respondWith(
    fetch(e.request)
      .then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(c => c.put(e.request, clone));
        return res;
      })
      .catch(() => caches.match(e.request))
  );
});
