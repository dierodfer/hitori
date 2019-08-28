import copy

class Tablero:
    def __init__(self, celdas):
        self.celdas = celdas
    
    def size_hor(self):
        return len(self.celdas[0])
    
    def size_ver(self):
        return len(self.celdas)
    
    def get_Fila(self, f):
        return self.celdas[f]
    
    def get_traspuesta(self):
        return Tablero(list(zip(*self.celdas)))
    
    def get_celda(self, f, c):
        #devuelve -1 si sale de rango
        if ((f<0) or (f+1>self.size_hor()) or (c<0) or (c+1>self.size_ver())):
            return -1
        else:
            return self.celdas[f][c]
        
    def set_celda(self, f, c, nuevoValor):
        copia = copy.deepcopy(self.celdas)
        copia[f][c] = nuevoValor
        return Tablero(copia)
    
    def get_coste_celda(self, fila, columna):
        valor = self.get_celda(fila, columna)
        costeFila = estado.get_Fila(fila).count(valor)
        transpuesta = estado.get_traspuesta()
        costeColumna = transpuesta.get_Fila(columna).count(valor)
        return -1 * (costeFila + costeColumna)
    
    def __str__(self):
        return 'Tablero: {}'.format(self.celdas)
