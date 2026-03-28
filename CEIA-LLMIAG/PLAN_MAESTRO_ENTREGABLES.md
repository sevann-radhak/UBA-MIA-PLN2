# 📋 Plan Maestro: Entregables Finales - PLN II
## Guía Completa para Finalizar la Materia

> **Objetivo**: Completar todos los trabajos prácticos requeridos para finalizar la materia  
> **Estado Actual**: Análisis completo de TP1, TP2, TP3  
> **Última actualización**: Diciembre 2025

---

## 🎯 RESUMEN EJECUTIVO

### Estado de Trabajos Prácticos

| TP | Tema | Estado | Fecha Entrega | Prioridad |
|---|---|---|---|---|
| **TP1** | TinyGPT (Preentrenamiento) | ❌ No implementado | ⚠️ Pasada (antes Clase 7) | 🔴 Baja* |
| **TP2** | Chatbot RAG con CVs | ✅ Implementado | 📅 **Sábado 13 dic 2025** | 🟢 Alta |
| **TP3** | Agentes con Múltiples CVs | 🟡 En desarrollo | 📅 **Sábado 13 dic 2025** | 🟢 Alta |

*Nota: TP1 ya pasó su fecha, consultar con docentes si es necesario entregarlo.

### Entregables Pendientes

1. **TP2**: Completar entrega (video, links al formulario)
2. **TP3**: Completar implementación y entrega
3. **Verificar**: Si TP1 es necesario o no (fecha pasada)

---

## 📚 RECAPITULACIÓN COMPLETA DE TRABAJOS PRÁCTICOS

### **TP1: Preentrenamiento de GPT (TinyGPT)**

#### 📋 Consigna Original

**Asociado a**: Clases II y IV  
**Notebook base**: `ClaseIV/TinyGPT.ipynb`

**Tareas requeridas:**

1. **Tarea 1 - Inferencia (Técnicas de Sampling)**
   - Implementar **greedy decoding** (token con mayor probabilidad)
   - Implementar **temperature sampling** (control de aleatoriedad)
   - Implementar **top-k sampling** (considerar solo k tokens más probables)
   - Implementar **top-p (nucleus) sampling** (tokens hasta acumular probabilidad p)

2. **Tarea 2 - Arquitectura (Mixture of Experts)**
   - Transformar TinyGPT a **MoE (Mixture of Experts)**
   - Implementar MoE con al menos 2 expertos
   - Comparar con versión vanilla
   - Visualizar atención en ambas versiones

#### ✅ Entregable Esperado

- Notebook completado con implementaciones
- Comparativas de generación (greedy vs sampling)
- Visualizaciones de atención (vanilla vs MoE)
- Conclusiones y hallazgos

#### 📅 Fechas

- **Entrega original**: Antes de Clase 7
- **Estado**: ⚠️ Fecha pasada
- **Tiempo disponible original**: ~1 mes y medio desde Clase 2

#### ⚠️ Información Crítica

**Problemas esperados (NO es error del estudiante):**
- Resultados de baja calidad son **esperados** debido a:
  - Dataset pequeño (Shakespeare insuficiente)
  - Tokenizer primitivo (basado en caracteres)
  - Modelo pequeño (pocos parámetros)
  - 50 épocas no mejoran significativamente (problema arquitectural)

**Mejoras recomendadas:**
1. Tokenizer robusto: Usar tokenizer preentrenado (ej: Llama 3 tokenizer)
2. Optimizadores de memoria: Bits and Bytes (8-bit Adam), Galore
3. Dataset más diverso: WebText open source
4. Escalar arquitectura: Más parámetros, más capas

**Observaciones:**
- Greedy decoding se atasca en una palabra (esperado)
- Otros métodos (temperature, top-k, top-p) funcionan mejor
- MoE es ~8x más lento en entrenamiento

#### 🔍 Estado Actual

- ❌ **No implementado** en el repositorio
- ⚠️ **Fecha de entrega pasada**
- ❓ **Acción requerida**: Consultar con docentes si es necesario entregarlo

---

### **TP2: Chatbot con RAG usando CVs**

#### 📋 Consigna Original

**Asociado a**: Clase VI (RAG, Vector DBs)  
**Objetivo**: Implementar chatbot que usa RAG con currículum vitae como fuente

#### ✅ Entregable Esperado

- ✅ Chatbot funcional con interfaz visual (Streamlit u otro)
- ✅ Video de captura de pantalla (OBS u otro software gratuito)
- ✅ Repositorio con código (mínimo 2 scripts)
- ✅ Links al formulario de entrega

#### 📝 Scripts Requeridos

**Script 1: `tp2_cargar_cv.py`**
```python
# Funcionalidades:
# 1. Cargar currículum desde archivo
# 2. Chunking (dividir texto en fragmentos)
# 3. Generar embeddings (Sentence Transformers)
# 4. Subir vectores a base de datos vectorial (Pinecone)
```

**Script 2: `tp2_chatbot.py`**
```python
# Funcionalidades:
# 1. Cargar modelo LLM (Groq u otro)
# 2. Conectar con base de datos vectorial
# 3. Implementar interfaz (Streamlit)
# 4. Gestionar historial de conversación
# 5. RAG: Buscar contexto → Pasar al LLM → Generar respuesta
```

#### 🔧 Libertad Total de Herramientas

- ✅ **Base de datos vectorial**: Cualquiera (Pinecone sugerido, free tier)
- ✅ **Modelo LLM**: Cualquiera (Groq sugerido, free tier)
- ✅ **Framework**: Cualquiera (LangChain, Llama Index, etc.)
- ✅ **Frontend**: Cualquiera (Streamlit sugerido)

#### 📅 Fechas

- **Entrega**: **Sábado 13 de diciembre de 2025** (fecha límite confirmada en Clase 8)
- **Estado**: ✅ Implementado, falta entregar
- **⚠️ URGENTE**: Fecha límite es sábado 13 de diciembre

#### 🔍 Estado Actual

**✅ Implementado:**
- ✅ `CEIA-LLMIAG/ClaseVI/codigo/tp2_cargar_cv.py` - Script 1 completo
- ✅ `CEIA-LLMIAG/ClaseVI/codigo/tp2_chatbot.py` - Script 2 completo
- ✅ `CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md` - Documentación completa
- ✅ `CEIA-LLMIAG/ClaseVI/codigo/cv_ejemplo.txt` - Ejemplo de CV

**❌ Pendiente:**
- ❌ Video de demostración (OBS)
- ❌ Enviar links al formulario de entrega
- ❌ Verificar que todo funciona correctamente

#### ⚠️ Importante

- **TP2 es base para TP3**: Mismo concepto pero con agentes
- **Chunking es clave**: Técnica más importante del TP
- **Debe estar funcionando** antes de empezar TP3
- **Fecha límite confirmada**: Sábado 13 de diciembre de 2025

---

### **TP3: Agentes con Múltiples CVs**

#### 📋 Consigna Original

**Asociado a**: Clase VII (Agentes)  
**Objetivo**: Continuar TP2 incorporando concepto de agentes para consultar múltiples currículums

#### ✅ Entregable Esperado

- Sistema funcional con agentes
- Múltiples CVs consultables (preferiblemente del grupo)
- Nodo decisor operativo
- Código y presentación

#### 🔧 Estructura Requerida

**Paso 1: Esquematizar flujo de trabajo**
```
Query → Nodo Decisor → ¿Qué CV usar? → Herramienta (RAG) → Respuesta
```

**Paso 2: Definir nodo condicional**
- Lógica de decisión: ¿Qué currículum usar?
- Cada CV es una herramienta (base vectorial con RAG)

**Paso 3: Implementar y compilar**
- Implementar cada nodo del diagrama
- Framework: LangChain, LangGraph, o implementación manual

#### 📋 Reglas Especiales

1. **Query genérica** → Responde como si fuera del alumno que presenta
2. **Múltiples CVs** → Traer contexto de cada uno y responder de manera acorde
3. **Trabajo individual**: Aunque se trabaja en grupo, entrega es individual

#### 📅 Fechas

- **Iniciado**: Clase 7 (trabajo en grupo)
- **Entrega**: Individual, **Sábado 13 de diciembre de 2025** (fecha límite confirmada en Clase 8)
- **Estado**: 🟡 En desarrollo
- **⚠️ URGENTE**: Fecha límite es sábado 13 de diciembre
- **⚠️ IMPORTANTE**: TP3 incluye **corrección y documentación** (importante para nota)

#### 🔍 Estado Actual

- 🟡 **Iniciado en Clase 7**
- ❌ **No implementado** en el repositorio
- ❓ **Requisito**: TP2 debe estar funcionando

#### ⚠️ Importante

- **TP2 debe estar funcionando**: Base necesaria
- **Dividir problema**: Trabajar bloque por bloque
  - Nodo decisor
  - Bases de datos vectoriales con CVs
  - Prueba de prompts
- **Currículums del grupo**: Necesarios para armar esquema
- **No perderse en código**: Trabajar bloque por bloque, mantener ownership
- **Fecha límite confirmada**: Sábado 13 de diciembre de 2025
- **Corrección y documentación**: Incluye aspectos que hacen a la nota
- **Repositorio documentado**: Debe ser algo que puedas mostrar (incluso en CV)

---

## 🎯 PLAN DE IMPLEMENTACIÓN COMPLETO

### FASE 1: Verificación y Preparación (Día 1)

#### 1.1 Verificar Estado de TP1
- [ ] Consultar con docentes si TP1 es necesario (fecha pasada)
- [ ] Si es necesario: Evaluar tiempo disponible vs complejidad
- [ ] Decisión: ¿Implementar TP1 o no?

#### 1.2 Verificar Estado de TP2
- [ ] Probar `tp2_cargar_cv.py` - Verificar que funciona
- [ ] Probar `tp2_chatbot.py` - Verificar que funciona
- [ ] Probar queries de ejemplo - Verificar respuestas
- [ ] Documentar cualquier problema encontrado

#### 1.3 Preparar Entorno para TP3
- [ ] Verificar que TP2 funciona completamente
- [ ] Obtener currículums del grupo (o usar genéricos)
- [ ] Preparar estructura de carpetas para TP3
- [ ] Revisar ejemplos de agentes en `ClaseVII/codigo/`

---

### FASE 2: Completar TP2 (Días 2-3)

#### 2.1 Verificar Funcionalidad
```bash
# Paso 1: Verificar script de carga
cd CEIA-LLMIAG/ClaseVI/codigo
python tp2_cargar_cv.py

# Paso 2: Verificar chatbot
streamlit run tp2_chatbot.py
```

**Checklist de verificación:**
- [ ] CV se carga correctamente a Pinecone
- [ ] Chunking funciona (verificar chunks generados)
- [ ] Embeddings se generan correctamente
- [ ] Chatbot responde preguntas sobre el CV
- [ ] Interfaz Streamlit es funcional
- [ ] Historial de conversación funciona

#### 2.2 Crear Video de Demostración
- [ ] Instalar OBS Studio (software gratuito)
- [ ] Preparar demo: Mostrar funcionalidades clave
  - Cargar CV
  - Hacer preguntas de ejemplo
  - Mostrar respuestas del chatbot
  - Mostrar interfaz Streamlit
- [ ] Grabar video (duración sugerida: 3-5 minutos)
- [ ] Subir video a YouTube o guardar en repo

#### 2.3 Preparar Entrega
- [ ] Verificar que repositorio está actualizado
- [ ] Verificar que README_TP2.md está completo
- [ ] Preparar links:
  - Link al repositorio
  - Link al video (o video en repo)
- [ ] Revisar formulario de entrega (Google Form)
- [ ] Enviar TP2 al formulario

---

### FASE 3: Implementar TP3 (Días 4-8)

#### 3.1 Esquematizar Flujo de Trabajo

**Diagrama conceptual:**
```
Usuario pregunta
    ↓
Nodo Decisor (LLM)
    ├─→ ¿Pregunta por persona específica?
    │   ├─→ Sí → Usar CV de esa persona
    │   └─→ No → Usar CV del alumno que presenta
    ↓
Herramienta RAG (Base vectorial del CV seleccionado)
    ↓
LLM con contexto
    ↓
Respuesta final
```

**Archivo a crear**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_diagrama.md`

#### 3.2 Implementar Nodo Decisor

**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_decisor.py`

```python
# Funcionalidad:
# 1. Recibir query del usuario
# 2. Usar LLM para determinar:
#    - ¿Menciona nombre específico?
#    - ¿Qué CV usar?
#    - ¿Múltiples CVs necesarios?
# 3. Retornar decisión (qué herramienta usar)
```

**Checklist:**
- [ ] Implementar función de decisión
- [ ] Probar con queries de ejemplo:
  - "¿Cuál es la experiencia de Juan?"
  - "¿Qué habilidades tiene Pedro?"
  - "¿Cuál es mi experiencia?" (genérica)
- [ ] Verificar que decisiones son correctas

#### 3.3 Implementar Herramientas RAG (una por CV)

**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_rag_tools.py`

```python
# Funcionalidad:
# 1. Herramienta RAG para CV1
# 2. Herramienta RAG para CV2
# 3. Herramienta RAG para CV3 (si aplica)
# Cada herramienta:
#   - Conecta con su base vectorial
#   - Busca contexto relevante
#   - Retorna contexto para el LLM
```

**Checklist:**
- [ ] Cargar múltiples CVs a Pinecone (índices separados o metadata)
- [ ] Crear función RAG para cada CV
- [ ] Probar búsqueda en cada CV
- [ ] Verificar que contextos son relevantes

#### 3.4 Implementar Agente Principal

**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_agente.py`

**Opción A: Implementación Manual (ReAct)**
```python
# Flujo:
# 1. Usuario pregunta
# 2. Nodo decisor determina qué CV usar
# 3. Herramienta RAG busca contexto
# 4. LLM genera respuesta con contexto
# 5. Si necesita más info, loop
```

**Opción B: Usar LangChain/LangGraph**
```python
# Ventaja: Más estructurado, menos código manual
# Desventaja: Menos control sobre flujo
```

**Checklist:**
- [ ] Implementar agente (manual o con framework)
- [ ] Integrar nodo decisor
- [ ] Integrar herramientas RAG
- [ ] Probar flujo completo
- [ ] Manejar queries genéricas (CV del alumno)
- [ ] Manejar queries con múltiples CVs

#### 3.5 Implementar Interfaz

**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/tp3_interfaz.py`

```python
# Funcionalidad:
# 1. Interfaz Streamlit (o similar)
# 2. Input de pregunta
# 3. Mostrar proceso del agente (opcional)
# 4. Mostrar respuesta
# 5. Historial de conversación
```

**Checklist:**
- [ ] Crear interfaz básica
- [ ] Integrar con agente
- [ ] Mostrar respuestas
- [ ] Opcional: Mostrar proceso de decisión
- [ ] Probar interfaz completa

#### 3.6 Testing y Validación

**Checklist de pruebas:**
- [ ] Query genérica → Responde con CV del alumno
- [ ] Query con nombre específico → Responde con CV correcto
- [ ] Query sobre múltiples personas → Trae contexto de cada uno
- [ ] Queries complejas → Agente itera correctamente
- [ ] Manejo de errores → Respuestas apropiadas

---

### FASE 4: Documentación y Entrega Final (Día 9-10)

#### 4.1 Documentar TP3

**Archivo**: `CEIA-LLMIAG/ClaseVII/codigo/README_TP3.md`

**Contenido:**
- Descripción del sistema
- Arquitectura (diagrama de flujo)
- Instrucciones de instalación
- Instrucciones de uso
- Ejemplos de queries
- Estructura del código

#### 4.2 Preparar Presentación

**Formato sugerido:**
- Video de demostración (OBS)
- O slides con capturas de pantalla
- Mostrar:
  - Flujo del agente
  - Ejemplos de queries
  - Decisiones del nodo decisor
  - Respuestas del sistema

#### 4.3 Entrega Final

**Checklist:**
- [ ] Repositorio actualizado con TP3
- [ ] README_TP3.md completo
- [ ] Video/presentación preparada
- [ ] Links preparados:
  - Repositorio
  - Video/presentación
- [ ] Enviar TP3 al formulario

---

## 📁 ESTRUCTURA DE ARCHIVOS PROPUESTA

```
CEIA-LLMIAG/
├── ClaseVI/
│   └── codigo/
│       ├── tp2_cargar_cv.py      ✅ Implementado
│       ├── tp2_chatbot.py        ✅ Implementado
│       ├── README_TP2.md         ✅ Implementado
│       └── cv.txt                ✅ Implementado
│
├── ClaseVII/
│   └── codigo/
│       ├── tp3_decisor.py        ❌ Por implementar
│       ├── tp3_rag_tools.py      ❌ Por implementar
│       ├── tp3_agente.py         ❌ Por implementar
│       ├── tp3_interfaz.py       ❌ Por implementar
│       ├── tp3_diagrama.md       ❌ Por crear
│       ├── README_TP3.md         ❌ Por crear
│       └── cvs/                  ❌ Por crear
│           ├── cv_alumno.txt
│           ├── cv_companero1.txt
│           └── cv_companero2.txt
│
└── ClaseIV/
    └── TinyGPT.ipynb             ❓ Evaluar si necesario
```

---

## 🛠️ GUÍA TÉCNICA DE IMPLEMENTACIÓN

### TP3: Componentes Técnicos

#### 1. Nodo Decisor

**Implementación sugerida:**
```python
def decidir_cv(query: str, llm) -> dict:
    """
    Determina qué CV(s) usar basado en la query.
    
    Returns:
        {
            'cvs': ['cv_alumno', 'cv_juan'],  # Lista de CVs a consultar
            'razon': 'Query menciona a Juan específicamente'
        }
    """
    prompt = f"""
    Analiza la siguiente pregunta y determina:
    1. ¿Menciona el nombre de alguna persona específica?
    2. ¿Qué CV(s) debería consultar?
    3. Si no menciona nombre, usar CV del alumno que presenta.
    
    Pregunta: {query}
    
    Responde en formato JSON:
    {{
        "cvs": ["cv_alumno"],
        "razon": "explicación"
    }}
    """
    # Llamar a LLM
    # Parsear respuesta
    # Retornar decisión
```

#### 2. Herramientas RAG

**Implementación sugerida:**
```python
class RAGTool:
    def __init__(self, cv_name: str, index_name: str):
        self.cv_name = cv_name
        self.index = pinecone.Index(index_name)
        self.embedding_model = SentenceTransformer('model-name')
    
    def buscar_contexto(self, query: str, top_k: int = 3) -> str:
        """
        Busca contexto relevante en el CV.
        """
        # Generar embedding de query
        query_embedding = self.embedding_model.encode(query)
        
        # Buscar en Pinecone
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        
        # Extraer textos de chunks
        contextos = [r['metadata']['text'] for r in results['matches']]
        
        # Concatenar contextos
        return '\n\n'.join(contextos)
```

#### 3. Agente Principal

**Implementación ReAct manual:**
```python
class AgenteCV:
    def __init__(self, llm, decisor, rag_tools):
        self.llm = llm
        self.decisor = decisor
        self.rag_tools = rag_tools  # Dict: {'cv_alumno': RAGTool, ...}
    
    def procesar_query(self, query: str, max_iteraciones: int = 5) -> str:
        """
        Procesa query usando patrón ReAct.
        """
        # Paso 1: Decidir qué CV usar
        decision = self.decisor(query)
        
        # Paso 2: Buscar contexto en CV(s) seleccionado(s)
        contextos = []
        for cv_name in decision['cvs']:
            if cv_name in self.rag_tools:
                contexto = self.rag_tools[cv_name].buscar_contexto(query)
                contextos.append(f"Contexto de {cv_name}:\n{contexto}")
        
        # Paso 3: Generar respuesta con contexto
        respuesta = self.llm.generate(
            query=query,
            context='\n\n'.join(contextos)
        )
        
        return respuesta
```

#### 4. Integración con LangChain (Alternativa)

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.tools import Tool

# Crear herramientas
rag_tool_cv1 = Tool(
    name="Buscar en CV de Juan",
    func=lambda q: rag_tool_cv1.buscar_contexto(q),
    description="Busca información en el CV de Juan"
)

rag_tool_cv2 = Tool(
    name="Buscar en CV del alumno",
    func=lambda q: rag_tool_alumno.buscar_contexto(q),
    description="Busca información en el CV del alumno que presenta"
)

# Crear agente
agent = create_react_agent(llm, [rag_tool_cv1, rag_tool_cv2], prompt)
agent_executor = AgentExecutor(agent=agent, tools=[rag_tool_cv1, rag_tool_cv2])
```

---

## 📋 CHECKLIST FINAL DE ENTREGA

### TP2
- [ ] Código funcionando correctamente
- [ ] Video de demostración grabado
- [ ] Repositorio actualizado
- [ ] Links preparados
- [ ] Enviado al formulario

### TP3
- [ ] Nodo decisor implementado y funcionando
- [ ] Herramientas RAG para múltiples CVs
- [ ] Agente principal funcionando
- [ ] Interfaz implementada
- [ ] Testing completo
- [ ] Documentación completa (README_TP3.md)
- [ ] Video/presentación preparada
- [ ] Repositorio actualizado
- [ ] Links preparados
- [ ] Enviado al formulario

### TP1 (si es necesario)
- [ ] Consultar con docentes
- [ ] Si necesario: Implementar sampling techniques
- [ ] Si necesario: Implementar MoE
- [ ] Si necesario: Visualizaciones
- [ ] Si necesario: Documentación
- [ ] Si necesario: Entrega

---

## 🚨 PUNTOS CRÍTICOS Y RECOMENDACIONES

### Puntos Críticos

1. **TP2 debe funcionar antes de TP3**
   - Verificar completamente antes de empezar TP3
   - Si hay problemas, resolverlos primero

2. **Dividir TP3 en bloques**
   - No intentar implementar todo de una vez
   - Trabajar bloque por bloque
   - Probar cada bloque antes de continuar

3. **Mantener ownership del código**
   - No depender completamente de código generado por IA
   - Entender cada componente
   - Documentar decisiones

4. **Currículums del grupo**
   - Asegurarse de tenerlos antes de empezar
   - O usar CVs genéricos para desarrollo

### Recomendaciones

1. **Empezar con implementación simple**
   - Primero: Nodo decisor básico
   - Segundo: Una herramienta RAG
   - Tercero: Agente simple
   - Cuarto: Agregar complejidad

2. **Testing continuo**
   - Probar cada componente individualmente
   - Probar integraciones paso a paso
   - No esperar al final para probar

3. **Documentación mientras desarrollas**
   - Documentar decisiones
   - Documentar problemas encontrados
   - Documentar soluciones

4. **Consultas tempranas**
   - Si hay dudas, consultar con docentes
   - No esperar hasta el último momento

---

## 📞 CONTACTO Y RECURSOS

### Docentes
- **Esp. Abraham Rodriguez**: abraham.rodz17@gmail.com
- **Esp. Ezequiel Guinsburg**: ezequiel.guinsburg@gmail.com

### Recursos del Curso
- Repositorio del curso (GitHub)
- Código de ejemplo en cada clase
- Papers y documentación técnica

### Herramientas Sugeridas
- **OBS Studio**: Para grabación de video (gratis)
- **Streamlit**: Para interfaces (ya usado en TP2)
- **LangChain/LangGraph**: Para agentes (opcional)
- **Pinecone**: Base de datos vectorial (free tier)
- **Groq**: LLM API (free tier)

---

## 🎯 PRÓXIMOS PASOS INMEDIATOS

1. **Verificar estado de TP2**
   - Probar scripts
   - Documentar problemas si los hay

2. **Consultar sobre TP1**
   - Enviar correo a docentes preguntando si es necesario

3. **Preparar para TP3**
   - Obtener currículums del grupo
   - Revisar ejemplos de agentes en ClaseVII

4. **Comenzar implementación de TP3**
   - Empezar con nodo decisor
   - Probar con queries de ejemplo

---

---

## 🚨 INFORMACIÓN CRÍTICA DE CLASE 8

### Fecha Límite Confirmada
- **Sábado 13 de diciembre de 2025**
- **Razón**: Notas deben entregarse el martes 16 de diciembre
- **TPs a entregar**: TP2 y TP3

### TP3: Requisitos Adicionales
- **Corrección y documentación**: Incluye aspectos que hacen a la nota
- **Repositorio documentado**: Debe ser algo que puedas mostrar (incluso en CV)
- **Trabajo individual**: Aunque se trabaja en grupo, entrega es individual

### Consejos del Docente (Clase 8)
1. **Trabajar modularmente**: Armar esqueleto primero, luego completar partes
2. **Probar cada paso**: No dejar que LLM resuelva varios pasos a la vez
3. **Estructura de archivos**: Crear archivos vacíos ayuda a dar contexto
4. **Documentación**: Importante para nota y para mostrar en CV
5. **Investigación**: No quedarse solo con lo visto en clase, investigar librerías y bases de datos

---

*Última actualización: 9 de diciembre de 2025 (después de Clase 8)*
*Fecha límite confirmada: Sábado 13 de diciembre de 2025*

