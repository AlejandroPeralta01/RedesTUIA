# REDES DE DATOS

Este proyecto incluye un entorno virtual para la gestión de dependencias de Python y permite instalar todos los requisitos necesarios desde un archivo `requirements.txt`.

## Requisitos Previos

Asegúrate de que tu sistema cumpla con los siguientes requisitos antes de empezar:

- Python instalado (versión 3.8 o superior recomendada).
- Administrador de paquetes `pip` incluido con tu instalación de Python.

## Pasos de Instalación

Sigue los pasos a continuación para configurar y ejecutar el entorno del proyecto:

### 1. Verificar que Python esté instalado

Ejecuta el siguiente comando para verificar que Python esté instalado correctamente en tu sistema:

```bash
python --version
```

Deberías ver algo similar a:

```bash
Python 3.x.x
```

Si no está instalado, descarga Python desde [python.org](https://www.python.org/downloads/).

---

### 2. Crear un entorno virtual

Para aislar las dependencias del proyecto, crea un entorno virtual con el siguiente comando:

```bash
python -m venv env
```

Esto creará una carpeta llamada `env` que contiene el entorno virtual.

---

### 3. Activar el entorno virtual

#### En Windows:

```bash
.\env\Scripts\activate
```

#### En macOS/Linux:

```bash
source env/bin/activate
```

Una vez activado, deberías ver el prefijo `(env)` en tu terminal.

---

### 4. Instalar dependencias

Con el entorno virtual activado, instala las dependencias necesarias desde el archivo `requirements.txt` ejecutando:

```bash
pip install -r requirements.txt
```

Esto instalará todos los paquetes listados en el archivo `requirements.txt`.

---

## Ejecución del Proyecto

Una vez que el entorno esté configurado y las dependencias instaladas, puedes ejecutar el script principal de tu proyecto (si existe) con:

(para el servidor)
```bash
python server.py
```

(para el cliente)
```bash
python client.py
```

