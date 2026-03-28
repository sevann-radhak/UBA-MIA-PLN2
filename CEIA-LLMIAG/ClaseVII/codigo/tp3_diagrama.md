# TP3 - Diagrama de Flujo del Sistema

## Arquitectura General

```
┌─────────────────────────────────────────────────────────────┐
│                    USUARIO                                   │
│              (Pregunta sobre CVs)                            │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              NODO DECISOR (DecisorCV)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1. Analiza query                                      │  │
│  │ 2. Detecta nombres o contexto                        │  │
│  │ 3. Decide qué CV(s) usar                              │  │
│  │    - Query genérica → CV del alumno                  │  │
│  │    - Menciona nombre → CV específico                 │  │
│  │    - Múltiples nombres → Múltiples CVs               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
         ┌───────────┴───────────┐
         │                       │
         ▼                       ▼
┌─────────────────┐     ┌─────────────────┐
│  CV Alumno      │     │  CV Pedro/Ana   │
│  (María)        │     │  (Otros)        │
└────────┬────────┘     └────────┬─────────┘
         │                       │
         └───────────┬───────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│         HERRAMIENTAS RAG (RAGToolsManager)                 │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ Para cada CV seleccionado:                           │  │
│  │ 1. Generar embedding de la query                     │  │
│  │ 2. Buscar en Pinecone (índice específico)           │  │
│  │ 3. Recuperar top-k chunks más relevantes             │  │
│  │ 4. Retornar contexto concatenado                     │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           AGENTE PRINCIPAL (AgenteCV)                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │ 1. Recibe decisión + contextos                      │  │
│  │ 2. Construye prompt con contexto                     │  │
│  │ 3. Genera respuesta usando LLM (Groq)                │  │
│  │ 4. Retorna respuesta final                          │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              RESPUESTA FINAL                                 │
│         (Mostrada al usuario)                               │
└─────────────────────────────────────────────────────────────┘
```

## Flujo Detallado por Tipo de Query

### Query Genérica (Ej: "¿Cuál es mi experiencia?")

```
Query: "¿Cuál es mi experiencia en Python?"
    ↓
Nodo Decisor:
  - No detecta nombres específicos
  - Decisión: usar CV del alumno (María)
    ↓
RAG Tool (CV Alumno):
  - Busca en índice "cv-alumno-tp3"
  - Retorna chunks sobre experiencia en Python
    ↓
Agente:
  - Construye prompt: "Responde como si fueras María González..."
  - Genera respuesta con contexto
    ↓
Respuesta: "María tiene 6 años de experiencia en Python..."
```

### Query con Nombre Específico (Ej: "¿Qué habilidades tiene Pedro?")

```
Query: "¿Qué habilidades tiene Pedro?"
    ↓
Nodo Decisor:
  - Detecta "Pedro" en query
  - Decisión: usar CV de Pedro
    ↓
RAG Tool (CV Pedro):
  - Busca en índice "cv-pedro-tp3"
  - Retorna chunks sobre habilidades
    ↓
Agente:
  - Construye prompt con contexto de Pedro
  - Genera respuesta
    ↓
Respuesta: "Pedro tiene habilidades en Python, Java, Go..."
```

### Query Comparativa (Ej: "Compara habilidades de Pedro y Ana")

```
Query: "Compara las habilidades de Pedro y Ana en Python"
    ↓
Nodo Decisor:
  - Detecta "Pedro" y "Ana"
  - Decisión: usar ambos CVs
    ↓
RAG Tools (CV Pedro + CV Ana):
  - Busca en "cv-pedro-tp3" → contexto sobre Python
  - Busca en "cv-ana-tp3" → contexto sobre Python
    ↓
Agente:
  - Construye prompt con ambos contextos
  - Instrucción: "Compara información de Pedro y Ana"
  - Genera respuesta comparativa
    ↓
Respuesta: "Pedro tiene 6 años de experiencia en Python...
            Ana tiene 6 años de experiencia en Python...
            Ambos tienen experiencia avanzada..."
```

## Componentes del Sistema

### 1. Nodo Decisor (`tp3_decisor.py`)
- **Clase**: `DecisorCV`
- **Método principal**: `decidir(query)`
- **Lógica**:
  - Detección simple por nombres/alias
  - Análisis con LLM si no detecta nombres
  - Default: CV del alumno

### 2. Herramientas RAG (`tp3_rag_tools.py`)
- **Clase**: `RAGTool` (una por CV)
- **Clase**: `RAGToolsManager` (gestor de todas)
- **Método principal**: `buscar_contexto(query, top_k)`
- **Funcionalidad**:
  - Genera embeddings de query
  - Busca en Pinecone (índice específico)
  - Retorna chunks relevantes

### 3. Agente Principal (`tp3_agente.py`)
- **Clase**: `AgenteCV`
- **Método principal**: `procesar_query(query)`
- **Flujo ReAct simplificado**:
  1. Decisión (qué CV usar)
  2. Búsqueda (contexto relevante)
  3. Generación (respuesta con LLM)

### 4. Interfaz (`tp3_interfaz.py`)
- **Framework**: Streamlit
- **Funcionalidades**:
  - Input de preguntas
  - Historial de conversación
  - Mostrar detalles del proceso
  - Configuración de parámetros

## Bases de Datos Vectoriales

### Índices en Pinecone
- `cv-alumno-tp3`: CV de María González (alumno)
- `cv-pedro-tp3`: CV de Pedro Martínez
- `cv-ana-tp3`: CV de Ana Rodríguez

### Estructura de Vectores
```json
{
  "id": "chunk_0001",
  "values": [0.123, -0.456, ...],  // 384 dimensiones
  "metadata": {
    "texto": "Experiencia en Python...",
    "chunk_numero": 1,
    "longitud": 250,
    "persona": "María González"
  }
}
```

## Flujo de Datos

```
1. Usuario → Query
2. Decisor → Análisis → CVs a consultar
3. RAG Tools → Embeddings → Pinecone → Chunks
4. Agente → Prompt (query + contextos) → LLM → Respuesta
5. Interfaz → Muestra respuesta al usuario
```

## Casos Especiales

### Query sin información en CVs
- Agente responde: "No tengo esa información en los CVs disponibles"

### Múltiples CVs con información relevante
- Agente integra información de todos los CVs consultados
- Puede comparar o sintetizar según el tipo de pregunta

### Error en búsqueda
- Sistema maneja errores gracefully
- Muestra mensaje de error al usuario
- Sugiere verificar índices de Pinecone



