usuarios = {}
suscrito = False
user_actual = None

def suscrip ():
    global suscrito, user_actual
    
    while True:
        nombre = input('Nombre: ').strip()
        if not nombre:
            print('Tu nombre no puede estar vacio')
            continue
        
        while True:
            carnet_str = input('Ingrese su carnet de identidad: ')
            try:
                id_user = int(carnet_str)
                break
            except ValueError:
                print('Deben ser numeros enteros .Prueba otra vez')
            
        if id_user in usuarios:
            print('Ese ID ya existe, ingrese otro')
            continue
            #Guarda los datos en el diccionario
        usuarios[id_user] = nombre
        suscrito = True
        user_actual = id_user
        print('Ya estas suscrito!!')
        
        print('[DEBUG] susc despues de asignar', suscrito)
        return True
        
#Cancelar Suscripcion

def canc_suscrip():
    global suscrito, user_actual
    
    while True:
        try:
            id_cancel = int(input('Ingresa tu carnet para cancelar: '))
            if id_cancel in usuarios:
                nombre = usuarios.pop(id_cancel)
                suscrito = False
                user_actual = None
                print('Suscripcion Cancelada')
                return True
            
            else:
                print('ID no encontrado')
        except ValueError:
            print('Ingresa un numero valido')
            

def menu_suscrip():
    if suscrito:
        
        while True:
            print('\n\tSuscrito\n')
            print('1. Cancelar Suscripcion')
            print('2. Atras')
            selecc = input('Elige una opcion: ').strip()
            
            if selecc == '1':
                if canc_suscrip():
                    return
                else:
                    print('No se pudo cancelar')
            elif selecc == '2':
                print('\nVolviendo al menu principal...')
                return
            else:
                print('Opcion invalida, elige 1 o 2')