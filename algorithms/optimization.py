import math
import random

from optimization.problem import SmartGridOptimizationProblem
from optimization.result import Configuration, OptimizationResult


def configuration_score(
    problem: SmartGridOptimizationProblem, configuration: Configuration
) -> float:
    """
    Combina cobertura, redundancia y exposición en un puntaje a maximizar.

    Tips:
    - Use problem.score_components(configuration); ya retorna cobertura,
      redundancia y exposición en ese orden.
    """
    cobertura, reundancia, exposicion = problem.score_components(configuration)
    return cobertura - reundancia - exposicion


def hill_climbing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    max_iterations: int = 500,
) -> OptimizationResult:
    """
    Ejecuta ascenso de colina con mejora estricta.

    Debe examinar todos los vecinos, seleccionar el de mayor puntaje y
    conservar el orden entregado por el problema para desempatar. La búsqueda
    termina cuando no existe una mejora estricta o se alcanza el límite.

    Tips:
    - problem.neighbors(current) retorna vecinos válidos en el orden que debe
      usarse para desempatar.
    - Cada llamada a configuration_score(...) cuenta como una evaluación.
    - Inicialice los historiales con la configuración inicial y agregue solo las
      mejoras aceptadas antes de retornar el OptimizationResult.
    """
    
    """
    En este problema hay que retornar un 'OptimizationResult'. Esta clase tiene
    esta estructura:
        best_configuration: Configuration
        best_score: float
        evaluations: int
        iterations: int
        history: list[Configuration] = field(default_factory=list)
        score_history: list[float] = field(default_factory=list)
        
    Hay que manetener todos los valores que pide esta clase.
    
    Estructura general de mi funcion:
    - crear current, un obj tipo OptimizationResult con una copia de 
      initial_config como best_config y el puntaje de initial_config como 
      best_score
    - un loop que cada iteración:
        - genera los vecinos de current
        - compara los vecinos
            - busca el mejor 
        - actualiza current (evals, iters)
        - si el mejor vecino es mejor que current:
            - actualiza current (best_config, best_score, hist, score_hist)
        - si no hay vecinos mejor que current:
            - return current
    - return current
    """
    #Creamos una copia de initial_config para no cambiarlo
    current_config=[]
    for i in initial_configuration:
        current_config.append(i)
    
    tuple_current_config = tuple(current_config)
    current_score = configuration_score(problem, tuple_current_config)
    current =  OptimizationResult(tuple_current_config ,
                                 current_score,
                                 1,0,[tuple_current_config],[current_score])
    
    #comenzamos el loop
    for i in range(max_iterations):
        #generemos los vecinos 
        list_neighbors = problem.neighbors(initial_configuration)
        
        #preparamos y comenzamos un ciclo para comparar los vecinos
        evals_per_cycle = 0
        for neighbor in list_neighbors:
            #si hay vecinos mejores que current, el mejor quedara en estas 
            #variables
            max_neighbor = None
            max_neighbor_score = 0
            
            #queremos evitar hacer mas evaluaciones de la cuenta 
            #entonces guardamos config_score en una variable
            temp_neighbor_score = configuration_score(problem, neighbor)
            #sumamos 1 por cada vez que hacemos config_eval
            evals_per_cycle =+ 1
            if temp_neighbor_score > current.best_score:
                max_neighbor_score = temp_neighbor_score
            
            
        #actualizemos current:
        #evals y iters
        current.evaluations += evals_per_cycle
        current.iterations += 1
        #Si hay un vecino mejor que current hay que actualizar:
        #best_config, best_score, hist, score_hist
        if max_neighbor != None:
            current.best_score = max_neighbor_score
            current.best_configuration = max_neighbor
            current.history.append(max_neighbor)
            current.score_history.append(max_neighbor_score)
        #si no, entonces estamos en el maximo local
        else:
            return current
    
    #si se cierra el loop es que llegamos a max_iterations
    #entonces, retornamos current
    return current
            


def cooling_schedule(initial_temperature: float, cooling_rate: float, iteration: int) -> float:
    """
    Retorna el programa geométrico T(t) = T0 * alpha**t.

    Esta función se invoca desde simulated_annealing en cada iteración.
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 2: implemente cooling_schedule")


def simulated_annealing(
    problem: SmartGridOptimizationProblem,
    initial_configuration: Configuration,
    initial_temperature: float = 20.0,
    cooling_rate: float = 0.97,
    max_iterations: int = 500,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta recocido simulado para un problema de maximización.

    Debe proponer un vecino aleatorio por iteración, aceptar siempre las
    mejoras y aplicar exp(delta / temperature) en los demás casos. El estado
    actual y el mejor estado encontrado deben conservarse por separado.

    Tips:
    - Seleccione el candidato con rng.choice(problem.neighbors(current)) y use
      exclusivamente rng para conservar la reproducibilidad.
    - Obtenga la temperatura con cooling_schedule(...) y calcule la aceptación
      con delta = puntaje_candidato - puntaje_actual y math.exp(...).
    - Mantenga separados el estado actual y el mejor encontrado; registre el
      estado actual después de cada intento, incluso si se rechaza.
    - Detenga la ejecución cuando la temperatura alcance minimum_temperature.
    """
    rng = rng or random.Random()
    minimum_temperature = 1e-9

    # TODO: Add your code here
    raise NotImplementedError("Punto 2: implemente simulated_annealing")


def one_point_crossover(
    parent1: Configuration, parent2: Configuration, rng: random.Random
) -> tuple[Configuration, Configuration]:
    """
    Realiza un cruce de un punto y retorna dos descendientes.

    La reparación de la cantidad de módulos se realiza posteriormente.

    Tips:
    - Seleccione con rng un corte interior, entre las posiciones 1 y len-1.
    - Cada descendiente combina el prefijo de un padre con el sufijo del otro.
    - Retorne tuplas y no repare aquí los descendientes.
    """
    if len(parent1) != len(parent2):
        raise ValueError("Los padres deben tener la misma longitud")
    if len(parent1) < 2:
        return parent1, parent2

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente one_point_crossover")


def swap_mutation(
    individual: Configuration, mutation_probability: float, rng: random.Random
) -> Configuration:
    """
    Aplica mutación por intercambio con la probabilidad indicada.

    Cuando ocurre una mutación, intercambia un bit activo y uno inactivo para
    conservar la cantidad de módulos instalados.

    Tips:
    - Use rng.random() para decidir si se aplica la mutación.
    - Identifique por separado los índices activos e inactivos y seleccione uno
      de cada grupo con rng.choice(...).
    - Si alguno de los dos grupos está vacío, no hay un intercambio posible.
    - Retorne una tupla nueva; no modifique el individuo recibido.
    """
    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente swap_mutation")


def genetic_algorithm(
    problem: SmartGridOptimizationProblem,
    population_size: int = 40,
    generations: int = 100,
    mutation_probability: float = 0.05,
    elite_size: int = 2,
    rng: random.Random | None = None,
) -> OptimizationResult:
    """
    Ejecuta un algoritmo genético generacional.

    Debe integrar la población inicial, la selección por torneo, el cruce, la
    reparación, la mutación y el elitismo entregados por el proyecto. Retorna
    el mejor individuo encontrado durante toda la ejecución.

    Tips:
    - Use problem.initial_population(...), problem.tournament_select(...) y
      problem.repair_configuration(...) para las operaciones ya entregadas.
    - Aplique one_point_crossover(...) antes de reparar y swap_mutation(...)
      después de la reparación.
    - Conserve los mejores individuos por elitismo y registre en los historiales
      el mejor global de cada generación.
    """
    rng = rng or random.Random()
    if population_size < 2:
        raise ValueError("La población debe tener al menos dos individuos")
    if generations < 0:
        raise ValueError("El número de generaciones no puede ser negativo")
    if not 0.0 <= mutation_probability <= 1.0:
        raise ValueError("La probabilidad de mutación debe estar entre 0 y 1")
    if not 0 <= elite_size <= population_size:
        raise ValueError("elite_size debe estar entre 0 y population_size")

    # TODO: Add your code here
    raise NotImplementedError("Punto 3: implemente genetic_algorithm")


