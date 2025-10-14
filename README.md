# 🦇 BatmanWL - Telegram Bot Profesional

Bot profesional de Telegram para verificación de tarjetas de crédito, búsqueda de BIN y generación masiva de tarjetas.

## 🌟 Características

### Funcionalidades Principales
- ✅ **Verificación de Tarjetas (CCN Check)**: Verifica si una tarjeta está activa o inactiva usando algoritmo Luhn
- 💰 **Prueba de Cargo**: Simula cargo de $1.00 para verificar aprobación (Premium/Admin)
- 🔐 **Verificador VBV/3D Secure**: Verifica estado de Verified by Visa (Premium/Admin)
- 📊 **Estado de Tarjeta**: Verifica si está activa o inactiva con disponibilidad de saldo (Premium/Admin)
- 🔍 **Búsqueda de BIN**: Obtén información detallada sobre cualquier BIN (tipo, red, emisor, país)
- 💳 **Generación Masiva de Tarjetas**: Genera hasta 50 tarjetas válidas con un BIN específico (Premium)
- 🎭 **Sistema de Roles**: User/Admin/Owner con permisos diferenciados
- 🔑 **Sistema Premium**: Claves de acceso con duración configurable
- 📈 **Estadísticas Completas**: Seguimiento de verificaciones y estadísticas globales

### Interfaz y Usabilidad
- 🎬 **Panel de Inicio con GIF**: Bienvenida animada profesional personalizable
- 🔘 **Menú Interactivo**: Botones inline para fácil navegación
- 📝 **Comandos Flexibles**: Soporta comandos con `/`, `.` o `..`
- 💬 **Mensajes Formatados**: Respuestas claras con Markdown y emojis
- 🐳 **Docker Ready**: Despliegue fácil con Docker y docker-compose

### Comandos de Verificación
- `/ccn` o `.chk` - Verificación básica de tarjeta
- `/ch` - Prueba de cargo (Premium/Admin)
- `/vbv` - Verificador VBV/3D Secure (Premium/Admin)
- `/cardstatus` - Estado activo/inactivo (Premium/Admin)
- `/bin` - Búsqueda de información BIN

## 📦 Instalación

### Requisitos Previos
- Python 3.8 o superior
- pip3
- Cuenta de Telegram
- Token de Bot (obtenerlo de @BotFather)

### Instalación Automática

1. **Clona el repositorio:**
```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
```

2. **Ejecuta el instalador:**
```bash
./install.sh
```

3. **Configura el bot:**
   - Edita `config.ini` con tu información
   - Añade tu token de bot de Telegram
   - Configura IDs de administradores

4. **Inicia el bot:**
```bash
./start.sh
```

### Instalación Manual

1. **Crea un entorno virtual:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Instala dependencias:**
```bash
pip install -r requirements.txt
```

3. **Configura el bot:**
```bash
cp config.example.ini config.ini
# Edita config.ini con tu configuración
```

4. **Ejecuta el bot:**
```bash
python bot.py
```

### 🐳 Instalación con Docker (Recomendado para Producción)

1. **Instala Docker y Docker Compose**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

2. **Clona y configura:**
```bash
git clone https://github.com/ElBrido/telegrambot.git
cd telegrambot
cp config.example.ini config.ini
# Edita config.ini con tu configuración
```

3. **Ejecuta con Docker Compose:**
```bash
docker-compose up -d
```

4. **Ver logs:**
```bash
docker-compose logs -f
```

Ver **[DEPLOYMENT.md](DEPLOYMENT.md)** para más opciones de despliegue (VPS, Cloud, PM2, etc.)

## ⚙️ Configuración

### Obtener Token de Bot

1. Abre Telegram y busca [@BotFather](https://t.me/BotFather)
2. Envía `/newbot`
3. Sigue las instrucciones para nombrar tu bot
4. Copia el token que te proporciona
5. Pégalo en `config.ini`

### Archivo config.ini

```ini
[BOT]
TOKEN = TU_TOKEN_AQUI
ADMIN_IDS = 123456789,987654321
OWNER_ID = 123456789

[WELCOME]
GIF_URL = https://media.giphy.com/media/xTiTnGeUsWOEwsGoG4/giphy.gif
MESSAGE = 🦇 ¡Bienvenido a BatmanWL Bot! 🦇

[PREMIUM]
KEY_DURATION_DAYS = 30

[DATABASE]
DB_NAME = batmanwl.db
```

### Configuración de Roles

- **OWNER_ID**: ID del propietario del bot (máximos privilegios)
- **ADMIN_IDS**: Lista de IDs de administradores separados por comas

Para obtener tu ID de Telegram, puedes usar [@userinfobot](https://t.me/userinfobot)

## 🎮 Uso

### Comandos Básicos

| Comando | Alternativa | Descripción |
|---------|-------------|-------------|
| `/start` | - | Inicia el bot y muestra el menú principal |
| `/menu` | `..menu` | Muestra el menú principal |
| `/help` | `..help` | Muestra la ayuda |

### Comandos de Verificación

| Comando | Alternativa | Descripción | Ejemplo |
|---------|-------------|-------------|---------|
| `/ccn <tarjeta>` | `.chk <tarjeta>` | Verifica una tarjeta | `/ccn 4532015112830366\|12\|25\|123` |
| `/bin <bin>` | `.bin <bin>` | Busca información de BIN | `/bin 453201` |

### Comandos Avanzados (Premium/Admin)

| Comando | Alternativa | Descripción | Ejemplo |
|---------|-------------|-------------|---------|
| `/ch <tarjeta>` | `.ch <tarjeta>` | Prueba de cargo | `/ch 4532015112830366\|12\|25\|123` |
| `/vbv <tarjeta>` | `.vbv <tarjeta>` | Verificador VBV/3D Secure | `/vbv 4532015112830366\|12\|25\|123` |
| `/cardstatus <tarjeta>` | `.cardstatus <tarjeta>` | Estado activa/inactiva | `/cardstatus 4532015112830366\|12\|25\|123` |

### Comandos Premium

| Comando | Alternativa | Descripción | Ejemplo |
|---------|-------------|-------------|---------|
| `/gen <bin> [cant]` | `..gen <bin> [cant]` | Genera tarjetas (Premium) | `/gen 453201 10` |
| `/key <clave>` | `..key <clave>` | Activa clave premium | `/key ABC123XYZ` |
| `/stats` | `..stats` | Muestra tus estadísticas | `/stats` |

### Comandos de Administración

| Comando | Descripción | Ejemplo |
|---------|-------------|---------|
| `/genkey [cant]` | Genera claves premium (Admin) | `/genkey 5` |

## 🔐 Sistema Premium

El sistema premium permite acceso a funciones avanzadas:

- **Generación masiva de tarjetas**
- **Límites más altos de verificaciones**
- **Acceso prioritario a nuevas funciones**

### Activar Premium

1. Obtén una clave premium de un administrador
2. Usa el comando: `/key TU_CLAVE_AQUI`
3. La clave se activará por el período configurado (default: 30 días)

### Generar Claves (Solo Admin)

```bash
/genkey 5  # Genera 5 claves premium
```

## 📊 Base de Datos

El bot utiliza SQLite para almacenar:
- **Usuarios**: ID, username, rol, fecha de registro
- **Claves Premium**: Código, usuario, fechas de activación/expiración
- **Historial de Verificaciones**: Tarjetas verificadas por usuario

### Backup

Para hacer backup de la base de datos:
```bash
cp batmanwl.db batmanwl_backup_$(date +%Y%m%d).db
```

## 🏗️ Arquitectura

```
telegrambot/
├── bot.py              # Bot principal con comandos
├── database.py         # Gestión de base de datos
├── card_utils.py       # Utilidades de tarjetas
├── config.ini          # Configuración (no incluido)
├── config.example.ini  # Ejemplo de configuración
├── requirements.txt    # Dependencias Python
├── install.sh          # Script de instalación
├── start.sh           # Script de inicio
├── .gitignore         # Archivos ignorados por git
└── README.md          # Este archivo
```

## 🔧 Desarrollo

### Estructura de Módulos

#### bot.py
Módulo principal que maneja:
- Comandos de Telegram
- Handlers de botones
- Lógica de negocio
- Integración con otros módulos

#### database.py
Gestión de base de datos:
- CRUD de usuarios
- Sistema de roles
- Claves premium
- Historial de operaciones

#### card_utils.py
Utilidades de tarjetas:
- Validación Luhn
- Generación de tarjetas
- Lookup de BIN
- Simulación de verificación CCN

### Agregar Nuevas Funciones

1. Define el comando en `bot.py`
2. Añade el handler correspondiente
3. Actualiza la ayuda y menús
4. Documenta en el README

### Testing

Para probar el bot localmente:
```bash
# Activa el entorno virtual
source venv/bin/activate

# Ejecuta el bot
python bot.py
```

## 📚 Documentación Completa

Este proyecto incluye documentación extensa para facilitar el uso y desarrollo:

- 📖 **[README.md](README.md)** - Este archivo, guía principal
- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Inicio rápido en 5 minutos
- 📋 **[COMMANDS.md](COMMANDS.md)** - Referencia completa de comandos
- ❓ **[FAQ.md](FAQ.md)** - Preguntas frecuentes
- 🚀 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Guías de despliegue (Docker, VPS, Cloud)
- 🏗️ **[ARCHITECTURE.md](ARCHITECTURE.md)** - Arquitectura y diseño del sistema
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Historial de cambios
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Guía para contribuidores
- 📊 **[IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md)** - Resumen de implementación
- 📸 **[EXAMPLES.md](EXAMPLES.md)** - Ejemplos de uso

## 🤝 Contribución

Las contribuciones son bienvenidas. Por favor lee **[CONTRIBUTING.md](CONTRIBUTING.md)** para más detalles.

Resumen rápido:
1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto es de código abierto y está disponible bajo la licencia MIT.

## ⚠️ Disclaimer

Este bot es solo para fines educativos y de demostración. No debe utilizarse para actividades ilegales. La verificación de tarjetas es simulada y no realiza verificaciones reales contra sistemas de pago.

## 📧 Soporte

Si tienes problemas o preguntas:
1. Revisa la documentación
2. Verifica tu configuración
3. Abre un issue en GitHub

## 🎯 Roadmap

- [ ] Integración con APIs reales de verificación
- [ ] Sistema de logs más robusto
- [ ] Panel web de administración
- [ ] Múltiples idiomas
- [ ] Sistema de notificaciones
- [ ] Exportación de datos
- [ ] Más métodos de pago para premium

---

Desarrollado con ❤️ por ElBrido