# Chatbot de Experiencia Laboral

Un chatbot inteligente desarrollado con Flask y LangChain que responde preguntas sobre experiencia laboral basándose en documentos PDF (CV) y archivos de texto con información adicional.

## Características

- 🤖 **Chatbot inteligente**: Utiliza OpenAI GPT-3.5-turbo para generar respuestas precisas
- 📄 **Procesamiento de documentos**: Lee y procesa archivos PDF (CV) y TXT (experiencia)
- 🔒 **Autenticación por token**: Protege el endpoint con autenticación basada en tokens
- 🌊 **Respuestas en streaming**: Las respuestas se generan y envían en tiempo real
- 🎯 **Sin alucinaciones**: Solo responde basándose en la información de los documentos
- 🔍 **Búsqueda semántica**: Utiliza embeddings y FAISS para encontrar información relevante

## Estructura del Proyecto

```
├── app/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── document_processor.py
│   │   └── chatbot_service.py
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chatbot.py
│   └── utils/
│       ├── __init__.py
│       └── auth.py
├── data/
│   ├── cv.pdf (tu CV en formato PDF)
│   └── experience.txt (información adicional sobre tu experiencia)
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## Instalación

1. **Clona el repositorio**:

```bash
git clone <repository-url>
cd chatbot-experiencia
```

2. **Crea un entorno virtual**:

```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instala las dependencias**:

```bash
pip install -r requirements.txt
```

4. **Configura las variables de entorno**:

```bash
cp .env.example .env
```

Edita el archivo `.env` con tus valores:

```env
OPENAI_API_KEY=tu_api_key_de_openai
AUTH_TOKEN=tu_token_secreto_para_autenticacion
FLASK_ENV=development
FLASK_DEBUG=True
```

5. **Prepara los documentos**:
   - Coloca tu CV en formato PDF como `data/cv.pdf`
   - Crea un archivo `data/experience.txt` con información adicional sobre tu experiencia

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

La aplicación estará disponible en `http://localhost:5000`

### Endpoints disponibles

#### 1. Chat (POST /api/chat)

Endpoint principal para hacer preguntas al chatbot.

**Headers requeridos:**

```
Authorization: Bearer tu_token_secreto
Content-Type: application/json
```

**Body:**

```json
{
  "question": "¿Cuál es tu experiencia con Python?"
}
```

**Respuesta:**
La respuesta se envía como stream de texto plano con chunks en formato JSON:

```
data: {"content": "Tengo", "type": "chunk"}
data: {"content": " experiencia", "type": "chunk"}
data: {"content": " con Python...", "type": "chunk"}
data: {"content": "", "type": "done"}
```

#### 2. Health Check (GET /api/health)

Verifica el estado del chatbot y si los documentos están cargados.

**Respuesta:**

```json
{
  "status": "healthy",
  "message": "Chatbot está funcionando correctamente",
  "documents_loaded": true
}
```

### Ejemplo de uso con curl

```bash
# Health check
curl -X GET http://localhost:5000/api/health

# Chat
curl -X POST http://localhost:5000/api/chat \
  -H "Authorization: Bearer tu_token_secreto" \
  -H "Content-Type: application/json" \
  -d '{"question": "¿Cuáles son tus principales habilidades técnicas?"}'
```

### Ejemplo de uso con JavaScript (Frontend)

```javascript
async function askChatbot(question) {
  const response = await fetch("/api/chat", {
    method: "POST",
    headers: {
      Authorization: "Bearer tu_token_secreto",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question }),
  });

  const reader = response.body.getReader();
  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    const chunk = decoder.decode(value);
    const lines = chunk.split("\n");

    for (const line of lines) {
      if (line.startsWith("data: ")) {
        const data = JSON.parse(line.slice(6));
        if (data.type === "chunk") {
          // Mostrar el chunk en la UI
          console.log(data.content);
        } else if (data.type === "done") {
          // Respuesta completa
          break;
        }
      }
    }
  }
}
```

## Configuración de Documentos

### CV (data/cv.pdf)

- Debe ser un archivo PDF válido
- Contiene tu currículum vitae con experiencia profesional, educación, habilidades, etc.

### Experiencia adicional (data/experience.txt)

Archivo de texto con información adicional como:

- Metodologías de trabajo preferidas
- Filosofía de desarrollo
- Experiencias específicas no detalladas en el CV
- Formas de resolver problemas
- Preferencias tecnológicas

Ejemplo de contenido para `experience.txt`:

```
Metodología de trabajo:
- Prefiero trabajar con metodologías ágiles como Scrum
- Me gusta el desarrollo iterativo y la retroalimentación constante
- Valoro mucho la comunicación clara y la documentación

Filosofía de desarrollo:
- Creo en el código limpio y mantenible
- Prefiero la simplicidad sobre la complejidad
- Me enfoco en la experiencia del usuario final

Resolución de problemas:
- Analizo el problema desde diferentes ángulos
- Busco soluciones simples y eficientes
- Me gusta investigar y aprender nuevas tecnologías cuando es necesario
```

## Seguridad

- **Autenticación por token**: Todos los endpoints están protegidos
- **Validación de entrada**: Se validan todas las entradas del usuario
- **Control de errores**: Manejo robusto de errores sin exponer información sensible
- **CORS configurado**: Para permitir acceso desde frontends específicos

## Desarrollo

### Estructura de código

- **app/core/**: Configuración y settings
- **app/services/**: Lógica de negocio (procesamiento de documentos, chatbot)
- **app/routes/**: Endpoints de la API
- **app/utils/**: Utilidades (autenticación, helpers)

### Agregar nuevas funcionalidades

1. **Nuevos endpoints**: Agregar en `app/routes/`
2. **Nueva lógica de negocio**: Agregar en `app/services/`
3. **Nuevas utilidades**: Agregar en `app/utils/`

## Troubleshooting

### Error: "No documents found"

- Verifica que existan los archivos `data/cv.pdf` y `data/experience.txt`
- Asegúrate de que el PDF no esté corrupto

### Error: "OpenAI API key not found"

- Verifica que `OPENAI_API_KEY` esté configurado en el archivo `.env`
- Asegúrate de que la API key sea válida

### Error: "Token de autorización inválido"

- Verifica que el header `Authorization` esté presente
- Asegúrate de que el token coincida con `AUTH_TOKEN` en `.env`

## Licencia

Este proyecto está bajo la licencia MIT.
