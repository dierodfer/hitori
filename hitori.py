import objetos as Objetos
from pickle import FALSE


class BloquearCasilla:
    def __init__(self, i, j, cost=1):
        self.nombre = 'Bloquear casilla ({},{})'.format(i+1, j+1)
        self.f = i
        self.c = j
        self.coste = cost
    
    def estaEnRango(self, estado, f, c):
        return estado.get_celda(f,c) != -1;
    
    def noEstaBloqueada(self, estado, f, c):
        return estado.get_celda(f,c) != 0;
    
    def esBorde(self, estado, f, c):
        return (f+1 == estado.size_hor() or c+1 == estado.size_ver() or  f == 0 or  c == 0)
    
    def coste_de_aplicar(self):
        return self.coste
    
    #Sigue el camino de adyacentes diagolanales comprobando que no tiene mas adyacentes o 
    #toca un limite del tablero
    def cumpleRestriccionDeCamino(self,estado,f,c, filaAnterior=-1, columnaAnterior=-1, iteraciones=1, anteriores=[] ):
        self.adyacentesDiagonales = self.getAdyacentesDiagonalesBloqueadas(estado, f, c)
        self.anteriores = anteriores
        
        #No es primera iteracion borra la casilla bloqueada anterior
        if(self.adyacentesDiagonales.count([filaAnterior,columnaAnterior]) == 1):
            self.adyacentesDiagonales.remove([filaAnterior,columnaAnterior])
        
        
        if((len(self.adyacentesDiagonales) == 1) & (not self.esBorde(estado, f, c)) & (filaAnterior == -1)):
            return True
        
        if(len(self.adyacentesDiagonales) == 0):
            #Es primera iteracion
            if(filaAnterior == -1):
                return True
            #No es primera iteracion
            else: 
                if(self.esBorde(estado, f, c)):
                    return False
                else:
                    return True
        else:
            caminosCumplidos = 0
            for nuevaCasilla in self.adyacentesDiagonales: 
                 #Elimina error de bucles se bloqueadas
#                 if nuevaCasilla in self.anteriores:
#                     return False
#                 else:
#                     self.anteriores.append(nuevaCasilla)
                
                iteraciones=iteraciones+1
                print(iteraciones)
                if iteraciones > 3:
                   print(f,c)

                caminosCumplidos += self.cumpleRestriccionDeCamino(estado, nuevaCasilla[0], nuevaCasilla[1], f, c, iteraciones)
            #Modificar para solucionar el problema de mas de 2 caminos
            if(caminosCumplidos == 0):
                return False
            else:
                return True      
    
    
    #Contiene una celda bloqueada directamente al lado
    def tieneAdyacentesEnCruzBloqueados(self,estado,f,c):
        return ((estado.get_celda(f+1,c) == 0) 
                or (estado.get_celda(f, c+1) == 0) 
                or (estado.get_celda(f-1,c) == 0) 
                or (estado.get_celda(f, c-1) == 0))

#     def tieneAdyacentesDiagonalesBloqueadas(self,estado,f,c):
#         return ((estado.get_celda(f+1,c+1) == 0) 
#                 or (estado.get_celda(f+1,c-1) == 0) 
#                 or (estado.get_celda(f-1,c+1) == 0) 
#                 or (estado.get_celda(f-1,c-1) == 0))
    
    def tieneBucleSimple(self,estado,f,c):
        return (self.tieneAdyacentesEnCruzBloqueados(estado, f-1, c)  
                or  self.tieneAdyacentesEnCruzBloqueados(estado, f+1, c)  
                or  self.tieneAdyacentesEnCruzBloqueados(estado, f, c-1)  
                or  self.tieneAdyacentesEnCruzBloqueados(estado, f, c+1))
    
    def getAdyacentesDiagonalesBloqueadas(self,estado,f,c):
       
        res= []
        if(estado.get_celda(f+1,c+1) == 0):
            res.append([f+1,c+1])
        if(estado.get_celda(f+1,c-1) == 0):
            res.append([f+1,c-1])
        if(estado.get_celda(f-1,c+1) == 0):
            res.append([f-1,c+1])
        if(estado.get_celda(f-1,c-1) == 0):
            res.append([f-1,c-1])
        return res
        
    #def numeroAdyacentesDiagonalesBloqueadas(self,estado,f,c):
        # res = []
        #res.append(estado.get_celda(f+1,c+1) == 0)
        #res.append(estado.get_celda(f-1,c+1) == 0)
        #res.append(estado.get_celda(f+1,c-1) == 0)
        #res.append(estado.get_celda(f-1,c-1) == 0)
        #return sum(res);
    
    def es_aplicable(self, estado):
        print(estado)
        print('AdyacentesEnCruz')
        print((not self.tieneAdyacentesEnCruzBloqueados(estado,self.f,self.c)))
        print('Bucle')
        print(not self.tieneBucleSimple(estado,self.f,self.c))
        return (self.estaEnRango(estado, self.f, self.c) and self.noEstaBloqueada(estado, self.f, self.c) 
                and (not self.tieneAdyacentesEnCruzBloqueados(estado,self.f,self.c)) 
                and (not self.tieneBucleSimple(estado,self.f,self.c)) 
                and self.cumpleRestriccionDeCamino(estado, self.f, self.c)
                )
    
    def aplicar(self, estado):
        nuevo_estado = estado.set_celda(self.f,self.c,0)
        return nuevo_estado
    
    def __str__(self):
        return 'Accion: {}'.format(self.nombre)
    
# class DesbloquearCasilla:
#     def __init__(self, i, j, nuevoValor):
#         nombre = 'Desbloquear casilla ({},{})'.format(i+1, j+1)
#         super().__init__(nombre)
#         self.f = i
#         self.c = j
#         self.nuevoValor = nuevoValor
#         self.coste = 1
#     
#     def estaBloqueada(self, estado, f, c):
#         return estado.get_celda(f,c) == 0;
#     
#     def es_aplicable(self, estado,f,c):
#         return self.estaBloqueada(estado,f,c)
#     
#     def aplicar(self, estado,f,c,nuevoValor):
#         nuevo_estado = estado.set_celda(f,c,nuevoValor)
#         return nuevo_estado
    
class ProblemaEspacioEstadosHitori:
    def __init__(self, acciones, estado_inicial=None):
        if not isinstance(acciones, list):
            raise TypeError('Debe proporcionarse una lista de acciones')
        self.acciones = acciones
        self.estado_inicial = Objetos.Tablero(estado_inicial)

    def es_estado_final(self, estado):
        return self.comprobacionPorColumnas(estado) and self.comprobacionPorFilas(estado)

    def acciones_aplicables(self, estado):
        return (accion
                for accion in self.acciones
                if accion.es_aplicable(estado))
    
    def comprobacionPorFilas(self, estado):
        for fila in range(0, estado.size_hor()):
            for f in [1,2,3,4,5,6,7,8,9]:       
                if (estado.get_Fila(fila).count(f) > 1):
                    return False
        return True

    def comprobacionPorColumnas(self, estado):
        transpuesta = estado.get_traspuesta()
        for columna in range(0, transpuesta.size_hor()):
            for c in [1,2,3,4,5,6,7,8,9]:
                if (transpuesta.get_Fila(columna).count(c) > 1):
                    return False
        return True
