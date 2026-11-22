const CACHE='prisa-v13';
const ASSETS=['./','./index.html','./manifest.json','./map-118.svg','./images/store-map-208.png','./hub.png','./displays.jpg','./et-mark.png','./et-logo.jpg','./icon-192.png','./icon-512.png','./apple-touch-icon.png',
  './ic-gondola.jpg','./ic-sbox.jpg','./ic-wall.jpg','./ic-stage.jpg','./ic-small.jpg','./ic-stand.jpg'];
self.addEventListener('install',e=>{e.waitUntil(caches.open(CACHE).then(c=>c.addAll(ASSETS)));self.skipWaiting();});
self.addEventListener('activate',e=>{e.waitUntil(caches.keys().then(k=>Promise.all(k.filter(x=>x!==CACHE).map(x=>caches.delete(x)))));self.clients.claim();});
// קודם רשת (גרסה עדכנית), ואם אין אינטרנט — מהמטמון
self.addEventListener('fetch',e=>{
  const u=new URL(e.request.url);
  if(e.request.method!=='GET'||u.origin!==location.origin)return;
  if(u.pathname.endsWith('.mp4'))return; // סרטון: ישירות מהרשת
  e.respondWith(fetch(e.request).then(r=>{const c=r.clone();caches.open(CACHE).then(x=>x.put(e.request,c));return r;}).catch(()=>caches.match(e.request,{ignoreSearch:true})));
});
