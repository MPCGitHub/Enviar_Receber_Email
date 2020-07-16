import re
from datetime import date
from Valida_Inbox import *
from validaPeriodo import *
from datetime import datetime
from cria_Texto_Chave import criaTextoChave
from Cria_Envia_Email import *

formatacao = "%d/%m/%Y %H:%M:%S"

#Armazena hora atual
hora_atual = datetime.now()
chave_DataValidade = lerEmailsRecebidos()
criaTextoChave(chave_DataValidade)
print('chave_DataValidade:', chave_DataValidade)

def validaChave():
        try:
                #Abre o arquivo onde se encontra o texto com as informações da Chave de ativação
                with open('Caminho\\Chave.txt', 'r') as in_file:
                        #txtChave armazena a leitura do arquivo de texto
                        txtChave = in_file.read()
                        
                        #validadeChave armazena o texto lido e separando os por linhas
                        txtChaveSplit = txtChave.splitlines()
                        
                        #Encontra no bloco de texto com findall formato padrão de datas(00/00/0000 00:00:00)
                        validaDatas = re.findall(r'\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}:\d{2}', txtChave, re.MULTILINE)
                        
                        #Armazena a data de validade da chave no formato datetime para calcular o tempo da validade
                        validade_fim = datetime.strptime(validaDatas[1],formatacao)
                        
                        #Armazena a data do ultimo envio da solicitação da chave no formato datetime
                        ultimoEnvio = datetime.strptime(validaDatas[-1],formatacao)
                        
                        #Chamada da função para calcular a validade da chave e do ultimo email enviado
                        calculaValidade(validade_fim, ultimoEnvio)
                        
        except:
                print('Não foi possível abrir o arquivo Chave.txt')
                

def calculaValidade(validade_fim, ultimoEnvio):
        #Calcula a diferença entre a validade e a hora atual
        diferenca = hora_atual - validade_fim

        #Calcula a diferença entre o ultimo e a hora atual
        diferencaEnvio = hora_atual - ultimoEnvio

        #Validade se o dia da semana está entre segunda-feira a sexta-feira
        if hora_atual.isoweekday()< 6:
                
                #Valida se a diferença é maior que a ultima data de envio e envia o email
                if diferenca.days == 0:
                        envia_email('enviar')

                #Valida se a diferença é menor que a ultima data de envio e reenvia
                elif diferenca.days >= 0 and validade_fim < ultimoEnvio:
                        envia_email('reenviar')
                else:
                        pass
                           

