import requests
from clases.producto import Producto
from clases.productocarrito import ProductoCarrito
from conexion import verificador

#Variables

URL = 'http://localhost:8000/productos'
URL_VENTAS = 'http://localhost:8000/ventas/'
URL_FACTURAS = 'http://localhost:8000/facturas/'

def imprimirProductos(listaProductos):
    print()
    print("PRODUCTOS: ")
    print()

    print('{:<10} {:<30} {:<30}'.format("ID", "NOMBRE", "PRECIO"))
    print("-------------------------------------------------")
    for i in range(len(listaProductos)):
        info = vars(listaProductos[i])
        print('{:<10} {:<30} $ {:<30}'.format(listaProductos[i].id, listaProductos[i].nombre, listaProductos[i].precio))

def imprimirProductosCarrito(listaProductosCarrito):
    total = 0
    print()
    print("PRODUCTOS REGISTRADOS EN LA VENTA    : ")
    print()

    print('{:<10} {:<30} {:<10} {:<10} {:<20}'.format("ID", "NOMBRE", "PRECIO", "CANTIDAD", "SUBTOTAL"))
    print("-------------------------------------------------------------------------")
    for i in range(len(listaProductosCarrito)):
        info = vars(listaProductosCarrito[i])
        total += listaProductosCarrito[i].subtotal
        print('{:<10} {:<30} $ {:<10} {:<10} $ {:<20}'.format(listaProductosCarrito[i].id, listaProductosCarrito[i].nombre, listaProductosCarrito[i].precio, listaProductosCarrito[i].cantidad, listaProductosCarrito[i].subtotal))
    print()
    print(('{:>75}'.format("TOTAL: $ " + str(total))))


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

                    productosEnCarrito = ProductoCarrito.crearProductoCarrito(producto, productosEnCarrito)
                    total += producto.precio


                else:
                    print("ID inválido. Por favor inténtelo de nuevo.")
        elif opc == 2:
            #Aca imprimo el Carrito (Se va a crear proximamente la clase ProductoCarrito para poder llevar cantidades correctamente)
            #imprimirProductos(productosEnCarrito)
            imprimirProductosCarrito(productosEnCarrito)

        elif opc == 3:
            # Crear objeto Venta y mandar la petición POST
            #print("Total", total)
            params = {
                'costoTotal' : total
            }
            headers = {'hash': verificador.encriptarHash(total)}
            response = requests.post(URL_VENTAS, data=params, headers = headers)
            response = response.json()
            idVenta = response[len(response) - 1]['pk']
            print("ID VENTA: " + str(idVenta))

            params = {
                'total' : total,
                'tipo' : tipo,
                'aceptada' : aceptada,
                'venta' : idVenta
            }
            headers = {'hash': verificador.encriptarHash(str(total) + str(tipo) + str(aceptada) + str(idVenta))}
            response = requests.post(URL_FACTURAS, data=params, headers = headers)
            response = response.json()
            idFactura = response[len(response) - 1]['pk']
            print("ID FACTURA: " + str(idFactura))
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

