# custom-entitites
## App

La aplicación buscará la intención del usuario las cuales serán `comprarOrdenador` o `consultarOrdenadores` , y también comprobará si hay entidades.

En caso de que sea `comprarOrdenador` y haya entidades, buscará por esas entidades en la base de datos.

En caso de que sea `consultarOrdenadores` responderá a la pregunta en base al `Custom Question Answering` .

### Propuesta inicial
Instrucciones: 

- Crear un servicio para convertir los PDF a texto 

- Etiquetar los ficheros de texto para identificar ordenadores con sus características 

- Crear una base de datos en la que se guarda la información de las características de los ordenadores 

- Crear un modelo conversacional (chatbot) para pedir comprar un equipo con ciertas características 

- Recuperar la ficha del producto y traducirla al idioma seleccionado (inglés, francés, chino o ruso) 

- Subir un fichero con un ordenador con unas características y hacer un pedido 


### Propuesta Actual
✅ Subida de los ficheros PDF a un Blob Storage Container
    Para disponer de ellos en la nube.

✅ Entrenamiento de un `Custom Entity Extraction Model` del servicio de Azure Document Intelligence
    Para extraer entidades personalizadas de los documentos PDF.

✅ Formarteo del JSON devuelto por el `Custom Entity Extraction Model` para quedarnos con el `label`y el `value`
    El servicio de Document Intelligence, nos devuelve un JSON con las entidades extraídas y otros datos adicionales pero solo nos interesa
    quedarnos con la `nombre de entidad` y el `valor de la entidad`.

✅ Guardamos el `label`y el `value` como campos en una base de datos CosmosDB con MongoDB
    Almacenaremos el nombre de la entidad y el valor (por ejemplo: Producto -> Lenovo) de cada especificación, y así con los demás productos.

✅ Crear un `Conversational Language Understanding model` en Azure AI Language Service para buscar las intenciones del usuario y crear un chatbot
    Con ello buscaremos saber la intención del usuario `comprarOrdenador` o si realizar una consulta `consultarOrdenadores`

✅ Crearemos un `Custom Question Answering` en Azure AI Language Service para responder a consultas sobre productos de la tienda
    Proporcionará al usuario respuestas sobre especificaciones de productos

#### Scripts

- `upload_files_to_azyre.py` : Subida de ficheros a Azure Blob Container

- ***`process_files_to_text.py` : Conversion de los archivos PDF a texto plano en fichero txt (en este caso el modelo extrae datos directamente del PDF, por lo que no lo necesitaremos)

- `entities_to_formatted_json.py` : Tras el etiquetado del `Custom Entity Extraction Model`, nos devolvera un archivo `json` pero tendremos que formatearlo para quedarlos con el nombre de la etiqueta y el valor

##### Intents&&Entities
- `intents_entities_testing_data.py` : Genera datos de testeo para el `Conversation Understading Model`

- `intents_entities_training_clu.py` : Genera datos de inteciones y entidades de entrenamiento para el `Conversation Understading Model`

##### db

- `save_to_db.py` : Guardaremos estos 2 valores en una base de datos en `Azure CosmosDB` el cual el nombre de la etiqueta sera el campo (field) y guardaremos su respectivo valor


