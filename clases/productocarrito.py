
class ProductoCarrito:

    def __init__(self, id, nombre, precio, cantidad, subtotal):
        self.id = id
        self.nombre = nombre
        self.precio = precio
        self.cantidad = cantidad
        self.subtotal = subtotal

    @classmethod
    def crearProductoCarrito(cls, producto, productosEnCarrito):
        for i in range(len(productosEnCarrito)):
            if producto.id == productosEnCarrito[i].id:
                productosEnCarrito[i].cantidad = productosEnCarrito[i].cantidad + 1
                productosEnCarrito[i].subtotal = productosEnCarrito[i].subtotal + productosEnCarrito[i].precio
                return productosEnCarrito

        nuevoProductoCarrito = cls(producto.id, producto.nombre, producto.precio, 1, producto.precio)
        productosEnCarrito.append(nuevoProductoCarrito)
        return productosEnCarrito

