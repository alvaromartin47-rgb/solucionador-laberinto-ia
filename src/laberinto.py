from entidades.mapa import generar_vecinas, Mapa
import random

def generar_laberinto(filas, columnas):
    """Generar un laberinto.

    Argumentos:
        filas, columnas (int): Tamaño del mapa

    Devuelve:
        Mapa: un mapa nuevo con celdas bloqueadas formando un laberinto
              aleatorio
    """
    
    tablero = Mapa(filas, columnas)
    mapa = Mapa(filas, columnas)
    
    bloquear_todo(tablero)
    
    vecinas = generar_vecinas(tablero.mapa)
    tablero.desbloquear(tablero.inicio)
    tablero = crear_caminos(tablero, vecinas)
    
    intercambiar(tablero, mapa)
    
    return mapa

def desbloquear_medio(anterior, actual, mapa):
    """Recibe dos tuplas y una lista de tuplas.
    _anterior_ y _actual_ son dos celdas de _mapa_, esta función desbloquea la celda que se encuentra
    entre medio de _anterior_ y _actual_ es decir, muta a _mapa_.
    """
    f, c = anterior
    f1, c1 = actual
    medio = mapa.trasladar_coord(anterior, (f1 - f)/2, (c1 - c)/2)
    mapa.desbloquear(medio)

def crear_caminos(mapa, vecinas):
    """Recibe _mapa_ (Mapa()), un diccionario con las celdas de _mapa_ como claves, y como valores
    sus celdas 'vecinas' que son las impares que se encuentran dentro de _mapa_ y estan a distancia 2.
    Y dos tuplas que representan celdas (Coord()).
    Esta función da forma al mapa generando caminos que conformaran un laberinto, de forma recursiva. Elige
    una vecina de _actual_ de forma aletoria, la desbloquea y desbloquea la celda que se encuentra entre éstas.  
    Entre estos caminos habra al menos uno que va desde el origen hasta el final. Devuelve _mapa_ mutado.
    """
    camino = []
    visitadas = set()
    
    camino.append((mapa.inicio, None))
    visitadas.add(mapa.inicio)
    cantidad_uniones = 0
    
    while len(camino) > 0:
        actual, anterior = camino.pop(random.randrange(len(camino)))
        vecinos = vecinas[actual]
        final_de_camino = True
        
        for vecina in vecinos:
            if vecina not in visitadas:
                camino.append((vecina, actual))
                camino.append((actual, anterior))
                
                desbloquear_medio(actual, vecina, mapa)
                mapa.desbloquear(vecina)
                
                visitadas.add(vecina)
                final_de_camino = False
                break
        
        if final_de_camino and anterior in vecinos and es_primo(cantidad_uniones):
            vecinas_aux = vecinas[actual]            
            vecinas_aux.remove(anterior)
            vecina_aux = vecinas_aux[random.randrange(len(vecinas_aux))]
            
            if vecina_aux != mapa.final:
                desbloquear_medio(actual, vecina_aux, mapa)
        
        cantidad_uniones += 1
    
    return mapa

def intercambiar(mapa, mapa2):
    """Recibe dos mapas (Mapa()), e intercambia sus celdas bloqueadas.
    Muta ambas instancias de la clase Mapa().
    """
    for e in mapa.bloqueadas:
        mapa2.bloqueadas.append(e)

def bloquear_todo(mapa):
    """Recibe (Mapa()) y bloquea todas sus celdas."""
    
    for e in mapa.mapa:
        mapa.alternar_bloque(e)

def es_primo(n):
    """Recibe un entero _n_ y devuelve True si es primo y False si no lo es."""
    
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
