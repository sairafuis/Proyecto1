import gra

#ga1 = gra.Grafo(False).dorogov(500)
#gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(3,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
#ga2 = gra.Grafo(False).DFSIterative(3,ga1)
#gra.Grafo(False).saveGraph(ga2)

#ga1 = gra.Grafo(False).dorogov(100)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).dorogov(500)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).grafoMalla(25,25)
#gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(3,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
#ga2 = gra.Grafo(False).DFSIterative(3,ga1)
#gra.Grafo(False).saveGraph(ga2)

#ga1 = gra.Grafo(False).grafoMalla(10,10)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).grafoMalla(25,25)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).barasi(500,5)
#gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(3,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
#ga2 = gra.Grafo(False).DFSIterative(3,ga1)
#gra.Grafo(False).saveGraph(ga2)

#ga1 = gra.Grafo(False).barasi(100,5)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).barasi(500,5)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).geografica(500,.5)
#gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(10,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
#ga2 = gra.Grafo(False).DFSIterative(3,ga1)
#gra.Grafo(False).saveGraph(ga2)


#ga1 = gra.Grafo(False).geografica(100,.7)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).geografica(500,.7)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).gilbert(500,.5)
#gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(10,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
#ga2 = gra.Grafo(False).DFSIterative(3,ga1)
#gra.Grafo(False).saveGraph(ga2)

#ga1 = gra.Grafo(False).gilbert(100,.5)
#gra.Grafo(False).saveGraph(ga1)

#ga1 = gra.Grafo(False).gilbert(500,.5)
#gra.Grafo(False).saveGraph(ga1)

ga1 = gra.Grafo(False).erdosRenyi(500,3000)
gra.Grafo(False).saveGraph(ga1)
#ga2 = gra.Grafo(False).BFS(10,ga1)
#gra.Grafo(False).saveGraph(ga2)
#revisado = set()
#a = []
#ga2 = gra.Grafo(False).DFSRecursive(3,ga1,revisado,a)
#gra.Grafo(False).saveGraph(ga2)
ga2 = gra.Grafo(False).DFSIterative(3,ga1)
gra.Grafo(False).saveGraph(ga2)