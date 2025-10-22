# 📤 GUÍA PARA SUBIR A GITHUB

## 🎯 Pasos para Subir tu Proyecto a GitHub

---

## 📋 **REQUISITOS PREVIOS:**

1. ✅ Tener Git instalado
2. ✅ Tener cuenta en GitHub
3. ✅ Proyecto listo para subir

---

## 🔧 **PASO 1: VERIFICAR GIT**

Abre PowerShell en la carpeta del proyecto y verifica que Git esté instalado:

```powershell
git --version
```

Si no está instalado, descárgalo de: https://git-scm.com/download/win

---

## 🆕 **PASO 2: CREAR REPOSITORIO EN GITHUB**

1. Ve a: https://github.com
2. Inicia sesión
3. Click en el botón **"+"** (arriba derecha)
4. Selecciona **"New repository"**
5. Llena los datos:
   - **Repository name:** `transporte_carga` o `cargotrack-pro`
   - **Description:** "Sistema de gestión de transporte de carga con GPS en tiempo real"
   - **Public** o **Private** (tu elección)
   - ❌ NO marques "Initialize with README" (ya tienes uno)
   - ❌ NO agregues .gitignore (ya tienes uno)
6. Click en **"Create repository"**

---

## 💻 **PASO 3: CONFIGURAR GIT LOCAL**

Abre PowerShell en la carpeta del proyecto:

```powershell
cd "c:\Users\H P\OneDrive\Escritorio\transporte_carga"
```

### Configurar tu nombre y email (solo la primera vez):

```powershell
git config --global user.name "Tu Nombre"
git config --global user.email "tu-email@ejemplo.com"
```

---

## 📦 **PASO 4: INICIALIZAR REPOSITORIO**

```powershell
# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Verificar qué archivos se agregarán
git status
```

Deberías ver una lista de archivos en verde. Los archivos en `.gitignore` NO aparecerán.

---

## 💾 **PASO 5: HACER PRIMER COMMIT**

```powershell
git commit -m "🚀 Initial commit: CargoTrack Pro - Sistema completo de gestión de transporte"
```

---

## 🔗 **PASO 6: CONECTAR CON GITHUB**

Reemplaza `TU_USUARIO` con tu nombre de usuario de GitHub:

```powershell
git remote add origin https://github.com/TU_USUARIO/transporte_carga.git
```

Ejemplo:
```powershell
git remote add origin https://github.com/juanperez/transporte_carga.git
```

### Verificar que se agregó correctamente:

```powershell
git remote -v
```

---

## 📤 **PASO 7: SUBIR A GITHUB**

```powershell
# Cambiar a rama main
git branch -M main

# Subir archivos
git push -u origin main
```

### Si te pide autenticación:

**Opción 1: Token de Acceso Personal (Recomendado)**

1. Ve a GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Click "Generate new token (classic)"
3. Selecciona permisos: `repo` (todos)
4. Copia el token generado
5. Úsalo como contraseña cuando Git lo pida

**Opción 2: GitHub CLI**

```powershell
# Instalar GitHub CLI
winget install --id GitHub.cli

# Autenticarse
gh auth login
```

---

## ✅ **PASO 8: VERIFICAR EN GITHUB**

1. Ve a: `https://github.com/TU_USUARIO/transporte_carga`
2. Deberías ver todos tus archivos
3. El README.md se mostrará automáticamente

---

## 🔄 **COMANDOS PARA ACTUALIZACIONES FUTURAS**

Cuando hagas cambios en el proyecto:

```powershell
# Ver archivos modificados
git status

# Agregar archivos modificados
git add .

# O agregar archivos específicos
git add archivo.py

# Hacer commit con mensaje descriptivo
git commit -m "✨ Descripción de los cambios"

# Subir cambios
git push
```

---

## 📝 **MENSAJES DE COMMIT RECOMENDADOS**

Usa emojis para mejor legibilidad:

```
🚀 Initial commit
✨ Agregar nueva funcionalidad
🐛 Corregir bug
📝 Actualizar documentación
🎨 Mejorar diseño/UI
♻️ Refactorizar código
🔧 Actualizar configuración
⚡ Mejorar rendimiento
🔒 Mejorar seguridad
```

Ejemplos:
```powershell
git commit -m "✨ Agregar rastreo en segundo plano"
git commit -m "🐛 Corregir error en login"
git commit -m "📝 Actualizar README con instrucciones"
```

---

## 🌿 **TRABAJAR CON RAMAS (OPCIONAL)**

Para nuevas funcionalidades:

```powershell
# Crear nueva rama
git checkout -b feature/nueva-funcionalidad

# Hacer cambios y commits
git add .
git commit -m "✨ Agregar nueva funcionalidad"

# Subir rama
git push -u origin feature/nueva-funcionalidad

# Volver a main
git checkout main

# Fusionar rama
git merge feature/nueva-funcionalidad
```

---

## 🔐 **ARCHIVOS QUE NO SE SUBIRÁN**

Gracias al `.gitignore`, estos archivos NO se subirán:

- ❌ `db.sqlite3` (base de datos)
- ❌ `*.pyc` (archivos compilados)
- ❌ `__pycache__/` (caché de Python)
- ❌ `venv/` (entorno virtual)
- ❌ `.env` (variables de entorno)
- ❌ `*.log` (archivos de log)
- ❌ `media/` (archivos subidos)

**Esto es correcto** - no quieres subir estos archivos.

---

## 📊 **ESTRUCTURA QUE SE SUBIRÁ**

```
✅ cargas/              (código de la app)
✅ core/                (configuración)
✅ static/              (archivos estáticos)
✅ templates/           (plantillas HTML)
✅ manage.py
✅ requirements.txt
✅ README.md
✅ .gitignore
✅ *.md                 (documentación)
❌ db.sqlite3          (NO se sube)
❌ venv/               (NO se sube)
❌ __pycache__/        (NO se sube)
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### Error: "fatal: not a git repository"
```powershell
git init
```

### Error: "remote origin already exists"
```powershell
git remote remove origin
git remote add origin https://github.com/TU_USUARIO/transporte_carga.git
```

### Error: "failed to push some refs"
```powershell
# Traer cambios del remoto primero
git pull origin main --allow-unrelated-histories

# Luego subir
git push -u origin main
```

### Olvidaste agregar archivo a .gitignore
```powershell
# Remover del staging
git rm --cached archivo.txt

# Agregar a .gitignore
echo "archivo.txt" >> .gitignore

# Commit
git add .gitignore
git commit -m "🔧 Actualizar .gitignore"
git push
```

---

## 🎨 **PERSONALIZAR README**

Antes de subir, edita `README.md` y reemplaza:

- `TU_USUARIO` → Tu usuario de GitHub
- `tu-email@ejemplo.com` → Tu email
- `Tu Nombre` → Tu nombre real
- Agrega capturas de pantalla si quieres

---

## 📸 **AGREGAR CAPTURAS DE PANTALLA (OPCIONAL)**

1. Crea carpeta `screenshots/` en el proyecto
2. Agrega imágenes: `dashboard.png`, `rastreo.png`, etc.
3. Referencia en README.md:

```markdown
## 📸 Capturas de Pantalla

### Dashboard Admin
![Dashboard](screenshots/dashboard.png)

### Rastreo GPS
![Rastreo](screenshots/rastreo.png)
```

---

## 🌟 **HACER TU REPO DESTACADO**

1. Agrega topics en GitHub:
   - `django`
   - `gps-tracking`
   - `pwa`
   - `websockets`
   - `logistics`
   - `python`

2. Agrega descripción corta

3. Agrega URL del demo (si tienes)

4. Marca como "Featured" en tu perfil

---

## 📋 **CHECKLIST FINAL**

Antes de subir, verifica:

- [ ] `.gitignore` creado
- [ ] `README.md` personalizado
- [ ] `requirements.txt` generado
- [ ] Archivos sensibles NO incluidos
- [ ] Código comentado y limpio
- [ ] Documentación completa
- [ ] API Keys removidas o en .env

---

## 🎉 **¡LISTO!**

Tu proyecto ahora está en GitHub y otros pueden:
- ⭐ Darle estrella
- 🍴 Hacer fork
- 👀 Ver el código
- 📥 Clonarlo
- 🤝 Contribuir

---

## 📞 **AYUDA ADICIONAL**

- Documentación Git: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/
- GitHub CLI: https://cli.github.com/

---

**¡Felicidades por subir tu proyecto a GitHub!** 🎊
