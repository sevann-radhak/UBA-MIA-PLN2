# Solución: Variables de Entorno no Encontradas

## Problema

Al ejecutar `tp3_verificar.py` desde `ClaseVII/codigo/`, no encuentra las variables de entorno porque el archivo `.env` está en la raíz del proyecto.

## Solución Implementada

Todos los scripts ahora buscan el `.env` en la raíz del proyecto automáticamente.

## Verificación

Ejecutar nuevamente:

```bash
cd CEIA-LLMIAG/ClaseVII/codigo
python tp3_verificar.py
```

Debería encontrar las variables de entorno correctamente.

## Si Aún No Funciona

### Opción 1: Verificar que .env existe en la raíz

El archivo `.env` debe estar en:
```
C:\Sevann\UBA\Maestria\2 bimestre\PLN2\.env
```

### Opción 2: Crear .env en el directorio de código

Alternativamente, puedes crear un `.env` en:
```
CEIA-LLMIAG/ClaseVII/codigo/.env
```

### Opción 3: Verificar contenido del .env

El archivo `.env` debe tener este formato (sin espacios alrededor del `=`):

```env
PINECONE_API_KEY=tu_api_key_aqui
PINECONE_ENVIRONMENT=us-east-1-aws
GROQ_API_KEY=tu_api_key_aqui
```

**Importante**: No debe haber espacios antes o después del `=`

### Opción 4: Verificar manualmente

Puedes verificar que las variables se cargan ejecutando:

```python
import os
from dotenv import load_dotenv

# Intentar cargar desde raíz
env_path = os.path.join('..', '..', '..', '.env')
load_dotenv(env_path)
load_dotenv()

print("PINECONE_API_KEY:", "✅ Configurada" if os.getenv("PINECONE_API_KEY") else "❌ No configurada")
print("GROQ_API_KEY:", "✅ Configurada" if os.getenv("GROQ_API_KEY") else "❌ No configurada")
```



