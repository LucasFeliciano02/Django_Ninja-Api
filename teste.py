import requests


file = {'file': open('samba.PNG', 'rb')}  # rb = leitura em binário

response = requests.post('http://127.0.0.1:8000/cadastro/api/file', files=file)

print(f'Tamanho do arquivo em Bytes: {response.text}')