from funciones.persistencia import cargar_estado
from funciones.menu import menu_principal


def main():
    try:
        cargar_estado()
    except FileNotFoundError:
        pass

    menu_principal()


if __name__ == '__main__':
    main()