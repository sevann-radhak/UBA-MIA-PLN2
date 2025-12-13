# -*- coding: utf-8 -*-
"""
TP3 - Script de Verificación
=============================

Verifica que todos los componentes del sistema TP3 están funcionando correctamente.

Autor: TP3 - Clase VII - CEIA LLMIAG
"""

import os
import sys
import io
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Cargar .env desde la raíz del proyecto
env_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', '.env')
load_dotenv(env_path)
# También intentar cargar desde directorio actual
load_dotenv()

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def verificar_env():
    """Verifica que las variables de entorno están configuradas."""
    print("=" * 60)
    print("1. Verificando Variables de Entorno")
    print("=" * 60)
    
    pinecone_key = os.getenv("PINECONE_API_KEY")
    groq_key = os.getenv("GROQ_API_KEY")
    pinecone_env = os.getenv("PINECONE_ENVIRONMENT", "us-east-1-aws")
    
    errores = []
    
    if not pinecone_key:
        errores.append("[ERROR] PINECONE_API_KEY no esta configurada")
    else:
        print("[OK] PINECONE_API_KEY configurada")
    
    if not groq_key:
        errores.append("[ERROR] GROQ_API_KEY no esta configurada")
    else:
        print("[OK] GROQ_API_KEY configurada")
    
    print(f"[OK] PINECONE_ENVIRONMENT: {pinecone_env}")
    
    if errores:
        print("\n[ADVERTENCIA] Errores encontrados:")
        for error in errores:
            print(f"   {error}")
        return False
    
    print("\n[OK] Todas las variables de entorno estan configuradas")
    return True


def verificar_archivos():
    """Verifica que los archivos necesarios existen."""
    print("\n" + "=" * 60)
    print("2. Verificando Archivos")
    print("=" * 60)
    
    archivos_requeridos = [
        "tp3_cargar_cvs.py",
        "tp3_decisor.py",
        "tp3_rag_tools.py",
        "tp3_agente.py",
        "tp3_interfaz.py",
        "cvs/cv_alumno.txt",
        "cvs/cv_pedro.txt",
        "cvs/cv_ana.txt"
    ]
    
    errores = []
    for archivo in archivos_requeridos:
        ruta = os.path.join(os.path.dirname(__file__), archivo)
        if os.path.exists(ruta):
            print(f"[OK] {archivo}")
        else:
            errores.append(f"[ERROR] {archivo} no encontrado")
            print(f"[ERROR] {archivo}")
    
    if errores:
        print("\n[ADVERTENCIA] Archivos faltantes:")
        for error in errores:
            print(f"   {error}")
        return False
    
    print("\n[OK] Todos los archivos necesarios estan presentes")
    return True


def verificar_pinecone():
    """Verifica conexión con Pinecone y existencia de índices."""
    print("\n" + "=" * 60)
    print("3. Verificando Conexión con Pinecone")
    print("=" * 60)
    
    try:
        from pinecone import Pinecone
        
        api_key = os.getenv("PINECONE_API_KEY")
        if not api_key:
            print("[ERROR] PINECONE_API_KEY no configurada")
            return False
        
        pc = Pinecone(api_key=api_key)
        indices = pc.list_indexes().names()
        
        print(f"[OK] Conexion con Pinecone exitosa")
        print(f"[INFO] Indices disponibles: {len(indices)}")
        
        indices_requeridos = [
            "cv-alumno-tp3",
            "cv-pedro-tp3",
            "cv-ana-tp3"
        ]
        
        indices_faltantes = []
        for indice in indices_requeridos:
            if indice in indices:
                stats = pc.Index(indice).describe_index_stats()
                print(f"[OK] {indice} existe ({stats['total_vector_count']} vectores)")
            else:
                indices_faltantes.append(indice)
                print(f"[ERROR] {indice} no existe")
        
        if indices_faltantes:
            print(f"\n[ADVERTENCIA] Indices faltantes: {', '.join(indices_faltantes)}")
            print("[INFO] Ejecuta: python tp3_cargar_cvs.py")
            return False
        
        print("\n[OK] Todos los indices necesarios existen")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al verificar Pinecone: {e}")
        return False


def verificar_groq():
    """Verifica conexión con Groq."""
    print("\n" + "=" * 60)
    print("4. Verificando Conexión con Groq")
    print("=" * 60)
    
    try:
        from groq import Groq
        
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            print("[ERROR] GROQ_API_KEY no configurada")
            return False
        
        cliente = Groq(api_key=api_key)
        
        # Prueba simple
        respuesta = cliente.chat.completions.create(
            messages=[{"role": "user", "content": "Hola"}],
            model="llama-3.1-8b-instant",
            max_tokens=10
        )
        
        print("[OK] Conexion con Groq exitosa")
        print(f"[OK] Modelo responde correctamente")
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al verificar Groq: {e}")
        return False


def verificar_componentes():
    """Verifica que los componentes se pueden importar."""
    print("\n" + "=" * 60)
    print("5. Verificando Componentes")
    print("=" * 60)
    
    componentes = [
        ("tp3_decisor", "DecisorCV"),
        ("tp3_rag_tools", "RAGToolsManager"),
        ("tp3_agente", "AgenteCV")
    ]
    
    errores = []
    for modulo, clase in componentes:
        try:
            mod = __import__(modulo, fromlist=[clase])
            getattr(mod, clase)
            print(f"[OK] {modulo}.{clase} importado correctamente")
        except Exception as e:
            errores.append(f"[ERROR] Error al importar {modulo}.{clase}: {e}")
            print(f"[ERROR] {modulo}.{clase}")
    
    if errores:
        print("\n[ADVERTENCIA] Errores de importacion:")
        for error in errores:
            print(f"   {error}")
        return False
    
    print("\n[OK] Todos los componentes se pueden importar")
    return True


def main():
    """Función principal de verificación."""
    print("\n" + "=" * 60)
    print("TP3 - Verificación del Sistema")
    print("=" * 60)
    
    resultados = []
    
    resultados.append(("Variables de Entorno", verificar_env()))
    resultados.append(("Archivos", verificar_archivos()))
    resultados.append(("Pinecone", verificar_pinecone()))
    resultados.append(("Groq", verificar_groq()))
    resultados.append(("Componentes", verificar_componentes()))
    
    print("\n" + "=" * 60)
    print("RESUMEN DE VERIFICACIÓN")
    print("=" * 60)
    
    todos_ok = True
    for nombre, resultado in resultados:
        estado = "[OK]" if resultado else "[ERROR]"
        print(f"{nombre}: {estado}")
        if not resultado:
            todos_ok = False
    
    print("\n" + "=" * 60)
    if todos_ok:
        print("[OK] SISTEMA LISTO PARA USAR")
        print("=" * 60)
        print("\n[INFO] Proximos pasos:")
        print("   1. Ejecutar: streamlit run tp3_interfaz.py")
        print("   2. Hacer preguntas en la interfaz")
    else:
        print("[ADVERTENCIA] HAY PROBLEMAS QUE RESOLVER")
        print("=" * 60)
        print("\n[INFO] Revisa los errores arriba y corrijelos")
    
    return todos_ok


if __name__ == "__main__":
    exit(0 if main() else 1)

