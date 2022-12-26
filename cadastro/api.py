# http://127.0.0.1:8000/cadastro/api/docs  =  Swagger

from ninja import ModelSchema, NinjaAPI, Schema, UploadedFile
from .models import Livro
import json
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict  # Converte model para dicionário no python


api = NinjaAPI()


#* Criar uma rota que consiguiremos acessar essa rota e vai me retornar tds os livros que estão cadastrados ali dentro

@api.get('livro/')
def listar(request):
    livro = Livro.objects.all()
    response = [{'id': i.id, 'titulo': i.titulo, 'descricao': i.descricao, 'autor': i.autor} for i in livro]
    print(response)
    return response

# http://127.0.0.1:8000/cadastro/api/livro/

#* Padrão de uso para 1 app

#* Receber um parâmetro pela url ou Swagger, no caso através do {id} que referencia a uma livro que tem seu titulo, descricao e autor
# URL com parâmetro de url

@api.get('livro/{id}')  
def listar_livro(request, id: int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)  

# http://127.0.0.1:8000/cadastro/api/livro/1
# http://127.0.0.1:8000/cadastro/api/livro/2


# URL com parâmetros de consulta

@api.get('livro_consulta/')
def listar_consulta(request, id: int = 1):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)  

# http://127.0.0.1:8000/cadastro/api/livro_consulta/
# http://127.0.0.1:8000/cadastro/api/livro_consulta/?id=2


#* Modelagem de dados, rota que tem classe que herda de esquema

'''class LivroSchema(Schema):
    titulo: str
    descricao: str
    autor: str = None  # Autor vem por padrão como none'''
    
class LivroSchema(ModelSchema):  # É a msm coisa da classe de cima
    class Config:
        model = Livro
        model_fields = "__all__"  # ['titulo', 'descricao']  =  Colocar campo por campo pois __all__ pode acabar revelando um dado sensível


@api.post('livro', response=LivroSchema)
def livro_criar(request, livro: LivroSchema):
    l1 = livro.dict()
    livro = Livro(**l1)
    livro.save()
    # print(livro.dict())
    return livro

'''
# * Para receber lista de livros para cadastrar varios no bd:


from typing import List

@api.post('livro', response=LivroSchema)
def livro_criar(request, livro: List[LivroSchema]):
'''


# * Para caso queira receber um arquivo

@api.post('/file')
def file_upload(request, file:UploadedFile):
    print(file.size)
    return file.size
