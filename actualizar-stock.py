import sqlite3

def inicializar_bd():

    try:

        conexion = sqlite3.connect ("inventario_stock.db")
        cursor = conexion.cursor ()

        cursor.execute ("""
            CREATE TABLE IF NOT EXISTS productos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                stock_actual INTEGER NOT NULL,
                stock_minimo INTEGER NOT NULL

            )
        """)

        cursor.execute("SELECT COUNT (*) FROM productos")
        cantidad = cursor.fetchone()[0]

        if cantidad == 0:
            productos_iniciales = [
                ("Resma A4 75 gr Autor", 15, 10),
                ("Caja Boligraos Azules x12", 4, 8),
                ("Toner Laser Negro HP", 2, 5),
                ("Carpeta 3 Anillos Oficio", 20, 10),
                ("Cuaderno Espiraldo A4", 6, 6)

            ]

            cursor.executemany(
                "INSERT INTO productos (nombre, stock_actual, stock_minimo) VALUES (?, ?, ?)",
                productos_iniciales
            )
            print ("Se cargaron 5 productos iniciales de prueba")

        conexion.commit()
        conexion.close()
    except sqlite3.Error as error_bd:
        print(f"Error al inicializar la base de datos: {error_bd}")

def ver_inventario():

    try:
        conexion = sqlite3.connect("inventario_stock.db")
        cursor = conexion.cursor()

        cursor.execute("SELECT id, nombre, stock_actual, stock_minimo FROM productos")
        filas = cursor.fetchall()

        print("\n--- INVENTARIO GENERAL ---")
        print(f"{'ID':<4} | {'PRODUCTO':<30} | {'STOCK':<8} | {'MÍNIMO':<8} | {'ESTADO'}")
        print("-" * 72)

        for fila in filas:
            id_prod, nombre, stock, minimo = fila
            estado = "REPONER URGENTE" if stock <= minimo else "OK"
            print(f"{id_prod:<4} | {nombre:<30} | {stock:<8} | {minimo:<8} | {estado}")

        conexion.close()

    except sqlite3.Error as error_bd:
        print (f"Error al leer el inventarioa: {error_bd}")

def registrar_venta():

    ver_inventario()

    id_valido = False
    id_producto = 0
    while id_valido == False:
        try:
            id_producto= int(input ("\nIngresá el ID del producto vendido: "))
            id_valido= True
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    cantidad_valida = False
    cantidad_vendidad = 0

    while cantidad_valida == False:

        try:
            cantidad_vendida = int (input("Ingresa la cantidad de unidades vendidas: "))
            if cantidad_vendida  > 0:
                cantidad_valida = True

            else:
                print("Error: La cantidad vendida debe ser mayor a 0.")

        except ValueError:
            print("Error: Ingresa un numero entero valido.")

    try:
        conexion = sqlite3.connect("inventario_stock.db")
        cursor = conexion.cursor ()


        cursor.execute("SELECT nombre, stock_actual FROM productos WHERE id = ?", (id_producto,))
        resultado = cursor.fetchone()

        if resultado is None:
            print(f"\nNo existe ningún producto con el ID {id_producto}.")
        else:
            nombre, stock_actual = resultado
            
            # Validación crítica de negocio: evitar stock negativo
            if cantidad_vendida > stock_actual:
                print(f"\nOperación cancelada: Stock insuficiente de '{nombre}'. Disponible: {stock_actual} unidades.")
            else:
                nuevo_stock = stock_actual - cantidad_vendida
                cursor.execute(
                    "UPDATE productos SET stock_actual = ? WHERE id = ?",
                    (nuevo_stock, id_producto)
                )
                conexion.commit()
                print(f"\nVenta registrada. Nuevo stock de '{nombre}': {nuevo_stock} unidades.")
                
        conexion.close()
    except sqlite3.Error as error_bd:
        print(f"Error en la base de datos: {error_bd}")

def ingresar_mercaderia():
    ver_inventario()
    
    id_valido = False
    id_producto = 0
    while id_valido == False:
        try:
            id_producto = int(input("\nIngresá el ID del producto que ingresó: "))
            id_valido = True
        except ValueError:
            print("Error: El ID debe ser un número entero.")

    cantidad_valida = False
    cantidad_ingresada = 0
    while cantidad_valida == False:
        try:
            cantidad_ingresada = int(input("Ingresá la cantidad de unidades recibidas: "))
            if cantidad_ingresada > 0:
                cantidad_valida = True
            else:
                print("Error: La cantidad debe ser mayor a cero.")
        except ValueError:
            print("Error: Ingresá un número entero válido.")
                                


    try:
        conexion = sqlite3.connect("inventario_stock.db")
        cursor= conexion.cursor()

        cursor.execute("UPDATE productos SET stock_actual = stock_actual + ? WHERE id=?", (cantidad_ingresada, id_producto))

        if cursor.rowcount > 0:
            conexion.commit ()
            print(f"nIngreso registrado. Se sumaron {cantidad_ingresada} unidades al producto ID {id_producto}.")
        else:
            print(f"\nNo se encontró ningún producto con el ID {id_producto}.")

        conexion.close()

    except sqlite3.error as error_bd:
        print(f"Error al actualizar el stock: {error_bd}")

def ver_alertas_reposicion():

    try:
        conexion = sqlite3.connect("inventario_stock.db")
        cursor = conexion.cursor()

        cursor.execute("""
            SELECT id, nombre, stock_actual, stock_minimo
            FROM productos
            WHERE stock_actual <= stock_minimo
        """)

        alertas = cursor.fetchall()

        print("\n=== ALERTAS DE REPOSICIÓN (STOCK CRÍTICO) ===")

        if len(alertas) == 0:
            print("Todo el inventario esta por encima del stock minimo")

        else:
            print(f"{'ID':<4} | {'PRODUCTO':<30} | {'ACTUAL':<8} | {'MÍNIMO':<8} | {'FALTANTE SUGERIDO'}")
            print("-" * 78)
            for fila in alertas:
                id_prod, nombre, actual, minimo = fila
                faltante = (minimo - actual) + 5  # Sugiere comprar hasta quedar 5 unidades arriba del mínimo
                print(f"{id_prod:<4} | {nombre:<30} | {actual:<8} | {minimo:<8} | Pedir {faltante} u.")

        conexion.close()
    except sqlite3.Error as error_bd:
          print(f"Error al consultar alertas: {error_bd}")            
      

def menu_principal():
    inicializar_bd()
    continuar = True

    while continuar:
        print("\n=== GESTOR DE STOCK Y ALERTAS ===")
        print("1. Ver inventario completo")
        print("2. Registrar venta (salida de stock)")
        print("3. Registrar compra a proveedor (ingreso de stock)")
        print("4. Ver reporte de alertas de reposición")
        print("5. Salir")


        opcion = input("Elegi una opcion(1-5):").strip()

        if opcion== "1":
            ver_inventario()

        elif opcion == "2":
            registrar_venta()

        elif opcion== "3":
            ingresar_mercaderia()

        elif opcion== "4":
            ver_alertas_reposicion()

        elif opcion== "5":
            print("Cerrando el gestor de stock. ¡Hasta la vista Baby!")
            continuar = False
        else:
            print("Opción incorrecta. Elegí un número del 1 al 5.")

menu_principal()
                        
