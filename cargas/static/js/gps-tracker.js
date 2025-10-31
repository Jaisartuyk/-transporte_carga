// GPS Tracker para rastreo en tiempo real
class GPSTracker {
    constructor(options = {}) {
        this.watchId = null;
        this.isTracking = false;
        this.updateInterval = options.updateInterval || 30000; // 30 segundos por defecto
        this.highAccuracy = options.highAccuracy !== false;
        this.onLocationUpdate = options.onLocationUpdate || null;
        this.onError = options.onError || null;
        this.lastPosition = null;
        this.websocket = null;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.locationHistory = [];
        this.maxHistorySize = 100;
        
        // IndexedDB para almacenamiento offline
        this.db = null;
        this.initIndexedDB();
    }
    
    // Inicializar IndexedDB
    async initIndexedDB() {
        try {
            this.db = await this.openDatabase();
            console.log('[GPS] IndexedDB inicializado');
        } catch (error) {
            console.error('[GPS] Error al inicializar IndexedDB:', error);
        }
    }
    
    openDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('CargoTrackDB', 1);
            
            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);
            
            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('pendingLocations')) {
                    db.createObjectStore('pendingLocations', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('locationHistory')) {
                    const store = db.createObjectStore('locationHistory', { keyPath: 'id', autoIncrement: true });
                    store.createIndex('timestamp', 'timestamp', { unique: false });
                }
            };
        });
    }
    
    // Iniciar rastreo GPS
    startTracking() {
        if (!navigator.geolocation) {
            const error = 'GPS no disponible en este dispositivo';
            console.error('[GPS]', error);
            if (this.onError) this.onError(error);
            return false;
        }
        
        if (this.isTracking) {
            console.log('[GPS] Ya está rastreando');
            return true;
        }
        
        console.log('[GPS] Iniciando rastreo...');
        
        // WebSocket deshabilitado - usando solo API REST
        // this.connectWebSocket();
        
        // Opciones de geolocalización
        const options = {
            enableHighAccuracy: this.highAccuracy,
            timeout: 10000,
            maximumAge: 0
        };
        
        // Obtener posición inicial
        navigator.geolocation.getCurrentPosition(
            (position) => {
                console.log('[GPS] Posición inicial obtenida');
                this.handlePosition(position);
            },
            (error) => {
                console.error('[GPS] Error al obtener posición inicial:', error);
                if (this.onError) this.onError(error.message);
            },
            options
        );
        
        // Iniciar watchPosition
        this.watchId = navigator.geolocation.watchPosition(
            (position) => this.handlePosition(position),
            (error) => this.handleError(error),
            options
        );
        
        this.isTracking = true;
        
        // Registrar sincronización en segundo plano
        this.registerBackgroundSync();
        
        return true;
    }
    
    // Detener rastreo GPS
    stopTracking() {
        if (!this.isTracking) {
            console.log('[GPS] No está rastreando');
            return;
        }
        
        console.log('[GPS] Deteniendo rastreo...');
        
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }
        
        if (this.websocket) {
            this.websocket.close();
            this.websocket = null;
        }
        
        this.isTracking = false;
    }
    
    // Manejar nueva posición
    handlePosition(position) {
        const coords = {
            lat: position.coords.latitude,
            lng: position.coords.longitude,
            accuracy: position.coords.accuracy,
            altitude: position.coords.altitude,
            altitudeAccuracy: position.coords.altitudeAccuracy,
            heading: position.coords.heading,
            speed: position.coords.speed,
            timestamp: new Date(position.timestamp).toISOString()
        };
        
        console.log('[GPS] Nueva posición:', coords);
        
        // Guardar en historial
        this.addToHistory(coords);
        
        // Guardar última posición
        this.lastPosition = coords;
        
        // Callback
        if (this.onLocationUpdate) {
            this.onLocationUpdate(coords);
        }
        
        // Enviar al servidor
        this.sendLocation(coords);
    }
    
    // Manejar errores
    handleError(error) {
        let errorMessage = 'Error desconocido';
        
        switch(error.code) {
            case error.PERMISSION_DENIED:
                errorMessage = 'Permiso de ubicación denegado';
                break;
            case error.POSITION_UNAVAILABLE:
                errorMessage = 'Ubicación no disponible';
                break;
            case error.TIMEOUT:
                errorMessage = 'Tiempo de espera agotado';
                break;
        }
        
        console.error('[GPS]', errorMessage, error);
        
        if (this.onError) {
            this.onError(errorMessage);
        }
    }
    
    // Conectar WebSocket
    connectWebSocket() {
        if (this.websocket && this.websocket.readyState === WebSocket.OPEN) {
            console.log('[GPS] WebSocket ya conectado');
            return;
        }
        
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/location/`;
        
        console.log('[GPS] Conectando WebSocket:', wsUrl);
        
        try {
            this.websocket = new WebSocket(wsUrl);
            
            this.websocket.onopen = () => {
                console.log('[GPS] WebSocket conectado');
                this.reconnectAttempts = 0;
                
                // Enviar última posición si existe
                if (this.lastPosition) {
                    this.sendLocationViaWebSocket(this.lastPosition);
                }
            };
            
            this.websocket.onmessage = (event) => {
                const data = JSON.parse(event.data);
                console.log('[GPS] Mensaje WebSocket:', data);
            };
            
            this.websocket.onerror = (error) => {
                console.error('[GPS] Error WebSocket:', error);
            };
            
            this.websocket.onclose = () => {
                console.log('[GPS] WebSocket cerrado');
                this.websocket = null;
                
                // Intentar reconectar
                if (this.isTracking && this.reconnectAttempts < this.maxReconnectAttempts) {
                    this.reconnectAttempts++;
                    console.log(`[GPS] Reintentando conexión (${this.reconnectAttempts}/${this.maxReconnectAttempts})...`);
                    setTimeout(() => this.connectWebSocket(), 5000);
                }
            };
        } catch (error) {
            console.error('[GPS] Error al crear WebSocket:', error);
        }
    }
    
    // Enviar ubicación al servidor (solo API REST, sin WebSocket)
    async sendLocation(coords) {
        // Usar solo API REST (WebSocket deshabilitado temporalmente)
        await this.sendLocationViaAPI(coords);
    }
    
    // Enviar vía WebSocket
    sendLocationViaWebSocket(coords) {
        try {
            this.websocket.send(JSON.stringify({
                type: 'location_update',
                data: coords
            }));
            console.log('[GPS] Ubicación enviada vía WebSocket');
        } catch (error) {
            console.error('[GPS] Error al enviar vía WebSocket:', error);
            this.sendLocationViaAPI(coords);
        }
    }
    
    // Enviar vía API REST
    async sendLocationViaAPI(coords) {
        try {
            console.log('[GPS] 📤 Enviando ubicación vía API...', coords);
            
            const csrfToken = this.getCookie('csrftoken');
            console.log('[GPS] 🔑 CSRF Token:', csrfToken ? 'Presente' : 'NO ENCONTRADO');
            
            const response = await fetch('/api/ubicacion/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify(coords)
            });
            
            console.log('[GPS] 📡 Respuesta del servidor:', response.status, response.statusText);
            
            if (response.ok) {
                const data = await response.json();
                console.log('[GPS] ✅ Ubicación enviada exitosamente:', data);
            } else {
                const errorText = await response.text();
                console.error('[GPS] ❌ Error del servidor:', response.status, errorText);
                throw new Error(`HTTP ${response.status}: ${errorText}`);
            }
        } catch (error) {
            console.error('[GPS] ❌ Error al enviar vía API:', error);
            // Guardar en IndexedDB para sincronizar después
            await this.savePendingLocation(coords);
        }
    }
    
    // Guardar ubicación pendiente en IndexedDB
    async savePendingLocation(coords) {
        if (!this.db) return;
        
        try {
            const transaction = this.db.transaction(['pendingLocations'], 'readwrite');
            const store = transaction.objectStore('pendingLocations');
            await store.add(coords);
            console.log('[GPS] Ubicación guardada para sincronizar después');
        } catch (error) {
            console.error('[GPS] Error al guardar en IndexedDB:', error);
        }
    }
    
    // Agregar al historial
    addToHistory(coords) {
        this.locationHistory.push(coords);
        
        // Limitar tamaño del historial
        if (this.locationHistory.length > this.maxHistorySize) {
            this.locationHistory.shift();
        }
        
        // Guardar en IndexedDB
        this.saveToHistory(coords);
    }
    
    // Guardar en historial de IndexedDB
    async saveToHistory(coords) {
        if (!this.db) return;
        
        try {
            const transaction = this.db.transaction(['locationHistory'], 'readwrite');
            const store = transaction.objectStore('locationHistory');
            await store.add(coords);
        } catch (error) {
            console.error('[GPS] Error al guardar historial:', error);
        }
    }
    
    // Registrar sincronización en segundo plano
    registerBackgroundSync() {
        if ('serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype) {
            navigator.serviceWorker.ready.then((registration) => {
                return registration.sync.register('sync-location');
            }).then(() => {
                console.log('[GPS] Background sync registrado');
            }).catch((error) => {
                console.error('[GPS] Error al registrar background sync:', error);
            });
        }
    }
    
    // Obtener cookie CSRF
    getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    // Obtener última posición
    getLastPosition() {
        return this.lastPosition;
    }
    
    // Obtener historial
    getHistory() {
        return this.locationHistory;
    }
    
    // Verificar si está rastreando
    isActive() {
        return this.isTracking;
    }
}

// Exportar
window.GPSTracker = GPSTracker;

console.log('[GPS] Módulo GPS Tracker cargado');
