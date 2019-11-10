import copy

class Tablero:
    def __init__(self, celdas):
        self.celdas = celdas
    
    def size_hor(self):
        return len(self.celdas[0])
    
    def size_ver(self):
        return len(self.celdas)
    
    def get_mayorDimension(self):
        return max([self.size_hor(), self.size_ver()])
    
    def get_Fila(self, f):
        return self.celdas[f]
    
    def get_traspuesta(self):
        return Tablero(list(zip(*self.celdas)))
    
    def get_array_orden(self):
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
        
    def set_celda(self, f, c, nuevoValor):
        copia = copy.deepcopy(self.celdas)
        copia[f][c] = nuevoValor
        return Tablero(copia)
    
    def getCountRepetidasConCosteByValor(self, valor):
        res = 0
        for i in range(0,self.size_hor()):
            for j in range(0,self.size_ver()):
                if ((self.get_celda(i, j) == valor) & (self.get_coste_celda(i, j) < 0)):
                    res+=1
        return res;
            
    def get_coste_celda(self, fila, columna):
        valor = self.get_celda(fila, columna)
        costeFila = self.get_Fila(fila).count(valor)
        transpuesta = self.get_traspuesta()
        costeColumna = transpuesta.get_Fila(columna).count(valor)
        return -1 * (costeFila + costeColumna -2)
    
    def getPosisionesCasillasRepetidas(self):
        res = []
        listaColumnas = self.devuelveColumnasRepetidas()
        listaFilas = self.devuelveFilasRepetidas()
    
        for i in listaColumnas:
            if i not in res:
                res.append(i)
        for i in listaFilas:
            if i not in res:
                res.append(i)
        return res

    def devuelveFilasRepetidas(self):
        res = []
        for fila in range(0, self.size_hor()):
            valoresFila = self.get_Fila(fila)
            for valorFila in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
                if (valoresFila.count(valorFila) > 1):
                    for columna in range(0, self.size_hor()):
                        if(self.get_celda(fila, columna) == valorFila):
                            res.append([fila, columna])
        return res
 
 
    def devuelveColumnasRepetidas(self):
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
