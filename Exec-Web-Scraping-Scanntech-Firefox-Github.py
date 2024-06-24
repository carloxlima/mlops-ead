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

dates_input = dates
recursive=0

if recursive == 1:
    caminho_arquivos = download_path_destiny
    arquivos = pd.DataFrame(columns=['files', 'name', 'mtime'])
    for filename in Path(caminho_arquivos).glob('*.csv'):
        new_row = {'files': str(
            filename), 'name': filename.name, 'mtime': filename.stat().st_mtime}
        arquivos = pd.concat(
            [arquivos, pd.DataFrame([new_row])], ignore_index=True)

    dates_compare = []

    for index, row in arquivos.iterrows():
        name = row['name']
        name_split = name.split('_')
        name_date = name_split[0] + ' '+name_split[1]+' '+name_split[2]
        dates_compare.append(name_date)

    datas_faltantes = [
        elemento for elemento in dates if elemento not in dates_compare]
    dates_input = datas_faltantes

options = Options()
options.add_argument('-headless')  # Execute o Firefox em modo headless

options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", download_path)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
options.set_preference("browser.download.manager.showWhenStarting", False)
# Desativa o visualizador de PDF embutido
options.set_preference("pdfjs.disabled", True)

print('antes do drive')

service = FirefoxService(executable_path='/usr/local/bin/geckodriver')

print('antes do drive2')

driver = webdriver.Firefox(service=service, options=options)

print('depois do drive')

url = url_01

driver.get(url)
print('\n')
print(driver.title)

try:

    print('try')
    # Wait for the login page to load and enter the email and password
    email_field = WebDriverWait(driver, tempo_espera_max).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#username'))
    )
    email_field.send_keys(email)

    password_field = WebDriverWait(driver, tempo_espera_max).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#password'))
    )
    password_field.send_keys(password)

    login_button = WebDriverWait(driver, tempo_espera_max).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#kc-login'))
    )
    login_button.click()

    time.sleep(10)  # Wait for the search results to load

    for date in dates_input:

        print('Loop for')
        url = url_02
        driver.get(url)

        time.sleep(10)  # Wait for the search results to load

        # Wait for the report page to load and switch to the iframe
        iframe = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#iframeHojaReporte'))
        )
        driver.switch_to.frame(iframe)

        # Click on the "Dispersao PDV" tab
        dispersion_tab = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@widgetid="tableauTabbedNavigation_tab_1"]'))
        )
        dispersion_tab.click()
        print('loop for 01')
        time.sleep(20)  # Wait for the search results to load

        # Encontra o elemento de filtro de reset e deixa ele visivel
        elemento = driver.find_element(
            By.XPATH, '//*[@id="tableau_base_widget_LegacyQuantitativeQuickFilter_0"]/div/div[1]/span[1]/span/span')

        # Execute o JavaScript para alterar o estilo do elemento
        driver.execute_script(
            "arguments[0].style.display = 'block';", elemento)

        # Click om the reset filter
        reset_filter = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#dijit_form_Button_162'))
        )
        reset_filter.click()
        print('loop for 02')
        time.sleep(20)  # Wait for the search results to load
        driver.save_screenshot("image_reset_filter.png")

        # Click on the "Filter" button
        filter_button = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#tabZoneId28'))
        )
        filter_button.click()

        # Clear the existing date selections
        checkbox = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="checkbox"]'))
        )
        checkbox.click()
        checkbox.click()
        print('loop for 03')
        # Enter the date in the search field
        search_field = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#tableau_base_widget_LegacyCategoricalQuickFilter_35_textbox'))
        )

        search_field.click()

        # Envia Ctrl + A para selecionar todo o texto
        search_field.send_keys(Keys.CONTROL, 'a')

        # Envia a tecla Del para apagar o texto selecionado
        search_field.send_keys(Keys.DELETE)
        print('loop for 04')
        # Envia a data para o campo de busca
        # Enter the date in the search field
        search_field.click()
        search_field.send_keys(date)

        time.sleep(15)  # Wait for the search results to load

        # Select the checkbox for the desired date
        checkbox = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@type="checkbox"]'))
        )
        checkbox.click()
        print('loop for 05')
        # Click the "Apply" button
        apply_button = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '/html/body/div[7]/div[3]/button[2]'))
        )
        apply_button.click()

        time.sleep(60)  # Wait for the search results to load

        # Wait for the report to load and click on the body to close the filter window
        body = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'body'))
        )
        #body.click()
        # Press Escape to close the filter window
        body.send_keys(Keys.ESCAPE)
        print('loop for 06')
        time.sleep(10)  # Wait for the search results to load

        # Click on the download table twice to enable the download button
        download_table = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabZoneId87"]/div'))
        )
        download_table.click()
        print('loop for 07')
        time.sleep(10)  # Wait for the search results to load

        download_table.click()

        time.sleep(10)  # Wait for the search results to load

        # Click on the download button
        download_button = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#download-ToolbarButton'))
        )
        download_button.click()
        print('loop for 08')
        # Click the "Data" button in the download dialog
        data_button = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="DownloadDialog-Dialog-Body-Id"]/div/fieldset/button[2]'))
        )
        data_button.click()

        driver.save_screenshot("troca_janela.png")
        
        # Switch to the new download window
        window_handles = driver.window_handles
        new_window_handle = window_handles[1]
        driver.switch_to.window(new_window_handle)
        print('loop for 09')
        # driver.save_screenshot("image_download" + datetime.today().strftime("%m%d%Y_%H%M%S")+".png")

        # Wait for the download to complete and find the download link
        download_link = WebDriverWait(driver, tempo_espera_max).until(
            EC.presence_of_element_located(
                (By.XPATH, '//*[@id="tabContent-panel-summary"]/div[1]/div[2]/a'))
        )
        # Click the download link
        download_link.click()
        print('loop for 10')
        if is_download_complete(download_path):
            print('loop for 11')
            # Check for downloaded files and rename the downloaded file
            downloaded_files = None
            while downloaded_files is None:
                downloaded_files = pd.DataFrame(columns=['files', 'mtime'])
                print('loop for 12')
                time.sleep(30)  # Wait for the search results to load
                for filename in Path(download_path).glob('*.csv'):
                    # print(filename.name)
                    new_row = {'files': str(filename),
                                'mtime': filename.stat().st_mtime}
                    downloaded_files = pd.concat(
                        [downloaded_files, pd.DataFrame([new_row])], ignore_index=True)
                time.sleep(15)
            print('loop for 13')
            display(downloaded_files)

            if not downloaded_files.empty:
                print('loop for 14')
                old_file_name = downloaded_files['files'].iloc[0]
                new_file_name = f"{date.replace(' ', '_')}_{report_name}.csv"
                Path(old_file_name).rename(
                    Path(download_path_destiny) / new_file_name)
        else:
            print("O download não foi concluído no tempo esperado.")

        # Close the new download window and switch back to the main window
        driver.close()
        window_handles = driver.window_handles

        if len(window_handles) > 1:
            driver.switch_to.window(window_handles[-1])
            driver.close()

        window_handles = driver.window_handles

        driver.switch_to.window(window_handles[0])

except:
    count += 1
    print(count)
    # Close the Chrome driver
    driver.quit()
    #WebScrapingScanntech(dates, download_path,download_path_destiny, tempo_espera_max, 1)

# Close the Chrome driver
driver.quit()


print('depois chamada funcao webscraping')

