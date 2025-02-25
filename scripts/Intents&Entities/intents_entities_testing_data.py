def generar_frases_prueba(doc):
    producto = doc.get("Producto", "Ordenador desconocido")
    precio = doc.get("Precio", "Precio no disponible")
    capacidad_memoria = doc.get("CapacidadMemoria", "Capacidad de memoria no especificada")
    color = doc.get("Color", "Color no especificado")
    fabricante_grafica = doc.get("FabricanteGrafica", "Fabricante de gráfica desconocido")
    fabricante_procesador = doc.get("FabricanteProcesador", "Fabricante de procesador desconocido")
    modelo_grafica = doc.get("ModeloGrafica", "Modelo de gráfica no especificado")
    modelo_procesador = doc.get("ModeloProcesador", "Modelo de procesador no especificado")
    ram = doc.get("MemoriaRAM", "RAM no especificada")
    almacenamiento = doc.get("CapacidadMemoria", "Almacenamiento no especificado")
    codigo = doc.get("CodigoProducto", "Código desconocido")
    pantalla = doc.get("Pulgadas", "Tamaño de pantalla no especificado")
    sistema = doc.get("SistemaOperativo", "Sistema operativo desconocido")
    webcam = doc.get("WebCamIncluida", "Información de webcam no disponible")
    procesador = doc.get("Procesador", "Procesador no especificado")
    tipo_memoria = doc.get("TipoMemoria", "Tipo de memoria no especificado")
    peso = doc.get("Peso", "Peso no especificado")

    frases = [
        ("comprarOrdenador", f"¿Tienes un portátil con {modelo_procesador} y {ram} de RAM?", [
            ("ModeloProcesador", modelo_procesador),
            ("MemoriaRAM", ram)
        ]),
        ("comprarOrdenador", f"Necesito un ordenador con al menos {almacenamiento} de almacenamiento.", [
            ("CapacidadMemoria", almacenamiento)
        ]),
        ("consultarOrdenadores", f"¿Cuál es la diferencia entre el {producto} y otros modelos?", [
            ("Producto", producto)
        ]),
        ("comprarOrdenador", f"Quiero hacer un pedido del {producto} en color {color}.", [
            ("Producto", producto),
            ("Color", color)
        ]),
        ("consultarOrdenadores", f"¿El {producto} tiene {sistema} como sistema operativo?", [
            ("Producto", producto),
            ("SistemaOperativo", sistema)
        ]),
        ("consultarOrdenadores", f"¿El {producto} incluye webcam?", [
            ("Producto", producto),
            ("WebCamIncluida", webcam)
        ]),
        ("consultarOrdenadores", f"¿Cuántas pulgadas tiene la pantalla del {producto}?", [
            ("Producto", producto),
            ("Pulgadas", pantalla)
        ]),
        ("consultarOrdenadores", f"¿Qué tarjeta gráfica tiene el {producto}?", [
            ("Producto", producto),
            ("ModeloGrafica", modelo_grafica),
            ("FabricanteGrafica", fabricante_grafica)
        ]),
        ("consultarOrdenadores", f"¿El {producto} tiene un procesador {procesador}?", [
            ("Producto", producto),
            ("Procesador", procesador)
        ]),
        ("consultarOrdenadores", f"¿Qué tipo de memoria usa el {producto}?", [
            ("Producto", producto),
            ("TipoMemoria", tipo_memoria)
        ]),
        ("consultarOrdenadores", f"¿Cuánto pesa el {producto}?", [
            ("Producto", producto),
            ("Peso", peso)
        ]),
        ("consultarOrdenadores", f"¿Cuál es el precio del {producto}?", [
            ("Producto", producto),
            ("Precio", precio)
        ]),
        ("consultarOrdenadores", f"¿Cuál es la capacidad de memoria del {producto}?", [
            ("Producto", producto),
            ("CapacidadMemoria", capacidad_memoria)
        ]),
        ("consultarOrdenadores", f"¿Quién es el fabricante del procesador del {producto}?", [
            ("Producto", producto),
            ("FabricanteProcesador", fabricante_procesador)
        ]),
        ("consultarOrdenadores", f"¿Cuál es el código del producto {producto}?", [
            ("Producto", producto),
            ("CodigoProducto", codigo)
        ])
    ]
    return frases
