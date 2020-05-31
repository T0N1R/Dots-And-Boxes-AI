import socketio
import random
import time
import copy

sio = socketio.Client()
#conectarse al address
#address = 'http://3.12.129.126:5000'
#address = 'http://3.12.129.126:4000'

address = 'http://localhost:4000'

sio.connect(address)

userName = 'Amuro'

tournamentID = 142857

# funcion obtenida del foro de la clase para saber el puntaje
# se puede quitar, el get_puntaje_pred es casi lo mismo,
# le cambie cosas para que solo me de el numero total de puntos
def get_puntaje(board_get_puntaje):

    N = 6

    # Variable para identificar espacios vacios
    EMPTY = 99

    # Estas son variables que nos sirven para iterar sobre cada renglon del tablero y poder llevar las cuentas de cuando nos pasemos al siguiente renglon de revision
    # Es parte del algoritmo de revison, y deben ir seteadas a cero antes de hacer el ciclo for que viene a continuacion que es quien hace la revision de cuantos cuadros
    # cerrados hay en el tablero
    acumulador = 0
    contador = 0
    contadorPuntos = 0

    # Primero hacemos un recorrido sobre el largo de uno de los 2 arreglos (esto es debido a que ambos arreglos son del mismo tamaño, porque asi será en el torneo)
    for i in range(len(board_get_puntaje[0])):
        # La logica de esto si alguien tiene alguna duda se los puedo mandar en una demostración que hice a papel de la simetría de los tableros cuadrados en totito chino
        # Pero en general se revisa si la posicion siguiente de la que se tiene actualmente en la iteracion del arreglo se sale de la fila "física" que se está revisando
        # para hacer un "salto de fila" ya que los cuadrados nunca se pueden formar con lineas horizontales o verticales que esten en lados opuestos del tablero
        if ((i + 1) % N) != 0:
            # En caso no estemos haciendo un "salto de linea" se revisa si hay un cuadrado formado alrededor de la posicion sobre la que se esta iterando
            # Si alguien tiene duda de como funciona saber cuales son los otras 3 posiciones que formarian el cuadrado, avisenme para que les pase la demostración
            if board_get_puntaje[0][i] != EMPTY and board_get_puntaje[0][i + 1] != EMPTY and board_get_puntaje[1][contador + acumulador] != EMPTY and board_get_puntaje[1][contador + acumulador + 1] != EMPTY:
                # En caso de que las 4 posiciones revisadas esten llenas, eso significa que se ha realizado un punto y se acumula
                contadorPuntos = contadorPuntos + 1
            # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
            acumulador = acumulador + N
        # En caso de que se tenga que hacer un "salto de linea"
        else:
            # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
            contador = contador + 1
            acumulador = 0

    ## Aqui está como se cuentan los puntos de cada jugador cuando reciben el tablero
    player1 = 0
    player2 = 0
    FILLEDP11 = 1
    FILLEDP12 = 2
    FILLEDP21 = -1
    FILLEDP22 = -2


    for i in range(len(board_get_puntaje[0])):
        if board_get_puntaje[0][i] == FILLEDP12:
            player1 = player1 + 2
        elif board_get_puntaje[0][i] == FILLEDP11:
            player1 = player1 + 1
        elif board_get_puntaje[0][i] == FILLEDP22:
            player2 = player2 + 2
        elif board_get_puntaje[0][i] == FILLEDP21:
            player2 = player2 + 1

    for j in range(len(board_get_puntaje[1])):
        if board_get_puntaje[1][j] == FILLEDP12:
            player1 = player1 + 2
        elif board_get_puntaje[1][j] == FILLEDP11:
            player1 = player1 + 1
        elif board_get_puntaje[1][j] == FILLEDP22:
            player2 = player2 + 2
        elif board_get_puntaje[1][j] == FILLEDP21:
            player2 = player2 + 1

    ## Aqui regresamos los punteos de cada jugador
    return player1, player2

# regresa el numero total de puntos (sin importar de quien sea)
def get_puntaje_pred(board_pred):
    N = 6

    # Variable para identificar espacios vacios
    EMPTY = 99

    # Estas son variables que nos sirven para iterar sobre cada renglon del tablero y poder llevar las cuentas de cuando nos pasemos al siguiente renglon de revision
    # Es parte del algoritmo de revison, y deben ir seteadas a cero antes de hacer el ciclo for que viene a continuacion que es quien hace la revision de cuantos cuadros
    # cerrados hay en el tablero
    acumulador = 0
    contador = 0
    contadorPuntos = 0

    # Primero hacemos un recorrido sobre el largo de uno de los 2 arreglos (esto es debido a que ambos arreglos son del mismo tamaño, porque asi será en el torneo)
    for i in range(len(board_pred[0])):
        # La logica de esto si alguien tiene alguna duda se los puedo mandar en una demostración que hice a papel de la simetría de los tableros cuadrados en totito chino
        # Pero en general se revisa si la posicion siguiente de la que se tiene actualmente en la iteracion del arreglo se sale de la fila "física" que se está revisando
        # para hacer un "salto de fila" ya que los cuadrados nunca se pueden formar con lineas horizontales o verticales que esten en lados opuestos del tablero
        if ((i + 1) % N) != 0:
            # En caso no estemos haciendo un "salto de linea" se revisa si hay un cuadrado formado alrededor de la posicion sobre la que se esta iterando
            # Si alguien tiene duda de como funciona saber cuales son los otras 3 posiciones que formarian el cuadrado, avisenme para que les pase la demostración
            if board_pred[0][i] != EMPTY and board_pred[0][i + 1] != EMPTY and board_pred[1][contador + acumulador] != EMPTY and board_pred[1][contador + acumulador + 1] != EMPTY:
                # En caso de que las 4 posiciones revisadas esten llenas, eso significa que se ha realizado un punto y se acumula
                contadorPuntos = contadorPuntos + 1
            # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
            acumulador = acumulador + N
        # En caso de que se tenga que hacer un "salto de linea"
        else:
            # Variable que ayuda a determinar 2 posiciones para formar un cuadrado en la siguiente iteración
            contador = contador + 1
            acumulador = 0

    return contadorPuntos

# se ingresa el posible movimiento y se simulan los cambios que va a tener en el board 
# regresa el numero total de puntos que produciria hacer este movimiento
def simular_movimiento(test_board, movimiento):

    test_board[int(movimiento[0])][int(movimiento[1])] = 0

    puntos_actuales = get_puntaje_pred(test_board)

    return puntos_actuales

# En othello y totito el modo de juego es
# un turno el oponente, un turno yo sin importar si yo obtuve puntos o no.
# En totito chino, si yo gano puntos, juego de nuevo y lo mismo para el oponente
# por lo que es importante predecir el movimiento del enemigo cuando no estoy
# recibiendo puntos, si recibo puntos, tengo otro movimiento.
def mmax(posibles_movimientos, board, move_param, valor_param, miTurno, valor_estatico, arreglo_movimientos_param):

    # maxMove
    movement = move_param

    # es maxValue
    valor = valor_param

    arreglo_movimientos = arreglo_movimientos_param

    # mi turno inicial 
    if miTurno:

        if len(posibles_movimientos) <= 1:
            movement = move_param
            valor = valor_param

        for x in range(0, len(posibles_movimientos) - 1):

            randomMove1 = x

            # PREDICCION    
            test_board = copy.deepcopy(board)  
            movimiento_prediccion = posibles_movimientos[randomMove1]

            puntos_simulador = simular_movimiento(test_board, movimiento_prediccion)

            print("movimiento: ", movimiento_prediccion, " || ", "puntaje/heuristica: ", puntos_simulador)

            # se guarda en arreglo_movimientos el movimiento hipotetico
            # y el board resultante de este movimiento
            # arreglo_movimientos se va a utilizar en caso de que no haya un movimiento
            # en el que anote
            arreglo_movimientos.append([movimiento_prediccion, test_board])

            # si el valor de puntos es mayor, realizar este movimiento es mas favorable
            if puntos_simulador > valor:
                movement = movimiento_prediccion
                valor = puntos_simulador

        # si la variable valor es igual a valor_estatico, 
        # siginfica que ninguno de los movimientos va a generar un punto,
        # hay que preocuparse por el movimiento que puede hacer el enemigo
        # se va a utilizar recursion para predecir el movimiento el enemigo
        if valor == valor_estatico:
            try:
                movement, valor = mmax(posibles_movimientos, test_board, movement, valor, False, valor_estatico, arreglo_movimientos)

            except:
                return movement, valor

    else:

        # minMove
        minMove = [0,0]

        # minValue
        minValue = 1000000000000000

        print("*-*-*-*-*-*-*-*-*-*-*-*-*-")
        print("imprimir POSICION y heuristica")
        print("-------------------------------")
        for x in arreglo_movimientos_param:

            movimiento_que_hice = x[0]
            arreglo_resultante = x[1]     

            movimientos_enemigo = []
            heuristica = 0

            #se buscan todos los espacios que tienen el valor 99
            for o in range(0, len(arreglo_resultante[0])):
                if arreglo_resultante[0][o] == 99:
                    movimientos_enemigo.append([0,o])

            #se buscan todos los espacios que tienen el valor 99
            for p in range(0, len(arreglo_resultante[1])):
                if arreglo_resultante[1][p] == 99:
                    movimientos_enemigo.append([1,p])


            #print("movimientos enemigos: ", movimientos_enemigo)

            for y in range(len(movimientos_enemigo) -1 ):

                randomMove1 = y

                test_board = copy.deepcopy(arreglo_resultante)  
                movimiento_prediccion = posibles_movimientos[randomMove1]

                puntos_simulador = simular_movimiento(test_board, movimiento_prediccion)

                #print("puntos_simulador: ", puntos_simulador)

                heuristica = heuristica + puntos_simulador

            print("movimiento que hicimos: ", movimiento_que_hice, " || heuristica: ", heuristica)

            if heuristica <= minValue:
                minMove = movimiento_que_hice
                minValue = heuristica

        return minMove, minValue

    return movement, valor

@sio.on('connect')
def connect():
    # Se conecta el cliente
    print("Conectado: " + userName)

    # sign in con el id 
    sio.emit('signin', {
        'user_name' : userName,
        'tournament_id' : tournamentID,
        'user_role' : 'player'
    })

@sio.on('ready')
def ready(data):

    board = data['board']

    # se separan el arreglo con posiciones horizontales y verticales
    moves_horizontal = board[0]
    moves_vertical = board[1]

    #array donde se listaran los posibles movimiento
    #son las espacios horizontales y verticales cuyo valor es 99
    posibles_movimientos = []

    #se buscan todos los espacios que tienen el valor 99
    for x in range(0, len(moves_horizontal)):
        if moves_horizontal[x] == 99:
            posibles_movimientos.append([0,x])

    #se buscan todos los espacios que tienen el valor 99
    for x in range(0, len(moves_vertical)):
        if moves_vertical[x] == 99:
            posibles_movimientos.append([1,x])

    # id de este jugador
    print("______________________________________________________")
    print("------TURNO JUGADOR------")
    print("||||  ID DEL JUGADOR: ", data['player_turn_id'], "||||")
    print("______________________________________________________")
    
    # obtener puntaje actual del partido
    print("----  PUNTAJE  ----")
    puntaje_player1, puntaje_player2 = get_puntaje(board)
    print("Puntaje Jugador1: ", puntaje_player1)
    print("Puntaje Jugador2: ", puntaje_player2)
    print("______________________________________________________")

    move_param = posibles_movimientos[0]
    valor_param = get_puntaje_pred(board)
    arreglo_movimientos = []

    movement, valor = mmax(posibles_movimientos, board, move_param, valor_param, True, valor_param, arreglo_movimientos)

    print("______________________________________________________")
    print("SE ELGIGE LA POSICION: ", movement, " con el valor: ", valor)

    sio.emit('play', {
        'player_turn_id' : data['player_turn_id'],
        'tournament_id' : tournamentID,
        'game_id' : data['game_id'],
        'movement': movement
    })

@sio.on('finish')
def finish(data):
    print("Game", data['game_id'], "has finished")

    print("Ready to play again!")

    ## Start Again

    sio.emit('player_ready', {
        'tournament_id' : tournamentID,
        'game_id' : data['game_id'],
        'player_turn_id': data['player_turn_id']
    })
