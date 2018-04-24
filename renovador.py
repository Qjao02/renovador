
# coding: utf-8

import requests
from bs4 import BeautifulSoup

login = {
    'tmp': '/tmp/filefc9Mz3',
    'IsisScript': 'phl82/026.xis',
    'login': None,
    'pwd': None,
    'submitter': 'Processando...'
}

#recebe os dados de login e senha
print('digite o login')
login['login'] = input()
print('digite a senha')
login['pwd'] = input()


#inicia a sessão
s = requests.Session()
#faz a resquisição post com os dadosdo login
r = s.post('http://www.dibib.ufsj.edu.br/cgi-bin/wxis.exe', data=login)
#requisição para a parte
r = s.get('http://www.dibib.ufsj.edu.br/cgi-bin/wxis.exe?IsisScript=phl82/017.xis&tmp=/tmp/filee5Aw0Y')

html = r.text

#pega o codigo html para achar o codigo dos livros
soup = BeautifulSoup(html,'html')
elements = soup.find_all('a',href=True)

#remove o elemento extra inutil
index = len(elements)
del(elements[len(elements)-1])

# realiza a renovação para cada obra
list = []
for element in elements:
    string = str(element)
    querrysplit = str(string).split('"')
    querry = querrysplit[1]
    
    while querry.find(';') > 0:
        index = querry.find(';')
        querry = querry[:index] +'&'+querry[index+1:]
    try:
        list.append(s.get("http://www.dibib.ufsj.edu.br" + querry))
        print("http://www.dibib.ufsj.edu.br" + querry)
    except:
        print('problema renovação')



