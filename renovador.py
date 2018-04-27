
# coding: utf-8

# ## Parte responsável por realizar as requisições

import requests
import time
import sys
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders




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

#criando a msg para o email
responseMessage = []
for element in response :
    soap = BeautifulSoup(element.text,'html')
    responseMessage.append(soap.find('h2').text)


status = []
soap = BeautifulSoup(r.text,'html')
status = soap.find_all('td',width="95%",align="left")

responseForEmail = []
i = 0
j = 0
while i < len(responseMessage):
    responseForEmail.append(status[j])
    responseForEmail.append(status[j+1])
    responseForEmail.append(responseMessage[i])
    j = j+2
    i = i+1

emailContent = ''
i = 0

while ( i+1 < len (responseForEmail)):
    emailContent = emailContent + (' Livro: ' + str(responseForEmail[i+1].text) + ' Status: ' + str(responseForEmail[i].text) + str('\n' + responseForEmail[i+2]+'\n'))
    i = i+3


#parte responsavel por enviar a notificacao

myEmail = sys.argv[3]
emailPass = sys.argv[4]
senderEmailAddress = myEmail
password = emailPass
receiverEmailAddress = myEmail

#subject do email 
emailSubjectLine = 'Renovação Livro biblioteca'

#configurando a mensagem para o email 
msg = MIMEMultipart()
msg['From'] = senderEmailAddress
msg['To'] = receiverEmailAddress
msg['Subject'] = 'Livros Renovação'
 
emailBody = emailContent
msg.attach(MIMEText(emailBody, 'plain'))
 
emailContent = msg.as_string()

#verifica o servidor smtp
if((myEmail.find('@outlook.com') > 1 or myEmail.find('@hotmail.com') > 1)):
    server = smtplib.SMTP('smtp-mail.outlook.com:587')
else:
    server = smtplib.SMTP('smtp-mail.gmail.com:587')
    
server.starttls()
server.login(senderEmailAddress, password)
 
server.sendmail(senderEmailAddress, receiverEmailAddress, emailContent)
server.quit()

