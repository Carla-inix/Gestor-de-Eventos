import json
from datetime import datetime
from estado import reservas_activas, juegos_reservados, tiempo_actual
from tienda_arcane import juegos_disponibles, compras_usuarios
import suscripcion


def guardar_estado():
    estado = {
        'tiempo_actual': tiempo_actual.strftime('%d-%m-%Y | %H:%M'),

        'reservas': {
            'reservas_activas': reservas_activas,
            'juegos_reservados': list(juegos_reservados)
        },

        'tienda': {
            'juegos_disponibles': juegos_disponibles,
            'compras_usuarios': compras_usuarios
        },

        'usuarios': {
            'usuario_actual': suscripcion.user_actual,
            'suscripciones_activas': list(suscripcion.suscripciones_activas)
        }
    }

    with open('estado_app.json', 'w', encoding='utf-8') as f:
        json.dump(estado, f, indent=4, ensure_ascii=False)
        
        
        
def cargar_estado():
    global tiempo_actual

    with open('estado_app.json', 'r', encoding='utf-8') as f:
        estado = json.load(f)

    # Tiempo
    tiempo_actual = datetime.strptime(
        estado['tiempo_actual'], '%d-%m-%Y | %H:%M'
    )

    # Reservas
    reservas_activas.clear()
    reservas_activas.extend(estado['reservas']['reservas_activas'])

    juegos_reservados.clear()
    juegos_reservados.update(estado['reservas']['juegos_reservados'])

    # Tienda
    juegos_disponibles.clear()
    juegos_disponibles.update(estado['tienda']['juegos_disponibles'])

    compras_usuarios.clear()
    compras_usuarios.update(estado['tienda']['compras_usuarios'])

    # Usuarios
    suscripcion.user_actual = estado['usuarios']['usuario_actual']
    suscripcion.suscripciones_activas.clear()
    suscripcion.suscripciones_activas.extend(
        estado['usuarios']['suscripciones_activas']
    )