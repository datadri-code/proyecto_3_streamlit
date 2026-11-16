# Titulo: Grafo y algoritmo de Dijkstra
# Autor: Adrián Carrera Ahumada
# Código: 225361598
# Fecha: 15/11/2026
# Descripcion: Clases Nodo y Grafo; calcula la ruta mas corta con Dijkstra.

from typing import Dict, List, Optional, Set, Tuple

INFINITO: float = float("inf")


class Nodo:
    """Un punto del mapa (estacion, colonia, ciudad) y sus conexiones."""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo con su nombre y sin vecinos."""
        self.nombre: str = nombre
        # vecinos guarda {nombre_del_vecino: peso_de_la_conexion}
        self.vecinos: Dict[str, float] = {}

    def agregar_vecino(self, nombre_vecino: str, peso: float) -> None:
        """Guarda una conexion hacia otro nodo con su costo."""
        self.vecinos[nombre_vecino] = peso


class Grafo:
    """Conjunto de nodos unidos por conexiones con peso."""

    def __init__(self) -> None:
        """Crea un grafo vacio."""
        # nodos guarda {nombre: objeto Nodo}
        self.nodos: Dict[str, Nodo] = {}

    def agregar_nodo(self, nombre: str) -> None:
        """Crea el nodo solo si todavia no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(self, origen: str, destino: str, peso: float) -> None:
        """Conecta dos nodos en ambos sentidos (grafo no dirigido)."""
        # Regla de negocio: Dijkstra no funciona con pesos negativos
        if peso < 0:
            raise ValueError("Dijkstra no admite pesos negativos")
        self.agregar_nodo(origen)
        self.agregar_nodo(destino)
        self.nodos[origen].agregar_vecino(destino, peso)
        self.nodos[destino].agregar_vecino(origen, peso)

    def dijkstra(
        self, origen: str, destino: str
    ) -> Tuple[Optional[float], Optional[List[str]]]:
        """Calcula la ruta mas corta entre origen y destino.

        Regresa (costo_total, ruta). Si algun nodo no existe o no hay
        camino entre ellos, regresa (None, None).
        """
        if origen not in self.nodos or destino not in self.nodos:
            return None, None

        # 1. Inicializar las 3 estructuras de seguimiento
        distancias: Dict[str, float] = {}
        previo: Dict[str, str] = {}
        visitados: Set[str] = set()
        for nombre in self.nodos:
            distancias[nombre] = INFINITO
            previo[nombre] = ""  # "" significa: aun no se de donde llegue
        distancias[origen] = 0

        while len(visitados) < len(self.nodos):
            # 2. Seleccionar el nodo NO visitado con menor distancia
            actual = ""
            menor = INFINITO
            for nombre in self.nodos:
                if nombre not in visitados and distancias[nombre] < menor:
                    menor = distancias[nombre]
                    actual = nombre

            # Si no encontramos ninguno, los que quedan son inalcanzables
            if actual == "":
                break
            # Al elegir el destino, su distancia ya es definitiva
            if actual == destino:
                break

            # 3. Relajar: mejorar a los vecinos si el nuevo camino es menor
            for vecino, peso in self.nodos[actual].vecinos.items():
                if vecino in visitados:
                    continue
                nueva_distancia = distancias[actual] + peso
                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    previo[vecino] = actual

            # 4. Marcar como visitado
            visitados.add(actual)

        if distancias[destino] == INFINITO:
            return None, None

        ruta = self.reconstruir_ruta(previo, destino)
        return distancias[destino], ruta

    def reconstruir_ruta(
        self, previo: Dict[str, str], destino: str
    ) -> List[str]:
        """Recorre 'previo' desde el destino hacia atras y lo invierte."""
        ruta: List[str] = []
        nodo = destino
        while nodo != "":
            ruta.append(nodo)
            nodo = previo[nodo]
        ruta.reverse()
        return ruta
