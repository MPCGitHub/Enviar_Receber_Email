import re
import sys
import email
import base64
import imaplib
from email import policy
from datetime import datetime
from dateutil.parser import parse



EMAIL = 'remetente@dominio.com.br'
PASSWORD = 'Senha'
SERVER = 'imap.dominio.com.br'

def conectaServidor():
    try:
        #Cria conexão com servidor Email
        mail = imaplib.IMAP4_SSL(SERVER)
        #Loga no servidor de Email
        mail.login(EMAIL, PASSWORD)
        return mail
    except:
        print("Não foi possivel conectar ao servidor de Emails! " )


def lerEmailsRecebidos():
    #mail recebe a conexão
    mail = conectaServidor()
    
    #Seleciona a Caixa de Entrada
    mail.select('inbox', readonly=True)
    
    #Procura o status e os Ids dos emails enviados do endereço especificado
    status, data = mail.search(None, '(From "RemetenteProcurado@dominio.com.br")')
    
    #Iteração com list comprehension em data para separar dentro da lista os Ids
    mail_ids = [block.split()for block in data]
    #print(mail_ids)
    
    #Iteração da lista onde estão os Ids 
    #e passamos por parametro para serem baixados pela função mail.fetch no formato(RFC822)
    for i in mail_ids[0]:
        status, data = mail.fetch(i, '(RFC822)')
        
    #Iteração em list Comprehension: gera uma lista a partir da iteração em data
    # Valida se response_part veio em formato de tupla que é o padrão com 2 elementos(cabeçalho e conteudo)
    for response_part in data:
        if isinstance(response_part, tuple):

            #No segundo elemento está o conteudo, será convertido em string
            message = email.message_from_bytes(response_part[1])
            
            #Estou extraindo a informação de data e hora do recebimento do email que está nas primeiras linhas
            dateReceived = message['received'].split(';')

            #Separa especificamente no formato data e hora com re.findall()00/00/0000 00:00:00
            recebido = re.findall(r'\d{1,2}\s\w{3}\s\d{4}\s\d{2}:\d{2}:\d{2}', dateReceived[1])

            #Converte em datetime para formatar em hora
            dataRecebida = datetime.strptime(recebido[0], "%d %b %Y %H:%M:%S")

            #Converte em uma string fomatada
            data_envio = dataRecebida.strftime("%d/%m/%Y %H:%M:%S")

            #Valida se é Multipart
            if message.is_multipart():
                mail_content = ''

                #Iteração para retirar o conteúdo 
                for part in message.get_payload():

                    #Se for Multipart retiramos o conteúdo
                    if part.get_content_type() == 'multipart/alternative':

                        #Armazena a primeira parte da mensagem
                        mail_content += str(part.get_payload(0, decode=False))

                        #Cria uma lista com o conteudo
                        conteudo =  mail_content.split('\n')

                        #Armazena o resultado da decodificação do texto
                        conteudoMail = decodificaBase64(conteudo)

                        #Cria uma lista com a chave e data da validade
                        chave_DataValidade = list(extraiValidadeChave(conteudoMail))
                        #Adiciona da data de envio a lista
                        chave_DataValidade.append(data_envio)
                        print('chave_DataValidade', chave_DataValidade)
                        
                    else:
                        mail_content = message.get_payload()
                        
    return chave_DataValidade


def decodificaBase64(conteudo):
    
    #Retira os espaços e cria uma nova lista
    listaConteudo = [novo_conteudo for novo_conteudo in conteudo if novo_conteudo != '']
    try:
        message =''
        
        #Iteração começa a partir do terceiro item, os 2 primeiros são informação do cabeçalho
        #Decodifica o texto que está em base64
        for texto in listaConteudo[2:]:
            base64_bytes = texto.encode('ascii')
            message_bytes = base64.b64decode(base64_bytes)
            message = message + str(message_bytes.decode())
    except UnicodeDecodeError:
        pass
      
    return message.splitlines()      

    
def extraiValidadeChave(conteudoMail):
    #Busca dentro do conteúdo a chave de ativação
    _chave = conteudoMail.index('Chave de Ativação:')+ 1

    #Busca o periodo de validade da chave
    _dataValidade = conteudoMail.index('Período Válido:') + 1

    #Armazena a chave
    chave = conteudoMail[_chave]

    #Armazena a data da validade da chave
    dataValidade = conteudoMail[_dataValidade]
    
    return chave, dataValidade


