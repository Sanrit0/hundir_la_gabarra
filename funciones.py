import variables as var
import numpy as np
import time
import os
import platform

def colocar_barco(matriz, tamano):
    valido = False
    while valido == False:
        origen = np.random.randint(10, size=(2,1))
        orientacion = np.random.choice(["N","S","E","O"])
        coord_x = origen[0][0]+1
        coord_y = origen[1][0]+1

        match orientacion:
            case "N":
                if coord_x - (tamano - 1) < 1 or (np.any(matriz[coord_x-(tamano - 1):coord_x+1,coord_y]) in [1,9]):
                    continue
                else:
                    matriz[(coord_x-(tamano - 1))-1:coord_x+2,coord_y-1:coord_y+2] = 9
                    matriz[coord_x-(tamano - 1):coord_x+1,coord_y] = 1
            case "S":
                if coord_x + (tamano - 1) > 10 or (np.any(matriz[coord_x:coord_x+tamano,coord_y]) in [1,9]):
                    continue
                else:
                    matriz[coord_x-1:coord_x+tamano+1,coord_y-1:coord_y+2] = 9
                    matriz[coord_x:coord_x+tamano,coord_y] = 1
            case "E":
                if coord_y + (tamano - 1) > 10 or (np.any(matriz[coord_x,coord_y:coord_y+tamano]) in [1,9]):
                    continue
                else:
                    matriz[coord_x-1:coord_x+2,coord_y-1:coord_y+tamano+1] = 9
                    matriz[coord_x,coord_y:coord_y+tamano] = 1
            case "O":
                if coord_y - (tamano - 1) < 1 or (np.any(matriz[coord_x,coord_y-(tamano - 1):coord_y+1]) in [1,9]):
                    continue
                else:
                    matriz[coord_x-1:coord_x+2,(coord_y-(tamano - 1))-1:coord_y+2] = 9
                    matriz[coord_x,coord_y-(tamano - 1):coord_y+1] = 1

        valido = True

def colocar_barcos():
    matriz = np.zeros((12,12))
    colocar_barco(matriz, 4)
    for i in range(2):
        colocar_barco(matriz,3)
    for i in range(3):
        colocar_barco(matriz,2)
    for i in range(4):
        colocar_barco(matriz,1)

    matriz[matriz == 9] = 0

    return matriz[1:-1,1:-1]

def comprobar_barco_hundido(matriz, x_coord, y_coord):
    matriz_margenes = np.zeros((12,12))
    matriz_margenes[1:-1,1:-1] = matriz
    x_aux = x_coord + 1
    y_aux = y_coord + 1
    matriz_margenes[y_aux,x_aux] = 8
    while True:
        if np.any(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 1):
            return False
        elif np.any(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2):
            if len(np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[0]) == 1:
                y_aux += (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[0][0]-1)
                x_aux += (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[1][0]-1)
                matriz_margenes[y_aux,x_aux] = 8
            else:
                return (comprobar_barco_hundido(matriz_margenes[1:-1,1:-1], \
                (x_aux + (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[1][0]-2)), \
                (y_aux + (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[0][0]-2)))) \
                and (comprobar_barco_hundido(matriz_margenes[1:-1,1:-1], \
                (x_aux + (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[1][1]-2)), \
                (y_aux + (np.where(matriz_margenes[y_aux-1:y_aux+2,x_aux-1:x_aux+2] == 2)[0][1]-2))))
            continue
        else:
            return True
        
def borrar_posiciones(lista, p1, p2):
    if p1[0] >= p2[0]:
        y1 = p2[0]
        y2 = p1[0]
    else:
        y1 = p1[0]
        y2 = p2[0]

    if p1[1] <= p2[1]:
        x1 = p1[1]
        x2 = p2[1]
    else:
        x1 = p2[1]
        x2 = p1[1]
    
    for i in range(int(y1-1), int(y2+2)):
        for j in range(int(x1-1), int(x2+2)):
            if (i,j) in lista:
                lista.remove((i,j))
    
    return lista

def comprobar_fin_juego(matriz):
    if np.any(matriz == 1):
        return False
    else:
        return True
    
def obtener_inputs():
    correcto = False
    while correcto == False:
        x_coord = input("introduce la coordenada X")
        if x_coord.isnumeric() == False or len(x_coord) != 1:
            print('Introduce un digito del 0 al 9')
        else:
            x_coord = int(x_coord)

            correcto = True
        time.sleep(0.5)

    correcto = False
    while correcto == False:

        y_coord = input("introduce la coordenada Y")
        if y_coord.isnumeric() == False or len(y_coord) != 1:
            print('Introduce un digito del 0 al 9')
        else:
            y_coord = int(y_coord)
            correcto = True
        time.sleep(0.5)

    return x_coord, y_coord

def disparar_eje_barco(x_coord,y_coord, lista1):
    if (y_coord+1,x_coord) in lista1:
        return (y_coord+1,x_coord)
    elif (y_coord-1,x_coord) in lista1:
        return (y_coord-1,x_coord)
    elif (y_coord,x_coord+1) in lista1:
        return (y_coord,x_coord+1)
    elif (y_coord,x_coord-1) in lista1:
        return (y_coord,x_coord-1)
    
def imprimir_matriz(matriz_print):
    matriz_imprimir = np.full((10, 10),'')
    matriz_imprimir[matriz_print == 3] = var.Agua_dibujo
    matriz_imprimir[matriz_print == 1] = var.barco_dibujo
    matriz_imprimir[matriz_print == 2] = var.tocado_dibujo
    matriz_imprimir[matriz_print == 0] = var.vacio_dibujo
    print(matriz_imprimir)

def borrar_print():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def jugar():
    matriz_jugador = colocar_barcos()
    matriz_ia = colocar_barcos()
    matriz_vista_jugador = np.zeros((10,10))

    lista_posiciones = []

    for i in range(10):
        for j in range(10):
            lista_posiciones.append((i,j))

    disparo = lista_posiciones[np.random.randint(len(lista_posiciones),size=1)[0]]

    origen_barco = None
    fin_juego = False
    tocado = 0
    cont = 0

    time.sleep(0.5)
    print(40 * '-')
    print('Tu tablero:')
    print(40 * '-')
    imprimir_matriz(matriz_jugador)
    print(40 * '-')
    print('Tablero de la máquina:')
    print(40 * '-')
    imprimir_matriz(matriz_vista_jugador)
    time.sleep(0.5)
    
    while not fin_juego:
        turno_jugador = True
        while turno_jugador == True:

            x,y = obtener_inputs()
            borrar_print()
            print((x,y))

            if int(matriz_vista_jugador[y,x]) in [2,3]:
                print('Ya has disparado aqui')
                time.sleep(0.5)
                continue

            match matriz_ia[y,x]:
                case 0:
                    print('Agua')
                    matriz_vista_jugador[y,x] = 3
                    turno_jugador = False
                case 1:
                    if comprobar_barco_hundido(matriz_ia,x,y) == True:
                        print('Hundido')
                    else:
                        print('Tocado')
                    matriz_vista_jugador[y,x] = 2
                    matriz_ia[y,x] = 2

            time.sleep(0.5)
            print(40 * '-')
            print('Tu tablero:')
            print(40 * '-')
            imprimir_matriz(matriz_jugador)
            print(40 * '-')
            print('Tablero de la máquina:')
            print(40 * '-')
            imprimir_matriz(matriz_vista_jugador)
            time.sleep(0.5)

            if comprobar_fin_juego(matriz_ia) == True:
                fin_juego = True
                print('Has ganado')
                time.sleep(5)
                break
        
        if fin_juego == True:
            break
        turno_ia = True

        while turno_ia == True:
            borrar_print()
            print((disparo[1],disparo[0]))
            if disparo in lista_posiciones:
                lista_posiciones.remove(disparo)
            match matriz_jugador[disparo]:
                case 0:
                    print('Agua')
                    turno_ia = False

                    if tocado == 0:
                        disparo = lista_posiciones[np.random.randint(len(lista_posiciones),size=1)[0]]
                    elif tocado == 1:
                        y = origen_barco[0]
                        x = origen_barco[1]
                        disparo = disparar_eje_barco(x,y,lista_posiciones)
                        
                    elif tocado == 2:
                        if disparo[0] == origen_barco[0]:
                            lista_posiciones = borrar_posiciones(lista_posiciones,origen_barco, \
                                            (disparo[0],int(disparo[1]+((origen_barco[1]-disparo[1])/abs(origen_barco[1]-disparo[1])))))
                        else:
                            lista_posiciones = borrar_posiciones(lista_posiciones,origen_barco, \
                                            (int(disparo[0]+((origen_barco[0]-disparo[0])/abs(origen_barco[0]-disparo[0]))),disparo[1]))
                        

                        disparo = (int(origen_barco[0] - ((disparo[0]-origen_barco[0])/abs((disparo[0]-origen_barco[0])+(disparo[1]-origen_barco[1])))), \
                                int(origen_barco[1] - ((disparo[1]-origen_barco[1])/abs((disparo[0]-origen_barco[0])+(disparo[1]-origen_barco[1])))))
            
                case 1:
                    matriz_jugador[disparo] = 2
                    if comprobar_barco_hundido(matriz_jugador,disparo[1],disparo[0]) == True:
                        print('Hundido')
                        if origen_barco is None:
                            lista_posiciones = borrar_posiciones(lista_posiciones,disparo,disparo)
                        else:
                            lista_posiciones = borrar_posiciones(lista_posiciones,origen_barco,disparo)
                        
                        if len(lista_posiciones) != 0:
                            disparo = lista_posiciones[np.random.randint(len(lista_posiciones),size=1)[0]]
                        tocado = 0
                        origen_barco = None
                    else:
                        print('Tocado')
                        y = disparo[0]
                        x = disparo[1]
                        

                        if tocado == 0:
                            tocado = 1
                            origen_barco = disparo
                            disparo = disparar_eje_barco(x,y,lista_posiciones)
                            
                        elif tocado in [1,2]:
                            tocado = 2
                            disparo = (int(disparo[0] - ((origen_barco[0]-disparo[0])/abs((origen_barco[0]-disparo[0])+(origen_barco[1]-disparo[1])))), \
                                    int(disparo[1] - ((origen_barco[1]-disparo[1])/abs((origen_barco[0]-disparo[0])+(origen_barco[1]-disparo[1])))))

                            if disparo not in lista_posiciones:
                                lista_posiciones = borrar_posiciones(lista_posiciones,origen_barco,disparo)

                                disparo = (int(origen_barco[0] - ((disparo[0]-origen_barco[0])/abs((disparo[0]-origen_barco[0])+(disparo[1]-origen_barco[1])))), \
                                        int(origen_barco[1] - ((disparo[1]-origen_barco[1])/abs((disparo[0]-origen_barco[0])+(disparo[1]-origen_barco[1])))))
                                
            time.sleep(0.5)
            print(40 * '-')
            print('Tu tablero:')
            print(40 * '-')
            imprimir_matriz(matriz_jugador)
            print(40 * '-')
            print('Tablero de la máquina:')
            print(40 * '-')
            imprimir_matriz(matriz_vista_jugador)
            time.sleep(0.5)

            if comprobar_fin_juego(matriz_jugador) == True:
                fin_juego = True
                print('Has perdido')
                time.sleep(5)
                break
