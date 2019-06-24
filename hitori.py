import objetos as Objetos
import problema_espacio_estados as problema

tablero = Objetos.Tablero([[11,12,13],[0,22,23],[31,32,33]])


def init():
    hola = tablero.set_celda(1, 1, 79878)
    print(hola)
    print(tablero)

if __name__ == '__main__':
        
    init()


class BloquearCasilla(problema.Accion):
    def __init__(self, i, j):
        nombre = 'Bloquear casilla {}'.format(i, j)
        super().__init__(nombre)
        self.f = i
        self.c = j
        self.coste = 1
    
    def estaEnRango(self, estado, f, c):
        return estado.get_celda(f,c) != -1;
    
    def noEstaBloqueada(self, estado, f, c):
        return estado.get_celda(f,c) != 0;
    
    def esBorde(self, estado, f, c):
        return (f+1 == estado.tamaño_hor() or c+1 == estado.tamaño_ver() or  f == 0 or  c == 0)
    
    #Restricción temporal, esta comprueba que no se cierren caminos, es poco efectiva
    def cumpleRestriccionDeCamino(self,estado,f,c):
        if self.esBorde(self,estado,f,c):
            return (not self.tieneAdyacentesBloqueadas(self,estado,f,c))
        else:
            return (self.numeroAdyacentesDiagonalesBloqueadas(self,estado,f,c) < 2)
    
    #Contiene una celda bloqueada directamente al lado
    def tieneAdyacentesEnCruzBloqueados(self,estado,f,c):
        return ((estado.get_celda(f+1,c) == 0) 
                or (estado.get_celda(f, c+1) == 0) 
                or (estado.get_celda(f-1,c) == 0) 
                or (estado.get_celda(f, c-1) == 0))

    def tieneAdyacentesDiagonalesBloqueadas(self,estado,f,c):
        return ((estado.get_celda(f+1,c+1) == 0) 
                or (estado.get_celda(f+1,c-1) == 0) 
                or (estado.get_celda(f-1,c+1) == 0) 
                or (estado.get_celda(f-1,c-1) == 0))
    
    def numeroAdyacentesDiagonalesBloqueadas(self,estado,f,c):
        res = []
        res.append(estado.get_celda(f+1,c+1) == 0)
        res.append(estado.get_celda(f-1,c+1) == 0)
        res.append(estado.get_celda(f+1,c-1) == 0)
        res.append(estado.get_celda(f-1,c-1) == 0)
        return sum(res);
    
    def es_aplicable(self, estado, f,c):
        return (self.estaEnRango(estado, f, c) and self.noEstaBloqueada(estado, f, c) 
                and (not self.tieneAdyacentesEnCruzBloqueados(estado,f,c)) and self.cumpleRestriccionDeCamino(estado, f, c))
    
    def aplicar(self, estado,f,c):
        nuevo_estado = estado.set_celda(f,c,0)
        return nuevo_estado
    
class DesbloquearCasilla(problema.Accion):
    def __init__(self, i, j, nuevoValor):
        nombre = 'Desbloquear casilla {}'.format(i, j)
        super().__init__(nombre)
        self.f = i
        self.c = j
        self.nuevoValor = nuevoValor
        self.coste = 1
    
    def estaBloqueada(self, estado, f, c):
        return estado.get_celda(f,c) == 0;
    
    def es_aplicable(self, estado,f,c):
        return self.estaBloqueada(estado,f,c)
    
    def aplicar(self, estado,f,c,nuevoValor):
        nuevo_estado = estado.set_celda(f,c,nuevoValor)
        return nuevo_estado
    
class ProblemaEspacioEstadosHitori:
    def __init__(self, acciones, estado_inicial=None):
        if not isinstance(acciones, list):
            raise TypeError('Debe proporcionarse una lista de acciones')
        self.acciones = acciones
        self.estado_inicial = Objetos.Tablero(estado_inicial)

    def es_estado_final(self, estado):
        return True#Añadir método LUIS que devuelva boolean

    def acciones_aplicables(self, estado):
        return (acción
                for acción in self.acciones
                if acción.es_aplicable(estado))
        
        
#SE DEBE DE AÑADIR LA FORMA DE INDICARLA EL ALGORITMO CUANDO USAR BLOQUEAR Y DESBLOQUEAR CASILLA
