from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

try:
    driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
    driver.find_element(By.ID, "vLOGIN").send_keys("lucas123test456@gmail.com")
    driver.find_element(By.ID, "vSENHA").send_keys("lucas_test")
    driver.find_element(By.ID, "vSENHA").send_keys(Keys.RETURN)
    msg = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div/div/span/div")))
    assert "Informações de e-mail/cpf ou senha inválidos" in msg.text
finally:
    driver.quit()