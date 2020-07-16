import re
import os.path
from datetime import datetime
from Valida_Inbox import *

formatacao = "%d/%m/%Y %H:%M:%S"
caminho = 'Caminho\\Chave.txt'

#Função cria o texto no formato padrão para ser lido posteriormente
#Recebe por parametro: chave,data_inicio, data_fim, hora_envio
def criaTextoChave(chave_DataValidade):
    try:
        txtChave = open(caminho, 'w')
        txtChave.write("EMPRESA MPCDEVENVOLVIMENTO LTDA\n\n")
        txtChave.write("Chave de Ativação:\n\n")
        txtChave.write(chave_DataValidade[0]+"\n\n")
        txtChave.write("Período Válido:\n\n")
        txtChave.write(chave_DataValidade[1]+ "\n\n")
        txtChave.write("Ultima solicitação Chave de Ativação:"+ chave_DataValidade[2] +"")
        txtChave.flush()
        txtChave.close()
        print('Criado com sucesso!')
    except:
        print('Não foi possível criar o arquivo Chave.txt')
      

def atualizaSolicitacao(ultimaSolicitação):
    if os.path.exists(caminho):
        try:
            with open(caminho, 'r') as in_file:
                txtChave = in_file.read()
                txtChaveSplit = txtChave.splitlines()
                validaDatas = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}', txtChave, re.MULTILINE)
                ultimaData = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}', ultimaSolicitação)
                hora_atual = datetime.now()
                chave_DataValidade = []
                chave = txtChaveSplit.index('Chave de Ativação:')+ 2
                chave_DataValidade.append(txtChaveSplit[chave])
                periodoValido = txtChaveSplit.index('Período Válido:')+ 2
                chave_DataValidade.append(txtChaveSplit[periodoValido])
                ultimoEnvio = datetime.strptime(validaDatas[-1],formatacao)
                ultimaSolicitação = datetime.strptime(str(ultimaData[0]),formatacao)
                chave_DataValidade.append(str(ultimaData[0]))
                if ultimoEnvio < ultimaSolicitação:
                    criaTextoChave(chave_DataValidade)
                    return
        except:
            print('Não foi possível abrir o arquivo Chave.txt')
    else:
        criaTextoChave(chave_DataValidade)
        

