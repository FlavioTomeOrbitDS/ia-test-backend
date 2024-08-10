from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import pandas as pd
import json

API_KEY = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJncHRtYWtlciIsImlkIjoiM0NGQTZENjQ0RDM0QzEyMDVFNDgwRTFFMEIyMzUyQzMiLCJ0ZW5hbnQiOiIzQ0ZBNkQ2NDREMzRDMTIwNUU0ODBFMUUwQjIzNTJDMyIsInV1aWQiOiI4MWU4N2IyOC1hODYyLTQyNGEtOTU2OS1mZDBjMTI5ZmJlZWYifQ.utRLGf4U3MwHbM0kXQjQvAvzO-qSojBcCe6BM4Wu2gE"
BASE_API = "https://api.gptmaker.ai"
WORKSPACE_ID = "3CFA6D6451C8A01DAF820E1E0B2352C3"

df_assistants = pd.DataFrame()

def criar_assistente(name: str, communicationType: str, type: str, supportFor: str, supportWebsite: str, supportDescription: str):
    url = f"https://api.gptmaker.ai/v1/workspace/{WORKSPACE_ID}/assistants"
    
    payload = {
        "name": name,
        "communicationType": communicationType,
        "type": type,
        "supportFor": supportFor,
        "supportWebsite": supportWebsite,
        "supportDescription": supportDescription
    }
    
    headers = {
        'Authorization': API_KEY,
        'Content-Type': 'application/json'
    }

    response = requests.post(url, headers=headers, json=payload)

    print(response.text)
    
    return response

def listar_assistentes():
    global df_assistants
    
    url = f"https://api.gptmaker.ai/v1/workspace/{WORKSPACE_ID}/assistants?page=1&pageSize=10&query="

    payload={}
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    
    print(response.text)
    data_dict = json.loads(response.text)
    # Extrair a lista de dados
    assistants_data = data_dict['data']
    # Criar o DataFrame a partir da lista
    df_assistants = pd.DataFrame(assistants_data)
    
    print(df_assistants)
    
    return response

def atualiza_assistente(id, name, status, communicationType, type, supportFor, supportWebSite, supportDescription):
        
    url = f"https://api.gptmaker.ai/v1/assistant/{id}"

    payload = {"avatar": "https://api.multiavatar.com/1686337499.svg",
               "name": name,
               "status": status,
               "communicationType": communicationType,
               "type": type,
               "supportFor": supportFor,
               "supportWebsite": supportWebSite,
               "supportDescription": supportDescription}
    
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("PUT", url, headers=headers, json=payload)

    print("atualiza assistente says:")
    print(response.text)

    return response

def desativa_assistant(assistant_id):
    url = f"https://api.gptmaker.ai/v1/assistant/{assistant_id}/inactive"

    payload = ""
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("PUT", url, headers=headers, data=payload)

    print(response.text)
    
    return response



def create_training(assistant_id, description, image):    
    url = f"https://api.gptmaker.ai/v1/assistant/{assistant_id}/affirmations"

    payload = {"description": description,
               "image": None}
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("POST", url, headers=headers, json=payload)

    print("Create Training says: ")
    print(response.text)
    
    return response

def list_trainings(assistant_id):
    url = f"https://api.gptmaker.ai/v1/assistant/{assistant_id}/affirmations?page=1&pageSize=100&query=&type=TEXT"

    payload = ""
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("GET", url, headers=headers, json=payload)

    print(response.text)
    
    return response
    
def format_json(json_string):
    try:
        # Carrega a string JSON para um objeto Python (dicionário)
        data = json.loads(json_string)

        # Aqui você pode adicionar qualquer lógica de normalização ou manipulação, se necessário
        # Por exemplo, vamos assumir que você apenas quer retornar o objeto como está
        return data
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}  # Retorna um erro se o JSON estiver mal formatado

def delete_training(id):
    url = f"https://api.gptmaker.ai/v1/affirmation/{id}"

    payload = ""
    headers = {
    'Authorization': API_KEY
    }

    response = requests.request("DELETE", url, headers=headers, json=payload)

    print(response.text)

    return response


# Criação da aplicação Flask
app = Flask(__name__)

# Habilitação do CORS para permitir que o frontend acesse o endpoint
CORS(app)

@app.route('/', methods=['GET'])
def main():

    print("Sales IA backend online!!")

    return jsonify("Online")

#********************* ASSISTANTS ************************************************
@app.route('/getassistants', methods=['GET'])
def getassistants():
    response = listar_assistentes()    
    return jsonify(response.text)

@app.route('/create-assistant', methods=['POST'])
def create_assistant():
    try:
        data = request.json
        name = data.get('name')
        communicationType = data.get('communicationType')
        type = data.get('type')
        supportFor = data.get('supportFor')
        supportWebsite = data.get('supportWebsite')
        supportDescription = data.get('supportDescription')

        # Chama a função para criar o assistente
        response = criar_assistente(name, communicationType, type, supportFor, supportWebsite, supportDescription)
        
        # Retorna a resposta da API externa
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/assistant/<string:assistant_id>', methods=['GET'])
def get_assistant(assistant_id):
    global df_assistants
    # Buscar o assistente pelo ID no DataFrame
    print(assistant_id)
    result = df_assistants[df_assistants['id'] == assistant_id]

    # Verificar se o assistente foi encontrado
    if not result.empty:
        # Convertendo o DataFrame para dicionário para JSONificação
        assistant_info = result.to_dict('records')[0]
        print(assistant_info)
        return jsonify(assistant_info), 200
    else:
        return jsonify({"error": "Assistant not found"}), 404
    
@app.route('/updateassistant', methods=['POST'])
def updateassistant():
    try:
        data = request.json
        id = data.get('id')
        name = data.get('name')
        status = data.get('status')
        communicationType = data.get('communicationType')
        type = data.get('type')
        supportFor = data.get('supportFor')
        supportWebsite = data.get('supportWebsite')
        supportDescription = data.get('supportDescription')

        # Chama a função para criar o assistente
        response = atualiza_assistente(id,name, status, communicationType, type, supportFor, supportWebsite, supportDescription)
        
        # Retorna a resposta da API externa
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/deactivateassistant', methods=['POST'])
def deactivateassistant():
    try:
        data = request.json
        id = data.get('id')
        
        # Chama a função para criar o assistente
        response = desativa_assistant(id)
        
        # Retorna a resposta da API externa
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

#******************************* TRAINING ************************************************
@app.route('/createtraining', methods=['POST'])
def createtraining():
    try:
        data = request.json
        assistantId = data.get('assistantId')        
        description = data.get('description')
        image = data.get('image')
        
        # Chama a função para criar o assistente
        response = create_training(assistantId,description, None)
        
        # Retorna a resposta da API externa
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/gettrainings', methods=['POST'])
def gettrainings():
    data = request.json
    assistant_id = data.get('assistantId')        
    response = list_trainings(assistant_id)    
    
    formatted_data = format_json(response.text)    

    return jsonify(formatted_data), 200

@app.route('/deletetraining', methods=['POST'])
def deletetraining():
    try:
        data = request.json
        id = data.get('id')        
                    
        response = delete_training(id)
        
        # Retorna a resposta da API externa
        return jsonify(response.json()), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    # Configura o servidor Flask para rodar na porta 8080
    app.run(host='0.0.0.0', port=8080)
