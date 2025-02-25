from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

# Cargar variables de entorno
load_dotenv()
cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
cosmos_database_name = os.getenv("COSMOSDB_DATABASE_NAME")
cosmos_collection_name = os.getenv("COSMOSDB_COLLECTION_NAME")

# Conectar a MongoDB
try:
    client = MongoClient(cosmos_connection_string)
    db = client[cosmos_database_name]
    collection = db[cosmos_collection_name]

    # Extraer documentos
    documents = list(collection.find())

    # Get the current date in YYYY-MM-DD format
    fecha_actual = datetime.now().strftime("%Y-%m-%d")

    # Generar pares de preguntas y respuestas
    qa_pairs = []

    for doc in documents:
        product_name = doc.get("Producto", "Producto desconocido")
        questions_answers = [
            (f"¿Cuál es el precio del {product_name}?", f"El precio del {product_name} es {doc.get('Precio', 'Precio no disponible')}."),
            (f"¿Cuánto cuesta el {product_name}?", f"El {product_name} cuesta {doc.get('Precio', 'Precio no disponible')}."),
            (f"¿Quién es el fabricante del procesador del {product_name}?", f"El fabricante del procesador del {product_name} es {doc.get('FabricanteProcesador', 'Fabricante no disponible')}."),
            (f"¿Quién fabrica el procesador del {product_name}?", f"El procesador del {product_name} es fabricado por {doc.get('FabricanteProcesador', 'Fabricante no disponible')}."),
            (f"¿Cuánta memoria RAM tiene el {product_name}?", f"El {product_name} tiene {doc.get('MemoriaRAM', 'Memoria RAM no disponible')}."),
            (f"¿Qué tipo de memoria RAM tiene el {product_name}?", f"El {product_name} tiene memoria RAM de tipo {doc.get('TipoRAM', 'Tipo de RAM no disponible')}."),
            (f"¿Cuál es la capacidad de memoria del {product_name}?", f"El {product_name} tiene una capacidad de memoria de {doc.get('CapacidadMemoria', 'Capacidad de memoria no disponible')}."),
            (f"¿Cuál es la capacidad de almacenamiento del {product_name}?", f"El {product_name} tiene una capacidad de almacenamiento de {doc.get('CapacidadMemoria', 'Capacidad de memoria no disponible')}."),
            (f"¿Qué tipo de almacenamiento tiene el {product_name}?", f"El {product_name} tiene almacenamiento de tipo {doc.get('TipoMemoria', 'Tipo de soporte no disponible')}."),
            (f"¿Qué tipo de soporte de memoria tiene el {product_name}?", f"El {product_name} tiene un soporte de memoria de tipo {doc.get('TipoMemoria', 'Tipo de soporte no disponible')}."),
            (f"¿Qué modelo de gráfica tiene el {product_name}?", f"El {product_name} tiene una gráfica modelo {doc.get('ModeloGrafica', 'Modelo gráfica no disponible')}."),
            (f"¿Cuál es el modelo de la gráfica del {product_name}?", f"El modelo de la gráfica del {product_name} es {doc.get('ModeloGrafica', 'Modelo gráfica no disponible')}."),
            (f"¿Quién es el fabricante de la gráfica del {product_name}?", f"El fabricante de la gráfica del {product_name} es {doc.get('FabricanteGrafica', 'Fabricante gráfica no disponible')}."),
            (f"¿Cuál es el peso del {product_name}?", f"El peso del {product_name} es {doc.get('Peso', 'Peso no disponible')}."),
            (f"¿Cuál es el tamaño de la pantalla del {product_name}?", f"El tamaño de la pantalla del {product_name} es {doc.get('Pulgadas', 'Tamaño de pantalla no disponible')}."),
            (f"¿De qué color es el {product_name}?", f"El color del {product_name} es {doc.get('Color', 'Color no disponible')}."),
            (f"¿Cuál es el sistema operativo del {product_name}?", f"El sistema operativo del {product_name} es {doc.get('SistemaOperativo', 'Sistema operativo no disponible')}."),
            (f"¿El {product_name} tiene webcam integrada?", f"{'Sí' if doc.get('WebCamIncluida', 'No').lower() == 'si' else 'No'}, el {product_name} {'tiene' if doc.get('WebCamIncluida', 'No').lower() == 'si' else 'no tiene'} webcam integrada."),
            (f"¿Cuál es el código del producto del {product_name}?", f"El código del producto del {product_name} es {doc.get('CodigoProducto', 'Código de producto no disponible')}."),
            (f"¿Quién vende el {product_name}?", f"El {product_name} es vendido por {doc.get('ComercianteNombre', 'Nombre del comerciante no disponible')}."),
            (f"¿Cuál es el nombre del comerciante del {product_name}?", f"El nombre del comerciante del {product_name} es {doc.get('ComercianteNombre', 'Nombre del comerciante no disponible')}."),
            (f"¿Cuál es la dirección del comerciante del {product_name}?", f"La dirección del comerciante del {product_name} es {doc.get('ComercianteDireccion', 'Dirección del comerciante no disponible')}."),
            (f"¿Cuál es el teléfono del comerciante del {product_name}?", f"El teléfono del comerciante del {product_name} es {doc.get('ComercianteTelefono', 'Teléfono del comerciante no disponible')}."),
            (f"¿Cuál es el número de contacto del comerciante del {product_name}?", f"El número de contacto del comerciante del {product_name} es {doc.get('ComercianteTelefono', 'Teléfono del comerciante no disponible')}."),
            (f"¿Cuál es el correo electrónico del comerciante del {product_name}?", f"El correo electrónico del comerciante del {product_name} es {doc.get('ComercianteEmail', 'Email del comerciante no disponible')}."),
            (f"¿Cuál es el email del comerciante del {product_name}?", f"El email del comerciante del {product_name} es {doc.get('ComercianteEmail', 'Email del comerciante no disponible')}."),
        ]
        qa_pairs.extend(questions_answers)

    # Create filename with the current date
    output_file = f"training_data/qna_training_basic_data_{fecha_actual}.txt"

    # Guardar pares de preguntas y respuestas en un archivo .txt
    with open(output_file, "w", encoding="utf-8") as f:
        for question, answer in qa_pairs:
            f.write(f"{question}\n")
            f.write(f"{answer}\n")

    print("Pares de preguntas y respuestas generados exitosamente en {output_file}.")

except Exception as e:
    print(f"Error al conectar a la base de datos: {e}")
