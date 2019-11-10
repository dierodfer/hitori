import objetos as Objetos

class BloquearCasilla:
    def __init__(self, i, j, ordenPorCoste, cost=1):
        self.nombre = 'Bloquear casilla ({},{})'.format(i+1, j+1)
        self.f = i
        self.c = j
        self.coste = cost
        self.ordenPorCoste = ordenPorCoste
        self.estado = None;
    
    def noEstaBloqueada(self):
        return self.estado.get_celda(self.f,self.c) != 0;
    
    def valorSoloEnFilaYColumna(self):
        return (self.estado.get_coste_celda(self.f,self.c) < 0) #OPTIMIZADO
        #return ([self.f,self.c] in estado.getPosisionesCasillasRepetidas(estado))
    
    #Busca el valos mas importante que esta actualmente abierto y lo compara con el valor de la celda que quiere ejecutar en la accion
    def esValorMasRepetidoConCoste(self):
        valor = self.estado.get_celda(self.f,self.c)
        for elemento in self.ordenPorCoste:
            if self.estado.getCountRepetidasConCosteByValor(elemento[1]) > 0:
                return (valor == elemento[1])
        return False
    
    def esBorde(self, f, c):
        return (f+1 == self.estado.size_hor() or c+1 == self.estado.size_ver() or  f == 0 or  c == 0)
    
    def coste_de_aplicar(self):
        return self.coste
    
    #Sigue el camino de adyacentes diagolanales comprobando que no tiene mas adyacentes o 
    #toca un limite del tablero
    def cumpleRestriccionDeCamino(self,f,c, filaAnterior=-1, columnaAnterior=-1, iteraciones=1):
        self.adyacentesDiagonales = self.getAdyacentesDiagonalesBloqueadas(f, c)

        #Si entra en bucle, es un camino cerrado.
        if iteraciones > 20:
            print('Esto es un bucle, existe un camino cerrado.')
            return False
               
        #No es primera iteracion borra la casilla bloqueada anterior
        if(self.adyacentesDiagonales.count([filaAnterior,columnaAnterior]) == 1):
            self.adyacentesDiagonales.remove([filaAnterior,columnaAnterior])
        
        
        #Si no es primera iteracion y es borde negativo
        if((filaAnterior > -1) & self.esBorde(f, c)):
            return False
        
        if(len(self.adyacentesDiagonales) == 0):
            return True

        else:
            caminosErroneos = 0
            iteraciones=iteraciones+1
            for nuevaCasilla in self.adyacentesDiagonales: 
                #Recursividad
                if(self.cumpleRestriccionDeCamino(nuevaCasilla[0], nuevaCasilla[1], f, c, iteraciones) == False):
                    caminosErroneos += 1
           
            if((filaAnterior == -1) & self.esBorde(f, c)):
                if(caminosErroneos > 0):
                    return False
                else:
                    return True      
            else:
                if((filaAnterior == -1) & (not self.esBorde(f, c))):
                    if(caminosErroneos > 1):
                        return False
                    else:
                        return True  
                else:
                    if(caminosErroneos > 0):
                        return False;
                    else:
                        return True;  

    
    #Contiene una celda bloqueada directamente al lado
    def tieneAdyacentesEnCruzBloqueados(self):
        return ((self.estado.get_celda(self.f+1,self.c) == 0) 
                or (self.estado.get_celda(self.f, self.c+1) == 0) 
                or (self.estado.get_celda(self.f-1,self.c) == 0) 
                or (self.estado.get_celda(self.f, self.c-1) == 0))
    
    def getAdyacentesDiagonalesBloqueadas(self,f,c):
       
        res= []
        if(self.estado.get_celda(f+1,c+1) == 0):
            res.append([f+1,c+1])
        if(self.estado.get_celda(f+1,c-1) == 0):
            res.append([f+1,c-1])
        if(self.estado.get_celda(f-1,c+1) == 0):
            res.append([f-1,c+1])
        if(self.estado.get_celda(f-1,c-1) == 0):
            res.append([f-1,c-1])
        return res
    
    def es_aplicable(self, estado):
        self.estado=estado; 
        return (
                self.noEstaBloqueada()
                and self.esValorMasRepetidoConCoste() 
                and self.valorSoloEnFilaYColumna()
                and (not self.tieneAdyacentesEnCruzBloqueados()) 
                and self.cumpleRestriccionDeCamino(self.f, self.c)#No quitar estas variables se necesitan ya que es un algoritmo recursivo
                )
    
    def aplicar(self, estado):
        nuevo_estado = estado.set_celda(self.f,self.c,0)
        return nuevo_estado
    
    def __str__(self):
        return 'Accion: {}'.format(self.nombre)


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
            for valor in range(1,estado.get_mayorDimension()+1):       
                if (estado.get_Fila(fila).count(valor) > 1):
                    return False
        return True

    def comprobacionPorColumnas(self, estado):
        transpuesta = estado.get_traspuesta()
        for columna in range(0, transpuesta.size_hor()):
            for valor in range(1,estado.get_mayorDimension()+1):
                if (transpuesta.get_Fila(columna).count(valor) > 1):
                    return False
        return True
