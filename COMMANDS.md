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

### /redeem
**Activar clave premium**

**Uso:**
```
/redeem <clave_premium>
/redeem ABC123XYZ
..redeem ABC123XYZ
```

**Características:**
- Activa premium por la duración configurada en la clave
- Desbloquea generación de tarjetas
- Acceso a comandos premium

---

## 🌐 Comandos de Payment Gateways

### /gatewayhelp
**Ver ayuda de gateways**

**Uso:** `/gatewayhelp`

**Muestra:**
- Lista de todos los gateways
- Comandos disponibles
- Tipo (FREE/PREMIUM)
- Características de cada gateway

---

### /gateways
**Ver estado de gateways**

**Uso:** `/gateways`

**Muestra:**
- Estado online/offline
- Gateways configurados
- Estado de CapSolver

---

### /adyen
**Adyen Auth + VBV (PREMIUM)**

**Uso:**
```
/adyen <tarjeta>|<mes>|<año>|<cvv>
/adyen 4532015112830366|12|25|123
```

**Características:**
- Autorización de tarjeta
- Verificación VBV/3D Secure
- Cobertura global
- Requiere Premium o Admin

---

### /bluepay
**BluePay CCN Validation (FREE)**

**Uso:**
```
/bluepay <tarjeta>|<mes>|<año>|<cvv>
/bluepay 4532015112830366|12|25|123
```

**Características:**
- Validación de número de tarjeta
- Verificación AVS
- Gratis para todos

---

### /braintree
**Braintree Auth (PREMIUM)**

**Uso:**
```
/braintree <tarjeta>|<mes>|<año>|<cvv>
/braintree 4532015112830366|12|25|123
```

**Características:**
- Autorización PayPal-owned
- Detección de fraude
- 3D Secure fuerte
- Requiere Premium o Admin

---

### /exact
**Exact CCN Check (FREE)**

**Uso:**
```
/exact <tarjeta>|<mes>|<año>|<cvv>
/exact 4532015112830366|12|25|123
```

**Características:**
- Validación rápida CCN
- Info básica de tarjeta
- Gratis para todos

---

### /chase
**Chase Paymentech (PREMIUM)**

**Uso:**
```
/chase <tarjeta>|<mes>|<año>|<cvv>
/chase 4532015112830366|12|25|123
```

**Características:**
- Procesador bancario mayor
- Validación completa
- Alto trust score
- Requiere Premium o Admin

---

### /payeezy
**Payeezy Charge Test (PREMIUM)**

**Uso:**
```
/payeezy <tarjeta>|<mes>|<año>|<cvv>
/payeezy 4532015112830366|12|25|123
```

**Características:**
- Prueba de cargo real ($1.00)
- Detección de fraude
- First Data infrastructure
- Requiere Premium o Admin

---

### /payflow
**PayPal Payflow Charge (PREMIUM)**

**Uso:**
```
/payflow <tarjeta>|<mes>|<año>|<cvv>
/payflow 4532015112830366|12|25|123
```

**Características:**
- Prueba de cargo real ($1.00)
- Infraestructura PayPal
- Procesamiento confiable
- Requiere Premium o Admin

---

### /paypalgateway
**PayPal Gateway (FREE)**

**Uso:**
```
/paypalgateway <tarjeta>|<mes>|<año>|<cvv>
/paypalgateway 4532015112830366|12|25|123
```

**Características:**
- Validación de tarjeta
- Cobertura global
- Protección al comprador
- Gratis (básico)

---

### /sewin
**Sewin CCN Check (FREE)**

**Uso:**
```
/sewin <tarjeta>|<mes>|<año>|<cvv>
/sewin 4532015112830366|12|25|123
```

**Características:**
- Validación rápida CCN
- Check de número de tarjeta
- Gratis para todos

---

### /stripegateway
**Stripe Auth + VBV (FREE/PREMIUM)**

**Uso:**
```
/stripegateway <tarjeta>|<mes>|<año>|<cvv>
/stripegateway 4532015112830366|12|25|123
```

**Características:**
- Autorización estándar
- Verificación 3D Secure
- Gratis (básico)
- Premium (VBV avanzado)

---

## 🔐 Comandos de Administración

### /genkey
**Generar claves premium (Admin)**

**Uso:**
```
/genkey [cantidad] [duración]
/genkey 5 24h
/genkey 3 30m
/genkey 10 7d
/genkey 2 3600s
```

**Características:**
- Genera hasta 20 claves
- Solo para admins
- Claves con duración personalizable (s/m/h/d)
- Claves más largas (32 caracteres) para mayor seguridad

**Unidades de tiempo:**
- `s` - Segundos
- `m` - Minutos  
- `h` - Horas
- `d` - Días

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
| Premium | `/redeem` | Sistema premium |
| Gateways | `/adyen` `/bluepay` `/braintree` `/exact` `/chase` `/payeezy` `/payflow` `/paypalgateway` `/sewin` `/stripegateway` | Gateways de pago |
| Gateway Info | `/gatewayhelp` `/gateways` | Información de gateways |
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
/genkey 5 24h
/genkey 3 30m
/ban 123456789
/addcredits 123456789 100
/broadcast ¡Nueva función disponible!
```

### Gateways de Pago
```
# FREE Gateways
/bluepay 4532015112830366|12|25|123
/exact 4532015112830366|12|25|123
/sewin 4532015112830366|12|25|123
/paypalgateway 4532015112830366|12|25|123

# PREMIUM Gateways
/adyen 4532015112830366|12|25|123
/braintree 4532015112830366|12|25|123
/chase 4532015112830366|12|25|123
/payeezy 4532015112830366|12|25|123
/payflow 4532015112830366|12|25|123
/stripegateway 4532015112830366|12|25|123

# Ver estado
/gateways
/gatewayhelp
```

---

¿Necesitas más ayuda? Usa `/help` en el bot o contacta al administrador.
