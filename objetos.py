import copy

class Tablero:
    def __init__(self, celdas):
        self.celdas = celdas
    
    def tamaño_hor(self):
        return len(self.celdas[0])
    
    def tamaño_ver(self):
        return len(self.celdas)
    
    def get_Fila(self, f):
        return self.celdas[f]
    
    def get_traspuesta(self):
        return Tablero(list(zip(*self.celdas)))
    
    def get_celda(self, f, c):
        #devuelve -1 si sale de rango
        if ((f<0) or (f+1>self.tamaño_hor()) or (c<0) or (c+1>self.tamaño_ver())):
            return -1
        else:
            return self.celdas[f][c]
        
    def set_celda(self, f, c, nuevoValor):
        copia = copy.deepcopy(self.celdas)
        copia[f][c] = nuevoValor
        return Tablero(copia)
    
    def __str__(self):
        return 'Tablero: {}'.format(self.celdas)
