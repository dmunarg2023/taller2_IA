# Punto 4: Defensa adversaria mediante Minimax

## Formulación del juego

| Componente | Formulación entregada |
|---|---|
| Estado inicial | `GameState.initial(layout)`: posiciones iniciales del defensor e intruso, todas las terminales críticas pendientes, puntaje 0 y turnos 0. |
| Jugador en turno | Defensor, índice 0, es MAX y juega primero; intruso, índice 1, es MIN. Se alternan después de cada acción. La búsqueda lleva el índice del jugador como parámetro. |
| Acciones | North, South, East, West y Stop, en ese orden; solo se permiten destinos transitables dentro del mapa, mediante `get_legal_actions`. |
| Función de resultado | `generate_successor(agent_index, action)` produce un nuevo estado. El defensor activa una terminal pendiente al entrar en ella, recibe 100 puntos y paga 1 punto por acción. El movimiento del intruso incrementa el contador de turnos. |
| Prueba terminal | Derrota si ambos ocupan la misma posición; victoria si no quedan terminales pendientes y no hay derrota. |
| Utilidad | +1000 para victoria y -1000 para derrota. En cortes no terminales, `evaluation_function` entregada retorna el puntaje acumulado. |

## Implementación

`MinimaxAgent.get_action` explora recursivamente todas las acciones legales.
MAX selecciona el mayor valor y MIN el menor. Las comparaciones estrictas
conservan la primera acción en los empates. Cada sucesor reduce la profundidad
restante en un ply; la raíz no consume profundidad. Los estados terminales,
los cortes y los estados sin acciones se evalúan con `evaluation_function`.
El contador se reinicia en cada decisión y aumenta una vez por llamada
recursiva, incluida la raíz.

## Experimentos

Se utilizó la evaluación base entregada y un límite de 60 rondas por partida.
Los nodos iniciales corresponden a la primera decisión del defensor; los
nodos totales suman todas sus decisiones durante la partida. Los nodos del
intruso se presentan por separado porque su política la ejecuta la infraestructura.

| Mapa | Profundidad (plies) | Acción inicial | Nodos iniciales | Resultado | Nodos totales MAX | Nodos totales MIN | Rondas |
|---|---:|---|---:|---|---:|---:|---:|
| single_terminal | 2 | South | 13 | Límite de rondas | 991 | 595 | 60 |
| single_terminal | 4 | South | 121 | Victoria | 1357 | 407 | 9 |
| tiny_defense | 2 | North | 13 | Límite de rondas | 1107 | 689 | 60 |
| tiny_defense | 4 | North | 143 | Límite de rondas | 15384 | 4146 | 60 |
| bottleneck | 2 | West | 9 | Límite de rondas | 983 | 805 | 60 |
| bottleneck | 4 | West | 89 | Límite de rondas | 10627 | 4292 | 60 |
| deceptive_distance | 2 | North | 17 | Límite de rondas | 1140 | 660 | 60 |
| deceptive_distance | 4 | North | 213 | Límite de rondas | 16168 | 3242 | 60 |

La profundidad 4 aumenta los nodos de la primera decisión en todos los mapas.
En el control `single_terminal` permite completar la activación en 9 rondas,
aunque conserva la misma acción inicial que profundidad 2. En los otros tres
mapas no basta para completar la partida antes del límite. Un límite de rondas
no equivale a derrota por intercepción.

Estos resultados son compatibles con la limitación de la evaluación base:
no recompensa acercarse a una terminal hasta activarla. Si la recompensa queda
fuera del horizonte, varios movimientos pueden empatar y el orden de acciones
determina la decisión. Aumentar la profundidad amplía la anticipación, pero no
garantiza ganar y aumenta el costo de búsqueda.

Para reproducir cada fila, sustituya el mapa y la profundidad:

```bash
python main.py -m adversarial -a MinimaxAgent -l single_terminal -d 4 --max-rounds 60 -q
```

También se verificó que profundidad 1 procesa exactamente la raíz y sus
sucesores inmediatos en los cuatro mapas, que decisiones repetidas reinician
el contador y que una raíz terminal retorna `None` con un único nodo procesado.
