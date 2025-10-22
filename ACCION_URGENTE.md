# ⚠️ ACCIÓN URGENTE: LIMPIAR CACHÉ DE RAILWAY

## 🔴 **PROBLEMA:**

Railway está usando una imagen Docker MUY antigua y no está detectando los cambios en `start.sh`.

El error `invalid int value: '$PORT'` indica que está ejecutando un comando antiguo, probablemente del `Procfile` que tenía un error.

---

## ✅ **LO QUE HICE:**

1. ✅ Eliminé `Procfile` para forzar que use solo Dockerfile
2. ✅ Push completado
3. ⏳ Railway re-desplegando...

---

## 🚨 **ACCIÓN REQUERIDA:**

Railway tiene caché muy agresivo. Necesitas **FORZAR UN REBUILD COMPLETO**:

### **OPCIÓN 1: Desde Railway Dashboard (RECOMENDADO)**

1. Ve a Railway Dashboard
2. Click en tu servicio
3. Ve a **"Settings"** (no Deployments)
4. Busca la sección **"Danger Zone"** o **"Service"**
5. Click en **"Remove Service"** o **"Delete Service"**
6. **CONFIRMA** (no te preocupes, no perderás la base de datos)
7. Crea un **NUEVO servicio**:
   - Click **"+ New"** → **"GitHub Repo"**
   - Selecciona `transporte_carga`
   - Railway construirá desde cero

### **OPCIÓN 2: Forzar Rebuild con CLI**

```powershell
# Instalar Railway CLI
npm install -g @railway/cli

# Login
railway login

# Vincular proyecto
railway link

# Forzar rebuild completo
railway up --detach
```

### **OPCIÓN 3: Crear Nuevo Deployment**

1. Ve a **"Deployments"**
2. Click en **"New Deployment"**
3. Selecciona **"Deploy from GitHub"**
4. Asegúrate que use la rama `main`

---

## 🔍 **VERIFICAR SETTINGS:**

Antes de re-desplegar, verifica en **Settings**:

### **1. Builder:**
- Debería decir: **"Dockerfile"** o **"Docker"**
- Si dice "Nixpacks" o "Buildpack", cámbialo a "Dockerfile"

### **2. Start Command:**
- Debería estar **VACÍO**
- Si tiene algo, bórralo (el Dockerfile tiene el CMD)

### **3. Root Directory:**
- Debería estar **VACÍO** o **"/"**

---

## 📊 **LO QUE DEBERÍA PASAR:**

Después del rebuild completo, deberías ver:

```
✅ Cloning repository from GitHub...
✅ Detected Dockerfile
✅ Building Docker image...
✅ FROM python:3.11-slim
✅ COPY start.sh /app/start.sh
✅ RUN chmod +x /app/start.sh
✅ CMD ["/app/start.sh"]
✅ Build successful
✅ Starting container...
✅ Starting Daphne server on port 8080...
✅ Listening on 0.0.0.0:8080
✅ Deployment successful!
```

---

## 🎯 **ALTERNATIVA: CAMBIAR A GUNICORN**

Si Railway sigue teniendo problemas con Daphne, podemos cambiar a Gunicorn:

### **Actualizar start.sh:**

```bash
#!/bin/bash
echo "Starting Gunicorn with Uvicorn worker on port 8080..."
exec gunicorn core.asgi:application \
    -k uvicorn.workers.UvicornWorker \
    -b 0.0.0.0:8080 \
    --workers 2 \
    --timeout 120
```

**Ventajas de Gunicorn:**
- Más estable en Railway
- Soporta WebSockets con Uvicorn worker
- Menos problemas de configuración

---

## 📝 **VARIABLES A VERIFICAR:**

Asegúrate que estas variables estén configuradas:

```
✅ SECRET_KEY=alsv3$-z6^v+a&8uzzj95c$l5ykc*6^&^*(jf5n%@pp(ou1%lf
✅ DEBUG=False
✅ ALLOWED_HOSTS=transportecarga-production.up.railway.app,*.railway.app
✅ GOOGLE_MAPS_API_KEY=AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ
✅ DJANGO_SETTINGS_MODULE=core.settings
✅ DATABASE_URL=(auto-generada)
```

**NO agregues:**
- ❌ PORT (Railway la genera automáticamente)

---

## 🔧 **SI QUIERES PROBAR GUNICORN:**

Dime y actualizo `start.sh` para usar Gunicorn en lugar de Daphne.

Gunicorn es más confiable en Railway y soporta WebSockets con el worker de Uvicorn.

---

## ✅ **CHECKLIST:**

- [ ] Eliminar servicio actual en Railway
- [ ] Crear nuevo servicio desde GitHub
- [ ] Verificar que use Dockerfile
- [ ] Verificar variables de entorno
- [ ] Esperar build completo
- [ ] Probar app en URL
- [ ] Crear superusuario
- [ ] Probar funcionalidades

---

## 🆘 **RECOMENDACIÓN:**

**OPCIÓN MÁS RÁPIDA:**

1. **Elimina el servicio actual** en Railway
2. **Crea uno nuevo** desde GitHub
3. **Agrega PostgreSQL** de nuevo
4. **Configura variables** de entorno
5. **Espera el build**

Esto garantiza que Railway construya desde cero sin caché.

---

## 🎯 **PRÓXIMOS PASOS:**

1. **Decide:** ¿Eliminar servicio y crear nuevo? o ¿Probar Gunicorn?
2. **Ejecuta** la acción elegida
3. **Monitorea** el build
4. **Prueba** la app

---

**Railway está siendo muy problemático con el caché. La solución más confiable es crear un servicio nuevo desde cero.** 🔄

**¿Quieres que actualice start.sh para usar Gunicorn en lugar de Daphne?** 🤔
