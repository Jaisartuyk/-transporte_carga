// PWA Installation Handler
let deferredPrompt;
let isInstalled = false;

// Verificar si ya está instalada
if (window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true) {
    isInstalled = true;
    console.log('[PWA] App ya está instalada');
}

// Registrar Service Worker
if ('serviceWorker' in navigator) {
    window.addEventListener('load', () => {
        navigator.serviceWorker.register('/static/js/service-worker.js')
            .then((registration) => {
                console.log('[PWA] Service Worker registrado:', registration.scope);
                
                // Verificar actualizaciones cada hora
                setInterval(() => {
                    registration.update();
                }, 60 * 60 * 1000);
                
                // Escuchar actualizaciones
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    console.log('[PWA] Nueva versión encontrada');
                    
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            // Mostrar notificación de actualización
                            showUpdateNotification();
                        }
                    });
                });
            })
            .catch((error) => {
                console.error('[PWA] Error al registrar Service Worker:', error);
            });
    });
}

// Capturar evento beforeinstallprompt
window.addEventListener('beforeinstallprompt', (e) => {
    console.log('[PWA] beforeinstallprompt disparado');
    
    // Prevenir el prompt automático
    e.preventDefault();
    
    // Guardar el evento para usarlo después
    deferredPrompt = e;
    
    // Mostrar botón de instalación
    showInstallButton();
});

// Detectar cuando se instala la app
window.addEventListener('appinstalled', () => {
    console.log('[PWA] App instalada exitosamente');
    isInstalled = true;
    hideInstallButton();
    
    // Mostrar mensaje de éxito
    showToast('¡App instalada! Ahora puedes usarla desde tu pantalla de inicio 🎉', 'success');
    
    // Limpiar el prompt
    deferredPrompt = null;
});

// Función para mostrar botón de instalación
function showInstallButton() {
    // Crear botón flotante si no existe
    let installBtn = document.getElementById('pwa-install-btn');
    
    if (!installBtn && !isInstalled) {
        installBtn = document.createElement('button');
        installBtn.id = 'pwa-install-btn';
        installBtn.className = 'btn btn-primary position-fixed';
        installBtn.style.cssText = `
            bottom: 20px;
            right: 20px;
            z-index: 9999;
            border-radius: 50px;
            padding: 12px 24px;
            box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4);
            animation: pulse 2s infinite;
        `;
        installBtn.innerHTML = '<i class="bi bi-download"></i> Instalar App';
        
        installBtn.addEventListener('click', installPWA);
        
        document.body.appendChild(installBtn);
        
        // Agregar animación
        const style = document.createElement('style');
        style.textContent = `
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
        `;
        document.head.appendChild(style);
    }
}

// Función para ocultar botón de instalación
function hideInstallButton() {
    const installBtn = document.getElementById('pwa-install-btn');
    if (installBtn) {
        installBtn.style.display = 'none';
    }
}

// Función para instalar PWA
async function installPWA() {
    if (!deferredPrompt) {
        console.log('[PWA] No hay prompt disponible');
        return;
    }
    
    // Mostrar el prompt
    deferredPrompt.prompt();
    
    // Esperar la respuesta del usuario
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`[PWA] Usuario eligió: ${outcome}`);
    
    if (outcome === 'accepted') {
        console.log('[PWA] Usuario aceptó instalar');
    } else {
        console.log('[PWA] Usuario rechazó instalar');
    }
    
    // Limpiar el prompt
    deferredPrompt = null;
    hideInstallButton();
}

// Mostrar notificación de actualización
function showUpdateNotification() {
    const updateBanner = document.createElement('div');
    updateBanner.className = 'alert alert-info position-fixed';
    updateBanner.style.cssText = `
        top: 20px;
        left: 50%;
        transform: translateX(-50%);
        z-index: 10000;
        min-width: 300px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    `;
    updateBanner.innerHTML = `
        <div class="d-flex align-items-center justify-content-between">
            <span><i class="bi bi-arrow-clockwise"></i> Nueva versión disponible</span>
            <button class="btn btn-sm btn-primary ms-3" onclick="window.location.reload()">
                Actualizar
            </button>
        </div>
    `;
    
    document.body.appendChild(updateBanner);
    
    // Auto-remover después de 10 segundos
    setTimeout(() => {
        updateBanner.remove();
    }, 10000);
}

// Función auxiliar para mostrar toast
function showToast(message, type = 'info') {
    // Verificar si Bootstrap toast está disponible
    if (typeof bootstrap !== 'undefined' && bootstrap.Toast) {
        const toastContainer = document.getElementById('toast-container') || createToastContainer();
        
        const toastEl = document.createElement('div');
        toastEl.className = `toast align-items-center text-white bg-${type} border-0`;
        toastEl.setAttribute('role', 'alert');
        toastEl.innerHTML = `
            <div class="d-flex">
                <div class="toast-body">${message}</div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        `;
        
        toastContainer.appendChild(toastEl);
        const toast = new bootstrap.Toast(toastEl);
        toast.show();
        
        toastEl.addEventListener('hidden.bs.toast', () => {
            toastEl.remove();
        });
    } else {
        // Fallback: alert simple
        alert(message);
    }
}

// Crear contenedor de toasts
function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toast-container';
    container.className = 'toast-container position-fixed top-0 end-0 p-3';
    container.style.zIndex = '11000';
    document.body.appendChild(container);
    return container;
}

// Detectar modo standalone
function isRunningStandalone() {
    return window.matchMedia('(display-mode: standalone)').matches || 
           window.navigator.standalone === true;
}

// Exportar funciones
window.PWA = {
    install: installPWA,
    isInstalled: () => isInstalled,
    isStandalone: isRunningStandalone
};

console.log('[PWA] Script de instalación cargado');
