from abc import ABC, abstractmethod

from algorithms.evaluation import evaluation_function
from world.game_state import GameState


class MultiAgentSearchAgent(ABC):
    """Clase base para los agentes de búsqueda adversaria."""

    def __init__(self, depth: int | str = 2) -> None:
        self.depth = int(depth)
        if self.depth < 1:
            raise ValueError("La profundidad debe ser al menos 1 ply")
        self.nodes_evaluated = 0

    @abstractmethod
    def get_action(self, state: GameState) -> str | None:
        raise NotImplementedError


class MinimaxAgent(MultiAgentSearchAgent):
    """Agente Minimax para el defensor MAX frente al intruso MIN."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción del defensor con mayor valor Minimax.

        El defensor es MAX (agente 0), el intruso es MIN (agente 1) y cada
        acción consume un ply. Debe respetar el orden de las acciones legales,
        usar evaluation_function en terminales y cortes, y contar cada estado
        procesado una vez en self.nodes_evaluated, incluida la raíz.

        Tips:
        - Use state.get_legal_actions(agent_index) y
          state.generate_successor(agent_index, action) para expandir el árbol.
        - Compruebe state.is_win(), state.is_lose() y el corte de profundidad;
          evalúe esos estados con evaluation_function(state).
        - El siguiente agente es (agent_index + 1) % state.get_num_agents().
          depth=1 incluye una acción de MAX y depth=2 una de MAX y una de MIN.
        - Reinicie las métricas y cuente una vez cada estado procesado, incluida
          la raíz. Retorne la acción de MAX y conserve la primera en los empates.
        """
        self.nodes_evaluated = 0

        def minimax(node: GameState, agent_index: int, plies_left: int):
            # Cada llamada procesa un estado, incluida la raíz.
            self.nodes_evaluated += 1
            if node.is_win() or node.is_lose() or plies_left == 0:
                return evaluation_function(node), None

            actions = node.get_legal_actions(agent_index)
            if not actions:
                return evaluation_function(node), None

            is_max = agent_index == 0
            best_value = float("-inf") if is_max else float("inf")
            best_action = actions[0]
            next_agent = (agent_index + 1) % node.get_num_agents()

            for action in actions:
                successor = node.generate_successor(agent_index, action)
                value, _ = minimax(successor, next_agent, plies_left - 1)
                # La comparación estricta conserva la primera acción empatada.
                if (is_max and value > best_value) or (
                    not is_max and value < best_value
                ):
                    best_value = value
                    best_action = action

            return best_value, best_action

        _, action = minimax(state, 0, self.depth)
        return action


class AlphaBetaAgent(MultiAgentSearchAgent):
    """Agente Minimax que evita explorar ramas mediante poda alfa-beta."""

    def get_action(self, state: GameState) -> str | None:
        """
        Retorna la acción de Minimax aplicando poda alfa-beta.

        Debe usar la misma profundidad, orden de acciones y función de
        evaluación que Minimax.

        Tips:
        - Conserve la misma estructura y casos base de MinimaxAgent.
        - Inicie alpha en -infinito y beta en +infinito, y páselos en las
          llamadas recursivas.
        - En MAX actualice alpha y corte si valor >= beta; en MIN actualice beta
          y corte si valor <= alpha.
        """
        # TODO: Add your code here
        raise NotImplementedError("Punto 5: implemente AlphaBetaAgent.get_action")
