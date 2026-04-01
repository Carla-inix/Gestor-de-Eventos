from datetime import datetime

# Tiempo de referencia del sistema
tiempo_actual = datetime.now()

# Lista de reservas activas en este momento
reservas_activas = []

# Historial completo de reservas ,incluyendo las terminadas
historial_reservas = []

# Índices de juegos de consola que están reservados actualmente
juegos_reservados = set()