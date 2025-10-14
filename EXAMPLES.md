# 📚 Ejemplos de Uso - BatmanWL Bot

## Verificación de Tarjetas (CCN Check)

### Ejemplo 1: Verificar una tarjeta

```
/ccn 4532015112830366
```

**Respuesta:**
```
🔍 Verificación de Tarjeta

💳 Tarjeta: 4532 0151 1283 0366
✅ Tarjeta ACTIVA

Estado: ACTIVE
```

### Ejemplo 2: Verificar con formato alternativo

```
..ccn 5425233430109903
```

**Respuesta:**
```
🔍 Verificación de Tarjeta

💳 Tarjeta: 5425 2334 3010 9903
❌ Tarjeta INACTIVA

Estado: INACTIVE
```

### Ejemplo 3: Tarjeta inválida

```
/ccn 1234567890123456
```

**Respuesta:**
```
🔍 Verificación de Tarjeta

💳 Tarjeta: 1234 5678 9012 3456
❌ Tarjeta inválida (no pasa validación Luhn)

Estado: INVALID
```

---

## Búsqueda de BIN

### Ejemplo 1: BIN de VISA

```
/bin 453201
```

**Respuesta:**
```
🔍 Información BIN

📊 BIN: 453201
🏦 Tipo: VISA
🌐 Red: Visa
🏢 Emisor: Banco emisor VISA
🌍 País: Internacional
```

### Ejemplo 2: BIN de Mastercard

```
..bin 542523
```

**Respuesta:**
```
🔍 Información BIN

📊 BIN: 542523
🏦 Tipo: MASTERCARD
🌐 Red: Mastercard
🏢 Emisor: Banco emisor MASTERCARD
🌍 País: Internacional
```

### Ejemplo 3: BIN de American Express

```
/bin 378282
```

**Respuesta:**
```
🔍 Información BIN

📊 BIN: 378282
🏦 Tipo: AMEX
🌐 Red: American Express
🏢 Emisor: American Express
🌍 País: USA
```

---

## Generación de Tarjetas (Premium)

### Ejemplo 1: Generar 10 tarjetas

```
/gen 453201 10
```

**Respuesta:**
```
💳 Tarjetas Generadas

🔢 BIN: 453201
📊 Cantidad: 10

4532 0191 3762 8912|08/28|847
4532 0145 2793 0156|03/27|293
4532 0198 4521 6734|11/29|612
4532 0173 8495 0283|05/26|458
4532 0162 9374 5018|09/28|731
4532 0187 2946 3502|12/27|925
4532 0154 8320 9176|06/29|384
4532 0193 7568 2409|02/26|576
4532 0178 4053 6921|10/28|492
4532 0165 9182 7435|04/27|638

✅ Todas las tarjetas pasan validación Luhn
```

### Ejemplo 2: Generar pocas tarjetas

```
..gen 542523 3
```

**Respuesta:**
```
💳 Tarjetas Generadas

🔢 BIN: 542523
📊 Cantidad: 3

5425 2334 8192 7456|07/28|912
5425 2371 6583 0294|01/29|347
5425 2398 5274 6130|11/26|589

✅ Todas las tarjetas pasan validación Luhn
```

### Ejemplo 3: Sin premium

```
/gen 453201 10
```

**Respuesta:**
```
❌ Esta función requiere Premium
Usa /key <clave> para activar premium
```

---

## Sistema Premium

### Ejemplo 1: Activar clave premium

```
/key ABC123XYZ456
```

**Respuesta:**
```
✅ Clave activada! Premium hasta: 2025-11-13 15:30:45
```

### Ejemplo 2: Clave ya usada

```
/key ABC123XYZ456
```

**Respuesta:**
```
❌ Esta clave ya ha sido utilizada
```

### Ejemplo 3: Clave inválida

```
/key CLAVEINVALIDA
```

**Respuesta:**
```
❌ Clave no válida
```

---

## Estadísticas de Usuario

### Ejemplo 1: Usuario normal

```
/stats
```

**Respuesta:**
```
📊 Tus Estadísticas

👤 Usuario: @testuser
🆔 ID: 123456789
🎭 Rol: user
⭐ Premium: ❌ Inactivo

📈 Verificaciones: 15
```

### Ejemplo 2: Usuario premium

```
..stats
```

**Respuesta:**
```
📊 Tus Estadísticas

👤 Usuario: @premiumuser
🆔 ID: 987654321
🎭 Rol: user
⭐ Premium: ✅ Activo

📈 Verificaciones: 87
```

### Ejemplo 3: Administrador

```
/stats
```

**Respuesta:**
```
📊 Tus Estadísticas

👤 Usuario: @adminuser
🆔 ID: 555555555
🎭 Rol: admin
⭐ Premium: ✅ Activo

📈 Verificaciones: 234
```

---

## Comandos de Administración

### Ejemplo 1: Generar una clave

```
/genkey
```

**Respuesta:**
```
🔑 Claves Premium Generadas

Cantidad: 1

tKp9Xm4nL8QwR2vY

Duración: 30 días
```

### Ejemplo 2: Generar múltiples claves

```
/genkey 5
```

**Respuesta:**
```
🔑 Claves Premium Generadas

Cantidad: 5

tKp9Xm4nL8QwR2vY
bNm7Hj3kP5RwT9xZ
gQw2Vn8mL4KpX6yT
jRx5Mn9kP2LwV7zQ
fTy8Kp3mN6RwX4vL

Duración: 30 días
```

### Ejemplo 3: Usuario sin permisos

```
/genkey
```

**Respuesta:**
```
❌ No tienes permiso para usar este comando
```

---

## Usando el Menú Interactivo

### Opción 1: Desde el inicio

1. Envía `/start`
2. Verás el GIF de bienvenida y botones
3. Presiona el botón "✅ Verificar Tarjeta (CCN)"
4. Sigue las instrucciones

### Opción 2: Menú principal

1. Envía `/menu` o `..menu`
2. Selecciona una opción:
   - ✅ Verificar Tarjeta (CCN)
   - 🔍 Buscar BIN
   - 💳 Generar Tarjetas (solo premium)
   - 🔑 Activar Clave Premium
   - 📊 Mis Estadísticas
   - ⚙️ Panel Admin (solo admin)
   - ℹ️ Ayuda

---

## Flujo de Trabajo Típico

### Flujo 1: Usuario Nuevo

```
1. /start              → Ver bienvenida
2. /ccn 4532...        → Probar verificación
3. /bin 453201         → Buscar BIN
4. /key ABC123XYZ      → Activar premium
5. /gen 453201 10      → Generar tarjetas
6. /stats              → Ver estadísticas
```

### Flujo 2: Administrador

```
1. /start              → Ver bienvenida
2. /genkey 10          → Generar claves
3. (compartir claves con usuarios)
4. /gen 453201 20      → Generar tarjetas
5. /stats              → Ver estadísticas
```

### Flujo 3: Usuario Premium

```
1. /menu               → Ver menú
2. /ccn 5425...        → Verificar tarjetas
3. /gen 542523 15      → Generar tarjetas
4. /bin 542523         → Buscar BIN
5. /stats              → Ver progreso
```

---

## Tips y Trucos

### Tip 1: Comandos rápidos con ".."

En lugar de `/ccn`, usa `..ccn` para escribir más rápido.

### Tip 2: Copiar tarjetas generadas

Las tarjetas se generan en formato copiable con backticks:
```
4532 0191 3762 8912|08/28|847
```

Puedes copiar directamente desde Telegram.

### Tip 3: Verificación masiva

Aunque no hay un comando específico, puedes usar un script:
```bash
for card in 4532015112830366 5425233430109903; do
    echo "/ccn $card"
done
```

### Tip 4: Guardar estadísticas

Toma screenshots de tus `/stats` para hacer seguimiento.

---

## Casos de Uso Avanzados

### Caso 1: Testing de Integración

Usa el bot para generar tarjetas de prueba para tu aplicación:
```
/gen 453201 50
```

### Caso 2: Educación

Enseña sobre validación Luhn usando `/ccn` con diferentes tarjetas.

### Caso 3: Gestión de Usuarios

Como admin, distribuye claves premium a usuarios confiables:
```
/genkey 10
```

---

## Próximos Pasos

1. Lee el [README completo](README.md)
2. Consulta la [Guía Rápida](QUICKSTART.md)
3. Explora todas las funciones del bot
4. Reporta bugs o sugiere mejoras

**¡Disfruta BatmanWL! 🦇**
