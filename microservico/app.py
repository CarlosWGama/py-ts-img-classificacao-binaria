from flask import Flask, request, jsonify
from PIL import Image
from os import listdir
from os.path import isdir
import numpy as np
from tensorflow import keras
import requests
import base64
import io
model = keras.models.load_model('modelo-treinado')

def select_image(filename):
    # load image from file
    if(filename.startswith('http')):
        image = Image.open(requests.get(filename, stream=True).raw) #ARQUIVO URL
    else:
        image = Image.open(io.BytesIO(base64.b64decode(str(filename)))) #ARQUIVO FISICO
    # convert to RGB, if needed
    image = image.convert('RGB')
    image = image.resize((150,150))
    # convert to array
    return np.asarray(image)

###########################################

app = Flask(__name__)

@app.route('/')
def welcome():
    return 'Bem vindo a API de Reconhecimento de imagens!'

@app.route('/image', methods=["POST"])
def analyse():
    data = request.json
    image = data['image']

    image = select_image(image)
    image = np.array(list(image)) / 255.0  ## convertendo de lista para array

    #### Recupera o modelo treinado
    results = model(np.array([image]))
    result = results[0].numpy() 
    print(result)
    response = {"value":0, "acc":0, "value_name": ""}
    if (result[0] > result[1]):
        response["value"] = "0"
        response["value_name"] = "elefante"
        response["acc"] = str(result[0])
    else:
        response["value"] = "1"
        response["value_name"] = "girafa"
        response["acc"] = str(result[1])

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0')