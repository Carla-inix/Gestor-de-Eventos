import json
import os
from datetime import datetime
from . import estado
from .datos import salas
from .tienda_arcane import juegos_disponibles, compras_usuarios
from . import suscripcion


ARCHIVO_ESTADO = 'datos/estado_app.json'


# Serializar reservas: datetime - texto, objeto sala - nombre (str)
def guardar_estado():
    reservas_serializadas = []
    for r in estado.reservas_activas:
        reservas_serializadas.append({
            'usuario': r['usuario'],
            'sala': r['sala']['nombre'],
            'inicio': r['inicio'].strftime('%d-%m-%Y | %H:%M'),
            'fin': r['fin'].strftime('%d-%m-%Y | %H:%M'),
            'horas': r['horas'],
            'personas': r['personas'],
            'juegos': r['juegos'],
            'recursos': r['recursos'],
            'costo': r['costo'],
            'descuento': r['descuento'],
        })
        
    historial_serializado = []

    for r in estado.historial_reservas:
        historial_serializado.append({
            'usuario': r['usuario'],
            'sala': r['sala']['nombre'] if isinstance(r['sala'], dict) else r['sala'],
            'inicio': r['inicio'].strftime('%d-%m-%Y | %H:%M') if hasattr(r['inicio'], 'strftime') else r['inicio'],
            'fin': r['fin'].strftime('%d-%m-%Y | %H:%M') if hasattr(r['fin'], 'strftime') else r['fin'],
            'horas': r.get('horas'),
            'personas': r.get('personas'),
            'juegos': r.get('juegos'),
            'recursos': r.get('recursos'),
            'costo': r.get('costo'),
            'descuento': r.get('descuento'),
        })

    # Serializar compras: datetime - texto
    compras_serializadas = {}
    
    for user, compras in compras_usuarios.items():
        compras_serializadas[str(user)] = [
            {**c, 'fecha': c['fecha'].strftime('%d-%m-%Y | %H:%M')}
            for c in compras
        ]

    datos = {
        'tiempo_actual': estado.tiempo_actual.strftime('%d-%m-%Y | %H:%M'),

        'reservas': {
            'reservas_activas': reservas_serializadas,
            'juegos_reservados': list(estado.juegos_reservados),
            'historial_reservas': historial_serializado
        },

        'tienda': {
            'juegos_disponibles': juegos_disponibles,
            'compras_usuarios': compras_serializadas
        },

        'usuarios': {
            'user_actual': suscripcion.user_actual,
            'usuarios': {str(k): v for k, v in suscripcion.usuarios.items()},
            'suscrito': suscripcion.suscrito,
            'cupon_disponible': suscripcion.cupon_disponible,
            'cupon_usado': suscripcion.cupon_usado,
        }
    }

    with open(ARCHIVO_ESTADO, 'w', encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

    print('\nEstado guardado')


#Carga el estado desde estado_app.json
def cargar_estado():
    if not os.path.exists(ARCHIVO_ESTADO):
        return

    try:
        with open(ARCHIVO_ESTADO, 'r', encoding='utf-8') as f:
            datos = json.load(f)

        # Restaurar tiempo del sistema
        estado.tiempo_actual = datetime.strptime(datos['tiempo_actual'], '%d-%m-%Y | %H:%M')

        # Restaurar reservas: texto - datetime, nombre de sala - objeto sala
        estado.reservas_activas.clear()
        for r in datos['reservas']['reservas_activas']:
            sala_obj = next((s for s in salas if s['nombre'] == r['sala']), None)
            
            if sala_obj is None:
                continue
            
            r['inicio'] = datetime.strptime(r['inicio'], '%d-%m-%Y | %H:%M')
            r['fin'] = datetime.strptime(r['fin'],    '%d-%m-%Y | %H:%M')
            r['sala'] = sala_obj
            
            estado.reservas_activas.append(r)

        # Restaurar juegos reservados
        estado.juegos_reservados.clear()
        estado.juegos_reservados.update(datos['reservas']['juegos_reservados'])
        
        estado.historial_reservas = datos['reservas'].get('historial_reservas', [])

        # Restaurar tienda
        juegos_disponibles.clear()
        juegos_disponibles.extend(datos['tienda']['juegos_disponibles'])

        compras_usuarios.clear()
        for user_str, compras in datos['tienda']['compras_usuarios'].items():
            for c in compras:
                c['fecha'] = datetime.strptime(c['fecha'], '%d-%m-%Y | %H:%M')
                
            compras_usuarios[int(user_str)] = compras

        # Restaurar usuario y estado de suscripción
        suscripcion.user_actual = datos['usuarios']['user_actual']
        suscripcion.usuarios = {int(k): v for k, v in datos['usuarios']['usuarios'].items()}
        suscripcion.suscrito = datos['usuarios']['suscrito']
        suscripcion.cupon_disponible = datos['usuarios']['cupon_disponible']
        suscripcion.cupon_usado = datos['usuarios']['cupon_usado']


    # Si el archivo está corrupto o con formato incorrecto, arrancar de cero
    except (KeyError, ValueError, json.JSONDecodeError):
        print('\nArchivo de estado corrupto o incompatible. Iniciando desde cero')