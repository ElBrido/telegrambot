# ❓ Preguntas Frecuentes (FAQ)

## Preguntas Generales

### ¿Qué es BatmanWL Bot?
BatmanWL es un bot profesional de Telegram para verificación de tarjetas de crédito. Utiliza algoritmos estándar de la industria (Luhn) para validar números de tarjeta y proporciona información detallada sobre tarjetas y BINs.

### ¿Es gratis usar el bot?
Sí, el bot es gratis para las funciones básicas de verificación. Las funciones premium como la generación masiva de tarjetas requieren una clave premium.

### ¿Es seguro usar?
El bot está diseñado con seguridad en mente. Ten en cuenta que esto es una simulación con fines educativos. Solo se almacenan los últimos 4 dígitos de las tarjetas en la base de datos por privacidad.

### ¿Cómo funciona la verificación de tarjetas?
El bot valida tarjetas usando el algoritmo Luhn y simula respuestas de gateway. Las verificaciones son simuladas para fines educativos.

---

## Primeros Pasos

### ¿Cómo empiezo a usar el bot?
1. Busca el bot en Telegram
2. Envía el comando `/start`
3. Verás el panel de bienvenida
4. Usa `/ccn` o `.chk` para verificar tu primera tarjeta

### ¿Qué comandos puedo usar?
Envía `/help` para ver todos los comandos disponibles. Puedes usar prefijos `/`, `.` o `..` para todos los comandos.

### ¿Puedo usar comandos con punto (.) en lugar de barra (/)?
¡Sí! Todos los comandos soportan ambos prefijos. Por ejemplo, tanto `/ccn` como `.chk` funcionan igual.

---

## Verificación de Tarjetas

### ¿Qué formato debo usar para verificar tarjetas?
Usa este formato: `número_tarjeta|mes|año|cvv`

Ejemplo: `/ccn 4532015112830366|12|25|123`

También puedes usar formato parcial:
- Solo número: `4532015112830366`
- Sin CVV: `4532015112830366|12|25`

### ¿Qué comandos de verificación están disponibles?
- `/ccn` o `/chk` - Verificación básica (gratis)
- `/ch` - Prueba de cargo (Premium/Admin)
- `/vbv` - Verificador VBV/3D Secure (Premium/Admin)
- `/cardstatus` - Estado activa/inactiva (Premium/Admin)
- `/bin` - Búsqueda de información BIN (gratis)

### ¿Qué tipos de tarjetas son soportados?
El bot soporta:
- VISA
- Mastercard
- American Express (AMEX)
- Discover
- Diners Club
- JCB

### ¿Qué significa "APPROVED" o "DECLINED"?
Son respuestas simuladas para fines educativos:
- **APPROVED**: La tarjeta pasó las validaciones
- **DECLINED**: La tarjeta falló la validación

### ¿El bot almacena mis números de tarjeta?
Solo se almacenan los últimos 4 dígitos en la base de datos para estadísticas. Los números completos nunca se almacenan.

---

## Sistema Premium

### ¿Qué es Premium?
Premium desbloquea funciones adicionales:
- Generación masiva de tarjetas (`/gen`)
- Prueba de cargo (`/ch`)
- Verificador VBV (`/vbv`)
- Verificación de estado (`/cardstatus`)

### ¿Cómo obtengo Premium?
Contacta a un administrador para obtener una clave premium. Luego usa:
```
/key <tu_clave_premium>
```

### ¿Cuánto dura Premium?
La duración se configura cuando se genera la clave (típicamente 30 días).

### ¿Puedo compartir mi clave premium?
No, cada clave es de un solo uso y se vincula a tu cuenta.

---

## Generación de Tarjetas

### ¿Cómo genero tarjetas? (Premium)
Usa el comando `/gen`:
```
/gen <bin> [cantidad]
/gen 453201 10
```

Esto genera tarjetas válidas que pasan el algoritmo Luhn.

### ¿Cuántas tarjetas puedo generar?
Hasta 50 tarjetas por comando.

### ¿Las tarjetas generadas son reales?
No, son números válidos matemáticamente (pasan Luhn) pero son ficticios. Solo para pruebas educativas.

---

## Admin y Roles

### ¿Cómo me convierto en admin?
El estado de admin es controlado por el owner del bot. Contacta al propietario si necesitas acceso admin.

### ¿Qué pueden hacer los admins?
Los admins pueden:
- Banear/desbanear usuarios
- Agregar créditos a usuarios
- Generar claves premium
- Enviar mensajes broadcast
- Ver estadísticas globales

### ¿Qué es un Owner?
El Owner tiene todos los permisos de admin más control total sobre el bot.

---

## BIN Lookup

### ¿Qué es un BIN?
BIN (Bank Identification Number) son los primeros 6 dígitos de una tarjeta que identifican al emisor.

### ¿Cómo hago una búsqueda BIN?
```
/bin 453201
.bin 453201
```

### ¿Es gratis el BIN lookup?
Sí, la búsqueda BIN es gratis para todos los usuarios.

### ¿Qué información muestra?
- Tipo de tarjeta (Crédito/Débito)
- Red (VISA, Mastercard, etc.)
- Banco emisor
- País

---

## Estadísticas

### ¿Cómo veo mis estadísticas?
Usa el comando `/stats` o `.stats`

### ¿Qué estadísticas se muestran?
- Tu ID de usuario
- Rol (user/admin/owner)
- Estado Premium
- Total de verificaciones realizadas

### ¿Los admins tienen estadísticas especiales?
Sí, los admins pueden usar `/statsadmin` para ver estadísticas globales del bot.

---

## Problemas Comunes

### El bot no responde
**Verifica:**
1. ¿El bot está en línea? Contacta al admin
2. ¿Estás baneado? Contacta al admin
3. ¿Telegram tiene problemas? Verifica el estado de Telegram

### Obtengo error "Invalid format"
Asegúrate de usar el formato correcto: `tarjeta|mes|año|cvv`

Ejemplo correcto: `4532015112830366|12|25|123`

### El comando no funciona
1. Verifica que escribiste el comando correctamente
2. Algunos comandos requieren Premium o Admin
3. Usa `/help` para ver la sintaxis correcta

### No puedo generar tarjetas
La generación de tarjetas (`/gen`) requiere:
- Estado Premium activo, O
- Rol de Admin o Owner

Usa `/key <clave>` para activar premium.

### Olvidé mi clave premium
Las claves son de un solo uso. Si ya activaste premium, puedes verificar tu estado con `/stats`. Si no la usaste, contacta a quien te la dio.

---

## Seguridad y Privacidad

### ¿Es legal usar este bot?
El bot es para fines educativos y de prueba únicamente. No debe usarse para actividades ilegales.

### ¿Mis datos están seguros?
- Solo se almacenan IDs de usuario y estadísticas básicas
- No se almacenan números completos de tarjeta
- Los datos no se comparten con terceros

### ¿Qué información se registra?
- ID de usuario y username
- Rol y estado premium
- Historial de verificaciones (solo últimos 4 dígitos)
- Estadísticas de uso

---

## Comandos Adicionales

### ¿Cómo veo todos los comandos?
Usa `/help` o `.help` para ver la lista completa con ejemplos.

### ¿Hay comandos ocultos?
No, todos los comandos están documentados en `/help`.

### ¿Puedo sugerir nuevas funciones?
Sí, contacta al owner del bot con tus sugerencias.

---

## Soporte

### ¿Cómo obtengo ayuda?
1. Usa `/help` para guía general
2. Lee este FAQ
3. Contacta al administrador del bot

### ¿Dónde reporto bugs?
Contacta al owner del bot o abre un issue en el repositorio de GitHub (si está disponible).

### ¿Puedo contribuir al bot?
Si el bot es de código abierto, puedes contribuir siguiendo las guías de contribución.

---

## Disclaimer Legal

⚠️ **IMPORTANTE**: Este bot es solo para fines educativos y de demostración. No debe utilizarse para:
- Actividades ilegales
- Fraude con tarjetas
- Verificación real de pagos sin autorización
- Cualquier uso que viole términos de servicio

La verificación de tarjetas es simulada y no realiza verificaciones reales contra sistemas de pago.

---

¿Tienes más preguntas? Usa `/help` en el bot o contacta al administrador.
