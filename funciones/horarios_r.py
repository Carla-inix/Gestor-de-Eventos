from datetime import datetime, timedelta
from inputs import pedir_numero
from estado import tiempo_actual, reservas_activas
from recursos_r import liberar_reservas


def obtener_horas_dispo(fecha, sala):
    horas_disponibles = []

    for h in range(9, 23): 
        inicio = fecha.replace(hour=h, minute=0)
        fin = inicio + timedelta(hours=1)

        ocupada = False
        for reserva in reservas_activas:
            if reserva['sala'] == sala:
                if inicio < reserva['fin'] and fin > reserva['inicio']:
                    ocupada = True
                    break

        if not ocupada:
            horas_disponibles.append(h)

    return horas_disponibles


def buscar_prox_horario(sala, duracion, dias_max=8):
    base = tiempo_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    
    for d in range(dias_max):
        fecha = base + timedelta(days=d)
        horas_disp = obtener_horas_dispo(fecha, sala)
        
        if d == 0 and tiempo_actual.hour >= 22:
            continue
        
        for h in horas_disp:
            if h + duracion > 23:
                continue
            
            horas_necesarias = range(h, h + duracion)
            if all(x in horas_disp for x in horas_necesarias):
                inicio = fecha.replace(hour=h, minute=0)
                fin = inicio + timedelta(hours=duracion)
                return inicio, fin
            
    return None 


def pedir_duracion(hora_inicio, horas_disponibles):
    while True:
        horas = pedir_numero('Cuántas horas reservará? (1-5): ', minimo=1, maximo=5, atras=True)
        
        if horas == 'atras':
            return None

        if hora_inicio + horas > 23:
            print('\nEl horario excede las 23:00\n')
            continue

        horas_necesarias = range(hora_inicio, hora_inicio + horas)
        if not all(h in horas_disponibles for h in horas_necesarias):
            print('\nEsa duración invade un horario no disponible\n')
            continue

        return horas
    
    
def solapamiento_reserva(inicio1, fin1, inicio2, fin2):
    return inicio1 < fin2 and inicio2 < fin1


def usuario_ocupado(usuario, inicio, fin):
    for reserva in reservas_activas:
        if reserva['usuario'] == usuario:
            if solapamiento_reserva(inicio, fin, reserva['inicio'], reserva['fin']):
                return True
            
    return False


#FUNCIÓN DE SIMULACIÓN (TEST)
#=======================================
                
def avanzar_tiempo (horas=1):
    global tiempo_actual
    tiempo_actual += timedelta(hours=horas)
    print(f'\nTiempo avanzado {horas} horas. Hora actual: {tiempo_actual.strftime('%d-%m-%Y | %H:%M')}')
    
    liberadas = liberar_reservas()
        
    if liberadas:
        print(f'\nSe liberaron {liberadas} reservas')
    else:
        print('\nNo hay reservas que hayan terminado aún')
        
def reset_tiempo():
    global tiempo_actual, reservas_activas, juegos_reservados
    tiempo_actual = datetime.now()
    reservas_activas = []
    juegos_reservados.clear()
    print('\nSistemas reiniciados')