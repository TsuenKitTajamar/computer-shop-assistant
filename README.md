# custom-entitites

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

✅ Entrenamiento de un `Custom Entity Extraction Model` del servicio de Azure Document Intelligence

✅ Formarteo del JSON devuelto por el `Custom Entity Extraction Model` para quedarnos con el `label`y el `value`

✅ Guardamos el `label`y el `value` como campos en una base de datos CosmosDB con MongoDB

✅ Crear un `Conversational Language Understanding model` en Azure AI Language Service para buscar las intenciones del usuario y crear un chatbot


- `upload_files_to_azyre.py` : Subida de ficheros a Azure Blob Container

- ***`process_files_to_text.py` : Conversion de los archivos PDF a texto plano en fichero txt (en este caso el modelo extrae datos directamente del PDF, por lo que no lo necesitaremos)

- `entities_to_formatted_json.py` : Tras el etiquetado del `Custom Entity Extraction Model`, nos devolvera un archivo `json` pero tendremos que formatearlo para quedarlos con el nombre de la etiqueta y el valor

- `save_to_db.py` : Guardaremos estos 2 valores en una base de datos en `Azure CosmosDB` el cual el nombre de la etiqueta sera el campo (field) y guardaremos su respectivo valor

- `intents_entities_testing_data.py` : Genera datos de testeo para el `Conversation Understading Model`

- `intents_entities_training_clu.py` : Genera datos de inteciones y entidades de entrenamiento para el `Conversation Understading Model`

