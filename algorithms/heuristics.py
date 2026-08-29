from typing import Tuple
from algorithms import utils
from algorithms.problems import SystemRepairProblem
import math


def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def manhattanHeuristic(state, problem):
    """
    The Manhattan distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    # TODO: Add your code here
    position, gotKit, systems = state
    
    if not gotKit:                      #Consigió el kit?
        target = problem.kitPosition    # Si si, sigue; sino, no. Entonces ve para el kit
    elif len(systems)>0:                # Reparó todo?, NO, entonces calcula:
        closestSystem = systems[0]                                                                      #Toma el primer sistema
        closestDistance = abs(position[0] - closestSystem[0]) + abs(position[1] - closestSystem[1])     # Calcula su distancia manhattan
        
        for system in systems:                                                                          #Para cada sistema, 
            distance = abs(position[0] - system[0]) + abs(position[1] - system[1])        # Calcula su distancia manhattan
            
            if distance < closestDistance:                                                              #Busca la distancia mínima
                closestDistance = distance
                closestSystem = system
                
        target = closestSystem                                                                          # El objetivo es la distancia mínima
    else:                               # SI, Ya reparó todo
        target = problem.controlPosition    # Manda al robot a la meta final
    
    return abs(position[0] - target[0]) + abs(position[1] - target[1])      #Retorna la distancia manhattan entre la posición actual y el objetivo de posición.


def euclideanHeuristic(state, problem):
    """
    The Euclidean distance heuristic.

    Baseline rule for this workshop: estimate the direct distance to the next
    mandatory target:
    - K if the robot does not have the kit yet.
    - the nearest pending T if the robot has the kit and systems remain.
    - C if all systems have been repaired.
    """
    # TODO: Add your code here
    position, gotKit, systems = state
    if not gotKit:                      #Consigió el kit?
        target = problem.kitPosition    # Si si, sigue; sino, no. Entonces ve para el kit
    elif len(systems)>0:                # Reparó todo?, NO, entonces calcula:
        closestSystem = systems[0]                                                                                  #Toma el primer sistema
        closestDistance = math.sqrt((position[0] - closestSystem[0])**2 + (position[1] - closestSystem[1])**2)      # Calcula su distancia euclidiana
            
        for system in systems:                                                                                      #Para cada sistema, 
            distance = math.sqrt((position[0] - system[0])**2 + (position[1] - system[1])**2)         # Calcula su distancia euclidiana
                
            if distance < closestDistance:                                                              #Busca la distancia mínima
                closestDistance = distance
                closestSystem = system
                    
        target = closestSystem                                                                          # El objetivo es la distancia mínima
    else:                               # SI, Ya reparó todo
        target = problem.controlPosition    # Manda al robot a la meta final
        
    return math.sqrt((position[0] - target[0])**2 + (position[1] - target[1])**2)      #Retorna la distancia euclidiana entre la posición actual y el objetivo de posición.



def systemRepairHeuristic(
    state: Tuple[Tuple, bool, Tuple], problem: SystemRepairProblem
):
    """
    Your heuristic for the SystemRepairProblem.

    state: (position, hasKit, pendingSystems)
    problem: SystemRepairProblem instance

    This must be admissible and preferably consistent.

    Hints:
    - Use problem.heuristicInfo to cache expensive computations
    - Go with some simple heuristics first, then build up to more complex ones
    - Consider the kit, pending systems, and the final return to control center
    - Balance heuristic strength vs. computation time (do experiments!)
    """
    # TODO: Add your code here
    position, gotKit, systems = state
    
    if not gotKit:                      # Si no ha conseguido el kit, tiene que ir por el, por lo que retorna la distancia manhattan hasta K desde R
        kit = problem.kitPosition       #Toma ubicación de Kit
        return abs(position[0] - kit[0]) + abs(position[1] - kit[1])    #Calcula posición manhattan entre el kit y el robot
    
    if len(systems) > 0:                # Aún hay sistemas por reparar?
        nodes = [position]             # Crea una lista que servirá como MST. Guarda la posición actual del robot
        
        for system in systems:          # Para cada sistema que falta reparar
            nodes.append(system)       # Lo añade a la lista de nodos a visitar
            
        nodes.append(problem.controlPosition)       # Añade a la lista el centro de control a visitar (C)
        
        included = [False] * len(nodes)             # Crea una nueva lista para saber cuales nodos ya est+an en el MST
        included[0] = True                          # Marca la posición actual del robot
        
        totalCost = 0                               # Costo total del MST
        for i in range(len(nodes) - 1):             # Repite hasta conectar todos los nodos
            shortestDistance = float("inf")         # valores para hallar una distancia minima y un punto cercano
            closestPoint = -1
            
            for j in range(len(nodes)):             # recorre todos los puntos
                if included[j]:                     # Está incluido el nodo en el MST?
                    for k in range(len(nodes)):     # Recorre los nodos que podrían conectarse
                        if not included[k]:         # Este punto aún no está incluido?
                            distance = (abs(nodes[j][0] - nodes[k][0])+ abs(nodes[j][1] - nodes[k][1])) #Manhatan entre ambos puntos (J y K)
                            if distance < shortestDistance:     # Revisa si la distancia es la mínima y guarda la distancia y el punto
                                shortestDistance = distance
                                closestPoint = k
                                
            totalCost += shortestDistance       # Suma la distancia más corta al costo total
            included[closestPoint] = True       # Marca que ya se visitó el nodo en el MST
            
        return totalCost                        #Retorna el Costo total para visitar todos los T y C
    
    control = problem.controlPosition           # Si ya había agarrado el Kit, y ya había revisado todos los T, entonces solo falta C
    return abs(position[0] - control[0]) + abs(position[1] - control[1])    #Retorna Manhattan desde posición actual hasta C
