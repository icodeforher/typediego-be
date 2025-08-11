# Guía de Uso del API

## Configuración de Autenticación

El API utiliza autenticación por API Key para proteger los endpoints.

### Headers Requeridos

```
X-API-KEY: tu-api-key-aqui
Content-Type: application/json
```

## Endpoints Disponibles

### 1. Chat - `/api/chat`

**Método:** POST  
**Autenticación:** Requerida (X-API-KEY)  
**Descripción:** Endpoint principal para hacer preguntas al chatbot

#### Request Body

```json
{
  "question": "¿Tienes experiencia con Python?"
}
```

#### Response (Streaming)

El endpoint retorna una respuesta en streaming formato Server-Sent Events:

```
data: {"content": "Sí, tengo", "type": "chunk"}

data: {"content": " experiencia con Python...", "type": "chunk"}

data: {"content": "", "type": "done"}
```

#### Ejemplo con JavaScript

```javascript
const response = await fetch("https://tu-app.onrender.com/api/chat", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-API-KEY": "tu-api-key",
  },
  body: JSON.stringify({
    question: "¿Tienes experiencia con React?",
  }),
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
        console.log(data.content);
      } else if (data.type === "done") {
        console.log("Respuesta completa");
      }
    }
  }
}
```

#### Ejemplo con cURL

```bash
curl -X POST https://tu-app.onrender.com/api/chat \
  -H "Content-Type: application/json" \
  -H "X-API-KEY: tu-api-key" \
  -d '{"question": "¿Cuál es tu experiencia laboral?"}'
```

### 2. Health Check - `/api/health`

**Método:** GET  
**Autenticación:** No requerida  
**Descripción:** Verifica el estado del servicio

#### Response

```json
{
  "status": "healthy",
  "message": "Chatbot está funcionando correctamente",
  "documents_loaded": true
}
```

## Códigos de Error

### 401 - Unauthorized

```json
{
  "error": "API Key requerida",
  "message": "Debe proporcionar una API key en el header X-API-KEY"
}
```

### 403 - Forbidden

```json
{
  "error": "API Key inválida",
  "message": "La API key proporcionada no es válida"
}
```

### 400 - Bad Request

```json
{
  "error": "Pregunta requerida",
  "message": "Debe proporcionar una pregunta en el campo 'question'"
}
```

### 500 - Internal Server Error

```json
{
  "error": "Configuración incompleta",
  "message": "No se encontraron documentos para procesar"
}
```

## CORS

El API está configurado para aceptar requests desde:

- `https://typediego.com`
- `http://localhost:3000`

## Límites y Consideraciones

- **Rate Limiting:** No implementado actualmente
- **Tamaño máximo de pregunta:** Sin límite específico
- **Timeout:** 120 segundos por request
- **Streaming:** Las respuestas se envían en chunks para mejor UX

## Ejemplo de Integración Completa

```javascript
class ChatbotAPI {
  constructor(apiKey, baseUrl) {
    this.apiKey = apiKey;
    this.baseUrl = baseUrl;
  }

  async ask(question, onChunk = null) {
    const response = await fetch(`${this.baseUrl}/api/chat`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-API-KEY": this.apiKey,
      },
      body: JSON.stringify({ question }),
    });

    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.message);
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let fullResponse = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value);
      const lines = chunk.split("\n");

      for (const line of lines) {
        if (line.startsWith("data: ")) {
          const data = JSON.parse(line.slice(6));
          if (data.type === "chunk") {
            fullResponse += data.content;
            if (onChunk) onChunk(data.content);
          } else if (data.type === "done") {
            return fullResponse;
          } else if (data.type === "error") {
            throw new Error(data.content);
          }
        }
      }
    }

    return fullResponse;
  }

  async healthCheck() {
    const response = await fetch(`${this.baseUrl}/api/health`);
    return await response.json();
  }
}

// Uso
const chatbot = new ChatbotAPI("tu-api-key", "https://tu-app.onrender.com");

// Con streaming
await chatbot.ask("¿Tienes experiencia con JavaScript?", (chunk) => {
  console.log("Chunk recibido:", chunk);
});

// Health check
const health = await chatbot.healthCheck();
console.log("Estado del servicio:", health);
```
