# Titulo: Interfaz web de la red de transporte (Proyecto 3)
# Autor: Adrián Carrera Ahumada
# Código: 225361598
# Fecha: 16/11/2026
# Descripcion: App en Streamlit para registrar conexiones y usar Dijkstra.

from typing import List, Tuple

import pandas as pd
import streamlit as st

from grafo import Grafo
from io_handler import (
    ARCHIVO_CSV,
    ENCABEZADOS,
    construir_grafo,
    convertir_peso,
    guardar_conexion,
    leer_conexiones,
)


def inicializar_estado() -> None:
    """Lee el CSV UNA sola vez y guarda los datos en session_state.

    Streamlit vuelve a ejecutar todo el archivo en cada clic. Gracias al
    'if', la lectura del disco solo ocurre la primera vez.
    """
    if "grafo" not in st.session_state:
        conexiones, avisos = leer_conexiones(ARCHIVO_CSV)
        st.session_state.conexiones = conexiones
        st.session_state.avisos = avisos
        st.session_state.grafo = construir_grafo(conexiones)


def mostrar_avisos_de_carga() -> None:
    """Muestra las filas del CSV que se omitieron al cargar."""
    avisos: List[str] = st.session_state.avisos
    if len(avisos) > 0:
        with st.expander(f"Avisos de carga ({len(avisos)})", expanded=True):
            for aviso in avisos:
                st.warning(aviso)


def registrar_conexion(origen: str, destino: str, texto_peso: str) -> None:
    """Valida los datos, los guarda en el CSV y actualiza la memoria."""
    try:
        if origen == "" or destino == "":
            raise ValueError("el origen y el destino no pueden quedar vacios")
        if origen == destino:
            raise ValueError("el origen y el destino deben ser distintos")
        peso = convertir_peso(texto_peso)
        guardar_conexion(origen, destino, peso, ARCHIVO_CSV)
    except ValueError as error:
        st.sidebar.error(f"Dato invalido: {error}.")
    except PermissionError:
        st.sidebar.error(f"No hay permiso para escribir en {ARCHIVO_CSV}.")
    else:
        # Se actualiza el grafo en memoria SIN volver a leer el CSV
        st.session_state.grafo.agregar_arista(origen, destino, peso)
        st.session_state.conexiones.append((origen, destino, peso))
        st.sidebar.success(f"Guardada: {origen} <-> {destino} ({peso})")


def mostrar_registro() -> None:
    """Barra lateral con los campos para agregar una conexion."""
    st.sidebar.header("Registrar conexion")
    origen = st.sidebar.text_input("Nodo origen").strip()
    destino = st.sidebar.text_input("Nodo destino").strip()
    texto_peso = st.sidebar.text_input("Peso (minutos)").strip()
    if st.sidebar.button("Guardar conexion"):
        registrar_conexion(origen, destino, texto_peso)


def mostrar_red() -> None:
    """Muestra un resumen y la tabla de conexiones con pandas."""
    st.header("Red actual")
    grafo: Grafo = st.session_state.grafo
    conexiones: List[Tuple[str, str, float]] = st.session_state.conexiones

    if len(conexiones) == 0:
        st.info("No hay conexiones. Registra una en la barra lateral.")
        return

    columna_nodos, columna_conexiones = st.columns(2)
    columna_nodos.metric("Nodos", len(grafo.nodos))
    columna_conexiones.metric("Conexiones", len(conexiones))

    tabla = pd.DataFrame(conexiones, columns=ENCABEZADOS)
    st.dataframe(tabla, hide_index=True)


def calcular_y_mostrar_ruta(grafo: Grafo, origen: str, destino: str) -> None:
    """Valida los nodos, ejecuta Dijkstra y muestra el resultado."""
    if origen == "" or destino == "":
        st.warning("Escribe el nodo de inicio y el nodo de destino.")
        return
    if origen not in grafo.nodos:
        st.error(f"El nodo '{origen}' no existe en la red.")
        return
    if destino not in grafo.nodos:
        st.error(f"El nodo '{destino}' no existe en la red.")
        return

    distancia, ruta = grafo.dijkstra(origen, destino)
    if distancia is None or ruta is None:
        st.warning(f"No existe un camino entre {origen} y {destino}.")
        return

    st.success("Ruta: " + " -> ".join(ruta))
    columna_costo, columna_paradas = st.columns(2)
    columna_costo.metric("Costo total", f"{distancia} min")
    columna_paradas.metric("Nodos en la ruta", len(ruta))


def mostrar_calculo_ruta() -> None:
    """Campos de inicio y destino lado a lado, y boton para calcular."""
    st.header("Calcular ruta mas corta")
    grafo: Grafo = st.session_state.grafo
    st.caption("Nodos disponibles: " + ", ".join(grafo.nodos))

    columna_inicio, columna_destino = st.columns(2)
    with columna_inicio:
        origen = st.text_input("Nodo de inicio").strip()
    with columna_destino:
        destino = st.text_input("Nodo de destino").strip()

    if st.button("Calcular ruta", type="primary"):
        calcular_y_mostrar_ruta(grafo, origen, destino)


def main() -> None:
    """Arma la pagina en orden, de arriba hacia abajo."""
    st.set_page_config(page_title="Red de transporte", layout="wide")
    st.title("Red de transporte - Dijkstra")
    inicializar_estado()
    mostrar_avisos_de_carga()
    # El registro va antes de la tabla para que una conexion nueva
    # aparezca en la tabla en el mismo clic
    mostrar_registro()
    mostrar_red()
    mostrar_calculo_ruta()


if __name__ == "__main__":
    main()
