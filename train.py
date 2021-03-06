from PIL import Image
from os import listdir
from os.path import isdir
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelBinarizer
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import VGG19
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import layers
from tensorflow.keras import models
from tensorflow.keras import optimizers
from tensorflow import keras


##########################################
### CONFIGURAÇÕES #####
dataset_folder = "D:\\Documentos\\Python\\classificacao-imagem\\dataset\\" #Pasta onde estão as fotos apra treinamento
avaliar = True #Faz também a avaliaçaõ do modelo
###########################################


#################################### Trata as images
def select_image(filename):
    # load image from file
    image = Image.open(filename)
    # convert to RGB, if needed
    image = image.convert('RGB')
    image = image.resize((150,150))
    # convert to array
    return np.asarray(image)

def load_classes(diretorio, classe, imagens, labels):
    # iterando arquivos
    for filename in listdir(diretorio):

        path = diretorio + filename

        try:
            imagens.append(select_image(path))
            labels.append(classe)
        except:
            print("Erro ao ler imagem {}".format(path))

    return imagens, labels

def select_data_set(diretorio):
    imagens = list()
    labels = list()

    for subdir in listdir(diretorio):
        # path
        path = diretorio + subdir + '\\'

        if not isdir(path):
            continue
        imagens, labels = load_classes(path, subdir, imagens, labels)

    return imagens, labels

#Carrega as imagens

imagens, labels  = select_data_set(dataset_folder)
imagens = np.array(imagens) / 255.0  ## convertendo de lista para array
labels = np.array(labels)  ## convertendo de lista para array
############### Padroniza para Binário
lb = LabelBinarizer()
labels = lb.fit_transform(labels)
labels = to_categorical(labels)

###
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau
batch_size   = 32
input_shape  = (150, 150, 3)
random_state = 42
alpha        = 1e-5
epoch        = 100


#### Faz um tratamento de checkpoint para evitar perder tudo no meio do caminho
filepath="transferlearning_weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='val_acc', verbose=1, save_best_only=True, mode='max')
lr_reduce = ReduceLROnPlateau(monitor='val_acc', factor=0.1, min_delta=alpha, patience=5, verbose=1)
callbacks = [checkpoint, lr_reduce]

(trainX, testX, trainY, testY) = train_test_split(imagens, labels, test_size=0.20)

##### Aumenta as imagens com as mesmas imagens em posições diferentes
train_datagen = ImageDataGenerator(
        rotation_range=20,
        zoom_range=0.2)
train_datagen.fit(trainX)

data_aug = train_datagen.flow(trainX, trainY, batch_size=batch_size)

####### Aprimora a base
conv_base = VGG19(weights='imagenet', include_top=False, input_shape=input_shape)
conv_base.trainable = True
set_trainable = False

for layer in conv_base.layers:
  if layer.name == 'block5_conv1':
    set_trainable = True
  if set_trainable:
    layer.trainable = True
  else:
    layer.trainable = False

### Criando o modelo
model = models.Sequential()
model.add(conv_base)
model.add(layers.GlobalAveragePooling2D())
model.add(layers.BatchNormalization())
model.add(layers.Flatten())
model.add(layers.Dense(128, activation='relu'))
model.add(layers.Dropout(0.6))
model.add(layers.Dense(2, activation='softmax'))

model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['acc'])
    
history = model.fit_generator(
                              data_aug,
                              steps_per_epoch=len(trainX)// batch_size, # parte inteira da divisão
                              validation_data=(testX, testY),
                              validation_steps=len(testX) // batch_size,# parte inteira da divisão
                              callbacks=callbacks,
                              epochs=epoch)

#### Salva o Modelo
model.save('modelo-treinado')


#### Avalia
if (avaliar):
    from sklearn.metrics import confusion_matrix
    import matplotlib.pyplot as plt
    pred = model.predict(testX)
    pred = np.argmax(pred,axis = 1) 
    y_true = np.argmax(testY,axis = 1)

    cm = confusion_matrix(y_true, pred)
    total = sum(sum(cm))
    acc = (cm[0, 0] + cm[1, 1]) / total
    sensitivity = cm[0, 0] / (cm[0, 0] + cm[0, 1])
    specificity = cm[1, 1] / (cm[1, 0] + cm[1, 1])

    print("Acurácia: {:.4f}".format(acc))
    print("Sensitividade: {:.4f}".format(sensitivity))
    print("Especificidade: {:.4f}".format(specificity))

    from mlxtend.plotting import plot_confusion_matrix
    fig, ax = plot_confusion_matrix(conf_mat=cm ,  figsize=(5, 5))
    plt.show()

#### FINALIZA
print("[FIM]")