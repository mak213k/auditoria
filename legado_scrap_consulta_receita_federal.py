# !pip install dearpygui
# !pip install selenium
# !pip install selenium-recaptcha-solver
# python -m pip install selenium-recaptcha-solver
# pip install hcaptcha-solver
# pip install 2captcha-python
# pip install beautifulsoup4


# from selenium_recaptcha_solver import RecaptchaSolver

# from hcaptcha_solver import hcaptcha_solver

from bs4 import BeautifulSoup
import undetected_chromedriver as uc

# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
# from selenium.webdriver.chrome.options import Options
import time

options = uc.ChromeOptions()
#options = Options()
#options.add_argument('--headless')
#options.add_argument('--window-size=1920x1080')
#options.add_argument("--headless=new")
headers = {
    "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
    "upgrade-insecure-requests":"1",
    "connection":"keep-alive",
    "sec-ch-ua":'"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "host":"solucoes.receita.fazenda.gov.br",
    "sec-ch-ua-platform":"Windows",
    "sec-fetch-dest":"document",
    "set-cookie":"ASPSESSIONIDAESSQQCR=JMEPBDBCIKFCIFEOMCBFOILD; secure; path=/",
    # "set-cookie":"TS0185a354=01fef04d4ecb91efcfaa079d8812a989a8bb979a62524a303635cc49d2d88e38aaec86191afa4b120715dd616c711a6d4948ff7a46b260eaed4f666578ecf95fbac2d50b2b; Path=/; Domain=.solucoes.receita.fazenda.gov.br",
    # "set-cookie":"TSf5592824027=082670627aab2000890340eac60e87f2ca08dd186bf087fa2941ff97654346b06017c05087ccc21c08b137863a1130003a4df8275c2bcb0642dc888f18596eb8e9143cda050ffa9a4b3a432e93457c9f6949a6e428f4a1e10e01f46686946d77; Path=/"
    }
options.headless = False
undetect_driver = uc.Chrome(options=options)

# chrome_driver_path = "chromedriver_win32/"

# options.add_argument(f'--user-agent={test_ua}')

# driver = webdriver.Firefox(options=options)

# driver = webdriver.Firefox()

# solver = RecaptchaSolver(driver=undetect_driver)

# captch_solver = hcaptcha_solver.Captcha_Solver(verbose=True)

undetect_driver.get("https://solucoes.receita.fazenda.gov.br/servicos/cnpjreva/cnpjreva_solicitacao.asp")

print("digitar texto..")
element = undetect_driver.find_element(By.NAME,"cnpj")
element.send_keys('60.195.538/0001-20')



# RecaptchaSolver = undetect_driver.find_element(By.CSS_SELECTOR,'#frmConsulta')
# solver.solve_recaptcha_v2_challenge(iframe=RecaptchaSolver )

# captch_solver.is_captcha_present(undetect_driver)
# captch_solver.solve_captcha(undetect_driver)

# Aqui, o usuário precisa interagir com o hCaptcha manualmente
print("Por favor, resolva o hCaptcha manualmente.")
time.sleep(20)  # tempo para o usuário resolve

form_submit = undetect_driver.find_element(By.CSS_SELECTOR, '#frmConsulta > div:nth-child(4) > div > button')
# form_submit = undetect_driver.find_element(By.NAME, 'search_type')
form_submit.click()

#frmConsulta > div:nth-child(4) > div > button.btn.btn-primary - BOTÃO SUBMIT
#frmConsulta - FORM,
time.sleep(10)  # tempo para o usuário resolve

html=BeautifulSoup(undetect_driver.page_source, 'html.parser')
# log_scrapers = html.find_all("div",class_='#principal > table:nth-child(1) > tbody > tr > td')
print(html.get_text())
print('fim')

# Finaliza o driver
undetect_driver.quit()
print("✅ Fim do scraping.")
exit(0)