from . import estado
from .datos import juegos_consola


#Muestra los juegos disponibles
def selecc_juegos(juegos_consola):
    while True:
        print('\n' + '=' * 40)
        print('\nElije hasta 3 juegos:\n')

        # Filtra los juegos que no están en el set de reservados usando su índice global en el catálogo original
        disponibles = [
            juego for i, juego in enumerate(juegos_consola)
            if i not in estado.juegos_reservados
        ]

        if not disponibles:
            print('\nNo quedan juegos disponibles')
            return []

        for i, juego in enumerate(disponibles, 1):
            print(f'{i}. {juego}')

        selecc = input('\nEscribe los números separados por coma o atras para volver: ').strip()

        if selecc == 'atras':
            return None

        # Valida que no haya ceros iniciales (ej: 007 no es válido)
        if any(x.startswith('0') and len(x) > 1 for x in selecc.split(',')):
            print('\nNo se permiten ceros al inicio. Intenta de nuevo\n')
            continue

        partes = [x.strip() for x in selecc.split(',')]

        # Valida que todo lo ingresado sean números
        if any(not x.isdigit() for x in partes):
            print('\nEntrada inválida\n')
            continue

        idxs = [int(x) - 1 for x in partes]

        # Valida que los números estén dentro del rango mostrado
        if any(i < 0 or i >= len(disponibles) for i in idxs):
            print('\nElige una de las opciones disponibles\n')
            continue

        # Valida que no repita el mismo número dos veces
        if len(set(idxs)) != len(idxs):
            print('\nNo repitas juegos\n')
            continue

        if len(idxs) > 3:
            print('\nMáximo 3 juegos\n')
            continue

        # Traduce los índices de la lista filtrada al índice global del catálogo
        seleccionados = []
        for i in idxs:
            idx_global = juegos_consola.index(disponibles[i])
            seleccionados.append(idx_global)

        # Marca los juegos como reservados para que no aparezcan disponibles
        estado.juegos_reservados.update(seleccionados)

        return [juegos_consola[i] for i in seleccionados]


#Devuelve True si todavía hay al menos un juego sin reservar
def validar_juegos():
    return len(estado.juegos_reservados) < len(juegos_consola)


#Devuelve la fecha más próxima en que se liberará un juego
def prox_liberacion_juegos():
    fechas = [
        r['fin'] for r in estado.reservas_activas
        if 'Consolas' in r['sala']['nombre'] and r['juegos']
    ]
    return min(fechas) if fechas else None