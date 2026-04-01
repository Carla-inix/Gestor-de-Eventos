from datetime import timedelta
from . import suscripcion
from . import estado
from .inputs import pedir_numero
from .datos import salas, juegos_consola
from .horarios_r import obtener_horas_dispo, buscar_prox_horario, pedir_duracion, usuario_ocupado
from .recursos_r import recursos_stock, recursos_en_uso, validar_dispo_recursos, consumir_recursos, liberar_reservas
from .juegos import selecc_juegos, validar_juegos, prox_liberacion_juegos
from .ofertas import contar_reservas_usuario


# RESERVAS
# ===============================

def reservar():
    liberar_reservas()

    while True:
        print('\n' + '=' * 40)
        print('           Salas disponibles')
        print('=' * 40)

        for i, sala in enumerate(salas, 1):
            print(f'{i}. {sala["nombre"]}')
        print('\n.Atrás\n')

        selecc = pedir_numero('Selecciona una sala: ', minimo=1, maximo=len(salas), atras=True)

        if selecc == 'atras':
            return

        sala = salas[selecc - 1]
        
        recursos_usados = {}


        #Validación de recursos disponibles
        disponible, fecha_libre = validar_dispo_recursos(sala)

        if not disponible:
            print('\nNo hay equipos suficientes para reservar esta sala')
            
            if fecha_libre:
                print(f'Volverá a estar disponible el: {fecha_libre.strftime("%d-%m-%Y | %H:%M")}')
            
            input('\nPresiona Enter para volver...')
            continue

        # Valida que haya juegos disponibles en las salas de consolas
        if 'Consolas' in sala['nombre'] and not validar_juegos():
            print('\nNo hay juegos disponibles para reservar la sala')
            fecha = prox_liberacion_juegos()
            
            if fecha:
                print(f'Volverá a estar disponible el: {fecha.strftime("%d-%m-%Y | %H:%M")}')
            
            input('\nPresiona Enter para volver...')
            continue
        

        #Info de la Sala
        #===================================
        
        print('\n' + '=' * 50)
        print(f'                {sala["nombre"]}')
        print('=' * 50)
        print(sala['descripcion'])
        print('-' * 50)
        print('.Atrás\n')

        personas = pedir_numero(
            f'Cuántas personas asistirán? (Máx {sala["max_personas"]}): ',
            minimo=1,
            maximo=sala['max_personas'],
            atras=True
        )

        if personas == 'atras':
            continue


        # RECURSOS/EQUIPOS
        #===============================

        # CONSOLAS I y II
        if 'Consolas' in sala['nombre']:

            disponibles_sillas = recursos_stock['sillas'] - recursos_en_uso['sillas']
            disponibles_sofas = recursos_stock['sofas'] - recursos_en_uso['sofas']
            disponibles_mandos = recursos_stock['mandos'] - recursos_en_uso['mandos']

            max_sillas_real = min(sala['max_sillas'], disponibles_sillas)
            max_sofas_real = min(sala['max_sofas'], disponibles_sofas)
            max_mandos_real = min(sala['max_mandos'], disponibles_mandos)

            # Si ambos están agotados, la sala no puede reservarse
            if disponibles_sillas == 0 and disponibles_sofas == 0:
                print('\nNo hay sillas ni sofás disponibles para reservar la sala')
                input('\nPresiona Enter para volver...')
                continue

            # Restricción de exclusión mutua: sillas o sofás, no ambos
            # Si solo uno tiene stock, se asigna automáticamente
            if disponibles_sillas > 0 and disponibles_sofas > 0:
                tipo_asiento = pedir_numero('Usarán sillas (1) o sofás (2)? ', minimo=1, maximo=2, atras=True)
                
                if tipo_asiento == 'atras':
                    continue
                
            elif disponibles_sillas > 0:
                print('\nSofás agotados. Se asignarán sillas automáticamente')
                tipo_asiento = 1
                
            else:
                print('\nSillas agotadas. Se asignarán sofás automáticamente')
                tipo_asiento = 2
        

            if tipo_asiento == 1:
                sillas = pedir_numero(
                    f'Cuántas sillas usarán? (Máx {sala["max_sillas"]} | Disponibles: {disponibles_sillas}): ',
                    minimo=1,
                    maximo=max_sillas_real,
                    atras=True
                )
                if sillas == 'atras':
                    continue
                recursos_usados['sillas'] = sillas

            elif tipo_asiento == 2:
                sofas = pedir_numero(
                    f'Cuántos sofás usarán? (Máx {sala["max_sofas"]} | Disponibles: {disponibles_sofas}): ',
                    minimo=1,
                    maximo=max_sofas_real,
                    atras=True
                )
                if sofas == 'atras':
                    continue
                recursos_usados['sofas'] = sofas

            mandos = pedir_numero(
                f'Cuántos mandos usarán? (Máx {sala["max_mandos"]} | Disponibles: {disponibles_mandos}): ',
                minimo=1,
                maximo=max_mandos_real,
                atras=True
            )
            if mandos == 'atras':
                continue
            recursos_usados['mandos'] = mandos


        # PCs
        elif 'PCs' in sala['nombre']:

            disponibles_sillas = recursos_stock['sillas'] - recursos_en_uso['sillas']
            disponibles_audifonos = recursos_stock['audifonos'] - recursos_en_uso['audifonos']

            max_sillas_real = min(sala['max_sillas'], disponibles_sillas)
            max_audifonos_real = min(sala['max_audifonos'], disponibles_audifonos)
            
            # Sin sillas no se puede usar la sala PCs
            if disponibles_sillas == 0:
                print('\nNo hay sillas disponibles para reservar la sala')
                input('\nPresiona Enter para volver...')
                continue

            sillas = pedir_numero(
                f'Cuántas sillas usarán? (Máx {sala["max_sillas"]} | Disponibles: {disponibles_sillas}): ',
                minimo=1,
                maximo=max_sillas_real,
                atras=True
            )
            if sillas == 'atras':
                continue
            recursos_usados['sillas'] = sillas

            audifonos = pedir_numero(
                f'Cuántos audífonos usarán? (Máx {sala["max_audifonos"]} | Disponibles: {disponibles_audifonos}): ',
                minimo=1,
                maximo=max_audifonos_real,
                atras=True
            )
            if audifonos == 'atras':
                continue
            recursos_usados['audifonos'] = audifonos


        # REALIDAD VIRTUAL
        elif 'Realidad Virtual' in sala['nombre']:

            disponibles_visores = recursos_stock['visores_rv'] - recursos_en_uso['visores_rv']
            disponibles_mandos_rv = recursos_stock['mandos_rv'] - recursos_en_uso['mandos_rv']
            disponibles_caminadoras = recursos_stock['caminadora_rv'] - recursos_en_uso['caminadora_rv']

            max_visores_real = min(sala['max_visores_rv'], disponibles_visores)
            max_mandos_rv_real = min(sala['max_mandos_rv'], disponibles_mandos_rv)
            max_caminadoras_real = min(sala['max_caminadora_rv'], disponibles_caminadoras)

            visores = pedir_numero(
                f'Cuántos visores RV usarán? (Máx {sala["max_visores_rv"]} | Disponibles: {disponibles_visores}): ',
                minimo=1,
                maximo=max_visores_real,
                atras=True
            )
            if visores == 'atras':
                continue
            recursos_usados['visores_rv'] = visores

            # Si uno de los dos equipos está agotado, ambos quedan fuera
            if disponibles_mandos_rv == 0 or disponibles_caminadoras == 0:
                agotado = 'Mandos RV' if disponibles_mandos_rv == 0 else 'Caminadoras Omnis'
                print(f'\n{agotado} agotados. Para usar los mandos RV o las caminadoras Omnis, ambos deben estar disponibles')
                seguir = input('Deseas continuar la reserva sin estos equipos? si/no: ').strip().lower()
                
                if seguir != 'si':
                    continue
                mandos_rv = 0
                caminadoras = 0
                
            else:
                mandos_rv = pedir_numero(
                    f'Cuántos mandos RV usarán? (Máx {sala["max_mandos_rv"]}, 0 si no necesitan | Disponibles: {disponibles_mandos_rv}): ',
                    minimo=0,
                    maximo=max_mandos_rv_real,
                    atras=True
                )
                if mandos_rv == 'atras':
                    continue

                caminadoras = pedir_numero(
                    f'Cuántas caminadoras Omnis usarán? (Máx {sala["max_caminadora_rv"]}, 0 si no necesitan | Disponibles: {disponibles_caminadoras}): ',
                    minimo=0,
                    maximo=max_caminadoras_real,
                    atras=True
                )
                if caminadoras == 'atras':
                    continue

            # Restricción de co-requisito: mando RV y caminadora RV deben ir juntos
            if (mandos_rv > 0 and caminadoras == 0) or (caminadoras > 0 and mandos_rv == 0):
                print('\nPara usar una caminadora Omnis necesitas también un mando RV, y viceversa\n')
                continue

            if mandos_rv > 0:
                recursos_usados['mandos_rv'] = mandos_rv
                
            if caminadoras > 0:
                recursos_usados['caminadora_rv'] = caminadoras


        # JUEGOS CONSOLAS
        #===============================
        
        juegos = []
        if 'Consolas' in sala['nombre']:
            juegos = selecc_juegos(juegos_consola)
            if juegos is None:
                continue


        # FECHA Y HORARIO
        #===============================
        
        inicio = None
        fin = None
        horas = None
        cancelado = False

        while True:
            hoy = estado.tiempo_actual.replace(hour=0, minute=0, second=0, microsecond=0)
            print('\n' + '=' * 30)
            print('      Fechas disponibles:')
            print('=' * 30)
            for i in range(7):
                print(f'{i + 1}. {(hoy + timedelta(days=i)).strftime("%d-%m-%Y")}')

            selecc_f = pedir_numero('\nSelecciona la fecha: ', minimo=1, maximo=7, atras=True)

            if selecc_f == 'atras':
                cancelado = True
                break

            fecha = hoy + timedelta(days=selecc_f - 1)
            horas_disp = obtener_horas_dispo(fecha, sala)

            if not horas_disp:
                print('\nNo hay horarios disponibles para ese día')
                sugerido = buscar_prox_horario(sala, 1)
                if sugerido:
                    ini_sug, fin_sug = sugerido
                    print(
                        f'Próximo hueco disponible: '
                        f'{ini_sug.strftime("%d-%m-%Y")} | {ini_sug.strftime("%H:%M")} '
                        f'a {fin_sug.strftime("%H:%M")}'
                    )
                continue

            #Horario
            while True:
                print('\n' + '=' * 30)
                print('     Horarios disponibles:')
                print('=' * 30)
                for i, h in enumerate(horas_disp, 1):
                    print(f'{i}. {h:02d}:00')

                selecc_h = pedir_numero('Hora de inicio: ', minimo=1, maximo=len(horas_disp), atras=True)

                if selecc_h == 'atras':
                    break

                hora_inicio = horas_disp[selecc_h - 1]
                inicio = fecha.replace(hour=hora_inicio, minute=0)

                if inicio <= estado.tiempo_actual:
                    print('\nEse horario ya pasó, elige uno futuro\n')
                    continue

                #Duración
                print('\n' + '=' * 30)
                print('\nEl costo es 1000$ por hora')
                horas = pedir_duracion(hora_inicio, horas_disp)
                if horas is None:
                    continue

                fin = inicio + timedelta(hours=horas)

                if usuario_ocupado(suscripcion.user_actual, inicio, fin):
                    print('\nYa tienes una reserva en ese horario\n')
                    inicio = None
                    fin = None
                    horas = None
                    continue

                break

            if horas is not None:
                break

        if cancelado:
            continue

        if horas is None:
            continue


        # COSTO Y CUPÓN 
        #=================================
        
        costo_base = horas * 1000
        descuento_aplicado = False
        usar_cupon = False

        if suscripcion.cupon_disponible and not suscripcion.cupon_usado:
            descuento = costo_base * 0.20
            precio_final = costo_base - descuento
            usar_cupon = True
            print('=' * 30)
            print(f'\nCupón aplicado! Descuento: {int(descuento)}$')
            print(f'Costo total: {int(precio_final)}$')
            
        else:
            print('=' * 30)
            precio_final = costo_base
            print(f'\nCosto total: {int(precio_final)}$')


        # CONFIRMACIÓN
        #==================================
        
        while True:
            confirmar = input('\nConfirmar reserva si/no: ').strip().lower()

            if confirmar == 'si':
                if usar_cupon:
                    suscripcion.cupon_usado = True
                    suscripcion.cupon_disponible = False
                    descuento_aplicado = True

                # Guardar la reserva
                reserva = {
                    'usuario': suscripcion.user_actual,
                    'sala': sala,
                    'inicio': inicio,
                    'fin': fin,
                    'horas': horas,
                    'personas': personas,
                    'juegos': juegos,
                    'recursos': recursos_usados,
                    'costo': precio_final,
                    'descuento': descuento_aplicado,
                }

                estado.reservas_activas.append(reserva)
                estado.historial_reservas.append(reserva)
                consumir_recursos(recursos_usados)

                # Verificar si el usuario desbloqueó el cupón con esta reserva
                total_reservas = contar_reservas_usuario(suscripcion.user_actual)
                if total_reservas >= 5 and not suscripcion.cupon_usado:
                    suscripcion.cupon_disponible = True
                    print('=' * 40)
                    print('\nDesbloqueaste un cupón de 20% de descuento!')

                print('\nReserva realizada con éxito!❤')
                input('\nPresiona Enter para volver...')
                return

            elif confirmar == 'no':
                print('\nReserva cancelada')
                input('\nPresiona Enter para volver...')
                return

            else:
                print('\nRespuesta inválida. Escribe si o no\n')