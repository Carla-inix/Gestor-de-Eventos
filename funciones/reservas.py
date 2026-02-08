from datetime import timedelta
import suscripcion
from inputs import pedir_numero
from estado import reservas_activas, historial_reservas
from datos import salas, juegos_consola
from horarios_r import tiempo_actual, obtener_horas_dispo, buscar_prox_horario, pedir_duracion, usuario_ocupado
from recursos_r import recursos_stock, recursos_en_uso, validar_dispo_recursos, consumir_recursos, liberar_reservas
from juegos import selecc_juegos, validar_juegos, prox_liberacion_juegos


# RESERVAS
# ===============================

def reservar():
    liberar_reservas()
    while True:
        print('\n' + '=' * 40)
        print('           Salas disponibles')
        print('=' * 40)
        
        for i, sala in enumerate(salas, 1):
            print(f'{i}. {sala['nombre']}')
        print('\n.Atrás\n')

        selecc = pedir_numero('Selecciona una sala: ', minimo=1, maximo=len(salas), atras=True)
        
        if selecc == 'atras':
            return
        
        sala = salas[num - 1]
        
        recursos_usados = {}
        
        
        #Validación de recursos disponibles
        disponible, fecha_libre = validar_dispo_recursos(sala)
        
        if not disponible:
            print('\nNo hay equipos suficientes para reservar la sala')

            if fecha_libre:
                print(f'Volverá a estar disponible el: {fecha_libre.strftime('%d-%m-%Y | %H:%M')}')
                
            input('\nPresiona Enter para volver...')
            continue
        
        
        #Validación de juegos disponibles
        if 'Consolas' in sala['nombre'] and not validar_juegos():
            print('\nNo hay juegos disponibles para reservar la sala')  
            fecha = prox_liberacion_juegos()
            
            if fecha:
                print(f'Volverá a estar disponible el: {fecha.strftime('%d-%m-%Y | %H:%M')}')
                
            input('\nPresiona enter para volver...') 
            continue
            
        
        #Info de la Sala
        #====================================
        
        print(f'\n    {sala['nombre']}\n')
        print(sala['descripcion'])
        print('\n.Atrás\n')
        

        personas = pedir_numero(f'Cuántas personas asistirán? Máximo son {sala['max_personas']}: ', minimo=1, maximo=sala['max_personas'], atras=True)
        
        if personas == 'atras':
            continue
        
        
        #Recursos\Equipos: sillas, sofás, mandos, audífonos, visores, caminadoras

        #CONSOLAS
        if 'Consolas' in sala['nombre']:
           
            disponibles_sillas = recursos_stock['sillas'] - recursos_en_uso['sillas']
            disponibles_sofas = recursos_stock['sofas'] - recursos_en_uso['sofas']
            disponibles_mandos = recursos_stock['mandos'] - recursos_en_uso['mandos']
            
            max_sillas_real = min(sala['max_sillas'], disponibles_sillas)
            max_sofas_real = min(sala['max_sofas'], disponibles_sofas)
            max_mandos_real = min(sala['max_mandos'], disponibles_mandos)
            
            tipo_asiento = pedir_numero('Usarán sillas (1) o sofás (2)? ', minimo=1, maximo=2, atras=True)
            if tipo_asiento == 1:
                sillas = pedir_numero(
                f'Cuántas sillas usarán? (Máx 4 | Disponibles: {disponibles_sillas}): ',
                minimo=1,
                maximo=max_sillas_real,
                atras=True
            )

                if sillas == 'atras':
                    continue

                recursos_usados['sillas'] = sillas
                
            elif tipo_asiento == 2:
                sofas = pedir_numero(
                f'Cuántos sofas usarán? (Máx 2 | Disponibles: {disponibles_sofas}): ',
                minimo=1,
                maximo=max_sofas_real,
                atras=True
            )

                if sofas == 'atras':
                    continue

                recursos_usados['sofas'] = sofas
    
            mandos = pedir_numero(
                f'Cuántos mandos usarán? (Máx 4 | Disponibles: {disponibles_mandos}): ',
                minimo=1,
                maximo=max_mandos_real,
                atras=True
            )

            if mandos == 'atras':
                continue

            recursos_usados['mandos'] = mandos 


        #PCs
        elif 'PCs' in sala['nombre']:
            disponibles_sillas = recursos_stock['sillas'] - recursos_en_uso['sillas']
            disponibles_audifonos = recursos_stock['audifonos'] - recursos_en_uso['audifonos']
            
            max_sillas_real = min(sala['max_sillas'], disponibles_sillas)
            max_audifonos_real = min(sala['max_audifonos'], disponibles_audifonos)
            
            sillas = pedir_numero(
                f'Cuántas sillas usarán? (Máx 4 | Disponibles: {disponibles_sillas}): ',
                minimo=1,
                maximo=max_sillas_real,
                atras=True
            )

            if sillas == 'atras':
                continue

            recursos_usados['sillas'] = sillas

            audifonos = pedir_numero(
                f'Cuántos audífonos usarán? (Máx 6 | Disponibles: {disponibles_audifonos}): ',
                minimo=1,
                maximo=max_audifonos_real,
                atras=True
            )

            if audifonos == 'atras':
                continue

            recursos_usados['audifonos'] = audifonos


        #Realidad Virtual
        elif 'Realidad Virtual' in sala['nombre']:

            disponibles_visores_rv = recursos_stock['visores_rv'] - recursos_en_uso['visores_rv']
            disponibles_mandos_rv = recursos_stock['mandos_rv'] - recursos_en_uso['mandos_rv']
            disponibles_caminadora_rv = recursos_stock['caminadora_rv'] - recursos_en_uso['caminadora_rv']
            
            max_visores_rv_real = min(sala['max_visores_rv'], disponibles_visores_rv)
            max_mandos_rv_real = min(sala['max_mandos_rv'], disponibles_mandos_rv)
            max_caminadora_rv_real = min(sala['max_caminadora_rv'], disponibles_caminadora_rv)

            visores_rv = pedir_numero(
                f'Cuántos visores RV usarán? (Máx 8 | Disponibles: {disponibles_visores_rv}): ',
                minimo=1,
                maximo=max_visores_rv_real,
                atras=True
            )
            
            if visores_rv == 'atras':
                continue

            mandos_rv = pedir_numero(
                f'Cuántos mandos RV usarán? (Máx 8 | Disponibles: {disponibles_mandos_rv}): ',
                minimo=0,
                maximo=max_mandos_rv_real,
                atras=True
            )
            
            if mandos_rv == 'atras':
                continue

            caminadora_rv = pedir_numero(
                f'Cuántas caminadoras RV usarán? (Máx 3 | Disponibles: {disponibles_caminadora_rv}): ',
                minimo=0,
                maximo=max_caminadora_rv_real,
                atras=True
            )
            
            if caminadora_rv == 'atras':
                continue
            
            if (mandos_rv > 0 and caminadora_rv == 0) or (caminadora_rv > 0 and mandos_rv == 0):
                print('\nPara usar una caminadora RV debes usar un mando RV o viceversa\n')
                continue
            
            recursos_usados['visores_rv'] = visores_rv

            if mandos_rv > 0:
                recursos_usados['mandos_rv'] = mandos_rv

            if caminadora_rv > 0:
                recursos_usados['caminadora_rv'] = caminadora_rv
          
              
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
        
        while True:
            hoy = tiempo_actual.replace(hour=0, minute=0, second=0, microsecond=0)
            print('\nFechas disponibles:\n')
            for i in range(7):
                print(f'{i+1}. {(hoy + timedelta(days=i)).strftime('%d-%m-%Y')}')

            selecc_f = pedir_numero('Selecciona la fecha: ', minimo=1, maximo=7, atras=True)
            
            if selecc_f == 'atras':
                break 

            fecha = hoy + timedelta(days=selecc_f - 1)
            horas_disp = obtener_horas_dispo(fecha, sala)

            if not horas_disp:
                print('No hay horarios disponibles para ese día')
                sugerido = buscar_prox_horario(sala, 1)
                if sugerido:
                    ini_sug, fin_sug = sugerido
                    print(
                        f'Próximo hueco disponible: '
                        f'{ini_sug.strftime('%d-%m-%Y')} | {ini_sug.strftime('%H:%M')} '
                        f'a {fin_sug.strftime('%d-%m-%Y')} | {fin_sug.strftime('%H:%M')}'
                    )
                continue

            #Horario
            while True:
                print('\nHorarios disponibles:\n')
                for i, h in enumerate(horas_disp, 1):
                    print(f'{i}. {h:02d}:00')

                selecc_h = pedir_numero('Hora de inicio: ', minimo=1, maximo=len(horas_disp), atras=True)
                
                if selecc_h == 'atras':
                    break

                hora_inicio = horas_disp[selecc_h - 1]
                inicio = fecha.replace(hour=hora_inicio, minute=0)

                if inicio <= tiempo_actual:
                    print('\nHorario inválido\n')
                    continue

                #Duración
                print('\nEl costo es 1000$ la hora')
                horas = pedir_duracion(hora_inicio, horas_disp)
                if horas is None:
                    continue 

                fin = inicio + timedelta(hours=horas)
                
                if usuario_ocupado(suscripcion.user_actual, inicio, fin):
                    print('\nNo puedes reservar dos salas en el mismo horario')
                    continue
                
                break

            if horas is not None:
                break
        
        if horas is None:
            continue
        
        
        # COSTO Y CUPÓN 
        #=================================
        
        costo_base = horas * 1000
        descuento_aplicado = False
        usar_cupon = False

        if suscripcion.cupon_disponible and not suscripcion.cupon_usado:
            descuento = costo_base * 0.20
            precio_final -= descuento
            usar_cupon = True
            
            print(f'\nCupón aplicado: {descuento}$')

        else:
            print(f'\nCosto total: {costo_base}$')
        
        
         # CONFIRMACIÓN
        #==================================
        
        while True:
            
            confirmar = input('\nConfirmar reserva si/no: ').strip().lower()
            
            if confirmar == 'si':
                if usar_cupon:
                    suscripcion.cupon_usado = True
                    suscripcion.cupon_disponible = False
                    descuento_aplicado = True
                
                print('\nReserva realizada con éxito!')
               
                #Guardar la reserva
                reserva = ({
                    'usuario': suscripcion.user_actual,
                    'sala': sala,
                    'inicio': inicio,
                    'fin': fin,
                    'horas': horas,
                    'personas': personas,
                    'juegos': juegos,
                    'recursos': recursos_usados,
                    'descuento': descuento_aplicado,
                })

                reservas_activas.append(reserva)
                historial_reservas.append(reserva)
                
                consumir_recursos(recursos_usados)
                
                from ofertas import contar_reservas_usuario
                
                total_c = contar_reservas_usuario(suscripcion.user_actual)
                if total_c >=5 and not suscripcion.cupon_usado:
                    suscripcion.cupon_disponible = True
                    
                input('\nPresiona Enter para volver...')
                return
            
            elif confirmar == 'no':
                print('\nReserva cancelada')
                input('\nPresiona Enter para volver...')
                return
                
            else:
                print('\nRespuesta inválida. Escribe si o no\n')