import smtplib
from valida_Chave import *
from validaPeriodo import *
from datetime import datetime
from cria_Texto_Chave import *
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

#Armazena a saudação
saudacao = validaPeriodo()

#Returna a hora do envio do e-mail
def hora_envio():
    formatacao = "%d/%m/%Y %H:%M:%S"
    hora_atual = datetime.now()
    hora_envio = hora_atual.strftime(formatacao)
    return hora_envio

#Cria o corpo do E-mail de envio
def cria_Email(saudacao):
    try:
        txtHTML = open("envio_email.html", "w+")
        txtHTML.write('''<!DOCTYPE html>
                        <html lang="pt-BR">
                        <html>
                        <body>
                        <p>João, '''+ saudacao +'''<br>
                        Poderia pedir uma nova chave de ativação para acesso ao Netsales, por gentileza?<br><br>
                        <br><b>Atenciosamente,</b>
                        </p>
                        <img width=588 height=151 id="Assinatura" src="cid:Image1.png">
                        </body>
                        </html>''')
        txtHTML.flush()           
        txtHTML.close()
    except:
        print('Não foi possível criar o corpo do E-mail!')


#Cria o corpo do E-mail de reenvio
def reenvia_Email(saudacao):
    try:
        txtHTML = open("reenvio_email.html", "w+")
        txtHTML.write('''<!DOCTYPE html>
                        <html lang="pt-BR">
                        <html>
                        <body>
                        <p>João, '''+ saudacao +'''<br>
                        Ainda não recebemos a chave de ativação do Netsales, pode nos enviar por gentileza?<br><br>
                        <br><b>Atenciosamente,</b>
                        </p>
                        <img width=588 height=151 id="Assinatura" src="cid:Image1.png">
                        </body>
                        </html>''')
        txtHTML.flush()           
        txtHTML.close()
    except:
        print('Não foi possível criar o corpo do E-mail para reenviar!')

#Valida se é envio ou reenvio de E-mail
def envia_email(texto):
    if texto == 'reenviar':
        reenvia_Email(saudacao)
        try:
            with open('Caminho\\reenvio_email.html', 'r') as in_file:
                txtCorpo_Email = in_file.read()
                body = txtCorpo_Email
        except:
            print('Não foi possível abrir o arquivo reenvio_email.html!')
    else:
        cria_Email(saudacao)
        try:
            with open('Caminho\\envio_email.html', 'r') as in_file:
                txtCorpo_Email = in_file.read()
                body = txtCorpo_Email
                #txtChave armazena a leitura do arquivo de texto
        except:
            print('Não foi possível abrir o arquivo envio_email.html!')
            
    #Endereços de E-mails      
    fromaddr = 'remetente@dominio.com.br'
    toaddr = 'destinatario@dominio.com'
    cc = 'destinatario@dominio.com'

    #Cria o e-mail MIME Multipart
    msg = MIMEMultipart('alternative')
    msg_alternativa = MIMEMultipart('alternative')
    msg.attach(msg_alternativa)
    bodyText = MIMEText(body, 'html')
    msg_alternativa.attach(bodyText)

    #Abre a imagem assinatura
    with open('Image1.png', 'rb') as fp:
        msgImage = MIMEImage(fp.read())
        
    #Anexa a iamgem assinatura    
    msg.attach(msg_alternativa)
    msgImage.add_header('Content-ID', '<Image1>')
    msg.attach(msgImage)

    #Salva numa lista os endereços de E-mails
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Cc'] = cc
    msg['Subject'] = "Email Teste Python"
    
    #Configura o servidor SMTP
    s = smtplib.SMTP('smtp.dominio.com.br', 587)
    s.starttls()
    
    #Insere login e senha do E-mail
    s.login(fromaddr, "Senha")

    #Envia E-mail
    text = msg.as_string()
    s.sendmail(msg["From"], msg["To"].split(",") + msg["Cc"].split(","), text)
    s.quit()

    #Salva hora enviada
    ultimaSolicitação = hora_envio()

    #Atualiza a solicitação no arquivo texto da chave
    atualizaSolicitacao(ultimaSolicitação)
    
texto = 'reenviar'
envia_email(texto)
