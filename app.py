import os
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient
from dotenv import load_dotenv
from azure.core.credentials import AzureKeyCredential
from azure.ai.language.questionanswering import QuestionAnsweringClient
from azure.ai.language.conversations import ConversationAnalysisClient
from azure.core.exceptions import HttpResponseError

# Cargar variables de entorno
load_dotenv()

cosmos_connection_string = os.getenv("COSMOSDB_CONNECTION_STRING")
cosmos_database_name = os.getenv("COSMOSDB_DATABASE_NAME")
cosmos_collection_name = os.getenv("COSMOSDB_COLLECTION_NAME")

ai_endpoint = os.getenv('AZURE_COGNITIVE_SERVICE_ENDPOINT')
ai_key = os.getenv('AZURE_COGNITIVE_SERVICE_KEY')

qa_project_name = os.getenv('QnA_PROJECT_NAME')
qa_deployment_name = os.getenv('QnA_DEPLOYMENT_NAME')

# Conectar a MongoDB
client = MongoClient(cosmos_connection_string)
db = client[cosmos_database_name]
collection = db[cosmos_collection_name]

# Inicializar clientes de Azure
credential = AzureKeyCredential(ai_key)
qa_client = QuestionAnsweringClient(endpoint=ai_endpoint, credential=credential)
conversation_client = ConversationAnalysisClient(endpoint=ai_endpoint, credential=credential)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_question = request.json.get("question")

    if not user_question:
        return jsonify({"error": "Pregunta no proporcionada"}), 400

    # Analizar la intención del usuario
    try:
        print("Before analyze_intent")
        top_intent, confidence_score, entities = analyze_intent(user_question)
    except HttpResponseError as e:
        return jsonify({"error": str(e)}), e.status_code

    # Procesar la intención
    print(f"Processing intent: {top_intent}, Confidence Score: {confidence_score}, Entities: {entities}")
    if top_intent == "comprarOrdenador":
        # Buscar la entidad "Producto" en la lista de entidades
        producto = next((entity["text"] for entity in entities if entity["category"] == "Producto"), None)
        if producto:
            print("Processing 'comprarOrdenador' intent with entities")
            response = comprar_ordenador({"Producto": producto})
        else:
            print("No 'Producto' entity found for 'comprarOrdenador' intent")
            response = "Por favor, proporciona un nombre de producto más específico. Si no estás seguro del nombre exacto, es posible que no dispongamos de ese producto."
    elif top_intent == "consultarOrdenadores":
        print("Processing 'consultarOrdenadores' intent")
        response = get_answer(user_question)
    else:
        print("Processing QnA Maker response for unknown intent")
        response = get_answer(user_question)

    return jsonify({
        "response": response,
        "intent": top_intent,
        "confidence_score": confidence_score,
        "entities": entities
    })

def get_answer(question):
    try:
        response = qa_client.get_answers(
            question=question,
            project_name=qa_project_name,
            deployment_name=qa_deployment_name
        )
        # Devuelve la mejor respuesta encontrada
        return response.answers[0].answer if response.answers else "No se encontró una respuesta."
    except HttpResponseError as e:
        print(f"Error al obtener la respuesta: {e}")
        return "Lo siento, ocurrió un error al obtener la respuesta."

def analyze_intent(query):
    cls_project = "computer-store"
    deployment_slot = "production"

    result = conversation_client.analyze_conversation(
        task={
            "kind": "Conversation",
            "analysisInput": {
                "conversationItem": {
                    "participantId": "1",
                    "id": "1",
                    "modality": "text",
                    "language": "es",
                    "text": query
                },
                "isLoggingEnabled": False
            },
            "parameters": {
                "projectName": cls_project,
                "deploymentName": deployment_slot,
                "verbose": True
            }
        }
    )

    top_intent = result["result"]["prediction"]["topIntent"]
    confidence_score = result["result"]["prediction"]["intents"][0]["confidenceScore"]
    entities = result["result"]["prediction"]["entities"]

    # Log the detected intent, confidence score, and entities
    print(f"Top Intent: {top_intent}, Confidence Score: {confidence_score}")
    print(f"Entities: {entities}")

    return top_intent, confidence_score, entities

def buscar_ordenador(entidades):
    query = {}
    for entidad, valor in entidades.items():
        if entidad in ["MemoriaRAM", "Procesador", "CapacidadMemoria", "ModeloGrafica"]:
            query[entidad] = valor

    print(f"Query: {query}")  # Log the query for debugging
    resultados = list(collection.find(query))

    if resultados:
        respuesta = "He encontrado los siguientes ordenadores que cumplen con tus criterios:\n"
        for ordenador in resultados:
            nombre = ordenador.get("Producto", "Producto desconocido")
            precio = ordenador.get("Precio", "Precio no disponible")
            respuesta += f"- {nombre}: {precio}\n"
    else:
        respuesta = "No hay ordenadores disponibles que cumplan con tus criterios."

    print(f"Respuesta: {respuesta}")  # Log the response for debugging
    return respuesta

def comparar_ordenadores(entidades):
    producto1 = entidades.get("Producto1")
    producto2 = entidades.get("Producto2")

    ordenador1 = collection.find_one({"Producto": producto1})
    ordenador2 = collection.find_one({"Producto": producto2})

    if ordenador1 and ordenador2:
        respuesta = f"Comparación entre {producto1} y {producto2}:\n"
        respuesta += f"- Precio: {ordenador1['Precio']} vs {ordenador2['Precio']}\n"
        respuesta += f"- RAM: {ordenador1['MemoriaRAM']} vs {ordenador2['MemoriaRAM']}\n"
        respuesta += f"- Procesador: {ordenador1['Procesador']} vs {ordenador2['Procesador']}\n"
    else:
        respuesta = "No se encontraron ambos ordenadores para comparar."

    return respuesta

def consultas_adicionales(entidades):
    producto = entidades.get("Producto")
    consulta = entidades.get("Consulta")

    ordenador = collection.find_one({"Producto": producto})

    if ordenador:
        if consulta == "SistemaOperativo":
            respuesta = f"El sistema operativo del {producto} es {ordenador.get('SistemaOperativo', 'No disponible')}."
        elif consulta == "WebCamIncluida":
            respuesta = f"{'Sí' if ordenador.get('WebCamIncluida', 'No').lower() == 'si' else 'No'}, el {producto} {'tiene' if ordenador.get('WebCamIncluida', 'No').lower() == 'si' else 'no tiene'} webcam integrada."
        else:
            respuesta = "No tengo información sobre esa consulta."
    else:
        respuesta = f"No se encontró el ordenador {producto}."

    return respuesta

def comprar_ordenador(entidades):
    query = {}
    for entity in entidades:
        category = entity["category"]
        value = entity["text"]
        if category in ["MemoriaRAM", "Procesador", "CapacidadMemoria", "ModeloGrafica", "Producto"]:
            query[category] = value

    print(f"Query: {query}")  # Log the query for debugging
    resultados = list(collection.find(query))

    if resultados:
        respuesta = "He encontrado los siguientes ordenadores que cumplen con tus criterios:\n"
        for ordenador in resultados:
            nombre = ordenador.get("Producto", "Producto desconocido")
            precio = ordenador.get("Precio", "Precio no disponible")
            respuesta += f"- {nombre}: {precio}\n"
    else:
        respuesta = "No hay ordenadores disponibles que cumplan con tus criterios."

    print(f"Respuesta: {respuesta}")  # Log the response for debugging
    return respuesta

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
