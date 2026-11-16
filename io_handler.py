# Titulo: Manejo de archivos CSV y JSON
# Autor: Adrián Carrera Ahumada
# Código: 225361598
# Fecha: 16/11/2026
# Descripcion: Guarda y lee conexiones del grafo de forma segura.

import csv
import json
import os
from typing import List, Tuple

from grafo import Grafo

ARCHIVO_CSV: str = "nodos.csv"
ARCHIVO_JSON: str = "grafo.json"
ENCABEZADOS: List[str] = ["Origen", "Destino", "Peso"]


def convertir_peso(texto: str) -> float:
    """Convierte un texto en un peso valido (numero mayor que 0).

    Si no se puede, lanza ValueError con un mensaje en espanol.
    """
    if texto.strip() == "":
        raise ValueError("el peso no puede quedar vacio")
    try:
        peso = float(texto)
    except ValueError:
        raise ValueError(f"el peso '{texto}' no es un numero")
    if peso <= 0:
        raise ValueError("el peso debe ser mayor que 0")
    return peso


def guardar_conexion(
    origen: str, destino: str, peso: float, ruta: str = ARCHIVO_CSV
) -> None:
    """Agrega una conexion al final del CSV (modo append 'a')."""
    # Si el archivo aun no existe, primero hay que escribir los encabezados
    archivo_nuevo = not os.path.exists(ruta)
    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        if archivo_nuevo:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, peso])


def leer_conexiones(
    ruta: str = ARCHIVO_CSV,
) -> Tuple[List[Tuple[str, str, float]], List[str]]:
    """Lee el CSV fila por fila y regresa (conexiones, avisos).

    Las filas incompletas o con datos corruptos se omiten. Por cada una
    se agrega un aviso a la lista, para que quien llame decida si lo
    imprime en consola (main.py) o lo muestra en pantalla (app.py).
    """
    conexiones: List[Tuple[str, str, float]] = []
    avisos: List[str] = []
    try:
        with open(ruta, "r", newline="", encoding="utf-8") as archivo:
            lector = csv.DictReader(archivo)
            numero_fila = 1  # la fila 1 es la de encabezados
            for fila in lector:
                numero_fila += 1
                try:
                    origen = fila["Origen"].strip()
                    destino = fila["Destino"].strip()
                    peso = convertir_peso(fila["Peso"])
                    if origen == "" or destino == "":
                        raise ValueError("nombre de nodo vacio")
                except KeyError as error:
                    avisos.append(f"Fila {numero_fila} omitida: "
                                  f"falta la columna {error}.")
                except ValueError as error:
                    avisos.append(f"Fila {numero_fila} omitida: {error}.")
                except (AttributeError, TypeError):
                    # Pasa cuando a la fila le faltan valores (llegan None)
                    avisos.append(f"Fila {numero_fila} omitida: "
                                  "fila incompleta.")
                else:
                    # Solo se ejecuta si la fila no tuvo ningun error
                    conexiones.append((origen, destino, peso))
    except FileNotFoundError:
        avisos.append(f"No existe '{ruta}'. Se empieza sin conexiones.")
    return conexiones, avisos


def construir_grafo(conexiones: List[Tuple[str, str, float]]) -> Grafo:
    """Crea un objeto Grafo a partir de una lista de conexiones."""
    grafo = Grafo()
    for origen, destino, peso in conexiones:
        grafo.agregar_arista(origen, destino, peso)
    return grafo


def exportar_json(
    conexiones: List[Tuple[str, str, float]], ruta: str = ARCHIVO_JSON
) -> None:
    """Guarda la lista de conexiones en un archivo JSON."""
    lista_json = []
    for origen, destino, peso in conexiones:
        lista_json.append(
            {"origen": origen, "destino": destino, "peso": peso}
        )
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(lista_json, archivo, indent=4, ensure_ascii=False)


def importar_json(
    ruta: str = ARCHIVO_JSON,
) -> Tuple[List[Tuple[str, str, float]], List[str]]:
    """Lee las conexiones de un archivo JSON y regresa (conexiones, avisos)."""
    conexiones: List[Tuple[str, str, float]] = []
    avisos: List[str] = []
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            datos = json.load(archivo)
    except FileNotFoundError:
        avisos.append(f"No existe '{ruta}'.")
        return conexiones, avisos
    except json.JSONDecodeError:
        avisos.append(f"'{ruta}' no tiene un formato JSON valido.")
        return conexiones, avisos

    numero = 0
    for elemento in datos:
        numero += 1
        try:
            origen = str(elemento["origen"]).strip()
            destino = str(elemento["destino"]).strip()
            peso = convertir_peso(str(elemento["peso"]))
            if origen == "" or destino == "":
                raise ValueError("nombre de nodo vacio")
        except KeyError as error:
            avisos.append(f"Conexion {numero} omitida: falta {error}.")
        except ValueError as error:
            avisos.append(f"Conexion {numero} omitida: {error}.")
        except TypeError:
            # Pasa si el elemento no es un diccionario {"origen": ...}
            avisos.append(f"Conexion {numero} omitida: formato incorrecto.")
        else:
            conexiones.append((origen, destino, peso))
    return conexiones, avisos
