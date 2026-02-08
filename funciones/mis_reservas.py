from datetime import datetime
from estado import reservas_activas 
from recursos_r import cancelar_reserva, liberar_reservas
from inputs import pedir_numero
import suscripcion


def reservas_usuario():
    liberar_reservas()
   
    while True:
        print('\n' + '=' * 40)
        print('              Mis Reservas')
        print('=' * 40)

        if suscripcion.user_actual is None:
            print('No hay ningún usuario activo')
            input('\nPresiona Enter para volver...')
            return
        
        
        # Obtener reservas del usuario
        mis_reservas = [
            r for r in reservas_activas
            if r['usuario'] == suscripcion.user_actual
        ]

        if not mis_reservas:
            print('No tienes reservas activas')
            input('\nPresiona Enter para volver...')
            return
        

        # Mostrar reservas
        for i, reserva in enumerate(mis_reservas, 1):
            inicio = reserva['inicio'].strftime('%d-%m-%Y | %H:%M')
            fin = reserva['fin'].strftime('%H:%M')

            print(f'{i}. {reserva['sala']['nombre']}')
            print(f'    Horario: {inicio} - {fin}')
            print(f'    Duración: {reserva['horas']} horas')
            print(f'    Personas: {reserva['personas']}')
            
            if reserva.get('recursos'):
                equipos = ', '.join(
                    f'{r.replace('_', ' ')} {c}'
                    for r, c in reserva['recursos'].items()
                )
                print(f'    Equipos: {equipos}')

            if reserva['juegos']:
                print(f'    Juegos: {', '.join(reserva['juegos'])}')

            if reserva.get('descuento'):
                print('    Descuento aplicado: 20%')

            print('-' * 35)
            
        

        #MENÚ
        #===============================
        
        print('\nOpciones:')
        print('1. Cancelar reservas')
        print('2. Atrás')

        selecc = input('\nElige una opción: ').strip()
        
        if selecc == '1':
            cancelar = input(
                '\nEscribe los números de las reservas a cancelar '
                '(ej: 1,3), todas o atras para volver: '
            ).strip().lower()

            if cancelar == 'atras':
                continue

            if cancelar == 'todas':
                for r in mis_reservas[:]:
                    cancelar_reserva(r)

                print('\nTodas las reservas han sido canceladas')
                continue

            partes = [x.strip() for x in cancelar.split(',')]

            if not all(p.isdigit() for p in partes):
                print('\nEntrada inválida\n')
                continue

            indices = sorted(set(int(p) for p in partes))

            if any(i < 1 or i > len(mis_reservas) for i in indices):
                print('\nEntrada inválida\n')
                continue

            for i in reversed(indices):
                cancelar_reserva(mis_reservas[i - 1])

            print('\nReservas canceladas con éxito')
            input('\nPresiona Enter para continuar...')

        elif selecc == '2':
            return

        else:
            print('\nOpción inválida\n')