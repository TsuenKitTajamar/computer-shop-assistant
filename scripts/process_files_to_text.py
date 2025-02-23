import os, io
from dotenv import load_dotenv
from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from azure.storage.blob import BlobServiceClient

# Cargar variables de entorno
load_dotenv()

# Conexión con Azure Blob Storage
blob_service_client = BlobServiceClient(account_url=os.getenv("BLOB_ACCOUNT_URL"), credential=os.getenv("SAS_TOKEN"))
container_client = blob_service_client.get_container_client(os.getenv("BLOB_CONTAINER_NAME"))

# Listar los archivos PDF en el contenedor
pdf_files = [blob.name for blob in container_client.list_blobs() if blob.name.endswith('.pdf')]

print("Archivos PDF en el contenedor:", pdf_files)

# Conexión con Azure Document Intelligence
client = DocumentAnalysisClient(
    endpoint=os.getenv("AZURE_DI_ENDPOINT"),
    credential=AzureKeyCredential(os.getenv("AZURE_DI_API_KEY"))
)

# Conectar con Azure Blob Storage
blob_service_client = BlobServiceClient(account_url=os.getenv("BLOB_ACCOUNT_URL"), credential=os.getenv("SAS_TOKEN"))
container_client = blob_service_client.get_container_client(os.getenv("BLOB_CONTAINER_NAME"))

# Definir la carpeta de salida
output_folder = "outputs"
os.makedirs(output_folder, exist_ok=True)  # Crear la carpeta si no existe

# Procesar cada archivo PDF
for pdf_file in pdf_files:
    # Obtener el Blob directamente sin descargarlo
    blob_client = container_client.get_blob_client(pdf_file)

    # Usar Azure Document Intelligence para extraer el texto del PDF
    blob_data = blob_client.download_blob()
    pdf_data = blob_data.readall()  # Leer todo el contenido del blob PDF

    # Usar el contenido de PDF para procesarlo con Azure Document Intelligence
    with io.BytesIO(pdf_data) as pdf_file_stream:  # Convertir los bytes en un stream en memoria
        poller = client.begin_analyze_document("prebuilt-layout", pdf_file_stream)  # Usamos el modelo 'layout'
        result = poller.result()

    # # Usar Azure Document Intelligence para extraer el texto del PDF
    # with open(pdf_file, "rb") as f:
    #     poller = client.begin_analyze_document("prebuilt-layout", f)  # Usamos el modelo 'layout' para extraer el texto
    #     result = poller.result()

    # Extraer el texto del resultado
    extracted_text = ""
    for page in result.pages:
        for line in page.lines:
            extracted_text += line.content + "\n"

    # Guardar el texto extraído en la carpeta 'outputs'
    txt_filename = os.path.join(output_folder, pdf_file.replace('.pdf', '.txt'))
    with open(txt_filename, "w", encoding="utf-8") as text_file:
        text_file.write(extracted_text)

    print(f"Texto extraído y guardado en {txt_filename}")

# Mensaje al final de que todos los documentos han sido procesados
print("¡Todos los documentos han sido extraídos!")
