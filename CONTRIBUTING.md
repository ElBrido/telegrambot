# Contribuyendo a BatmanWL Bot

¡Gracias por considerar contribuir a BatmanWL Bot! 🦇

## ¿Cómo puedo contribuir?

### Reportar Bugs

Antes de crear un reporte de bug, verifica la lista de issues existentes. Cuando crees un reporte, incluye tantos detalles como sea posible:

* Usa un título claro y descriptivo
* Describe los pasos exactos para reproducir el problema
* Proporciona ejemplos específicos
* Describe el comportamiento que observaste
* Explica el comportamiento que esperabas ver
* Incluye capturas de pantalla si es posible
* Menciona tu versión de Python y sistema operativo

### Sugerir Mejoras

Las sugerencias de mejoras se rastrean como issues de GitHub. Al crear una sugerencia, incluye:

* Título claro y descriptivo
* Descripción paso a paso de la mejora sugerida
* Ejemplos específicos
* Descripción del comportamiento actual vs. esperado
* Explica por qué esta mejora sería útil

### Pull Requests

* Completa la plantilla requerida
* No incluyas números de issue en el título del PR
* Sigue la guía de estilo de Python (PEP 8)
* Incluye tests para nueva funcionalidad
* Actualiza la documentación según sea necesario
* Finaliza todos los archivos con una nueva línea

## Configuración de Desarrollo

1. Haz fork del repositorio
2. Clona tu fork: 
   ```bash
   git clone https://github.com/TU_USUARIO/telegrambot.git
   ```
3. Crea un entorno virtual:
   ```bash
   python3 -m venv venv
   ```
4. Activa el entorno virtual:
   ```bash
   source venv/bin/activate  # En Linux/Mac
   venv\Scripts\activate     # En Windows
   ```
5. Instala dependencias:
   ```bash
   pip install -r requirements.txt
   ```
6. Crea un archivo `config.ini` basado en `config.example.ini`
7. Haz tus cambios
8. Ejecuta tests:
   ```bash
   python3 test_bot.py
   ```
9. Haz commit de tus cambios con un mensaje claro
10. Haz push a tu fork y envía un pull request

## Guías de Estilo

### Mensajes de Commit Git

* Usa el tiempo presente ("Agrega feature" no "Agregó feature")
* Usa el modo imperativo ("Mover cursor a..." no "Mueve cursor a...")
* Limita la primera línea a 72 caracteres o menos
* Referencia issues y pull requests después de la primera línea
* Considera comenzar el mensaje con un emoji aplicable:
  * 🎨 `:art:` mejoras de formato/estructura
  * ⚡ `:zap:` mejoras de rendimiento
  * 🐛 `:bug:` corrección de bugs
  * ✨ `:sparkles:` nueva característica
  * 📝 `:memo:` documentación
  * 🔒 `:lock:` seguridad

### Guía de Estilo Python

* Sigue PEP 8
* Usa 4 espacios para indentación (no tabs)
* Usa docstrings para todas las clases y funciones públicas
* Mantén las líneas bajo 100 caracteres cuando sea posible
* Usa nombres de variables significativos
* Comenta código complejo
* Usa type hints cuando sea apropiado

Ejemplo:
```python
def check_card(card_number: str) -> dict:
    """
    Verifica una tarjeta usando el algoritmo Luhn.
    
    Args:
        card_number: Número de tarjeta a verificar
        
    Returns:
        dict: Resultado de la verificación con status y mensaje
    """
    # Tu código aquí
    pass
```

### Guía de Documentación

* Usa Markdown para documentación
* Mantén la documentación actualizada con los cambios de código
* Incluye ejemplos donde sea apropiado
* Usa emojis apropiados para mejor legibilidad
* Documenta tanto en español como en inglés cuando sea posible

## Testing

* Escribe tests para nueva funcionalidad
* Asegúrate de que todos los tests pasen antes de enviar un PR
* Apunta a alta cobertura de tests
* Usa nombres descriptivos para tests

Ejemplo de test:
```python
def test_card_validation():
    """Test que la validación Luhn funciona correctamente"""
    assert validate_card("4532015112830366") == True
    assert validate_card("1234567890123456") == False
```

## Áreas donde puedes contribuir

### 🐛 Corrección de Bugs
- Revisa los issues abiertos etiquetados como "bug"
- Reproduce el bug
- Identifica la causa
- Proporciona una corrección con tests

### ✨ Nuevas Características
- Comandos adicionales
- Mejoras en la interfaz de usuario
- Integraciones con APIs externas
- Mejoras de rendimiento

### 📝 Documentación
- Mejorar README
- Agregar más ejemplos
- Traducir documentación
- Crear tutoriales

### 🧪 Testing
- Agregar más tests
- Mejorar cobertura de tests
- Tests de integración
- Tests de rendimiento

### 🌍 Internacionalización
- Traducir mensajes del bot
- Agregar soporte multi-idioma
- Documentación en otros idiomas

## Código de Conducta

### Nuestras Promesas

* Ser respetuoso e inclusivo
* Dar la bienvenida a principiantes
* Enfocarse en lo mejor para la comunidad
- Mostrar empatía hacia otros miembros

### Comportamiento Inaceptable

* Lenguaje ofensivo o discriminatorio
* Acoso público o privado
* Publicar información privada de otros
* Conducta no profesional

## Proceso de Review

1. **Submit**: Envía tu PR con descripción clara
2. **Review**: Los mantenedores revisarán tu código
3. **Feedback**: Responde al feedback y haz cambios si es necesario
4. **Approval**: Una vez aprobado, será mergeado
5. **Thanks**: ¡Gracias por tu contribución!

## Preguntas Frecuentes para Contribuidores

### ¿Cómo encuentro algo en lo que trabajar?
- Revisa los issues abiertos
- Busca issues etiquetados como "good first issue"
- Pregunta en los issues si necesitas clarificación

### ¿Puedo trabajar en múltiples issues a la vez?
- Mejor enfocarte en uno a la vez
- Completa uno antes de comenzar otro
- Comunica si necesitas abandonar un issue

### ¿Cuánto tiempo toma el review?
- Dependiendo de la disponibilidad de los mantenedores
- Usualmente dentro de 1-2 semanas
- Puedes hacer ping amablemente si pasa más tiempo

### ¿Qué pasa si mi PR es rechazado?
- No te desanimes
- Aprende del feedback
- Puedes intentar con otra contribución

## Recursos Útiles

- [Python PEP 8](https://www.python.org/dev/peps/pep-0008/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot Documentation](https://docs.python-telegram-bot.org/)
- [Markdown Guide](https://www.markdownguide.org/)

## Contacto

¿Preguntas? Abre un issue o contacta a los mantenedores directamente.

---

¡Gracias por contribuir! 🙏🦇
