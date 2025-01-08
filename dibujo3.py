import pygame
import gra
import copy
import time
import math
#from graph_data import graph

display_width = 1920
display_height = 900
radius = 10
C1 = 1 # Constante de atracción
C2 = 2  # Constante de repulsión
C3 = .5 # Coeficiente de movimiento
ITERACIONES = 700
umbral_distanacia = 50

ga1 = gra.Grafo(False).grafoMalla(10,10)
gra.Grafo(False).saveGraph(ga1,1)
nodos = gra.Grafo(False).calcularNodos(ga1)
nodosNew = gra.Grafo(False).nodosPosicion(nodos)
nodosNewPosicion =  [0] * nodos


pygame.init()
screen = pygame.display.set_mode((display_width,display_height))
clock = pygame.time.Clock()
screen.fill((0,0,0))


for j in range(1,ITERACIONES):
    screen.fill((0,0,0))    
    for l in nodosNew:
            pygame.draw.circle(screen,(0,150,150),l.posicion,radius)


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
        for e2 in range(0,nodos):
            if e != e2:
                terminox = ((nodosNew[e].posicion[0]) - (nodosNew[e2].posicion[0]))
                terminoy = ((nodosNew[e].posicion[1]) - (nodosNew[e2].posicion[1]))
                distancia = math.sqrt(terminox ** 2 + terminoy ** 2) or 1 
                if distancia < umbral_distanacia:
                    fuerza2 = (C2**2)/distancia
                    try:
                        newx = nodosNewPosicion[e][0] + (terminox / distancia) * fuerza2 
                        newy = nodosNewPosicion[e][1] + (terminoy / distancia) * fuerza2 
                    except:
                        newx = nodosNewPosicion[e] + (terminox / distancia) * fuerza2 
                        newy = nodosNewPosicion[e] + (terminoy / distancia) * fuerza2 
                    #cordenadasNuevas = [newx,newy]
                    #print(newx,newy)
                    nodosNewPosicion[e] = [newx,newy]      

    for i in ga1:
        terminox = ((nodosNew[i.idConexion[0]-1].posicion[0]) - (nodosNew[i.idConexion[1]-1].posicion[0]))
        terminoy = ((nodosNew[i.idConexion[0]-1].posicion[1]) - (nodosNew[i.idConexion[1]-1].posicion[1]))
        distancia = math.sqrt(terminox**2 + terminoy**2) or 1
        if distancia < umbral_distanacia:
            fuerza = (distancia**2) / C1
            nodosNewPosicion[i.idConexion[0]-1][0] += (terminox / distancia) * fuerza 
            nodosNewPosicion[i.idConexion[0]-1][1] += (terminoy / distancia) * fuerza 
            nodosNewPosicion[i.idConexion[1]-1][0] -= (terminox / distancia) * fuerza 
            nodosNewPosicion[i.idConexion[1]-1][1] -= (terminoy / distancia) * fuerza 

    for e in range(0,nodos):
        fuerza2 = 0
        newx = 0
        newy = 0
        newx2 = 0
        newy2 = 0
        for e2 in range(0,nodos):
            if e != e2:
                try:
                    terminox = ((nodosNew[e].posicion[0]) - (nodosNew[e2].posicion[0]))
                    terminoy = ((nodosNew[e].posicion[1]) - (nodosNew[e2].posicion[1]))
                    distancia = math.sqrt(terminox ** 2 + terminoy ** 2) or 1 
                    if distancia < umbral_distanacia:
                        distancia_superpuesta = umbral_distanacia - distancia
                        newx =  ((terminox / distancia) * (distancia_superpuesta /2)) 
                        newy =  ((terminox / distancia) * (distancia_superpuesta /2)) 
                        newx2 = ((terminox / distancia) * (distancia_superpuesta /2)) 
                        newy2 = ((terminox / distancia) * (distancia_superpuesta /2)) 
                        nodosNew[e].posicion[0] += newx
                        nodosNew[e].posicion[1] += newy
                        nodosNew[e2].posicion[0] += newx2
                        nodosNew[e2].posicion[1] -= newy2
                except:
                    None

    for n in range(0,nodos):
        x = 0
        y = 0
        newx = 0
        newy = 0
        try: 
            x = nodosNewPosicion[n][0]
            y = nodosNewPosicion[n][1]
            distancia = math.sqrt(x**2 + y**2) or 0.01
            if distancia > C3:
                x = (C3 * (x / distancia))
                y = (C3 * (y / distancia))
            else:
                #x = (C3 * (nodosNewPosicion[n][0] + nodosNew[n].posicion[0]))
                #y = (C3 * (nodosNewPosicion[n][1] + nodosNew[n].posicion[1]))
                None
            x = min(max((nodosNew[n].posicion[0] + x), 0), 1920)
            y = min(max((nodosNew[n].posicion[1] + y), 0), 900)
            #x = (x + 150) / 20
            #y = (y + 50) / 20
 
            nodosNew[n].posicion = (x,y)   
            nodosNew[n].posicion = (x,y)  

        except: 
            None
        

while(1):
    clock.tick(30)