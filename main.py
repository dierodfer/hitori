'''
Created on 26 abr. 2019

@author: Diego Rodriguez Fernandez
@author: Luis Miguel Garcia Rodriguez
'''
from tkinter import *
from tkinter.ttk import *
import random
from datetime import datetime
import time 
import ast
import hitori as problema_hitori
import busqueda_espacio_estados as busqueda_estados
import objetos as Objetos

# Variables Globales
filas = 0
columnas = 0
tipoBusqueda = 'Busqueda en procfundidad'
tablero = []


def init():
    sys.setrecursionlimit(99999)
    global window
    window = Tk()
    window.title("Hitori")
    window.geometry('800x500')
    global columnas
    # Labels    
    lblFila = Label(window, text="N: " + str(filas))
    lblFila.grid(padx=5, pady=5, column=3, row=0)
    lblColumna = Label(window, text="M: " + str(columnas))
    lblColumna.grid(padx=5, pady=5, column=4, row=0)   
    lblBusqueda = Label(window, text=tipoBusqueda)
    lblBusqueda.grid(padx=5, pady=5, column=5, row=0)
    lblX = Label(window, text="x")
    lblRuta = Label(window, text="Ruta:")
    lblRutaResultado = Label(window, text="Ruta donde se creara el resultado:")
    lblLineaALeer = Label(window, text="Linea:")
    lblError = Label(window, text="Errores", background="red")

    btnCargar = Button(window, text="Cargar", width=40)
    btnResolver = Button(window, text="Resolver", width=40)
    btnResolverFichero = Button(window, text="Cargar y resolver fichero", width=40)
    
    # Inputs
    inputRuta = Entry(window, width=30)
    inputRutaFicheroResultado = Entry(window, width=30)
    inputLineaALeer = Entry(window, width=4)   
    inputFilas = Entry(window, width=4)
    inputColumnas = Entry(window, width=4)
    inputTipo = Combobox(window)
    inputTipo['values'] = ('Busqueda en profundidad', 'Busqueda en anchura', 'Busqueda optima', 'Busqueda A*')
    inputTipo.current(0)
    
    # Muestra el error enviado
    def mostrarError(error):
        lblError.config(text=error)
        lblError.grid(pady=5, padx=5, column=3, row=3, columnspan=6)
    
    # Funciones botones
    def clickBtnCargar1():
        if len(inputFilas.get()) & len(inputColumnas.get()):
            escondeComponentes()
            lblFila.configure(text='N: ' + inputFilas.get())
            lblColumna.configure(text='M: ' + inputColumnas.get())
            lblBusqueda.configure(text=inputTipo.get())
            btnResolver.grid(column=3, row=1, columnspan=6)
            
            cargarVariablesGlobales(inputFilas.get(), inputColumnas.get(), inputTipo.get())
            createRandomTablero()
            displayTablero()
        else:
            mostrarError('Valores entre [1,9]')
        
    def clickBtnCargar2():
        if len(inputRuta.get()) > 0:
            escondeComponentes()
            if(cargarTableroFichero(inputRuta.get(), inputLineaALeer.get(), inputTipo.get())):
                # TODO cambiar valores N/A por los globales
                lblFila.configure(text='N: ' + str(filas))
                lblColumna.configure(text='M: ' + str(columnas))
                lblBusqueda.configure(text=tipoBusqueda)
                btnResolver.grid(column=3, row=1, columnspan=6)
            else:
                mostrarError('No se pudo cargar el archivo')
        else:
            mostrarError('Complete el campo ruta')
    
    def clickBtnResolver():
        starttime = datetime.now()
        solucion = resolverHitori()
        displayTableroSolucion(solucion)
        diff = datetime.now() - starttime;
        print('Finalizado en: ' + str(diff.seconds) + ',' + str(diff.microseconds) + 'segundos')
        escondeComponentes()
        
    def clickBtnResolverFichero():
        if len(inputRuta.get()) > 0:
            if len(inputRutaFicheroResultado.get()) > 0:
                escondeComponentes()
                if(cargarYResuelveTableroFichero(inputRuta.get(), inputRutaFicheroResultado.get(), inputTipo.get())):
                    # TODO cambiar valores N/A por los globales
                    lblFila.configure(text='N: ' + str(filas))
                    lblColumna.configure(text='M: ' + str(columnas))
                    lblBusqueda.configure(text=tipoBusqueda)
                else:
                    mostrarError('No se pudo cargar el archivo')
        else:
            mostrarError('Complete el campo ruta')
    
    def clickBtnGenerar():
        escondeComponentes()
        inputFilas.grid(padx=5, pady=5, column=6, row=1)
        lblX.grid(column=7, row=1)
        inputColumnas.grid(padx=5, pady=5, column=8, row=1)
        inputTipo.grid(padx=5, pady=5, column=3, row=1, columnspan=3)
        btnCargar.configure(command=clickBtnCargar1)
        btnCargar.grid(column=3, row=2, columnspan=6)
        
    def clickBtnLeer():
        escondeComponentes()
        inputRuta.grid(padx=5, pady=5, column=4, row=2, columnspan=3)
        lblRuta.grid(padx=5, pady=5, column=3, row=2)
        inputLineaALeer.grid(padx=5, pady=5, column=4, row=3, columnspan=3)
        lblLineaALeer.grid(padx=1, pady=1, column=3, row=3)
        inputTipo.grid(padx=5, pady=5, column=3, row=1, columnspan=3)
        btnCargar.configure(command=clickBtnCargar2)
        btnCargar.grid(column=3, row=4, columnspan=6)
    
    def clickBtnLeerFichero():
        escondeComponentes()
        inputRuta.grid(padx=5, pady=5, column=4, row=2, columnspan=3)
        lblRuta.grid(padx=5, pady=5, column=3, row=2)
        inputRutaFicheroResultado.grid(padx=5, pady=5, column=4, row=3, columnspan=3)
        lblRutaResultado.grid(padx=1, pady=1, column=3, row=3)
        inputTipo.grid(padx=5, pady=5, column=3, row=1, columnspan=3)
        btnResolverFichero.configure(command=clickBtnResolverFichero)
        btnResolverFichero.grid(column=3, row=4, columnspan=6)
    
    def escondeComponentes():
        inputColumnas.grid_remove()
        lblX.grid_remove()
        inputFilas.grid_remove()
        inputTipo.grid_remove()
        inputRuta.grid_remove()
        lblRuta.grid_remove()
        inputLineaALeer.grid_remove()
        lblLineaALeer.grid_remove()
        btnCargar.grid_remove()
        lblError.grid_remove()
        btnResolver.grid_remove()
        inputRutaFicheroResultado.grid_remove()
        lblRutaResultado.grid_remove()

    # Botones
    btnGenerar = Button(window, text="Generar Hitori", command=clickBtnGenerar, width=30)
    btnGenerar.grid(padx=5, pady=5, column=1, row=0)
    btnLeer = Button(window, text="Leer Hitori", command=clickBtnLeer, width=30)
    btnLeer.grid(padx=5, pady=5, column=1, row=1)
    btnLeerFichero = Button(window, text="Leer fichero completo", command=clickBtnLeerFichero, width=30)
    btnLeerFichero.grid(padx=5, pady=5, column=1, row=2)
    btnResolver.configure(command=clickBtnResolver)
    btnReset = Button(window, text="Reset", command=reset, width=30)
    btnReset.grid(padx=5, pady=5, column=1, row=3)

    window.mainloop()


def resolverHitori():
    print(tipoBusqueda)
    acciones = []
    result = ''
    table = Objetos.Tablero(tablero)
    for posicion in getPosisionesCasillasRepetidas(Objetos.Tablero(tablero)):
        acciones.append(problema_hitori.BloquearCasilla(posicion[0], posicion[1], table.get_coste_celda(posicion[0], posicion[1])))
    
    problemaHiroti = problema_hitori.ProblemaEspacioEstadosHitori(acciones, tablero);
    
    if(tipoBusqueda == 'Busqueda en anchura'):
        b_anchura = busqueda_estados.BusquedaEnAnchura(detallado=False)
        result = b_anchura.buscar(problemaHiroti)
    if(tipoBusqueda == 'Busqueda en profundidad'):
        b_profundidad = busqueda_estados.BusquedaEnProfundidad(detallado=False)
        result = b_profundidad.buscar(problemaHiroti)
    if(tipoBusqueda == 'Busqueda optima'):
        b_optima = busqueda_estados.Busquedaoptima(detallado=True)
        result = b_optima.buscar(problemaHiroti)
    if(tipoBusqueda == 'Busqueda A*'):
        # TODO 
        result = 'hola'
    print(result)
    return result

    
def cargarVariablesGlobales(fil, col, tipo):
    global filas
    global columnas
    global tipoBusqueda
    filas = int(fil)
    columnas = int(col)
    tipoBusqueda = tipo

    
def createRandomTablero():
    global tablero
    tablero = []
    for f in range(filas):
        arrayColumnas = []
        for c in range(columnas):
            arrayColumnas.append(random.randrange(1, filas + 1))
        tablero.append(arrayColumnas)


def displayTablero():
    global lblTablero
    for fila in range(filas):
        for columna in range(columnas):
            lblTablero = Label(window, text=tablero[fila][columna]).grid(padx=3, pady=3 , row=fila + 1, column=columna + 12)
    Label            
    
def displayTableroSolucion(solucion):
    global lblTableroSolucion
    if(solucion== None):
        lblSolucion= Label(window, text="Solucion:     No tiene solucion").grid(padx=5, pady=5, column=5, row=filas+5, columnspan=5)
    else:
        lblSolucion= Label(window, text="Solucion: ").grid(padx=5, pady=5, column=5, row=filas+5, columnspan=5)
        for fila in range(filas):
            for columna in range(columnas):
                 for posicion in solucion:
                    x = posicion[18:19]
                    y = posicion[20:21]
                    if(fila + 1 == int(x) and columna + 1 == int(y)):
                        lblTableroSolucion = Label(window, text='X').grid(padx=3, pady=3 , row=filas+fila+7, column=columna+12)
                        break
                    else:    
                        lblTableroSolucion = Label(window, text=tablero[fila][columna]).grid(padx=3, pady=3 , row=filas+fila+7, column=columna+12)

            
def cargarTableroFichero(ruta, lineaSeleccionada, tipoBusqueda):
    global tablero
    tablero = []
    fichero = open(ruta, 'r')
    lineaLectura = 1
    for linea in fichero:
        if lineaLectura == int(lineaSeleccionada):
            tablero = ast.literal_eval(linea)
            break
        else: 
            lineaLectura = lineaLectura + 1 
            
    tamColumna = len(tablero[0])
    tamFila = len(tablero)  
    cargarVariablesGlobales(tamColumna, tamFila, tipoBusqueda)
    displayTablero()
    return True


def cargarYResuelveTableroFichero(ruta, rutaSolucion, tipoBusqueda):
    global tablero
    tablero = []
    fichero = open(ruta, 'r')
    ficheroResultado = open(rutaSolucion + '/ficheroResultadoHitori.txt', 'w')
    for linea in fichero:
        starttime = datetime.now()
        tablero = ast.literal_eval(linea)
        tamColumna = len(tablero[0])
        tamFila = len(tablero)  
        cargarVariablesGlobales(tamColumna, tamFila, tipoBusqueda)
        solucion = resolverHitori()
        tiempo = datetime.now() - starttime
        ficheroResultado.write('Hitori: ' + str(linea) + 'Resultado: ' + str(solucion) + '\n' + 'Finalizado en: ' + str(tiempo.seconds) + ',' + str(tiempo.microseconds) + 'segundos' + '\n' + '\n')
    return ficheroResultado
    
    
def getPosisionesCasillasRepetidas(estado):
    res = []
    listaColumnas = devuelveRepetidasColumnas(estado)
    listaFilas = devuelveRepetidasFilas(estado)
#     listaColumnas.__add__(listaFilas)
    for i in listaColumnas:
        if i not in res:
            res.append(i)
    for i in listaFilas:
        if i not in res:
            res.append(i)
    return res


def devuelveRepetidasFilas(estado):
    res = []
    for fila in range(0, estado.size_hor()):
        for valorFila in [1, 2, 3, 4, 5, 6, 7, 8, 9]:       
            valoresFila = estado.get_Fila(fila)
            if (valoresFila.count(valorFila) > 1):
                for columna in range(0, estado.size_hor()):
                    if(estado.get_celda(fila, columna) == valorFila):
                        res.append([fila, columna])
    return res


def devuelveRepetidasColumnas(estado):
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

    
if __name__ == '__main__':

    def reset():
        window.destroy()
        init()
        
    init()
