import suscripcion

juegos_disponibles = {
    1: {'nombre': 'FIFA 24', 'precio': 350, 'stock': 3},
    2: {'nombre': 'Assasind Cread: Black Flad', 'precio': 500, 'stock': 2},
    3: {'nombre': 'Spider-Man 2', 'precio': 500, 'stock': 2},
    4: {'nombre': 'Mario Kart 8', 'precio': 400, 'stock': 3},
    5: {'nombre': 'Bramble', 'precio': 500, 'stock': 2},
    6: {'nombre': 'Resident Evil 4 remake', 'precio': 600, 'stock': 1}
}
# Total de juegos: 13

# Compras realizadas por el usuario
compras_usuarios = {}

def comprar_juegos():
    print('\nJuegos Disponibles\n')

    for num, juego in juegos_disponibles.items():
        if juego['stock'] > 0:
            print(f'{num}. {juego['nombre']} - {juego['precio']}$ | Stock: {juego['stock']}')

    print('\n0. Atras')

    selecc = input('Elige una opción: ').strip()

    if selecc == '1':
        comprar_juegos()
    elif selecc == '2':
        mostrar_mis_compras()
    elif selecc == '3':
        return
    else:
        print('Opción inválida')
            
            
def comprar_juegos():
    while True:
        print('\n     Juegos Disponibles\n')

        for num, juego in juegos_disponibles.items():
            if juego['stock'] > 0:
                print(f'{num}. {juego['nombre']} - {juego['precio']}$ | Stock: {juego['stock']}')
            else:
                print(f'{num}. {juego['nombre']} - AGOTADO')
        
        print('\n0. Atras')
        selecc = input('Selecciona un juego: ').strip()

        if selecc == '0':
            return

        if not selecc.isdigit():
            print('Opcion invalida')
            continue

        if len(selecc) > 1 and selecc.startswith('0'):
            print('No se permiten ceros al inicio')
            continue

        selecc = int(selecc)

        if selecc not in juegos_disponibles:
            print('Juego inválido')
            continue

        juego = juegos_disponibles[selecc]

        if juego['stock'] == 0:
            print('Este juego ya no está disponible')
            return

        cantidad = input('Cantidad a comprar: ').strip()

        if not cantidad.isdigit():
            print('Cantidad inválida')
            continue

        cantidad = int(cantidad)

        if cantidad <= 0:
            print('Cantidad inválida')
            continue

        if cantidad > juego['stock']:
            print('No hay suficiente stock')
            continue

        total = cantidad * juego['precio']

        confirmar = input(f'Total {total}$. \nConfirmar compra? si/no: ').lower()

        if confirmar != 'si':
            print('Compra cancelada')
            return

        juego['stock'] -= cantidad

        # Guardar compra
        user = suscripcion.user_actual
        compras_usuarios.setdefault(user, []).append({
            'juego': juego['nombre'],
            'cantidad': cantidad,
            'total': total
        })

        print('Compra realizada con éxito!')
        return
    
    
def mostrar_mis_compras():
    user = suscripcion.user_actual

    print('\n   Mis Compras\n')

    if user not in compras_usuarios or not compras_usuarios[user]:
        print('No has realizado compras')
        input('\nPresiona Enter para volver...')
        return

    for compra in compras_usuarios[user]:
        print(f'{compra['juego']} x{compra['cantidad']} = {compra['total']}$')
        print('-' * 30)

    input('\nPresiona Enter para volver...')