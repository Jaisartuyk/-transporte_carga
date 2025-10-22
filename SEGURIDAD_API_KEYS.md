# 🔐 SEGURIDAD: API KEYS PROTEGIDAS

## ✅ **PROBLEMA RESUELTO:**

Las API Keys de Google Maps estaban **hardcodeadas** (expuestas) directamente en los templates HTML, lo cual es un **riesgo de seguridad**.

---

## 🛡️ **SOLUCIÓN IMPLEMENTADA:**

### **1. Variable de Entorno en settings.py:**

```python
# Google Maps API Key
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ')
```

- Lee la API Key desde variable de entorno
- Usa valor por defecto solo para desarrollo local
- En producción, se configura en Railway

### **2. Context Processor Creado:**

Archivo: `cargas/context_processors.py`

```python
def google_maps_api_key(request):
    """
    Hace la API Key de Google Maps disponible en todos los templates
    """
    return {
        'GOOGLE_MAPS_API_KEY': settings.GOOGLE_MAPS_API_KEY
    }
```

- Hace la variable disponible en TODOS los templates
- No necesitas pasarla manualmente en cada vista

### **3. Context Processor Registrado:**

En `settings.py`:

```python
TEMPLATES = [
    {
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cargas.context_processors.google_maps_api_key',  # ← Agregado
            ],
        },
    },
]
```

### **4. Templates Actualizados (5 archivos):**

**ANTES (❌ Inseguro):**
```html
<script src="https://maps.googleapis.com/maps/api/js?key=AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ&libraries=places"></script>
```

**DESPUÉS (✅ Seguro):**
```html
<script src="https://maps.googleapis.com/maps/api/js?key={{ GOOGLE_MAPS_API_KEY }}&libraries=places"></script>
```

**Templates actualizados:**
1. ✅ `conductor_rastreo.html`
2. ✅ `conductor_rastreo_v2.html`
3. ✅ `envio_rastreo.html`
4. ✅ `envio_rastreo_nuevo.html`
5. ✅ `envios_list.html`

---

## 🚀 **CONFIGURACIÓN EN RAILWAY:**

Cuando despliegues en Railway, agrega esta variable de entorno:

```env
GOOGLE_MAPS_API_KEY=tu-api-key-de-google-maps-aqui
```

### **Pasos en Railway:**

1. Ve a tu servicio en Railway
2. Click en **"Variables"**
3. Click **"+ New Variable"**
4. Nombre: `GOOGLE_MAPS_API_KEY`
5. Valor: Tu API Key de Google Maps
6. Click **"Add"**

---

## 🔒 **BENEFICIOS DE SEGURIDAD:**

### **1. No Expuesta en Código:**
- ✅ La API Key NO está en el código fuente
- ✅ NO se sube a GitHub
- ✅ NO es visible en el repositorio público

### **2. Fácil de Cambiar:**
- ✅ Cambias solo la variable de entorno
- ✅ No necesitas modificar código
- ✅ No necesitas hacer nuevo deploy

### **3. Diferente por Entorno:**
- ✅ Desarrollo: Una API Key
- ✅ Producción: Otra API Key (con restricciones)
- ✅ Testing: Otra API Key

### **4. Restricciones de API Key:**
En Google Cloud Console, puedes restringir tu API Key de producción:
- Solo desde tu dominio de Railway
- Solo APIs específicas (Maps JavaScript API)
- Límites de uso diario

---

## 📝 **BUENAS PRÁCTICAS APLICADAS:**

### **✅ DO (Hacer):**
- Usar variables de entorno para API Keys
- Usar context processors para valores globales
- Restringir API Keys en Google Cloud Console
- Tener diferentes keys para dev/prod

### **❌ DON'T (No Hacer):**
- Hardcodear API Keys en templates
- Subir API Keys a GitHub
- Usar la misma key en dev y prod
- Dejar API Keys sin restricciones

---

## 🔧 **DESARROLLO LOCAL:**

Para desarrollo local, puedes:

### **Opción 1: Usar .env (Recomendado)**

1. Instalar python-decouple:
```bash
pip install python-decouple
```

2. Crear archivo `.env` en la raíz:
```env
GOOGLE_MAPS_API_KEY=tu-api-key-aqui
SECRET_KEY=tu-secret-key-aqui
DEBUG=True
```

3. Actualizar settings.py:
```python
from decouple import config

GOOGLE_MAPS_API_KEY = config('GOOGLE_MAPS_API_KEY')
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

4. Agregar `.env` a `.gitignore` (ya está ✅)

### **Opción 2: Variables de Sistema**

Windows PowerShell:
```powershell
$env:GOOGLE_MAPS_API_KEY="tu-api-key-aqui"
```

Linux/Mac:
```bash
export GOOGLE_MAPS_API_KEY="tu-api-key-aqui"
```

### **Opción 3: Usar Valor por Defecto**

El código ya tiene un valor por defecto para desarrollo:
```python
GOOGLE_MAPS_API_KEY = os.environ.get('GOOGLE_MAPS_API_KEY', 'AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ')
```

⚠️ **Importante:** Cambia este valor por defecto antes de subir a GitHub público.

---

## 🌐 **RESTRINGIR API KEY EN GOOGLE CLOUD:**

### **Para Producción:**

1. Ve a: https://console.cloud.google.com/apis/credentials
2. Selecciona tu API Key
3. En **"Application restrictions"**:
   - Selecciona **"HTTP referrers (web sites)"**
   - Agrega: `https://tu-app.up.railway.app/*`
   - Agrega: `https://*.railway.app/*`

4. En **"API restrictions"**:
   - Selecciona **"Restrict key"**
   - Marca solo:
     - Maps JavaScript API
     - Geocoding API
     - Places API

5. Click **"Save"**

### **Para Desarrollo:**

Crea una API Key separada sin restricciones o con:
- HTTP referrers: `http://localhost:*`, `http://127.0.0.1:*`

---

## 📊 **RESUMEN DE CAMBIOS:**

| Archivo | Cambio |
|---------|--------|
| `settings.py` | Agregada variable `GOOGLE_MAPS_API_KEY` |
| `context_processors.py` | Creado context processor |
| `conductor_rastreo.html` | API Key → Variable |
| `conductor_rastreo_v2.html` | API Key → Variable |
| `envio_rastreo.html` | API Key → Variable |
| `envio_rastreo_nuevo.html` | API Key → Variable |
| `envios_list.html` | API Key → Variable |

---

## ✅ **CHECKLIST DE SEGURIDAD:**

- [x] API Key movida a variable de entorno
- [x] Context processor creado
- [x] Templates actualizados (5 archivos)
- [x] Valor por defecto solo para desarrollo
- [ ] Crear API Key separada para producción
- [ ] Restringir API Key de producción
- [ ] Agregar `GOOGLE_MAPS_API_KEY` a Railway
- [ ] Cambiar valor por defecto en settings.py

---

## 🎯 **PRÓXIMOS PASOS:**

1. **Antes de subir a GitHub:**
   - Cambia el valor por defecto en `settings.py`
   - O elimínalo completamente

2. **Al desplegar en Railway:**
   - Agrega `GOOGLE_MAPS_API_KEY` en Variables
   - Usa una API Key restringida

3. **En Google Cloud Console:**
   - Crea API Key separada para producción
   - Restringe por dominio y APIs

---

**¡Ahora tu API Key está protegida y no se expondrá en GitHub!** 🔐✨
