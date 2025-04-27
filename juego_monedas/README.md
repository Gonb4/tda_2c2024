# Trabajo Práctico 2: Programación Dinámica For The Win

El presente trabajo busca evaluar el desarrollo de un algoritmo de Programación Dinámica. 

## Introducción

Cuando Mateo nació, Sophia estaba muy contenta, finalmente tendría un hermano con quien jugar. Pasaron los años, y fueron cambiando los juegos hasta que cuando Mateo cumplió 4 años, el padre de ambos les explicó un juego:

Se dispone una fila de $$n$$ monedas, de diferentes valores. En cada turno, un jugador debe elegir alguna moneda. Pero no puede elegir cualquiera: sólo puede elegir o bien la primera de la fila, o bien la última. Al elegirla, la remueve de la fila, y le toca luego al otro jugador, quien debe elegir otra moneda siguiendo la misma regla. Siguen agarrando monedas hasta que no quede ninguna. Quien gane será quien tenga el mayor valor acumulado (por sumatoria).

## Consigna

Dada la secuencia de monedas $$m_1, m_2, \cdots, m_n$$, sabiendo que Sophia empieza el juego y que Mateo siempre elegirá la moneda más grande para sí entre la primera y la última moneda en sus respectivos turnos, definir qué monedas debe elegir Sophia para asegurarse obtener el **máximo valor acumulado posible**. Esto no necesariamente le asegurará a Sophia ganar, ya que puede ser que esto no sea obtenible, dado por cómo juega Mateo. Por ejemplo, para `[1, 10, 5]`, no importa lo que haga Sophia, Mateo ganará.

Proponer un algoritmo por programación dinámica que obtenga la solución óptima al problema planteado.
