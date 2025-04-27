# Trabajo Práctico 3: Diversión NP-Completa

El presente trabajo busca evaluar el desarrollo de un algoritmo de Backtracking y (opcionalmente) un modelo de programación lineal para resolver un Problema NP-Completo.

## Introducción

La Batalla Naval Individual es un juego inventado en Argentina por Jaime Poniachik (uno de los fundadores de _Ediciones de Mente_) en 1982. 

En dicho juego, tenemos un tablero de $$n \times m$$ casilleros, y $$k$$ barcos. Cada barco $$i$$ tiene $$b_i$$ de largo. Es decir, requiere de $$b_i$$ casilleros para ser ubicado. Todos los barcos tienen 1 casillero de ancho. El tablero a su vez tiene un requisito de consumo tanto en sus filas como en sus columnas. Si en una fila indica un 3, significa que deben haber 3 casilleros de dicha fila siendo ocupados. Ni más, ni menos. No podemos poner dos barcos de forma adyacente (es decir, no pueden estar contiguos ni por fila, ni por columna, ni en diagonal directamente). Debemos ubicar todos los barcos de tal manera que se cumplan todos los requisitos. A continuación mostramos un ejemplo de un juego resuelto:


<!-- ![battleships](battleships.png) -->
<img src="battleships.png" alt="battleships" width="200" height="200"/>


## Consigna

Escribir un algoritmo que, por backtracking, obtenga la solución óptima al problema (valga la redundancia) en la versión de optimización: Dado un tablero de $$n \times m$$ casilleros, y una lista de $$k$$ barcos (donde el barco $$i$$ tiene $$b_i$$ de largo) una lista de las demandas de las $$n$$ filas y una lista de las $$m$$ demandas de las columnas, dar la asignación de posiciones de los barcos de tal forma que se reduzca al mínimo la cantidad de demanda incumplida. Pueden no utilizarse todos los barcos. Si simplemente no se cumple que una columna que debería tene 3 casilleros ocupados tiene 1, entonces contará como 2 de demanda incumplida. Por el contrario, no está permitido exceder la cantidad demandada.

(Opcional) Escribir un modelo de programación lineal que resuelva el problema de forma óptima.
