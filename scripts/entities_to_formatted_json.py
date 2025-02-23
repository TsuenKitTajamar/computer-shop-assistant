import json
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Cargar variables de entorno
load_dotenv()

# Conexión con Azure Blob Storage para el contenedor de origen
blob_service_client_origin = BlobServiceClient(
    account_url=os.getenv("BLOB_ACCOUNT_URL"),
    credential=os.getenv("SAS_TOKEN_ORIGIN_CONTAINER")
)
source_container_client = blob_service_client_origin.get_container_client(os.getenv("BLOB_CONTAINER_NAME"))

# Conexión con Azure Blob Storage para el contenedor de destino
blob_service_client_dest = BlobServiceClient(
    account_url=os.getenv("BLOB_ACCOUNT_URL"),
    credential=os.getenv("SAS_TOKEN_DEST_CONTAINER")
)
destination_container_client = blob_service_client_dest.get_container_client(os.getenv("BLOB_CONTAINER_NAME_DEST"))

# Función para procesar un archivo JSON
def process_json_file(json_content):
    data = json.loads(json_content)
    document_name = data.get("document", "")
    labels = data.get("labels", [])

    result = {
        "$schema": "https://schema.cognitiveservices.azure.com/formrecognizer/2021-03-01/labels.json",
        "document": document_name,
        "labels": []
    }

    for label in labels:
        label_name = label.get("label", "")
        values = label.get("value", [])

        # Concatenar los textos del mismo label
        concatenated_text = " ".join([value.get("text", "") for value in values])

        label_result = {
            "label": label_name,
            "text": concatenated_text
        }

        result["labels"].append(label_result)

    return result

# Iterar sobre los blobs en el contenedor de origen
blob_list = source_container_client.list_blobs()
print("Listando blobs en el contenedor de origen...")
for blob in blob_list:
    print(f"Blob encontrado: {blob.name}")
    if blob.name.endswith(".pdf.labels.json"):
        print(f"Procesando blob: {blob.name}")
        blob_client = source_container_client.get_blob_client(blob)
        try:
            json_content = blob_client.download_blob().readall()

            # Procesar el archivo JSON
            result = process_json_file(json_content)

            # Guardar el resultado en el contenedor de destino con encoding UTF-8
            destination_blob_name = blob.name.replace(".pdf.labels.json", ".json")
            destination_blob_client = destination_container_client.get_blob_client(destination_blob_name)
            destination_blob_client.upload_blob(json.dumps(result, indent=4, ensure_ascii=False).encode('utf-8'), overwrite=True)

            print(f"Procesado y guardado: {destination_blob_name}")
        except Exception as e:
            print(f"Error al procesar el blob {blob.name}: {e}")
    else:
        print(f"Omitiendo blob: {blob.name} (no es un archivo .pdf.labels.json)")

print("Procesamiento completado.")
