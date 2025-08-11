# Guía de Despliegue en Render.com

## Pasos para desplegar tu chatbot CV en Render.com (GRATIS)

### 1. Preparación del repositorio

- Asegúrate de que tu código esté en un repositorio de GitHub o GitLab
- Los archivos `Dockerfile`, `.dockerignore` y `render.yaml` ya están configurados

### 2. Crear cuenta en Render.com

1. Ve a [render.com](https://render.com)
2. Regístrate con tu cuenta de GitHub/GitLab (es gratis)
3. No necesitas tarjeta de crédito para el plan gratuito

### 3. Crear nuevo Web Service

1. En el dashboard de Render, haz clic en "New +"
2. Selecciona "Web Service"
3. Conecta tu repositorio de GitHub/GitLab
4. Selecciona el repositorio de tu chatbot

### 4. Configuración del servicio

Render detectará automáticamente el `render.yaml` y configurará:

- **Name**: chatbot-cv
- **Environment**: Docker
- **Plan**: Free
- **Build Command**: Automático (usa Dockerfile)
- **Start Command**: Automático (desde Dockerfile)

### 5. Variables de entorno

**IMPORTANTE**: Debes configurar estas variables de entorno:

1. En la configuración del servicio, ve a "Environment"
2. Añade las siguientes variables:
   - `OPENAI_API_KEY`: Tu clave de OpenAI (obtener en platform.openai.com)
   - `API_KEYS`: Claves para acceder a tu API separadas por comas (ej: `mi-key-secreta,otra-key`)
3. Las demás variables ya están configuradas en render.yaml

**Ejemplo de configuración:**

```
OPENAI_API_KEY=sk-proj-abc123...
API_KEYS=my-secret-key-2024,backup-key-dev
```

### 6. Desplegar

1. Haz clic en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. El proceso toma entre 5-10 minutos la primera vez
4. Una vez completado, tendrás una URL pública como: `https://chatbot-cv-xxxx.onrender.com`

### 7. Limitaciones del plan gratuito

- La aplicación se "duerme" después de 15 minutos de inactividad
- Tarda ~30 segundos en "despertar" cuando recibe una nueva solicitud
- 750 horas de uso por mes (suficiente para uso personal)

### 8. Actualizaciones automáticas

- Cada vez que hagas push a tu repositorio, Render desplegará automáticamente
- Puedes ver los logs de despliegue en tiempo real

### 9. Monitoreo

- Render proporciona logs en tiempo real
- Métricas básicas de uso
- Alertas por email si hay problemas

## Archivos de configuración incluidos:

- **Dockerfile**: Conteneriza la aplicación Flask
- **.dockerignore**: Excluye archivos innecesarios del contenedor
- **render.yaml**: Configuración específica para Render.com

¡Tu chatbot estará disponible 24/7 de forma gratuita!
