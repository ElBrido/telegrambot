# 💳 Configuración de Pasarela de Pagos

Esta guía te ayudará a configurar una pasarela de pagos real para el bot BatmanWL.

## 📋 Tabla de Contenidos

- [Pasarelas Soportadas](#pasarelas-soportadas)
- [Configuración General](#configuración-general)
- [Stripe](#stripe)
- [PayPal](#paypal)
- [MercadoPago](#mercadopago)
- [Modo de Prueba vs Producción](#modo-de-prueba-vs-producción)

## 🎯 Pasarelas Soportadas

El bot actualmente soporta las siguientes pasarelas de pago:

- ✅ **Stripe** - Totalmente implementado
- ⚠️ **PayPal** - Requiere SDK adicional
- ⚠️ **MercadoPago** - Requiere SDK adicional

Si no configuras ninguna pasarela, el bot funcionará en **modo simulación**.

## ⚙️ Configuración General

Edita el archivo `config.ini` y localiza la sección `[PAYMENT_GATEWAY]`:

```ini
[PAYMENT_GATEWAY]
# Payment gateway configuration for real charge testing
# Supported: stripe, paypal, mercadopago, or leave empty for simulation mode
GATEWAY_TYPE = 

# API credentials - Get these from your payment gateway dashboard
API_KEY = 
API_SECRET = 

# Webhook secret for payment confirmations (optional)
WEBHOOK_SECRET = 

# Test mode (true/false) - Use test API keys when true
TEST_MODE = true
```

## 🔵 Stripe

### Paso 1: Crear cuenta en Stripe

1. Ve a [https://stripe.com](https://stripe.com)
2. Crea una cuenta o inicia sesión
3. Ve al Dashboard

### Paso 2: Obtener claves API

1. En el Dashboard, ve a **Developers** → **API keys**
2. Encontrarás dos tipos de claves:
   - **Test keys** (para pruebas)
   - **Live keys** (para producción)

3. Copia las claves:
   - **Publishable key** (clave pública)
   - **Secret key** (clave secreta) ← Esta es la que necesitas

### Paso 3: Instalar librería de Stripe

```bash
pip install stripe
```

### Paso 4: Configurar en config.ini

Para **modo de prueba**:
```ini
[PAYMENT_GATEWAY]
GATEWAY_TYPE = stripe
API_KEY = sk_test_XXXXXXXXXXXXXXXXXXXXXXXX
API_SECRET = 
TEST_MODE = true
```

Para **modo producción**:
```ini
[PAYMENT_GATEWAY]
GATEWAY_TYPE = stripe
API_KEY = sk_live_XXXXXXXXXXXXXXXXXXXXXXXX
API_SECRET = 
TEST_MODE = false
```

### Paso 5: Tarjetas de prueba

Cuando `TEST_MODE = true`, puedes usar estas tarjetas de prueba:

- **Aprobada**: 4242 4242 4242 4242
- **Requiere autenticación**: 4000 0025 0000 3155
- **Declinada**: 4000 0000 0000 0002

Usa cualquier:
- CVV: 3 dígitos
- Fecha de expiración: en el futuro
- ZIP: cualquier código postal

### 📚 Documentación oficial

- [Stripe API Docs](https://stripe.com/docs/api)
- [Testing Stripe](https://stripe.com/docs/testing)

## 🟡 PayPal

⚠️ **Implementación en desarrollo**

Para usar PayPal necesitarás:

### Paso 1: Crear cuenta de desarrollador

1. Ve a [https://developer.paypal.com](https://developer.paypal.com)
2. Crea una cuenta de desarrollador
3. Ve a **Dashboard** → **My Apps & Credentials**

### Paso 2: Crear una aplicación

1. Crea una nueva app REST API
2. Obtén tus credenciales:
   - **Client ID**
   - **Secret**

### Paso 3: Instalar SDK

```bash
pip install paypalrestsdk
```

### Paso 4: Configurar

```ini
[PAYMENT_GATEWAY]
GATEWAY_TYPE = paypal
API_KEY = YOUR_CLIENT_ID
API_SECRET = YOUR_SECRET
TEST_MODE = true
```

**Nota**: La implementación completa de PayPal requiere desarrollo adicional.

## 🟢 MercadoPago

⚠️ **Implementación en desarrollo**

Para usar MercadoPago:

### Paso 1: Crear cuenta

1. Ve a [https://www.mercadopago.com](https://www.mercadopago.com)
2. Crea una cuenta
3. Ve a **Tus integraciones**

### Paso 2: Obtener credenciales

1. En el panel, ve a **Credenciales**
2. Obtén:
   - **Public key**
   - **Access token**

### Paso 3: Instalar SDK

```bash
pip install mercadopago
```

### Paso 4: Configurar

```ini
[PAYMENT_GATEWAY]
GATEWAY_TYPE = mercadopago
API_KEY = YOUR_ACCESS_TOKEN
API_SECRET = 
TEST_MODE = true
```

**Nota**: La implementación completa de MercadoPago requiere desarrollo adicional.

## 🔄 Modo de Prueba vs Producción

### Modo de Prueba (TEST_MODE = true)

- ✅ Usa claves API de prueba
- ✅ No se realizan cargos reales
- ✅ Ideal para desarrollo y testing
- ❌ Los cargos no aparecen en tu cuenta bancaria

### Modo Producción (TEST_MODE = false)

- ⚠️ Usa claves API en vivo
- 💰 Se realizan cargos REALES
- 💳 Los fondos se depositan en tu cuenta
- ⚠️ **IMPORTANTE**: Solo activa esto cuando estés listo para cobros reales

## 🔐 Seguridad

### Mejores Prácticas

1. **Nunca compartas tus claves API**
   - Las claves secretas deben mantenerse privadas
   - No las subas a repositorios públicos
   - Usa variables de entorno en producción

2. **Usa .gitignore**
   ```
   config.ini
   *.db
   ```

3. **Rotar claves periódicamente**
   - Cambia tus claves API cada 3-6 meses
   - Inmediatamente si sospechas una filtración

4. **Monitoreo**
   - Revisa regularmente las transacciones
   - Configura alertas en tu pasarela de pago
   - Verifica logs del bot

## 🆘 Solución de Problemas

### Error: "Gateway configuration error"

**Causa**: Claves API incorrectas o faltantes

**Solución**:
1. Verifica que `GATEWAY_TYPE` esté correctamente escrito
2. Asegúrate de que `API_KEY` tenga el valor correcto
3. Verifica que la librería esté instalada (`pip install stripe`)

### Error: "Stripe library not installed"

**Solución**:
```bash
pip install stripe
```

### Cargos en modo simulación

Si ves el mensaje "Modo Simulación", significa que:
- `GATEWAY_TYPE` está vacío, O
- `API_KEY` está vacío

Para usar una pasarela real, configura ambos valores.

### Cargos declinados constantemente

**En modo prueba**:
- Verifica que uses tarjetas de prueba válidas
- Revisa que la fecha de expiración sea futura

**En modo producción**:
- El problema puede estar en la tarjeta del usuario
- Verifica los logs de tu pasarela de pago
- Revisa límites de tu cuenta

## 💡 Preguntas Frecuentes

### ¿Cuánto cuesta usar Stripe?

- **Por transacción**: ~2.9% + $0.30 USD
- **Sin cuota mensual** en el plan básico
- Consulta [precios de Stripe](https://stripe.com/pricing)

### ¿Puedo usar múltiples pasarelas?

Actualmente el bot soporta una pasarela a la vez. Para cambiar:
1. Modifica `GATEWAY_TYPE` en config.ini
2. Actualiza las credenciales API
3. Reinicia el bot

### ¿Los cargos son seguros?

Sí, cuando usas pasarelas oficiales como Stripe:
- ✅ Encriptación SSL/TLS
- ✅ Cumplimiento PCI-DSS
- ✅ Autenticación 3D Secure
- ✅ Protección contra fraude

### ¿Qué pasa si no configuro una pasarela?

El bot funcionará en **modo simulación**:
- Los comandos de cargo funcionarán
- Los resultados serán simulados (aleatorios)
- No se realizarán cargos reales
- Útil para demostración y pruebas

## 📞 Soporte

Si necesitas ayuda:

1. Revisa esta documentación
2. Consulta la documentación oficial de tu pasarela
3. Revisa los logs del bot para errores
4. Abre un issue en GitHub con detalles del problema

---

**Desarrollado con ❤️ para BatmanWL Bot**
