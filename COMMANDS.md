# 📋 BatmanWL Bot - Comandos

Referencia completa de todos los comandos disponibles. Todos los comandos soportan prefijos `/` y `.` o `..`.

## 💳 Comandos de Verificación

### /ccn o /chk
**Verificar tarjeta de crédito**

**Uso:**
```
/ccn <tarjeta>
/ccn <tarjeta>|<mes>|<año>|<cvv>
.chk 4532015112830366|12|25|123
```

**Características:**
- Valida usando algoritmo Luhn
- Identifica tipo de tarjeta (VISA, Mastercard, etc.)
- Retorna resultado detallado
- Registra en historial

---

### /ch
**Prueba de cargo (Premium/Admin)**

**Uso:**
```
/ch <tarjeta>|<mes>|<año>|<cvv>
.ch 4532015112830366|12|25|123
```

**Características:**
- Simula prueba de cargo de $1.00
- Requiere Premium o Admin
- Muestra aprobado/rechazado
- Incluye respuesta del CVV

---

### /vbv
**Verificador VBV/3D Secure (Premium/Admin)**

**Uso:**
```
/vbv <tarjeta>|<mes>|<año>|<cvv>
.vbv 4532015112830366|12|25|123
```

**Características:**
- Verifica estado VBV
- Chequea 3D Secure
- Muestra nivel de seguridad
- Requiere Premium o Admin

---

### /cardstatus
**Estado de tarjeta activa/inactiva (Premium/Admin)**

**Uso:**
```
/cardstatus <tarjeta>|<mes>|<año>|<cvv>
.cardstatus 4532015112830366|12|25|123
```

**Características:**
- Verifica si está activa o inactiva
- Muestra disponibilidad de saldo
- Requiere Premium o Admin

---

### /bin
**Búsqueda de información BIN**

**Uso:**
```
/bin <bin_número>
/bin <bin>|<mes>|<año>
.bin 453201
```

**Características:**
- Muestra tipo de tarjeta
- Muestra red (VISA, Mastercard, etc.)
- Muestra emisor y país
- Gratis para todos los usuarios

---

## 🎲 Generación de Tarjetas

### /gen
**Generar tarjetas válidas (Premium)**

**Uso:**
```
/gen <bin> [cantidad]
/gen <bin>|<mes>|<año> [cantidad]
.gen 453201 10
..mass 453201
```

**Características:**
- Genera hasta 50 tarjetas
- Todas pasan validación Luhn
- Incluye CVV y expiración
- Requiere Premium o Admin

---

## 👤 Comandos de Usuario

### /start
**Iniciar bot y ver menú principal**

**Uso:** `/start`

**Muestra:**
- Panel de bienvenida con GIF
- Menú interactivo con botones
- Tu ID de usuario
- Características del bot

---

### /menu
**Mostrar menú principal**

**Uso:** `/menu` o `.menu`

**Características:**
- Menú con botones interactivos
- Acceso rápido a funciones
- Opciones según tu rol

---

### /stats
**Ver tus estadísticas**

**Uso:** `/stats` o `.stats`

**Muestra:**
- Tu ID y nombre
- Rol (user/admin/owner)
- Estado Premium
- Total de verificaciones

---

### /help
**Mostrar ayuda y comandos**

**Uso:** `/help` o `.help`

**Características:**
- Lista completa de comandos
- Ejemplos de uso
- Formato profesional
- Comandos admin (si aplica)

---

## 🔑 Premium

### /key
**Activar clave premium**

**Uso:**
```
/key <clave_premium>
/key ABC123XYZ
```

**Características:**
- Activa premium por 30 días (configurable)
- Desbloquea generación de tarjetas
- Acceso a comandos premium

---

## 🔐 Comandos de Administración

### /genkey
**Generar claves premium (Admin)**

**Uso:**
```
/genkey [cantidad]
/genkey 5
```

**Características:**
- Genera hasta 20 claves
- Solo para admins
- Claves válidas por duración configurada

---

### /ban
**Banear usuario (Admin)**

**Uso:**
```
/ban <user_id>
/ban 123456789
```

**Características:**
- Impide uso del bot
- Se registra en logs
- Reversible con /unban

---

### /unban
**Desbanear usuario (Admin)**

**Uso:**
```
/unban <user_id>
/unban 123456789
```

**Características:**
- Restaura acceso del usuario
- Se registra en logs

---

### /addcredits
**Agregar créditos (Admin)**

**Uso:**
```
/addcredits <user_id> <cantidad>
/addcredits 123456789 100
```

**Características:**
- Agrega cualquier cantidad
- Efecto inmediato
- Se registra en logs

---

### /broadcast
**Enviar mensaje a todos (Admin)**

**Uso:**
```
/broadcast <mensaje>
/broadcast ¡Nueva actualización disponible!
```

**Características:**
- Envía a todos los usuarios registrados
- Solo admins
- Útil para anuncios

---

### /statsadmin
**Ver estadísticas globales (Admin)**

**Uso:** `/statsadmin`

**Muestra:**
- Total de usuarios
- Total de verificaciones
- Usuarios premium
- Estadísticas detalladas

---

## 💡 Consejos de Uso

### Usando Prefijos
Todos los comandos funcionan con `/`, `.` o `..`:
```
/ccn 4532015112830366|12|25|123
.chk 4532015112830366|12|25|123
..ccn 4532015112830366|12|25|123
```

### Formato de Tarjeta
El formato completo es: `tarjeta|mes|año|cvv`
```
4532015112830366|12|25|123
```

También puedes usar formatos parciales:
```
4532015112830366           # Solo número
4532015112830366|12|25     # Sin CVV
```

### Acceso Rápido
Usa los botones del menú en `/start` para acceso rápido a comandos comunes.

### Obtener Ayuda
- Usa `/help` para guía general
- Cada comando muestra ayuda si se usa incorrectamente
- Contacta al owner para soporte

---

## 📊 Resumen de Categorías

| Categoría | Comandos | Descripción |
|-----------|----------|-------------|
| Verificación | `/ccn` `/ch` `/vbv` `/cardstatus` `/bin` | Validación de tarjetas |
| Generación | `/gen` | Generación de tarjetas (Premium) |
| Usuario | `/start` `/menu` `/stats` `/help` | Gestión de cuenta |
| Premium | `/key` | Sistema premium |
| Admin | `/genkey` `/ban` `/unban` `/addcredits` `/broadcast` `/statsadmin` | Administración |

---

## 🎯 Ejemplos

### Verificación Básica
```
.chk 4532015112830366|12|25|123
```

### Verificación Avanzada (Premium)
```
.ch 4532015112830366|12|25|123
.vbv 4532015112830366|12|25|123
.cardstatus 4532015112830366|12|25|123
```

### Búsqueda BIN
```
.bin 453201
```

### Generación de Tarjetas (Premium)
```
.gen 453201 10
..mass 453201
```

### Operaciones Admin
```
/ban 123456789
/addcredits 123456789 100
/broadcast ¡Nueva función disponible!
```

---

¿Necesitas más ayuda? Usa `/help` en el bot o contacta al administrador.
