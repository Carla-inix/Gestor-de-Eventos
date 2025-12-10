from suscripcion import suscrip, canc_suscrip, menu_suscrip, suscrito
from reservas import reservar, tiempo_actual, avanzar_tiempo, reservas_activas, juegos_reservados

def mostrar_hora_actual():
    print(f'\nHora actual: {tiempo_actual.strftime('%Y-%m-%d %H:%M')}')
 
def menu_principal():
    global suscrito
    
    while True:
        mostrar_hora_actual()
        print('[GLOBAL CHECK] al entrar al menu', suscrito)
        print('\n\tBienvenido a Arcane\n')
        print('1. Reservar\n2. Mis Reservas\n3. Comprar Juegos\n4. Suscripcion.\n'
            '5. Ofertas\n6. Avanzar Tiempo (Simulacion manual)\n7. Salir')

        selecc = input('Elige una opcion: ')
        if selecc == '1':
            #if suscrito:
                reservar()
            #else:
                #print('\nPara poder reservar necesitas estar suscrito')
                #print('Vamos a registrarte..')
                #if suscrip():
                    #print('Ya puedes reservar!!')
                    #reservar()
                    
        #elif selecc == '2':
            #if reservas_activas:
                #print(f'Tienes {len(reservas_activas)} reservas activas:')
                #for e in reservas_activas:
                    #print(f'-Sala: {r['sala']['nombre']} | Fin: {r['hora_fin'].strftime('$Y-%m-%d %H:%M')} | Personas: {r['personas']}')
            #else:
               #print('No tienes reservas activas')
                    
        elif selecc == '3':
            pass
        
        if selecc == '4':
            print('[DEBUG] valor de suscrito antes:',suscrito)
            if suscrito:
                print('ya estas suscrito')
                menu_suscrip()
            else:
                print('Vamos a registrarte')
                menu_suscrip()
                if suscrip():
                    print('[DEBUG] registro exitoso', suscrito)
                    menu_suscrip()  
                    
        if selecc == '5':
            pass
        
        if selecc == '6':
            try:
                horas = int(input('Cuantas horas avanzar?: '))
                avanzar_tiempo(horas)
            except ValueError:
                print('Ingresa un numero valido')
                      
        elif selecc == '7':
           print('Hasta pronto')
           break
       
        else:
            print('Opcion invalida. Elige 1-7')
    
menu_principal()