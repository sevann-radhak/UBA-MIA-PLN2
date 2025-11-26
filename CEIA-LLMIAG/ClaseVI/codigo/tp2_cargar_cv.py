"""
TP2 - Script 1: Cargar CV a Base de Datos Vectorial
====================================================

Este script realiza las siguientes tareas:
1. Cargar currículum vitae (CV) desde archivo
2. Realizar chunking (dividir texto en fragmentos)
3. Generar embeddings para cada chunk
4. Subir vectores a Pinecone

Autor: TP2 - Clase VI - CEIA LLMIAG
"""

import os
import time
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ================================
# CONFIGURACIÓN
# ================================

# Configurar Pinecone
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
# Extraer región y cloud del environment
# Para FREE TIER: AWS suele tener más regiones disponibles (us-east-1, us-west-2)
# GCP en free tier tiene regiones limitadas
if "-gcp" in PINECONE_ENVIRONMENT:
    cloud = "gcp"
    region = PINECONE_ENVIRONMENT.replace("-gcp", "")
elif "-aws" in PINECONE_ENVIRONMENT:
    cloud = "aws"
    region = PINECONE_ENVIRONMENT.replace("-aws", "")
else:
    # Por defecto usar AWS (más regiones disponibles en free tier)
    cloud = "aws"
    region = "us-east-1"

# Modelo de embeddings (debe ser el mismo para cargar y buscar)
MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"  # 384 dimensiones

# Nombre del índice en Pinecone
NOMBRE_INDICE = "cv-rag-tp2"

# Archivo del CV (ajustar según tu caso)
ARCHIVO_CV = "cv.txt"  # Puede ser .txt, .pdf, etc.


# ================================
# FUNCIONES DE CHUNKING
# ================================

def chunking_simple(texto: str, chunk_size: int = 200, overlap: int = 50) -> List[str]:
    """
    Chunking simple por caracteres con overlap.
    
    Args:
        texto: Texto completo a dividir
        chunk_size: Tamaño de cada chunk en caracteres
        overlap: Caracteres de solapamiento entre chunks
    
    Returns:
        Lista de chunks
    """
    chunks = []
    inicio = 0
    
    while inicio < len(texto):
        fin = inicio + chunk_size
        chunk = texto[inicio:fin]
        chunks.append(chunk.strip())
        inicio = fin - overlap  # Overlap para mantener contexto
    
    return chunks


def chunking_por_oraciones(texto: str, max_chars: int = 300) -> List[str]:
    """
    Chunking por oraciones, agrupando hasta alcanzar max_chars.
    
    Args:
        texto: Texto completo
        max_chars: Máximo de caracteres por chunk
    
    Returns:
        Lista de chunks
    """
    # Dividir por oraciones (puntos, signos de exclamación, etc.)
    import re
    oraciones = re.split(r'[.!?]\s+', texto)
    
    chunks = []
    chunk_actual = ""
    
    for oracion in oraciones:
        oracion = oracion.strip()
        if not oracion:
            continue
        
        # Si agregar esta oración excede el límite, guardar chunk actual
        if len(chunk_actual) + len(oracion) + 1 > max_chars and chunk_actual:
            chunks.append(chunk_actual.strip())
            chunk_actual = oracion
        else:
            # Agregar oración al chunk actual
            if chunk_actual:
                chunk_actual += ". " + oracion
            else:
                chunk_actual = oracion
    
    # Agregar último chunk
    if chunk_actual:
        chunks.append(chunk_actual.strip())
    
    return chunks


# ================================
# FUNCIONES PRINCIPALES
# ================================

def cargar_cv(archivo: str) -> str:
    """
    Carga el CV desde un archivo de texto.
    
    Args:
        archivo: Ruta al archivo del CV
    
    Returns:
        Texto completo del CV
    """
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
        print(f"✅ CV cargado desde {archivo} ({len(texto)} caracteres)")
        return texto
    except FileNotFoundError:
        print(f"❌ Error: No se encontró el archivo {archivo}")
        print("💡 Crea un archivo cv.txt con tu currículum")
        raise


def procesar_cv_a_chunks(texto_cv: str, metodo: str = "oraciones") -> List[Dict[str, Any]]:
    """
    Procesa el CV y lo divide en chunks.
    
    Args:
        texto_cv: Texto completo del CV
        metodo: Método de chunking ("simple" o "oraciones")
    
    Returns:
        Lista de diccionarios con chunks y metadata
    """
    print(f"\n🔄 Procesando CV con método: {metodo}")
    
    if metodo == "simple":
        chunks = chunking_simple(texto_cv, chunk_size=200, overlap=50)
    else:  # oraciones
        chunks = chunking_por_oraciones(texto_cv, max_chars=300)
    
    # Crear lista de documentos con metadata
    documentos = []
    for i, chunk in enumerate(chunks):
        documentos.append({
            "id": f"chunk_{i:04d}",
            "texto": chunk,
            "chunk_numero": i,
            "longitud": len(chunk)
        })
    
    print(f"✅ CV dividido en {len(documentos)} chunks")
    return documentos


def configurar_pinecone():
    """Configura la conexión con Pinecone (nueva API v3+)."""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY no está configurada en .env")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print(f"✅ Pinecone configurado (cloud: {cloud}, region: {region})")
    return pc


def crear_indice_pinecone(pc: Pinecone, nombre_indice: str, dimension: int):
    """Crea el índice en Pinecone si no existe (nueva API v3+)."""
    indices_existentes = pc.list_indexes().names()
    
    if nombre_indice in indices_existentes:
        print(f"⚠️  El índice '{nombre_indice}' ya existe")
        return True
    
    print(f"🔄 Creando índice '{nombre_indice}'...")
    pc.create_index(
        name=nombre_indice,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=cloud,
            region=region
        )
    )
    
    # Esperar a que el índice esté listo
    while nombre_indice not in pc.list_indexes().names():
        time.sleep(1)
    
    print(f"✅ Índice '{nombre_indice}' creado exitosamente")
    return True


def cargar_vectores_a_pinecone(
    pc: Pinecone,
    nombre_indice: str,
    documentos: List[Dict[str, Any]],
    modelo_embedding: str
):
    """
    Genera embeddings y los carga a Pinecone.
    
    Args:
        pc: Instancia de Pinecone
        nombre_indice: Nombre del índice en Pinecone
        documentos: Lista de documentos con chunks
        modelo_embedding: Nombre del modelo de embeddings
    """
    print(f"\n🔄 Cargando modelo de embeddings: {modelo_embedding}")
    modelo = SentenceTransformer(modelo_embedding)
    dimension = modelo.get_sentence_embedding_dimension()
    print(f"✅ Modelo cargado (dimensión: {dimension})")
    
    # Conectar al índice (nueva API)
    indice = pc.Index(nombre_indice)
    
    # Generar embeddings para todos los chunks
    print(f"\n🔄 Generando embeddings para {len(documentos)} chunks...")
    textos = [doc["texto"] for doc in documentos]
    embeddings = modelo.encode(textos, show_progress_bar=True)
    
    # Preparar vectores para inserción
    print(f"\n🔄 Preparando vectores para Pinecone...")
    vectors_para_insertar = []
    
    for i, doc in enumerate(documentos):
        vector_data = {
            "id": doc["id"],
            "values": embeddings[i].tolist(),
            "metadata": {
                "texto": doc["texto"],
                "chunk_numero": doc["chunk_numero"],
                "longitud": doc["longitud"]
            }
        }
        vectors_para_insertar.append(vector_data)
    
    # Insertar en lotes (Pinecone recomienda lotes de hasta 100)
    lote_size = 100
    total_insertados = 0
    
    print(f"\n🔄 Insertando vectores en Pinecone (lotes de {lote_size})...")
    for i in range(0, len(vectors_para_insertar), lote_size):
        lote = vectors_para_insertar[i:i + lote_size]
        indice.upsert(vectors=lote)
        total_insertados += len(lote)
        print(f"   ✅ Insertados {total_insertados}/{len(vectors_para_insertar)} vectores")
    
    # Verificar estadísticas
    estadisticas = indice.describe_index_stats()
    print(f"\n✅ Vectores cargados exitosamente")
    print(f"   📊 Total de vectores: {estadisticas['total_vector_count']}")
    print(f"   📏 Dimensión: {estadisticas['dimension']}")


# ================================
# FUNCIÓN PRINCIPAL
# ================================

def main():
    """Función principal del script."""
    print("=" * 60)
    print("TP2 - Script 1: Cargar CV a Base de Datos Vectorial")
    print("=" * 60)
    
    try:
        # 1. Cargar CV
        texto_cv = cargar_cv(ARCHIVO_CV)
        
        # 2. Procesar CV en chunks
        documentos = procesar_cv_a_chunks(texto_cv, metodo="oraciones")
        
        # 3. Configurar Pinecone
        pc = configurar_pinecone()
        
        # 4. Inicializar modelo de embeddings para obtener dimensión
        modelo = SentenceTransformer(MODELO_EMBEDDINGS)
        dimension = modelo.get_sentence_embedding_dimension()
        
        # 5. Crear índice en Pinecone
        crear_indice_pinecone(pc, NOMBRE_INDICE, dimension)
        
        # 6. Cargar vectores a Pinecone
        cargar_vectores_a_pinecone(pc, NOMBRE_INDICE, documentos, MODELO_EMBEDDINGS)
        
        print("\n" + "=" * 60)
        print("✅ PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print(f"📁 Índice '{NOMBRE_INDICE}' está listo para usar")
        print(f"💡 Ahora puedes ejecutar tp2_chatbot.py para usar el chatbot")
        
    except Exception as e:
        print(f"\n❌ Error durante la ejecución: {str(e)}")
        raise


if __name__ == "__main__":
    main()

