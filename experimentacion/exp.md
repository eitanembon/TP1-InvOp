prob.get_time() para medir tiempo

parameters.mip.strategy.nodeselect
0 DFS
1 best bound search
2 best estimate search
3 Alteranate BES

opcional probar 
parameters.mip.strategy.variableselect
0 auto
1 maximum int feasibility
2 pseudo costs
3 strong branching
4 pseudo reduced costs

probar tiempo con/sin presolve

parameters.mip.strategy.heuristiceffort
0 sin
1 default
< 1 poco
> 1 mucho

parameters.mip.cuts.cutpasses
-1 sin cortes
0 auto
n > 0 cantidad de cortes en la raiz

parameters.mip.cuts.nodecuts
-1 sin
0 auto
1,2,3 agresividad de generar cortes

parameters.mip.cuts.gomory
igual q anterior pero hasta 2

RESTRICCIONES

Considerar un archive a parte donde sacamos las restricciones opcionales y las agregamosa la function de costo

