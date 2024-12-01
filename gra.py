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
	def __init__(self,idConexion,peso=0):
		self.idConexion = idConexion
		self.peso = peso

	def mostrarDatos(self):
		print("Conexion: ", self.idConexion)
		print("Peso: ", self.peso)

#Clase de grafo
class Grafo(Nodo,Vertice):
	def __init__(self,dirigido):
		self.dirigido = dirigido

	def crearNode(self,id):
		nodos = Nodo(id)
		return nodos

	def crearConexion(self,conexion,peso):
		conexion = Vertice(conexion,peso)
		return conexion


#Metodo para calcular cantidad de nodos
	def calcularNodos(self,verticesList):
		nodos = set()
		for i in verticesList:
			nodos.add(i.idConexion[1])
			nodos.add(i.idConexion[0])
		return len(nodos)
	
#Metodo para generar grafo de Malla
	def grafoMalla(self,col,filas):
		liga = []
		g = Grafo(False)
		x = 1
		g.crearNode(x)
		for i in range(1,filas+1):
			for j in range(1,col+1):
				#peso = random.randrange(1,100)
				#peso2 = random.randrange(1,100)
				peso = round(random.uniform(1, 100), 2)
				peso2 = round(random.uniform(1, 100), 2)
				if i == filas and j == col:
					continue
				elif i == filas:
					liga.append(g.crearConexion((x,x+1),peso))
				elif j != col:  
					liga.append(g.crearConexion((x,x+1),peso))
					liga.append(g.crearConexion((x,x+col),peso2))
				else:
					liga.append(g.crearConexion((x,x+col),peso))
				x += 1
		return liga
	


#Metodo para salvar el grafo
	def saveGraph(self,graph,version):
		with open('grafo'+ str(version) +'.gv','w',encoding = 'utf-8') as f:
   			f.write("graph x {\n")
   			for i in graph:
   				f.write(str(i.idConexion[0]) + " -- " + str(i.idConexion[1]) + "[label=" + str(i.peso) + "];" +  "\n")
   			f.write("}")
		f.close()


#Metodo para salvar el grafo con pesos en las aristas
	def saveGraph2(self,graph,pesos):
		with open('grafo2.gv','w',encoding = 'utf-8') as f:
   			f.write("graph x {\n")
   			for i in graph:
   				f.write(str(i.idConexion[0]) + "(" +str(pesos[i.idConexion[0]-1]) + ") -- " + str(i.idConexion[1]) +  "(" + str(pesos[i.idConexion[1]-1]) + ")" + "[label=" + str(i.peso) + "];" + "\n")
   			f.write("}")
		f.close()


#Metodo para generar grafo de erdos
	def erdosRenyi(self,nodos,vertices):
		random.seed(45)
		semilla = 46
		verticesList = []
		numeros = set()
		contenoVertice = 0
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		peso = round(random.uniform(1, 200), 3)
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			for j in range(1,nodos +1):
				tiro = random.random()
				a = False
				while a != True:
					peso = round(random.uniform(1, 1000), 3)
					if peso not in numeros:
						numeros.add(peso)
						a = True
				if tiro > .5 and ((j,i) not in verticesList) and i != j and contenoVertice < vertices:
					verticesList.append(Grafo(False).crearConexion((i,j),peso))
					contenoVertice += 1
					for n in range(0,len(verticesList)):
						if verticesList[n].idConexion[1] == i and verticesList[n].idConexion[0] == j:
							verticesList.pop(n)
							contenoVertice -= 1
							break
				else:
					continue
		#print(numeros)
		return verticesList

#Metodo para generar grafo de gilbert
	def gilbert(self,nodos,probabilidad):
		random.seed(45)
		semilla = 46
		verticesList = []
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		numeros = set()
		a = False
		while a != True:
			peso = round(random.uniform(1, 1000), 3)
			if peso not in numeros:
				numeros.add(peso)
				a = True
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			for j in range(1,nodos +1):
				tiro = random.random()
				peso = round(random.uniform(1, 100), 2)
				if tiro > probabilidad and ((j,i) not in verticesList) and i != j:
					verticesList.append(Grafo(False).crearConexion((i,j),peso))
					for n in range(0,len(verticesList)):
						if verticesList[n].idConexion[1] == i and verticesList[n].idConexion[0] == j:
							verticesList.pop(n)
							break	
		return verticesList

#Metodo para generar grafo geogrfico
	def geografica(self,nodos,distancia):
		grafo = [Grafo(False).crearNode(i) for i in range(1,nodos)]
		random.seed(45)
		semilla = 1
		posiciones = []
		verticesList = []
		numeros = set()
		for i in range(1,nodos+1):
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			x = random.random()
			y = random.random()
			posiciones.append((x,y))
		for i in range(0,nodos):
			for j in range(0,nodos):
				a = False
				while a != True:
					peso = round(random.uniform(1, 1000), 3)
					if peso not in numeros:
						numeros.add(peso)
						a = True
				#peso = round(random.uniform(1, 100), 2)
				xx = (posiciones[j][0]-posiciones[i][0])**2
				yy = (posiciones[j][1]-posiciones[i][1])**2
				d = sqrt(xx+yy) 
				if d > distancia and ((j+1,i+1) not in verticesList) and i+1 != j+1:
					verticesList.append(Grafo(False).crearConexion((i+1,j+1),peso))
				else:
					continue
		return verticesList

#Metodo para generar grafo barasi
	def barasi(self,nodos,vertices):
		random.seed(3)
		semilla = 1
		nodo = [Grafo(False).crearNode(i) for i in range(1,3)]
		verticesList = []
		peso = round(random.uniform(1, 100), 2)
		verticesList.append(Grafo(False).crearConexion((1,2),peso))
		cantidadVertices = []
		cantidadVertices.append(1)
		cantidadVertices.append(1)
		numeros = set()
		numeros.add(peso)
		for i in range(3,nodos+1):
			nodo.append(Grafo(False).crearNode(i+2))
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			cuentaVerticeCurrent = 0
			for j in range(1,len(cantidadVertices)+1):
				#peso = round(random.uniform(1, 100), 2)
				a = False
				while a != True:
					peso = round(random.uniform(1, 1000), 3)
					if peso not in numeros:
						numeros.add(peso)
						a = True
				p = 1 -(cantidadVertices[j-1]/vertices)
				tiro = random.random()
				if tiro < p and cantidadVertices[j-1] <= vertices:
					cuentaVerticeCurrent +=1
					cantidadVertices[j-1] +=1
					verticesList.append(Grafo(False).crearConexion((i,j),peso))
			cantidadVertices.append(cuentaVerticeCurrent)
		return verticesList

#Metodo para generar grfo de dorogov
	def dorogov(self,nodos):
		random.seed(30)
		semilla = 30
		nodo = [Grafo(False).crearNode(i) for i in range(1,3)]
		verticesList = []
		peso3 = round(random.uniform(1, 1000), 2)
		peso4 = round(random.uniform(1, 1000), 2)
		peso5 = round(random.uniform(1, 1000), 2)
		numeros = set()
		numeros.add(peso3)
		numeros.add(peso4)
		numeros.add(peso5)
		verticesList.append(Grafo(False).crearConexion((1,2),peso3))
		verticesList.append(Grafo(False).crearConexion((1,3),peso4))
		verticesList.append(Grafo(False).crearConexion((2,3),peso5))
		for i in range(4,nodos+1):
			a = False
			while a != True:
				peso = round(random.uniform(1, 1000), 3)
				peso2 = round(random.uniform(1, 1000), 3)
				if peso not in numeros and peso2 not in numeros:
					numeros.add(peso)
					a = True
			#peso = round(random.uniform(1, 100), 2)
			#peso2 = round(random.uniform(1, 100), 2)
			nodo.append(Grafo(False).crearNode(i+2))
			if i%2 ==0:
				semilla = 3 + semilla
				random.seed(semilla)
			cuentaVerticeCurrent = 0
			tiro = random.randrange(1,i)
			tiro2 = random.randrange(0,len(verticesList))
			verticesList.append(Grafo(False).crearConexion((i,verticesList[tiro2].idConexion[0]),peso))
			verticesList.append(Grafo(False).crearConexion((i,verticesList[tiro2].idConexion[1]),peso2))
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

#Metodo para calcular el dijkstra
	def dijkstra(self,s,verticesList):
		nodos = Grafo(False).calcularNodos(verticesList)
		prioridades = [0] * nodos
		plox = set()
		for i in range(0,nodos):
			prioridades[i] = 9999
		prioridades[s-1]=0
		visitados = []
		revisaditos = []
		visitados.append(s)
		while len(plox) != nodos:
			a = 9999
			indexito = 0
			for i in range(0,nodos):
				if i not in revisaditos:
					if a > prioridades[i]:
						a = prioridades[i]
						indexito = i
			actual = indexito
			if prioridades[actual]== 9999:
				break
			for i in verticesList:
				if i.idConexion[0] == actual+1:
					visitados.append(i.idConexion[1])
					prioridad = prioridades[actual] + i.peso
					if prioridad < prioridades[i.idConexion[1]-1]:
						prioridades[i.idConexion[1]-1] = prioridad
				elif i.idConexion[1] == actual+1:
					visitados.append(i.idConexion[0])
					prioridad = prioridades[actual] + i.peso
					if prioridad < prioridades[i.idConexion[0]-1]:
						prioridades[i.idConexion[0]-1] = prioridad
			plox.add(actual)
			revisaditos.append(actual)
			try: 
				visitados.pop(actual)
			except:
				None
		return prioridades
	
	
	def partition(self,array, low, high):
		pivot = array[high].peso
		i = low - 1
		for j in range(low, high):
			if array[j].peso <= pivot:
				i = i + 1
				(array[i], array[j]) = (array[j], array[i])
		(array[i + 1], array[high]) = (array[high], array[i + 1])
		return i + 1
	
	def ordenar(self,array, low, high):        ## metodo para ordenar quick sorting
		if low < high:
			pi = Grafo(False).partition(array, low, high)
			Grafo(False).ordenar(array, low, pi - 1)
			Grafo(False).ordenar(array, pi + 1, high)

		
	def Kruskal(self,verticesList):
		h = len(verticesList)-1
		Grafo(False).ordenar(verticesList,0,h)
		t= []
		nodos = Grafo(False).calcularNodos(verticesList)
		conjuntos = [0] * nodos
		for i in range(nodos):
			#print(i)
			conjuntos[i] = i
		#print(conjuntos)
		for i in verticesList:
			#i.mostrarDatos()
			#print(conjuntos[i.idConexion[0]-1])
			#print(conjuntos[i.idConexion[1]-1])
			#print(conjuntos.index(conjuntos[i.idConexion[0]-1]))
			#print(conjuntos.index(conjuntos[i.idConexion[1]-1]))
			#print(conjuntos)
			if conjuntos[i.idConexion[0]-1] != conjuntos[i.idConexion[1]-1]:
				#print("entre principal")
				t.append(i)
				r = conjuntos[i.idConexion[0]-1]
				for j in range(0,len(conjuntos)):
					if conjuntos[j] == r:
						conjuntos[j] = conjuntos[i.idConexion[1]-1]
						#print(j)
			#print(conjuntos)
		#print(len(t))
		a= 0
		for i in t:
			#i.mostrarDatos()
			a = a + i.peso
		print("Peso Kruskal",round(a,2))
		return t

	def kruskalInverso(self,verticesList):
		h = len(verticesList)-1
		Grafo(False).ordenar(verticesList,0,h)
		rverticesList = reversed(verticesList)
		#for n in rverticesList:
		#	n.mostrarDatos()
		#print("-----------------------------------")
		#a = Grafo(False).BFS(2,verticesList)
		#print(a)
		#for j in verticesList:
		#	j.mostrarDatos()
		
		for i in rverticesList:
			#i.mostrarDatos()
			#print(i.idConexion[0])
			#a = Grafo(False).BFS(i.idConexion[0],verticesList)
			try:
				nodos = Grafo(False).calcularNodos(verticesList)
				verticesList.pop(verticesList.index(i))
				a = Grafo(False).BFS(1,verticesList)
				nodos1 = Grafo(False).calcularNodos(a)
				#print(nodos,nodos1,len(a)+1)
				if nodos != len(a) +1:
					verticesList.append(i)
					#i.mostrarDatos()
				#print()
			except:
				#print("entres")
				verticesList.append(i)
				#i.mostrarDatos()
				continue
		a= 0
		for i in verticesList:
			#i.mostrarDatos()
			a = a + i.peso
		print("Peso Kruskal Inverso",round(a,2))
		return verticesList

	def prim(self,verticesList):
		nodos = Grafo(False).calcularNodos(verticesList)
		s = random.randrange(1,nodos)
		revisados = set()
		revisados.add(s)
		aristas = [0] * nodos
		aristasSolas = []
		final = []
		#adyacentes = []
		#for p in verticesList:
			#p.mostrarDatos()
		#print("------------------------------------------------")
		#print("fuente",s)
		while len(revisados) != nodos:
			#print(revisados)
			adyacentes = []
			#print("fuente:",s)
			for i in verticesList:
				#if i.idConexion[0] == s or i.idConexion[1] == s and (i not in aristasSolas):
				if ((i.idConexion[0] not in revisados) or (i.idConexion[1] not in revisados))and(i.idConexion[0] == s or i.idConexion[1]==s):
					#i.mostrarDatos()
					adyacentes.append(i)
					aristasSolas.append(i)
			h = len(aristasSolas)-1
			Grafo(False).ordenar(aristasSolas,0,h)
			
			#print("  ")
			#for j in aristasSolas:
			#	j.mostrarDatos()
			#print("  ")
			final.append(aristasSolas[0])
			#aristasSolas[0].mostrarDatos()
			
			if (aristasSolas[0].idConexion[0] != s) and (aristasSolas[0].idConexion[0] not in revisados):
				s =  aristasSolas[0].idConexion[0]
			else:
				s = aristasSolas[0].idConexion[1]
			#print("fuente:",s)
			revisados.add(aristasSolas[0].idConexion[0])
			revisados.add(aristasSolas[0].idConexion[1])
			aristasSolas.pop(0)
			#print(len(aristasSolas))
			aristasSolas2 = aristasSolas[:]
			for l in aristasSolas:
				#l.mostrarDatos()
				if l.idConexion[0] == s and l.idConexion[1] in revisados:
					aristasSolas2.remove(l)
				elif l.idConexion[1] == s and l.idConexion[0] in revisados:
					aristasSolas2.remove(l)
			aristasSolas = aristasSolas2[:]
			#for n in aristasSolas:
				#n.mostrarDatos()
				#if ((n.idConexion[0] == s) and (n.idConexion[1] in revisados)) or ((n.idConexion[1] == s) and (n.idConexion[0] in revisados)):
					#print("salio")
					#n.mostrarDatos()
					#aristasSolas.remove(n)
				#elif (n.idConexion[1] == s and n.idConexion[0] in revisados):
				#	print("salio 1")
				#	n.mostrarDatos()
				#	aristasSolas.remove(n)
			#print("Revisados:", revisados)
		a= 0
		for i in final:
			#i.mostrarDatos()
			a = a + i.peso
		print("Peso Prim",round(a,2))
		return final
			





"""	def Kruskal(self,verticesList):
		h = len(verticesList)-1
		Grafo(False).ordenar(verticesList,0,h)
		t= []
		nodos = Grafo(False).calcularNodos(verticesList)
		conjuntos = [0] * nodos
		for i in range(nodos):
			#print(i)
			conjuntos[i] = i
		#print(conjuntos)
		for i in verticesList:
			i.mostrarDatos()
			print(conjuntos[i.idConexion[0]-1])
			print(conjuntos[i.idConexion[1]-1])
			print(conjuntos.index(conjuntos[i.idConexion[0]-1]))
			print(conjuntos.index(conjuntos[i.idConexion[1]-1]))
			print(conjuntos)
			if conjuntos[i.idConexion[0]-1] != conjuntos[i.idConexion[1]-1]:
				print("entre principal")
				t.append(i)
				if conjuntos[i.idConexion[0]-1] == conjuntos.index(conjuntos[i.idConexion[0]-1]):
					print("entre 1")
					conjuntos[i.idConexion[0]-1] = conjuntos[i.idConexion[1] -1]
					conjuntos[i.idConexion[1]-1] = conjuntos[i.idConexion[1] -1]
				elif conjuntos[i.idConexion[1]-1] == conjuntos.index(conjuntos[i.idConexion[1]-1]):
					print("entre 2")
					conjuntos[i.idConexion[0]-1] = conjuntos[i.idConexion[0] -1]
					conjuntos[i.idConexion[1]-1] = conjuntos[i.idConexion[0] -1]
			print(conjuntos)
		print(len(t))
		for i in t:
			i.mostrarDatos()
		return t"""