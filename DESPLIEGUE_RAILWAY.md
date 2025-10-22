# 🚂 GUÍA PARA DESPLEGAR EN RAILWAY

## 🎯 **¿QUÉ ES RAILWAY?**

Railway es una plataforma moderna de despliegue que permite alojar aplicaciones web de forma gratuita (con límites) o de pago. Es ideal para Django y soporta WebSockets.

---

## ✅ **ARCHIVOS CREADOS PARA RAILWAY:**

1. ✅ **`Procfile`** - Comandos de inicio
2. ✅ **`runtime.txt`** - Versión de Python
3. ✅ **`railway.json`** - Configuración de Railway
4. ✅ **`requirements.txt`** - Dependencias actualizadas
5. ✅ **`settings.py`** - Configurado para producción

---

## 🚀 **PASO 1: SUBIR A GITHUB (SI NO LO HICISTE)**

Railway necesita que tu código esté en GitHub:

```powershell
# Conectar con GitHub
git remote add origin https://github.com/TU_USUARIO/transporte_carga.git

# Cambiar a main
git branch -M main

# Agregar archivos nuevos
git add .

# Commit
git commit -m "🚀 Preparar para despliegue en Railway"

# Subir
git push -u origin main
```

---

## 📋 **PASO 2: CREAR CUENTA EN RAILWAY**

1. Ve a: **https://railway.app**
2. Click en **"Start a New Project"** o **"Login"**
3. **Inicia sesión con GitHub** (recomendado)
4. Autoriza a Railway para acceder a tus repositorios

---

## 🆕 **PASO 3: CREAR NUEVO PROYECTO**

### **Opción A: Desde Dashboard**

1. En Railway Dashboard, click **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Busca y selecciona **`transporte_carga`**
4. Click en **"Deploy Now"**

### **Opción B: Desde CLI (Opcional)**

```powershell
# Instalar Railway CLI
npm install -g @railway/cli

# O con Scoop
scoop install railway

# Login
railway login

# Iniciar proyecto
railway init

# Vincular repo
railway link

# Deploy
railway up
```

---

## 🗄️ **PASO 4: AGREGAR BASE DE DATOS POSTGRESQL**

Railway detectará que necesitas una base de datos:

1. En tu proyecto, click **"+ New"**
2. Selecciona **"Database"**
3. Elige **"Add PostgreSQL"**
4. Railway creará automáticamente la base de datos
5. Se generará la variable `DATABASE_URL`

---

## ⚙️ **PASO 5: CONFIGURAR VARIABLES DE ENTORNO**

En Railway, ve a tu servicio → **Variables**:

### **Variables Requeridas:**

```env
# Django
SECRET_KEY=tu-secret-key-super-segura-aqui-cambiala
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
DJANGO_SETTINGS_MODULE=core.settings

# Database (se crea automáticamente)
DATABASE_URL=postgresql://... (Railway lo genera)

# Channels (WebSockets)
REDIS_URL=redis://... (si usas Redis)

# Google Maps (opcional)
GOOGLE_MAPS_API_KEY=tu-api-key-aqui
```

### **Cómo agregar variables:**

1. Click en tu servicio
2. Ve a **"Variables"**
3. Click **"+ New Variable"**
4. Agrega cada variable con su valor
5. Click **"Add"**

---

## 🔑 **GENERAR SECRET_KEY SEGURA**

En tu terminal local:

```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Copia el resultado y úsalo como `SECRET_KEY` en Railway.

---

## 🔧 **PASO 6: CONFIGURAR SETTINGS PARA RAILWAY**

Railway ya tiene tu código, pero necesitas actualizar `settings.py`:

### **Actualizar DATABASES (ya está configurado):**

```python
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///db.sqlite3',
        conn_max_age=600
    )
}
```

### **Actualizar MIDDLEWARE (agregar WhiteNoise):**

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ← Agregar esto
    'django.contrib.sessions.middleware.SessionMiddleware',
    # ... resto del middleware
]
```

### **Configurar archivos estáticos:**

```python
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'cargas' / 'static']

# WhiteNoise
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📦 **PASO 7: ACTUALIZAR requirements.txt**

Asegúrate de que incluya:

```txt
Django==5.2
djangorestframework==3.16.0
channels==4.3.1
daphne==4.2.1
whitenoise==6.6.0
dj-database-url==3.0.1
psycopg2-binary==2.9.9
gunicorn==21.2.0
```

---

## 🚀 **PASO 8: HACER COMMIT Y PUSH**

```powershell
# Agregar cambios
git add .

# Commit
git commit -m "⚙️ Configurar para Railway con PostgreSQL"

# Push
git push
```

Railway detectará el push y **desplegará automáticamente**.

---

## 📊 **PASO 9: MONITOREAR EL DESPLIEGUE**

1. En Railway, ve a **"Deployments"**
2. Verás el progreso en tiempo real:
   - ✅ Building...
   - ✅ Running migrations...
   - ✅ Collecting static files...
   - ✅ Starting server...

3. Si hay errores, revisa los **logs**

---

## 🌐 **PASO 10: OBTENER URL PÚBLICA**

1. En Railway, ve a **"Settings"**
2. Sección **"Domains"**
3. Click **"Generate Domain"**
4. Railway generará una URL como:
   ```
   https://transporte-carga-production.up.railway.app
   ```

5. **Copia esta URL** y agrégala a `ALLOWED_HOSTS`:

```env
ALLOWED_HOSTS=transporte-carga-production.up.railway.app,*.railway.app
```

---

## 🗃️ **PASO 11: CREAR SUPERUSUARIO**

Desde Railway CLI o usando el shell:

### **Opción A: Railway CLI**

```powershell
railway run python manage.py createsuperuser
```

### **Opción B: Desde Railway Dashboard**

1. Ve a tu servicio
2. Click en **"Settings"**
3. Busca **"Service Variables"**
4. Agrega comando personalizado:
   ```
   python manage.py createsuperuser --noinput --username admin --email admin@ejemplo.com
   ```

---

## 🔍 **PASO 12: VERIFICAR DESPLIEGUE**

1. Abre tu URL de Railway
2. Deberías ver tu aplicación funcionando
3. Prueba:
   - ✅ Login: `https://tu-app.railway.app/login/`
   - ✅ Admin: `https://tu-app.railway.app/admin/`
   - ✅ Dashboard: `https://tu-app.railway.app/dashboard/`

---

## 🐛 **SOLUCIÓN DE PROBLEMAS**

### **Error: "Application failed to respond"**

**Causa:** El puerto no está configurado correctamente.

**Solución:** Verifica que `Procfile` use `$PORT`:
```
web: daphne -b 0.0.0.0 -p $PORT core.asgi:application
```

### **Error: "Static files not found"**

**Causa:** Archivos estáticos no se recolectaron.

**Solución:** Agrega a `Procfile`:
```
release: python manage.py collectstatic --noinput && python manage.py migrate --noinput
```

### **Error: "Database connection failed"**

**Causa:** PostgreSQL no está configurado.

**Solución:**
1. Verifica que agregaste PostgreSQL en Railway
2. Verifica que `DATABASE_URL` esté en variables
3. Instala `psycopg2-binary` en requirements.txt

### **Error: "SECRET_KEY not set"**

**Causa:** Falta variable de entorno.

**Solución:** Agrega `SECRET_KEY` en Variables de Railway.

### **WebSockets no funcionan**

**Causa:** Railway necesita configuración especial.

**Solución:** Usa Daphne (ya configurado en Procfile).

---

## 📊 **LOGS Y DEBUGGING**

### **Ver logs en tiempo real:**

```powershell
railway logs
```

### **Ver logs desde Dashboard:**

1. Ve a tu servicio
2. Click en **"Deployments"**
3. Click en el deployment activo
4. Verás los logs en tiempo real

---

## 💰 **COSTOS Y LÍMITES**

### **Plan Gratuito (Trial):**
- ✅ $5 de crédito gratis
- ✅ 500 horas de ejecución/mes
- ✅ 1 GB RAM
- ✅ 1 GB almacenamiento
- ⚠️ Requiere tarjeta de crédito (no se cobra)

### **Plan Hobby ($5/mes):**
- ✅ $5 de crédito/mes
- ✅ Ilimitado
- ✅ Mejor rendimiento

---

## 🔄 **ACTUALIZACIONES FUTURAS**

Cada vez que hagas cambios:

```powershell
# 1. Hacer cambios en el código

# 2. Commit
git add .
git commit -m "✨ Descripción del cambio"

# 3. Push
git push

# 4. Railway despliega automáticamente
```

---

## 🌐 **DOMINIO PERSONALIZADO (OPCIONAL)**

1. En Railway → **Settings** → **Domains**
2. Click **"Custom Domain"**
3. Agrega tu dominio: `www.tudominio.com`
4. Configura DNS en tu proveedor:
   ```
   CNAME www tu-app.up.railway.app
   ```

---

## 📋 **CHECKLIST DE DESPLIEGUE**

- [ ] Código subido a GitHub
- [ ] Proyecto creado en Railway
- [ ] PostgreSQL agregado
- [ ] Variables de entorno configuradas
- [ ] SECRET_KEY generada y agregada
- [ ] ALLOWED_HOSTS actualizado
- [ ] Despliegue exitoso
- [ ] URL pública generada
- [ ] Superusuario creado
- [ ] Login funciona
- [ ] Admin funciona
- [ ] Rastreo GPS funciona
- [ ] WebSockets funcionan

---

## 🎉 **¡LISTO!**

Tu aplicación ahora está en producción en:
```
https://tu-app.up.railway.app
```

**Características funcionando:**
- ✅ Django con PostgreSQL
- ✅ WebSockets (Daphne)
- ✅ Archivos estáticos (WhiteNoise)
- ✅ Rastreo GPS en tiempo real
- ✅ PWA instalable
- ✅ Multi-rol (Admin, Conductor, Cliente)

---

## 📞 **RECURSOS**

- **Railway Docs:** https://docs.railway.app/
- **Railway CLI:** https://docs.railway.app/develop/cli
- **Django on Railway:** https://docs.railway.app/guides/django
- **Soporte:** https://railway.app/help

---

## 🔧 **COMANDOS ÚTILES DE RAILWAY CLI**

```powershell
# Ver logs
railway logs

# Abrir shell
railway run python manage.py shell

# Ejecutar migraciones
railway run python manage.py migrate

# Crear superusuario
railway run python manage.py createsuperuser

# Abrir en navegador
railway open

# Ver variables
railway variables

# Vincular proyecto
railway link
```

---

**¡Tu aplicación está lista para el mundo!** 🚀🌍

**Comparte tu URL:**
- Con clientes
- En tu portafolio
- En tu CV
- En redes sociales

**¡Felicidades por desplegar tu proyecto!** 🎊
