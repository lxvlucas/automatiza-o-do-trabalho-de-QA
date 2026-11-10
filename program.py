from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

XPATH_MSG = "/html/body/form/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div/div/span/div"

def ct001():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
        driver.find_element(By.ID, "vLOGIN").send_keys("lucas123test456@gmail.com")
        driver.find_element(By.ID, "vSENHA").send_keys("lucas_test")
        driver.find_element(By.ID, "vSENHA").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_MSG)))
        assert "Informações de e-mail/cpf ou senha inválidos" in msg.text
    finally:
        driver.quit()
ct001()

def ct002():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("Abc12345!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("Abc12345!")
        driver.find_element(By.ID, "BTNENTRAR").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_MSG)))
        assert "Senha não pode conter sequencia de números" in msg.text
    finally:
        driver.quit()
ct002()

def ct003():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get("https://admin.ielcarreiras.com.br/cadastrocandidato.aspx")
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("invalido")
        driver.find_element(By.ID, "vNOVASENHA").send_keys(".")
        msg = wait.until(EC.visibility_of_element_located((By.ID, "vNOVOEMAIL_Balloon")))
        assert "O valor de Novo Email não coincide com o padrão especificado" in msg.text
    finally:
        driver.quit()
ct003()

def ct004():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("Ab1!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("Ab1!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, XPATH_MSG)))
        assert "Senha informada deve conter no mínimo oito caracteres com letras e números" in msg.text
    finally:
        driver.quit()
ct004()

def ct005():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("SenhaForte@82")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("OutraSenha@82")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.ID, XPATH_MSG)))
        assert "Senhas informadas são diferentes" in msg.text
    finally:
        driver.quit()