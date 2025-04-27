import pulp
import sys

H = 'h'
V = 'v'

def batalla_naval(demanda_filas, demanda_columnas, barcos):
    
    # Parámetros del problema
    n, m = len(demanda_filas), len(demanda_columnas)  # Dimensiones del tablero
    k = len(barcos)  # Número de barcos

    # Modelo de programación lineal
    problema = pulp.LpProblem("Batalla_Naval", pulp.LpMaximize)

    # Variables
    x = pulp.LpVariable.dicts("x", (range(k), range(n), range(m), [H, V]), cat="Binary")
    u = pulp.LpVariable.dicts("u", (range(n), range(m)), cat="Binary")

    # Relación entre x y u
    for i in range(k):
        barco = barcos[i]
        for f in range(n):
            for c in range(m):
                if c + barco <= m:  # Horizontal
                    for t in range(barco):
                        problema += u[f][c + t] >= x[i][f][c][H]
                else:
                    problema += x[i][f][c][H] == 0 # (por casillero si el barco no entra horizontalmente empezando ahi -> x = 0)
                if f + barco <= n:  # Vertical
                    for t in range(barco):
                        problema += u[f + t][c] >= x[i][f][c][V]
                else:
                    problema += x[i][f][c][V] == 0 # (por casillero si el barco no entra verticalmente empezando ahi -> x = 0)

    # cada barco solo puede tener una variable x = 1 (solo puede empezar en 1 casillero en 1 direccion)
    for i in range(k):
        problema += pulp.lpSum(x[i][f][c][d] for f in range(n)
                                                for c in range(m)
                                                    for d in [H, V]) <= 1

    # si un barco empieza en un casillero ningun otro puede empezar en los casilleros que ocupa
    for f in range(n):
        for c in range(m):
            # problema += pulp.lpSum(x[i][f][c][d] for i in range(k) for d in [H, V]) <= 1 ## un solo barco (o ninguno) puede empezar en este casillero
            for i in range(k):
                barco = barcos[i]
                for t in range(barco):
                    if c + t < m: # aunque el barco no entre aprovecho para restringir (solo un barco (o ninguno) puede empezar en estos casilleros)
                        problema += x[i][f][c][H] + pulp.lpSum(x[ii][f][c + t][d] for ii in range(k)
                                                                                        for d in [H, V]
                                                                                            if ii != i) <= 1
                    if f + t < n:
                        problema += x[i][f][c][V] + pulp.lpSum(x[ii][f + t][c][d] for ii in range(k)
                                                                                        for d in [H, V]
                                                                                            if ii != i) <= 1

    # escudo de adyacentes
    for f in range(n):
        for c in range(m):
            for i in range(k):
                barco = barcos[i]
                if c + barco <= m:
                    for (ff, cc) in coords_ady_hor(n, m, f, c, barco):
                        problema += x[i][f][c][H] + u[ff][cc] <= 1
                if f + barco <= n:
                    for (ff, cc) in coords_ady_ver(n, m, f, c, barco):
                        problema += x[i][f][c][V] + u[ff][cc] <= 1

    # no se pueden superar las demandas
    for f in range(n):
        problema += pulp.lpSum(u[f][c] for c in range(m)) <= demanda_filas[f]
    for c in range(m):
        problema += pulp.lpSum(u[f][c] for f in range(n)) <= demanda_columnas[c]

    # controlar que casilleros ocupados == barcos colocados * largos
    problema += pulp.lpSum(u[f][c] for f in range(n)
                                        for c in range(m)) == \
                pulp.lpSum((x[i][f][c][d] * barcos[i]) for i in range(k)
                                                            for f in range(n)
                                                                for c in range(m)
                                                                    for d in [H, V])

    # funcion objetivo: maximizar colocaciones de barcos
    problema += pulp.lpSum(x[i][f][c][d] for i in range(k)
                                            for f in range(n)
                                                for c in range(m)
                                                    for d in [H, V])

    # Resolver el modelo
    problema.solve(pulp.PULP_CBC_CMD(msg=False))

    # Imprimir resultados
    demanda_cumplida_filas = [sum(u[f][c].varValue for c in range(m)) for f in range(n)]
    demanda_cumplida_columnas = [sum(u[f][c].varValue for f in range(n)) for c in range(m)]

    print("Demanda cumplida:", sum(demanda_cumplida_filas) + sum(demanda_cumplida_columnas))
    print("Demanda total:", sum(demanda_filas) + sum(demanda_columnas))
    for f in range(n):
        print([int(u[f][c].varValue) for c in range(m)], demanda_filas[f])
    print(" " + ", ".join(map(str, demanda_columnas)) + "\n")

    print("Barcos:", barcos)
    print("Colocaciones:", end= " ")
    print([x[i][f][c][d] for i in range(k)
                            for f in range(n)
                                for c in range(m)
                                    for d in [H, V] if x[i][f][c][d].varValue > 0])


def coords_ady_hor(n_fil, n_col, fil, col, l):
    coords = []
    
    for c in range(col, col + l):
        if fil > 0:
            coords.append((fil - 1, c))
        if fil < n_fil - 1:
            coords.append((fil + 1, c))
    
    if col > 0:
        coords.append((fil, col - 1))
        if fil > 0:
            coords.append((fil - 1, col - 1))
        if fil < n_fil - 1:
            coords.append((fil + 1, col - 1))

    if col + l < n_col:
        coords.append((fil, col + l))
        if fil > 0:
            coords.append((fil - 1, col + l))
        if fil < n_fil - 1:
            coords.append((fil + 1, col + l))
    
    return coords


def coords_ady_ver(n_fil, n_col, fil, col, l):
    coords = []
    
    for f in range(fil, fil + l):
        if col > 0:
            coords.append((f, col - 1))
        if col < n_col - 1:
            coords.append((f, col + 1))
    
    if fil > 0:
        coords.append((fil - 1, col))
        if col > 0:
            coords.append((fil - 1, col - 1))
        if col < n_col - 1:
            coords.append((fil - 1, col + 1))
    
    if fil + l < n_fil:
        coords.append((fil + l, col))
        if col > 0:
            coords.append((fil + l, col - 1))
        if col < n_col - 1:
            coords.append((fil + l, col + 1))
    
    return coords


if __name__ == '__main__':
    archivo = sys.argv[1]

    with open(archivo, 'r') as f:
        f.readline()
        f.readline()
        contenido = f.read().strip().split('\n\n')

        demandas_f = list(map(int, contenido[0].splitlines()))
        demandas_c = list(map(int, contenido[1].splitlines()))
        barcos = list(map(int, contenido[2].splitlines()))

        batalla_naval(demandas_f, demandas_c, barcos)
