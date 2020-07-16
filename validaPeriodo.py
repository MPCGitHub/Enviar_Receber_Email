from datetime import date
from datetime import datetime
from datetime import timedelta

formatacao = "%d/%m/%Y %H:%M:%S"
hora_atual = datetime.now()
horas = hora_atual.strftime("%H:%M:%S")

#Função pra validar a hora atual para apresentar a saudação correta no Email
def validaPeriodo():
    manha = "11:59:59"
    tarde = "17:59:59"
    noite = "23:59:59"
    if(horas > tarde) and (horas < noite):
        saudacao = "Boa noite!"
    if(horas > manha) and (horas < tarde):
        saudacao = "Boa tarde!"
    if(horas < manha):
        saudacao = "Bom dia!"
        
    return saudacao


