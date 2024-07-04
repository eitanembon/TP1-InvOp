import sys
import cplex
from modules import *


def main():
    # El 1er parametro es el nombre del archivo de entrada 	
    nombre_archivo = sys.argv[1].strip()
    
    # Lectura de datos desde el archivo de entrada
    instancia = cargar_instancia(nombre_archivo)
    
    # Definicion del problema de Cplex
    prob = cplex.Cplex()

    # Definicion del modelo
    model = Modelo(instancia, prob)

    # Armamos modelo
    model.armar_lp()
    
    # Resolucion del modelo
    model.resolver_lp()

    # Obtencion de la solucion
    model.mostrar_solucion()

if __name__ == '__main__':
    main()
