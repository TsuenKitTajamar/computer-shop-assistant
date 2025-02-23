import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient

# Cargar variables de entorno
load_dotenv()

# Datos de Azure Blob Storage
blob_account_url = os.getenv("BLOB_ACCOUNT_URL")  # URL de tu cuenta Blob
blob_container_name = os.getenv("BLOB_CONTAINER_NAME")  # Nombre del contenedor
sas_token = os.getenv("SAS_TOKEN")  # Si tienes un SAS token

# Carpeta donde se encuentran los archivos PDF
pdfs_folder = "pdfs"  # Ruta de los archivos PDF locales

# Función para verificar si el archivo ya existe en el contenedor de Blob Storage
def file_exists_in_blob(file_name):
    blob_service_client = BlobServiceClient(account_url=blob_account_url, credential=sas_token)
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=file_name)
    try:
        # Intentar obtener el blob, si existe no dará error
        blob_client.get_blob_properties()
        return True
    except:
        return False

# Función para subir el archivo a Azure Blob Storage
def upload_file_to_blob(file_path, file_name):
    if file_exists_in_blob(file_name):
        print(f"El archivo {file_name} ya existe en Azure Blob Storage. Omitiendo carga.")
        return None

    blob_service_client = BlobServiceClient(account_url=blob_account_url, credential=sas_token)
    blob_client = blob_service_client.get_blob_client(container=blob_container_name, blob=file_name)
    
    # Subir el archivo
    with open(file_path, "rb") as file:
        blob_client.upload_blob(file, overwrite=True)
    
    # Obtener la URL del archivo
    file_url = f"{blob_account_url}/{blob_container_name}/{file_name}?{sas_token}" if sas_token else f"{blob_account_url}/{blob_container_name}/{file_name}"
    return file_url

# Subir todos los archivos PDF a Azure Blob Storage
pdf_urls = []
for file in os.listdir(pdfs_folder):
    if file.lower().endswith(".pdf"):
        pdf_path = os.path.join(pdfs_folder, file)
        pdf_name = os.path.basename(pdf_path)
        
        # Subir el archivo solo si no existe en Azure Blob Storage
        pdf_url = upload_file_to_blob(pdf_path, pdf_name)
        if pdf_url:
            pdf_urls.append(pdf_url)
            print(f"Archivo subido a: {pdf_url}")

# Guardar las URLs de los archivos subidos en un archivo para procesar más tarde
with open("uploaded_files.txt", "w") as f:
    for url in pdf_urls:
        f.write(url + "\n")

print("Subida completada para todos los archivos PDF.")
