from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from pydomo import Domo
import pandas as pd
import os

client_id = os.environ['client_id']
client_secret = os.environ['client_secret']

domo = Domo(client_id, client_secret, api_host='api.domo.com')
car_data = domo.ds_get('11bec3ba-7e78-44c2-82ff-fa9ba0620c59')

print(car_data)

options = Options()
options.add_argument('-headless')  # Execute o Firefox em modo headless

options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.dir", '/')
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "text/csv")
options.set_preference("browser.download.manager.showWhenStarting", False)
# Desativa o visualizador de PDF embutido
options.set_preference("pdfjs.disabled", True)

service = Service(executable_path='/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=options)

# Seu código para usar o driver vai aqui
url = 'https://www.stats.govt.nz/large-datasets/csv-files-for-download/'
driver.get(url)
print(driver.title)

dispersion_tab = WebDriverWait(driver, tempo_espera_max).until(EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/section/div/div/div/article/div/div[2]/article/ul/li[1]/div/div/h3/a')))
dispersion_tab.click()

with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")



driver.quit()
