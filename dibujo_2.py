import pygame
import gra
import copy
import time
import math
#from graph_data import graph

display_width = 1920
display_height = 900
radius = 10
C1 = 2 # Constante de atracción
C2 = 500 # Constante de repulsión
C3 = 1 # Coeficiente de movimiento
C4 = .5# fuerza del algoritmo
ITERACIONES = 700 # Coeficiente de movimiento
umbral_distancia = 5 
area = 10000
temp = 100
damp = .993




#ga1 = gra.Grafo(False).grafoMalla(4,4)
ga1 = gra.Grafo(False).grafoMalla(4,4)
gra.Grafo(False).saveGraph(ga1,1)
nodos = gra.Grafo(False).calcularNodos(ga1)
nodosNew = gra.Grafo(False).nodosPosicion(nodos)
nodosNewPosicion =  [0] * nodos
#k = C4 * math.sqrt(area / nodos)
k = 50

pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
screen.fill((0,0,0))


for j in range(1,ITERACIONES):
    screen.fill((0,0,0))    
    for l in nodosNew:
        pygame.draw.circle(screen,(0,150,150),l.posicion,radius)

    # fueza de atracción 
    for p in ga1:
        posicion1 = nodosNew[p.idConexion[1]-1].posicion
        posicion2 = nodosNew[p.idConexion[0]-1].posicion
        pygame.draw.line(screen,(255,255,255),posicion1,posicion2)
    pygame.display.flip()
    fuerza2 = 0
    newx = 0
    newy = 0
    for e in range(0,nodos):
        fuerza2 = 0
        newx = 0
        newy = 0
        newx2 = 0
        newy2 = 0
        for e2 in range(0,nodos):
            if e != e2:
                terminox = ((nodosNew[e].posicion[0]) - (nodosNew[e2].posicion[0]))
                terminoy = ((nodosNew[e].posicion[1]) - (nodosNew[e2].posicion[1]))
                distancia = math.sqrt(terminox ** 2 + terminoy ** 2) or 1
                #fuerza2 = C2/(distancia)
                #if distancia < umbral_distancia:
                fuerza2 = (k**2)/distancia
                newx += (fuerza2 * terminox / distancia) /2
                newy += (fuerza2 * terminoy / distancia) /2
                newx2 -= (fuerza2 * terminox / distancia) /2
                newy2 -= (fuerza2 * terminoy / distancia)/2
                        #cordenadasNuevas = [newx,newy]
                nodosNewPosicion[e2] = [newx,newy]
                nodosNewPosicion[e] = [newx2,newy2]
                #else: 
                    #nodosNewPosicion[e] = [nodosNew[e].posicion[0],nodosNew[e].posicion[1]]
        
    for i in ga1:
        terminox = ((nodosNew[i.idConexion[0]-1].posicion[0]) - (nodosNew[i.idConexion[1]-1].posicion[0]))
        terminoy = ((nodosNew[i.idConexion[0]-1].posicion[1]) - (nodosNew[i.idConexion[1]-1].posicion[1]))
        distancia = math.sqrt(terminox**2 + terminoy**2) or 1
        #if distancia < umbral_distancia:
        #fuerza = 
        nodosNewPosicion[i.idConexion[0]-1][0] += distancia * terminox / k
        nodosNewPosicion[i.idConexion[0]-1][1] += distancia * terminoy / k
        nodosNewPosicion[i.idConexion[1]-1][0] -= distancia * terminox / k
        nodosNewPosicion[i.idConexion[1]-1][1] -= distancia * terminoy / k
        #else: 
            #nodosNewPosicion[e] = [nodosNew[e].posicion[0],nodosNew[e].posicion[1]]

    #distancia_superpuesta = 1
    for e in range(0,nodos):
        fuerzax = 0
        fuerzay = 0
        newx = 0
        newy = 0
        terminox = (nodosNew[e].posicion[0])
        terminoy = (nodosNew[e].posicion[1])
        distancia = math.sqrt(terminox ** 2 + terminoy ** 2) or 1
        fuerzax = distancia * terminox / k
        fuerzay = distancia * terminoy / k
        newx = nodosNew[e].posicion[0] - (fuerzax/10)
        newy = nodosNew[e].posicion[1] - (fuerzay/10)
        nodosNewPosicion[e] = [newx,newy]

    
    x = 0
    y = 0
    newx = 0
    newy = 0
    for n in range(0,nodos):
        x = 0
        y = 0
        newx = 0
        newy = 0
        modulo = math.sqrt(nodosNewPosicion[n][0] ** 2 + nodosNewPosicion[n][1] ** 2)
        if modulo > temp:
            nodosNewPosicion[n][0] *= temp / modulo
            nodosNewPosicion[n][1] *= temp / modulo
        print(nodosNewPosicion[n])
        x = (C3 * (nodosNewPosicion[n][0] + nodosNew[n].posicion[0]))
        #x = (C3 * (nodosNewPosicion[n][0] + nodosNew[n].posicion[0]))
        y = (C3 * (nodosNewPosicion[n][1] + nodosNew[n].posicion[1]))
        #nodosNew[n].posicion[0] += C3 * nodosNewPosicion[n][0]
        #nodosNew[n].posicion[1] += C3 * nodosNewPosicion[n][1]
        #nodo[1] += C3 * nodo[3]
        nodosNew[n].posicion = (x,y)   
        #print(nodosNew[n].posicion)  

        #if x > 960 and y < 450:
        #x = (x+100)/1.009
        #y = (y+50)/1.00
        #elif x <= 960 and y < 450:
         #   x = x+20
          #  y = y+20
        #elif x <= 960 and y >= 450:
         #   x = x+20
          #  y = y-20
        #else: 
         #   x = x-20
          #  y = y-20
        #x =  max(20, min(1920 - 20, nodosNew[n].posicion[0]))
        #y =  max(20, min(900 - 20, nodosNew[n].posicion[1]))
        #nodosNew[n].posicion = (x,y)  

        #nodosNew[n].posicion = (newx,newy) 
    temp *= damp

while(1):
    clock.tick(30)