
from asignacion_cuadrillas import InstanciaAsignacionCuadrillas
import random
from recordclass import recordclass
Orden = recordclass('Orden', 'id beneficio cantidad_de_trabajadores')

random.seed(0)
def generar_par_aleratorio(maximo):
    while True:
        a = random.randint(0, maximo)
        b = random.randint(0, maximo)
        if a != b:
            return a, b



def generate_inputs():
    for cant_trabajadores in range(10, 15):
        for cant_ordenes in range(30, 35):
            cant_ordenes_correlativas = random.randint(0,5)
            cant_ordenes_conflictivas = random.randint(0,5)
            cant_conflictos_trabajadores = random.randint(2,5)  # Opcional
            cant_ordenes_repetitivas = random.randint(2,5)      # Opcional
            
            # Create an instance of the class
            instancia = InstanciaAsignacionCuadrillas()
            # Set the values
            instancia.cantidad_trabajadores = cant_trabajadores
            instancia.cantidad_ordenes = cant_ordenes
            instancia.ordenes = [Orden(j, random.randint(1500, 15000), random.randint(0, cant_trabajadores)) for j in range(cant_ordenes)]
            instancia.conflictos_trabajadores = [generar_par_aleratorio(cant_trabajadores) for i in range(cant_conflictos_trabajadores)]
            instancia.ordenes_correlativas = [generar_par_aleratorio(cant_ordenes_correlativas) for i in range(cant_ordenes_correlativas)]
            instancia.ordenes_conflictivas = [generar_par_aleratorio(cant_ordenes_correlativas) for i in range(cant_ordenes_conflictivas)]
            instancia.ordenes_repetitivas = [generar_par_aleratorio(cant_ordenes_correlativas) for i in range(cant_ordenes_repetitivas)]
            # Save the instance to a file
            instancia.save('inputs/input_{}_{}_{}_{}_{}_{}.txt'.format(cant_trabajadores, cant_ordenes, cant_conflictos_trabajadores, cant_ordenes_correlativas, cant_ordenes_conflictivas, cant_ordenes_repetitivas))