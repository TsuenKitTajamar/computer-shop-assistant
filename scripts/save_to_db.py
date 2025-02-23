import os
import json
from pymongo import MongoClient
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de Azure Blob Storage
blob_account_url = os.getenv("BLOB_ACCOUNT_URL")
sas_token = os.getenv("SAS_TOKEN_DEST_CONTAINER")
blob_container_name = os.getenv("BLOB_CONTAINER_NAME_DEST")

# Configuración de Cosmos DB
cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
cosmos_database_name = os.getenv("COSMOSDB_DATABASE_NAME")
cosmos_collection_name = os.getenv("COSMOSDB_COLLECTION_NAME")

# Inicializar Blob Service Client con SAS token
blob_service_client = BlobServiceClient(account_url=blob_account_url, credential=sas_token)
container_client = blob_service_client.get_container_client(blob_container_name)

# Inicializar MongoDB Client
cosmos_client = MongoClient(cosmos_connection_string)
cosmos_db = cosmos_client[cosmos_database_name]
cosmos_collection = cosmos_db[cosmos_collection_name]

# Función para leer y procesar archivos JSON desde Blob Storage
def process_blobs():
    blob_list = container_client.list_blobs()
    for blob in blob_list:
        blob_client = container_client.get_blob_client(blob)
        blob_data = blob_client.download_blob().readall()
        json_data = json.loads(blob_data)

        # Transformar los datos
        transformed_data = {item['label']: item['text'] for item in json_data.get('labels', [])}

        # Insertar los datos transformados en Cosmos DB
        cosmos_collection.insert_one(transformed_data)
        print(f"Datos de {blob.name} insertados correctamente!")

# Procesar todos los archivos JSON en el contenedor de blobs
process_blobs()