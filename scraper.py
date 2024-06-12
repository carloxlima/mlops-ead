from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

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
