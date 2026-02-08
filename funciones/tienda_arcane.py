import suscripcion
from datetime import datetime
from inputs import pedir_numero

#DATOS
#=======================

juegos_disponibles = [
    {'nombre': 'FIFA 24', 'precio': 350, 'stock': 2, 'descripcion': 'Simulador de fútbol con equipos y ligas oficiales'},
    {'nombre': 'Assassins Creed: Black Flag', 'precio': 500, 'stock': 4, 'descripcion': 'Aventura de piratas con exploración naval y combate'},
    {'nombre': 'Spider-Man 2', 'precio': 500, 'stock': 4, 'descripcion': 'Acción y mundo abierto controlando a Spider-Man'},
    {'nombre': 'Mario Kart 8', 'precio': 400, 'stock': 3, 'descripcion': 'Carreras divertidas con personajes de Nintendo'},
    {'nombre': 'Bramble', 'precio': 500, 'stock': 2, 'descripcion': 'Aventura oscura inspirada en cuentos nórdicos'},
    {'nombre': 'Resident Evil 4 Remake', 'precio': 600, 'stock': 1, 'descripcion': 'Súrvival horror con acción y enemigos aterradores'},
]

# Historial de compras por usuario
compras_usuarios = {}


#FUNCIONES
#========================

def comprar_juegos():
    while True:
        user = suscripcion.user_actual

        # Restricción: máximo 2 compras por día
        if compras_hoy(user, compras_usuarios) >= 2:
            print('\nSolo puedes hacer 2 compras por día\n')
            input('Presiona Enter para volver...')
            return
        
        
        print('\n' + '=' *40)
        print('            Juegos Disponibles')

        for i, juego in enumerate(juegos_disponibles, 1):
            print('=' * 40)
            print(f'{i}. {juego['nombre']}')
            
            if juego['stock'] > 0:
                print(f'Precio: {juego['precio']}$')
                print(f'Stock: {juego['stock']}')
                print(f'Descripción: {juego['descripcion']}')
            else:
                print('AGOTADO⭕')
        
        print('\nAtrás')
        
        selecc = pedir_numero(
            'Selecciona un juego: ',
            minimo=1,
            maximo=len(juegos_disponibles),
            atras=True
        )

        if selecc == 'atras':
            return

        juego = juegos_disponibles[selecc - 1]

        if juego['stock'] == 0:
            print('\nEste juego está agotado')
            continue

        cantidad = pedir_numero(
            '\nCantidad a comprar: ',
            minimo=1,
            maximo=juego['stock'],
            atras=True
        )

        if cantidad == 'atras':
            continue

        costo = cantidad * juego['precio']
        
        # Restricción: máximo 3 copias del mismo juego por usuario
        if copias_compradas(user, juego['nombre']) + cantidad > 3:
            print('\nNo puedes comprar más de 3 copias del mismo juego')
            continue

        while True:    
            confirmar = input(
                f'\nCosto total: {costo}$\nConfirmar compra? si/no: '
            ).lower().strip()

            if confirmar == 'si':
                juego['stock'] -= cantidad

                # Registrar compra
                compras_usuarios.setdefault(user, []).append({
                    'fecha': datetime.now(),
                    'juego': juego['nombre'],
                    'precio': juego['precio'],
                    'cantidad': cantidad,
                    'costo': costo,
                    
                })

                print('Compra realizada con éxito!')
                input('\nPresiona Enter para volver...')
                return
        
            elif confirmar == 'no':
                print('\nCompra cancelada')
                return
            
            else:
                print('\nRespuesta inválida. Escribe si o no\n')


def compras_hoy(usuario, compras_usuarios):
    hoy = datetime.now().date()
    return sum(
        1 for compra in compras_usuarios.get(usuario, [])
        if compra['fecha'].date() == hoy
    )


def mostrar_mis_compras():
    user = suscripcion.user_actual

    print('\n' + '=' * 30)
    print('          Mis Compras')
    print('=' * 30)
    
    if user not in compras_usuarios or not compras_usuarios[user]:
        print('No has realizado compras')
        input('\nPresiona Enter para volver...')
        return

    for compra in compras_usuarios[user]:
        print(f'Fecha: {compra['fecha'].strftime('%d-%m-%Y | %H:%M')}')
        print(f'Juego: {compra['juego']} {compra['precio']}$')
        print(f'Cantidad: {compra['cantidad']}')
        print(f'Costo: {compra['costo']}$')
        print('-' * 30)

    input('\nPresiona Enter para volver...')
    
    
def copias_compradas(user, nombre_juego):
    total = 0
    for compra in compras_usuarios.get(user, []):
        if compra['juego'] == nombre_juego:
            total += compra['cantidad']
    return total


# MENÚ DE LA TIENDA
# ======================================

def menu_tienda():
    if suscripcion.user_actual is None:
        print('\nDebes estar suscrito/a para acceder a la tienda')
        input('\nPresiona Enter para volver...')
        return

    while True:
        print('\n' + '=' * 40)
        print('             Tienda Arcane')
        print('=' * 40)
        print('\n1. Comprar juegos')
        print('2. Ver mis compras')
        print('3. Atrás')

        selecc = pedir_numero('Elige una opción: ', 1,3)

        if selecc == 1:
            comprar_juegos()
            
        elif selecc == 2:
            mostrar_mis_compras()
            
        elif selecc == 3:
            return