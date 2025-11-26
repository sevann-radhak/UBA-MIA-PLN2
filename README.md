# UBA-MIA-PLN2

Repositorio personal para el curso **Procesamiento del Lenguaje Natural II** de la Maestría en Inteligencia Artificial (UBA).

## 📚 Sobre el Curso

**Materia**: Procesamiento del Lenguaje Natural II  
**Institución**: Universidad de Buenos Aires (UBA)  
**Programa**: Maestría en Inteligencia Artificial

### Docentes
- **Esp. Abraham Rodriguez**: abraham.rodz17@gmail.com
- **Esp. Ezequiel Guinsburg**: ezequielguinsburg@gmail.com

### Programa del Curso

1. Repaso de Transformers, Arquitectura y Tokenizers
2. Arquitecturas de LLMs, Transformer Decoder
3. Ecosistema actual, APIs, costos, HuggingFace y OpenAI. Evaluación de LLMs
4. MoEs, técnicas de prompts
5. Modelos locales y uso de APIs
6. RAG, vector DBs, chatbots y práctica
7. Agentes, fine-tuning y práctica
8. LLMs de Razonamiento. Optimización, Generación multimodal y práctica

---

## 📁 Estructura del Repositorio

```
.
├── CEIA-LLMIAG/              # Material del curso (repositorio original)
│   ├── ClaseI/               # Transformers y Tokenizers
│   ├── ClaseII/              # Arquitecturas LLMs
│   ├── ClaseIII/             # Ecosistema y Evaluación
│   ├── ClaseIV/              # MoEs y Prompts
│   ├── ClaseV/               # Modelos Locales
│   ├── ClaseVI/              # RAG y Vector DBs ⭐ TP2
│   │   └── codigo/
│   │       ├── tp2_cargar_cv.py    # Script 1: Cargar CV a Pinecone
│   │       ├── tp2_chatbot.py      # Script 2: Chatbot con RAG
│   │       ├── README_TP2.md        # Documentación del TP2
│   │       └── requirements.txt    # Dependencias
│   ├── ClaseVII/             # Agentes y Fine-tuning
│   ├── ClaseVIII/             # Razonamiento y Multimodal
│   └── Papers/               # Papers académicos
└── .gitignore                # Archivos excluidos del repositorio
```

---

## 🚀 Trabajo Práctico 2: Chatbot con RAG

### Descripción

Implementación de un chatbot que usa **RAG (Retrieval-Augmented Generation)** para responder preguntas sobre currículums vitae usando:
- **Pinecone**: Base de datos vectorial
- **Groq**: API de LLM para generación
- **Streamlit**: Interfaz de usuario
- **Sentence Transformers**: Modelos de embeddings

### 📋 Requisitos

- Python 3.8+
- API Key de Pinecone (gratis en [pinecone.io](https://www.pinecone.io/))
- API Key de Groq (gratis en [console.groq.com](https://console.groq.com/))

### 🛠️ Instalación Rápida

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/sevann-radhak/UBA-MIA-PLN2.git
   cd UBA-MIA-PLN2/CEIA-LLMIAG/ClaseVI/codigo
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar API Keys**:
   - Crea un archivo `.env` en `CEIA-LLMIAG/ClaseVI/codigo/`
   - Agrega tus API keys:
     ```env
     PINECONE_API_KEY=tu_api_key_aqui
     PINECONE_ENVIRONMENT=us-east-1-aws
     GROQ_API_KEY=tu_api_key_aqui
     ```

4. **Crear archivo CV**:
   - Crea `cv.txt` con tu currículum en texto plano

### ▶️ Uso

1. **Cargar CV a Pinecone**:
   ```bash
   python tp2_cargar_cv.py
   ```

2. **Ejecutar el Chatbot**:
   ```bash
   streamlit run tp2_chatbot.py
   ```

### 📖 Documentación Completa

Para más detalles, consulta: [`CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md`](CEIA-LLMIAG/ClaseVI/codigo/README_TP2.md)

---

## 🔒 Seguridad

Este repositorio está configurado para **NO subir**:
- ❌ Archivos `.env` con API keys
- ❌ Archivos personales de análisis
- ❌ Documentos de notas personales
- ❌ CVs personales

Consulta el [`.gitignore`](.gitignore) para más detalles.

---

## 📝 Notas

- Este repositorio contiene material del curso y trabajos prácticos personales
- El material original del curso está en `CEIA-LLMIAG/`
- Los trabajos prácticos incluyen implementaciones propias y mejoras

---

## 📄 Licencia

Este repositorio es para uso educativo personal. El material del curso pertenece a los docentes de la UBA.

---

## 🤝 Contribuciones

Este es un repositorio personal para el curso. No se aceptan contribuciones externas.

---

## 📧 Contacto

Para consultas sobre el curso, contactar a los docentes:
- abraham.rodz17@gmail.com
- ezequielguinsburg@gmail.com

---

**Última actualización**: Noviembre 2025

