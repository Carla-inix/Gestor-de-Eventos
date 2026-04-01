# Arcane Gaming Lounge — Planificador de Eventos

Sistema de gestión de reservas para un gaming lounge, desarrollado como proyecto final del primer semestre de Programación. Permite a los usuarios suscribirse, reservar salas con equipos específicos, gestionar horarios sin conflictos y comprar juegos en una tienda integrada.

---

## Índice

1. [Descripción del dominio](#descripción-del-dominio)
2. [Recursos del sistema](#recursos-del-sistema)
3. [Restricciones implementadas](#restricciones-implementadas)
4. [Estructura del proyecto](#estructura-del-proyecto)
5. [Cómo ejecutar](#cómo-ejecutar)
6. [Funcionalidades](#funcionalidades)
7. [Persistencia de datos](#persistencia-de-datos)
8. [Archivo de datos de ejemplo](#archivo-de-datos-de-ejemplo)
9. [Desafíos opcionales implementados](#desafíos-opcionales-implementados)

---

## Descripción del dominio

El dominio elegido es un **gaming lounge** llamado **Arcane**, un local de entretenimiento con salas equipadas para diferentes tipos de experiencias de videojuegos. Los clientes se registran como usuarios y pueden reservar salas por bloques de tiempo, eligiendo los equipos que necesitan para su sesión.

Se eligió este dominio porque refleja un problema real de gestión de recursos: los equipos físicos (mandos, sillas, visores) son finitos y compartidos entre salas, y los horarios no pueden superponerse. Esto hace que la lógica de conflictos y restricciones sea genuinamente necesaria y no artificial.

---

## Recursos del sistema

El sistema gestiona dos tipos de recursos: **salas** y **equipos físicos**.

### Salas (Eventos)

| Sala | Capacidad | Equipos requeridos |
|---|---|---|
| Arca: Consolas I | 8 personas | Mandos, Sillas o Sofás |
| Arca: Consolas II | 8 personas | Mandos, Sillas o Sofás |
| Arca: PCs | 6 personas | Sillas, Audífonos |
| Arca: Realidad Virtual | 6 personas | Visores RV, Mandos RV (opc.), Caminadoras RV (opc.) |

### Inventario de equipos (Pools de recursos)

| Recurso | Stock total |
|---|---|
| Sillas | 20 |
| Sofás | 10 |
| Mandos (consola) | 20 |
| Audífonos | 24 |
| Visores RV | 20 |
| Mandos RV | 20 |
| Caminadoras RV | 12 |

Cada recurso tiene una cantidad disponible. El sistema descuenta las unidades al confirmar una reserva y las libera automáticamente cuando la reserva termina.

---

## Restricciones implementadas

### 1. Restricción de Co-requisito — Sala de Realidad Virtual

**Regla:** Si se solicita una caminadora RV, es obligatorio solicitar también un mando RV, y viceversa. No tiene sentido usar la caminadora sin el mando que la controla, ni el mando sin la caminadora que amplifica el movimiento.

**Implementación en código (`reservas.py`):**
```python
if (mandos_rv > 0 and caminadoras == 0) or (caminadoras > 0 and mandos_rv == 0):
    print('Para usar una caminadora RV necesitas también un mando RV, y viceversa')
    continue
```

**Ejemplo válido:** 2 visores + 2 mandos RV + 2 caminadoras ✅  
**Ejemplo inválido:** 2 visores + 1 caminadora + 0 mandos RV ❌

---

### 2. Restricción de Exclusión Mutua — Salas de Consolas

**Regla:** En una sesión de consolas, el grupo debe elegir entre usar **sillas** o **sofás**, no ambos al mismo tiempo. El mobiliario de la sala está organizado por zonas y mezclarlos genera conflictos de espacio.

**Implementación en código (`reservas.py`):**
```python
tipo_asiento = pedir_numero('Usarán sillas (1) o sofás (2)? ', minimo=1, maximo=2)
if tipo_asiento == 1:
    # se asignan sillas
elif tipo_asiento == 2:
    # se asignan sofás
```

**Ejemplo válido:** 4 sofás + 4 mandos ✅  
**Ejemplo inválido:** 2 sillas + 1 sofá + 3 mandos ❌

---

## Estructura del proyecto

```
arcane-gaming-lounge/
│
├── main.py                  # Punto de entrada — ejecutar este archivo
├── README.md
├── datos/
│   └── estado_app.json
│   └── estado_ejemplo.json  # Datos de ejemplo del sistema
│
└── funciones/
    ├── __init__.py          # Marca la carpeta como paquete Python
    ├── estado.py            # Variables globales compartidas (reservas, tiempo)
    ├── datos.py             # Catálogo de salas y juegos (datos estáticos)
    ├── inputs.py            # Función reutilizable para validar entradas
    ├── horarios_r.py        # Lógica de tiempo: disponibilidad y conflictos
    ├── recursos_r.py        # Gestión del inventario de equipos
    ├── juegos.py            # Lógica de selección de juegos para consolas
    ├── reservas.py          # Flujo completo de creación de una reserva
    ├── mis_reservas.py      # Ver y cancelar reservas del usuario
    ├── suscripcion.py       # Registro de usuarios y gestión de sesión
    ├── ofertas.py           # Sistema de cupones por reservas acumuladas
    ├── tienda_arcane.py     # Tienda de compra de juegos físicos
    ├── menu.py              # Menú principal y enrutamiento de opciones
    └── persistencia.py      # Guardar y cargar estado en JSON
```

---

## Cómo ejecutar

### Requisitos

- Python 3.10 o superior (se usan f-strings con comillas anidadas)
- No se requieren librerías externas

### Pasos

```bash
# 1. Clonar el repositorio
git 
cd 

# 2. Ejecutar el programa
python main.py
```

El programa carga automáticamente el estado guardado si existe `estado_app.json`. Si no existe, inicia desde cero.

Para probar el sistema con datos de ejemplo, copia el archivo de ejemplo:
```bash
cp datos/estado_ejemplo.json datos/estado_app.json
python main.py
```

---

## Funcionalidades

### Reservar una sala
El usuario selecciona sala, cantidad de personas, equipos, juegos (si aplica), fecha y hora. El sistema valida automáticamente:
- Que haya equipos disponibles en el inventario. Si sillas o sofás se agotan en salas de consolas, el sistema asigna el disponible automáticamente. Si ambos se agotan, la sala no puede reservarse. Si mandos RV o caminadoras RV se agotan, ambos quedan fuera por co-requisito y se pregunta si desea continuar sin ellos
- Que no haya conflicto de horario en esa sala
- Que el usuario no tenga otra reserva solapada
- Que se respeten las restricciones de co-requisito y exclusión mutua

### Búsqueda automática de horarios
Si una fecha está completamente ocupada, el sistema sugiere automáticamente el próximo bloque de tiempo disponible para esa sala.

### Mis Reservas
Lista todas las reservas activas del usuario con detalles completos. Permite cancelar una, varias (separadas por coma) o todas a la vez. Al cancelar, los recursos se liberan inmediatamente.

### Suscripción
Los usuarios se registran con nombre y carnet de identidad. Sin suscripción activa no es posible reservar ni comprar. Al cancelar la suscripción, todas las reservas del usuario se eliminan.

### Tienda Arcane
Permite comprar copias físicas de juegos con estas restricciones:
- Máximo 3 compras por día
- Máximo 3 copias del mismo juego por usuario
- Stock limitado por juego

### Ofertas
Sistema de cupón de descuento: al acumular 5 reservas en el historial, el usuario desbloquea un cupón de 20% de descuento aplicable a su siguiente reserva.

### Guardar y Salir
Al elegir esta opción, el estado completo de la aplicación (reservas, inventario, usuarios, compras) se serializa y guarda en `estado_app.json`. Al iniciar el programa de nuevo, este estado se restaura automáticamente.

---

## Persistencia de datos

Todo el estado se guarda en un único archivo `estado_app.json`. El archivo es ignorado en Git (.gitignore) para evitar conflictos. El desafío técnico principal es la **serialización**: Python maneja fechas como objetos `datetime`, pero JSON solo acepta texto, números y listas.

La solución implementada convierte las fechas a texto al guardar (`strftime`) y las reconstruye al cargar (`strptime`). Los objetos de sala también se guardan como texto (su nombre) y se reconstruyen buscando la sala correspondiente en el catálogo.

Si el archivo está corrupto o tiene un formato incompatible, el programa lo detecta y arranca limpio en lugar de crashear.

---

## Archivo de datos de ejemplo

El archivo `estado_ejemplo.json` contiene:
- 2 usuarios registrados (Carlos y Maria)
- 1 reserva activa
- 1 compra en la tienda
- Stock de juegos con una unidad ya vendida

Muestra el formato completo de todos los campos del sistema y puede usarse como referencia para entender la estructura de datos.

---

## Desafíos opcionales implementados

### ✅ Recursos con cantidad (Pools de recursos)
En lugar de modelar cada equipo como un ítem único ("Mando 1", "Mando 2"...), el sistema gestiona los recursos como cantidades disponibles. La lógica de conflictos verifica si quedan unidades suficientes, no solo si el recurso está "libre u ocupado".

### ✅ Modo de prueba con simulación de tiempo
Accesible desde el menú principal (opción 7), permite avanzar el reloj del sistema por horas para probar la liberación automática de reservas vencidas sin esperar en tiempo real.
