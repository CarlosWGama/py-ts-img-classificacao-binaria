from PIL import Image
from os import listdir
from os.path import isdir
import numpy as np
from tensorflow import keras
import requests

######################################
### Configurações
#imagem = 'D:\\Documentos\\Python\\cancer\\teste\\elefante.jpg'
imagem = 'https://images.theconversation.com/files/230552/original/file-20180803-41366-8x4waf.JPG?ixlib=rb-1.1.0&q=45&auto=format&w=926&fit=clip'


####################################
def select_image(filename):
    # load image from file
    if(filename.startswith('http')):
        image = Image.open(requests.get(filename, stream=True).raw) #ARQUIVO URL
    else:
        image = Image.open(filename) #ARQUIVO FISICO
    # convert to RGB, if needed
    image = image.convert('RGB')
    image = image.resize((150,150))
    # convert to array
    return np.asarray(image)



imagens = select_image(imagem)
imagens = np.array(list(imagens)) / 255.0  ## convertendo de lista para array

#### Recupera o modelo treinado
model = keras.models.load_model('modelo-treinado')
results = model.predict(np.array([imagens]))
result = results[0]

response = {"value":0, "acc":0}
if (result[0] > result[1]):
    response["value"] = 0
    response["acc"] = result[0]
else:
    response["value"] = 1
    response["acc"] = result[1]

print(response)