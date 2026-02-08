def pedir_numero(mensaje, minimo=None, maximo=None, atras=False):

    while True:
        valor = input(mensaje).strip().lower()

        if atras and valor == 'atras':
            return 'atras'

        if valor == '':
            print('\nDebes ingresar un número')
            continue

        if not valor.isdigit():
            print('\nIngresa solo números válidos')
            continue

        if valor != str(int(valor)):
            print('\nNúmero inválido')
            continue

        numero = int(valor)

        if minimo is not None and numero < minimo:
            print(f'\nEl valor mínimo es {minimo}\n')
            continue

        if maximo is not None and numero > maximo:
            print(f'\nEl valor máximo es {maximo}\n')
            continue

        return numero