from modules.entities import *


def cargar_instancia(nombre_archivo="entrada_asignacion_cuadrillas.txt"):
    # Crea la instancia vacia
    instancia = InstanciaAsignacionCuadrillas()
    # Llena la instancia con los datos del archivo de entrada 
    instancia.leer_datos(nombre_archivo)
    return instancia


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
