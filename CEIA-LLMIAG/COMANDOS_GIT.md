# Comandos Git - Verificar Repositorio

## 🔍 Comandos para Verificar el Repositorio

### 1. Ver Remotes (Repositorios Remotos)
```bash
git remote -v
```
**Qué muestra**: Todos los repositorios remotos configurados (origin, upstream, etc.) y sus URLs

### 2. Ver URL del Repositorio Remoto Principal
```bash
git remote get-url origin
```
**Qué muestra**: La URL del repositorio remoto principal (si existe)

### 3. Ver Todas las URLs de Remotes
```bash
git remote show origin
```
**Qué muestra**: Información detallada del remote 'origin' (URL, branches, etc.)

### 4. Verificar si es un Repositorio Git
```bash
git status
```
**Qué muestra**: Estado del repositorio (si es un repo Git válido)

### 5. Ver Configuración de Usuario Git
```bash
git config user.name
git config user.email
```
**Qué muestra**: Nombre y email configurados en Git (puede ser personal o del curso)

### 6. Ver Todas las Configuraciones
```bash
git config --list
```
**Qué muestra**: Todas las configuraciones de Git (usuario, remotes, etc.)

### 7. Ver Historial de Commits
```bash
git log --oneline -10
```
**Qué muestra**: Últimos 10 commits (para verificar actividad)

---

## 📋 Secuencia de Comandos Recomendada

Ejecuta estos comandos en orden para obtener toda la información:

```bash
# 1. Verificar que es un repo Git
git status

# 2. Ver remotes configurados
git remote -v

# 3. Ver URL del origin (si existe)
git remote get-url origin

# 4. Ver información detallada del remote
git remote show origin

# 5. Ver configuración de usuario
git config user.name
git config user.email
```

---

## 🔍 Interpretación de Resultados

### Si `git remote -v` muestra algo como:
```
origin  https://github.com/usuario/repo.git (fetch)
origin  https://github.com/usuario/repo.git (push)
```
→ El repositorio está vinculado a ese GitHub

### Si muestra:
```
origin  https://github.com/CEIA-LLMIAG/PLN2.git (fetch)
origin  https://github.com/CEIA-LLMIAG/PLN2.git (push)
```
→ El repositorio está vinculado al repositorio del curso

### Si no muestra nada:
→ El repositorio es local, no tiene remotes configurados

### Si `git status` dice "not a git repository":
→ No es un repositorio Git, necesitas inicializarlo con `git init`

---

## 💡 Comandos Útiles Adicionales

### Ver Branch Actual
```bash
git branch
```

### Ver Último Commit
```bash
git log -1
```

### Ver Diferencias con el Remoto
```bash
git fetch
git status
```

---

## ⚠️ Si No Tienes Repositorio Remoto

Si quieres crear un repositorio en GitHub y vincularlo:

```bash
# 1. Crear repo en GitHub (desde la web)

# 2. Agregar remote
git remote add origin https://github.com/tu-usuario/tu-repo.git

# 3. Verificar
git remote -v

# 4. Hacer push (si tienes commits)
git push -u origin main
```

---

**Nota**: Ejecuta estos comandos desde la raíz del proyecto para obtener la información completa.



