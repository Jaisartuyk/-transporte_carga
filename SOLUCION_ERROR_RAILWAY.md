# 🔧 SOLUCIÓN: Error de Build en Railway

## ❌ **ERROR:**
```
Deployment failed during the build process
Error creating build plan with Railpack
```

## ✅ **SOLUCIÓN APLICADA:**

### **1. Creado `nixpacks.toml`**

Railway usa Nixpacks para detectar el tipo de proyecto. He creado este archivo para especificar la configuración de Python/Django:

```toml
[phases.setup]
nixPkgs = ["python311", "postgresql"]

[phases.install]
cmds = ["pip install -r requirements.txt"]

[phases.build]
cmds = ["python manage.py collectstatic --noinput"]

[start]
cmd = "daphne -b 0.0.0.0 -p $PORT core.asgi:application"
```

### **2. Corregido `.gitignore`**

El `.gitignore` estaba bloqueando `requirements.txt` y `runtime.txt`, archivos necesarios para Railway:

```gitignore
*.txt
!requirements.txt  # ← Permitir
!runtime.txt       # ← Permitir
```

### **3. Commit realizado**

```bash
✅ Commit: "🔧 Agregar nixpacks.toml para Railway y corregir .gitignore"
```

---

## 🚀 **PRÓXIMOS PASOS:**

### **PASO 1: Push a GitHub**

Si aún no has conectado con GitHub:

```powershell
# Conectar (reemplaza TU_USUARIO)
git remote add origin https://github.com/TU_USUARIO/transporte_carga.git

# Push
git push -u origin main
```

Si ya está conectado:

```powershell
# Solo push
git push
```

### **PASO 2: Railway Re-desplegará Automáticamente**

Railway detectará el push y:
1. ✅ Leerá `nixpacks.toml`
2. ✅ Instalará Python 3.11
3. ✅ Instalará dependencias de `requirements.txt`
4. ✅ Ejecutará `collectstatic`
5. ✅ Iniciará Daphne

### **PASO 3: Monitorear el Despliegue**

En Railway:
1. Ve a **"Deployments"**
2. Verás el nuevo deployment en progreso
3. Deberías ver:
   ```
   ✅ Building...
   ✅ Installing dependencies...
   ✅ Collecting static files...
   ✅ Starting server...
   ✅ Deployed successfully
   ```

---

## 📊 **ARCHIVOS IMPORTANTES PARA RAILWAY:**

Railway necesita estos archivos para desplegar:

| Archivo | Propósito | Estado |
|---------|-----------|--------|
| `requirements.txt` | Dependencias Python | ✅ Incluido |
| `runtime.txt` | Versión de Python | ✅ Incluido |
| `Procfile` | Comando de inicio | ✅ Incluido |
| `nixpacks.toml` | Configuración build | ✅ Creado |
| `railway.json` | Config Railway | ✅ Incluido |

---

## 🔍 **VERIFICAR QUE ARCHIVOS ESTÁN EN GIT:**

```powershell
# Ver archivos trackeados
git ls-files | findstr -i "requirements runtime procfile nixpacks railway"
```

Deberías ver:
```
Procfile
nixpacks.toml
railway.json
requirements.txt
runtime.txt
```

---

## 🐛 **SI EL ERROR PERSISTE:**

### **Opción 1: Verificar Logs**

En Railway → Deployments → Click en el deployment fallido → Ver logs completos

### **Opción 2: Forzar Re-deploy**

En Railway:
1. Ve a **"Deployments"**
2. Click en **"..."** del último deployment
3. Selecciona **"Redeploy"**

### **Opción 3: Verificar Variables**

Asegúrate de tener todas las variables:
- ✅ `SECRET_KEY`
- ✅ `DEBUG=False`
- ✅ `ALLOWED_HOSTS`
- ✅ `GOOGLE_MAPS_API_KEY`
- ✅ `DATABASE_URL` (auto-generada)

### **Opción 4: Cambiar a Dockerfile (Plan B)**

Si Nixpacks sigue fallando, puedo crear un `Dockerfile`:

```dockerfile
FROM python:3.11
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput
CMD daphne -b 0.0.0.0 -p $PORT core.asgi:application
```

---

## 📝 **COMANDOS RESUMEN:**

```powershell
# 1. Push a GitHub (si no lo hiciste)
git push

# 2. Ver logs de Railway (con CLI)
railway logs

# 3. Forzar re-deploy (con CLI)
railway up --detach
```

---

## ✅ **CHECKLIST:**

- [x] `nixpacks.toml` creado
- [x] `.gitignore` corregido
- [x] Commit realizado
- [ ] Push a GitHub
- [ ] Railway re-desplegando
- [ ] Deployment exitoso

---

## 🎯 **RESULTADO ESPERADO:**

Después del push, Railway debería:

```
✅ Detected Python project
✅ Using Python 3.11
✅ Installing dependencies...
✅ Collecting static files...
✅ Starting Daphne server...
✅ Deployment successful!
```

---

## 💡 **NOTA IMPORTANTE:**

El error "Error creating build plan" generalmente ocurre cuando:
1. ❌ Railway no detecta el lenguaje/framework
2. ❌ Faltan archivos de configuración
3. ❌ `requirements.txt` no está en el repo

**Solución:** `nixpacks.toml` le dice explícitamente a Railway cómo construir tu proyecto.

---

**¡Haz push y Railway debería desplegar correctamente!** 🚀
