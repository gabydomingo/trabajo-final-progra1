#gabriel domingo- 1168660
#tobias alfonso- 1169215
#lautaro papaianni- 1170805
#santino lozano- 1173470

import os
from random import randint
from tabulate import tabulate
def mostrar_menu() -> None:
    """ Muestra y recorre el menu del sistema.

        type menu: tuple.
        pre: El contenido de menu debe ser str.
        post: Imprime el recorrido de menu.
        return: None

    """
    menu = ('1-Mostrar Menu Completo','2-Realizar Pedido','3-Buscar x comida dentro del Menu','4-Buscar x categoria en el menu','5-Pagar mesa','S para salir')
    print('---------Menu---------')
    for elem in menu:
        print(elem)
    return
def menu() -> None:
    """ Invoca la funcion 'mostrar_menu()' y Solicita a un usuario ingresar una opcion, validando la misma.
        Ejecuta las funciones.

        pre: Las opciones se manejan como string.
        post: Entra en la funcion asignada a cada opcion.
    """
    while True:
        mostrar_menu()
        op = input('Ingrese que pocion quiere realizar: ')
        print('')
        if op.lower() == 's' and op in tuple("12345s"):
            print('Adios, Vuelva Pronto.')
            return
        elif op == '1':
            mostrar_menu_comida()
        elif op == '2':
            hacer_pedido()
        elif op == '3':
            buscar_x_nombre()
        elif op == '4':
            buscar_x_categoria()
        elif op == '5':
            cobro()
        else:
            print('ERROR! Ingrese una opcion valida.\n')
    return

def mostrar_menu_comida() -> None:
    """ Lee el csv.
        Separa del mismo el cuerpo del encabezado.

        pre: debe existir un archivo.csv con datos.
        post: Muestra por pantalla el cuerpo ordenado del archivo, el cual contiene la carta completa
    """
    try:
        with open('menu.csv', 'rt', encoding='utf-8') as arch:
            encabezado = arch.readline()
            lineas = tabulate([linea.rstrip().split(';') for linea in arch])
    except Exception as e:
        print(f'El error es: {e}')
    else:
        print(lineas)
    return

def hacer_pedido() -> None:
    """ Muestra las mesas y carga los pedidos en las mismas

        type mesas: dict
        pre: Se recorre el diccionario con las mesas y se pide al usuario ingresar un de las disponibles
        post: Se exporta un csv con el numero de la mesa y el contenido de la misma

    """
    print(f'Las mesas disponibles son:', end=' ')
    for elem in mesas.keys():
        print(elem, end= ' ')
    elegir_mesa = input('Ingrese el número de mesa que usted quiera: ')
    if elegir_mesa.isalnum() and elegir_mesa in mesas.keys():
        while True:
            pedido = input('Ingrese lo que quiera pedir (0 para salir): ')
            if pedido == '0':
                try:
                    with open(f'pedido_mesa{elegir_mesa}.csv', 'rt', encoding= 'utf-8') as arch2:
                        if arch2:
                            for linea in arch2:
                                lineas = linea.rstrip().split(';')
                                mesas[elegir_mesa].append(lineas)
                    print('Su pedido fue exitoso')
                    return
                except Exception as e:
                    print(f"El error es {e}")
            else:
                try:
                    with open('menu.csv', 'rt', encoding='utf-8') as arch:
                        encabezado = arch.readline()
                        for linea in arch:
                            if linea.split(';')[0] == pedido:
                                with open(f'pedido_mesa{elegir_mesa}.csv', 'at', encoding= 'utf-8') as arch2:
                                    arch2.write(linea)
                                break
                except Exception as e:
                    print(f"El error es {e}")
    else:
        print('Ingrese una mesa valida para comenzar con su pedido')
    return

def pagar(total: int, mesa_cobrar: str) -> None:
    """ Abre el Archivo de la mesa que se le pasa como parametro y lo elimina.
        Informa con que medio se realizara el pago y de ser credito se le suma un extra.

        Param:
            total: numero de monto a pagar.
            mesa_cobrar: nombre de la mesa seleccionada.
        Type total: int.
        Type mesa_cobrar: str.
        Tre: Debe haber un archivo creado con el nombre de esa mesa y datos cargados.
        Post: borra el csv seleccionado, y cobra la mesa.
    """
    try:
        with open(f"pedido_mesa{mesa_cobrar}.csv", "w", encoding= "utf-8-sig") as archivo:
            os.remove(f"pedido_mesa{mesa_cobrar}.csv")
    except Exception as e:
        print(f"El error es {e}")
    pago = input('ingrese con que abonar E (Efectivo) o T (Tarjeta): ')
    if pago.lower() == 'e':
        print(f'Pase por caja para pagar. Muchas Gracias, vuelva pronto')
        return
    elif pago.lower() == 't':
        tarjeta = input('Ingrese con que tarjeta D (Debito) o C (Credito + 10%): ')
        if tarjeta.upper() == 'D':
            print('Su pago a sido recibido con exito. Muchas Gracias, vuelva pronto')
            return
        elif tarjeta.upper() == 'C':
            try:
                total_credito = int(total) * 1.10
            except Exception as e:
                print(f'Ha ocurrido un error: {e}')
            else:
                print(f'El monto total sería ${round(total_credito)}')
                print(f'Su pago a sido recibido con exito. Muchas Gracias, vuelva pronto')
                return        

def cobro() -> None:
    """ Solicita una mesa y la busca en el diccionario, validando que tenga datos cargados.

        Pre: el usuario ingresa una mesa y esta debe estar con datos y en el diccionario de mesas.
        Post: ingresa en la funcion pagar(total, mesa_cobrar).
    """
    mesa_cobrar = input('Ingrese la mesa: ')
    if mesa_cobrar in mesas.keys():
        total = 0
        try:
            with open(f'pedido_mesa{mesa_cobrar}.csv', 'rt', encoding= 'utf-8') as arch:
                print('Su pedido es: ')
                for lista in arch:
                    listas = lista.rstrip().split(';')
                    print(f'{listas[1]} ---- ${listas[3]}')
                    total += int(listas[3])
        except FileNotFoundError as file:
            print('No se encuentra un pedido para la mesa ingresada.')
        except Exception as e:
            print(f'ERROR! = {e}')
        else:
            print(f'El total de su pedido es de ${total}\n')
            print('¿Como deseará abonar?')
            pagar(total, mesa_cobrar)
    return

def buscar_x_nombre() -> None:
    """ Busca un plato o bebida por su nombre(str) y muestra todas las coincidencias que aranquen con el mismo nombre.

        Pre: Debe leer el menu y recibir lo que le ingreso el usuario.
        Post: Devuelve una matriz de los elementos que sean igual a lo que ingreso el usuario.
    """
    try:
        with open('menu.csv', 'rt', encoding='utf-8') as arch:
            busqueda = input('Ingrese lo que quiera buscar especificamente en en menu: ')
            busq = tabulate([linea.rstrip().split(';') for linea in arch if linea.split(';')[1].lower().startswith(busqueda)])
            print(busq)
    except Exception as e:
        print(f'Ta Mal por esto: {e}')
    return

def buscar_x_categoria() -> None:
    """ Imprime todos los elementos de la categoria informada por el usuario.

        Pre: debe leer el menu y recibir lo que le ingreso el usuario.
        Post: devuelve una matriz con todos los elementos de la categoria informada por el archivo.
    """
    try:
        with open('menu.csv', 'rt', encoding='utf-8-sig') as arch:
            busqueda = input('Ingrese la categoría que quieras buscar: ')
            busq = tabulate([linea.rstrip().split(';') for linea in arch if linea.split(';')[2].lower().startswith(busqueda)])
            print(busq)
    except Exception as e:
        print(f'El error es {e}')
    return

mesas = {f'{_}': [] for _ in range(1, 13)}
if __name__ == '__main__':
    menu()

