# TP3: Agentes con Múltiples CVs

## Descripción

Sistema de agentes que consulta múltiples currículums vitae usando RAG (Retrieval-Augmented Generation). El sistema incluye un nodo decisor que determina qué CV(s) consultar basado en la pregunta del usuario, herramientas RAG para buscar contexto relevante, y un agente principal que integra todo para generar respuestas.

## Arquitectura

El sistema está compuesto por los siguientes componentes:

1. **Nodo Decisor**: Analiza la pregunta y determina qué CV(s) usar
2. **Herramientas RAG**: Buscan contexto relevante en cada CV usando embeddings
3. **Agente Principal**: Integra decisión + contexto + LLM para generar respuesta
4. **Interfaz**: Streamlit para interactuar con el sistema

Ver `tp3_diagrama.md` para diagrama de flujo detallado.

## Estructura de Archivos

```
ClaseVII/codigo/
├── cvs/
│   ├── cv_alumno.txt      # CV de María González (alumno)
│   ├── cv_pedro.txt       # CV de Pedro Martínez
│   └── cv_ana.txt         # CV de Ana Rodríguez
├── tp3_cargar_cvs.py      # Script para cargar CVs a Pinecone
├── tp3_decisor.py         # Nodo decisor
├── tp3_rag_tools.py       # Herramientas RAG
├── tp3_agente.py          # Agente principal
├── tp3_interfaz.py        # Interfaz Streamlit
├── tp3_diagrama.md        # Diagrama de flujo
└── README_TP3.md          # Esta documentación
```

## Requisitos

### Dependencias

Instalar dependencias desde `requirements.txt`:

```bash
pip install -r requirements.txt
```

O instalar manualmente:

```bash
pip install pinecone sentence-transformers groq streamlit python-dotenv
```

### Variables de Entorno

Crear archivo `.env` en la raíz del proyecto con:

```env
PINECONE_API_KEY=tu_api_key_de_pinecone
PINECONE_ENVIRONMENT=us-east-1-aws
GROQ_API_KEY=tu_api_key_de_groq
```

**Nota**: Ver `.env.example` para formato.

### Cuentas Necesarias

1. **Pinecone**: 
   - Crear cuenta en https://www.pinecone.io/
   - Obtener API key (free tier disponible)
   - Notar el environment (ej: us-east-1-aws)

2. **Groq**:
   - Crear cuenta en https://console.groq.com/
   - Obtener API key (free tier disponible)

## Instalación y Configuración

### Paso 1: Configurar Variables de Entorno

1. Copiar `.env.example` a `.env`
2. Agregar tus API keys

### Paso 2: Cargar CVs a Pinecone

Ejecutar script para cargar todos los CVs:

```bash
cd CEIA-LLMIAG/ClaseVII/codigo
python tp3_cargar_cvs.py
```

Este script:
- Carga 3 CVs (alumno, pedro, ana)
- Crea 3 índices separados en Pinecone
- Genera embeddings y los carga

**Tiempo estimado**: 2-5 minutos

### Paso 3: Verificar que Todo Funciona

Probar componentes individualmente:

```bash
# Probar nodo decisor
python tp3_decisor.py

# Probar herramientas RAG
python tp3_rag_tools.py

# Probar agente completo
python tp3_agente.py
```

### Paso 4: Ejecutar Interfaz

```bash
streamlit run tp3_interfaz.py
```

La interfaz se abrirá en `http://localhost:8501`

## Uso

### Interfaz Web (Recomendado)

1. Ejecutar `streamlit run tp3_interfaz.py`
2. Hacer preguntas en el input
3. Ver respuestas y detalles del proceso

### Uso Programático

```python
from tp3_agente import AgenteCV

# Inicializar agente
agente = AgenteCV()

# Procesar query
resultado = agente.procesar_query("¿Cuál es mi experiencia en Python?")

print(resultado['respuesta'])
print(f"CVs usados: {resultado['cvs_usados']}")
```

## Ejemplos de Preguntas

### Preguntas Genéricas (CV del Alumno)

- "¿Cuál es mi experiencia en Python?"
- "¿Qué proyectos he realizado?"
- "¿Cuáles son mis habilidades técnicas?"
- "¿Dónde estudié?"

### Preguntas sobre Personas Específicas

- "¿Qué experiencia tiene Pedro en backend?"
- "¿Cuál es la experiencia de Ana en MLOps?"
- "¿Qué habilidades tiene María en NLP?"
- "¿Dónde trabaja Pedro?"

### Preguntas Comparativas

- "Compara las habilidades de Pedro y Ana en Python"
- "¿Quién tiene más experiencia en cloud?"
- "Compara la experiencia de María y Ana en machine learning"

## Componentes Detallados

### 1. Nodo Decisor (`tp3_decisor.py`)

**Clase**: `DecisorCV`

**Funcionalidad**:
- Analiza la query del usuario
- Detecta nombres de personas o contexto
- Decide qué CV(s) consultar

**Lógica de Decisión**:
- Query genérica → CV del alumno (María)
- Menciona nombre específico → CV de esa persona
- Múltiples nombres → Múltiples CVs

**Métodos principales**:
- `decidir(query)`: Retorna decisión sobre qué CVs usar
- `obtener_indices_pinecone(cvs)`: Obtiene nombres de índices

### 2. Herramientas RAG (`tp3_rag_tools.py`)

**Clases**:
- `RAGTool`: Herramienta RAG para un CV específico
- `RAGToolsManager`: Gestor de múltiples herramientas

**Funcionalidad**:
- Genera embeddings de queries
- Busca en Pinecone (índice específico)
- Retorna chunks relevantes

**Métodos principales**:
- `buscar_contexto(query, top_k)`: Busca y retorna contexto
- `buscar_contexto_detallado(query, top_k)`: Retorna información detallada

### 3. Agente Principal (`tp3_agente.py`)

**Clase**: `AgenteCV`

**Funcionalidad**:
- Integra nodo decisor + herramientas RAG + LLM
- Implementa patrón ReAct simplificado
- Genera respuestas basadas en contexto

**Flujo**:
1. Decisión (qué CV usar)
2. Búsqueda (contexto relevante)
3. Generación (respuesta con LLM)

**Métodos principales**:
- `procesar_query(query, top_k)`: Procesa query completa
- `procesar_query_con_detalles(query, top_k)`: Retorna información detallada

### 4. Interfaz (`tp3_interfaz.py`)

**Framework**: Streamlit

**Funcionalidades**:
- Input de preguntas
- Historial de conversación
- Mostrar detalles del proceso (opcional)
- Configuración de parámetros (top_k)

## Reglas Especiales

1. **Query genérica**: Responde como si fuera del alumno que presenta (María)
2. **Múltiples CVs**: Trae contexto de cada uno y responde de manera acorde
3. **Trabajo individual**: Aunque se trabaja en grupo, entrega es individual

## Troubleshooting

### Error: "PINECONE_API_KEY no está configurada"
- Verificar que existe archivo `.env`
- Verificar que tiene `PINECONE_API_KEY=...`
- Verificar que no hay espacios extra

### Error: "No se encontró el archivo cvs/cv_alumno.txt"
- Verificar que los CVs están en `ClaseVII/codigo/cvs/`
- Verificar nombres de archivos

### Error: "Index not found" en Pinecone
- Ejecutar `tp3_cargar_cvs.py` primero
- Verificar nombres de índices en el código

### Error: "GROQ_API_KEY no está configurada"
- Verificar que existe en `.env`
- Verificar formato correcto

### La interfaz no muestra respuestas
- Verificar que los índices de Pinecone tienen datos
- Verificar que las API keys son válidas
- Revisar logs en la terminal

## Mejoras Futuras

- [ ] Agregar más CVs del grupo
- [ ] Implementar razonamiento más complejo (múltiples iteraciones)
- [ ] Agregar evaluación de respuestas (RAGAS)
- [ ] Mejorar chunking semántico
- [ ] Agregar soporte para actualizar CVs dinámicamente

## Referencias

- **Clase VII**: Agentes, Fine-tuning y Profundización en RAG
- **Código de ejemplo**: `Agentes_desde_cero.ipynb`, `Agentes_Langchain.ipynb`
- **TP2**: Base para este trabajo práctico

## Autor

TP3 - Clase VII - CEIA LLMIAG
Procesamiento del Lenguaje Natural II - Maestría en IA - UBA

## Fecha de Entrega

Sábado 13 de diciembre de 2025

