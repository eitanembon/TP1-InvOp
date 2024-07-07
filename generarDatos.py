from src import *
import cplex
import glob
from pathlib import Path
import numpy as np

instances_path = "./inputs_v2/"

def corre_instancia_en_modelo(model:Modelo):
    # Armamos modelo
    print('Armando la lp')
    model.armar_lp('lps/')
    
    print('Resolviendo la lp')
    # Resolucion del modelo
    model.resolver_lp('logs')

    return model 

def correr_instancias_base(modificacion, nombre):
    print(nombre)
    tiempos = []
    objetivos = []
    contador = 0
    for path in glob.glob(instances_path + 'input_*.txt'):
        if contador > 9: 
            break;
        print(f"Instancia: {path}")
        model = Modelo(path)
        modificacion(model)
        start = model.prob.get_time()
        model = corre_instancia_en_modelo(model)
        end = model.prob.get_time()
        tiempos += [end - start]
        objetivos += [model.valor_objetivo()]
        contador += 1
    times = np.array(tiempos)
    objectives = np.array(objetivos)
    np.save("outputs/" + nombre, np.vstack((times, objectives)))

correr_instancias_default = correr_instancias_base(lambda x : 0, "default")

correr_instancias_sin_presolve = correr_instancias_base(lambda model : model.prob.parameters.preprocessing.presolve.set(0), "no_presolve")

correr_instancias_nodeselect_BBS = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.nodeselect.set(1), "best_bound")
correr_instancias_nodeselect_BES = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.nodeselect.set(2), "best_estimate")
correr_instancias_nodeselect_ABES = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.nodeselect.set(3), "alternate_best_estimate")

correr_instancias_maxint = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.variableselect.set(1), "max_int")
correr_instancias_pseudocosts = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.variableselect.set(2), "pseudo_costs")
correr_instancias_strong = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.variableselect.set(3), "strong_branch")
correr_instancias_pseudoreduced = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.variableselect.set(4), "pseudo_reduced")

correr_instancias_no_heuristics = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.heuristiceffort.set(0), "no_heuristics")
correr_instancias_some_heuristics = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.heuristiceffort.set(0.5), "some_heuristics")
correr_instancias_more_heuristics = correr_instancias_base(lambda model : model.prob.parameters.mip.strategy.heuristiceffort.set(2), "more_heuristics")

correr_instancias_sin_cortes_raiz = correr_instancias_base(lambda model : model.prob.parameters.mip.limits.cutpasses.set(-1), "no_root_cuts")
correr_instancias_muchos_cortes_raiz = correr_instancias_base(lambda model : model.prob.parameters.mip.limits.cutpasses.set(2000), "many_root_cuts")

correr_instancias_sin_cortes = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.nodecuts.set(-1), "no_cuts")
correr_instancias_pocos_cortes = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.nodecuts.set(1), "few_cuts")
correr_instancias_varios_cortes = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.nodecuts.set(2), "some_cuts")
correr_instancias_muchos_cortes = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.nodecuts.set(3), "many_cuts")

correr_instancias_sin_gomory = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.gomory.set(-1), "no_gomory")
correr_instancias_poco_gomory = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.gomory.set(1), "some_gomory")
correr_instancias_mucho_gomory = correr_instancias_base(lambda model : model.prob.parameters.mip.cuts.gomory.set(2), "many_gomory")

