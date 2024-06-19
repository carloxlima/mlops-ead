from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
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

service = Service(executable_path='/usr/local/bin/geckodriver')
driver = webdriver.Firefox(service=service, options=options)

# Seu código para usar o driver vai aqui
url = 'https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html'
driver.get(url)
print(driver.title)
with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")



driver.quit()
