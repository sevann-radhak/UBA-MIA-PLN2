# -*- coding: utf-8 -*-
"""
TP3 - Script: Cargar Múltiples CVs a Base de Datos Vectorial
============================================================

Este script carga múltiples currículums a Pinecone, creando índices separados
o usando metadata para diferenciarlos.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
import sys

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
import time
from typing import List, Dict, Any
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual (por si acaso)
load_dotenv()

# ================================
# CONFIGURACIÓN
# ================================

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
PINECONE_ENVIRONMENT = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")

if "-gcp" in PINECONE_ENVIRONMENT:
    cloud = "gcp"
    region = PINECONE_ENVIRONMENT.replace("-gcp", "")
elif "-aws" in PINECONE_ENVIRONMENT:
    cloud = "aws"
    region = PINECONE_ENVIRONMENT.replace("-aws", "")
else:
    cloud = "aws"
    region = "us-east-1"

MODELO_EMBEDDINGS = "sentence-transformers/all-MiniLM-L6-v2"

# Configuración de CVs
CVS_CONFIG = [
    {
        "nombre": "alumno",
        "archivo": "cvs/cv_alumno.txt",
        "indice": "cv-alumno-tp3",
        "persona": "María González"
    },
    {
        "nombre": "pedro",
        "archivo": "cvs/cv_pedro.txt",
        "indice": "cv-pedro-tp3",
        "persona": "Pedro Martínez"
    },
    {
        "nombre": "ana",
        "archivo": "cvs/cv_ana.txt",
        "indice": "cv-ana-tp3",
        "persona": "Ana Rodríguez"
    }
]


# ================================
# FUNCIONES DE CHUNKING
# ================================

def chunking_por_oraciones(texto: str, max_chars: int = 300) -> List[str]:
    """Chunking por oraciones, agrupando hasta alcanzar max_chars."""
    import re
    oraciones = re.split(r'[.!?]\s+', texto)
    
    chunks = []
    chunk_actual = ""
    
    for oracion in oraciones:
        oracion = oracion.strip()
        if not oracion:
            continue
        
        if len(chunk_actual) + len(oracion) + 1 > max_chars and chunk_actual:
            chunks.append(chunk_actual.strip())
            chunk_actual = oracion
        else:
            if chunk_actual:
                chunk_actual += ". " + oracion
            else:
                chunk_actual = oracion
    
    if chunk_actual:
        chunks.append(chunk_actual.strip())
    
    return chunks


# ================================
# FUNCIONES PRINCIPALES
# ================================

def cargar_cv(archivo: str) -> str:
    """Carga el CV desde un archivo de texto."""
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            texto = f.read()
        print(f"[OK] CV cargado desde {archivo} ({len(texto)} caracteres)")
        return texto
    except FileNotFoundError:
        print(f"[ERROR] No se encontro el archivo {archivo}")
        raise


def procesar_cv_a_chunks(texto_cv: str, persona: str) -> List[Dict[str, Any]]:
    """Procesa el CV y lo divide en chunks con metadata."""
    print(f"\n[PROCESANDO] Procesando CV de {persona}")
    
    chunks = chunking_por_oraciones(texto_cv, max_chars=300)
    
    documentos = []
    for i, chunk in enumerate(chunks):
        documentos.append({
            "id": f"chunk_{i:04d}",
            "texto": chunk,
            "chunk_numero": i,
            "longitud": len(chunk),
            "persona": persona
        })
    
    print(f"[OK] CV dividido en {len(documentos)} chunks")
    return documentos


def configurar_pinecone():
    """Configura la conexión con Pinecone."""
    if not PINECONE_API_KEY:
        raise ValueError("PINECONE_API_KEY no está configurada en .env")
    
    pc = Pinecone(api_key=PINECONE_API_KEY)
    print(f"[OK] Pinecone configurado (cloud: {cloud}, region: {region})")
    return pc


def crear_indice_pinecone(pc: Pinecone, nombre_indice: str, dimension: int):
    """Crea el índice en Pinecone si no existe."""
    indices_existentes = pc.list_indexes().names()
    
    if nombre_indice in indices_existentes:
        print(f"[ADVERTENCIA] El indice '{nombre_indice}' ya existe")
        respuesta = input(f"¿Deseas borrarlo y recrearlo? (s/n): ")
        if respuesta.lower() == 's':
            print(f"[PROCESANDO] Borrando indice '{nombre_indice}'...")
            pc.delete_index(nombre_indice)
            time.sleep(5)
        else:
            return True
    
    print(f"[PROCESANDO] Creando indice '{nombre_indice}'...")
    pc.create_index(
        name=nombre_indice,
        dimension=dimension,
        metric="cosine",
        spec=ServerlessSpec(
            cloud=cloud,
            region=region
        )
    )
    
    while nombre_indice not in pc.list_indexes().names():
        time.sleep(1)
    
    print(f"[OK] Indice '{nombre_indice}' creado exitosamente")
    return True


def cargar_vectores_a_pinecone(
    pc: Pinecone,
    nombre_indice: str,
    documentos: List[Dict[str, Any]],
    modelo_embedding: str,
    persona: str
):
    """Genera embeddings y los carga a Pinecone."""
    print(f"\n[PROCESANDO] Cargando modelo de embeddings: {modelo_embedding}")
    modelo = SentenceTransformer(modelo_embedding)
    dimension = modelo.get_sentence_embedding_dimension()
    print(f"[OK] Modelo cargado (dimension: {dimension})")
    
    indice = pc.Index(nombre_indice)
    
    print(f"\n[PROCESANDO] Generando embeddings para {len(documentos)} chunks...")
    textos = [doc["texto"] for doc in documentos]
    embeddings = modelo.encode(textos, show_progress_bar=True)
    
    print(f"\n[PROCESANDO] Preparando vectores para Pinecone...")
    vectors_para_insertar = []
    
    for i, doc in enumerate(documentos):
        vector_data = {
            "id": doc["id"],
            "values": embeddings[i].tolist(),
            "metadata": {
                "texto": doc["texto"],
                "chunk_numero": doc["chunk_numero"],
                "longitud": doc["longitud"],
                "persona": doc["persona"]
            }
        }
        vectors_para_insertar.append(vector_data)
    
    lote_size = 100
    total_insertados = 0
    
    print(f"\n[PROCESANDO] Insertando vectores en Pinecone (lotes de {lote_size})...")
    for i in range(0, len(vectors_para_insertar), lote_size):
        lote = vectors_para_insertar[i:i + lote_size]
        indice.upsert(vectors=lote)
        total_insertados += len(lote)
        print(f"   [OK] Insertados {total_insertados}/{len(vectors_para_insertar)} vectores")
    
    estadisticas = indice.describe_index_stats()
    print(f"\n[OK] Vectores de {persona} cargados exitosamente")
    print(f"   [INFO] Total de vectores: {estadisticas['total_vector_count']}")
    print(f"   [INFO] Dimension: {estadisticas['dimension']}")


def procesar_cv_completo(pc: Pinecone, cv_config: Dict[str, str]):
    """Procesa un CV completo: carga, chunking, embeddings, Pinecone."""
    print("\n" + "=" * 60)
    print(f"Procesando CV: {cv_config['persona']}")
    print("=" * 60)
    
    # 1. Cargar CV
    texto_cv = cargar_cv(cv_config['archivo'])
    
    # 2. Procesar en chunks
    documentos = procesar_cv_a_chunks(texto_cv, cv_config['persona'])
    
    # 3. Inicializar modelo para obtener dimensión
    modelo = SentenceTransformer(MODELO_EMBEDDINGS)
    dimension = modelo.get_sentence_embedding_dimension()
    
    # 4. Crear índice
    crear_indice_pinecone(pc, cv_config['indice'], dimension)
    
    # 5. Cargar vectores
    cargar_vectores_a_pinecone(
        pc,
        cv_config['indice'],
        documentos,
        MODELO_EMBEDDINGS,
        cv_config['persona']
    )


# ================================
# FUNCIÓN PRINCIPAL
# ================================

def main():
    """Función principal del script."""
    print("=" * 60)
    print("TP3 - Cargar Múltiples CVs a Base de Datos Vectorial")
    print("=" * 60)
    
    try:
        # Configurar Pinecone
        pc = configurar_pinecone()
        
        # Procesar cada CV
        for cv_config in CVS_CONFIG:
            procesar_cv_completo(pc, cv_config)
            print("\n")
        
        print("=" * 60)
        print("[OK] PROCESO COMPLETADO EXITOSAMENTE")
        print("=" * 60)
        print("[INFO] Indices creados:")
        for cv_config in CVS_CONFIG:
            print(f"   - {cv_config['indice']} ({cv_config['persona']})")
        print(f"\n[INFO] Ahora puedes ejecutar tp3_interfaz.py para usar el agente")
        
    except Exception as e:
        print(f"\n[ERROR] Error durante la ejecucion: {str(e)}")
        raise


if __name__ == "__main__":
    main()

