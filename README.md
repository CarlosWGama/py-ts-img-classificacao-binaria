<h1> Algoritmo </h1>

Projeto criado e adaptado do Canal do Sandeco! 

Recomendo a todos acompanharem lá também!

<h2>Instruções</h2>

- A ferramenta reconhece problemas binários, devendo ser inserido as imagens de treinamento dentro da pasta dataset
- Na pasta dataset também deve ser separado em pastas distintas cada conteúdo (Exemplo uma pasta só com fotos de cachorros e outra pasta só com fotos de gato)
- No arquivo train.py deve ser alterada as seguintes variáveis:
```
dataset_folder = "D:\\Documentos\\Python\\cancer\\dataset\\" #Pasta onde estão as fotos apra treinamento
avaliar = True #Faz também a avaliação do modelo
```
- No arquivo predict.py deve ser alterada as seguintes variável imagem:
```
imagem = 'https://urlparasuafoto'
```
- A variavel pode ser tanto um arquivo local ou via url

------
<h2>Conteúdos</h2>

- Bibliotecas para instalar:
```
matplotlib
flask==2.0.1
tensorflow==2.2.0
numpy==1.18.1
pillow==7.1.1
sklearn
```
-------
<h2>Microserviço</h2>

- A pasta microserviço disponibiliza um servidor em flask para analise dos resultados de um modelo já treinado. 
- Também a possibiliade de usá-lo com Docker.


------------------
<p><b>Construído por:</b> Carlos W. Gama (carloswgama.com.br) e adaptado de Sandeco. </p>
<p><b>Licença:</b> MIT</p>