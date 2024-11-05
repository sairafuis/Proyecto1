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
	
#Metodo para calcular cantidad de nodos
	def calcularNodos(self,verticesList):
		nodos = set()
		for i in verticesList:
			nodos.add(i.idConexion[1])
			nodos.add(i.idConexion[0])
		return len(nodos)

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
	
#Metodo para calcula el BFS
	def BFS(self,fuente,verticesList):
		Descubierto = []
		Layers = []
		verticesNew =[]
		fuentes = []
		revisados = []
		fuentes.append(fuente)
		revisados.append(fuente)
		nodosExtension = Grafo(False).calcularNodos(verticesList)
		for i in range(0,nodosExtension):
			Descubierto.append(False)
		contadorLayer = 0
		Layers.append(fuentes)
		while len(Layers[contadorLayer]) >> 0:
			currentV = [] 
			for nodo in Layers[contadorLayer]:
				if Descubierto[nodo-1] == False:
					Descubierto[nodo-1] = True
					for l in verticesList:
						if nodo == l.idConexion[0] and (Descubierto[l.idConexion[1]-1]==False) and (l.idConexion[1]) not in revisados:
							currentV.append(l.idConexion[1])
							revisados.append(l.idConexion[1])
							verticesNew.append(l)
						elif nodo == l.idConexion[1] and Descubierto[l.idConexion[0]-1]==False and (l.idConexion[0]) not in revisados:
							currentV.append(l.idConexion[0])
							revisados.append(l.idConexion[0])
							verticesNew.append(l)
			contadorLayer += 1
			Layers.append(currentV)
		return verticesNew

#Metodo para calcular el DFS recursivo
	def DFSRecursive(self,fuente,verticesList,revisado,a):
		revisado.add(fuente)
		adyacentes = []
		currentContado = 0
		for i in verticesList:
			if i.idConexion[0] == fuente or i.idConexion[1] == fuente:
				adyacentes.append(i)
		for j in adyacentes:
			if (j.idConexion[0] not in revisado or j.idConexion[1] not in revisado) and currentContado != len(adyacentes):
				a.append(j)
				verticesList.remove(j)
				if j.idConexion[0] not in revisado:
					b = Grafo(False).DFSRecursive(j.idConexion[0],verticesList,revisado,a)
				elif j.idConexion[1] not in revisado:
					b = Grafo(False).DFSRecursive(j.idConexion[1],verticesList,revisado,a)
				currentContado += 1
		return a
			
#Metodo para calcular el DFS iterativo
	def DFSIterative(self,fuente,verticesList):
		revisado = []
		pila = []
		vertices = []
		vNew = verticesList.copy()
		extension = Grafo(False).calcularNodos(verticesList)
		pila.append(fuente)
		ultimo = None
		while len(pila):
			fuenteb = 0
			vertices.append(ultimo)
			ultimo = None
			fuente = pila.pop()
			if fuente not in revisado:
				revisado.append(fuente)
				for i in verticesList:
					if i.idConexion[0] == fuente and i.idConexion[1] not in revisado:
						pila.append(i.idConexion[1])
						ultimo= i
						fuenteb = 1
					elif i.idConexion[1] == fuente and i.idConexion[0] not in revisado:
						pila.append(i.idConexion[0])
						ultimo= i
						fuenteb = 1 
		new = []
		for i in range(len(revisado)-1,-1,-1):
			flag = 0
			for j in range(i-1,-1,-1):
				for n in verticesList:
					if n.idConexion[0] == revisado[i] and n.idConexion[1] == revisado[j]:
						new.append(n)
						flag = 1
						break
					elif n.idConexion[1] == revisado[i] and n.idConexion[0] == revisado[j]:
						new.append(n)
						flag = 1
						break
				if flag == 1:
					break
		return new
			
		