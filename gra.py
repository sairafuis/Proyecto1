from math import sqrt
import random

#Clase de nodo.
class Nodo:
	def __init__(self,idNodo):
		self.idNodo = idNodo

	def mostrarDatos(self):
		print("ID Nodo", self.idNodo)

#Clase de vertice.
class Vertice:
	def __init__(self,idConexion):
		self.idConexion = idConexion

	def mostrarDatos(self):
		print("Conexion: ", self.idConexion)

#Clase de grafo
class Grafo(Nodo,Vertice):
	def __init__(self,dirigido):
		self.dirigido = dirigido

	def crearNode(self,id):
		nodos = Nodo(id)
		return nodos

	def crearConexion(self,conexion):
		conexion = Vertice(conexion)
		return conexion
	
#Metodo para generar grafo de Malla
	def grafoMalla(self,col,filas):
		liga = []
		g = Grafo(False)
		x = 1
		g.crearNode(x)
		for i in range(1,filas+1):
			for j in range(1,col+1):
				if i == filas and j == col:
					continue
				elif i == filas:
					liga.append(g.crearConexion((x,x+1)))
				elif j != col:  
					liga.append(g.crearConexion((x,x+1)))
					liga.append(g.crearConexion((x,x+col)))
				else:
					liga.append(g.crearConexion((x,x+col)))
				x += 1
		return liga

#Metodo para salvar el grafo
	def saveGraph(self,graph):
		with open('grafo.gv','w',encoding = 'utf-8') as f:
   			f.write("graph x {\n")
   			for i in graph:
   				f.write(str(i.idConexion[0]) + " -- " + str(i.idConexion[1]) + "\n")
   			f.write("}")
		f.close()

#Metodo para generar grafo de erdos
	def erdosRenyi(self,nodos,vertices):
		random.seed(45)
		semilla = 46
		verticesList = []
		contenoVertice = 0
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			for j in range(1,nodos +1):
				tiro = random.random()
				if tiro > .5 and ((j,i) not in verticesList) and i != j and contenoVertice < vertices:
					verticesList.append(Grafo(False).crearConexion((i,j)))
					contenoVertice += 1
					for n in range(0,len(verticesList)):
						if verticesList[n].idConexion[1] == i and verticesList[n].idConexion[0] == j:
							verticesList.pop(n)
							contenoVertice -= 1
							break
				else:
					continue
		return verticesList

#Metodo para generar grafo de gilbert
	def gilbert(self,nodos,probabilidad):
		random.seed(45)
		semilla = 46
		verticesList = []
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			for j in range(1,nodos +1):
				tiro = random.random()
				if tiro > probabilidad and ((j,i) not in verticesList) and i != j:
					#print("tiro:",tiro)
					#print("j:",j)
					#print("i",i)
					#print(len(verticesList))
					verticesList.append(Grafo(False).crearConexion((i,j)))
					for n in range(0,len(verticesList)):
						#print("entre")
						if verticesList[n].idConexion[1] == i and verticesList[n].idConexion[0] == j:
							#print(verticesList[n].idConexion[1],verticesList[n].idConexion[0])
							#print(i,j)
							verticesList.pop(n)
							#print("posicion 1",verticesList[n].idConexion[1])
							break	
						#else:
							#verticesList.append(Grafo(False).crearConexion((i,j)))
							#print(type(verticesList[0]))
				#else:
					#print("else")
					#continue
		#print("final")
		return verticesList

#Metodo para generar grafo geogrfico
	def geografica(self,nodos,distancia):
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		random.seed(45)
		semilla = 1
		posiciones = []
		verticesList = []
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			x = random.random()
			y = random.random()
			posiciones.append((x,y))
		for i in range(0,nodos):
			for j in range(0,nodos):
				xx = (posiciones[j][0]-posiciones[i][0])**2
				yy = (posiciones[j][1]-posiciones[i][1])**2
				d = sqrt(xx+yy) 
				if d > distancia and ((j+1,i+1) not in verticesList) and i+1 != j+1:
					verticesList.append(Grafo(False).crearConexion((i+1,j+1)))
				else:
					continue
		return verticesList

#Metodo para generar grafo barasi
	def barasi(self,nodos,vertices):
		random.seed(3)
		semilla = 1
		nodo = [Grafo(False).crearNode(i) for i in range(1,3)]
		verticesList = []
		verticesList.append(Grafo(False).crearConexion((1,2)))
		cantidadVertices = []
		cantidadVertices.append(1)
		cantidadVertices.append(1)
		for i in range(3,nodos+1):
			nodo.append(Grafo(False).crearNode(i+2))
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			cuentaVerticeCurrent = 0
			for j in range(1,len(cantidadVertices)+1):
				p = 1 -(cantidadVertices[j-1]/vertices)
				tiro = random.random()
				if tiro < p and cantidadVertices[j-1] <= vertices:
					cuentaVerticeCurrent +=1
					cantidadVertices[j-1] +=1
					verticesList.append(Grafo(False).crearConexion((i,j)))
			cantidadVertices.append(cuentaVerticeCurrent)
		return verticesList

#Metodo para generar grfo de dorogov
	def dorogov(self,nodos):
		random.seed(30)
		semilla = 30
		nodo = [Grafo(False).crearNode(i) for i in range(1,3)]
		verticesList = []
		verticesList.append(Grafo(False).crearConexion((1,2)))
		verticesList.append(Grafo(False).crearConexion((1,3)))
		verticesList.append(Grafo(False).crearConexion((2,3)))
		for i in range(4,nodos+1):
			nodo.append(Grafo(False).crearNode(i+2))
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			cuentaVerticeCurrent = 0
			tiro = random.randrange(1,i)
			tiro2 = random.randrange(0,len(verticesList))
			verticesList.append(Grafo(False).crearConexion((i,verticesList[tiro2].idConexion[0])))
			verticesList.append(Grafo(False).crearConexion((i,verticesList[tiro2].idConexion[1])))
		return verticesList


ga1 = Grafo(False).dorogov(500)
Grafo(False).saveGraph(ga1)
