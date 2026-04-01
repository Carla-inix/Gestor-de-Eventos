from .inputs import pedir_numero

# Estado global del usuario en sesión
usuarios = {}          
suscrito = False       
user_actual = None     
cupon_disponible = False  
cupon_usado = False       


# REGISTRO
#===========================================

def suscrip():
    global suscrito, user_actual
    
    print('\nVamos a registrarte..')
    
    while True:
        nombre = input('Nombre: ').strip()

        if nombre == 'atras':
            return

        if nombre == '':
            print('\nTu nombre no puede estar vacío\n')
            continue

        if not nombre.isalpha():
            print('\nTu nombre solo puede tener letras\n')
            continue

        while True:
            carnet = input('Ingresa tu carnet de identidad (11 números): ').strip()

            if carnet == 'atras':
                return

            if carnet == '':
                print('\nTu ID no puede estar vacío\n')
                continue

            if not carnet.isdigit():
                print('\nTu ID solo puede tener números enteros\n')
                continue

            if len(carnet) != 11:
                print('\nEl ID debe tener exactamente 11 dígitos\n')
                continue

            id_user = int(carnet)

            if id_user in usuarios:
                print('\nEse ID ya está registrado\n')
                continue

            break
         
        # Registrar usuario y activar sesión           
        usuarios[id_user] = nombre
        suscrito = True
        user_actual = id_user

        print('\nYa estás suscrito/a!❤️')
        input('\nPresiona Enter para volver...')
        return True


# CANCELAR SUSCRIPCIÓN
# ==============================================

#Cancela la suscripción del usuario actual
def canc_suscrip():
    from . import estado
    from .recursos_r import cancelar_reserva
    global suscrito, user_actual

    while True:
        print('\nAl cancelar tu suscripción se eliminarán todas tus reservas activas')

        confirmar = input('Seguro/a que quieres cancelar? si/no: ').strip().lower()

        if confirmar == 'si':
            # Cancela todas las reservas activas del usuario
            for r in estado.reservas_activas[:]:
                if r['usuario'] == user_actual:
                    cancelar_reserva(r)
            
            # Eliminar usuario del registro y cerrar sesión    
            suscrito = False
            user_actual = None
            print('\nSuscripción Cancelada')
            input('\nPresiona Enter para volver...')
            return True

        elif confirmar == 'no':
            return

        else:
            print('\nRespuesta inválida. Escribe si o no')


# MENÚ DE SUSCRIPCIÓN
# =========================================

def menu_suscrip():
    if suscrito:
        
        while True:
            nombre = usuarios.get(user_actual, 'Desconocido')

            print('\n' + '=' * 30)
            print('         Suscrito/a ❤')
            print('=' * 30)
            print(f'Usuario: {nombre}')
            print(f'ID: {user_actual}')
            print('\n' + '-' * 30)

            print('1. Cancelar Suscripción')
            print('2. Atrás')

            selecc = pedir_numero('\nElige una opción: ', 1, 2)

            if selecc == 1:
                if canc_suscrip():
                    return

            elif selecc == 2:
                return