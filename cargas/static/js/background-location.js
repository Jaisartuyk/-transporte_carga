/**
 * 📍 BACKGROUND GEOLOCATION TRACKER
 * Sistema de rastreo GPS en segundo plano para PWA
 * Funciona incluso cuando la app está minimizada
 */

class BackgroundLocationTracker {
    constructor() {
        this.watchId = null;
        this.wakeLock = null;
        this.isTracking = false;
        this.lastPosition = null;
        this.updateInterval = 30000; // 30 segundos
        this.minDistance = 10; // 10 metros mínimo de movimiento
        
        console.log('🎯 Background Location Tracker inicializado');
    }

    /**
     * Iniciar rastreo en segundo plano
     */
    async startTracking(envioId) {
        if (this.isTracking) {
            console.log('⚠️ Ya está rastreando');
            return;
        }

        console.log('🚀 Iniciando rastreo en segundo plano...');
        
        try {
            // 1. Solicitar permisos de ubicación
            const permission = await this.requestLocationPermission();
            if (!permission) {
                throw new Error('Permiso de ubicación denegado');
            }

            // 2. Solicitar Wake Lock (mantener pantalla activa)
            await this.requestWakeLock();

            // 3. Iniciar rastreo continuo
            this.startContinuousTracking(envioId);

            // 4. Registrar Background Sync
            await this.registerBackgroundSync();

            // 5. Mostrar notificación persistente
            this.showTrackingNotification();

            this.isTracking = true;
            console.log('✅ Rastreo en segundo plano activado');

        } catch (error) {
            console.error('❌ Error al iniciar rastreo:', error);
            throw error;
        }
    }

    /**
     * Detener rastreo
     */
    stopTracking() {
        console.log('🛑 Deteniendo rastreo...');

        // Detener watch de ubicación
        if (this.watchId) {
            navigator.geolocation.clearWatch(this.watchId);
            this.watchId = null;
        }

        // Liberar Wake Lock
        if (this.wakeLock) {
            this.wakeLock.release();
            this.wakeLock = null;
        }

        this.isTracking = false;
        console.log('✅ Rastreo detenido');
    }

    /**
     * Solicitar permisos de ubicación
     */
    async requestLocationPermission() {
        if (!('geolocation' in navigator)) {
            alert('Tu dispositivo no soporta geolocalización');
            return false;
        }

        try {
            // Intentar obtener ubicación para verificar permisos
            const position = await new Promise((resolve, reject) => {
                navigator.geolocation.getCurrentPosition(resolve, reject, {
                    enableHighAccuracy: true,
                    timeout: 10000,
                    maximumAge: 0
                });
            });

            console.log('✅ Permiso de ubicación concedido');
            return true;

        } catch (error) {
            console.error('❌ Permiso de ubicación denegado:', error);
            alert('Por favor, permite el acceso a tu ubicación para usar el rastreo GPS');
            return false;
        }
    }

    /**
     * Solicitar Wake Lock (mantener dispositivo activo)
     */
    async requestWakeLock() {
        if (!('wakeLock' in navigator)) {
            console.warn('⚠️ Wake Lock API no disponible');
            return;
        }

        try {
            this.wakeLock = await navigator.wakeLock.request('screen');
            console.log('✅ Wake Lock activado');

            // Re-adquirir wake lock si se pierde
            this.wakeLock.addEventListener('release', () => {
                console.log('⚠️ Wake Lock liberado');
            });

        } catch (error) {
            console.error('❌ Error al solicitar Wake Lock:', error);
        }
    }

    /**
     * Rastreo continuo de ubicación
     */
    startContinuousTracking(envioId) {
        const options = {
            enableHighAccuracy: true,
            timeout: 30000,
            maximumAge: 0
        };

        this.watchId = navigator.geolocation.watchPosition(
            (position) => this.handlePositionUpdate(position, envioId),
            (error) => this.handlePositionError(error),
            options
        );

        console.log('📡 Watch Position iniciado');
    }

    /**
     * Manejar actualización de posición
     */
    async handlePositionUpdate(position, envioId) {
        const coords = {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
            accuracy: position.coords.accuracy,
            speed: position.coords.speed,
            heading: position.coords.heading,
            timestamp: new Date().toISOString()
        };

        console.log('📍 Nueva posición:', coords);

        // Verificar si se movió lo suficiente
        if (this.lastPosition && !this.hasMovedEnough(coords)) {
            console.log('⏭️ Movimiento insuficiente, omitiendo...');
            return;
        }

        // Enviar ubicación al servidor
        try {
            await this.sendLocationToServer(envioId, coords);
            this.lastPosition = coords;

            // Actualizar notificación
            this.updateTrackingNotification(coords);

        } catch (error) {
            console.error('❌ Error al enviar ubicación:', error);
            // Guardar en IndexedDB para sincronizar después
            await this.saveLocationOffline(envioId, coords);
        }
    }

    /**
     * Verificar si se movió lo suficiente
     */
    hasMovedEnough(newCoords) {
        if (!this.lastPosition) return true;

        const distance = this.calculateDistance(
            this.lastPosition.latitude,
            this.lastPosition.longitude,
            newCoords.latitude,
            newCoords.longitude
        );

        return distance >= this.minDistance;
    }

    /**
     * Calcular distancia entre dos puntos (Haversine)
     */
    calculateDistance(lat1, lon1, lat2, lon2) {
        const R = 6371e3; // Radio de la Tierra en metros
        const φ1 = lat1 * Math.PI / 180;
        const φ2 = lat2 * Math.PI / 180;
        const Δφ = (lat2 - lat1) * Math.PI / 180;
        const Δλ = (lon2 - lon1) * Math.PI / 180;

        const a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
                  Math.cos(φ1) * Math.cos(φ2) *
                  Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
        const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return R * c; // Distancia en metros
    }

    /**
     * Enviar ubicación al servidor
     */
    async sendLocationToServer(envioId, coords) {
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

        const response = await fetch('/api/ubicacion/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify({
                envio_id: envioId,
                latitud: coords.latitude,
                longitud: coords.longitude,
                precision: coords.accuracy,
                velocidad: coords.speed,
                rumbo: coords.heading,
                timestamp: coords.timestamp
            })
        });

        if (!response.ok) {
            throw new Error(`HTTP ${response.status}`);
        }

        console.log('✅ Ubicación enviada al servidor');
    }

    /**
     * Guardar ubicación offline en IndexedDB
     */
    async saveLocationOffline(envioId, coords) {
        if (!('indexedDB' in window)) return;

        try {
            const db = await this.openDatabase();
            const tx = db.transaction('locations', 'readwrite');
            const store = tx.objectStore('locations');

            await store.add({
                envioId: envioId,
                coords: coords,
                synced: false,
                timestamp: Date.now()
            });

            console.log('💾 Ubicación guardada offline');

        } catch (error) {
            console.error('❌ Error al guardar offline:', error);
        }
    }

    /**
     * Abrir base de datos IndexedDB
     */
    openDatabase() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open('GPSTrackerDB', 1);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => resolve(request.result);

            request.onupgradeneeded = (event) => {
                const db = event.target.result;
                if (!db.objectStoreNames.contains('locations')) {
                    db.createObjectStore('locations', { keyPath: 'id', autoIncrement: true });
                }
            };
        });
    }

    /**
     * Registrar Background Sync
     */
    async registerBackgroundSync() {
        if (!('serviceWorker' in navigator) || !('sync' in navigator.serviceWorker)) {
            console.warn('⚠️ Background Sync no disponible');
            return;
        }

        try {
            const registration = await navigator.serviceWorker.ready;
            await registration.sync.register('sync-locations');
            console.log('✅ Background Sync registrado');

        } catch (error) {
            console.error('❌ Error al registrar Background Sync:', error);
        }
    }

    /**
     * Mostrar notificación de rastreo activo
     */
    async showTrackingNotification() {
        if (!('Notification' in window)) return;

        if (Notification.permission === 'granted') {
            new Notification('🚛 Rastreo GPS Activo', {
                body: 'Tu ubicación se está compartiendo en tiempo real',
                icon: '/static/icons/icon-192.png',
                badge: '/static/icons/badge-72.png',
                tag: 'gps-tracking',
                requireInteraction: true,
                silent: false
            });
        }
    }

    /**
     * Actualizar notificación con nueva ubicación
     */
    updateTrackingNotification(coords) {
        if (!('Notification' in window) || Notification.permission !== 'granted') return;

        const speed = coords.speed ? `${Math.round(coords.speed * 3.6)} km/h` : 'Detenido';

        new Notification('📍 Ubicación Actualizada', {
            body: `Velocidad: ${speed}\nPrecisión: ${Math.round(coords.accuracy)}m`,
            icon: '/static/icons/icon-192.png',
            tag: 'gps-update',
            silent: true
        });
    }

    /**
     * Manejar errores de ubicación
     */
    handlePositionError(error) {
        console.error('❌ Error de ubicación:', error);

        let message = 'Error al obtener ubicación';
        switch (error.code) {
            case error.PERMISSION_DENIED:
                message = 'Permiso de ubicación denegado';
                break;
            case error.POSITION_UNAVAILABLE:
                message = 'Ubicación no disponible';
                break;
            case error.TIMEOUT:
                message = 'Tiempo de espera agotado';
                break;
        }

        console.warn(`⚠️ ${message}`);
    }
}

// Instancia global
window.backgroundTracker = new BackgroundLocationTracker();

console.log('✅ Background Location Tracker cargado');
