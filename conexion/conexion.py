import requests
from clases.producto import Producto

#Variables

URL = 'http://localhost:8000/productos'
URL_VENTAS = 'http://localhost:8000/ventas/'

def imprimirProductos(listaProductos):
    print()
    print("PRODUCTOS: ")
    print()

    print('{:<10} {:<30} {:<30}'.format("ID", "NOMBRE", "PRECIO"))
    print("-------------------------------------------------")
    for i in range(len(listaProductos)):
        info = vars(listaProductos[i])
        print('{:<10} {:<30} $ {:<30}'.format(listaProductos[i].id, listaProductos[i].nombre, listaProductos[i].precio))

def imprimirMenuVenta():
    print()
    print("-------------------Registrando Venta-------------- ")
    print()
    print("1. Añadir producto.")
    print("2. Ver carrito.")
    print("3. Facturar venta.")
    print("4. Salir.")
    print()

def getProductos():
    productos = []
    response = requests.get(URL)
    jsonResponse = response.json()
    #print(jsonResponse)
    # Imprimo solo los fields
    #print(jsonResponse[0]['fields'])
    print()
    # print('Tamaño json: ' + str(len(jsonResponse)))
    for i in range(len(jsonResponse)):
        #id = jsonResponse[i]['pk']
        #print('ID: ' + str(id))
        #print(jsonResponse[i]['fields'])
        producto = Producto(jsonResponse[i]['pk'], jsonResponse[i]['fields']['nombre'], jsonResponse[i]['fields']['precio'])
        productos.append(producto)
    return productos

def buscarProductoPorId(productos, id):
    for i in range(len(productos)):
        if productos[i].id == id:
            return productos[i]

def validarExistenciaProducto(productos, id):
    for i in range(len(productos)):
        if productos[i].id == id:
            return True
    return False

def registrarVenta():
    productosActuales = []
    productosEnCarrito = []
    total = 0
    tipo = "Electrónica"
    aceptada = True
    venta = ""  # Aca tiene que ir el ID de la venta que se asociará
    salir = False

    while not salir:
        imprimirMenuVenta()
        opc = int(input("Seleccione una opcion:"))
        # print("Opcion seleccionada:", opc)

        if opc == 1:
            encontro = False
            while not encontro:
                productosActuales = getProductos()
                imprimirProductos(productosActuales)
                id = input("Digite el ID del producto a añadir:")

                # Validación del ID digitado
                encontro = validarExistenciaProducto(productos, int(id))
                if encontro:
                    producto = buscarProductoPorId(productosActuales, int(id))
                    productosEnCarrito.append(producto)
                    total += producto.precio

                else:
                    print("ID inválido. Por favor inténtelo de nuevo.")
        elif opc == 2:
            #Aca imprimo el Carrito (Se va a crear proximamente la clase ProductoCarrito para poder llevar cantidades correctamente)
            imprimirProductos(productosEnCarrito)
        elif opc == 3:
            # Crear objeto Venta y mandar la petición POST
            print("Total", total)
            params = {
                'costoTotal' : total
            }
            response = requests.post(URL_VENTAS, data=params)
            #print(response.json())
        elif opc == 4:
            salir = True

def iniciarVenta():
    total = 0
    tipo = "Electrónica"
    aceptada = True
    venta = "" #Aca tiene que ir el ID de la venta que se asociará

    registrarVenta()

def imprimirMenu():
    salir = False

    while salir == False:
        print()
        print("-------------------CAJA-------------- ")
        print()
        print("1. Registrar venta")
        print("2. Listar productos")
        print("3. Salir")
        print()
        opc = input("Seleccione una opcion:")
        #print("Opcion seleccionada:", opc)

        if int(opc) == 1:
            print("Inicio de registro de venta")
            iniciarVenta()
        elif int(opc) == 2:
            imprimirProductos(getProductos())
        elif int(opc) == 3:
            salir = True



productos = getProductos()
#imprimirProductos(productos)
imprimirMenu()

