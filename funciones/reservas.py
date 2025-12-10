from datetime import datetime, timedelta

#Tiempo simulado que empieza en el momento actual
tiempo_actual = datetime.now()

#Lista de diccionarios para guardar las reservas activas y liberar al terminar
reservas_activas = []

# Lista de salas
salas = [
    {'nombre': 'Sala 1: Consolas', 'descripcion': 'Esta sala cuenta con dos PlayStation 5 y está condicionada para que tengas una excelente partida.', 'max_personas': 8, 'max_sillas': 8, 'max_sofas': 2, 'max_mandos': 4},
    {'nombre': 'Sala 2: Consolas', 'descripcion': 'Esta sala cuenta con dos PlayStation 5 y está condicionada para que tengas una excelente partida.', 'max_personas': 8, 'max_sillas': 8, 'max_sofas': 2, 'max_mandos': 4},
    {'nombre': 'Sala 3: PCs', 'descripcion': 'Esta sala cuenta con tres computadoras listas para su disfrute. Tienen servicio a internet ilimitado y una gran variedad de videojuegos',  'max_personas': 6, 'max_sillas': 6, 'max_audifonos': 6},
    {'nombre': 'Sala 4: Realidad Virtual', 'descripcion': 'Esta sala cuenta con cuatro equipos de realidad virtual de gran inmersión para que la pases en grande.\nEstos son:\n- Dos RV Cooperativo de exploración y combate\n- RV de carreras\n- RV simulador de atracciones', 'max_personas': 6, 'max_mandos_rv': 6, 'max_visores_rv': 5, 'max_caminadora_rv': 3}
]

juegos_consola = [
    'Hollow Knight', 'Stardew Valley', 'Clair Obscur: Expedition 33', 'Call of Duty',
    'Undertale', 'It Takes Two', 'Mortal Kombat 11', 'Overcooked', 'The Quarry', 'The Last of Us'
]

juegos_reservados = set()  #Para evitar duplicados

def mostrar_salas_disponibles():
    print('\n     Salas Disponibles\n')
    for i, sala in enumerate(salas, 1):
        estado = 'Reservada' if not sala['disponible'] else ''
        
        #Quita el prefijo sala x para que no se repita al imprimirlo
        nombre_limpio = sala['nombre'].replace(f'Sala {i}:', '')
        print(f'Sala {i}: {nombre_limpio} {estado}')
    print('Atras')

def pedir_numero(mensaje, minimo=1, maximo=None):
    while True:
        valor = input(mensaje).strip()
        if valor.lower() in ['atras']:
            return 'atras'
        
        #Es para prohibir ceros a la izquierda (003,01, etc)
        if valor.startswith('0') and len(valor) > 1:
            print('\nNo se permiten ceros al inicio. Prueba de nuevo')
            continue
        
        try:
            num = int(valor)
            if num < minimo:
                print(f'\nMinimo {minimo}')
                continue
            if maximo is not None and num > maximo:
                print(f'\nMaximo {maximo}')
                continue
            if num == 0:
                print('\nNo puede ser 0. Intenta de nuevo')
                continue
            return num
        except ValueError:
            print('\nIngresa un numero valido')

def reservar():
    while True:
        mostrar_salas_disponibles()
        selecc = input('\nSelecciona una sala: ').strip().lower()
        
        if selecc == 'atras':
            print('Volviendo al menu principal...')
            return
        
        try:
            num = int(selecc)
            if num < 1 or num > len(salas):
                print(f'\nValor invalido. Elige entre 1 y {len(salas)}')
                continue
            sala = salas[num - 1]
        except ValueError:
            print('\nValor invalido')
            continue
        
        if not sala['disponible']:
            print('\nEsta sala esta reservada. Elige otra')
            continue
        
        print(f'\n    {sala['nombre']}\n')
        print(sala['descripcion'])
        print('\nAtras')
        print()
        
        # Personas
        personas = pedir_numero(f'Cuantas personas asistiran? Maximo son {sala['max_personas']}: ', minimo=1, maximo=sala['max_personas'])
        if personas == 'atras':
            continue
        
        # Mandos / audifonos / visores
        if 'Consolas' in sala['nombre']:
            mandos = pedir_numero(f'Cuantos mandos usaran? Maximo {sala['max_mandos']}: ', minimo=1, maximo=sala['max_mandos'])
            if mandos == 'atras':
                continue
            
        elif 'PCs' in sala['nombre']:
            audifonos = pedir_numero(f'Cuantos audífonos usaran? Maximo {sala['max_audifonos']}: ', minimo=1, maximo=sala['max_audifonos'])
            if audifonos == 'atras':
                continue
            
        elif 'Realidad Virtual' in sala['nombre']:
            mandos_rv = pedir_numero(f'Cuantos mandos RV usaran? Maximo {sala['max_mandos_rv']}: ', minimo=1, maximo=sala['max_mandos_rv'])
            if mandos_rv == 'atras':
                continue
            visores_rv = pedir_numero(f'Cuantos visores RV usaran? Maximo {sala['max_visores_rv']}: ', minimo=1, maximo=sala['max_visores_rv'])
            if visores_rv == 'atras':
                continue
        
        #ERROR NO MUESTRA SMS DE ERROR
        # Juegos SOLO para consolas
        if 'Consolas' in sala['nombre']:
            while True:
                print('\nElija los juegos que quiera (Maximo 5)')
                print('Juegos disponibles:')
                
                juegos_disponibles_actuales = [juego for idx, juego in enumerate(juegos_consola) if idx not in juegos_reservados]
                
                if not juegos_disponibles_actuales:
                    print('\nNo quedan juegos disponibles')
                    print('Intenta de nuevo mas tarde o elige otra sala.')
                    break
                
                for j, juego in enumerate(juegos_disponibles_actuales, 1):
                    print(f'{j}. {juego}')
                
                print('Escribe numeros separados por coma o atras para volver')
                
                juegos_input = input().strip()
                
                if juegos_input.lower() == 'atras':
                    break
                
                # Prohibir ceros iniciales
                if any(x.startswith('0') and len(x) > 1 for x in juegos_input.split(',')):
                    print('\nNo se permiten ceros al inicio. Intenta de nuevo')
                    continue
                
                if not juegos_input:
                    print('\nError ,elige una de la opciones disponibes')
                    continue
                
                try:
                    idx_input = [int(x.strip()) - 1 for x in juegos_input.split(',')]
                    # Convertir a indices reales de la lista original
                    idx_globales = []
                    for idx_local in idx_input:
                        if 0 <= idx_local < len(juegos_disponibles_actuales):
                            juego = juegos_disponibles_actuales[idx_local]
                            idx_global = juegos_consola.index(juego)  # índice real en la lista original
                            idx_globales.append(idx_global)
                        else:
                            print(f'\nEl numero {idx_local + 1} esta fuera de rango. Intenta de nuevo')
                            break
                    
                    if len(idx_globales) != len(idx_input):
                        continue  # hubo error en algún número
                    
                    # Filtrar solo validos y sin repeticion
                    idx_validos = list(set(idx_globales))  # elimina duplicados
                    if len(idx_validos) != len(idx_globales):
                        print('\nNo se pueden repetir juegos en la misma reserva')
                        continue
                    
                    if len(idx_validos) > 5:
                        print(f'\nSolo puedes escoger hasta 5 juegos')
                        continue
                    
                    if len(idx_validos) == 0:
                        print('\nNingun juego valido seleccionado')
                        continue
                    
                    # Chequear si ya están reservados en la otra sala
                    reservados_actuales = set(idx_validos) & juegos_reservados
                    if reservados_actuales:
                        juegos_malos = [juegos_consola[i] for i in reservados_actuales]
                        print(f'\nLos siguientes juegos ya estan reservados en la otra sala: {', '.join(juegos_malos)}')
                        continue
                    
                    juegos_seleccionados = [juegos_consola[i] for i in idx_validos]
                    print(f'Juegos seleccionados ({len(juegos_seleccionados)}): {', '.join(juegos_seleccionados)}')
                    
                    # Guardar como reservados 
                    juegos_reservados.update(idx_validos)
                    break
                
                except ValueError:
                    print('\nError: Usa solo números separados por coma (ej. 1,3,5). Intenta de nuevo')
                    continue
        
        # Fecha y horario
        hoy = datetime.now()
        print('\nBien, seleccione la fecha y el horario en el que va a reservar')
        print('Fechas disponibles:')
        
        #Fechas disponibles en un plazo de 15 dias
        for d in range(16):
            fecha = hoy + timedelta(days=d)
            print(f'{d+1}. {fecha.strftime('%Y-%m-%d (%A)')}')
        
        fecha_num = pedir_numero('Selecciona fecha (numero): ', minimo=1, maximo=16)
        if fecha_num == 'atras':
            continue
        fecha_elegida = hoy + timedelta(days=fecha_num-1)
        
        print('\nHorarios disponibles (9:00 a 23:00):')
        for h in range(9, 23):
            print(f'{h-8}. {h:02d}:00')
        
        inicio_num = pedir_numero('Selecciona hora de inicio: ', minimo=1, maximo=14)
        if inicio_num == 'atras':
            continue
        hora_inicio = 8 + inicio_num
        
        while True:
            horas = pedir_numero('Cuantas horas? (minimo 1, maximo 5): ', minimo=1, maximo=5)
            if horas == 'atras':
                break
            
            hora_fin = hora_inicio + horas
            if hora_fin > 23:
                print('El horario excede las 23:00. Intenta de nuevo')
                continue
            
            #Chequear conflictos con reservas existentes en esta sala
            conflicto = False
            inicio_elegido = fecha_elegida.replace(hour=hora_inicio, minute=0)
            fin_elegido = inicio_elegido + timedelta(hours=horas)
            
            for reserva in reservas_activas:
                if reserva['sala'] == sala:
                    inicio_reserva = reserva['inicio']
                    fin_reserva = reserva['fin']
                    if (inicio_elegido < fin_reserva and fin_elegido > inicio_reserva):
                        print('Ya existe una reserva en este horario')
                        conflicto = True
                        break
            if conflicto:
                continue  #repite la pregunta de horas
            break
        
        if horas == 'atras':
            continue
        
        costo = horas * 1000
        print(f'\nCosto total: {costo}$ ({horas} horas)')
        
        while True:
            confirmar = input('\nConfirmar reserva? si/no: ').strip().lower()
            
            if confirmar in ['si']:
                print('\nReserva realizada con exito!')
                
                #Guardar la reserva
                reserva = {
                    'sala': sala,
                    'inicio': inicio_elegido,
                    'fin': fin_elegido,
                    'horas': horas,
                    'juegos': juegos_seleccionados if 'Consolas' in sala['nombre'] else [],
                    'personas': personas,
                }
                reservas_activas.append(reserva)
                
                sala['disponible'] = False
                return
            
            elif confirmar in ['no']:
                print('Reserva cancelada. Volviendo al menu principal...')
                return
            
            else:
                print('\nRespuesta invalida. Escribe si o no')
                
def avanzar_tiempo (horas=1):
    global tiempo_actual
    tiempo_actual += timedelta(hours=horas)
    print(f'\nTiempo avanzado {horas} horas. Hora actual simulada: {tiempo_actual.strftime('%Y-%m-%d %H:%M')}')
    
    #Chequear reservas terminadas
    terminadas = []
    for reserva in reservas_activas[:]:
        if tiempo_actual >= reserva['hora_fin']:
            reserva['sala']['disponible'] = True
            
            #Liberar juegos de consolas
            if 'Consolas' in reserva['sala']['nombre']:
                for juego in reserva['juegos']:
                    idx = juegos_consola.index(juego)
                    if idx in juegos_reservados:
                        juegos_reservados.remove(idx)
            terminadas.append(reserva)
            
    #Quitar las terminadas de la lista activa
    for t in terminadas:
        reservas_activas.remove(t)
        
    if terminadas:
        print(f'Se liberaron {len(terminadas)} reservas automaticamente')
    else:
        print('No hay reservas que hayan terminado aun')
        
def reset_tiempo():
    global tiempo_actual, reservas_activas, juegos_reservados
    tiempo_actual = datetime.now()
    reservas_activas = []
    juegos_reservados.clear()
    for sala in salas:
        sala['disponible'] = True
    print('Tiempo y reservas reseteados')
