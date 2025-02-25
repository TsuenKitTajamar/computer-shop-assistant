import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()

# Configuración de Cosmos DB
cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
cosmos_database_name = os.getenv("COSMOSDB_DATABASE_NAME")
cosmos_collection_name = os.getenv("COSMOSDB_COLLECTION_NAME")

# Conectar a MongoDB
client = MongoClient(cosmos_connection_string)
db = client[cosmos_database_name]
collection = db[cosmos_collection_name]

# Extraer los documentos
documents = list(collection.find())

# Obtener la fecha actual en formato YYYY-MM-DD
fecha_actual = datetime.now().strftime("%Y-%m-%d")

# Función para generar frases de entrenamiento con entidades
def generar_frases(doc):
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
        ("comprarOrdenador", f"Necesito un portátil con {modelo_procesador} y {ram}, que tenga {capacidad_memoria}.", [
            ("ModeloProcesador", modelo_procesador),
            ("MemoriaRAM", ram),
            ("CapacidadMemoria", capacidad_memoria)
        ]),
        ("comprarOrdenador", f"Estoy buscando un ordenador con {fabricante_procesador} y al menos {almacenamiento}.", [
            ("FabricanteProcesador", fabricante_procesador),
            ("CapacidadMemoria", almacenamiento)
        ]),
        ("comprarOrdenador", f"Quiero comprar el {producto} de color {color} que cuesta {precio}.", [
            ("Producto", producto),
            ("Color", color),
            ("Precio", precio)
        ]),
        ("comprarOrdenador", f"Voy a hacer un pedido del {producto} con código {codigo}.", [
            ("Producto", producto),
            ("CodigoProducto", codigo)
        ]),
        ("consultarOrdenadores", f"¿Qué sistema operativo tiene el {producto}? {sistema}", [
            ("Producto", producto),
            ("SistemaOperativo", sistema)
        ]),
        ("consultarOrdenadores", f"¿Este ordenador tiene webcam? {webcam}", [
            ("Producto", producto),
            ("WebCamIncluida", webcam)
        ]),
        ("consultarOrdenadores", f"¿Cuántas pulgadas tiene la pantalla del {producto}? {pantalla}", [
            ("Producto", producto),
            ("Pulgadas", pantalla)
        ]),
        ("consultarOrdenadores", f"¿Cuál es la tarjeta gráfica del {producto}? {modelo_grafica} fabricada por {fabricante_grafica}.", [
            ("Producto", producto),
            ("ModeloGrafica", modelo_grafica),
            ("FabricanteGrafica", fabricante_grafica)
        ]),
        ("consultarOrdenadores", f"¿Cuál es el procesador del {producto}? {procesador}.", [
            ("Producto", producto),
            ("Procesador", procesador)
        ]),
        ("consultarOrdenadores", f"¿Qué tipo de memoria tiene el {producto}? {tipo_memoria}.", [
            ("Producto", producto),
            ("TipoMemoria", tipo_memoria)
        ]),
        ("consultarOrdenadores", f"¿Cuánto pesa el {producto}? {peso}.", [
            ("Producto", producto),
            ("Peso", peso)
        ])
    ]

    return frases

# Estructura JSON correcta para CLU
clu_data = []
unique_utterances = set()  # Use a set to track unique utterances

# Agregar los datos generados sin duplicados
for doc in documents:
    for intent, text, entities in generar_frases(doc):
        if text not in unique_utterances:
            unique_utterances.add(text)
            entidades = []
            for category, value in entities:
                offset = text.find(value)
                if offset != -1:  # Ensure the entity exists in the phrase
                    entidades.append({
                        "category": category,
                        "offset": offset,
                        "length": len(value)
                    })
            clu_data.append({
                "intent": intent,
                "language": "es-es",
                "text": text,
                "entities": entidades
            })

# Crear nombre del archivo con la fecha
output_file = f"training_data/clu_training_data_{fecha_actual}.json"

# Guardar en un archivo JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clu_data, f, indent=4, ensure_ascii=False)

print(f"Datos convertidos y guardados en {output_file}")
