# http://127.0.0.1:8000/cadastro/api/docs  =  Swagger


from ninja import NinjaAPI
from .models import Livro
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict  # Converte model para dicionário no python

# pip install orjson
import orjson  # Biblioteca orjson para fazer o parser mais rápida que o json para fazer a serealização de dados 
from ninja.parser import Parser
from django.http import HttpRequest


class ORJSONParser(Parser):
    def parse_body(self, request: HttpRequest):
        return orjson.loads(request.body)


api = NinjaAPI(parser=ORJSONParser())

# Criar uma rota que consiguiremos acessar essa rota e vai me retornar tds os livros que estão cadastrados ali dentro

@api.get('livro/')
def listar(request):
    livro = Livro.objects.all()
    response = [{'id': i.id, 'titulo': i.titulo, 'descricao': i.descricao, 'autor': i.autor} for i in livro]
    print(response)
    return response


# Receber um parâmetro pela url ou Swagger, no caso através do {id} colocado que corresponde a uma livro que tem seu titulo, descricao e autor

@api.get('livro/{id}')
def listar_livro(request, id: int):
    livro = get_object_or_404(Livro, id=id)
    return model_to_dict(livro)  
