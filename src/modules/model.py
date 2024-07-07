import cplex
from src.modules.instancia import cargar_instancia
import time
class Modelo:
    def __init__(self, nombre_input):
        self.input_name = nombre_input
        self.prob = cplex.Cplex()
        self.instancia = cargar_instancia(nombre_input)
        self.coeficientes_funcion_objetivo = []
        self.nombres2indices = {}
        # Poner nombre a las variables
        self.nombres = []


    def armar_lp(self, nombre_archivo_salida = "asignacionCuadrillas"):

        print('Agregando Variables')
        # Agregar las variables
        self.agregar_variables_sin_refactor()

        
        # Agregar las variables al problema
        cantVar = len(self.nombres)
        self.prob.variables.add(obj = self.coeficientes_funcion_objetivo, lb = [0]*cantVar, ub = [1]*cantVar, types=['B']*cantVar, names=self.nombres)

        print('Agregando Restricciones')
        # Agregar las restricciones 
        self.agregar_restricciones()

        # Setear el sentido del self.problema
        self.prob.objective.set_sense(self.prob.objective.sense.maximize)

        # nombre del problema
        self.prob.set_problem_name('Asignacion de cuadrillas')

        print('Escribiendo archivo')
        # Escribir el lp a archivo
        self.prob.write(f'{nombre_archivo_salida}input{self.input_name[-6:]}''.lp')



    """====================Variables===================="""
    def agregar_variable(self,nombre, coeficiente:float, indices:list[int]):
        nombre_var = nombre + '_' + '_'.join(map(str,indices))
        # print(nombre_var)
        self.nombres.append(nombre_var)
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
        nro_ecuacion += 1
        
        return nro_ecuacion

        
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
        for i1 in range(self.instancia.cantidad_trabajadores-1):
            for i2 in range(i1+1,self.instancia.cantidad_trabajadores):
                indices = []
                valores = []
                for j in range(self.instancia.cantidad_ordenes):
                    indices += [self.nombres2indices[f'X_{i1}_{j}'], self.nombres2indices[f'X_{i2}_{j}']]
                    valores += [1, -1]
                fila = [indices,valores]
                self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[8], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                nro_restriccion += 1 

        for i1 in range(self.instancia.cantidad_trabajadores-1):
            for i2 in range(i1+1,self.instancia.cantidad_trabajadores):
                indices = []
                valores = []
                for j in range(self.instancia.cantidad_ordenes):
                    indices += [self.nombres2indices[f'X_{i1}_{j}'], self.nombres2indices[f'X_{i2}_{j}']]
                    valores += [1, -1]
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
            indices = []
            valores = []
            for j in range(self.instancia.cantidad_ordenes):
                indices += [self.nombres2indices[f'X_{i}_{j}']]
                valores += [1]

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
    def resolver_lp(self, log_stream = None):
        
        # Definir los parametros del solver
        # prob.parameters....
        
        # Resolver el lp
        # if log_stream is not None:
        #     with open(log_stream, 'w') as f:
        #         self.prob.set_log_stream(f)
        #         self.prob.set_results_stream(f)
        

        start_time = time.process_time()
        self.prob.solve()
        end_time = time.process_time()

        self.time = round(end_time - start_time, 3)
                

    def guardar_resultados(self, dict):
        dict[self.input_name] = {'f_obj': self.prob.solution.get_objective_value(), 'tiempo': self.time}
        
    def tiempo_ejecucion(self):
        return self.time
        
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

    def valor_objetivo(self):
        return self.prob.solution.get_objective_value()