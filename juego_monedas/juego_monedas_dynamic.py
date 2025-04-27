import sys

def juego_de_monedas(monedas):
    S = generar_soluciones(monedas)
    suma_sophia = S[len(monedas)-1][0]
    print("Sophia:", suma_sophia)
    print("Mateo:", sum(monedas) - suma_sophia)
    # for f in S:
    #     print(f)
    selecc_sophia = []
    ini = 0
    fin = len(monedas) - 1

    while fin >= ini+2: # reconstruccion solucion
        suma_con_izq = monedas[ini]
        if monedas[ini+1] > monedas[fin]:
            suma_con_izq += S[fin][ini+2]
            nuevo_fin_i, nuevo_ini_i = fin, ini+2
        else:
            suma_con_izq += S[fin-1][ini+1]
            nuevo_fin_i, nuevo_ini_i = fin-1, ini+1

        suma_con_der = monedas[fin]
        if monedas[ini] > monedas[fin-1]:
            suma_con_der += S[fin-1][ini+1]
            nuevo_fin_d, nuevo_ini_d = fin-1, ini+1
        else:
            suma_con_der += S[fin-2][ini]
            nuevo_fin_d, nuevo_ini_d = fin-2, ini
    
        if S[fin][ini] == suma_con_izq:
            selecc_sophia.append(monedas[ini])
            fin, ini = nuevo_fin_i, nuevo_ini_i
        else:
            selecc_sophia.append(monedas[fin]) 
            fin, ini = nuevo_fin_d, nuevo_ini_d
    
    if fin == ini or fin == ini+1:
        selecc_sophia.append(max(monedas[ini], monedas[fin]))

    print(selecc_sophia)


def generar_soluciones(monedas):
    S = [[0] * len(monedas) for _ in range(len(monedas))] # S[ult_mon][pri_mon]
    S[0][0] = monedas[0]

    for i in range(1, len(monedas)):
        S[i][i] = monedas[i]
        S[i][i-1] = max(monedas[i], monedas[i-1])

    for fin in range(2, len(monedas)):
        for ini in range(fin-2, -1, -1):
            suma_con_izq = monedas[ini]
            if monedas[ini+1] > monedas[fin]:
                suma_con_izq += S[fin][ini+2]
            else:
                suma_con_izq += S[fin-1][ini+1]

            suma_con_der = monedas[fin]
            if monedas[ini] > monedas[fin-1]:
                suma_con_der += S[fin-1][ini+1]
            else:
                suma_con_der += S[fin-2][ini]

            S[fin][ini] = max(suma_con_izq, suma_con_der)

    return S



if __name__ == "__main__":
    archivo = sys.argv[1]

    with open(archivo, 'r') as ejemplos:
       ejemplos.readline()
       contenido = ejemplos.read().strip()
       monedas = list(map(int, contenido.split(';')))

    juego_de_monedas(monedas)