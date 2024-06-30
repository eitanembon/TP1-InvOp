from asignacion_cuadrillas import InstanciaAsignacionCuadrillas
import random
import math
from recordclass import recordclass

Orden = recordclass('Orden', 'id beneficio cantidad_de_trabajadores')
random.seed(0)
# Generamos pares ordenados asi no hay ciclos de correlatividades
def generar_par_aleatorio(maximo):
    while True:
        a = random.randint(0, maximo)
        b = random.randint(0, maximo)
        if a != b:
            return min(a,b), max(a,b)

def generate_inputs():
    for i in range(100):

        cant_trabajadores = random.randint(20,100)
        cant_ordenes = random.randint(cant_trabajadores // 2, 4 * cant_trabajadores)

        cant_ordenes_correlativas = random.randint(math.ceil(0.03 * cant_ordenes), math.floor(0.08 * cant_ordenes))
        cant_ordenes_conflictivas = random.randint(math.ceil(0.02 * cant_ordenes), math.floor(0.05 * cant_ordenes))
        cant_conflictos_trabajadores = random.randint(math.ceil(0.02 * cant_trabajadores), math.floor(0.08 * cant_trabajadores))  # Opcional
        cant_ordenes_repetitivas = random.randint(math.ceil(0.05 * cant_ordenes), math.floor(0.12 * cant_ordenes))      # Opcional
            
        # Create an instance of the class
        instancia = InstanciaAsignacionCuadrillas()
        # Set the values
        instancia.cantidad_trabajadores = cant_trabajadores
        instancia.cantidad_ordenes = cant_ordenes
        instancia.ordenes = []
        for j in range(cant_ordenes):
            cant_trabajdores_orden = random.randint(1, cant_trabajadores)
            beneficio = random.randint(1200 * cant_trabajdores_orden, 4000 * cant_trabajdores_orden)
            instancia.ordenes.append(Orden(j, beneficio, cant_trabajdores_orden))
        instancia.conflictos_trabajadores = [generar_par_aleatorio(cant_trabajadores - 1) for i in range(cant_conflictos_trabajadores)]
        instancia.ordenes_correlativas = [generar_par_aleatorio(cant_ordenes - 1) for i in range(cant_ordenes_correlativas)]
        instancia.ordenes_conflictivas = [generar_par_aleatorio(cant_ordenes - 1) for i in range(cant_ordenes_conflictivas)]
        instancia.ordenes_repetitivas = [generar_par_aleatorio(cant_ordenes - 1) for i in range(cant_ordenes_repetitivas)]
        # Save the instance to a file
        instancia.save('inputs/input_{}.txt'.format(i))

generate_inputs()