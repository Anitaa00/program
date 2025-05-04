import customtkinter as ctk
from tkinter import messagebox, ttk
import tkinter as tk
from back_cafe import Inventario
from back_cafe import Pedido, Bebida, Postre, Menu
from PIL import Image, ImageTk
import json
import os
import random


def obtener_ruta_archivo(nombre_archivo, subcarpeta=""):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_archivo = os.path.join(script_dir, subcarpeta, nombre_archivo)
    return ruta_archivo

def cargar_menu():
    try:
        with open(obtener_ruta_archivo("menu.json"), "r", encoding="utf-8") as f:
            datos_menu = json.load(f)
            return datos_menu["menu"]
    except FileNotFoundError:
        messagebox.showerror("Error", "No se pudo cargar el menú.")
        return {} 

menu = cargar_menu()

def guardar_pedido(pedido_data):
    try:
        pedidos_path = obtener_ruta_archivo("pedidos.json")
        if os.path.exists(pedidos_path):
            with open(pedidos_path, "r", encoding="utf-8") as f:
                pedidos = json.load(f)
        else:
            pedidos = []
        pedidos.append(pedido_data)
        with open(pedidos_path, "w", encoding="utf-8") as f:
            json.dump(pedidos, f, indent=4, ensure_ascii=False)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo guardar el pedido: {e}")

pedido_actual = []
pedidos = []

inventario = Inventario()

ctk.set_appearance_mode("system")  
ctk.set_default_color_theme("dark-blue")



def ventana_principal():
    global root 
    root = ctk.CTk()
    root.title("Caferería")
    root.geometry("700x700")
    root.iconbitmap(obtener_ruta_archivo("taza.ico", "iconos"))


    imagen_fondo = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fondo1.png", "imgs")),
                                dark_image=Image.open(obtener_ruta_archivo("fondo1.png", "imgs")),
                                size=(700, 700))
    
    fondo_label = ctk.CTkLabel(root, image=imagen_fondo, text="")
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1)


    imagen_boton_b = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("barista.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("barista.png", "imgs")),
                                  size=(50, 50))

    imagen_boton_c = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("cliente.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("cliente.png", "imgs")),
                                  size=(50, 50))
    

    titulo = ctk.CTkLabel(root, text="BIENVENIDO", font=("Lucida Calligraphy", 60, "bold"), text_color="white", fg_color="#230f08")
    titulo.place(relx=0.5, rely=0.1, anchor="center")

    frame_botones = ctk.CTkFrame(root, corner_radius=0, fg_color="#230f08")
    frame_botones.place(relx=0.5, rely=0.5, anchor="center")



    def abrir_barista():
        root.after_cancel("all")
        root.destroy()
        ventana_barista()

    def abrir_cliente():
        root.after_cancel("all")
        root.destroy()
        ventana_cliente()
        
    boton_barista = ctk.CTkButton(frame_botones, text="Barista", command=abrir_barista, width=250, height=70, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#523f31", hover_color="#523f31", compound=ctk.LEFT)
    boton_barista.configure(image=imagen_boton_b, compound=ctk.LEFT)
    boton_barista.image = imagen_boton_b
    boton_barista.pack(pady=10)

    boton_cliente = ctk.CTkButton(frame_botones, text="Cliente", command=abrir_cliente, width=250, height=70, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#523f31", hover_color="#523f31", compound=ctk.LEFT)
    boton_cliente.configure(image=imagen_boton_c, compound=ctk.LEFT)
    boton_cliente.image = imagen_boton_c
    boton_cliente.pack(pady=10)

    root.mainloop()

def ventana_barista():
    barista_window = ctk.CTk()
    barista_window.title("Ventana de Barista")
    barista_window.geometry("700x700")
    barista_window.iconbitmap(obtener_ruta_archivo("icon.bari.ico", "iconos"))
    
    imagen_pil = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fondo4.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("fondo4.png", "imgs")),
                              size=(700, 700))

    fondo_label = ctk.CTkLabel(barista_window, image=imagen_pil, text="")
    fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    imag = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("baris.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("baris.png", "imgs")),
                              size=(200, 200))
    imagen = ctk.CTkLabel(barista_window, image=imag, bg_color="#2a1911", text="")
    imagen.place(relx=1.0, rely=1.0, anchor= "se" )

    imagen = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("baris2.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("baris2.png", "imgs")),
                              size=(150, 150))
    imagen = ctk.CTkLabel(barista_window, image=imagen, bg_color="#2a1911", text="")
    imagen.place(relx=0.0, rely=0.0, anchor= "nw" )

    def ver_inventario(): 
        ventana_inventario = ctk.CTkToplevel(barista_window)
        ventana_inventario.title("Inventario")
        ventana_inventario.geometry("700x700")
    
        img_fondo = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fondo5.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("fondo5.png", "imgs")),
                              size=(700, 700))

        fondo_label = ctk.CTkLabel(ventana_inventario, image=img_fondo, text="")
        fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)
        
        scroll_frame = ctk.CTkScrollableFrame(ventana_inventario, width=650, height=650, scrollbar_button_color="#523f31")
        scroll_frame.pack(pady=10, padx=10)

        encabezado_ingrediente = ctk.CTkLabel(scroll_frame, text="INGREDIENTE", font=("Bodoni MT", 16, "bold"), width=350, fg_color="#674333")
        encabezado_ingrediente.grid(row=0, column=0, padx=5, sticky="ew")

        encabezado_cantidad = ctk.CTkLabel(scroll_frame, text="CANTIDAD", font=("Bodoni MT", 16, "bold"), width=250, fg_color="#674333")
        encabezado_cantidad.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        for i, (ingrediente, cantidad) in enumerate(inventario.items(), start=1):
            ctk.CTkLabel(scroll_frame, text=ingrediente, font=("Arial", 12)).grid(row=i, column=0, padx=5, pady=2)
            ctk.CTkLabel(scroll_frame, text=str(cantidad), font=("Arial", 12)).grid(row=i, column=1, padx=5, pady=2)

        boton_cerrar = ctk.CTkButton(ventana_inventario, text="Cerrar", command=ventana_inventario.destroy)
        boton_cerrar.pack(pady=10)


    def agregar_ingredientes(): 
        ventana_agregar = ctk.CTkToplevel(barista_window)
        ventana_agregar.title("Agregar ingredientes")
        ventana_agregar.geometry("700x700")

        img_fond_agr = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fondo6.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("fondo6.png", "imgs")),
                              size=(700, 700))

        fondo_label = ctk.CTkLabel(ventana_agregar, image=img_fond_agr, text="")
        fondo_label.place(relx=0, rely=0, relwidth=1, relheight=1)


        ctk.CTkLabel(ventana_agregar, text="INGREDIENTE:", font=("Century", 16), bg_color="#311d17").pack(pady=(10, 0), padx=25)
        ingrediente_entry = ctk.CTkEntry(ventana_agregar, border_color="#311d17", text_color="#f2e8d5", width=300, height=30)
        ingrediente_entry.pack(pady=(0, 10))

        ctk.CTkLabel(ventana_agregar, text="CANTIDAD:", font=("Century", 16), bg_color="#311d17").pack(pady=(10, 0), padx=25)
        cantidad_entry = ctk.CTkEntry(ventana_agregar, border_color="#311d17", text_color="#f2e8d5", width=300, height=30)
        cantidad_entry.pack(pady=(0, 10))

        def agregar(): 
            ingrediente = ingrediente_entry.get().strip()
            try: 
                cantidad = int(cantidad_entry.get())
                if ingrediente: 
                    inventario.agregar_ingrediente(ingrediente, cantidad)
                    #inventario.guardar_inventario(inventario)
                    messagebox.showinfo("Ingredientes agregados", f"De {ingrediente} se agregaron {cantidad} unidades.")
                    ingrediente_entry.delete(0, 'end')
                    cantidad_entry.delete(0, 'end')
            except ValueError:
                messagebox.showerror("Error", "Por favor ingresa una cantidad valida")

        ctk.CTkButton(ventana_agregar, text="AGREGAR", command=agregar, fg_color="#674333", width=350, height=40, corner_radius=10, font=("Georgia", 16), hover_color="#311d17").pack(pady=10)
        ctk.CTkButton(ventana_agregar, text="VER INVENTARIO", command=ver_inventario, fg_color="#674333", font=("Georgia", 16), hover_color="#311d17", width=350, height=40, corner_radius=10).pack(pady=10)

    frame_botones = ctk.CTkFrame(barista_window, fg_color="#2a1911", corner_radius=0)
    frame_botones.place(relx=0.5, rely=0.5, anchor="center")


    imagen_boton_inv = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("inv.fond.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("inv.fond.png", "imgs")),
                                  size=(50, 50))
    boton_ver_inv = ctk.CTkButton(frame_botones, text="Ver Inventario", command=ver_inventario, width=250, height=70, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#4a2619", hover_color="#2a1911")
    boton_ver_inv.configure(image=imagen_boton_inv, compound=ctk.LEFT)
    boton_ver_inv.image = imagen_boton_inv
    boton_ver_inv.pack(pady=10)

    imagen_boton_agr = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("ing.fond.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("ing.fond.png", "imgs")),
                                  size=(50, 50))
    boton_agregar_ing = ctk.CTkButton(frame_botones, text="Agregar Ingredientes", command=agregar_ingredientes, width=250, height=70, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#4a2619", hover_color="#2a1911")
    boton_agregar_ing.configure(image=imagen_boton_agr, compound=ctk.LEFT)
    boton_agregar_ing.image = imagen_boton_agr
    boton_agregar_ing.pack(pady=10)
    
    imagen_boton_salir = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("salida.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("salida.png", "imgs")),
                                  size=(50, 50))
    
    boton_salir = ctk.CTkButton(frame_botones, text="Salir", command=barista_window.destroy, width=250, height=70, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#4a2619", hover_color="#674333")
    boton_salir.configure(image=imagen_boton_salir, compound=ctk.LEFT)
    boton_salir.image = imagen_boton_salir
    boton_salir.pack(pady=10)

    def on_closing():
        barista_window.destroy()

    barista_window.protocol("WM_DELETE_WINDOW", on_closing)  
    barista_window.mainloop()



def ventana_cliente():
    cliente_window = ctk.CTk()
    cliente_window.title("Ventana de cliente")
    cliente_window.geometry("700x700")
    cliente_window.iconbitmap(obtener_ruta_archivo("ico.menu.ico", "iconos"))

    imagen_fondo = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fond.vm.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("fond.vm.png", "imgs")),
                              size=(700, 700))

    fondo_label = ctk.CTkLabel(cliente_window, image=imagen_fondo, text="")
    fondo_label.place(x=0, y=0, relwidth=1, relheight=1) 

    img_men = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("men2.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("men2.png", "imgs")),
                              size=(200, 200))
    imagen = ctk.CTkLabel(cliente_window, image=img_men, bg_color="#342519", text="")
    imagen.place(relx=0.5, rely=1.0, anchor= "s" )
    

#ID
    def orden_id():
        numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
               'V', 'W', 'X', 'Y', 'Z']
        order_id = "ORD_" 
        random_letters = ""
        random_digits = ""
        for i in range(0,3):
            random_letters += random.choice(letters)
            random_digits += str(random.choice(numbers))

        order_id += random_letters + random_digits
        return order_id
    

    with open("menu.json", "r", encoding="utf-8") as archivo:
        datos_menu = json.load(archivo)
        menu = datos_menu["menu"]


    def ver_menu():
        global ventana_menu, pedido_actual, total_label, items_frame, pedido_frame
        ventana_menu = ctk.CTkToplevel(cliente_window)
        ventana_menu.title("Menu")
        ventana_menu.geometry("1300x800")

        inventario.cargar_inventario()
        pedido_id = orden_id()

        row_count = 0

        contenedor = ctk.CTkFrame(ventana_menu)
        contenedor.pack(expand=True, fill="both", padx=10, pady=10)

        menu_frame = ctk.CTkScrollableFrame(contenedor, width=700, height=600, fg_color="#4c2b08", scrollbar_button_color="#aa7743")
        menu_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))

        pedido_frame = ctk.CTkFrame(contenedor, width=450, height=30, fg_color="#4c2b08" )
        pedido_frame.pack(side="right", fill="y", padx=10, pady=10)
       # pedido_frame.grid_columnconfigure(0, weight=1)

        id_pedido_frame = ctk.CTkFrame(pedido_frame, fg_color="transparent")
        id_pedido_frame.pack(expand=True, fill="both", padx=10, pady=10)

        items_frame = ctk.CTkScrollableFrame(pedido_frame, fg_color="#4c2b08", width=230, height=300, scrollbar_button_color="#aa7743")
        items_frame.pack(expand=True, fill="both")

        total_frame = ctk.CTkFrame(pedido_frame, fg_color="#4c2b08")
        total_frame.pack(pady=5)

        id_pedido_label = ctk.CTkLabel(pedido_frame, width=270, text=f"ID ORDEN: {pedido_id}", font=("Lucida Fax", 12, "bold"))
        id_pedido_label.pack(pady=5)

        global total_label
        total_label = ctk.CTkLabel(total_frame, width=280, text="TOTAL: $0.00", font=("Lucida Fax", 14, "bold"))
        total_label.pack(pady=5)

        ordenar_boton = ctk.CTkButton(pedido_frame, text="ORDENAR", 
                                      command=lambda: confirma_pedido(pedido_id), 
                                      fg_color="#2a1911", hover_color="#2a1911", width=200)
        ordenar_boton.pack()

        pedido_vacio = ctk.CTkLabel(items_frame, text="Tu pedido está vacío", font=("Georgia", 14))

        def ordenar(self): 
            if not self.carrito:
                return
            
            for producto, cantidad in self.carrito.items():
                if self.inventario.get(producto, 0) < cantidad:
                    messagebox.showwarning("Inventario insuficiente", f"No hay suficiente {producto} en inventario.")
                    return
                
            for producto, cantidad in self.carrito.items():
                self.inventario[producto] -= cantidad

            self.crear_ticket() 
            self.carrito.clear()
            self.actualizar_interfaz()

        pedido_vacio = ctk.CTkLabel(pedido_frame, text="Tu pedido está vacio", font=("Georgia", 14))

        def actualizar_vista_pedido():
            for widget in items_frame.winfo_children():
                widget.destroy()

            if not pedido_actual:
                pedido_vacio.pack(pady=10)
                total_label.configure(text="TOTAL: $0.00")
            else:
                pedido_vacio.pack_forget()
                total = 0
                for i, item in enumerate(pedido_actual):
                    texto = f"{item['nombre']} - ${item['precio']:.2f}\n" + "\n".join([f"{k}: {v}" for k, v in item["personalizaciones"].items()])
                    ctk.CTkLabel(items_frame, text=texto, font=("Arial", 14), anchor="w", justify="left").pack(anchor="w", padx=10, pady=5)

                    def eliminar(index):
                        if 0 <= index < len(pedido_actual):
                            pedido_actual.pop(index)
                            actualizar_vista_pedido()

                    ctk.CTkButton(items_frame, text="Eliminar", command=lambda i=i: eliminar(i), width=100, fg_color="#3c2012").pack(padx=10, pady=2)
                    #total += item["precio"]

                total_label.configure(text=f"Total: ${total:.2f}")



            total = 0
            for item in pedido_actual:
                nombre = item['nombre']
                precio = float(item['precio'])
                cantidad = item['cantidad']
                subtotal = precio * cantidad
                total += subtotal

                item_label = ctk.CTkLabel(items_frame, text=f"{nombre} x {cantidad} = ${subtotal:.2f}")
                item_label.pack(pady=2, anchor="w")

            total_label.configure(text=f"TOTAL: ${total:.2f}")

        def agregar(item_menu):
            global pedido_actual
            nombre = item_menu['nombre']
            precio = item_menu['precio']

            encontrado = False
            for item in pedido_actual:
                if item['nombre'] == nombre:
                    item['cantidad'] += 1
                    encontrado = True
                    break
            if not encontrado:
                pedido_actual.append({'nombre': nombre, 'precio': precio, 'cantidad': 1})

        def devolver_ingredientes(pedido):
            ingredientes = obt_ingre_real(pedido)
            for ing, cant in ingredientes.items():
                if ing in inventario:
                    inventario[ing] += cant
                else:
                    inventario[ing] = cant 

        def obt_ingre_real(pedido): 
            ingredientes_totales = {}

            for item in pedido: 
                ingredientes = item.get("ingredientes", {})
                personalizaciones = item.get("personalizaciones", {})

                for ing, canti in ingredientes.items():
                    if any(
                        valor.lower().replace(" ", "_") in ing.lower()
                        for valor in personalizaciones.values()
                    ):
                        ingredientes_totales[ing] = ingredientes_totales.get(ing, 0) + canti
                    elif "_" not in ing:  # Ingredientes genéricos (sin personalización)
                        ingredientes_totales[ing] = ingredientes_totales.get(ing, 0) + canti

            return ingredientes_totales

        def mostrar_ticket(pedido_id, items, total): 
            ticket_window = ctk.CTkToplevel()
            ticket_window.title(f"Ticket- Pedido {pedido_id}")
            ticket_window.geometry("500x600")

            img_tick = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("fondo7.jpg", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("fondo7.jpg", "imgs")),
                              size=(500, 600))

            fondo_label = ctk.CTkLabel(ticket_window, image=img_tick, text="")
            fondo_label.place(x=0, y=0, relwidth=1, relheight=1) 

            imagen1 = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("menu4.png", "imgs")),
                              dark_image=Image.open(obtener_ruta_archivo("menu4.png", "imgs")),
                              size=(80, 80))
            imagen = ctk.CTkLabel(ticket_window, image=imagen1, bg_color="#43532a", text="")
            imagen.place(relx=1.0, rely=1.0, anchor= "se" )

            ticket_label = ctk.CTkLabel(
                ticket_window,
                text=f"ORDEN #{pedido_id}",
                font=("Georgia", 20, "bold"),
                text_color="#f2e8d5",
                bg_color="#43532a",
            )
            ticket_label.pack(pady=15)

            frame_items = ctk.CTkScrollableFrame(ticket_window, width=450, height=400)
            frame_items.pack(pady=10, padx=20, fill="both", expand=True)

            for item in items: 
                texto = f"{item['nombre']} - ${item['precio']:.2f}"
                items_label = ctk.CTkLabel(frame_items, text=texto, font=("Georgia", 16), anchor="w", justify="left", text_color="#f2e8d5", bg_color="transparent")
                items_label.pack(anchor="w", padx=10, pady=(8, 2))# fill="x")

                for k, v in item["personalizaciones"].items():
                    ctk.CTkLabel(frame_items, text=f" {k}: {v}", font=("Georgia", 16), anchor="w", text_color="#f2e8d5", bg_color="transparent").pack(pady=5)

                ctk.CTkLabel(frame_items, text="-" * 50, font=("Consolas", 10)).pack(pady=5)

            ctk.CTkLabel(
                ticket_window,
                text=f"TOTAL: ${total:.2f}",
                font=("Georgia", 18, "bold"),
                text_color="#f2e8d5",
                fg_color="#43532a",
                bg_color="#43532a",
            ).pack(pady=15)

            botones_frame = ctk.CTkFrame(ticket_window, fg_color="#43532a")
            botones_frame.pack(pady=10)

            def cancelar_pedido(pedido_id):
                global pedidos
                pedidos_actual = next((p for p in pedidos if p["id"] == pedido_id), None)
                if pedidos_actual:
                    pedidos.remove(pedidos_actual)

            def cancelar():
                global pedidos
                pedido_actual = next((p for p in pedidos if p["id"] == pedido_id), None)
                if pedido_actual:
                    devolver_ingredientes(pedido_actual["items"])
                    cancelar_pedido(pedido_id)
                ticket_window.destroy()

            btn_cancelar = ctk.CTkButton(
                botones_frame,
                text="CANCELAR PEDIDO",
                command=cancelar,
                fg_color="#9c996d",
                hover_color="#9c996d",
                width=160
            )
            btn_cancelar.pack(side="left", padx=10)

            btn_cerrar = ctk.CTkButton(
                botones_frame,
                text="CERRAR",
                command=ticket_window.destroy,
                width=120,
                fg_color="#7f8040",
                hover_color="#7f8040"
            )
            btn_cerrar.pack(side="left", padx=10)

           # ctk.CTkLabel(ticket_window, text=f"TOTAL: ${total:.2f}", font=("Arial", 16, "bold")).pack(pady=10)

            #ctk.CTkButton(ticket_window, text="CERRAR", command=ticket_window.destroy, width=120).pack(pady=10)

        def confirma_pedido(pedido_id): 
            if not pedido_actual:
                messagebox.showinfo("Pedido vacio")
                return
            
            total = sum(item['precio'] for item in pedido_actual)

            ingrediente_totales = obt_ingre_real(pedido_actual)

            if not inventario.verificar_disponibilidad(ingrediente_totales):
                messagebox.showwarning("Stock insuficientes", "No hay productos suficientes")
                return
            
            inventario.actualizar_stock(ingrediente_totales)

            pedido_guarda = {
                "id_pedido": pedido_id,
                "items": pedido_actual,
                "total": total
            }

            try: 
                if os.path.exists("pedidos.json"):
                    with open("pedidos.json", "r", encoding="utf-8") as f: 
                        pedidos = json.load(f)
                else: 
                    pedidos = []

                pedidos.append(pedido_guarda)

                with open("pedidos.json", "w", encoding="utf-8") as f: 
                    json.dump(pedidos, f, indent=4, ensure_ascii=False)

                mostrar_ticket(pedido_id, pedido_actual.copy(), total)

                messagebox.showinfo("Éxito", f"Pedido {pedido_id} confirmado y guardado.")
                pedido_actual.clear()
                actualizar_vista_pedido()

            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el pedido: {e}")


                print(f"total_label: {total_label}")
                try:
                    print(f"total_label.winfo_exists(): {total_label.winfo_exists()}")
                except Exception as e:
                    print(f"Error al verificar existencia de total_label: {e}")



        for i, (categoria, productos) in enumerate(menu.items()):
            cat_label = ctk.CTkLabel(menu_frame, text=categoria.replace("_", " ").title(), font=("Arial", 18, "bold"), text_color="white")
            cat_label.grid(row=row_count, column= 0, columnspan=2, sticky="ew", padx=5, pady=(10, 0))
            row_count += 1

            for j, producto in enumerate(productos):
                row = row_count + (j//2)
                col = j % 2 

                frame = ctk.CTkFrame(menu_frame, corner_radius=10, fg_color="#2a1911")
                frame.grid(row=row, column=col, padx=10, pady=5, sticky="nsew")

                if "imagen" in producto and os.path.exists(obtener_ruta_archivo (producto["imagen"], "imagenes")):
                    try:
                        imagen = ctk.CTkImage(Image.open(obtener_ruta_archivo(producto["imagen"], "imagenes")), size=(120, 120))
                        ctk.CTkLabel(frame, image=imagen, text="").pack(side="left", padx=10)
                    except:
                        pass


                marco_frame = ctk.CTkFrame(frame, fg_color="transparent")
                marco_frame.pack(side="left", padx=10)

                ctk.CTkLabel(marco_frame, text=f"{producto['nombre']} - ${producto['precio']:.2f}", font=("Georgia", 14, "bold"), text_color="#f2e8d5").pack(anchor="w")

                vars_personalizacion = {}
                for key, opciones in producto.get("personalizaciones", {}).items():
                    var = ctk.StringVar(value=opciones[0] if opciones else "")
                    ctk.CTkLabel(marco_frame, text=f"{key}:", font=("Arial", 12)).pack(anchor="w")
                    if opciones:
                        ctk.CTkOptionMenu(marco_frame, values=opciones, variable=var, fg_color="#513528", button_color="#513528", font=("Perpetua", 15) ).pack(anchor="w", pady=2)
                        vars_personalizacion[key] = var
                if not producto.get("personalizaciones"):
                    ctk.CTkLabel(marco_frame, text="No disponible", font=("Arial", 12 )).pack(anchor="w", pady=2)


                def crear_agregar(p=producto, pers=vars_personalizacion):
                    def agregar():
                        item = {
                            "nombre": p["nombre"],
                            "precio": p["precio"],
                            "personalizaciones": {k: v.get() for k, v in pers.items()}, 
                            "ingredientes": p.get("ingredientes", {}),
                            "cantidad": 1
                        }

                        ingredientes_usados = obt_ingre_real([item])

                        if not inventario.verificar_disponibilidad(ingredientes_usados):
                            messagebox.showwarning("Sin stock", f"No hay ingredientes")
                            return
                        
                        for extistente in pedido_actual:
                            if (
                                extistente["nombre"] == item["nombre"] and 
                                extistente.get("personalizaciones", {} == item.get("personalizaciones", {}))
                            ):
                                extistente["cantidad"] += 1 
                                actualizar_vista_pedido()
                                return
                        
                        pedido_actual.append(item)
                        actualizar_vista_pedido()

                    return agregar
                   
                ctk.CTkButton(marco_frame, text="Agregar al pedido", command=crear_agregar(), fg_color="#412c17", font=("Georgia", 14, "bold")).pack(anchor="w", pady=5)
            row_count += (len(productos) + 1) // 2

        for i in range(menu_frame.grid_size()[1]):
            menu_frame.grid_rowconfigure(i, weight=1)

        actualizar_vista_pedido() 
    
    frame_botones = ctk.CTkFrame(cliente_window, fg_color="#342519", corner_radius=0)
    frame_botones.place(relx=0.5, rely=0.5, anchor="center")
        
    imagen_boton_ver_menu = ctk.CTkImage(light_image=Image.open(obtener_ruta_archivo("img.menu.png", "imgs")),
                                  dark_image=Image.open(obtener_ruta_archivo("img.menu.png", "imgs")),
                                  size=(70, 70))
    boton_ver_menu = ctk.CTkButton(frame_botones, text="Ver Menu", command=ver_menu, width=250, height=90, font=("Centaur", 25, "bold"), corner_radius=10, fg_color="#573c32", hover_color="#573c32")
    boton_ver_menu.configure(image=imagen_boton_ver_menu, compound=ctk.LEFT)
    boton_ver_menu.image = imagen_boton_ver_menu
    boton_ver_menu.pack(pady=10)

    

    def on_closing():
        cliente_window.destroy()

    cliente_window.protocol("WM_DELETE_WINDOW", on_closing)  
    cliente_window.mainloop()



ventana_principal()