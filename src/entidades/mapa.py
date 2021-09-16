import random

class Coord:
    """
    Representa las coordenadas de una celda en una grilla 2D, representada
    como filas y columnas. Las coordendas ``fila = 0, columna = 0`` corresponden
    a la celda de arriba a la izquierda.

    Las instancias de Coord son inmutables.
    """

    def __init__(self, fila=0, columna=0):
        """Constructor.

        Argumentos:
            fila, columna (int): Coordenadas de la celda
        """
        self.celda = (fila, columna)

    def trasladar(self, df, dc):
        """Trasladar una celda.

        Devuelve una nueva instancia de Coord, correspondiente a las coordenadas
        de la celda que se encuentra ``df`` filas y ``dc`` columnas de distancia.

        Argumentos:
            df (int): Cantidad de filas a trasladar
            dc (int): Cantidad de columnas a trasladar

        Devuelve:
            Coord: Las coordenadas de la celda trasladada
        """
        return Coord(int(self.celda[0] + df), int(self.celda[1] + dc))

    def distancia(self, otra):
        """Distancia entre dos celdas.

        Argumentos:
            otra (Coord)

        Devuelve:
            int|float: La distancia entre las dos celdas (no negativo)
        """
        x = self.celda[0] - otra.celda[0]
        y = self.celda[1] - otra.celda[1]
        
        return (x**2 + y**2) ** 0.5

    def __eq__(self, otra):
        """Determina si dos coordenadas son iguales"""
        return otra == self.celda

    def __iter__(self):
        """Iterar las componentes de la coordenada.

        Devuelve un iterador de forma tal que:
        >>> coord = Coord(3, 5)
        >>> f, c = coord
        >>> assert f == 3
        >>> assert c == 5
        """
        self.actual = 0
        return self.celda.__iter__()
   
    def __next__(self):
       
        if len(self.celda) >= self.actual:
            raise StopIteration

        self.actual += 1   
        return self.celda[self.actual-1]

    def __hash__(self):
        """Código "hash" de la instancia inmutable."""
        # Este método es llamado por la función de Python hash(objeto), y debe devolver
        # un número entero.
        # Más información (y un ejemplo de cómo implementar la funcion) en:
        # https://docs.python.org/3/reference/datamodel.html#object.__hash__
        
        return hash((self.celda))
    
    def __repr__(self):
        """Representación de la coordenada como cadena de texto"""
       
        return f'({self.celda[0]}, {self.celda[1]})'

    def __lt__(self, otro):
        '''
        '''
        return self.celda < otro.celda

class Mapa:
    """
    Representa el mapa de un laberinto en una grilla 2D con:

    * un tamaño determinado (filas y columnas)
    * una celda origen
    * una celda destino
    * 0 o más celdas "bloqueadas", que representan las paredes del laberinto

    Las instancias de Mapa son mutables.
    """
    def __init__(self, filas, columnas):
        """Constructor.

        El mapa creado tiene todas las celdas desbloqueadas, el origen en la celda
        de arriba a la izquierda y el destino en el extremo opuesto.

        Argumentos:
            filas, columnas (int): Tamaño del mapa
        """
        self.filas = filas
        self.columnas = columnas
        self.mapa, self.inicio, self.final = generar_mapa(filas, columnas)
        self.bloqueadas = []
    
    def dimension(self):
        """Dimensiones del mapa (filas y columnas).

        Devuelve:
            (int, int): Cantidad de filas y columnas
        """
        return (self.filas, self.columnas)

    def origen(self):
        """Celda origen.

        Devuelve:
            Coord: Las coordenadas de la celda origen
        """
        return self.inicio

    def destino(self):
        """Celda destino.

        Devuelve:
            Coord: Las coordenadas de la celda destino
        """
        return self.final

    def asignar_origen(self, coord):
        """Asignar la celda origen.

        Argumentos:
            coord (Coord): Coordenadas de la celda origen
        """
        self.inicio = coord.celda

    def asignar_destino(self, coord):
        """Asignar la celda destino.

        Argumentos:
            coord (Coord): Coordenadas de la celda destino
        """
        self.final = coord.celda
        
    def celda_bloqueada(self, coord):
        """¿La celda está bloqueada?

        Argumentos:
            coord (Coord): Coordenadas de la celda

        Devuelve:
            bool: True si la celda está bloqueada
        """
        return coord in self.bloqueadas

    def bloquear(self, coord):
        """Bloquear una celda.

        Si la celda estaba previamente bloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a bloquear
        """
        if not coord.celda in self.bloqueadas:
            self.bloqueadas.append(coord.celda)
        
        return 

    def desbloquear(self, coord):
        """Desbloquear una celda.

        Si la celda estaba previamente desbloqueada, no hace nada.

        Argumentos:
            coord (Coord): Coordenadas de la celda a desbloquear
        """
        if coord.celda in self.bloqueadas:
            self.bloqueadas.remove(coord.celda)
        
        return
        
    def alternar_bloque(self, coord):
        """Alternar entre celda bloqueada y desbloqueada.

        Si la celda estaba previamente desbloqueada, la bloquea, y viceversa.

        Argumentos:
            coord (Coord): Coordenadas de la celda a alternar
        """
        if coord.celda not in self.bloqueadas: 
            self.bloqueadas.append(coord.celda)
        
        else: self.bloqueadas.remove(coord.celda)

    def es_coord_valida(self, coord):
        """¿Las coordenadas están dentro del mapa?

        Argumentos:
            coord (Coord): Coordenadas de una celda

        Devuelve:
            bool: True si las coordenadas corresponden a una celda dentro del mapa
        """
        return coord.celda[0] <= self.filas and coord.celda[1] <= self.columnas
        

    def trasladar_coord(self, coord, df, dc):
        """Trasladar una coordenada, si es posible.

        Argumentos:
            coord: La coordenada de una celda en el mapa
            df, dc: La traslación a realizar

        Devuelve:
            Coord: La coordenada trasladada si queda dentro del mapa. En caso
                   contrario, devuelve la coordenada recibida.
        """
        trasladada = coord.trasladar(df, dc)
        if coord.celda[0] <= self.filas and coord.celda[1] <= self.columnas:
            return trasladada
        
        return coord

    def __iter__(self):
        """Iterar por las coordenadas de todas las celdas del mapa.

        Se debe garantizar que la iteración cubre todas las celdas del mapa, en
        cualquier orden.

        Ejemplo:
            >>> mapa = Mapa(10, 10)
            >>> for coord in mapa:
            >>>     print(coord, mapa.celda_bloqueada(coord))
        """
        self.actual = 0
        
        return self.mapa.__iter__()
    
    def __next__(self):
       
        if len(self.mapa) >= self.actual:
            raise StopIteration

        self.actual += 1   
        
        return self.mapa[self.actual-1]

# FUNCIONES AUXILIARES

def es_par(n):
    '''
    Recibe entero _n_ y devuelve True si _n_ es par, o False si es impar.
    '''
    return n % 2 == 0

def generar_vecinas(mapa):
    '''
    Recibe _mapa_ que representa un mapa de 'n' filas, y 'm' columnas, se trata de
    una lista de tuplas en la que cada tupla representa una celda de _mapa_.
    Devuelve un diccionario que tiene como claves cada celda impar de _mapa_ y como valor
    una lista con sus celdas 'vecinas', que son las que se encuentran a distancia 2 de la 
    misma.
    '''
    vecinos = {}
    for i in range(len(mapa)):
        actual = mapa[i]
        f, c = actual
        
        if not es_par(f) and not es_par(c):
            vecinos[actual] = []
            ultimo = actual
        
            for coord in mapa: 
                if actual.distancia(coord) == 2:
                    vecinos[actual].append(coord)
    
    vecinos[ultimo] = []
    
    return vecinos

def generar_mapa(filas, columnas):
    '''
    Recibe dos enteros _filas_ y _columnas_ y de acuerdo a las combinaciones si son pares o impares
    ambos, devuelve una lista (mapa), que tendra Coordenadas, un inicio y un final.
    '''
    if es_par(filas):
        if es_par(columnas): return generar(filas-1, columnas-1)
        return generar(filas-1, columnas)
    
    if es_par(columnas): return generar(filas, columnas-1)
    
    return generar(filas, columnas)

def generar(filas, columnas):
    '''
    Recibe dos enteros _filas_ y _columnas_ y devuelve una lista de tuplas (Coord).
    La lista representa el mapa donde se desarrollará el laberinto, y las tuplas
    cada una de sus celdas.
    Devuelve el mapa generado, la celda inicio (arriba a la izquierda), y la celda
    final (abajo a la derecha).
    '''
    mapa = []
    inicio = Coord(1,1)
    
    for f in range(filas):
        for c in range(columnas):
            actual = Coord(f, c)
            f, c = actual
            
            mapa.append(actual)
            
            if not es_par(f) and not es_par(c): final = actual
    
    return mapa, inicio, final

def elegir_vecina(vecinas, actual):
    '''
    Recibe un diccionario con claves tuplas y valores listas de tuplas correspondientes
    a cada celda impar 'vecina' y sus respectivas 'vecinas' que se encuentran a distancia 2.
    Recibe una celda _actual_.
    Esta funcion devuelve una 'vecina' random de _actual_.
    '''
    vecina = vecinas[actual][random.randrange(len(vecinas[actual]))]   
    
    return vecina