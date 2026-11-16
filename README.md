# Proyecto 3: Interfaz Web con Streamlit

**Alumno:** Adrián Carrera Ahumada
**Código:** 225361598
**Materia:** Programación III (Unidad 3)

Aplicación web en Streamlit que funciona como interfaz visual del grafo
(Proyecto 1) y del sistema de archivos CSV (Proyecto 2). Permite registrar
conexiones de una red de transporte de Guadalajara, verlas en una tabla y
calcular la ruta más corta con Dijkstra.

## Estructura

| Archivo | Descripción |
|---|---|
| `app.py` | Interfaz visual en Streamlit |
| `main.py` | Versión de consola (Proyecto 2) |
| `grafo.py` | Clases `Nodo` y `Grafo` con Dijkstra |
| `io_handler.py` | Lectura y escritura de `nodos.csv` y JSON |
| `nodos.csv` | Base de datos de conexiones |
| `requirements.txt` | Dependencias: flake8, pandas, streamlit |

## Cómo ejecutarlo

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

La versión de consola sigue disponible con `python3 main.py`.

## Características

- **Lectura única del CSV:** el grafo se guarda en `st.session_state` y el
  archivo solo se lee la primera vez que se abre la página.
- **Registro de conexiones** en la barra lateral (`st.sidebar`). Cada conexión
  válida se guarda en `nodos.csv` y se agrega al grafo en memoria.
- **Tabla de la red** con `pandas` y `st.dataframe`.
- **Cálculo de ruta** con campos de inicio y destino en columnas
  (`st.columns`).
- **Tolerancia a fallos:** pesos inválidos, nodos inexistentes y filas dañadas
  del CSV se muestran con `st.error` / `st.warning` sin detener la app.

## Validar estilo

```bash
flake8
```
