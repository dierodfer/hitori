import objetos as Objetos

tablero = Objetos.Tablero([[3, 1, 5, 0, 2, 6], [0, 3, 0, 5, 4, 0], [2, 4, 3, 6, 1, 5], [0, 5, 0, 3, 0, 4], [5, 2, 4, 0, 3, 1], [0, 6, 0, 2, 5, 1]])

def comprobacionPorColumnas(estado):
    transpuesta = estado.get_traspuesta()
    for columna in range(0, transpuesta.size_hor()):
        for c in [1,2,3,4,5,6,7,8,9]:
            if (transpuesta.get_Fila(columna).count(c) > 1):
                return False
    return True

def comprobacionPorFilas(estado):
    for fila in range(0, estado.size_hor()):
        for f in [1,2,3,4,5,6,7,8,9]:       
            if (estado.get_Fila(fila).count(f) > 1):
                return False
    return True

def getAdyacentesDiagonalesBloqueadas(estado,f,c):
   
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

def esBorde(estado, f, c):
    return (f+1 == estado.size_hor() or c+1 == estado.size_ver() or  f == 0 or  c == 0)
    
def cumpleRestriccionDeCamino(estado,f,c, filaAnterior=-1, columnaAnterior=-1, iteraciones=1):
        adyacentesDiagonales = getAdyacentesDiagonalesBloqueadas(estado, f, c)

        #Si entra en bucle, es un camino cerrado.
        if iteraciones > 25:
            print('false iteraciones')
            return False
               
        print("Iteracion: {}".format(iteraciones)) 
        print(f,c,adyacentesDiagonales)
        print(filaAnterior,columnaAnterior)
        #No es primera iteracion borra la casilla bloqueada anterior
        if(adyacentesDiagonales.count([filaAnterior,columnaAnterior]) == 1):
            adyacentesDiagonales.remove([filaAnterior,columnaAnterior])
        print(adyacentesDiagonales)
        
        #Si no es primera iteracion y es borde negativo
        if((filaAnterior > -1) & esBorde(estado, f, c)):
            print('false Borde')
            return False
        
        if(len(adyacentesDiagonales) == 0):
            print('True Ultima casilla')
            return True

        else:
            caminosErroneos = 0
            iteraciones=iteraciones+1
            for nuevaCasilla in adyacentesDiagonales: 
                if(cumpleRestriccionDeCamino(estado, nuevaCasilla[0], nuevaCasilla[1], f, c, iteraciones) == False):
                    caminosErroneos += 1
            #Modificar para solucionar el problema de mas de 2 caminos
            if((filaAnterior == -1) & esBorde(estado, f, c)):
                if(caminosErroneos > 0):
                    return False
                else:
                    return True      
            else:
                if((filaAnterior == -1) & (not esBorde(estado, f, c))):
                    if(caminosErroneos > 1):
                        return False
                    else:
                        return True  
                else:
                    if(caminosErroneos > 0):
                        return False;
                    else:
                        return True;



def main():
    print(esBorde(tablero, 4, 5))
    print(cumpleRestriccionDeCamino(tablero, 4, 5))
#     print(comprobacionPorColumnas(tablero))
#     print(comprobacionPorFilas(tablero))
#     tablero = Objetos.Tablero([[0, 4, 0], [3, 8, 1], [0, 9, 0]])
#     print(comprobacionPorColumnas(tablero))
#     print(comprobacionPorFilas(tablero))
  
if __name__== "__main__":
  main()