# Titulo: Red de transporte con Dijkstra (Proyecto 2)
# Autor: Adrián Carrera Ahumada
# Código: 225361598
# Fecha: 16/11/2026
# Descripcion: Menu de consola para capturar conexiones y calcular rutas.

from typing import List, Tuple

from io_handler import (
    ARCHIVO_CSV,
    ARCHIVO_JSON,
    construir_grafo,
    exportar_json,
    guardar_conexion,
    importar_json,
    leer_conexiones,
)


def leer_con_avisos() -> List[Tuple[str, str, float]]:
    """Lee el CSV y muestra en consola los avisos de filas omitidas."""
    conexiones, avisos = leer_conexiones()
    for aviso in avisos:
        print("Aviso: " + aviso)
    return conexiones


def pedir_nombre(mensaje: str) -> str:
    """Pide el nombre de un nodo hasta que el usuario escriba algo."""
    while True:
        nombre = input(mensaje).strip()
        if nombre != "":
            return nombre
        print("Error: el nombre no puede quedar vacio.")


def pedir_peso(mensaje: str) -> float:
    """Pide el peso hasta que sea un numero mayor que 0."""
    while True:
        texto = input(mensaje).strip()
        try:
            peso = float(texto)
        except ValueError:
            if texto == "":
                print("Error: el peso no puede quedar vacio.")
            else:
                print(f"Error: '{texto}' no es un numero. Ejemplo: 7 o 2.5")
        else:
            if peso > 0:
                return peso
            print("Error: el peso debe ser mayor que 0.")


def agregar_conexion() -> None:
    """Pide una conexion al usuario y la guarda en el CSV."""
    print("\n--- Nueva conexion ---")
    origen = pedir_nombre("Nodo origen: ")
    destino = pedir_nombre("Nodo destino: ")
    if origen == destino:
        print("Error: el origen y el destino no pueden ser el mismo nodo.")
        return
    peso = pedir_peso("Peso (minutos): ")
    try:
        guardar_conexion(origen, destino, peso)
    except PermissionError:
        print(f"Error: no hay permiso para escribir en {ARCHIVO_CSV}.")
    else:
        print(f"Conexion guardada: {origen} <-> {destino} ({peso})")


def ver_conexiones() -> None:
    """Muestra todas las conexiones validas guardadas en el CSV."""
    conexiones = leer_con_avisos()
    if len(conexiones) == 0:
        print("No hay conexiones guardadas.")
        return
    print(f"\n--- {len(conexiones)} conexiones guardadas ---")
    for origen, destino, peso in conexiones:
        print(f"  {origen} <-> {destino}: {peso}")


def calcular_ruta() -> None:
    """Carga el grafo desde el CSV y calcula la ruta mas corta."""
    grafo = construir_grafo(leer_con_avisos())
    if len(grafo.nodos) == 0:
        print("El grafo esta vacio. Agrega conexiones primero.")
        return

    print("\nNodos disponibles:", ", ".join(grafo.nodos))
    origen = pedir_nombre("Nodo de inicio: ")
    destino = pedir_nombre("Nodo de destino: ")

    if origen not in grafo.nodos:
        print(f"Error: el nodo '{origen}' no existe.")
        return
    if destino not in grafo.nodos:
        print(f"Error: el nodo '{destino}' no existe.")
        return

    distancia, ruta = grafo.dijkstra(origen, destino)
    if distancia is None or ruta is None:
        print(f"No existe un camino entre {origen} y {destino}.")
    else:
        print("Ruta mas corta: " + " -> ".join(ruta))
        print(f"Peso total: {distancia}")


def exportar_a_json() -> None:
    """Copia las conexiones del CSV a un archivo JSON."""
    conexiones = leer_con_avisos()
    if len(conexiones) == 0:
        print("No hay conexiones para exportar.")
        return
    try:
        exportar_json(conexiones)
    except PermissionError:
        print(f"Error: no hay permiso para escribir en {ARCHIVO_JSON}.")
    else:
        print(f"Se exportaron {len(conexiones)} conexiones a {ARCHIVO_JSON}.")


def importar_desde_json() -> None:
    """Agrega al CSV las conexiones del JSON que todavia no existan."""
    nuevas, avisos = importar_json()
    for aviso in avisos:
        print("Aviso: " + aviso)
    if len(nuevas) == 0:
        print("No se importo ninguna conexion.")
        return
    existentes = leer_con_avisos()
    agregadas = 0
    try:
        for origen, destino, peso in nuevas:
            # Evita duplicar conexiones que ya estan en el CSV
            if (origen, destino, peso) not in existentes:
                guardar_conexion(origen, destino, peso)
                agregadas += 1
    except PermissionError:
        print(f"Error: no hay permiso para escribir en {ARCHIVO_CSV}.")
    else:
        print(f"Se agregaron {agregadas} conexiones nuevas al CSV.")


def mostrar_menu() -> None:
    """Imprime las opciones del menu principal."""
    print("\n===== Red de transporte - Dijkstra =====")
    print("1. Agregar conexion")
    print("2. Ver conexiones")
    print("3. Calcular ruta mas corta")
    print("4. Exportar conexiones a JSON")
    print("5. Importar conexiones desde JSON")
    print("6. Salir")


def main() -> None:
    """Ciclo principal: muestra el menu hasta que el usuario sale."""
    while True:
        mostrar_menu()
        opcion = input("Elige una opcion: ").strip()
        if opcion == "1":
            agregar_conexion()
        elif opcion == "2":
            ver_conexiones()
        elif opcion == "3":
            calcular_ruta()
        elif opcion == "4":
            exportar_a_json()
        elif opcion == "5":
            importar_desde_json()
        elif opcion == "6":
            print("Hasta luego.")
            break
        else:
            print("Opcion invalida. Escribe un numero del 1 al 6.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # El usuario presiono Ctrl+C: salimos sin mostrar el traceback
        print("\nPrograma terminado por el usuario.")
