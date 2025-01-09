import pygame
import gra
import copy
import time
import math

# Configuración de Pygame
ANCHO, ALTO = 1820, 980
FPS = 60
pygame.init()
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Visualización de Grafos - Barnes-Hut")
reloj = pygame.time.Clock()

# Parámetros del modelo de resortes
atraccion = 0.05  # Constante de fuerza atractiva
repulsion = 10  # Constante de fuerza repulsiva
FRICCION = 0.97  # Incrementar fricción para estabilizar
MAX_VELOCIDAD = 5  # Limitar la velocidad máxima de los nodos
MIN_DISTANCIA = 5  # Evitar explosiones por nodos demasiado cercanos
THETA = 0.5  # Parámetro de apertura para Barnes-Hut

# Generar grafo utilizando el modelo deseado
aristas = gra.Grafo(False).grafoMalla(10,10)

# Extraer nodos y aristas del grafo
#nodos = {nodo.id: [random.randint(10, ANCHO - 10), random.randint(10, ALTO - 10)] for nodo in grafo.nodos}
#aristas = [(arista.nodo1.id, arista.nodo2.id) for arista in grafo.aristas]
nodos = gra.Grafo(False).calcularNodos(aristas)
posiciones = gra.Grafo(False).nodosPosicion(nodos)
#print(aristas)

# Función para calcular distancia entre dos nodos
def distancia(nodo1, nodo2):
    dx = nodo2[0] - nodo1[0] 
    dy = nodo2[1] - nodo1[1]
    dist = math.sqrt(dx**2 + dy**2)
    return dist, dx, dy

# Clase para el QuadTree
class QuadTree:
    def __init__(self, x, y, ancho, alto):
        self.x = x
        self.y = y
        self.ancho = ancho
        self.alto = alto
        self.nodos = []
        self.dividido = False
        self.centro_de_masa = None
        self.masa_total = 0

    def insertar(self, nodo_id, pos):
        if not (self.x <= pos[0] < self.x + self.ancho and self.y <= pos[1] < self.y + self.alto):
            return False

        if len(self.nodos) < 1 and not self.dividido:
            self.nodos.append((nodo_id, pos))
            return True

        if not self.dividido:
            self.subdividir()

        for subcuadro in self.subcuadros:
            if subcuadro.insertar(nodo_id, pos):
                return True

        return False

    def subdividir(self):
        w, h = self.ancho / 2, self.alto / 2
        self.subcuadros = [
            QuadTree(self.x, self.y, w, h),
            QuadTree(self.x + w, self.y, w, h),
            QuadTree(self.x, self.y + h, w, h),
            QuadTree(self.x + w, self.y + h, w, h)
        ]
        for nodo_id, pos in self.nodos:
            for subcuadro in self.subcuadros:
                if subcuadro.insertar(nodo_id, pos):
                    break
        self.nodos = []
        self.dividido = True

    def calcular_centro_de_masa(self):
        if self.dividido:
            masa_total = 0
            centro_x, centro_y = 0, 0
            for subcuadro in self.subcuadros:
                subcuadro.calcular_centro_de_masa()
                if subcuadro.masa_total > 0:
                    masa_total += subcuadro.masa_total
                    centro_x += subcuadro.centro_de_masa[0] * subcuadro.masa_total
                    centro_y += subcuadro.centro_de_masa[1] * subcuadro.masa_total
            if masa_total > 0:
                self.centro_de_masa = (centro_x / masa_total, centro_y / masa_total)
                self.masa_total = masa_total
        elif self.nodos:
            self.centro_de_masa = self.nodos[0][1]
            self.masa_total = 1

    def calcular_fuerza(self, nodo_id, nodo_pos, theta, fuerza):
        if self.masa_total == 0 or self.centro_de_masa is None or nodo_id in [n[0] for n in self.nodos]:
            return

        dx = self.centro_de_masa[0] - nodo_pos[0]
        dy = self.centro_de_masa[1] - nodo_pos[1]
        dist = math.sqrt(dx**2 + dy**2)

        if dist < MIN_DISTANCIA:
            return

        if (self.ancho / dist) < theta or not self.dividido:
            fuerza_repulsiva = repulsion * self.masa_total / (dist**2)
            fuerza[0] -= fuerza_repulsiva * dx / dist
            fuerza[1] -= fuerza_repulsiva * dy / dist
        else:
            for subcuadro in self.subcuadros:
                subcuadro.calcular_fuerza(nodo_id, nodo_pos, theta, fuerza)

# Simulación de fuerzas
velocidades = {i: [0, 0] for i in range(0,nodos)}

# Número de iteraciones que quieres que dure la simulación
NUM_ITERACIONES = 1000

# Bucle principal con un número limitado de iteraciones
ejecutando = True
iteracion = 0  # Contador de iteraciones

while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False

    # Si hemos alcanzado el número máximo de iteraciones, terminamos el bucle
    if iteracion >= NUM_ITERACIONES:
        ejecutando = False

    # Inicializar fuerzas
    fuerzas = {i: [0, 0] for i in range(0,nodos)}

    # Crear el QuadTree
    quadtree = QuadTree(0, 0, ANCHO, ALTO)
    for nodo_id in range(1,nodos+1):
        quadtree.insertar(nodo_id, posiciones[nodo_id-1].posicion)
    quadtree.calcular_centro_de_masa()

    # Calcular fuerzas repulsivas usando Barnes-Hut
    for nodo_id in range(1,nodos+1):
        quadtree.calcular_fuerza(nodo_id, posiciones[nodo_id-1].posicion, THETA, fuerzas[nodo_id-1])

    # Calcular fuerzas atractivas
    for i in aristas:
        dist, dx, dy = distancia(posiciones[i.idConexion[0]-1].posicion, posiciones[i.idConexion[1]-1].posicion)
        if dist > 0:
            fuerza_atractiva = atraccion * math.log(dist + 1)
            fuerzas[i.idConexion[0]-1][0] += fuerza_atractiva * dx / dist
            fuerzas[i.idConexion[0]-1][1] += fuerza_atractiva * dy / dist
            fuerzas[i.idConexion[1]-1][0] -= fuerza_atractiva * dx / dist
            fuerzas[i.idConexion[1]-1][1] -= fuerza_atractiva * dy / dist

    # Actualización de posiciones
    for i in range(0,nodos):
        # Actualizar velocidad
        velocidades[i][0] = max(-MAX_VELOCIDAD, min(MAX_VELOCIDAD, (velocidades[i][0] + fuerzas[i][0]) * FRICCION))
        velocidades[i][1] = max(-MAX_VELOCIDAD, min(MAX_VELOCIDAD, (velocidades[i][1] + fuerzas[i][1]) * FRICCION))
        
        # Actualizar posición
        #print(nodos[i][0])
        x = posiciones[i].posicion[0] + velocidades[i][0]
        y = posiciones[i].posicion[1] + velocidades[i][1]
        posiciones[i].posicion = (x,y)

        # Asegurar que los nodos estén dentro de los límites de la ventana
        x = max(10, min(ANCHO - 10, posiciones[i].posicion[0]))  # Limitar en X
        y = max(10, min(ALTO - 10, posiciones[i].posicion[1]))    # Limitar en Y
        posiciones[i].posicion = (x,y)

    # Dibujar en Pygame
    pantalla.fill((255, 255, 255))
    
    # Dibujar aristas
    #for nodo1, nodo2 in posiciones:
    #    pygame.draw.line(pantalla, (200, 200, 200), nodos[nodo1], nodos[nodo2], 1)

    for p in aristas:
        posicion1 = posiciones[p.idConexion[1]-1].posicion
        posicion2 = posiciones[p.idConexion[0]-1].posicion
        #pygame.draw.line(screen,(255,255,255),posicion1,posicion2)  
        pygame.draw.line(pantalla, (200, 200, 200), posicion1, posicion2, 1)  

    # Dibujar nodos
    #for i in nodos:
    #   pygame.draw.circle(pantalla, (0, 0, 255), (int(nodos[i][0]), int(nodos[i][1])), 5)

    for l in posiciones:
            pygame.draw.circle(pantalla,(0,150,150),l.posicion,5)    

    # Dibujar el QuadTree
    def dibujar_quadtree(quadtree):
        pygame.draw.rect(pantalla, (150, 150, 150), (quadtree.x, quadtree.y, quadtree.ancho, quadtree.alto), 1)
        if quadtree.dividido:
            for subcuadro in quadtree.subcuadros:
                dibujar_quadtree(subcuadro)

    dibujar_quadtree(quadtree)

    pygame.display.flip()
    reloj.tick(FPS)
    
    iteracion += 1  # Incrementar el contador de iteraciones

# Cerrar Pygame después de finalizar las iteraciones
pygame.quit()