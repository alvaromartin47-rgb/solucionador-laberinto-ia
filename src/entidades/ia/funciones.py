from entidades.cola import Cola
from entidades.grafo import Grafo

def calcular_camino(padres, destino):
    solucion_set = set()

    while True:
        solucion_set.add(destino)
        if not padres[destino]: break
        destino = padres[destino]
    
    return None, solucion_set

def cargar_grafo(mapa):
    '''
    Recibe un mapa de 'n' filas y 'm' columnas. Genera un grafo y asigna como nodo a cada
    una de las celdas desbloqueadas del mapa (camino del laberinto).
    '''
    desbloqueadas = []
    grafo = Grafo()
    for celda in mapa.mapa:
        if not mapa.celda_bloqueada(celda):
            desbloqueadas.append(celda)
            grafo.agregar_vertice(celda)
    
    for celda in desbloqueadas:
        for vecina in desbloqueadas:
            if vecina.distancia(celda) == 1:
                grafo.agregar_arista_dirigido(celda, vecina)

    return grafo

def camino_minimo(grafo, mapa, destino):
    q = Cola()
    visitados = set()
    dist = dict()
    padres = dict()

    q.encolar(mapa.inicio)
    dist[mapa.inicio] = 0
    padres[mapa.inicio] = None
    visitados.add(mapa.inicio)

    while not q.esta_vacia():
        v = q.desencolar()
        
        if v == destino: return calcular_camino(padres, mapa.final)

        for w in grafo.obtener_adyacentes(v):
            if w not in visitados:
                visitados.add(w)
                dist[w] = dist[v] + 1
                padres[w] = v
                q.encolar(w)