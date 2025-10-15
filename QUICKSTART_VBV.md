# 🚀 Guía Rápida: Cómo Usar VBV Real de Forma Segura

## ⚡ Inicio Rápido (5 minutos)

### Paso 1: Crear cuenta Stripe (Gratis)
1. Ve a [https://stripe.com](https://stripe.com)
2. Crea una cuenta
3. NO necesitas verificar tu negocio para modo test

### Paso 2: Obtener clave API de prueba
1. En Dashboard de Stripe → **Developers** → **API keys**
2. Copia tu **Secret key** que empieza con `sk_test_...`
3. ⚠️ **IMPORTANTE**: Debe ser `sk_test_...` NO `sk_live_...`

### Paso 3: Configurar el bot
Edita `config.ini`:
```ini
[PAYMENT_GATEWAY]
GATEWAY_TYPE = stripe
API_KEY = sk_test_tu_clave_aqui
TEST_MODE = true
```

### Paso 4: Instalar librería Stripe
```bash
pip install stripe
```

### Paso 5: Reiniciar el bot
```bash
python bot.py
```

Verás en los logs:
```
💳 Payment Gateway: stripe
```

## ✅ Probar VBV

### Comando:
```
/vbv 4242424242424242|12|25|123
```

### Resultado esperado:
```
🔐 VERIFICADOR VBV

💳 Tarjeta: 4242424242424242
🏦 Tipo: VISA
🏷️ Marca: VISA

Estado VBV: ✅ HABILITADO
3D Secure: ✅ Activo
Nivel de Seguridad: 🔒 Alto

✅ Gateway Real: stripe
⚠️ Modo Test - Solo usar tarjetas de prueba de Stripe
🔖 ID: pm_1xxxxxxxxxxxxx
```

## 🎯 Tarjetas de Prueba de Stripe

### Para usar en modo TEST:
- ✅ **4242 4242 4242 4242** - Siempre aprobada
- ✅ **4000 0025 0000 3155** - Requiere autenticación 3D
- ✅ **4000 0000 0000 0002** - Siempre declinada

### NUNCA uses:
- ❌ Tarjetas reales de banco
- ❌ Tu tarjeta personal
- ❌ Tarjetas de clientes

## ⚠️ Reglas de Oro

### ✅ SIEMPRE:
1. Usa `TEST_MODE = true` para pruebas
2. Usa solo tarjetas de prueba de Stripe
3. Verifica que tu API key sea `sk_test_...`
4. Lee los logs al iniciar el bot

### ❌ NUNCA:
1. Uses tarjetas reales en modo TEST
2. Cambies a `TEST_MODE = false` sin entender las consecuencias
3. Compartas tu API key en público
4. Ignores advertencias del bot

## 🔍 Verificar Configuración

### ✅ Configuración correcta:
```
Logs al iniciar:
💳 Payment Gateway: stripe

Respuesta del bot:
✅ Gateway Real: stripe
⚠️ Modo Test - Solo usar tarjetas de prueba de Stripe
```

### ❌ Configuración incorrecta:
```
Respuesta del bot:
❌ Error de Configuración
⚠️ VBV real requiere configurar PAYMENT_GATEWAY
```

## 📧 ¿Recibiste Email de Alerta?

### Pasos inmediatos:
1. **DETÉN el bot** inmediatamente
2. **VERIFICA** tu config.ini:
   ```ini
   TEST_MODE = true  ← ¿Está en true?
   API_KEY = sk_test_...  ← ¿Empieza con sk_test?
   ```
3. **ELIMINA** cualquier dato de tarjetas reales del sistema
4. **RESPONDE** al email de Stripe explicando:
   ```
   Hola,
   
   Estoy desarrollando un bot de Telegram y estaba probando
   la integración con su API. 
   
   He configurado TEST_MODE = true y solo usaré tarjetas
   de prueba de Stripe de aquí en adelante.
   
   ¿Podrían indicarme si mi cuenta está en buen estado?
   
   Gracias
   ```

## 💡 Tips Adicionales

### Monitorear uso:
- En Dashboard de Stripe puedes ver todas las transacciones
- En modo test, todo es gratis
- Las tarjetas de prueba no generan cargos reales

### Cuándo pasar a producción:
- Solo cuando tengas un negocio real
- Después de verificar tu identidad con Stripe
- Cambia `TEST_MODE = false` y usa `sk_live_...`
- **IMPORTANTE**: En producción solo procesa pagos legítimos de clientes reales

## 🎓 Recursos de Aprendizaje

### Documentación del bot:
- [VBV_FRAUD_PREVENTION.md](VBV_FRAUD_PREVENTION.md) - Guía completa
- [PAYMENT_GATEWAY_SETUP.md](PAYMENT_GATEWAY_SETUP.md) - Configuración detallada
- [COMPARISON_BEFORE_AFTER.md](COMPARISON_BEFORE_AFTER.md) - Ver cambios

### Documentación de Stripe:
- [Testing Cards](https://stripe.com/docs/testing) - Tarjetas de prueba
- [3D Secure](https://stripe.com/docs/strong-customer-authentication) - Info sobre 3DS
- [Best Practices](https://stripe.com/docs/security/best-practices) - Seguridad

## ❓ FAQ Rápido

**P: ¿Es gratis usar Stripe en modo test?**
R: Sí, modo test es 100% gratis, sin límites.

**P: ¿Necesito verificar mi negocio?**
R: No para modo test. Solo para modo producción.

**P: ¿Qué pasa si uso una tarjeta real por error?**
R: Puede generar alerta de fraude. Sigue los pasos de la sección "¿Recibiste Email de Alerta?"

**P: ¿Puedo usar VBV sin configurar Stripe?**
R: Sí, pero el bot te mostrará un error indicando que necesitas configurarlo para usar VBV real.

**P: ¿Cuántas veces puedo probar VBV?**
R: En modo test, ilimitadas veces con tarjetas de prueba.

## ✅ Checklist Final

Antes de usar VBV, verifica:

- [ ] Cuenta de Stripe creada
- [ ] API key `sk_test_...` copiada
- [ ] `config.ini` editado con tu API key
- [ ] `TEST_MODE = true` configurado
- [ ] `pip install stripe` ejecutado
- [ ] Bot reiniciado y logs verificados
- [ ] Solo usarás tarjetas de prueba (4242...)
- [ ] Has leído esta guía completa

**¿Todo marcado? ¡Listo para usar VBV real! 🎉**

---

**Problemas?** Lee [VBV_FRAUD_PREVENTION.md](VBV_FRAUD_PREVENTION.md) o [PAYMENT_GATEWAY_SETUP.md](PAYMENT_GATEWAY_SETUP.md)
