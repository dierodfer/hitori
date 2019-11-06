import objetos as Objetos

class BloquearCasilla:
    def __init__(self, i, j, arrayCostes, cost=1):
        self.nombre = 'Bloquear casilla ({},{})'.format(i+1, j+1)
        self.f = i
        self.c = j
        self.coste = cost
        self.arrayCostes = arrayCostes
    
    def estaEnRango(self, estado, f, c):
        return estado.get_celda(f,c) != -1;
    
    def noEstaBloqueada(self, estado, f, c):
        return estado.get_celda(f,c) != 0;
    
    def valorSoloEnFilaYColumna(self,estado):
        return (estado.get_coste_celda(self.f,self.c) < 0)
        #return ([self.f,self.c] in self.getPosisionesCasillasRepetidas(estado))
    
    def esValorMasRepetidoConCoste(self, estado):
        valor = estado.get_celda(self.f,self.c)
        for elemento in self.arrayCostes:
            if estado.getCountRepetidasConCosteByValor(elemento[1]) > 0:
                valorMaximo = elemento[1]
                break
        return valorMaximo == valor 
    
    def esBorde(self, estado, f, c):
        return (f+1 == estado.size_hor() or c+1 == estado.size_ver() or  f == 0 or  c == 0)
    
    def coste_de_aplicar(self):
        return self.coste
    
    #Sigue el camino de adyacentes diagolanales comprobando que no tiene mas adyacentes o 
    #toca un limite del tablero
    def cumpleRestriccionDeCamino(self,estado,f,c, filaAnterior=-1, columnaAnterior=-1, iteraciones=1):
        self.adyacentesDiagonales = self.getAdyacentesDiagonalesBloqueadas(estado, f, c)

        #Si entra en bucle, es un camino cerrado.
        if iteraciones > 20:
            print('Esto es un bucle, existe un camino cerrado.')
            return False
               
        #No es primera iteracion borra la casilla bloqueada anterior
        if(self.adyacentesDiagonales.count([filaAnterior,columnaAnterior]) == 1):
            self.adyacentesDiagonales.remove([filaAnterior,columnaAnterior])
        
        
        #Si no es primera iteracion y es borde negativo
        if((filaAnterior > -1) & self.esBorde(estado, f, c)):
            return False
        
        if(len(self.adyacentesDiagonales) == 0):
            return True

        else:
            caminosErroneos = 0
            iteraciones=iteraciones+1
            for nuevaCasilla in self.adyacentesDiagonales: 
                #Recursividad
                if(self.cumpleRestriccionDeCamino(estado, nuevaCasilla[0], nuevaCasilla[1], f, c, iteraciones) == False):
                    caminosErroneos += 1
           
            if((filaAnterior == -1) & self.esBorde(estado, f, c)):
                if(caminosErroneos > 0):
                    return False
                else:
                    return True      
            else:
                if((filaAnterior == -1) & (not self.esBorde(estado, f, c))):
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
    def tieneAdyacentesEnCruzBloqueados(self,estado,f,c):
        return ((estado.get_celda(f+1,c) == 0) 
                or (estado.get_celda(f, c+1) == 0) 
                or (estado.get_celda(f-1,c) == 0) 
                or (estado.get_celda(f, c-1) == 0))
    
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
        
    #Optimizado ya no se usa no borrar
    def devuelveRepetidasFilas(self,estado):
        res = []
        for fila in range(0, estado.size_hor()):
            for valorFila in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
                valoresFila = estado.get_Fila(fila)
                if (valoresFila.count(valorFila) > 1):
                    for columna in range(0, estado.size_hor()):
                        if(estado.get_celda(fila, columna) == valorFila):
                            res.append([fila, columna])
        return res
     
    #Optimizado ya no se usa no borrar
    def devuelveRepetidasColumnas(self,estado):
        transpuesta = estado.get_traspuesta()
        res = []
        for columna in range(0, transpuesta.size_hor()):
            for valorColumna in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
                valoresColumna = transpuesta.get_Fila(columna)
                if (valoresColumna.count(valorColumna) > 1):
                    for fila in range(0, transpuesta.size_hor()):
                        if(transpuesta.get_celda(columna, fila) == valorColumna):
                            res.append([fila, columna])
        return res
    
    #Optimizado ya no se usa no borrar
    def getPosisionesCasillasRepetidas(self,estado):
        res = []
        listaColumnas = self.devuelveRepetidasColumnas(estado)
        listaFilas = self.devuelveRepetidasFilas(estado)
    
        for i in listaColumnas:
            if i not in res:
                res.append(i)
        for i in listaFilas:
            if i not in res:
                res.append(i)
        return res
    
    
    def es_aplicable(self, estado):
        return (
                self.noEstaBloqueada(estado, self.f, self.c)
                and self.esValorMasRepetidoConCoste(estado) 
                and self.valorSoloEnFilaYColumna(estado)
                and (not self.tieneAdyacentesEnCruzBloqueados(estado,self.f,self.c)) 
                and self.cumpleRestriccionDeCamino(estado, self.f, self.c)
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
