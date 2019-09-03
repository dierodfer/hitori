import objetos as Objetos


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

def main():
    print(True+True)
#     tablero = Objetos.Tablero([[0, 4, 0], [3, 8, 1], [0, 9, 0]])
#     print(comprobacionPorColumnas(tablero))
#     print(comprobacionPorFilas(tablero))
  
if __name__== "__main__":
  main()