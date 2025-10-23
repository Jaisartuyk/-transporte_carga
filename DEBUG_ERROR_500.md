# 🐛 DEBUG: ERROR 500 PERSISTENTE

## 🔍 **VERIFICAR SI RAILWAY DESPLEGÓ EL CÓDIGO NUEVO:**

### **PASO 1: Ver Deployments en Railway Dashboard**

1. Ve a Railway Dashboard: https://railway.app
2. Click en tu proyecto
3. Click en tu servicio `-transporte_carga`
4. Ve a la pestaña **"Deployments"**
5. Verifica:
   - ¿Cuál es el commit más reciente?
   - ¿Dice `c230b6c` o posterior?
   - Si NO, Railway no ha desplegado el nuevo código

### **PASO 2: Ver el Traceback Completo del Error**

1. En Railway Dashboard → Tu servicio
2. Ve a **"Deployments"**
3. Click en el deployment activo (running)
4. Busca los logs del error 500
5. **Comparte el traceback completo aquí**

Deberías ver algo como:
```
Traceback (most recent call last):
  File "/app/cargas/views.py", line XXX
  ...
```

---

## 🔄 **FORZAR RE-DEPLOY COMPLETO:**

Si Railway no detectó el cambio:

```powershell
# Opción 1: Forzar con CLI
railway up --detach

# Opción 2: Desde Dashboard
# Deployments → "..." → "Redeploy"
```

---

## 🎯 **VERIFICACIÓN ALTERNATIVA:**

Podemos verificar si el problema es el código o los datos:

### **Probar con otra vista similar:**

Ve a alguna otra vista que funcione para confirmar que Railway está corriendo.

### **Acceder al shell de Railway:**

```powershell
railway run python manage.py shell
```

Luego ejecuta:
```python
from cargas.models import Envio, EventoEnvio

# Ver si hay envíos en ruta
envios = Envio.objects.filter(estado='en_ruta')
print(f"Envíos en ruta: {envios.count()}")

# Ver si hay eventos con ubicación
eventos = EventoEnvio.objects.filter(
    latitud__isnull=False, 
    longitud__isnull=False
)
print(f"Eventos con ubicación: {eventos.count()}")
```

---

## 🚨 **POSIBLES CAUSAS DEL ERROR:**

### **1. Railway NO desplegó el código nuevo** (más probable)
- Solución: Forzar redeploy

### **2. Falta importar EventoEnvio en views.py**
Verificar que en `views.py` esté:
```python
from .models import Usuario, Vehiculo, Envio, EventoEnvio, Alerta, Sensor
```

### **3. El template tiene un error**
Ver el template `panel_rastreo_general.html`

### **4. No hay permisos**
Asegúrate de estar logueado como admin

---

## 📝 **ACCIÓN INMEDIATA:**

**Por favor, ve a Railway Dashboard y comparte:**

1. ¿Qué commit está desplegado actualmente?
2. El traceback completo del error 500
3. La hora del último deployment

Con esa información puedo diagnosticar exactamente qué está pasando.

---

## 🔧 **ALTERNATIVA: DESACTIVAR DEBUG=False TEMPORALMENTE**

Para ver el error completo en el navegador:

1. Railway Dashboard → Variables
2. Cambia `DEBUG=False` a `DEBUG=True`
3. Railway re-desplegará
4. Recarga `/panel/rastreo/`
5. Verás el traceback completo en el navegador

**IMPORTANTE:** Vuelve a poner `DEBUG=False` después de ver el error.

---

**¿Puedes compartir el traceback del error desde Railway?** 🔍
