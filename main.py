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

#Variables Globales
filas = 0
columnas = 0
tipoBusqueda = 'Tipo Busqueda 1'
tablero = []


def init():
    
    global window
    window = Tk()
    window.title("Hitori")
    window.geometry('800x350')

    #Labels    
    lblFila = Label(window, text="N: " + str(filas))
    lblFila.grid(padx=5, pady=5, column=3, row=0)
    lblColumna = Label(window, text="M: " + str(columnas))
    lblColumna.grid(padx=5, pady=5, column=4, row=0)   
    lblBusqueda = Label(window, text= tipoBusqueda)
    lblBusqueda.grid(padx=5, pady=5, column=5, row=0)
    lblX = Label(window, text="x")
    lblRuta = Label(window, text="Ruta:")
    lblError = Label(window, text="Errores", background="red")

    btnCargar = Button(window, text="Cargar", width=40)
    btnResolver = Button(window, text="Resolver", width=40)
    
    #Inputs
    inputRuta = Entry(window,width=30)    
    inputFilas = Entry(window,width=4)
    inputColumnas = Entry(window,width=4)
    inputTipo = Combobox(window)
    inputTipo['values']= ('Tipo busqueda 1', 'Tipo busqueda 2', 'Tipo busqueda 3', 'Tipo busqueda 4')
    inputTipo.current(0)
    
    #Muestra el error enviado
    def mostrarError(error):
        lblError.config(text=error)
        lblError.grid(pady=5, padx= 5, column=3, row=3, columnspan=6)
    
    
    #Funciones botones
    def clickBtnCargar1():
        if len(inputFilas.get()) & len(inputColumnas.get()):
            escondeComponentes()
            lblFila.configure(text='N: '+inputFilas.get())
            lblColumna.configure(text='M: '+inputColumnas.get())
            lblBusqueda.configure(text= inputTipo.get())
            btnResolver.grid(column=3, row=1, columnspan=6)
            
            cargarVariablesGlobales(inputFilas.get(), inputColumnas.get(), inputTipo.get())
            createRandomTablero()
            displayTablero()
        else:
            mostrarError('Valores entre [1,9]')
        
    def clickBtnCargar2():
        if len(inputRuta.get()) > 0:
            escondeComponentes()
            if(cargarFichero(inputRuta.get())):
                #TODO cambiar valores N/A por los globales
                lblFila.configure(text='N: '+'0')
                lblColumna.configure(text='M: '+'0')
            else:
                mostrarError('No se pudo cargar el archivo')
        else:
            mostrarError('Complete el campo ruta')
    
    def clickBtnResolver():
        starttime = datetime.now()
        resolverHitori()
        diff =  datetime.now() - starttime;
        print('Finalizado en: ' + str(diff.seconds) + ',' +str(diff.microseconds) + 'segundos')
        escondeComponentes()
    
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
        inputRuta.grid(padx=5, pady=5, column=4, row=1, columnspan=2)
        lblRuta.grid(padx=5, pady=5, column=3, row=1)
        btnCargar.configure(command=clickBtnCargar2)
        btnCargar.grid(column=3, row=2, columnspan=6)
    
    def escondeComponentes():
        inputColumnas.grid_remove()
        lblX.grid_remove()
        inputFilas.grid_remove()
        inputTipo.grid_remove()
        inputRuta.grid_remove()
        lblRuta.grid_remove()
        btnCargar.grid_remove()
        lblError.grid_remove()
        btnResolver.grid_remove()
    

    #Botones
    btnGenerar = Button(window, text="Generar Hitori", command=clickBtnGenerar, width=30)
    btnGenerar.grid(padx=5, pady=5, column=1, row=0)
    btnLeer = Button(window, text="Leer Hitori", command=clickBtnLeer, width=30)
    btnLeer.grid(padx=5, pady=5, column=1, row=1)
    btnResolver.configure(command=clickBtnResolver)
    btnLeer = Button(window, text="Reset", command=reset, width=30)
    btnLeer.grid(padx=5, pady=5, column=1, row=2)

    window.mainloop()

def resolverHitori():
    print(tipoBusqueda)
    time.sleep(5)
    #TODO HEURISTICAS

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
            arrayColumnas.append(random.randrange(1, 9))
        tablero.append(arrayColumnas)

def displayTablero():
    for fila in range(filas):
        for columna in range(columnas):
            Label(window, text=tablero[fila][columna]).grid(padx=3, pady=3 ,row=fila+1,column=columna+12)
            
def cargarFichero(ruta):
    #TODO Devuelve false en caso de error y true en caso positivo
    cargarVariablesGlobales('0','0', 'Tipo Busqueda 1')
    #Una vez cargado el tablero ejecutar displayTablero()
    return True
    
         
if __name__ == '__main__':
    def reset():
        window.destroy()
        init()
        
    init()