# 🚀 Quick Start Guide - BatmanWL Bot

## Instalación Rápida (5 minutos)

### 1. Preparación

```bash
# Clona el repositorio
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
```

### 2. Obtén tu Token de Bot

1. Abre Telegram
2. Busca [@BotFather](https://t.me/BotFather)
3. Envía `/newbot`
4. Nombra tu bot (ej: "BatmanWL Test Bot")
5. Dale un username (ej: "batmanwl_test_bot")
6. **Copia el token** que te da (formato: `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### 3. Obtén tu User ID

1. Busca [@userinfobot](https://t.me/userinfobot)
2. Envía `/start`
3. **Copia tu ID** (ej: `123456789`)

### 4. Instalación Automática

```bash
# Ejecuta el instalador
./install.sh

# Edita la configuración
nano config.ini

# O usa cualquier editor de texto
vim config.ini
# code config.ini
```

### 5. Configuración Mínima

Edita `config.ini` y cambia:

```ini
[BOT]
TOKEN = TU_TOKEN_AQUI          # ← Pega el token de @BotFather
ADMIN_IDS = TU_USER_ID_AQUI    # ← Pega tu user ID
OWNER_ID = TU_USER_ID_AQUI     # ← Pega tu user ID

# El resto puedes dejarlo por defecto
```

### 6. Inicia el Bot

```bash
./start.sh
```

**¡Listo!** Ahora ve a Telegram y busca tu bot.

---

## Primeros Pasos en Telegram

### 1. Inicia el Bot

En Telegram, busca tu bot y envía:
```
/start
```

Verás el menú principal con un GIF de bienvenida.

### 2. Prueba Comandos Básicos

**Verificar una tarjeta:**
```
/ccn 4532015112830366
```

**Buscar información de BIN:**
```
/bin 453201
```

**Ver tu perfil:**
```
/stats
```

### 3. Genera Claves Premium (Como Admin)

```
/genkey 5
```

Esto generará 5 claves premium que podrás compartir.

### 4. Activa Premium

Copia una de las claves generadas y envía:
```
/key LA_CLAVE_AQUI
```

### 5. Genera Tarjetas (Con Premium)

```
/gen 453201 10
```

Esto generará 10 tarjetas válidas con el BIN 453201.

---

## Comandos con ".."

También puedes usar `..` en lugar de `/`:

```
..menu
..ccn 4532015112830366
..bin 453201
..gen 453201 10
```

---

## Solución de Problemas Comunes

### ❌ "No module named 'telegram'"

**Solución:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### ❌ "Error: Unauthorized"

**Problema:** Token incorrecto.

**Solución:**
1. Verifica que copiaste todo el token
2. Asegúrate de no tener espacios extra
3. El formato es: `123456789:ABC...`

### ❌ "No tienes permiso"

**Problema:** Tu user ID no está en ADMIN_IDS.

**Solución:**
1. Verifica tu ID con @userinfobot
2. Añádelo a config.ini
3. Reinicia el bot

### ❌ Bot no responde

**Solución:**
1. Verifica que el bot esté corriendo: `./start.sh`
2. Revisa los logs en la terminal
3. Envía `/start` en Telegram

---

## Comandos Útiles de Administración

```bash
# Iniciar el bot
./start.sh

# Detener el bot (Ctrl+C en la terminal)

# Ver logs en tiempo real
tail -f logs/bot.log  # (si configuraste logs)

# Backup de la base de datos
cp batmanwl.db backup_$(date +%Y%m%d).db

# Actualizar el bot
git pull
source venv/bin/activate
pip install -r requirements.txt --upgrade
```

---

## Siguientes Pasos

1. **Personaliza el GIF**: Cambia `GIF_URL` en config.ini
2. **Añade más admins**: Agrega más IDs en `ADMIN_IDS`
3. **Configura duración premium**: Cambia `KEY_DURATION_DAYS`
4. **Lee el README completo**: [README.md](README.md)

---

## Ayuda y Soporte

- 📖 [README Completo](README.md)
- 🐛 [Reportar un Bug](https://github.com/ElBrido/telegrambot/issues)
- 💬 [Discusiones](https://github.com/ElBrido/telegrambot/discussions)

---

**¡Disfruta tu bot BatmanWL! 🦇**
