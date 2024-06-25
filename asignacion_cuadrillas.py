import sys
#importamos el modulo cplex
import cplex
from recordclass import recordclass
from functools import reduce
import math
TOLERANCE =10e-6 
Orden = recordclass('Orden', 'id beneficio cantidad_de_trabajadores')

class InstanciaAsignacionCuadrillas:
    def __init__(self):
        self.cantidad_trabajadores = 0
        self.cantidad_ordenes = 0
        self.ordenes = []
        self.conflictos_trabajadores = []
        self.ordenes_correlativas = []
        self.ordenes_conflictivas = []
        self.ordenes_repetitivas = []
        self.dias = 6
        self.turnos = 5
    
    def save(self, path):
        if not path:
            raise ValueError("Path is empty")
        with open(path, 'w') as writeable:
            # Se escribe la cantidad de trabajadores y la cantidad de ordenes
            writeable.write(str(self.cantidad_trabajadores) + '\n')
            writeable.write(str(self.cantidad_ordenes) + '\n')
            
            # Se escriben las ordenes
            for orden in self.ordenes:
                writeable.write(f'{orden.id} {orden.beneficio} {orden.cantidad_de_trabajadores}\n')
            
            # Se escriben los conflictos entre los trabajadores
            writeable.write(str(len(self.conflictos_trabajadores)) + '\n')
            for conflicto in self.conflictos_trabajadores:
                writeable.write(f'{conflicto[0]} {conflicto[1]}\n')
            
            # Se escriben las ordenes correlativas
            writeable.write(str(len(self.ordenes_correlativas)) + '\n')
            for correlativa in self.ordenes_correlativas:
                writeable.write(f'{correlativa[0]} {correlativa[1]}\n')
            
            # Se escriben las ordenes conflictivas
            writeable.write(str(len(self.ordenes_conflictivas)) + '\n')
            for conflictiva in self.ordenes_conflictivas:
                writeable.write(f'{conflictiva[0]} {conflictiva[1]}\n')
            
            # Se escriben las ordenes repetitivas
            writeable.write(str(len(self.ordenes_repetitivas)) + '\n')
            for repetitiva in self.ordenes_repetitivas:
                writeable.write(f'{repetitiva[0]} {repetitiva[1]}\n')
            
    def leer_datos(self,nombre_archivo):

        # Se abre el archivo
        f = open(nombre_archivo)

        # Lectura cantidad de trabajadores
        self.cantidad_trabajadores = int(f.readline())
        
        # Lectura cantidad de ordenes
        self.cantidad_ordenes = int(f.readline())
        
        # Lectura de las ordenes
        self.ordenes = []
        for i in range(self.cantidad_ordenes):
            linea = f.readline().rstrip().split(' ')
            self.ordenes.append(Orden(linea[0],linea[1],linea[2]))
        
        # Lectura cantidad de conflictos entre los trabajadores
        cantidad_conflictos_trabajadores = int(f.readline())
        
        # Lectura conflictos entre los trabajadores
        self.conflictos_trabajadores = []
        for i in range(cantidad_conflictos_trabajadores):
            linea = f.readline().split(' ')
            self.conflictos_trabajadores.append(list(map(int,linea)))
            
        # Lectura cantidad de ordenes correlativas
        cantidad_ordenes_correlativas = int(f.readline())
        
        # Lectura ordenes correlativas
        self.ordenes_correlativas = []
        for i in range(cantidad_ordenes_correlativas):
            linea = f.readline().split(' ')
            self.ordenes_correlativas.append(list(map(int,linea)))
            
        # Lectura cantidad de ordenes conflictivas
        cantidad_ordenes_conflictivas = int(f.readline())
        
        # Lectura ordenes conflictivas
        self.ordenes_conflictivas = []
        for i in range(cantidad_ordenes_conflictivas):
            linea = f.readline().split(' ')
            self.ordenes_conflictivas.append(list(map(int,linea)))
        
        # Lectura cantidad de ordenes repetitivas
        cantidad_ordenes_repetitivas = int(f.readline())
        
        # Lectura ordenes repetitivas
        self.ordenes_repetitivas = []
        for i in range(cantidad_ordenes_repetitivas):
            linea = f.readline().split(' ')
            self.ordenes_repetitivas.append(list(map(int,linea)))
        
        # Se cierra el archivo de entrada
        f.close()


def cargar_instancia(nombre_archivo="entrada_asignacion_cuadrillas.txt"):
    # Crea la instancia vacia
    instancia = InstanciaAsignacionCuadrillas()
    # Llena la instancia con los datos del archivo de entrada 
    instancia.leer_datos(nombre_archivo)
    return instancia

class Modelo:
    def __init__(self, instancia, prob):
        self.prob = prob
        self.instancia = instancia
        self.coeficientes_funcion_objetivo = []
        self.nombres2indices = {}
        # Poner nombre a las variables
        self.nombres = []

    def armar_lp(self, nombre_archivo_salida = "asignacionCuadrillas"):

        # Agregar las variables
        self.agregar_variables_sin_refactor()

        # Agregar las restricciones 
        self.agregar_restricciones()

        # Setear el sentido del self.problema
        self.prob.objective.set_sense(self.prob.objective.sense.maximize)

        # nombre del problema
        self.prob.set_problem_name('Asignacion de cuadrillas')

        # Escribir el lp a archivo
        self.prob.write(f'{nombre_archivo_salida}.lp')



    """====================Variables===================="""
    def agregar_variable(self,nombre, coeficiente, indices):
        nombre_var = nombre + '_' + '_'.join(map(str,indices))
        # print(nombre_var)
        self.nombres.append(nombre)
        self.coeficientes_funcion_objetivo.append(coeficiente)
        self.nombres2indices[nombre_var] = len(self.nombres) - 1
    
    def agregar_variables_sin_refactor(self):
        # Definir y agregar las variables:
        # metodo 'add' de 'variables', con parametros:
        # obj: costos de la funcion objetivo
        # lb: cotas inferiores
        # ub: cotas superiores
        # types: tipo de las variables
        # names: nombre (como van a aparecer en el archivo .lp)
        
        # Llenar coef\_funcion\_objetivo

        # Poner nombre a las variables
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos):
                        nombre = 'W_' + str(i) + '_' + str(j) + '_' + str(d) + '_' + str(t)
                        self.nombres.append(nombre)
                        self.coeficientes_funcion_objetivo.append(0)
                        self.nombres2indices[nombre] = len(self.nombres) - 1
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    nombre = 'H_' + str(i) + '_' + str(d) + '_' + str(t)
                    self.nombres.append(nombre)
                    self.coeficientes_funcion_objetivo.append(0)
                    self.nombres2indices[nombre] = len(self.nombres) - 1
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                nombre = 'L_' + str(i) + '_' + str(d)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(0)
                self.nombres2indices[nombre] = len(self.nombres) - 1
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                nombre = 'X_' + str(i) + '_' + str(j)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(0)
                self.nombres2indices[nombre] = len(self.nombres) - 1
        for i in range(self.instancia.cantidad_trabajadores):
            for k in range(5):
                nombre = 'Y_' + str(i) + '_' + str(k)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(-1000)
                self.nombres2indices[nombre] = len(self.nombres) - 1
            for k in range(5, 10):
                nombre = 'Y_' + str(i) + '_' + str(k)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(-1200)
                self.nombres2indices[nombre] = len(self.nombres) - 1
            for k in range(10, 15):
                nombre = 'Y_' + str(i) + '_' + str(k)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(-1400)
                self.nombres2indices[nombre] = len(self.nombres) - 1
            for k in range(15, 20):
                nombre = 'Y_' + str(i) + '_' + str(k)
                self.nombres.append(nombre)
                self.coeficientes_funcion_objetivo.append(-1500)
                self.nombres2indices[nombre] = len(self.nombres) - 1
        
        for j in range(self.instancia.cantidad_ordenes):
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    nombre = 'Z_' + str(j) + '_' + str(d) + '_' + str(t)
                    self.nombres.append(nombre)
                    self.coeficientes_funcion_objetivo.append(0)
                    self.nombres2indices[nombre] = len(self.nombres) - 1
        for j in range(self.instancia.cantidad_ordenes):
            nombre = 'K_' + str(j)
            self.nombres.append(nombre)
            self.coeficientes_funcion_objetivo.append(int(self.instancia.ordenes[j].beneficio))
            self.nombres2indices[nombre] = len(self.nombres) - 1
            
        
        cantVar = len(self.nombres)
        # Agregar las variables
        self.prob.variables.add(obj = self.coeficientes_funcion_objetivo, lb = [0]*cantVar, ub = [1]*cantVar, types=['B']*cantVar, names=self.nombres)



    def agregar_variables(self):
        # Definir y agregar las variables:
        # metodo 'add' de 'variables', con parametros:
        # obj: costos de la funcion objetivo
        # lb: cotas inferiores
        # ub: cotas superiores
        # types: tipo de las variables
        # names: nombre (como van a aparecer en el archivo .lp)
        
        # Llenar coef\_funcion\_objetivo
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos):
                        self.agregar_variable('W', 0, [i, j, d, t])
                        
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    self.agregar_variable('H', 0, [i, d, t])

        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                self.agregar_variable('L', 0, [i, d])

        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                self.agregar_variable('X', 0, [i, j])
                
        for i in range(self.instancia.cantidad_trabajadores):
            for k in range(5):
                self.agregar_variable('Y', -1000, [i, k])
            for k in range(5, 10):
                self.agregar_variable('Y', -1200, [i, k])
            for k in range(10, 15):
                self.agregar_variable('Y', -1400, [i, k])
            for k in range(15, 20):
                self.agregar_variable('Y', -1500, [i, k])
        
        for j in range(self.instancia.cantidad_ordenes):
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    self.agregar_variable('Z', 0, [j, d, t])
        for j in range(self.instancia.cantidad_ordenes):
            self.agregar_variable('K', 0, [j])
            
        
        cantVar = len(self.nombres)
        # Agregar las variables
        self.prob.variables.add(obj = self.coeficientes_funcion_objetivo, lb = [0]*cantVar, ub = [1]*cantVar, types=['B']*cantVar, names=self.nombres)
    
    """====================Restricciones===================="""
    def agregar_restricciones(self):
        # Agregar las restricciones ax <= (>= ==) b:
        # funcion 'add' de 'linear_constraints' con parametros:
        # lin_expr: lista de listas de [ind,val] de a
        # sense: lista de 'L', 'G' o 'E'
        # rhs: lista de los b
        # names: nombre (como van a aparecer en el archivo .lp)
        
        # Notar que cplex espera "una matriz de restricciones", es decir, una
        # lista de restricciones del tipo ax <= b, [ax <= b]. Por lo tanto, aun cuando
        # agreguemos una unica restriccion, tenemos que hacerlo como una lista de un unico
        # elemento.
        nro_ecuacion = 0
        self.un_trabajador_no_puede_realizar_dos_trabajos_al_mismo_tiempo(nro_ecuacion)
        nro_ecuacion += 1
        self.un_trabajador_no_puede_realizar_un_trabajo_en_dos_tiempos_diferentes(nro_ecuacion)
        nro_ecuacion += 1
        self.Z_y_X_sii_W(nro_ecuacion)
        nro_ecuacion += 1
        self.cada_orden_de_trebajo_se_puede_realizar_utilizando_un_solo_turno(nro_ecuacion)
        nro_ecuacion += 1
        self.la_cantidad_de_trabajadores_de_la_tarea_j_es_tj_si_se_realiza_y_0_si_no_se_realiza(nro_ecuacion)
        nro_ecuacion += 1
        self.un_trabajador_no_puede_trabajar_los_6_dias_de_la_planificacion(nro_ecuacion)
        nro_ecuacion += 1
        self.un_trabajador_no_puede_trabajar_los_5_turnos_de_un_dia(nro_ecuacion)
        nro_ecuacion += 1
        self.Lid_sii_existe_t_tal_que_Hidt(nro_ecuacion)
        nro_ecuacion += 1
        self.si_el_trabajador_i_realiza_su_k_tareas_sii_el_trabajador_i_realiza_k_ordenes(nro_ecuacion)
        nro_ecuacion += 1
        self.si_el_trabajador_i_hizo_k_mas_1_ordenes_entonces_hizo_k(nro_ecuacion)
        nro_ecuacion += 1
        self.para_todo_par_de_trabajadores_la_diferencia_de_la_cantidad_de_trabajos_que_realizan_no_puede_ser_mayor_a_8(nro_ecuacion) 
        """Ordenes correlativas"""
        nro_ecuacion += 1
        self.si_la_orden_j_debe_realizarse_antes_que_la_orden_k_enotonces_Zjdt_sii_Zkdt_mas_1(nro_ecuacion)
        nro_ecuacion += 1
        self.si_hay_dos_ordenes_correlativas_la_primera_no_puede_realizarse_en_el_ultimo_turno_y_la_ultima_no_puede_realizarse_en_el_primero(nro_ecuacion)
        nro_ecuacion += 1
        self.si_las_ordenes_j1_y_j2_son_conflictivas_y_se_realizan_en_turnos_consecutivos_entonces_no_puede_ser_el_mismo_trabajador_quien_las_realiza(nro_ecuacion)

        ###(Opcional) Si i1 y i2 tienen conflicos, entonces no pueden estar asignados en una orden de trabajo 
        # nro_ecuacion += 1
        # nro_restriccion = 0
        # for conflicto in self.instancia.conflictos_trabajadores:
        #     for j in range(self.instancia.cantidad_ordenes):
        #         indices = [self.nombres2indices[f'X_{conflicto[0]}_{j}'], self.nombres2indices[f'X_{conflicto[1]}_{j}']]
        #         valores = [1, 1]
        #         fila = [indices,valores]
        #         self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
        #         nro_restriccion += 1

        # ### (Opcional) Si j y j'  son repetitivas entonces no puede haber un trabajador i que las realice a ambas
        # nro_ecuacion += 1
        # nro_restriccion = 0
        # for repeticion in self.instancia.ordenes_repetitivas:
        #     for i in range(self.instancia.cantidad_trabajadores):
        #         indices = [self.nombres2indices[f'X_{i}_{repeticion[0]}'], self.nombres2indices[f'X_{i}_{repeticion[1]}']]
        #         valores = [1, 1]
        #         fila = [indices,valores]
        #         self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
        #         nro_restriccion += 1
        
    def si_las_ordenes_j1_y_j2_son_conflictivas_y_se_realizan_en_turnos_consecutivos_entonces_no_puede_ser_el_mismo_trabajador_quien_las_realiza(self, nro_ecuacion):
        nro_restriccion = 0
        for orden in self.instancia.ordenes_conflictivas:
            for i in range(self.instancia.cantidad_trabajadores):
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos - 1): 
                        indices1 = [self.nombres2indices[f'Z_{orden[0]}_{d}_{t}'], self.nombres2indices[f'Z_{orden[1]}_{d}_{t+1}'], self.nombres2indices[f'X_{i}_{orden[0]}'], self.nombres2indices[f'X_{i}_{orden[1]}']]
                        indices2 = [self.nombres2indices[f'Z_{orden[1]}_{d}_{t}'], self.nombres2indices[f'Z_{orden[0]}_{d}_{t+1}'], self.nombres2indices[f'X_{i}_{orden[0]}'], self.nombres2indices[f'X_{i}_{orden[1]}']]
                        valores = [2, 2, 1, 1]
                        fila1 = [indices1,valores]
                        fila2 = [indices2,valores]
                        self.prob.linear_constraints.add(lin_expr=[fila1, fila2], senses=['L', 'L'], rhs=[4, 4], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}', f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion + 1}'])
                        nro_restriccion += 2

    def para_todo_par_de_trabajadores_la_diferencia_de_la_cantidad_de_trabajos_que_realizan_no_puede_ser_mayor_a_8(self, nro_ecuacion):
        ###-8 \leq \sum_{j\in O} X_{ij} - X_{i'j} \leq 8, \qquad \forall i<i' \in T
        nro_restriccion = 0
        for j in range(self.instancia.cantidad_ordenes):
            for i1 in range(self.instancia.cantidad_trabajadores-1):
                for i2 in range(i1+1,self.instancia.cantidad_trabajadores):
                    indices = [self.nombres2indices[f'X_{i1}_{j}'], self.nombres2indices[f'X_{i2}_{j}']]
                    valores = [1, -1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[8], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1 
        for j in range(self.instancia.cantidad_ordenes):
            for i1 in range(self.instancia.cantidad_trabajadores-1):
                for i2 in range(i1+1,self.instancia.cantidad_trabajadores):
                    indices = [self.nombres2indices[f'X_{i1}_{j}'], self.nombres2indices[f'X_{i2}_{j}']]
                    valores = [1, -1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['G'], rhs=[-8], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1

    def si_hay_dos_ordenes_correlativas_la_primera_no_puede_realizarse_en_el_ultimo_turno_y_la_ultima_no_puede_realizarse_en_el_primero(self, nro_ecuacion):
        nro_restriccion = 0
        for orden in self.instancia.ordenes_correlativas:
            for d in range(self.instancia.dias):
                indices = [self.nombres2indices[f'Z_{orden[0]}_{d}_{self.instancia.turnos-1}'], self.nombres2indices[f'Z_{orden[1]}_{d}_0']]
                valores = [1, 1]
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1

    def si_la_orden_j_debe_realizarse_antes_que_la_orden_k_enotonces_Zjdt_sii_Zkdt_mas_1(self, nro_ecuacion):
        nro_restriccion = 0
        for orden in self.instancia.ordenes_correlativas:
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos - 1):
                    indices = [self.nombres2indices[f'Z_{orden[0]}_{d}_{t}'], self.nombres2indices[f'Z_{orden[1]}_{d}_{t+1}']]
                    valores = [1, -1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1

    def si_el_trabajador_i_hizo_k_mas_1_ordenes_entonces_hizo_k(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            for k in range(19):
                indices = [self.nombres2indices[f'Y_{i}_{k+1}'], self.nombres2indices[f'Y_{i}_{k}']]
                valores = [1, -1]
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1

    def si_el_trabajador_i_realiza_su_k_tareas_sii_el_trabajador_i_realiza_k_ordenes(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                indices = [self.nombres2indices[f'X_{i}_{j}']]
                valores = [1]

            for k in range(20):
                indices.append(self.nombres2indices[f'Y_{i}_{k}'])
                valores.append(-1)

            fila = [indices,valores]
            self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
            nro_restriccion += 1

    def Lid_sii_existe_t_tal_que_Hidt(self, nro_ecuacion):
        nro_restriccion = 0
        ## Si el trabajador i trabaja en el dia d entonces existe un turno t en el que el trabajador i trabaja en el dia d
        nro_restriccion = self.Lid_implica_existe_t_tq_Hidt(nro_ecuacion, nro_restriccion)
        ## Si existe un turno t en el que el trabajador i trabaja en el dia d entonces el trabajador i trabaja en el dia d
        self.existe_t_tq_Hidt_implica_Lid(nro_ecuacion, nro_restriccion)

    def existe_t_tq_Hidt_implica_Lid(self, nro_ecuacion, nro_restriccion):
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                indices = [self.nombres2indices[f'L_{i}_{d}']]
                valores = [5]
                for t in range(self.instancia.turnos):
                    indices.append(self.nombres2indices[f'H_{i}_{d}_{t}'])
                    valores.append(-1)
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['G'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1

    def Lid_implica_existe_t_tq_Hidt(self, nro_ecuacion, nro_restriccion):
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                indices = [self.nombres2indices[f'L_{i}_{d}']]
                valores = [1]
                for t in range(self.instancia.turnos):
                    indices.append(self.nombres2indices[f'H_{i}_{d}_{t}'])
                    valores.append(-1)
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1
        return nro_restriccion

    def un_trabajador_no_puede_trabajar_los_5_turnos_de_un_dia(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                indices = []
                valores = []
                for t in range(self.instancia.turnos):
                    indices.append(self.nombres2indices[f'H_{i}_{d}_{t}'])
                    valores.append(1)
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[4], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1

    def un_trabajador_no_puede_trabajar_los_6_dias_de_la_planificacion(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            indices = []
            valores = []
            for d in range(self.instancia.dias):
                indices.append(self.nombres2indices[f'L_{i}_{d}'])
                valores.append(1)
            fila = [indices,valores]
            self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[5], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
            nro_restriccion += 1

    def la_cantidad_de_trabajadores_de_la_tarea_j_es_tj_si_se_realiza_y_0_si_no_se_realiza(self, nro_ecuacion):
        nro_restriccion = 0
        for j in range(self.instancia.cantidad_ordenes):
            indices = [self.nombres2indices[f'K_{j}']]
            valores = [int(self.instancia.ordenes[j].cantidad_de_trabajadores)]
            for i in range(self.instancia.cantidad_trabajadores):
                indices.append(self.nombres2indices[f'X_{i}_{j}'])
                valores.append(-1)
            fila = [indices,valores]
            self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
            nro_restriccion += 1

    def cada_orden_de_trebajo_se_puede_realizar_utilizando_un_solo_turno(self, nro_ecuacion):
        nro_restriccion = 0
        for j in range(self.instancia.cantidad_ordenes):
            indices = [self.nombres2indices[f'K_{j}']]
            valores = [1]
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    indices.append(self.nombres2indices[f'Z_{j}_{d}_{t}'])
                    valores.append(-1)
            fila = [indices,valores]
            self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
            nro_restriccion += 1

    def Z_y_X_sii_W(self, nro_ecuacion):
        nro_restriccion = 0
        # Si el trabajador i realiza la tarea j en el dia d y el turno t, entonces la tarea j se realiza en el dia d y el turno t y además el trabajador i realiza la tarea j
        nro_restriccion = self.W_implica_Z_y_X(nro_ecuacion, nro_restriccion)
        # la tarea j se realiza en el dia d y el turno t y además el trabajador i realiza la tarea j, entonces el trabajador i realiza la tarea j en el dia d y el turno t
        self.Z_y_X_implica_W(nro_ecuacion, nro_restriccion)

    def Z_y_X_implica_W(self, nro_ecuacion, nro_restriccion):
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos):
                        indices = [self.nombres2indices[f'W_{i}_{j}_{d}_{t}'], self.nombres2indices[f'X_{i}_{j}'], self.nombres2indices[f'Z_{j}_{d}_{t}']]
                        valores = [-1, 1, 1]
                        fila = [indices,valores]
                        self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                        nro_restriccion += 1

    def W_implica_Z_y_X(self, nro_ecuacion, nro_restriccion):
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos):
                        indices = [self.nombres2indices[f'W_{i}_{j}_{d}_{t}'], self.nombres2indices[f'X_{i}_{j}'], self.nombres2indices[f'Z_{j}_{d}_{t}']]
                        valores = [2, -1, -1]
                        fila = [indices,valores]
                        self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                        nro_restriccion += 1
        return nro_restriccion
    def un_trabajador_no_puede_realizar_un_trabajo_en_dos_tiempos_diferentes(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            for j in range(self.instancia.cantidad_ordenes):
                indices = [self.nombres2indices[f'X_{i}_{j}']]
                valores = [1]
                for d in range(self.instancia.dias):
                    for t in range(self.instancia.turnos):
                        indices.append(self.nombres2indices[f'W_{i}_{j}_{d}_{t}'])
                        valores.append(-1)
                        
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1

    def un_trabajador_no_puede_realizar_dos_trabajos_al_mismo_tiempo(self, nro_ecuacion):
        nro_restriccion = 0
        for i in range(self.instancia.cantidad_trabajadores):
            for d in range(self.instancia.dias):
                for t in range(self.instancia.turnos):
                    indices = [self.nombres2indices['H_' + str(i) + '_' + str(d) + '_' + str(t)]]
                    valores = [1]
                    for j in range(self.instancia.cantidad_ordenes):
                        indices = indices + [self.nombres2indices['W_' + str(i) + '_' + str(j) + '_' + str(d) + '_' + str(t)]]
                        valores = valores + [-1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['E'], rhs=[0], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1
    
    """====================Solucion===================="""
    def resolver_lp(self):
        
        # Definir los parametros del solver
        # prob.parameters....
        
        # Resolver el lp
        self.prob.solve()

    def mostrar_solucion(self):
        # Obtener informacion de la solucion a traves de 'solution'
        
        # Tomar el estado de la resolucion
        status = self.prob.solution.get_status_string(status_code = self.prob.solution.get_status())
        
        # Tomar el valor del funcional
        valor_obj = self.prob.solution.get_objective_value()
        
        print('Funcion objetivo: ',valor_obj,'(' + str(status) + ')')
        
        # Tomar los valores de las variables
        x  = self.prob.solution.get_values()
        # Mostrar las variables con valor positivo (mayor que una tolerancia)
        print('Variables con valor positivo:')
        for i in range(len(x)):
            if x[i] > 1e-5:
                print(self.prob.variables.get_names(i), x[i])


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
