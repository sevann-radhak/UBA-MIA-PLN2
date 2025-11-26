# TP2: Chatbot con RAG usando CVs

## 📋 Descripción

Implementar un chatbot que usa RAG (Retrieval-Augmented Generation) para responder preguntas sobre tu currículum vitae.

## 🎯 Objetivos

1. Cargar CV en base de datos vectorial (Pinecone)
2. Implementar chunking efectivo
3. Crear chatbot con RAG usando Streamlit
4. Integrar búsqueda vectorial con LLM (Groq)

## 📁 Archivos del TP2

- `tp2_cargar_cv.py`: Script 1 - Cargar CV a Pinecone
- `tp2_chatbot.py`: Script 2 - Chatbot con RAG
- `cv.txt`: Tu currículum vitae (crear este archivo)
- `.env`: Variables de entorno con API keys (crear este archivo)

## 🚀 Instalación

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

O instalar manualmente:
```bash
pip install pinecone-client sentence-transformers groq streamlit python-dotenv
```

### 2. Configurar API Keys

Crea un archivo `.env` en la carpeta `codigo/` con el siguiente contenido:

```env
# Pinecone API Key
PINECONE_API_KEY=tu_pinecone_api_key_aqui
PINECONE_ENVIRONMENT=us-west1-gcp

# Groq API Key
GROQ_API_KEY=tu_groq_api_key_aqui
```

**⚠️ IMPORTANTE**: 
- Reemplaza `tu_pinecone_api_key_aqui` con tu API key de Pinecone
- Reemplaza `tu_groq_api_key_aqui` con tu API key de Groq
- No subas el archivo `.env` a Git (debe estar en .gitignore)

### 3. Crear archivo CV

Crea un archivo `cv.txt` en la carpeta `codigo/` con tu currículum vitae en texto plano.

Ejemplo de estructura:
```
Nombre: Tu Nombre
Email: tu@email.com
Teléfono: +54 11 1234-5678

EXPERIENCIA LABORAL
-------------------
2020 - Presente: Desarrollador Python
- Desarrollo de aplicaciones web con Django
- Implementación de modelos de ML
- Trabajo con bases de datos SQL y NoSQL

EDUCACIÓN
---------
2018 - 2020: Maestría en Inteligencia Artificial
Universidad de Buenos Aires

HABILIDADES
-----------
- Python, JavaScript, SQL
- Machine Learning, Deep Learning
- Docker, Kubernetes
```

## 📝 Uso

### Paso 1: Cargar CV a Pinecone

Ejecuta el script para cargar tu CV:

```bash
python tp2_cargar_cv.py
```

Este script:
1. ✅ Carga el CV desde `cv.txt`
2. ✅ Divide el texto en chunks (chunking)
3. ✅ Genera embeddings para cada chunk
4. ✅ Carga los vectores a Pinecone

**Nota**: Si el índice ya existe, puedes modificarlo o eliminarlo desde la consola de Pinecone.

### Paso 2: Ejecutar el Chatbot

Ejecuta el chatbot con Streamlit:

```bash
streamlit run tp2_chatbot.py
```

El chatbot se abrirá en tu navegador (normalmente en `http://localhost:8501`).

## 🔧 Configuración Avanzada

### Cambiar método de chunking

En `tp2_cargar_cv.py`, puedes cambiar el método de chunking:

```python
# En la función main()
documentos = procesar_cv_a_chunks(texto_cv, metodo="oraciones")  # o "simple"
```

- `"oraciones"`: Agrupa por oraciones (recomendado)
- `"simple"`: Chunking por caracteres con overlap

### Ajustar número de chunks recuperados

En `tp2_chatbot.py` o desde la interfaz:
- Usa el slider en el sidebar para ajustar `top_k`
- Más chunks = más contexto pero más tokens

### Cambiar modelo de embeddings

En ambos scripts, puedes cambiar:
```python
MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensiones
```

Otros modelos disponibles:
- `sentence-transformers/all-mpnet-base-v2` (768 dimensiones)
- `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (multilingüe)

**⚠️ IMPORTANTE**: Usa el mismo modelo en ambos scripts.

## 🐛 Solución de Problemas

### Error: "PINECONE_API_KEY no está configurada"
- Verifica que el archivo `.env` existe
- Verifica que las variables están correctamente escritas
- Asegúrate de estar en la carpeta correcta

### Error: "No se encontró el archivo cv.txt"
- Crea el archivo `cv.txt` en la carpeta `codigo/`
- Verifica que el nombre del archivo coincide

### Error: "El índice ya existe"
- Puedes eliminar el índice desde la consola de Pinecone
- O modificar `NOMBRE_INDICE` en ambos scripts

### El chatbot no encuentra contexto relevante
- Verifica que ejecutaste `tp2_cargar_cv.py` primero
- Aumenta el valor de `top_k` en el chatbot
- Revisa que el CV tiene información relacionada con tu pregunta

## 📊 Estructura del Proyecto

```
ClaseVI/codigo/
├── tp2_cargar_cv.py      # Script 1: Cargar CV
├── tp2_chatbot.py        # Script 2: Chatbot RAG
├── cv.txt                # Tu currículum (crear)
├── .env                  # API keys (crear, no subir a Git)
├── requirements.txt      # Dependencias
├── ejemplo_pinecone.py   # Ejemplo de Pinecone
├── chatbot_gestionada.py # Ejemplo de chatbot
└── README_TP2.md        # Este archivo
```

## ✅ Checklist de Entrega

- [ ] Script 1 (`tp2_cargar_cv.py`) funciona correctamente
- [ ] Script 2 (`tp2_chatbot.py`) funciona correctamente
- [ ] Chatbot responde preguntas sobre el CV
- [ ] Interfaz Streamlit es funcional
- [ ] Video de demostración grabado
- [ ] Repositorio con código subido
- [ ] Links enviados al formulario de entrega

## 💡 Mejoras Opcionales

Si tienes tiempo extra, puedes explorar:

1. **Chunking más inteligente**: Usar LangChain para chunking semántico
2. **Mejorar el prompt**: Ajustar el prompt del LLM para mejores respuestas
3. **Metadata adicional**: Agregar más metadata a los chunks (sección del CV, etc.)
4. **Búsqueda híbrida**: Combinar embeddings con BM25
5. **Interfaz mejorada**: Mejorar el diseño de Streamlit

## 📚 Recursos

- [Documentación Pinecone](https://docs.pinecone.io/)
- [Documentación Groq](https://console.groq.com/docs)
- [Documentación Streamlit](https://docs.streamlit.io/)
- [Sentence Transformers](https://www.sbert.net/)

## 🆘 Ayuda

- Consultas por correo: abraham.rodz17@gmail.com, ezequiel.guinsburg@gmail.com
- Código de ejemplo en el repositorio del curso
- ChatGPT para consultas técnicas

---

**¡Buena suerte con el TP2! 🚀**

