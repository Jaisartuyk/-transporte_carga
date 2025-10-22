# 👤 MANUAL DEL CLIENTE - CargoTrack Pro

## 🎯 **¿QUÉ ES UN CLIENTE?**

El **Cliente** es el usuario que solicita envíos de carga. Es la persona o empresa que necesita transportar mercancía de un lugar a otro.

---

## 🔐 **ACCESO AL SISTEMA:**

### **1. Iniciar Sesión:**
1. Ir a: `http://127.0.0.1:8000/login/`
2. Ingresar usuario y contraseña
3. Click en "Iniciar Sesión"
4. Automáticamente redirige a **Dashboard Cliente**

### **2. Cerrar Sesión:**
- Click en el botón rojo de "Salir" en el navbar
- O click en "Cerrar Sesión" en el menú lateral

---

## 📱 **MENÚ DEL CLIENTE:**

El cliente ve un menú **simplificado** con solo lo que necesita:

```
┌─────────────────────────────┐
│ 📊 Principal                │
│  └─ Dashboard               │
│                             │
│ 📦 Gestión                  │
│  ├─ Mis Envíos              │
│  └─ Mis Alertas             │
│                             │
│ ⚙️ Sistema                  │
│  └─ Cerrar Sesión           │
└─────────────────────────────┘
```

**NO VE:**
- ❌ Vehículos
- ❌ Conductores
- ❌ Rastreo GPS (panel conductor)
- ❌ Administración

---

## 🏠 **DASHBOARD CLIENTE:**

### **Vista Principal:**
Al iniciar sesión, el cliente ve su dashboard personalizado con:

#### **📊 Estadísticas (4 tarjetas):**
1. **Envíos Activos** 🚛
   - Cantidad de envíos en tránsito
   - Color: Rosa/Rojo

2. **Completados** ✅
   - Envíos entregados exitosamente
   - Color: Verde

3. **Con Incidencia** ⚠️
   - Envíos con problemas
   - Color: Rojo

4. **Total Envíos** 📦
   - Todos sus envíos históricos
   - Color: Azul

#### **🚚 Envíos en Tránsito:**
Lista de envíos actualmente en camino:
- Número de guía
- Origen → Destino
- Vehículo asignado
- Conductor asignado
- Fecha de creación
- **Botón "Rastrear"** 📍 (ver ubicación en tiempo real)

#### **📋 Historial de Envíos:**
Últimos 10 envíos con:
- Número de guía
- Ruta (origen → destino)
- Vehículo y conductor
- Estado (badge de color)
- Botones:
  - "Ver Detalle"
  - "Rastrear" (si está en ruta)

#### **⚡ Acciones Rápidas:**
Panel con botones para:
- ➕ Nuevo Envío
- 📋 Mis Envíos

#### **⚠️ Alertas:**
Notificaciones sobre sus envíos:
- Tipo de alerta
- Número de guía del envío
- Descripción
- Fecha y hora

#### **📞 Contacto:**
Información de soporte:
- Teléfono: +593 99 123 4567
- Email: soporte@cargotrack.ec

---

## 📦 **MIS ENVÍOS:**

### **Acceso:**
- Menú lateral → "Mis Envíos"
- O Dashboard → "Mis Envíos"

### **Qué ve:**
Lista completa de **SOLO SUS ENVÍOS** (no ve envíos de otros clientes)

### **Información mostrada:**
Para cada envío:
- ✅ Número de guía
- ✅ Origen y destino
- ✅ Vehículo asignado (placa)
- ✅ Conductor asignado (nombre)
- ✅ Estado actual (badge de color):
  - 🟡 Pendiente
  - 🔵 En Ruta
  - 🟢 Entregado
  - 🔴 Incidencia
- ✅ Fecha de creación

### **Acciones disponibles:**
1. **Ver Detalle** 👁️
   - Click en "Ver Detalle"
   - Muestra información completa del envío

2. **Rastrear en Tiempo Real** 📍
   - Solo si está "En Ruta"
   - Click en "Rastrear"
   - Abre mapa con ubicación actual

### **Filtros:**
- Por estado (pendiente, en ruta, entregado)
- Por fecha
- Búsqueda por número de guía

---

## 🔍 **RASTREAR ENVÍO:**

### **Acceso:**
- Dashboard → Botón "Rastrear" en envío activo
- Mis Envíos → Botón "Rastrear"

### **Qué ve:**
1. **Mapa Interactivo** 🗺️
   - Ubicación actual del vehículo
   - Marcador animado
   - Ruta recorrida (línea azul)
   - Controles de zoom

2. **Información del Envío:**
   - Número de guía
   - Origen → Destino
   - Vehículo (placa)
   - Conductor (nombre y teléfono)
   - Estado actual

3. **Última Ubicación:**
   - Dirección aproximada
   - Coordenadas GPS
   - Fecha y hora de actualización
   - Precisión (metros)

4. **Velocidad Actual:**
   - km/h en tiempo real
   - Solo si el vehículo está en movimiento

5. **Actualizaciones Automáticas:**
   - Se actualiza cada 30 segundos
   - Sin necesidad de recargar la página
   - Usa WebSockets (tiempo real)

### **Funciones:**
- ✅ Ver ubicación en tiempo real
- ✅ Zoom in/out en el mapa
- ✅ Ver ruta recorrida
- ✅ Ver información del conductor
- ✅ Actualización automática

---

## ⚠️ **MIS ALERTAS:**

### **Acceso:**
- Menú lateral → "Mis Alertas"

### **Qué ve:**
Lista de **SOLO ALERTAS DE SUS ENVÍOS**

### **Tipos de alertas:**
1. **Robo** 🚨
   - Alerta de seguridad crítica

2. **Accidente** 💥
   - Incidente en la ruta

3. **Desvío de Ruta** 🛣️
   - Vehículo fuera de ruta planificada

4. **Retraso** ⏰
   - Demora en la entrega

5. **Temperatura** 🌡️
   - Problemas con carga refrigerada

### **Información mostrada:**
- Tipo de alerta
- Envío afectado (número de guía)
- Descripción detallada
- Fecha y hora
- Estado (atendida/pendiente)
- Quién la atendió (si aplica)

---

## 📊 **DETALLE DE ENVÍO:**

### **Acceso:**
- Mis Envíos → "Ver Detalle"

### **Información completa:**

#### **1. Datos Generales:**
- Número de guía
- Estado actual
- Fecha de creación
- Prioridad (si aplica)

#### **2. Ruta:**
- Origen (dirección completa)
- Destino (dirección completa)
- Distancia estimada

#### **3. Vehículo Asignado:**
- Placa
- Marca y modelo
- Año
- Capacidad

#### **4. Conductor:**
- Nombre completo
- Teléfono de contacto
- Documento de identidad

#### **5. Historial de Eventos:**
Línea de tiempo con:
- Fecha y hora de cada evento
- Tipo de evento (recogida, en tránsito, entrega)
- Ubicación
- Observaciones

#### **6. Alertas Asociadas:**
Lista de alertas relacionadas con este envío

---

## ❌ **LO QUE EL CLIENTE NO PUEDE HACER:**

### **NO Puede Ver:**
- ❌ Envíos de otros clientes
- ❌ Lista de todos los vehículos
- ❌ Lista de conductores
- ❌ Panel de rastreo GPS del conductor
- ❌ Panel de administración Django
- ❌ Estadísticas globales del sistema
- ❌ Alertas de otros clientes

### **NO Puede Hacer:**
- ❌ Crear/editar vehículos
- ❌ Crear/editar conductores
- ❌ Ver ubicación de vehículos no asignados a sus envíos
- ❌ Modificar envíos de otros clientes
- ❌ Acceder a configuración del sistema
- ❌ Ver información de otros clientes

### **NO Tiene Acceso A:**
- ❌ `/vehiculos/` - Lista de vehículos
- ❌ `/conductores/` - Lista de conductores
- ❌ `/conductores/rastreo/` - Panel GPS conductor
- ❌ `/admin/` - Administración Django

---

## ✅ **LO QUE EL CLIENTE SÍ PUEDE HACER:**

### **Puede Ver:**
- ✅ **SUS** envíos (todos)
- ✅ **SUS** alertas (solo de sus envíos)
- ✅ Ubicación en tiempo real de **SUS** envíos activos
- ✅ Información del vehículo asignado a **SUS** envíos
- ✅ Información del conductor asignado a **SUS** envíos
- ✅ Historial de **SUS** envíos
- ✅ Dashboard personalizado con **SUS** estadísticas

### **Puede Hacer:**
- ✅ Rastrear sus envíos en tiempo real
- ✅ Ver detalles completos de sus envíos
- ✅ Ver alertas de sus envíos
- ✅ Contactar al conductor (teléfono visible)
- ✅ Ver historial de eventos
- ✅ Buscar sus envíos por número de guía
- ✅ Filtrar sus envíos por estado

---

## 🎨 **INTERFAZ DEL CLIENTE:**

### **Colores y Diseño:**
- **Avatar:** Gradiente azul (#4facfe → #00f2fe)
- **Icono:** Persona 👤
- **Rol mostrado:** "Cliente"

### **Textos Personalizados:**
- "Mis Envíos" (en lugar de "Envíos")
- "Mis Alertas" (en lugar de "Alertas")
- "Buscar mis envíos..." (en buscador)

### **Badges y Estados:**
- 🟡 **Pendiente:** Amarillo
- 🔵 **En Ruta:** Azul
- 🟢 **Entregado:** Verde
- 🔴 **Incidencia:** Rojo

---

## 📱 **USAR COMO PWA:**

### **Instalación:**
1. Abrir en Chrome (móvil)
2. Menú → "Agregar a pantalla de inicio"
3. Confirmar instalación
4. Abrir desde icono en pantalla

### **Ventajas:**
- ✅ Funciona offline (caché)
- ✅ Icono en pantalla de inicio
- ✅ Pantalla completa (sin barra del navegador)
- ✅ Notificaciones push (próximamente)
- ✅ Acceso rápido

---

## 🔔 **NOTIFICACIONES (Próximamente):**

El cliente recibirá notificaciones sobre:
- 📍 Envío en camino
- ✅ Envío entregado
- ⚠️ Alertas de sus envíos
- 🚨 Incidencias
- ⏰ Retrasos

---

## 📞 **SOPORTE:**

### **Contacto:**
- **Teléfono:** +593 99 123 4567
- **Email:** soporte@cargotrack.ec

### **Horario:**
- Lunes a Viernes: 8:00 AM - 6:00 PM
- Sábados: 9:00 AM - 1:00 PM

---

## 🎯 **FLUJO TÍPICO DEL CLIENTE:**

### **Escenario 1: Rastrear Envío Activo**
1. Iniciar sesión
2. Ver dashboard
3. Localizar envío en "Envíos en Tránsito"
4. Click en "Rastrear"
5. Ver ubicación en tiempo real en el mapa
6. Ver información del conductor
7. Contactar al conductor si es necesario

### **Escenario 2: Ver Historial**
1. Iniciar sesión
2. Click en "Mis Envíos" (menú lateral)
3. Ver lista completa de envíos
4. Filtrar por estado o fecha
5. Click en "Ver Detalle" para más información

### **Escenario 3: Revisar Alertas**
1. Iniciar sesión
2. Ver badge de alertas en menú
3. Click en "Mis Alertas"
4. Revisar alertas pendientes
5. Ver detalles de cada alerta

---

## 🔐 **SEGURIDAD Y PRIVACIDAD:**

### **Protección de Datos:**
- ✅ Solo ve **SUS** envíos
- ✅ No puede ver envíos de otros clientes
- ✅ Datos encriptados en tránsito (HTTPS)
- ✅ Sesión segura con timeout
- ✅ Logout automático por inactividad

### **Permisos:**
- ✅ Lectura de sus envíos
- ✅ Lectura de sus alertas
- ❌ No puede modificar datos
- ❌ No puede eliminar envíos
- ❌ No puede acceder a datos de otros

---

## 💡 **CONSEJOS PARA EL CLIENTE:**

1. **Rastreo en Tiempo Real:**
   - Usa el botón "Rastrear" para ver ubicación actual
   - Se actualiza automáticamente cada 30 segundos

2. **Contacto con Conductor:**
   - El teléfono del conductor está visible
   - Puedes llamar directamente si necesitas

3. **Alertas:**
   - Revisa regularmente la sección de alertas
   - Las alertas críticas aparecen con badge rojo

4. **PWA:**
   - Instala la app en tu móvil para acceso rápido
   - Funciona offline para ver historial

5. **Soporte:**
   - Contacta a soporte si tienes dudas
   - Información de contacto en el dashboard

---

## 📊 **RESUMEN VISUAL:**

```
CLIENTE PUEDE:
✅ Ver SUS envíos
✅ Rastrear SUS envíos en tiempo real
✅ Ver SUS alertas
✅ Ver información del conductor asignado
✅ Ver información del vehículo asignado
✅ Contactar al conductor
✅ Ver historial de SUS envíos

CLIENTE NO PUEDE:
❌ Ver envíos de otros
❌ Ver lista de vehículos
❌ Ver lista de conductores
❌ Acceder a panel GPS del conductor
❌ Modificar datos del sistema
❌ Acceder a administración
```

---

**¡El cliente tiene todo lo necesario para rastrear y gestionar sus envíos de forma simple y efectiva!** 📦✨
