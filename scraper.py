from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager


profile = webdriver.FirefoxProfile()
profile.set_preference('browser.download.folderList', 2)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.helperApps.neverAsk.saveToDisk', '')
profile.set_preference('browser.download.manager.showAlertOnComplete', False)
profile.set_preference('browser.download.manager.useWindow', False)
profile.set_preference('browser.download.manager.focusWhenStarting', False)
profile.set_preference('browser.download.manager.showWhenStarting', False)
profile.set_preference('browser.download.manager.closeWhenDone', True)

# Instantiate options
options = Options()

# Add extra options
options.add_argument("--window-size=1920,1080")  # Set the window size
options.add_argument("--disable-infobars")  # Disable the infobars
options.add_argument("--disable-popup-blocking")  # Disable pop-ups

# Ignore certificate errors
options.add_argument("--ignore-certificate-errors")
options.add_argument("--incognito")  # Use Chrome in incognito mode

# Classe Service é usada para iniciar um instancia do Chrome WebDriver
service =  Service()

# webdriver.ChromeOptions é usado para definir a preferencia para o navegador do Chrome
# Esta ignorando as configurações que fiz no inicio
#options = webdriver.ChromeOptions()

#Inicia-se a instancia do Chrome WebDrive com as definiçoes do option e service.
#driver =  webdriver.Chrome(service=service, options=options)
#driver = webdriver.Chrome(executable_path='/path/to/driver/chromedriver')
#driver = webdriver.Chrome(ChromeDriverManager().install())
#driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://www.ibge.gov.br/estatisticas/downloads-estatisticas.html'
driver = webdriver.Firefox(
    service=FirefoxService(GeckoDriverManager().install()))
driver.get(url)
print(driver.title)

driver.get('http://github.com')
print(driver.title)
with open('./GitHub_Action_Results.txt', 'w') as f:
    f.write(f"This was written with a GitHub action {driver.title}")
