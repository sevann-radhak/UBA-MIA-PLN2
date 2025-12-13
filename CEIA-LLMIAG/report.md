**Entrega TP2 y TP3 - Procesamiento del Lenguaje Natural II**

---

### Trabajos entregados

**TP2: Chatbot RAG con CVs**  
**TP3: Agentes con múltiples CVs**

### Repositorio

**Link al repositorio**: https://github.com/sevann-radhak/UBA-MIA-PLN2

### Documentación y estructura

Toda la información detallada sobre la implementación, uso y estructura de los trabajos se encuentra en los siguientes archivos del repositorio:

#### Para TP2:
- **`CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md`** - documentación completa del TP2.
- **`CEIA-LLMIAG/ClaseVI/codigo/tp2_cargar_cv.py`** - script para cargar CV a Pinecone.
- **`CEIA-LLMIAG/ClaseVI/codigo/tp2_chatbot.py`** - Chatbot con interfaz Streamlit.

#### Para TP3:
- **`CEIA-LLMIAG/ClaseVII/codigo/README_TP3.md`** - documentación completa del TP3.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_diagrama.md`** - diagrama de flujo del sistema.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_verificar.py`** - script de verificación del sistema.

#### Archivos principales de implementación TP3:
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_cargar_cvs.py`** - carga múltiples CVs a Pinecone.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_decisor.py`** - nodo decisor que determina qué CV usar.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_rag_tools.py`** - herramientas RAG para cada CV.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_agente.py`** - agente principal que integra todos los componentes.
- **`CEIA-LLMIAG/ClaseVII/codigo/tp3_interfaz.py`** - interfaz Streamlit para interactuar con el agente.

### Características implementadas

#### TP2:
- Sistema RAG completo con Pinecone
- Chatbot funcional con Groq
- Interfaz Streamlit
- Chunking por oraciones
- Historial de conversación

#### TP3:
- Sistema de agentes con nodo decisor
- Múltiples CVs consultables (3 CVs: alumno, Pedro, Ana)
- Herramientas RAG independientes por CV
- Agente principal con patrón ReAct
- Soporte para queries genéricas (CV del alumno)
- Soporte para queries con nombres específicos
- Soporte para queries comparativas entre múltiples personas
- Interfaz completa con detalles del proceso
- Documentación exhaustiva

### Instrucciones de uso

Las instrucciones detalladas de instalación, configuración y uso se encuentran en:
- **TP2**: `CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md`
- **TP3**: `CEIA-LLMIAG/ClaseVII/codigo/README_TP3.md`

### Requisitos

- Python 3.x
- API keys de Pinecone y Groq (configuradas en archivo `.env`)
- Dependencias listadas en `requirements.txt`

### Notas Adicionales

- El código está completamente documentado y comentado.
- Todos los scripts incluyen manejo de errores.
- El sistema TP3 incluye script de verificación (`tp3_verificar.py`) para validar que todo funciona correctamente.
- Los CVs utilizados en TP3 son de ejemplo (María González, Pedro Martínez, Ana Rodríguez).

---
