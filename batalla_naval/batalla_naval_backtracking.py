import sys
# import time

LIBRE = 0
OCUPADO = 1
RESTRINGIDO = 2

def batalla_naval_bt(dem_fil, dem_col, barcos):
    barcos.sort(reverse=True)
    sol_opt = [[LIBRE] * len(dem_col) for _ in range(len(dem_fil))]
    sol_par = [[LIBRE] * len(dem_col) for _ in range(len(dem_fil))]

    solucion_optima, dem_cumpl_optima = backtracking(barcos, 0, list(dem_fil), list(dem_col), sol_opt, sol_par, 0, 0, sum(barcos)*2)

    for f in range(len(solucion_optima)):
        print([x if x == 1 else 0 for x in solucion_optima[f]], dem_fil[f])
    print(" " + ", ".join(map(str, dem_col)) + "\n")

    print("Demanda cumplida:", dem_cumpl_optima)
    print("Demanda total:", sum(dem_fil) + sum(dem_col))



def backtracking(barcos, i, dem_fil, dem_col, sol_opt, sol_par, d_cmp_opt, d_cmp_par, d_res):
    if i == len(barcos):
        if d_cmp_par > d_cmp_opt:
            return [f[:] for f in sol_par], d_cmp_par
        else:
            return sol_opt, d_cmp_opt
    
    if d_cmp_par + d_res <= d_cmp_opt:
        return sol_opt, d_cmp_opt
    
    for f in range(len(dem_fil)): # horizontal
        for c in range(len(dem_col) - barcos[i] + 1):
            if colocar_barco_hor(sol_par, f, c, barcos[i], dem_fil, dem_col):
                sol_opt, d_cmp_opt = backtracking(barcos, i+1, dem_fil, dem_col, sol_opt, sol_par, d_cmp_opt, d_cmp_par + barcos[i]*2, d_res - barcos[i]*2)
                quitar_barco_hor(sol_par, f, c, barcos[i], dem_fil, dem_col)

    for f in range(len(dem_fil) - barcos[i] + 1): # vertical
        for c in range(len(dem_col)):
            if colocar_barco_ver(sol_par, f, c, barcos[i], dem_fil, dem_col):
                sol_opt, d_cmp_opt = backtracking(barcos, i+1, dem_fil, dem_col, sol_opt, sol_par, d_cmp_opt, d_cmp_par + barcos[i]*2, d_res - barcos[i]*2)
                quitar_barco_ver(sol_par, f, c, barcos[i], dem_fil, dem_col)

    sol_opt, d_cmp_opt = backtracking(barcos, i+1, dem_fil, dem_col, sol_opt, sol_par, d_cmp_opt, d_cmp_par, d_res - barcos[i]*2)

    return sol_opt, d_cmp_opt


def colocar_barco_hor(tablero, fil, col, largo, dem_fil, dem_col):
    if dem_fil[fil] < largo:
        return False
    
    for c in range(col, col + largo):
        if dem_col[c] < 1:
            return False
        if tablero[fil][c] == OCUPADO or tablero[fil][c] == RESTRINGIDO:
            return False

    dem_fil[fil] -= largo        
    for c in range(col, col + largo):
        tablero[fil][c] = OCUPADO
        dem_col[c] -= 1

    for f, c in coords_ady_hor(len(dem_fil), len(dem_col), fil, col, largo):
        tablero[f][c] = RESTRINGIDO

    return True


def quitar_barco_hor(tablero, fil, col, largo, dem_fil, dem_col):
    dem_fil[fil] += largo
    for c in range(col, col + largo):
        tablero[fil][c] = LIBRE
        dem_col[c] += 1

    for f, c in coords_ady_hor(len(dem_fil), len(dem_col), fil, col, largo):
        tablero[f][c] = LIBRE


def colocar_barco_ver(tablero, fil, col, largo, dem_fil, dem_col):
    if dem_col[col] < largo:
        return False
    
    for f in range(fil, fil + largo):
        if dem_fil[f] < 1:
            return False
        if tablero[f][col] == OCUPADO or tablero[f][col] == RESTRINGIDO:
            return False

    dem_col[col] -= largo        
    for f in range(fil, fil + largo):
        tablero[f][col] = OCUPADO
        dem_fil[f] -= 1

    for f, c in coords_ady_ver(len(dem_fil), len(dem_col), fil, col, largo):
        tablero[f][c] = RESTRINGIDO

    return True


def quitar_barco_ver(tablero, fil, col, largo, dem_fil, dem_col):
    dem_col[col] += largo
    for f in range(fil, fil + largo):
        tablero[f][col] = LIBRE
        dem_fil[f] += 1

    for f, c in coords_ady_ver(len(dem_fil), len(dem_col), fil, col, largo):
        tablero[f][c] = LIBRE


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
        # t_inicio = time.time()
        batalla_naval_bt(demandas_f, demandas_c, barcos)
        # t_final = time.time()
        # print("tiempo:", t_final-t_inicio)