### Contamos con:

* [X] $T$ trabajadores
* [X] $O$ órdenes de trabajo a realizar
* [X] cada $o_i$ requiere de una cantidad prefijada de trabajadores, $t_i$, y realizarla da un
  beneficio $b_i$.
* [X] 6 dias de semana a planificar
* [X] Cada día tiene 5 turnos de 2 horas.
* [X] Cada órde de trabajo se puede realizar utilizando un solo turno
* [X] Un mismo trabajador no puede realizar más de una orden en un mismo turno.

#### Objetivo:

Maximizar la ganancia total asignando los trabajoderes a los ordenes y los ordenes a los turnos

La ganancia de la asignación se define como la suma de los beneficios de las órdenes satisfechas menos la remuneración otorgada a cada trabajador.

### Restricciones:

* [X] No toda orden de trabajo tiene que ser resuelta.
* [X] Ningún trabajador puede trabajar los 6 dı́as de la planificación.
* [X] Ningún trabajador puede trabajar los 5 turnos de un dı́a.
* [X] Hay pares de órdenes de trabajo que no pueden ser satisfechas en turnos consecutivos
  de un trabajador (si bien en este problema no nos preocupamos por el ruteo sino sólo
  por la asignación, hay órdenes tan lejanas geográficamente que no se podrán satisfacer
  consecutivamente por el mismo trabajador).
* [X] Una orden de trabajo $o_i$ debe tener asignados sus $t_i$ trabajadores en un mismo turno
  para poder ser resuelta.
* [X] Existen algunos pares de órdenes de trabajo correlativas. Un par ordenado de órdenes
  correlativas A y B, nos indica que si se satisface A, entonces debe satisfacerse B ese
  mismo dı́a en el turno consecutivo.
* [X] Los trabajadores son remunerados según la cantidad de órdenes asignadas, por lo que
  la diferencia entre el trabajador con más órdenes asignadas y el trabajador con menos
  órdenes no puede ser mayor a 8. Para esto se consideran todos los trabajadores, aún los
  que no tienen ninguna tarea asignada esa semana.

### Restricciones (Deseables)

* [X] Hay conflictos entre algunos trabajadores que hacen que prefieran no ser asignados a una misma orden de trabajo
* [ ] Hay pares de órdenes de trabajo que son repetitivas, por lo que será bueno que un mismo trabajador no sea asignado a ambas.

### Remuneración de trabajoders

Los trabajadores son remunerados según el siguiente esquema:

* Por cada una de las primeras 5 órdenes que realizan obtienen una remuneración de $1000.
* Por cada una de las órdenes entre la 6 y 10, obtienen una remuneraión de $ 1200.
* Por cada una de las órdenes entre la 11 y 15, obtienen una remuneración de $ 1400.
* A partir de la orden 15, obtienen una remuneración de $ 1500 por cada una.

### Modelo:

* [X]

$$
W_{ijdt}= \begin{cases}
	1 & \text{``El trabajador $i$ hace la tarea $j$ en el dia $d$ en el turno $t$"} \\
	0 & \text{cc}
\end{cases}
$$

* [X]

$$
H_{idt} = \begin{cases}
    1 & \text{si ``El trabajador $i$ realiza una órden el día $d$ en el turno $t$"}  \\ 
    0 & \text{cc}
\end{cases}
$$

* [X]

$$
L_{id} = \begin{cases}
    1 & \text{si ``El trabajador $i$ realiza alguna órden el día $d$"}  \\ 
    0 & \text{cc}
\end{cases}
$$

* [X]

$$
X_{ij} = \begin{cases}
    1 & \text{si ``El trabajador $i$ realiza la orden $j$ "}  \\ 
    0 & \text{cc}
\end{cases}
$$

* [X]

$$
Y_{ij} = \begin{cases} 
1 & \text{si ``El trabajador $i$ realiza su $j$-ésima tarea"} \\
0 & \text{cc}
\end{cases}
$$

* [X]

$$
Z_{jdt} = \begin{cases} 
1 & \text{si ``La órden $j$ se realiza en el día $d$ en el turno $t$"} \\
0 & \text{cc}
\end{cases}
$$

* [X]

$$
K_{j} = \begin{cases} 
1 & \text{si ``La órden $j$ es realizada"} \\
0 & \text{cc}
\end{cases}
$$

Maximizar:

$$
\sum_{j\in O}{b_jK_j} - \sum_{i\in T}\sum_{j\in [1,5]}{1000Y_{ij}} - \sum_{i\in T}\sum_{j\in [6,10]}{1200Y_{ij}} - \sum_{i\in T}\sum_{j\in [11,15]}{1400Y_{ij}} - \sum_{i\in T}\sum_{j\in [16,20]}{1500Y_{ij}}
$$

Restricciones:

* $H_{idt} \iff \exists! j \in O (W_{ijdt})$

  $$
  H_{idt} = \sum_{j\in O}{W_{ijdt}}
  $$
* $X_{ij}\iff \exists! d \in D, t\in [1,5] (W_{ijdt})$

  $$
  X_{ij} = \sum_{d\in D}\sum_{t\in [1,5]}{W_{ijdt}}
  $$
* $Z_{jdt} \land X_{ij}\iff W_{ijdt}$

  $$
  2W_{ijdt} \leq Z_{jdt} + X_{ij} \leq 2W_{ijdt} + M(2 - Z_{jdt} - X_{ij})
  $$

  $$


  $$
* Cada órden de trabajo se puede realizar utilizando un solo turno

$$
\sum_{d\in D}\sum_{t\in [1,5]} {Z_{jdt}} = K_j. \qquad \forall {j \in O}
$$

La cantidad de trabajadores de  la tarea $j$ es $t_i$ si se realiza

$$
\sum_{i\in T}{X_{ij}} = t_jK_j, \qquad \forall j\in O
$$


Un trabajador no puede trabajar en dos ordenes diferentes en un mismo turno

$$
X_{ij_1}+X_{ij_2} \leq 1 + M(1-Z_{j_1dt}) + M(1-Z_{j_2dt}), \qquad \forall i\in T, j_1,j_2\in O, d\in D, t\in [1,5]
$$


Un trabajador no puede trabajar los 6 dias de la planificación

$$
\sum_{d\in D}{L_{id}} \leq 5, \qquad \forall i \in T
$$


Un trabajador no puede trabajar los 5 turnos de un dia

$$
\sum_{t\in [1,5]}{H_{idt}} \leq 4, \qquad \forall i\in T, \forall d \in D
$$


Equivalencia entre Lid y Hidt (Lid$\iff$Existe un t tal que  Hidt )

$$
L_{id} \leq \sum_{t\in [1,5]}{H_{idt}} \leq 5L_{id}, \qquad  \forall i\in T, d\in D
$$


La cant de trabajos j que realiza i es igual

$$
\sum_{j\in O} {X_{ij}} = \sum_{k\in [1,20]}{Y_{ik}}, \qquad \forall i\in T
$$


$Y_{i(k+1)} \implies Y_{ik}$ para todo $k = 1\dots 19$

$$
Y_{i(k+1)} \leq Y_{ik}, \qquad \forall i \in T, k = 1 \dots 19
$$


Si la tarea $j$ debe realizarse antes que la tarea $j'$ entonces $Z_{jdt} \iff Z_{j'd(t+1)}$

$$
Z_{jdt} = Z_{j'd(t+1)}, \qquad \forall (j, j')\in O_{correlativas}, \forall d\in D, t = 1\dots 4
$$

* Siguiendo lo anterior, la tarea j no puede realizarse en el último turno y  la tarea j' no puede realizarse en el primer turno

  $$
  Z_{j'd1} = 0, \qquad \forall (j, j') \in O_{correlativas}, \forall d\in D
  $$

  $$
  Z_{jd5} = 0, \qquad \forall (j, j') \in O_{correlativas}, \forall d\in D
  $$

Si la tarea $j$ y $j'$ son conflictivas y se realizan en turnos consecutivos, entonces ningun trabajador puede tener asignado ambas.

$$
Z_{jdt} \land Z_{j'd(t+1)}  \implies \forall i \in T ¬(X_{ij} \land X_{ij'}), \qquad \forall (j,j')\in O_{conflictivas}, \forall d\in D, t = 1\dots 4
$$

$$
Z_{j'dt} \land Z_{jd(t+1)} \implies \forall i \in T ¬(X_{ij} \land X_{ij'}), \qquad \forall (j,j')\in O_{conflictivas}, \forall d\in D, t = 1\dots 4
$$

$$
Z_{jdt} + Z_{j'd(t+1)} \leq (1-X_{ij}) + (1-X_{ij'}) + M(2 - Z_{jdt} - Z_{j'd(t+1)}), \qquad \forall i\in T, (j,j')\in O_{conflictivas}, \forall d\in D, t = 1\dots 4
$$

$$
Z_{j'dt} + Z_{jd(t+1)} \leq (1-X_{ij}) + (1-X_{ij'}) + M(2 - Z_{j'dt} - Z_{jd(t+1)}), \qquad \forall i\in T, (j,j')\in O_{conflictivas}, \forall d\in D, t = 1\dots 4
$$

Para todo par i, i' trabajadores la diferencia de la cantidad de trabajos que realizan no puede ser mayor a 8

$$
-8 \leq \sum_{j\in O} X_{ij} - X_{i'j} \leq 8, \qquad \forall i<i' \in T
$$

* (Opcional) Si i y i' tienen conflicos, entonces no pueden estar asignados en una orden de trabajo

  $$
  ¬ (X_{ij} \land X_{i'j})
  $$

  $$
  X_{ij} + X_{i'j} \leq 1, \qquad \forall (i,i') \in T_{conflictivos}, j\in O
  $$
* (Opcional) Si j y j'  son repetitivas entonces no puede haber un trabajador i que las realice a ambas

  $$
  X_{ij} + X_{ij'} \leq 1, \qquad \forall (j,j') \in O_{repetitivos}, i\in T
  $$
