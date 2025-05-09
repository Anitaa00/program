import json 
import os 

INVENTARIO_JSON = "inventario.json"
MENU_JSON = "menu.json"
PEDIDOS_JSON = "pedidos.json"

class Producto: 
    def __init__(self, nombre, precio, imagen, ingredientes=None):
        self.nombre = nombre
        self.precio = precio
        self.imagen = imagen
        self.ingredientes = ingredientes if ingredientes else {}


class Bebida(Producto): 
    def __init__(self, nombre, precio,imagen, tamaño, tipo, personalizacion=None):
        super().__init__(nombre, precio, imagen)
        self.tamaño = tamaño
        self.tipo = tipo
        self.personalizacion = personalizacion if personalizacion else []
        self.ingredientes = {"Agua": 1}
        self.ingredientes.update(personalizacion or {})
        


class Postre(Producto):
    def __init__(self, nombre, precio, imagen, personalizacion=None, vegano=False, sin_gluten=False):
        super().__init__(nombre, precio, imagen)
        self.vegano = vegano
        self.sin_gluten = sin_gluten
        self.personalizacion = personalizacion
        self.ingredientes = {"Harina": 1}
        self.ingredientes.update(personalizacion)



class Pedido: 
    lista_pedidos = []
    
    def __init__(self, cliente):
        self.cliente = cliente
        self.productos = []
        self.estado = "Pendiente"
        self.total = 0

    def agregar_producto(self, producto):
        self.productos.append(producto)
        self.total += producto.precio

    def calcular_total(self):
        return self.total

    def actualizar_estado(self, nuevo_estado):
        self.estado = nuevo_estado
       
    def verificar_disponibilidad(self, ingredientes):
        print("verificar_disponibilidad() llamado")
        print(f"  Ingredientes a verificar: {ingredientes}")
        print(f"  Inventario en verificar_disponibilidad: {self.stock}")  # MUY IMPORTANTE
        faltantes = [ing for ing, cantidad in ingredientes.items() if self.stock.get(ing, 0) < cantidad]
        print(f"  Faltantes: {faltantes}")
        return len(faltantes) == 0

    def actualizar_stock(self, inventario):
        for prod in self.productos:
            inventario.actualizar_stock(prod.ingredientes)

    def guardar_pedido():
        pass 

    def cargar_pedido():
        pass


class Menu:

    @staticmethod
    def cargar_menu():
        if os.path.exists(MENU_JSON):
            try: 
                with open(MENU_JSON, "r", encoding="utf-8") as file:
                    data = json.load(file)

                productos = []
                menu_data = data.get("menu", {})
                
                for categoria, items in menu_data.items(): 
                    for item in items:
                        nombre = item.get("nombre")
                        precio = item.get("precio")
                        imagen = item.get("imagen", None)
                        personalizaciones = item.get("personalizaciones", {})

                        if categoria == "postres":
                            productos.append(Postre(nombre, precio, imagen, personalizacion=personalizaciones))
                        else: 
                            productos.append(Bebida(
                                nombre=nombre, 
                                precio=precio, 
                                imagen=imagen,
                                tamaño=None, 
                                tipo=categoria,
                                personalizacion=personalizaciones
                            ))

                    return productos
            except json.JSONDecodeError:
                print("Error al cargar el menu")
            return []


class Inventario:

    @staticmethod
    def cargar_inventario():
        if os.path.exists(INVENTARIO_JSON):
            try:
                with open(INVENTARIO_JSON, "r", encoding="utf-8") as file:
                    data = json.load(file)
                return data
            except json.JSONDecodeError:
                print("Advertencia: Error al decodificar inventario.json. Se cargará un inventario vacío.")
                return {}
        return {}

    @staticmethod
    def guardar_inventario(inventario):  # Elimina 'cls' del primer argumento
        with open(INVENTARIO_JSON, "w", encoding="utf-8") as file:
            json.dump(inventario, file, indent=4, ensure_ascii=False)

    def __init__(self):
        self.stock = self.cargar_inventario()

    def agregar_ingrediente(self, ingrediente, cantidad):
        self.stock[ingrediente] = self.stock.get(ingrediente, 0) + cantidad
        Inventario.guardar_inventario(self.stock)  # Llama al método estático correctamente

    def verificar_disponibilidad(self, ingredientes):
        faltantes = [ing for ing, cantidad in ingredientes.items() if self.stock.get(ing, 0) < cantidad]
        return len(faltantes) == 0

    def actualizar_stock(self, ingredientes):
        print("actualizar_stock() llamado")
        print(f"  Ingredientes a actualizar: {ingredientes}")
        print(f"  Inventario antes de actualizar: {self.stock}")
        for ing, cantidad in ingredientes.items():
            if ing in self.stock and self.stock[ing] >= cantidad:  # Añadí 'ing in self.stock'
                self.stock[ing] -= cantidad
            else:
                print(f"  Advertencia: No hay suficiente stock de {ing} para actualizar.")
        Inventario.guardar_inventario(self.stock)
        print(f"  Inventario después de actualizar: {self.stock}")

    def consultar_inventario(self):
        print("Inventario actual:")
        for ing, cantidad in self.stock.items():
            print(f"- {ing}: {cantidad} unidades")

    def items(self):
        return self.stock.items()


       




   
            
    