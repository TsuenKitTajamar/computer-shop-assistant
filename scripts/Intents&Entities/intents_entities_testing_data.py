from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Cosmos DB configuration
cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
cosmos_database_name = os.getenv("COSMOSDB_DATABASE_NAME")
cosmos_collection_name = os.getenv("COSMOSDB_COLLECTION_NAME")

# Connect to MongoDB
client = MongoClient(cosmos_connection_string)
db = client[cosmos_database_name]
collection = db[cosmos_collection_name]

# Extract documents
documents = list(collection.find())

# Get the current date in YYYY-MM-DD format
fecha_actual = datetime.now().strftime("%Y-%m-%d")

# Function to generate testing phrases with entities
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
        ("BuscarOrdenador", f"¿Tienes un portátil con {modelo_procesador} y {ram} de RAM?", [
            ("ModeloProcesador", modelo_procesador),
            ("MemoriaRAM", ram)
        ]),
        ("BuscarOrdenador", f"Necesito un ordenador con al menos {almacenamiento} de almacenamiento.", [
            ("CapacidadMemoria", almacenamiento)
        ]),
        ("CompararOrdenadores", f"¿Cuál es la diferencia entre el {producto} y otros modelos?", [
            ("Producto", producto)
        ]),
        ("HacerPedido", f"Quiero hacer un pedido del {producto} en color {color}.", [
            ("Producto", producto),
            ("Color", color)
        ]),
        ("ConsultasAdicionales", f"¿El {producto} tiene {sistema} como sistema operativo?", [
            ("Producto", producto),
            ("SistemaOperativo", sistema)
        ]),
        ("ConsultasAdicionales", f"¿El {producto} incluye webcam?", [
            ("Producto", producto),
            ("WebCamIncluida", webcam)
        ]),
        ("ConsultasAdicionales", f"¿Cuántas pulgadas tiene la pantalla del {producto}?", [
            ("Producto", producto),
            ("Pulgadas", pantalla)
        ]),
        ("ConsultasAdicionales", f"¿Qué tarjeta gráfica tiene el {producto}?", [
            ("Producto", producto),
            ("ModeloGrafica", modelo_grafica),
            ("FabricanteGrafica", fabricante_grafica)
        ]),
        ("ConsultasAdicionales", f"¿El {producto} tiene un procesador {procesador}?", [
            ("Producto", producto),
            ("Procesador", procesador)
        ]),
        ("ConsultasAdicionales", f"¿Qué tipo de memoria usa el {producto}?", [
            ("Producto", producto),
            ("TipoMemoria", tipo_memoria)
        ]),
        ("ConsultasAdicionales", f"¿Cuánto pesa el {producto}?", [
            ("Producto", producto),
            ("Peso", peso)
        ])
    ]

    return frases

# Structure for CLU testing data
clu_test_data = []
unique_utterances = set()  # Use a set to track unique utterances

# Add the generated data without duplicates
for doc in documents:
    for intent, text, entities in generar_frases_prueba(doc):
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
            clu_test_data.append({
                "intent": intent,
                "language": "es-es",
                "text": text,
                "entities": entidades
            })

# Create filename with the current date
output_file = f"testing_data/clu_testing_data_{fecha_actual}.json"

# Save to a JSON file
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(clu_test_data, f, indent=4, ensure_ascii=False)

print(f"Datos de prueba convertidos y guardados en {output_file}")
