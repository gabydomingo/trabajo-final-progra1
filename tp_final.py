#gabriel domingo- 1168660
#tobias alfonso- 1169215
#lautaro papaianni- 1170805
#santino lozano- 1173470

import os
from typing import List
from random import randint
from tabulate import tabulate
def mostrar_menu() -> None:
    """ Muestra y recorre las opciones del menu del sistema.

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
    """ Valida las opciones y ejecuta las funciones asignadas a cada opcion;

        Pre: Las opciones se manejan como string, el sistema se debe iniciar mostrando la carta.
        post: Entra y ejecuta la funcion asignada a cada opcion.
    """
    carta = False
    while True:
        mostrar_menu()
        op = input('Ingrese que opocion quiere realizar: ')
        print('')
        if op.lower() == 's' and op in tuple("12345s"):
            print('Adios, Vuelva Pronto.')
            return
        elif op == '1':
            carta = True
            lineas, encabezado = mostrar_menu_comida()
            print(tabulate(encabezado + lineas))
        if carta:
            if op == '2':
                hacer_pedido(lineas, encabezado)
            elif op == '3':
                buscar_x_nombre(lineas, encabezado)
            elif op == '4':
                buscar_x_categoria(lineas, encabezado)
            elif op == '5':
                cobro()
        else:
            print('Se debe iniciar mostrando la carta.\n')
    return

def mostrar_menu_comida() -> List[List[str]]:
    """ Lee el csv.
        Separa del mismo el cuerpo del encabezado.

        pre: debe existir un archivo.csv con datos.
        post: convierte el archivo a lista para poder usarse en el sistema
        returns:
                lineas: Una matriz con el archivo sin el primer indice
                encabezado: Una lista que solo contiene el primer indice de la matriz
    """
    try:
        with open('menu.csv', 'rt', encoding='utf-8') as arch:
            lineas = [linea.rstrip().split(';') for linea in arch]
            encabezado = [lineas.pop(0)]
    except Exception as e:
        print(f'El error es: {e}')
    else:
        return lineas, encabezado

def hacer_pedido(lineas, encabezado) -> None:
    """ Muestra las mesas y carga los pedidos en las mismas

        type mesas: dict
        pre: Se recorre el diccionario con las mesas y se pide al usuario ingresar un de las disponibles.
        post: Se exporta un csv con el numero de la mesa y el contenido de la misma, en caso de la mesa estar vacia se informa y sale de la funcion
        argumentos:
                lineas: matriz con el cuerpo del archivo menu.csv
                encabezado: matriz con el encabezado del archivo menu.csv
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
                    with open(f'pedido_mesa{elegir_mesa}.csv', 'rt', encoding= 'utf-8-sig') as arch2:
                        if arch2:
                            for linea in arch2:
                                line = linea.rstrip().split(';')
                                mesas[elegir_mesa].append(line)
                    print('Su pedido fue exitoso')
                    return
                except FileNotFoundError:
                    print(f"Esta mesa no tiene pedidos cargados")
                    return
                except Exception as e:
                    print(f'Error...{e}')
            else:
                pedido_encontrado = False
                for linea in lineas:
                    if pedido in linea[0]:
                        pedido_encontrado = True
                        try:
                            with open(f'pedido_mesa{elegir_mesa}.csv', 'at', encoding= 'utf-8-sig') as arch2:
                                arch2.write(';'.join(linea) + '\n')
                            break
                        except Exception as e:
                            print(f"El error es {e}")
                if not pedido_encontrado:
                    print('El codigo que ingreso esta fuera de rango')
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

def buscar_x_nombre(lineas, encabezado) -> None:
    """ Busca un plato o bebida por su nombre(str) y crea una matriz con todas las coincidencias que aranquen con el mismo nombre.

        Pre: crea una lista por comprension con las coincidencias de la carta y lo que le paso el usuario.
        Post: Si encontro coincidencias de lo que encontro el usuario las guarda, si no deja la lista vacia e informa que no se encontro nada.
        argumentos:
                lineas: matriz con el cuerpo del archivo menu.csv
                encabezado: matriz con el encabezado del archivo menu.csv
    """   
    busqueda = input('Ingrese lo que quiera buscar especificamente en en menu: ')
    busq = [linea for linea in lineas if linea[1].lower().startswith(busqueda)]
    if busq:
        print(tabulate(busq))
    else:
        print('Plato o bebida no encontrados')          
    return

def buscar_x_categoria(lineas, encabezado) -> None:
    """ Busca un plato o bebida por su nombre(str) y crea una matriz con todas las coincidencias que aranquen con el mismo nombre.

        Pre: crea una lista por comprension con las coincidencias de la carta y lo que le paso el usuario.
        Post: Si encontro coincidencias de lo que encontro el usuario las guarda, si no deja la lista vacia e informa que no se encontro nada.
        argumentos:
                lineas: matriz con el cuerpo del archivo menu.csv
                encabezado: matriz con el encabezado del archivo menu.csv
    """     
    busqueda = input('Ingrese la categoría que quieras buscar: ')
    busq =  [linea for linea in lineas if linea[2].lower().startswith(busqueda)]
    if busq:
        print(tabulate(busq))
    else:
        print('Categoria no encontrada')          
    return

mesas = {f'{_}': [] for _ in range(1, 13)}
if __name__ == '__main__':
    menu()


