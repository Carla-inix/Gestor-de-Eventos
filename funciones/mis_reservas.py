from . import estado
from .recursos_r import cancelar_reserva, liberar_reservas
from . import suscripcion


# Permite al usuario ver y cancelar sus reservas activas
def reservas_usuario():
    
    # Antes de mostrar, limpia las reservas que ya hayan terminado
    liberar_reservas()

    while True:
        print('\n' + '=' * 40)
        print('              Mis Reservas')
        print('=' * 40)

        if suscripcion.user_actual is None:
            print('No hay ningún usuario activo')
            input('\nPresiona Enter para volver...')
            return

        # Filtrar solo las reservas que pertenecen al usuario actual
        mis_reservas = [
            r for r in estado.reservas_activas
            if r['usuario'] == suscripcion.user_actual
        ]

        if not mis_reservas:
            print('\nNo tienes reservas activas')
            input('\nPresiona Enter para volver...')
            return

        # Mostrar cada reserva con su respectiva información
        for i, reserva in enumerate(mis_reservas, 1):
            inicio = reserva['inicio'].strftime('%d-%m-%Y | %H:%M')
            fin = reserva['fin'].strftime('%H:%M')

            print(f'\n{i}. {reserva["sala"]["nombre"]}')
            print(f'    Horario:  {inicio} - {fin}')
            print(f'    Duración: {reserva["horas"]} hora(s)')
            print(f'    Personas: {reserva["personas"]}')

            # Mostrar equipos reservados con nombres legibles
            if reserva.get('recursos'):
                equipos = ', '.join(
                    f'{r.replace("_", " ")} x{c}'
                    for r, c in reserva['recursos'].items()
                )
                print(f'    Equipos: {equipos}')

            if reserva['juegos']:
                print(f'    Juegos: {", ".join(reserva["juegos"])}')
                
            print(f'    Monto: {reserva["costo"]}$')

            if reserva.get('descuento'):
                print('    Descuento aplicado: 20%')

            print('-' * 35)
            

        # MENÚ
        #===========================================
        print('\nOpciones:')
        print('1. Cancelar reservas')
        print('2. Atrás')

        selecc = input('\nElige una opción: ').strip()

        if selecc == '1':
            while True:
                cancelar = input(
                    '\nEscribe los números de las reservas a cancelar '
                    '(ej: 1,3), todas o atras para volver: '
                ).strip().lower()
                
                if cancelar == 'atras':
                    break
                
                if cancelar == '':
                    print('\nTu respuesta no puede estar vacía')
                    continue

                # Cancelar todas las reservas del usuario
                if cancelar == 'todas':
                    for r in mis_reservas[:]:
                        cancelar_reserva(r)
                    print('\nTodas las reservas han sido canceladas')
                    input('\nPresiona Enter para continuar...')
                    break

                partes = [x.strip() for x in cancelar.split(',')]

                # Valida que los valores ingresados sean números
                if not all(p.isdigit() and not p.startswith('0') for p in partes):
                    print('\nEntrada inválida')
                    continue

                indices = sorted(set(int(p) for p in partes))

                # Valida que los números estén en el rango correcto
                if any(i < 1 or i > len(mis_reservas) for i in indices):
                    print('\nNúmero fuera de rango')
                    continue

                # Cancelar en orden inverso para no afectar los índices
                for i in reversed(indices):
                    cancelar_reserva(mis_reservas[i - 1])

                print('\nReservas canceladas con éxito')
                input('\nPresiona Enter para continuar...')
                break

        elif selecc == '2':
            return

        else:
            print('\nOpción inválida\n')