# 🚀 Guía de Despliegue - BatmanWL Bot

Esta guía cubre diferentes métodos para desplegar BatmanWL Bot en producción.

## 📋 Requisitos Previos

- Python 3.8 o superior
- Token de bot de Telegram (obtener de @BotFather)
- Servidor o computadora siempre encendida
- Conexión a Internet estable

---

## 🐳 Método 1: Docker (Recomendado)

### Ventajas
- Aislamiento completo
- Fácil de actualizar
- Consistente en diferentes sistemas
- Incluye todas las dependencias

### Pasos

1. **Instalar Docker**
   ```bash
   # En Ubuntu/Debian
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   
   # En otras distribuciones, ver: https://docs.docker.com/install/
   ```

2. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ElBrido/telegrambot.git
   cd telegrambot
   ```

3. **Configurar el bot**
   ```bash
   cp config.example.ini config.ini
   nano config.ini  # Edita con tu token y configuración
   ```

4. **Construir y ejecutar**
   ```bash
   docker-compose up -d
   ```

5. **Ver logs**
   ```bash
   docker-compose logs -f
   ```

6. **Detener el bot**
   ```bash
   docker-compose down
   ```

7. **Actualizar el bot**
   ```bash
   git pull
   docker-compose up -d --build
   ```

---

## 💻 Método 2: Linux VPS/Servidor

### Ventajas
- Control total del sistema
- Acceso directo a logs
- Fácil de debuggear

### En Ubuntu/Debian

1. **Actualizar sistema**
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

2. **Instalar Python y dependencias**
   ```bash
   sudo apt install python3 python3-pip python3-venv git -y
   ```

3. **Clonar repositorio**
   ```bash
   cd /opt
   sudo git clone https://github.com/ElBrido/telegrambot.git
   cd telegrambot
   ```

4. **Ejecutar instalación automática**
   ```bash
   sudo chmod +x install.sh
   ./install.sh
   ```

5. **Configurar el bot**
   ```bash
   nano config.ini
   # Agrega tu token y configuración
   ```

6. **Iniciar bot**
   ```bash
   chmod +x start.sh
   ./start.sh
   ```

### Mantener bot ejecutándose con systemd

1. **Crear archivo de servicio**
   ```bash
   sudo nano /etc/systemd/system/batmanwl-bot.service
   ```

2. **Agregar configuración**
   ```ini
   [Unit]
   Description=BatmanWL Telegram Bot
   After=network.target

   [Service]
   Type=simple
   User=tu_usuario
   WorkingDirectory=/opt/telegrambot
   ExecStart=/opt/telegrambot/venv/bin/python /opt/telegrambot/bot.py
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

3. **Habilitar y ejecutar servicio**
   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable batmanwl-bot
   sudo systemctl start batmanwl-bot
   ```

4. **Ver estado y logs**
   ```bash
   sudo systemctl status batmanwl-bot
   sudo journalctl -u batmanwl-bot -f
   ```

5. **Comandos útiles**
   ```bash
   sudo systemctl restart batmanwl-bot  # Reiniciar
   sudo systemctl stop batmanwl-bot     # Detener
   sudo systemctl disable batmanwl-bot  # Deshabilitar inicio automático
   ```

---

## 🪟 Método 3: Windows

### Despliegue Básico

1. **Instalar Python**
   - Descargar de https://www.python.org/downloads/
   - Marcar "Add Python to PATH" durante instalación

2. **Clonar repositorio**
   ```cmd
   git clone https://github.com/ElBrido/telegrambot.git
   cd telegrambot
   ```

3. **Crear entorno virtual**
   ```cmd
   python -m venv venv
   venv\Scripts\activate
   ```

4. **Instalar dependencias**
   ```cmd
   pip install -r requirements.txt
   ```

5. **Configurar**
   ```cmd
   copy config.example.ini config.ini
   notepad config.ini
   ```

6. **Ejecutar**
   ```cmd
   python bot.py
   ```

### Ejecutar como servicio (NSSM)

1. **Descargar NSSM**
   - https://nssm.cc/download

2. **Instalar como servicio**
   ```cmd
   nssm install BatmanWLBot "C:\ruta\a\telegrambot\venv\Scripts\python.exe" "C:\ruta\a\telegrambot\bot.py"
   nssm set BatmanWLBot AppDirectory "C:\ruta\a\telegrambot"
   nssm start BatmanWLBot
   ```

---

## ☁️ Método 4: Cloud Platforms

### Heroku

1. **Instalar Heroku CLI**
   ```bash
   curl https://cli-assets.heroku.com/install.sh | sh
   ```

2. **Login y crear app**
   ```bash
   heroku login
   heroku create batmanwl-bot
   ```

3. **Configurar variables**
   ```bash
   heroku config:set BOT_TOKEN=tu_token_aqui
   heroku config:set ADMIN_IDS=123456789
   heroku config:set OWNER_ID=123456789
   ```

4. **Crear Procfile**
   ```bash
   echo "worker: python bot.py" > Procfile
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

6. **Ver logs**
   ```bash
   heroku logs --tail
   ```

### Railway.app

1. **Conectar repositorio GitHub**
2. **Configurar variables de entorno**
3. **Deploy automático**

### DigitalOcean App Platform

1. **Conectar repositorio**
2. **Configurar build command**: `pip install -r requirements.txt`
3. **Configurar run command**: `python bot.py`
4. **Agregar variables de entorno**

---

## 🔧 Método 5: Process Manager (PM2)

### Ventajas
- Reinicio automático
- Logs integrados
- Fácil monitoreo
- Múltiples instancias

### Instalación

1. **Instalar Node.js y PM2**
   ```bash
   curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
   sudo apt install nodejs -y
   sudo npm install -g pm2
   ```

2. **Crear archivo ecosystem**
   ```bash
   nano ecosystem.config.js
   ```

   ```javascript
   module.exports = {
     apps: [{
       name: 'batmanwl-bot',
       script: '/opt/telegrambot/venv/bin/python',
       args: 'bot.py',
       cwd: '/opt/telegrambot',
       interpreter: 'none',
       autorestart: true,
       watch: false,
       max_memory_restart: '500M',
       env: {
         NODE_ENV: 'production'
       }
     }]
   }
   ```

3. **Iniciar con PM2**
   ```bash
   pm2 start ecosystem.config.js
   pm2 save
   pm2 startup
   ```

4. **Comandos PM2**
   ```bash
   pm2 status            # Ver estado
   pm2 logs batmanwl-bot # Ver logs
   pm2 restart all       # Reiniciar
   pm2 stop all          # Detener
   pm2 delete all        # Eliminar
   ```

---

## 📊 Monitoreo y Mantenimiento

### Logs

**Con systemd:**
```bash
sudo journalctl -u batmanwl-bot -f
```

**Con PM2:**
```bash
pm2 logs batmanwl-bot
```

**Con Docker:**
```bash
docker-compose logs -f
```

### Backup de Base de Datos

```bash
# Backup manual
cp batmanwl.db batmanwl_backup_$(date +%Y%m%d).db

# Backup automático diario (crontab)
0 0 * * * cp /opt/telegrambot/batmanwl.db /backup/batmanwl_$(date +\%Y\%m\%d).db
```

### Actualizar Bot

**Método Git:**
```bash
cd /opt/telegrambot
git pull
pip install -r requirements.txt --upgrade
sudo systemctl restart batmanwl-bot
```

**Con Docker:**
```bash
cd /opt/telegrambot
git pull
docker-compose up -d --build
```

---

## 🔒 Seguridad

### Firewall

```bash
# UFW (Ubuntu)
sudo ufw allow ssh
sudo ufw allow 443/tcp
sudo ufw enable
```

### Permisos de archivos

```bash
chmod 600 config.ini        # Solo propietario puede leer
chmod 600 batmanwl.db       # Proteger base de datos
```

### SSL/TLS (si usas webhooks)

```bash
# Certbot para certificado Let's Encrypt
sudo apt install certbot
sudo certbot certonly --standalone -d tudominio.com
```

---

## 🐛 Troubleshooting

### El bot no responde

1. **Verificar que está ejecutándose**
   ```bash
   ps aux | grep bot.py
   sudo systemctl status batmanwl-bot
   ```

2. **Revisar logs**
   ```bash
   sudo journalctl -u batmanwl-bot -n 50
   ```

3. **Verificar token**
   - Asegúrate de que el token en `config.ini` es correcto

4. **Verificar conectividad**
   ```bash
   curl https://api.telegram.org/bot<TOKEN>/getMe
   ```

### Errores de permisos

```bash
# Dar permisos al usuario
sudo chown -R $USER:$USER /opt/telegrambot
chmod +x install.sh start.sh
```

### Base de datos corrupta

```bash
# Restaurar desde backup
cp batmanwl_backup_YYYYMMDD.db batmanwl.db
```

### Alto uso de memoria

```bash
# Ver uso de recursos
htop
# O
top -p $(pgrep -f bot.py)
```

---

## 📈 Optimización

### Para alto tráfico

1. **Usar polling en lugar de webhooks**
   - Ya configurado por defecto en el bot

2. **Optimizar base de datos**
   ```bash
   sqlite3 batmanwl.db "VACUUM;"
   ```

3. **Limitar logs**
   ```bash
   # Rotar logs con logrotate
   sudo nano /etc/logrotate.d/batmanwl-bot
   ```

4. **Monitorear recursos**
   ```bash
   # Instalar htop
   sudo apt install htop
   htop
   ```

---

## 🎯 Checklist Pre-Producción

- [ ] Token de bot configurado
- [ ] Admin IDs configurados
- [ ] Owner ID configurado
- [ ] Base de datos creada
- [ ] Tests ejecutados y pasando
- [ ] Logs funcionando
- [ ] Backup automático configurado
- [ ] Servicio de reinicio automático (systemd/pm2)
- [ ] Firewall configurado
- [ ] Permisos de archivos verificados
- [ ] Documentación revisada
- [ ] Plan de monitoreo establecido

---

## 📚 Recursos Adicionales

- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Docs](https://docs.python-telegram-bot.org/)
- [Docker Docs](https://docs.docker.com/)
- [Systemd Documentation](https://www.freedesktop.org/software/systemd/man/)

---

¿Preguntas? Abre un issue en GitHub o contacta al mantenedor.

🦇 BatmanWL Bot - Desarrollado con ❤️ por ElBrido
