# Punto 5: Poda alfa-beta y función de evaluación

## Poda alfa-beta

`AlphaBetaAgent.get_action` conserva la estructura de Minimax y sus casos
base. En nodos MAX actualiza `alpha` y poda cuando el valor es mayor o igual
que `beta`; en nodos MIN actualiza `beta` y poda cuando el valor es menor o
igual que `alpha`. La búsqueda conserva el orden de acciones y solo reemplaza
la mejor acción ante una mejora estricta, por lo que mantiene la primera en
caso de empate. `nodes_evaluated` se reinicia en cada decisión y cuenta cada
estado procesado, incluida la raíz y los estados terminales o de corte.

## Función de evaluación

Los estados terminales conservan las utilidades de la función base: +1000 en
victoria y -1000 en derrota. Para estados no terminales se usa:

```text
valor = puntaje
        - 35 * terminales_pendientes
        - 4 * distancia_a_terminal_mas_cercana
        + 5 * min(distancia_intruso_defensor, 20)
        + 0.5 * acciones_legales_del_defensor
        - 100 si el intruso está a distancia 0 o 1
```

El resultado no terminal se limita al intervalo `[-999, 999]` para que una
victoria o derrota siempre domine cualquier estimación heurística. Las
distancias infinitas se sustituyen por 50 antes del cálculo.

Los pesos expresan las prioridades del defensor:

- El puntaje conserva el progreso ya obtenido y la recompensa de terminales
  activadas.
- La penalización de 35 por terminal pendiente favorece completar la misión.
- La distancia al objetivo incentiva avanzar incluso cuando la activación
  queda fuera del horizonte de búsqueda.
- La separación del intruso recompensa posiciones seguras; su aporte se limita
  a distancia 20 para que no domine el objetivo principal.
- La penalización de 100 representa el riesgo inmediato de captura.
- La movilidad tiene peso 0.5 y sirve como criterio secundario para evitar
  posiciones con pocas alternativas.

## Comparación experimental

Se comparó cada algoritmo sobre el mismo estado inicial, profundidad, orden de
acciones y función de evaluación. Los nodos corresponden a la decisión inicial.

| Mapa | Profundidad | Acción Minimax | Nodos Minimax | Acción alfa-beta | Nodos alfa-beta | Reducción |
|---|---:|---|---:|---|---:|---:|
| dual_terminal | 2 | West | 17 | West | 16 | 5.9 % |
| dual_terminal | 4 | East | 245 | East | 94 | 61.6 % |
| medium_defense | 2 | East | 25 | East | 19 | 24.0 % |
| medium_defense | 4 | East | 457 | East | 185 | 59.5 % |

Alfa-beta seleccionó la misma acción que Minimax en todos los casos. La
reducción fue mayor a profundidad 4 porque el árbol contiene más ramas cuyo
valor puede descartarse mediante los límites `alpha` y `beta`. La cantidad
exacta de podas depende del orden de las acciones: encontrar primero opciones
buenas produce límites más restrictivos y permite cortar más ramas.

Como comprobación adicional, una partida con alfa-beta y profundidad 4 obtuvo
victoria en `dual_terminal`; en `medium_defense` alcanzó el límite de 60 rondas.
La poda modifica el costo de búsqueda, pero no el valor ni la decisión que
calcularía Minimax sobre el mismo árbol.

Ejemplo de ejecución:

```bash
python main.py -m adversarial -a AlphaBetaAgent -l dual_terminal -d 4 -q
```
