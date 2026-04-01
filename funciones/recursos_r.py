from . import estado
from .datos import juegos_consola

recursos_stock = {
    'sillas': 20,
    'sofas': 10,
    'mandos': 20,
    'audifonos': 24,
    'mandos_rv': 20,
    'visores_rv': 20,
    'caminadora_rv': 12
}

RECURSOS_MIN_SALA = {
    'Consolas': {'mandos': 1},
    'PCs': {'sillas': 1, 'audifonos': 1},
    'Realidad Virtual': {'visores_rv': 1}
}

recursos_en_uso = {
    'sillas': 0,
    'sofas': 0,
    'mandos': 0,
    'audifonos': 0,
    'mandos_rv': 0,
    'visores_rv': 0,
    'caminadora_rv': 0
}


#Verifica si hay recursos mínimos disponibles para reservar una sala
#Devuelve (True, None) si hay disponibilidad, o (False, fecha_liberacion) si no la hay
def validar_dispo_recursos(sala):
    
    # Determinar el tipo de sala según su nombre
    for tipo in RECURSOS_MIN_SALA:
        if tipo in sala['nombre']:
            recursos_minimos = RECURSOS_MIN_SALA[tipo]
            break
    else:
        return True, None

    # Comprobar stock total
    faltantes = {}
    for r, minimo in recursos_minimos.items():
        disponibles = recursos_stock.get(r, 0) - recursos_en_uso.get(r, 0)
        if disponibles < minimo:
            faltantes[r] = minimo - disponibles

    if not faltantes:
        return True, None

    # Busca la fecha más cercana de liberación
    prox_fechas = []
    for reserva in estado.reservas_activas:
        for r in faltantes:
            if r in reserva.get('recursos', {}):
                prox_fechas.append(reserva['fin'])

    if prox_fechas:
        return False, min(prox_fechas)

    return False, None


#Cancela una reserva y libera todos los recursos y juegos asociados   
def cancelar_reserva(reserva):
    
    # Libera juegos si es de las salas de consolas
    if 'Consolas' in reserva['sala']['nombre']:
        for juego in reserva['juegos']:
            idx = juegos_consola.index(juego)
            estado.juegos_reservados.discard(idx)

    # Eliminar la reserva
    if reserva in estado.reservas_activas:
        estado.reservas_activas.remove(reserva)

    # Libera los recursos
    for r, c in reserva.get('recursos', {}).items():
        recursos_en_uso[r] -= c
    
#Revisa todas las reservas activas y elimina las que ya han terminado    
def liberar_reservas():
    terminadas = []

    for reserva in estado.reservas_activas[:]:
        if estado.tiempo_actual >= reserva['fin']:
            terminadas.append(reserva)

    for r in terminadas:
        cancelar_reserva(r)

    return len(terminadas)


def consumir_recursos(recursos_usados):
    for r, c in recursos_usados.items():
        recursos_en_uso[r] += c