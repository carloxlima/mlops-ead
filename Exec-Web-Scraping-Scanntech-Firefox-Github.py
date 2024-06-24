print('antes import')

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pathlib import Path
import time
import pandas as pd
from pydomo import Domo
import os
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import locale
from babel.dates import format_date, get_month_names
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service as FirefoxService

print('depois import')
# Criação das pastas de aramazenamento dos arquivos baixados

if not os.path.exists('Scanntech'):
    os.mkdir('Scanntech')

if not os.path.exists('Scanntech/downloads'):
    os.mkdir('Scanntech/downloads')

if not os.path.exists('Scanntech/concluidos'):
    os.mkdir('Scanntech/concluidos')


print('Antes variaveis')

# Variaveis
tempo_espera_max = 30
email = os.environ['email']
password = os.environ['password']
report_name = 'Scanntech_' + datetime.today().strftime("%m%d%Y_%H%M%S")
dates = ['janeiro de 2024']
cliente_id = os.environ['client_id']
secret = os.environ['client_secret']
dataset = '45057122-6f4b-4c29-ac78-614bb77837f5'
download_path = r'Scanntech/downloads'
download_path_destiny = r'Scanntech/concluidos'
url_01 = os.environ['url_01']
url_02 = os.environ['url_02']
count = 0

print('Depois variaveis')

# Gera a lista de datas
list_dates = []
#dates = []

print('Antes funcoes')

def geraListaDatas(start_date, end_date):
    global list_dates, dates

    # Define o locale para português do Brasil
    locale.setlocale(locale.LC_TIME, 'pt_BR.UTF-8')

    while start_date <= end_date:
        data_formatada = format_date(
            start_date, format="MMMM 'de' yyyy", locale='pt_BR')
        # list_dates.append(start_date.strftime("%B de %Y")) # Descartei ess opção pq o "Ç" estava indo zuado.
        list_dates.append(data_formatada)
        start_date += relativedelta(months=1)

    dates = list_dates
    # Imprime a lista de datas formatadas
    print(list_dates)

# Função para verificar se o download foi concluído
def is_download_complete(download_dir):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 1800:  # Limite de tempo de 120 segundos para o download
        time.sleep(1)
        dl_wait = False
        files = os.listdir(download_dir)
        for fname in files:
            if fname.endswith('.part'):  # firefox
                dl_wait = True
        seconds += 1
    return not dl_wait


def nome_para_numero_mes(nome_mes, locale='pt_BR'):
    # Obtém os nomes dos meses na localização especificada
    meses = get_month_names(locale=locale)
    meses_invertido = {v.lower(): k for k, v in meses.items()}

    try:
        return str(meses_invertido[nome_mes.lower()]).rjust(2, '0')
    except KeyError:
        return "Nome do mês inválido"

print('Depois funcoes')
