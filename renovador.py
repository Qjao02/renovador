
# coding: utf-8

# In[2]:



# coding: utf-8

import requests
import time
import sys
from bs4 import BeautifulSoup



login = {
    'tmp': '/tmp/filefc9Mz3',
    'IsisScript': 'phl82/026.xis',
    'login': None,
    'pwd': None,
    'submitter': 'Processando...'
}

#recebe os dados de login e senha
login['login'] = sys.argv[1]
login['pwd'] = sys.argv[2]

#inicia a sessão
s = requests.Session()
#faz a resquisição post com os dadosdo login
r = s.post('http://www.dibib.ufsj.edu.br/cgi-bin/wxis.exe', data=login)
#requisição para a parte
soap = BeautifulSoup(r.text,'html')
listLinks = soap.find_all('a',href = True)
link1 = str(listLinks[1])




#localizando o tmp file e realizando seu parse

link1.find('tmp=')
tmpFile = str(link1[56:].split()[0])
tmpFile = tmpFile[:len(tmpFile)-1]

#requisicao para o segundo link do dibib
link2request = 'http://www.dibib.ufsj.edu.br/cgi-bin/wxis.exe?IsisScript=phl82/017.xis&'+tmpFile
r = s.get(link2request)

# localizando todos os codigos dos livros alugados

soap = BeautifulSoup(r.text,'html')
listLinks = soap.find_all('a',href = True)

index = len(listLinks)
del(listLinks[index-1])

response = []
#realizando a requisicao para cada livro alugado
for element in listLinks:
    string = str(element).split(';')[1]
    bookCode = string.split('&')[0]
    response.append(s.get('http://www.dibib.ufsj.edu.br/cgi-bin/wxis.exe?IsisScript=phl82/037.xis&' + bookCode +'&acv=001&'+tmpFile))

#print resposta do servidor
for element in response:
    print(element.text)

