"""
TP2 - Script 2: Chatbot con RAG usando CV
==========================================

Este script implementa un chatbot que:
1. Conecta con Pinecone para buscar contexto relevante
2. Usa Groq para generar respuestas basadas en el CV
3. Interfaz web con Streamlit

Autor: TP2 - Clase VI - CEIA LLMIAG
"""

import os
from typing import List
import streamlit as st
from groq import Groq
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# ================================
# CONFIGURACIÓN
# ================================

# API Keys
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-west1-gcp")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Configuración del índice (debe coincidir con tp2_cargar_cv.py)
NOMBRE_INDICE = "cv-rag-tp2"
MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"

# Modelo de Groq
MODELO_GROQ = "llama-3.1-8b-instant"

# Número de chunks a recuperar
TOP_K = 3


# ================================
# INICIALIZACIÓN
# ================================

@st.cache_resource
def inicializar_pinecone():
    """Inicializa Pinecone (cached para Streamlit) - Nueva API v3+."""
    pc = Pinecone(api_key=PINECONE_API_KEY)
    return pc.Index(NOMBRE_INDICE)


@st.cache_resource
def inicializar_modelo_embeddings():
    """Inicializa el modelo de embeddings (cached para Streamlit)."""
    return SentenceTransformer(MODELO_EMBEDDINGS)


@st.cache_resource
def inicializar_groq():
    """Inicializa el cliente de Groq (cached para Streamlit)."""
    return Groq(api_key=GROQ_API_KEY)


# ================================
# FUNCIONES RAG
# ================================

def buscar_contexto_relevante(
    pregunta: str,
    indice,
    modelo_embeddings: SentenceTransformer,
    top_k: int = TOP_K
) -> List[dict]:
    """
    Busca los chunks más relevantes en Pinecone para una pregunta.
    
    Args:
        pregunta: Pregunta del usuario
        indice: Índice de Pinecone
        modelo_embeddings: Modelo para generar embeddings
        top_k: Número de resultados a recuperar
    
    Returns:
        Lista de chunks relevantes con scores
    """
    # Generar embedding de la pregunta
    embedding_pregunta = modelo_embeddings.encode(pregunta).tolist()
    
    # Buscar en Pinecone
    resultados = indice.query(
        vector=embedding_pregunta,
        top_k=top_k,
        include_metadata=True
    )
    
    # Formatear resultados
    chunks_relevantes = []
    for match in resultados['matches']:
        chunks_relevantes.append({
            "texto": match['metadata']['texto'],
            "score": match['score'],
            "chunk_numero": match['metadata']['chunk_numero']
        })
    
    return chunks_relevantes


def construir_prompt_rag(pregunta: str, contexto: List[dict]) -> str:
    """
    Construye el prompt para el LLM con el contexto de RAG.
    
    Args:
        pregunta: Pregunta del usuario
        contexto: Lista de chunks relevantes
    
    Returns:
        Prompt completo para el LLM
    """
    # Construir contexto a partir de los chunks
    contexto_texto = "\n\n".join([
        f"[Chunk {chunk['chunk_numero']}]: {chunk['texto']}"
        for chunk in contexto
    ])
    
    # Prompt con contexto
    prompt = f"""Eres un asistente que responde preguntas sobre un currículum vitae.

CONTEXTO DEL CV:
{contexto_texto}

INSTRUCCIONES:
- Responde la pregunta del usuario basándote ÚNICAMENTE en el contexto proporcionado
- Si la información no está en el contexto, di que no tienes esa información
- Sé claro y conciso
- Cita el chunk relevante cuando sea apropiado

PREGUNTA DEL USUARIO: {pregunta}

RESPUESTA:"""
    
    return prompt


# ================================
# INTERFAZ STREAMLIT
# ================================

def main():
    """Función principal de la aplicación."""
    
    # Verificar API keys
    if not PINECONE_API_KEY or not GROQ_API_KEY:
        st.error("⚠️ API Keys no configuradas")
        st.info("💡 Configura PINECONE_API_KEY y GROQ_API_KEY en .env")
        st.stop()
    
    # Título
    st.title("🤖 Chatbot RAG - CV")
    st.markdown("""
    **Chatbot con Retrieval-Augmented Generation (RAG)**
    
    Este chatbot responde preguntas sobre tu currículum vitae usando:
    - 🔍 Búsqueda vectorial en Pinecone
    - 🧠 Modelo de lenguaje Groq
    - 📚 Contexto relevante del CV
    """)
    
    # Inicializar componentes
    try:
        indice = inicializar_pinecone()
        modelo_embeddings = inicializar_modelo_embeddings()
        cliente_groq = inicializar_groq()
        st.sidebar.success("✅ Componentes inicializados")
    except Exception as e:
        st.error(f"❌ Error al inicializar: {str(e)}")
        st.info("💡 Asegúrate de haber ejecutado tp2_cargar_cv.py primero")
        st.stop()
    
    # Configuración en sidebar
    st.sidebar.title("⚙️ Configuración")
    
    top_k = st.sidebar.slider(
        "Número de chunks a recuperar (k)",
        min_value=1,
        max_value=10,
        value=TOP_K,
        help="Más chunks = más contexto pero más tokens"
    )
    
    modelo_seleccionado = st.sidebar.selectbox(
        "Modelo Groq",
        ["llama-3.1-8b-instant", "llama-3.3-70b-versatile"],
        index=0
    )
    
    # Inicializar historial de conversación
    if "historial" not in st.session_state:
        st.session_state.historial = []
    
    # Mostrar historial
    if st.session_state.historial:
        st.markdown("### 📜 Historial de Conversación")
        for i, mensaje in enumerate(st.session_state.historial):
            if mensaje["role"] == "user":
                st.markdown(f"**👤 Usuario:** {mensaje['content']}")
            else:
                with st.expander(f"🤖 Respuesta {i//2 + 1}"):
                    st.markdown(mensaje['content'])
                    if "chunks_usados" in mensaje:
                        st.caption(f"📚 Chunks usados: {len(mensaje['chunks_usados'])}")
        st.markdown("---")
    
    # Input del usuario
    pregunta = st.text_input(
        "💬 Haz una pregunta sobre el CV:",
        placeholder="Ejemplo: ¿Cuál es mi experiencia en Python?",
        key="pregunta_input"
    )
    
    # Botón para limpiar historial
    if st.sidebar.button("🗑️ Limpiar Historial"):
        st.session_state.historial = []
        st.rerun()
    
    # Procesar pregunta
    if pregunta:
        with st.spinner("🔍 Buscando contexto relevante..."):
            # 1. Buscar contexto relevante
            chunks_relevantes = buscar_contexto_relevante(
                pregunta,
                indice,
                modelo_embeddings,
                top_k=top_k
            )
            
            if not chunks_relevantes:
                st.warning("⚠️ No se encontró contexto relevante en el CV")
                st.stop()
            
            # Mostrar chunks encontrados (opcional, para debug)
            with st.expander(f"📚 Chunks relevantes encontrados ({len(chunks_relevantes)})"):
                for i, chunk in enumerate(chunks_relevantes):
                    st.markdown(f"**Chunk {i+1}** (Score: {chunk['score']:.3f})")
                    st.caption(chunk['texto'][:200] + "...")
        
        with st.spinner("🤔 Generando respuesta..."):
            # 2. Construir prompt con contexto
            prompt_completo = construir_prompt_rag(pregunta, chunks_relevantes)
            
            # 3. Generar respuesta con Groq
            try:
                respuesta = cliente_groq.chat.completions.create(
                    messages=[
                        {
                            "role": "user",
                            "content": prompt_completo
                        }
                    ],
                    model=modelo_seleccionado,
                    temperature=0.7,
                    max_tokens=1000
                )
                
                respuesta_texto = respuesta.choices[0].message.content
                
                # Guardar en historial
                st.session_state.historial.append({
                    "role": "user",
                    "content": pregunta
                })
                st.session_state.historial.append({
                    "role": "assistant",
                    "content": respuesta_texto,
                    "chunks_usados": chunks_relevantes
                })
                
                # Mostrar respuesta
                st.markdown("### 🤖 Respuesta:")
                st.markdown(respuesta_texto)
                
                # Información adicional
                st.caption(f"📊 Modelo: {modelo_seleccionado} | 📚 Chunks: {len(chunks_relevantes)}")
                
                # Recargar para mostrar historial actualizado
                st.rerun()
                
            except Exception as e:
                st.error(f"❌ Error al generar respuesta: {str(e)}")
    
    # Información adicional
    with st.expander("📚 Información sobre RAG"):
        st.markdown("""
        **¿Cómo funciona este chatbot?**
        
        1. **Retrieval**: Busca chunks relevantes en Pinecone usando embeddings
        2. **Augmentation**: Construye prompt con contexto relevante
        3. **Generation**: LLM genera respuesta basada en el contexto
        
        **Ventajas:**
        - Respuestas basadas en información específica del CV
        - Reducción de alucinaciones
        - Trazabilidad (puedes ver qué chunks se usaron)
        """)
    
    st.markdown("---")
    st.markdown("**📖 TP2 - Clase VI - CEIA LLMIAG**")


if __name__ == "__main__":
    main()

