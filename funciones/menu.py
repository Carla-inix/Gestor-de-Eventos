from reservas import reservar
from estado import tiempo_actual
from horarios_r import avanzar_tiempo, reset_tiempo
import suscripcion
import mis_reservas
import tienda_arcane
import ofertas


MODO_DEBUG = True

def mostrar_hora_actual():
    print(f'\nFecha y hora: {tiempo_actual.strftime('%d-%m-%Y | %H:%M')}')
    
def mostrar_encabezado():
    print('\n' + '=' * 40)
    print('         Arcane Gaming Lounge')
    print('=' * 40)
    print('Horario: 09:00 AM - 11:00 PM')
    print('Contacto: arcane@gaming.com | Tel: +53 53529701')
    print('-' * 40)
    
 
def menu_principal():
    while True:
        mostrar_encabezado()
        mostrar_hora_actual()
        print('-' * 40)
        
        print('\n1. Reservar')
        print('2. Mis Reservas')
        print('3. Tienda Arcane')
        print('4. Suscripción')
        print('5. Ofertas')
        print('6. Salir')
        
        if MODO_DEBUG:
            print('\n7. Avanzar Tiempo (Modo Prueba)')

        selecc = input('\nElige una opción: ')
        if selecc == '1':
            if suscripcion.suscrito:
                reservar()
            else:
                print('\nPara reservar necesitas estar suscrito/a')
    
                if suscripcion.suscrip():
                    reservar()
                    
        elif selecc == '2':
            mis_reservas.reservas_usuario()
                    
        elif selecc == '3':
            if suscripcion.suscrito:
                tienda_arcane.menu_tienda()
            else:
                print('\nPara acceder necesitas estar suscrito/a')
    
                if suscripcion.suscrip():
                    tienda_arcane.menu_tienda()
        
        elif selecc == '4':
            if suscripcion.suscrito:
                suscripcion.menu_suscrip()
                
            else:
                suscripcion.suscrip()
                    
        elif selecc == '5':
            ofertas.mostrar_ofertas()
            
        elif selecc == '6':
           print('Hasta pronto')
           break
        
        elif selecc == '7' and MODO_DEBUG:
            while True:
                print('\nMODO PRUEBA / SIMULACIÓN\n')
                print('1. Avanzar tiempo')
                print('2. Resetear tiempo y reservas')
                print('3. Atrás')

                opcion_test = input('Elige una opción: ').strip()

                if opcion_test == '1':
                    try:
                        horas = int(input('Cuántas horas deseas avanzar?: '))
                        if horas <= 0:
                            print('\nIngresa un número válido\n')
                        else:
                            avanzar_tiempo(horas)
                    except ValueError:
                        print('\nIngresa un número válido\n')

                elif opcion_test == '2':
                    confirmar = input(
                        '\nEsto eliminará reservas y reiniciará el tiempo\n'
                        'Estás seguro/a? si/no: '
                    ).lower().strip()

                    if confirmar == 'si':
                        reset_tiempo()

                elif opcion_test == '3':
                    break

                else:
                    print('\nOpción inválida')
                      
        else:
            print('\nOpción inválida. Elige 1-7')
    
menu_principal()