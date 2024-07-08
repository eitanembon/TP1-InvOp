from src.modules.model import Modelo

RESTRICCION_ORDENES_REPETITIVAS = 9990
RESTRICCION_CONFLICTO_TRAJABAJADORES = 9991

class ModeloWithRestrictionsAdded(Modelo):
    def __init__(self, input, restricciones_a_agregar: list):
        self.restricciones_a_agregar = restricciones_a_agregar
        super().__init__(input)
    def agregar_restricciones(self):

        nro_ecuacion = super().agregar_restricciones()
        # Agregar restricciones de conflictos entre trabajadores
        if RESTRICCION_CONFLICTO_TRAJABAJADORES in self.restricciones_a_agregar:
            ###(Opcional) Si i1 y i2 tienen conflicos, entonces no pueden estar asignados en una orden de trabajo 
            nro_ecuacion += 1
            nro_restriccion = 0
            for conflicto in self.instancia.conflictos_trabajadores:
                for j in range(self.instancia.cantidad_ordenes):
                    indices = [self.nombres2indices[f'X_{conflicto[0]}_{j}'], self.nombres2indices[f'X_{conflicto[1]}_{j}']]
                    valores = [1, 1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1 
            nro_ecuacion += 1
        if RESTRICCION_ORDENES_REPETITIVAS in self.restricciones_a_agregar:
            # ### (Opcional) Si j y j'  son repetitivas entonces no puede haber un trabajador i que las realice a ambas
            nro_ecuacion += 1
            nro_restriccion = 0
            for repeticion in self.instancia.ordenes_repetitivas:
                for i in range(self.instancia.cantidad_trabajadores):
                    indices = [self.nombres2indices[f'X_{i}_{repeticion[0]}'], self.nombres2indices[f'X_{i}_{repeticion[1]}']]
                    valores = [1, 1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[1], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1
            nro_ecuacion += 1



class ModeloWithRestrictionsInObjectiveFunction(Modelo):
    def __init__(self, input, restricciones_a_agregar: list, alpha1, alpha2):
        self.restricciones_a_agregar = restricciones_a_agregar
        self.alpha1 = alpha1
        self.alpha2 = alpha2
        super().__init__(input)
    def agregar_variables_sin_refactor(self):
        super().agregar_variables_sin_refactor()
        print('Agregando variables de restricciones en la funcion objetivo')
        if RESTRICCION_CONFLICTO_TRAJABAJADORES in self.restricciones_a_agregar:
            # Agregar variables de conflictos entre trabajadores
            nombre = 'D_1'
            self.nombres.append(nombre)
            self.coeficientes_funcion_objetivo.append(self.alpha1)
            self.nombres2indices[nombre] = len(self.nombres) - 1
        if RESTRICCION_ORDENES_REPETITIVAS in self.restricciones_a_agregar:
            # Agregar variables de ordenes repetitivas
            nombre = 'D_2'
            self.nombres.append(nombre)
            self.coeficientes_funcion_objetivo.append(self.alpha2)
            self.nombres2indices[nombre] = len(self.nombres) - 1
        
        
    def agregar_restricciones(self):
        nro_ecuacion = super().agregar_restricciones()
        if RESTRICCION_CONFLICTO_TRAJABAJADORES in self.restricciones_a_agregar:
            ###(Opcional) Si i1 y i2 tienen conflicos, entonces no pueden estar asignados en una orden de trabajo 
            nro_ecuacion += 1
            nro_restriccion = 0
            for i1, i2 in self.instancia.conflictos_trabajadores:
                for j in range(self.instancia.cantidad_ordenes):
                    indices = [self.nombres2indices[f'X_{i1}_{j}'], self.nombres2indices[f'X_{i2}_{j}'], self.nombres2indices[f'D_1']]
                    valores = [1, 1, 1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[2], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1 
            nro_ecuacion += 1
        if RESTRICCION_ORDENES_REPETITIVAS in self.restricciones_a_agregar:
            # ### (Opcional) Si j y j'  son repetitivas entonces no puede haber un trabajador i que las realice a ambas
            nro_ecuacion += 1
            nro_restriccion = 0
            for j, j_ in self.instancia.ordenes_repetitivas:
                for i in range(self.instancia.cantidad_trabajadores):
                    indices = [self.nombres2indices[f'X_{i}_{j}'], self.nombres2indices[f'X_{i}_{j_}'], self.nombres2indices[f'D_2']]
                    valores = [1, 1, 1]
                    fila = [indices,valores]
                    self.prob.linear_constraints.add(lin_expr=[fila], senses=['L'], rhs=[2], names=[f'Ecuacion_{nro_ecuacion}_Restriccion_{nro_restriccion}'])
                    nro_restriccion += 1
            nro_ecuacion += 1
        
    def valor_objetivo(self):
        return super().valor_objetivo() - self.alpha1 * self.prob.solution.get_values('D_1') - self.alpha2 * self.prob.solution.get_values('D_2')
    
    def obtener_asignacion_variables_deseables(self):
        return { 'D_1': self.prob.solution.get_values('D_1'), 'D_2': self.prob.solution.get_values('D_2')}