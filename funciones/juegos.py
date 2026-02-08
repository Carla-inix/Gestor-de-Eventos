from estado import reservas_activas, juegos_reservados
from datos import juegos_consola


def selecc_juegos(juegos_consola):
    while True:
        print('\nElije hasta 3 juegos:\n')
        disponibles = [
            juego for i, juego in enumerate(juegos_consola)
            if i not in juegos_reservados
        ]

        if not disponibles:
            print('\nNo quedan juegos disponibles')
            return []

        for i, juego in enumerate(disponibles, 1):
            print(f'{i}. {juego}')

        selecc = input('\nEscribe los números separados por coma o atras para volver: ').strip()
        
        if selecc == 'atras':
            return None
        
        # Prohibir ceros iniciales
        if any(x.startswith('0') and len(x) > 1 for x in  selecc.split(',')):
            print('\nNo se permiten ceros al inicio. Intenta de nuevo\n')
            continue

        partes = [x.strip() for x in  selecc.split(',')]
        if any(not x.isdigit() for x in partes):
            print('\nEntrada inválida\n')
            continue

        idxs = [int(x) - 1 for x in partes]
        if any(i < 0 or i >= len(disponibles) for i in idxs):
            print('\nElige una de la opciones disponibes\n')
            continue

        if len(set(idxs)) != len(idxs):
            print('\nNo repitas juegos\n')
            continue

        if len(idxs) > 3:
            print('\nMáximo 3 juegos\n')
            continue

        seleccionados = []
        for i in idxs:
            idx_global = juegos_consola.index(disponibles[i])
            seleccionados.append(idx_global)

        juegos_reservados.update(seleccionados)
        
        return [juegos_consola[i] for i in seleccionados]
    
    
def validar_juegos():
    return len(juegos_reservados) < len(juegos_consola)
    
    
def prox_liberacion_juegos():
    fechas = [
        r['fin'] for r in reservas_activas
        if 'Consolas' in r['sala']['nombre'] and r['juegos']
    ]
    return min(fechas) if fechas else None