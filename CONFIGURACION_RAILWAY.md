# ✅ CONFIGURACIÓN RAILWAY - ESTADO ACTUAL

## 🎉 **¡YA TIENES RAILWAY CONFIGURADO!**

Veo que ya creaste el proyecto en Railway y agregaste PostgreSQL. ¡Excelente!

---

## 📊 **VARIABLES QUE YA TIENES:**

### **✅ Generadas Automáticamente por Railway:**

```env
DATABASE_URL=postgresql://postgres:LAKljzeqdDsbtUWMAWFhNCdhehjCJFIa@postgres.railway.internal:5432/railway

DATABASE_PUBLIC_URL=postgresql://postgres:LAKljzeqdDsbtUWMAWFhNCdhehjCJFIa@shortline.proxy.rlwy.net:39097/railway
```

**Estas variables se crearon automáticamente cuando agregaste PostgreSQL.**
- ✅ `DATABASE_URL` - Usada por Django (interna)
- ✅ `DATABASE_PUBLIC_URL` - Para conexiones externas

---

## ⚙️ **VARIABLES QUE NECESITAS AGREGAR:**

Ahora agrega estas variables manualmente en Railway:

### **1. SECRET_KEY** (Django)
```env
SECRET_KEY=alsv3$-z6^v+a&8uzzj95c$l5ykc*6^&^*(jf5n%@pp(ou1%lf
```
**Descripción:** Clave secreta de Django (la que generaste)

### **2. DEBUG**
```env
DEBUG=False
```
**Descripción:** Modo producción (False = producción)

### **3. ALLOWED_HOSTS**
```env
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
```
**Descripción:** Dominios permitidos para acceder a tu app

### **4. GOOGLE_MAPS_API_KEY**
```env
GOOGLE_MAPS_API_KEY=AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ
```
**Descripción:** API Key de Google Maps

### **5. DJANGO_SETTINGS_MODULE** (Opcional)
```env
DJANGO_SETTINGS_MODULE=core.settings
```
**Descripción:** Módulo de configuración de Django

---

## 📝 **CÓMO AGREGAR LAS VARIABLES:**

1. En Railway, ve a tu servicio
2. Click en **"Variables"** (pestaña superior)
3. Click en **"+ New Variable"**
4. Copia y pega cada variable:
   - **Variable name:** `SECRET_KEY`
   - **Value:** `alsv3$-z6^v+a&8uzzj95c$l5ykc*6^&^*(jf5n%@pp(ou1%lf`
5. Click **"Add"**
6. Repite para cada variable de arriba

---

## 🔍 **VERIFICAR VARIABLES:**

Deberías tener en total **7 variables**:

```
✅ DATABASE_URL (auto-generada)
✅ DATABASE_PUBLIC_URL (auto-generada)
⏳ SECRET_KEY (agregar manualmente)
⏳ DEBUG (agregar manualmente)
⏳ ALLOWED_HOSTS (agregar manualmente)
⏳ GOOGLE_MAPS_API_KEY (agregar manualmente)
⏳ DJANGO_SETTINGS_MODULE (opcional)
```

---

## 🌐 **GENERAR DOMINIO:**

Después de agregar las variables:

1. Ve a **"Settings"** (pestaña)
2. Busca **"Domains"**
3. Click **"Generate Domain"**
4. Railway generará una URL como:
   ```
   https://transporte-carga-production.up.railway.app
   ```
5. **Copia esta URL** y actualiza `ALLOWED_HOSTS`:
   ```env
   ALLOWED_HOSTS=transporte-carga-production.up.railway.app,*.railway.app,*.up.railway.app
   ```

---

## 🚀 **DESPLIEGUE:**

Railway desplegará automáticamente cuando:
- ✅ Agregues las variables
- ✅ Hagas push a GitHub

**El despliegue incluirá:**
1. Instalar dependencias (`requirements.txt`)
2. Ejecutar migraciones (`python manage.py migrate`)
3. Recolectar archivos estáticos (`python manage.py collectstatic`)
4. Iniciar servidor Daphne

---

## 📊 **MONITOREAR DESPLIEGUE:**

1. Ve a **"Deployments"** (pestaña)
2. Verás el progreso en tiempo real:
   ```
   ✅ Building...
   ✅ Installing dependencies...
   ✅ Running migrations...
   ✅ Collecting static files...
   ✅ Starting server...
   ✅ Deployed successfully
   ```

3. Si hay errores, revisa los **logs**:
   - Click en el deployment
   - Verás los logs completos

---

## 👤 **CREAR SUPERUSUARIO:**

Una vez desplegado exitosamente:

### **Opción 1: Railway CLI**
```powershell
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Vincular proyecto (selecciona tu proyecto)
railway link

# Crear superusuario
railway run python manage.py createsuperuser
```

### **Opción 2: Desde Railway Dashboard**
1. Ve a tu servicio
2. Click en **"..."** (menú)
3. Selecciona **"Shell"**
4. Ejecuta:
   ```bash
   python manage.py createsuperuser
   ```

---

## ✅ **VERIFICAR QUE FUNCIONA:**

Una vez desplegado, abre tu URL de Railway:

```
https://tu-app.up.railway.app
```

**Prueba:**
1. **Login:** `https://tu-app.up.railway.app/login/`
2. **Admin:** `https://tu-app.up.railway.app/admin/`
3. **Dashboard:** `https://tu-app.up.railway.app/dashboard/`

---

## 🐛 **SOLUCIÓN DE PROBLEMAS:**

### **Error: "Application failed to respond"**
**Solución:** Verifica que todas las variables estén agregadas correctamente.

### **Error: "Static files not found"**
**Solución:** Railway ejecuta `collectstatic` automáticamente. Verifica los logs.

### **Error: "Database connection failed"**
**Solución:** Verifica que `DATABASE_URL` exista (debe estar auto-generada).

### **WebSockets no funcionan**
**Solución:** Daphne ya está configurado en `Procfile`. Debería funcionar automáticamente.

---

## 📋 **CHECKLIST:**

- [x] Proyecto creado en Railway
- [x] PostgreSQL agregado
- [x] `DATABASE_URL` generada automáticamente
- [ ] `SECRET_KEY` agregada
- [ ] `DEBUG` agregada
- [ ] `ALLOWED_HOSTS` agregada
- [ ] `GOOGLE_MAPS_API_KEY` agregada
- [ ] Dominio generado
- [ ] Despliegue exitoso
- [ ] Superusuario creado
- [ ] App funcionando

---

## 🎯 **PRÓXIMOS PASOS:**

1. **Agregar las 4 variables faltantes** (arriba)
2. **Generar dominio** en Settings → Domains
3. **Esperar despliegue** (automático)
4. **Crear superusuario** con Railway CLI
5. **Probar la app** en la URL generada

---

## 💡 **TIPS:**

### **Ver logs en tiempo real:**
```powershell
railway logs
```

### **Ejecutar comandos:**
```powershell
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py shell
```

### **Abrir app en navegador:**
```powershell
railway open
```

---

## 🎉 **¡CASI LISTO!**

Solo falta:
1. ✅ Agregar 4 variables
2. ✅ Generar dominio
3. ✅ Crear superusuario

**¡Tu app estará en producción en 5 minutos!** 🚀

---

**Variables a copiar y pegar:**

```
SECRET_KEY=alsv3$-z6^v+a&8uzzj95c$l5ykc*6^&^*(jf5n%@pp(ou1%lf
DEBUG=False
ALLOWED_HOSTS=*.railway.app,*.up.railway.app
GOOGLE_MAPS_API_KEY=AIzaSyBWy5uwBhRtafOG-EltQfe10KBp2R7eFTQ
```

**¡Adelante!** 💪
