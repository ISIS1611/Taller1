from algorithms.problems import SearchProblem
import algorithms.utils as utils
from world.game import Directions
from algorithms.heuristics import nullHeuristic


def tinyDiagnosticSearch(problem: SearchProblem):
    """
    Returns a hard-coded sequence of moves for the tinyDiagnostic layout.
    For any other station layout, the sequence of moves will be incorrect.
    """
    s = Directions.SOUTH
    e = Directions.EAST
    return [s, e, s, e, e, e, e, s, e, e, s, s, e, s, s, e, s, e, e, e, e, e, e, e]


def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.
    """
    frontier = utils.Stack()

    start_state = problem.getStartState()
    frontier.push((start_state, []))

    visited = {start_state}

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                frontier.push((successor, actions + [action]))

    return []


def breadthFirstSearch(problem: SearchProblem):
    """
    Search the shallowest nodes in the search tree first.
    """
    # TODO: Add your code here
    frontier = utils.Queue()

    start_state = problem.getStartState()
    frontier.push((start_state, []))

    visited = {start_state}

    while not frontier.isEmpty():
        state, actions = frontier.pop()

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                frontier.push((successor, actions + [action]))

    return []


def uniformCostSearch(problem: SearchProblem):
    """
    Search the node of least total cost first.
    """

    # TODO: Add your code here
    frontier = utils.PriorityQueue()

    start_state = problem.getStartState()
    frontier.push((start_state, [], 0), 0)

    best_cost = {
        start_state: 0
    }

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()

        if problem.isGoalState(state):
            return actions

        # Ignore outdated entries in the priority queue.
        if cost > best_cost[state]:
            continue

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost

            if successor not in best_cost or new_cost < best_cost[successor]:
                best_cost[successor] = new_cost

                new_actions = actions + [action]

                frontier.push(
                    (successor, new_actions, new_cost),
                    new_cost
                )

    return []



def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    # TODO: Add your code here
    
    start_state = problem.getStartState()                   # Toma el estado inicial del problema
    frontier = utils.PriorityQueue()                        # Crea una cola de prioridad vacia como frontera
    
    start_priority = heuristic(start_state, problem)        # Calcula g(n)+h(n) para determinar prioridad
    frontier.push((start_state, [], 0), start_priority)     # Guarda el estado, las acciones realizadas y el costo acumulado
                                                            #Estructura de la priority queue: (elemento:(estado[0], acciones[1], costo[2]), prioriodad[3])
    best_cost = {start_state: 0}                            # Estado inicial con costo 0 (servirá para avanzar más adelante)
    
    while not frontier.isEmpty():                           # Explora mientras existan nodos por explorar de la frontera actual
        state, actions, cost = frontier.pop()               # Saca de la frontera el nodo con menor prioridad (g(n)+h(n)) y sus estados, el de con menor prioridad
        
        if problem.isGoalState(state):                      # Revisa si llegó a la meta, y si si, devuelve el camino
            return actions
        
        if cost>best_cost[state]:                           # Revisa el costo del nodo que recien sacó de la frontera, si es viable, continua ejecutando, sino para y pasa a siguiente nodo
            continue
        
        for succesor, action, step_cost in problem.getSuccessors(state):        # Obtiene de los sucesores del nodo, su costo y acciones
            new_cost = cost + step_cost                                         # Calcula el costo acumulado (suma el actual con el del sucesor)
            if (succesor not in best_cost) or new_cost<best_cost[succesor]:     # Comprueba si es la primera vez que se visita (con el costo) o si hay ruta más barata
                best_cost[succesor] = new_cost                                  # Si paso el if, significa que tiene mejor costo en ese estado, por lo que guarda el costo nuevo
                new_actions = actions + [action]                                # Agrega la acción a la ruta tomada hasta el momento
                priority = new_cost + heuristic(succesor,problem)               # Calcula el g(n)+h(n)
                
                frontier.push((succesor, new_actions, new_cost), priority)      # Agrega el nodo a la frontera, guardando toda su info
    return []   # Si falló ps no retorna nadota


# Abbreviations (you can use them for the -f option in main.py)
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
