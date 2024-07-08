from src import InstanciaAsignacionCuadrillas
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
def generar_par_aleatorio_que_no_esta_en(conjunto, maximo):
    while True:
        a = random.randint(0, maximo)
        b = random.randint(0, maximo)
        new = min(a,b), max(a,b)
        if a != b and new not in conjunto and new not in conjunto:
            return new

def generate_inputs(var_values, instance_name):
    
    cant_trabajadores = var_values['cant_trabajadores']
    cant_ordenes = var_values['cant_ordenes']
    cant_ordenes_correlativas = var_values['cant_ordenes_correlativas']
    cant_ordenes_conflictivas = var_values['cant_ordenes_conflictivas']
    cant_ordenes_repetitivas = var_values['cant_ordenes_repetitivas']
    cant_conflictos_trabajadores = var_values['cant_conflictos_trabajadores']
    # Create an instance of the class
    instancia = InstanciaAsignacionCuadrillas()
    # Set the values
    instancia.cantidad_trabajadores = cant_trabajadores
    instancia.cantidad_ordenes = cant_ordenes
    instancia.ordenes = []
    for j in range(cant_ordenes):
        cant_trabajdores_orden = random.randint(1, math.ceil(0.3 * cant_trabajadores))
        beneficio = random.randint(1200 * cant_trabajdores_orden, 4000 * cant_trabajdores_orden)
        instancia.ordenes.append(Orden(j, beneficio, cant_trabajdores_orden))
    
    conflictos_trabajadores = set()
    for _ in range(cant_conflictos_trabajadores):
        conflictos_trabajadores.add(generar_par_aleatorio_que_no_esta_en(conflictos_trabajadores, cant_trabajadores - 1))
    ordenes_correlativas = set()
    for _ in range(cant_ordenes_correlativas):
        ordenes_correlativas.add(generar_par_aleatorio(cant_ordenes - 1))
    ordenes_conflictivas = set()
    for _ in range(cant_ordenes_conflictivas):
        ordenes_conflictivas.add(generar_par_aleatorio(cant_ordenes - 1))
    ordenes_repetitivas = set()
    for _ in range(cant_ordenes_repetitivas):
        ordenes_repetitivas.add(generar_par_aleatorio_que_no_esta_en(ordenes_repetitivas, cant_ordenes - 1))

    instancia.conflictos_trabajadores = list(conflictos_trabajadores)
    instancia.ordenes_correlativas = list(ordenes_correlativas)
    instancia.ordenes_conflictivas = list(ordenes_conflictivas)
    instancia.ordenes_repetitivas = list(ordenes_repetitivas)
    # Save the instance to a file
    instancia.save('input_rest_deseables/{}.txt'.format(instance_name))


if __name__ == "__main__":
    
    var_values = {}
    var_values['cant_trabajadores'] = 10
    var_values['cant_ordenes'] = math.ceil(1.5 * var_values['cant_trabajadores'])
    var_values['cant_ordenes_correlativas'] = math.ceil(0.05 * var_values['cant_ordenes'])
    var_values['cant_ordenes_conflictivas'] = math.ceil(0.05 * var_values['cant_ordenes'])

    # var_v enerate_inputs(var_values=var_values, instance_name=f"input_{var_values['cant_conflictos_trabajadores']}_{var_values['cant_ordenes_repetitivas']}")
    
    var_values['cant_conflictos_trabajadores'] = math.ceil(0.05 * var_values['cant_trabajadores'] )
    for i in range(1):
        var_values['cant_ordenes_repetitivas'] = math.floor(0.8 * (var_values['cant_ordenes'] * var_values['cant_ordenes'])//2)
        print('generando: ', f"input_{var_values['cant_conflictos_trabajadores']}_{var_values['cant_ordenes_repetitivas']}")
        generate_inputs(var_values=var_values, instance_name=f"input_{var_values['cant_conflictos_trabajadores']}_{var_values['cant_ordenes_repetitivas']}")