from . import suscripcion
from . import estado


def contar_reservas_usuario(id_usuario):
    contador = 0
    for reserva in estado.historial_reservas:
        if reserva.get('usuario') == id_usuario:
            contador += 1
            
    return contador


def mostrar_ofertas():
    print('\n' + '=' * 40)
    print('          Ofertas Disponibles')
    print('=' * 40)

    if suscripcion.user_actual is None:
        print('Debes suscribirte primero')
        input('\nPresiona Enter para volver...')
        return

    total = contar_reservas_usuario(suscripcion.user_actual)

    print('Cupón para nuevos usuarios⭐:')
    print('Reserva 5 veces y obtén un cupón del 20% de descuento\n')

    print(f'Reservas realizadas: {total}')

    if suscripcion.cupon_usado:
        print('Cupón utilizado⭕')
        
    elif total >= 5:
        suscripcion.cupon_disponible = True
        print('Cupón DISPONIBLE (20%)')
        
    else:
        print(f'Te faltan {5 - total} reservas para desbloquear el cupón')

    input('\nPresiona Enter para volver al menú...')