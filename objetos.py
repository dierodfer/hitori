import copy

''' Objeto tablero, para el problema los estados. 
    Contiene una lista de listas llamadas celdas [[1,2,3],[2,3,1],[1,3,2]]
    en cada posicion de estas celdas contiene un valor
'''
class Tablero:
    def __init__(self, celdas):
        self.celdas = celdas
    
    def size_hor(self):
        return len(self.celdas[0])
    
    def size_ver(self):
        return len(self.celdas)
    
    def get_mayorDimension(self):
        ''' Devuelve mayor dimension del tablero '''
        return max([self.size_hor(), self.size_ver()])
    
    def get_Fila(self, fila):
        ''' Devuelve valores de la fila tablero
        @params fila '''
        return self.celdas[fila]
    
    def get_traspuesta(self):
        ''' Devuelve una copia del tablero invirtiendo filas por columnas '''
        return Tablero(list(zip(*self.celdas)))
    
    def get_orden(self):
        ''' Devuelve una lista con el orden de loa valores existentes en el tablero ordenados por el coste. '''
        res = [[0,1],[0,2],[0,3],[0,4],[0,5],[0,6],[0,7],[0,8],[0,9]]
        for f in range(0, self.size_hor()):
            for c in range(0, self.size_ver()):
                valor = self.get_celda(f, c)
                coste = self.get_coste_celda(f, c)
                res[valor-1] = [res[valor-1][0]+coste,valor]
        res.sort(key=lambda elemento: elemento[0])
        return res
    
    #Devuelve valor -1 si no esta dentro del rango del tablero y 0 si esta bloqueada
    def get_celda(self, f, c):
        if ((f<0) or (f+1>self.size_hor()) or (c<0) or (c+1>self.size_ver())):
            return -1
        else:
            return self.celdas[f][c]
        
    def set_celda(self, fila, columna, nuevoValor):
        ''' Mofifica el valor de una casilla proporcionada, devuelve una copia del tablero con la accion realizada. '''
        copia = copy.deepcopy(self.celdas)
        copia[fila][columna] = nuevoValor
        return Tablero(copia)
    
    def getCountRepetidasConCosteByValor(self, valor):
        res = 0
        for i in range(0,self.size_hor()):
            for j in range(0,self.size_ver()):
                if ((self.get_celda(i, j) == valor) & (self.get_coste_celda(i, j) < 0)):
                    res+=1
        return res;
            
    def get_coste_celda(self, fila, columna):
        ''' Devuelve el coste de una casilla en concreto.
            El coste para este caso tomamos de referencias el numero de repeticiones que tienen las casillas segun su valor,
            mientras mas valores repetidos mas importancia tiene en el problema.
            Coste = (numero de repeticiones columna + numero de repeticiones fila)*-1
            El coste lo representamos en negativo para que el problema reconozca los mas importantes con un menor coste.
        '''
        valor = self.get_celda(fila, columna)
        costeFila = self.get_Fila(fila).count(valor)
        transpuesta = self.get_traspuesta()
        costeColumna = transpuesta.get_Fila(columna).count(valor)
        return -1 * (costeFila + costeColumna -2)
        #Se aplica -2 a la suma ya que se cuenta el propio valor de la casilla como 1 en fila y 1 en columna 
    
    def getPosisionesCasillasRepetidas(self):
        ''' Devuelve una lista con las posiciones de las casillas con valor repetidos en el tablero.
            Para el problema son nuestras posibles acciones.
            Para el calculo se hace la union de las posiciones repetidas en filas con las de columnas. 
        '''
        res = []
        listaCasillasConValorRepeticoEnColumnas = self.get_casillasRepetidasPorColumnaYValor()
        listaCasillasConValorRepeticoEnFilas = self.get_casillasRepetidasPorFilaYValor()
    
        #Union de las listas
        res.append(listaCasillasConValorRepeticoEnColumnas)
        for i in listaCasillasConValorRepeticoEnFilas:
            if i not in res:
                res.append(i)
        return res

    def get_casillasRepetidasPorFilaYValor(self):
        ''' Devuelve una lista con las posiciones [i,j] de todas las casillas repetidas dependiendo de su valor por filas. '''
        res = []
        for fila in range(0, self.size_hor()):
            valoresFila = self.get_Fila(fila)
            for valorFila in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
                if (valoresFila.count(valorFila) > 1):
                    for columna in range(0, self.size_hor()):
                        if(self.get_celda(fila, columna) == valorFila):
                            res.append([fila, columna])
        return res
 
 
    def get_casillasRepetidasPorColumnaYValor(self):
        ''' Devuelve una lista con las posiciones [i,j] de todas las casillas repetidas dependiendo de su valor por columnas. '''
        transpuesta = self.get_traspuesta()
        res = []
        for columna in range(0, transpuesta.size_hor()):
            valoresColumna = transpuesta.get_Fila(columna)
            for valorColumna in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
                if (valoresColumna.count(valorColumna) > 1):
                    for fila in range(0, transpuesta.size_hor()):
                        if(transpuesta.get_celda(columna, fila) == valorColumna):
                            res.append([fila, columna])
        return res
    
    def __str__(self):
        return 'Tablero: {}'.format(self.celdas)
