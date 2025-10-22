// Service Worker para CargoTrack Pro PWA
const CACHE_NAME = 'cargotrack-v1.0.0';
const RUNTIME_CACHE = 'cargotrack-runtime';

// Recursos para cachear en instalación
const STATIC_CACHE_URLS = [
    '/',
    '/dashboard/',
    '/envios/',
    '/static/css/style.css',
    '/static/js/main.js',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css',
    'https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js',
    'https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css',
];

// Instalación del Service Worker
self.addEventListener('install', (event) => {
    console.log('[SW] Instalando Service Worker...');
    
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('[SW] Cacheando recursos estáticos');
                return cache.addAll(STATIC_CACHE_URLS.map(url => new Request(url, {credentials: 'same-origin'})));
            })
            .catch((error) => {
                console.error('[SW] Error al cachear:', error);
            })
    );
    
    // Activar inmediatamente
    self.skipWaiting();
});

// Activación del Service Worker
self.addEventListener('activate', (event) => {
    console.log('[SW] Activando Service Worker...');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME && cacheName !== RUNTIME_CACHE) {
                        console.log('[SW] Eliminando caché antiguo:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    // Tomar control inmediatamente
    return self.clients.claim();
});

// Estrategia de caché: Network First, fallback to Cache
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    // Ignorar requests que no sean GET
    if (request.method !== 'GET') {
        return;
    }
    
    // Ignorar requests a otros dominios (excepto CDN)
    if (url.origin !== location.origin && !url.host.includes('cdn.jsdelivr.net')) {
        return;
    }
    
    // Estrategia Network First para páginas HTML
    if (request.headers.get('accept').includes('text/html')) {
        event.respondWith(
            fetch(request)
                .then((response) => {
                    // Cachear la respuesta
                    const responseClone = response.clone();
                    caches.open(RUNTIME_CACHE).then((cache) => {
                        cache.put(request, responseClone);
                    });
                    return response;
                })
                .catch(() => {
                    // Si falla, buscar en caché
                    return caches.match(request).then((cachedResponse) => {
                        return cachedResponse || caches.match('/');
                    });
                })
        );
        return;
    }
    
    // Estrategia Cache First para recursos estáticos
    event.respondWith(
        caches.match(request).then((cachedResponse) => {
            if (cachedResponse) {
                return cachedResponse;
            }
            
            return fetch(request).then((response) => {
                // No cachear respuestas inválidas
                if (!response || response.status !== 200 || response.type === 'error') {
                    return response;
                }
                
                // Cachear la respuesta
                const responseClone = response.clone();
                caches.open(RUNTIME_CACHE).then((cache) => {
                    cache.put(request, responseClone);
                });
                
                return response;
            });
        })
    );
});

// Sincronización en segundo plano
self.addEventListener('sync', (event) => {
    console.log('[SW] Sync event:', event.tag);
    
    if (event.tag === 'sync-location') {
        event.waitUntil(syncPendingLocations());
    }
});

// Sincronizar ubicaciones pendientes
async function syncPendingLocations() {
    try {
        // Obtener ubicaciones pendientes de IndexedDB
        const db = await openIndexedDB();
        const locations = await getAllPendingLocations(db);
        
        if (locations.length === 0) {
            console.log('[SW] No hay ubicaciones pendientes');
            return;
        }
        
        console.log(`[SW] Sincronizando ${locations.length} ubicaciones pendientes`);
        
        // Enviar cada ubicación al servidor
        for (const location of locations) {
            try {
                const response = await fetch('/api/ubicacion/sync/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(location)
                });
                
                if (response.ok) {
                    // Eliminar de IndexedDB si se envió correctamente
                    await deletePendingLocation(db, location.id);
                    console.log('[SW] Ubicación sincronizada:', location.id);
                }
            } catch (error) {
                console.error('[SW] Error al sincronizar ubicación:', error);
            }
        }
    } catch (error) {
        console.error('[SW] Error en syncPendingLocations:', error);
    }
}

// Notificaciones Push
self.addEventListener('push', (event) => {
    console.log('[SW] Push recibido');
    
    let data = {
        title: 'CargoTrack Pro',
        body: 'Nueva notificación',
        icon: '/static/icons/icon-192.png',
        badge: '/static/icons/badge-72.png'
    };
    
    if (event.data) {
        try {
            data = event.data.json();
        } catch (e) {
            data.body = event.data.text();
        }
    }
    
    const options = {
        body: data.body,
        icon: data.icon || '/static/icons/icon-192.png',
        badge: data.badge || '/static/icons/badge-72.png',
        vibrate: [200, 100, 200, 100, 200],
        tag: data.tag || 'default',
        requireInteraction: data.requireInteraction || false,
        data: data.data || {},
        actions: data.actions || []
    };
    
    event.waitUntil(
        self.registration.showNotification(data.title, options)
    );
});

// Click en notificación
self.addEventListener('notificationclick', (event) => {
    console.log('[SW] Notificación clickeada:', event.notification.tag);
    
    event.notification.close();
    
    const urlToOpen = event.notification.data?.url || '/dashboard/';
    
    event.waitUntil(
        clients.matchAll({ type: 'window', includeUncontrolled: true })
            .then((clientList) => {
                // Si ya hay una ventana abierta, enfocarla
                for (const client of clientList) {
                    if (client.url === urlToOpen && 'focus' in client) {
                        return client.focus();
                    }
                }
                // Si no, abrir nueva ventana
                if (clients.openWindow) {
                    return clients.openWindow(urlToOpen);
                }
            })
    );
});

// Funciones auxiliares para IndexedDB
function openIndexedDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('CargoTrackDB', 1);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
        
        request.onupgradeneeded = (event) => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('pendingLocations')) {
                db.createObjectStore('pendingLocations', { keyPath: 'id', autoIncrement: true });
            }
        };
    });
}

function getAllPendingLocations(db) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pendingLocations'], 'readonly');
        const store = transaction.objectStore('pendingLocations');
        const request = store.getAll();
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve(request.result);
    });
}

function deletePendingLocation(db, id) {
    return new Promise((resolve, reject) => {
        const transaction = db.transaction(['pendingLocations'], 'readwrite');
        const store = transaction.objectStore('pendingLocations');
        const request = store.delete(id);
        
        request.onerror = () => reject(request.error);
        request.onsuccess = () => resolve();
    });
}

// Mensaje desde la aplicación
self.addEventListener('message', (event) => {
    console.log('[SW] Mensaje recibido:', event.data);
    
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});
