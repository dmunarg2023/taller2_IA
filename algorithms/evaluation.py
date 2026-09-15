import math

from world.game_state import GameState


def base_evaluation_function(state: GameState) -> float:
    """
    Retorna la evaluación base entregada para desarrollar el punto 4.

    Esta función no forma parte del código que debe modificar el estudiante y
    permite probar Minimax antes de desarrollar la heurística del punto 5.
    """
    if state.is_win():
        return 1000.0
    if state.is_lose():
        return -1000.0
    return float(state.get_score())


def evaluation_function(state: GameState) -> float:
    """
    Evalúa un estado desde la perspectiva del defensor MAX.

    Debe conservar las utilidades terminales de la evaluación base y diseñar
    una valoración no trivial para estados de corte. Minimax y alfa-beta usan
    esta misma función al comparar sus decisiones en el punto 5.

    Tips:
    - Los estados terminales ya se resuelven antes del bloque TODO; diseñe allí
      únicamente la valoración de estados no terminales.
    - Consulte state.defender_position, state.intruder_position,
      state.pending_terminals, state.get_score() y state.get_legal_actions(0).
    - state.layout.distance(start, goal) calcula y almacena en caché la distancia
      real por el mapa respetando los muros.
    - Maneje conjuntos vacíos y distancias infinitas, y mantenga todo estado no
      terminal estrictamente entre -1000 y +1000.
    """
    if state.is_win() or state.is_lose():
        return base_evaluation_function(state)

    defender = state.defender_position
    intruder = state.intruder_position

    terminal_distances = [
        state.layout.distance(defender, terminal)
        for terminal in state.pending_terminals
    ]
    reachable_terminals = [
        distance for distance in terminal_distances if math.isfinite(distance)
    ]
    nearest_terminal = min(reachable_terminals, default=50.0)

    intruder_distance = state.layout.distance(intruder, defender)
    safe_distance = intruder_distance if math.isfinite(intruder_distance) else 50.0

    value = float(state.get_score())
    value -= 35.0 * len(state.pending_terminals)
    value -= 4.0 * nearest_terminal
    value += 5.0 * min(safe_distance, 20.0)
    value += 0.5 * len(state.get_legal_actions(0))

    # A un paso, MIN puede capturar al defensor en su próximo movimiento.
    if safe_distance <= 1:
        value -= 100.0

    return max(-999.0, min(999.0, value))
