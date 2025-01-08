import numpy as np
import matplotlib.pyplot as plt
import pygame
import gra
import copy
import time
import math

display_width = 1920
display_height = 900
radius = 10

ga1 = gra.Grafo(False).grafoMalla(10,10)
gra.Grafo(False).saveGraph(ga1,1)
nodos = gra.Grafo(False).calcularNodos(ga1)
nodosNew = gra.Grafo(False).nodosPosicion(nodos)
nodosNewPosicion =  [0] * nodos


pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
screen.fill((0,0,0))

class QuadTree:
    """
    Implementación de un QuadTree para dividir un espacio bidimensional en regiones cuadradas.
    Optimizado para trabajar con grafos, especialmente en la búsqueda de nodos cercanos.
    """

    def __init__(self, boundary, capacity):
        """
        Inicializa un QuadTree.

        Parámetros:
        - boundary: Rectángulo que define el área de este QuadTree (x, y, w, h).
        - capacity: Número máximo de nodos que un nodo puede contener antes de dividirse.
        """
        self.boundary = boundary  # (x, y, w, h)
        self.capacity = capacity
        self.nodes = []  # Lista de nodos (id, (x, y))
        self.divided = False

    def insert(self, node):
        """
        Inserta un nodo en el QuadTree.

        Parámetros:
        - node: Tupla con el id y coordenadas del nodo (id, (x, y)).

        Retorna:
        - True si el nodo fue insertado, False si está fuera del límite.
        """
        node_id, (x, y) = node
        bx, by, bw, bh = self.boundary

        if not (bx <= x < bx + bw and by <= y < by + bh):
            return False

        if len(self.nodes) < self.capacity:
            self.nodes.append(node)
            return True

        if not self.divided:
            self.subdivide()

        return (self.northeast.insert(node) or
                self.northwest.insert(node) or
                self.southeast.insert(node) or
                self.southwest.insert(node))

    def subdivide(self):
        """
        Divide este QuadTree en cuatro subárboles.
        """
        x, y, w, h = self.boundary
        half_w = w / 2
        half_h = h / 2

        self.northeast = QuadTree((x + half_w, y, half_w, half_h), self.capacity)
        self.northwest = QuadTree((x, y, half_w, half_h), self.capacity)
        self.southeast = QuadTree((x + half_w, y + half_h, half_w, half_h), self.capacity)
        self.southwest = QuadTree((x, y + half_h, half_w, half_h), self.capacity)

        self.divided = True

    def query(self, range_rect, found=None):
        """
        Encuentra todos los nodos dentro de un rectángulo dado.

        Parámetros:
        - range_rect: Rectángulo de consulta (x, y, w, h).
        - found: Lista de nodos encontrados (opcional).

        Retorna:
        - Lista de nodos dentro del rango.
        """
        if found is None:
            found = []

        rx, ry, rw, rh = range_rect
        bx, by, bw, bh = self.boundary

        if not (bx + bw > rx and bx < rx + rw and by + bh > ry and by < ry + rh):
            return found

        for node_id, (px, py) in self.nodes:
            if rx <= px < rx + rw and ry <= py < ry + rh:
                found.append((node_id, (px, py)))

        if self.divided:
            self.northwest.query(range_rect, found)
            self.northeast.query(range_rect, found)
            self.southwest.query(range_rect, found)
            self.southeast.query(range_rect, found)

        return found

    def draw(self, ax):
        """
        Dibuja el QuadTree en un gráfico dado.

        Parámetros:
        - ax: Objeto de ejes de Matplotlib.
        """
        x, y, w, h = self.boundary
        # Dibujar el rectángulo del límite
        rect = plt.Rectangle((x, y), w, h, edgecolor='black', fill=False)
        ax.add_patch(rect)

        # Dibujar los nodos
        for node_id, (px, py) in self.nodes:
            ax.plot(px, py, 'bo')
            ax.text(px, py, str(node_id), color='blue', fontsize=8)

        # Dibujar subdivisiones
        if self.divided:
            self.northeast.draw(ax)
            self.northwest.draw(ax)
            self.southeast.draw(ax)
            self.southwest.draw(ax)

# Ejemplo de uso con grafos
def main():
    boundary = (0, 0, 400, 400)
    qt = QuadTree(boundary, 4)

    # Crear un grafo con nodos y posiciones aleatorias
    np.random.seed(0)
    graph_nodes = [(i, tuple(np.random.randint(0, 400, 2))) for i in range(20)]

    # Insertar los nodos en el QuadTree
    for node in graph_nodes:
        qt.insert(node)

    # Configurar el gráfico
    fig, ax = plt.subplots(figsize=(8, 8))
    qt.draw(ax)

    # Dibujar un rango de consulta
    range_rect = (150, 150, 100, 100)
    rx, ry, rw, rh = range_rect
    consulta_rect = plt.Rectangle((rx, ry), rw, rh, edgecolor='red', fill=False, linestyle='--')
    ax.add_patch(consulta_rect)

    # Consultar y dibujar los nodos encontrados
    found_nodes = qt.query(range_rect)
    for node_id, (px, py) in found_nodes:
        ax.plot(px, py, 'ro')
        ax.text(px, py, str(node_id), color='red', fontsize=8)

    ax.set_xlim(0, 400)
    ax.set_ylim(0, 400)
    ax.set_aspect('equal')
    plt.show()

if __name__ == "__main__":
    main()
