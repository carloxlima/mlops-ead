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


# Criação das pastas de aramazenamento dos arquivos baixados

if not os.path.exists('Scanntech'):
    os.mkdir('Scanntech')

if not os.path.exists('Scanntech/downloads'):
    os.mkdir('Scanntech/downloads')

if not os.path.exists('Scanntech/concluidos'):
    os.mkdir('Scanntech/concluidos')


print('Hello')
