import suscripcion
from reservas import reservar, avanzar_tiempo, tiempo_actual, reservas_activas, juegos_reservados, reset_tiempo
import mis_reservas
import tienda_arcane
import ofertas


MODO_DEBUG = True

def mostrar_hora_actual():
    print(f'\nHora actual: {tiempo_actual.strftime('%Y-%m-%d | %H:%M')}')
    
def mostrar_encabezado():
    print('\n' + '=' * 40)
    print('           ARCANE GAMING LOUNGE')
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
        print('3. Comprar Juegos')
        print('4. Suscripción')
        print('5. Ofertas')
        
        if MODO_DEBUG:
           print('6. Avanzar Tiempo (Modo Prueba)')
           
        print('7. Salir')

        selecc = input('\nElige una opcion: ')
        if selecc == '1':
            if suscripcion.suscrito:
                reservar()
            else:
                print('\nPara poder reservar necesitas estar suscrito')
    
                if suscripcion.suscrip():
                    print('\nYa puedes reservar')
                    reservar()
                    
        elif selecc == '2':
            if suscripcion.user_actual is None:
                print('Debes suscribirte primero')
            else:
                mis_reservas.reservas_usuario()
                    
        elif selecc == '3':
            if suscripcion.suscrito:
                tienda_arcane.menu_tienda()
            else:
                print('\nPara poder comprar necesitas estar suscrito')
    
                if suscripcion.suscrip():
                    print('\nYa puedes comprar')
                    tienda_arcane.menu_tienda()
        
        elif selecc == '4':
            if suscripcion.suscrito:
                suscripcion.menu_suscrip()
                
            else:
                suscripcion.suscrip()
                    
        elif selecc == '5':
            ofertas.mostrar_ofertas()
        
        elif selecc == '6' and MODO_DEBUG:
            while True:
                print('\nMODO PRUEBA / SIMULACIÓN')
                print('1. Avanzar tiempo')
                print('2. Resetear tiempo y reservas')
                print('3. Atras')

                opcion_test = input('Elige una opción: ').strip()

                if opcion_test == '1':
                    try:
                        horas = int(input('Cuántas horas deseas avanzar?: '))
                        if horas <= 0:
                            print('Debes ingresar un número positivo')
                        else:
                            avanzar_tiempo(horas)
                    except ValueError:
                        print('Ingresa un número válido')

                elif opcion_test == '2':
                    confirmar = input(
                        '\nEsto eliminará reservas y reiniciará el tiempo\n'
                        'Estás seguro? si/no: '
                    ).lower().strip()

                    if confirmar == 'si':
                        reset_tiempo()

                elif opcion_test == '3':
                    break

                else:
                    print('Opción inválida')
                      
        elif selecc == '7':
           print('Hasta pronto')
           break
        else:
            print('Opcion invalida. Elige 1-7')
    
menu_principal()