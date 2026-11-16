from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

erro_login_msg = "/html/body/form/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div/div/span/div"

#funcão: login
def login(driver):
        driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
        time.sleep(2)
        campo = driver.find_element(By.ID, "vLOGIN")
        campo.send_keys(Keys.CONTROL, "a", Keys.NULL, Keys.DELETE)
        campo.send_keys("lucasgomesantunes85@gmail.com")
        driver.find_element(By.ID, "vSENHA").send_keys(Keys.CONTROL, "a", Keys.NULL, Keys.DELETE)
        driver.find_element(By.ID, "vSENHA").send_keys("98765lucastest")
        driver.find_element(By.ID, "vSENHA").send_keys(Keys.RETURN)

#Começo das CTs do lucas <3 :3 >w< ;P
#1. Entrar com e-mail e senha inválidos sem sucesso
def ct001():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
        driver.find_element(By.ID, "vLOGIN").send_keys("lucas123test456@gmail.com")
        driver.find_element(By.ID, "vSENHA").send_keys("lucas_test")
        driver.find_element(By.ID, "vSENHA").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, erro_login_msg)))
        assert "Informações de e-mail/cpf ou senha inválidos" in msg.text
    finally:
        driver.quit()
ct001()

#2. Cadastrar senha com sequência de números sem sucesso
def ct002():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("Abc12345!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("Abc12345!")
        driver.find_element(By.ID, "BTNENTRAR").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, erro_login_msg)))
        assert "Senha não pode conter sequencia de números" in msg.text
    finally:
        driver.quit()
ct002()

#3. Cadastrar com e-mail inválido sem sucesso
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

#4. Cadastrar com senha de menos de oito caracteres sem sucesso
def ct004():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("Ab1!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("Ab1!")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, erro_login_msg)))
        assert "Senha informada deve conter no mínimo oito caracteres com letras e números" in msg.text
    finally:
        driver.quit()
ct004()

#5. Cadastrar com confirmação de senha divergente sem sucesso
def ct005():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/cadastrocandidato.aspx')
        driver.find_element(By.ID, "vNOVOEMAIL").send_keys("20260930@example.com")
        driver.find_element(By.ID, "vNOVASENHA").send_keys("SenhaForte@82")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys("OutraSenha@82")
        driver.find_element(By.ID, "vNOVASENHA2").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, erro_login_msg)))
        assert "Senhas informadas são diferentes" in msg.text
    finally:
        driver.quit()
ct005()

#6. Entrar com e-mail e senha válidos com sucesso
def ct006():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
        driver.find_element(By.ID, "vLOGIN").send_keys("lucasgomesantunes85@gmail.com")
        driver.find_element(By.ID, "vSENHA").send_keys("98765lucastest")
        driver.find_element(By.ID, "vSENHA").send_keys(Keys.RETURN)
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "/html/body/form/div[2]/div[2]/div/div[2]/div/div/div[4]/div/div/div[2]/span")))
        assert "Bem-vindo, Lucas Gilberto Davi" in msg.text
    finally:
        driver.quit()
ct006()

#7. Salvar o currículo sem nome completo sem sucesso
def ct007():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "RSCUR_NOME")))
        driver.find_element(By.ID,"RSCUR_NOME").clear()
        driver.find_element(By.ID, "BTNSALVAR").click()
        msg = wait.until(EC.visibility_of_element_located((By.ID, "RSCUR_NOME_Balloon")))
        assert "Nome Completo deve ser informado" in msg.text
    finally:
        driver.quit()
ct007()

#8. Pesquisar uma vaga existente pelo título com sucesso pelo centro de oportunidades
def ct008():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.visibility_of_element_located((By.ID, "W0012TEXTBLOCKBOASVINDAS")))
        driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[2]/div/div/div[1]/ul/li[3]/a").click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "W0035vPESQUISA")
        campo.send_keys("2378 - Estágio Técnico e/ou Superior em Engenharia Mecânica e Eletromecânica - Matutino")
        campo.send_keys(Keys.RETURN)
        time.sleep(3)
        titulo = driver.find_element(By.ID, "W0035TEXTBLOCKTITULO_0001")
        titulo.click()
        time.sleep(2)
        titulo = driver.find_element(By.ID, "TEXTBLOCKVAGA")
        assert "2378 - Estágio Técnico e/ou Superior em Engenharia Mecânica e Eletromecânica - Matutino" in titulo.text
    finally:
        driver.quit()
ct008()

#9. Pesquisar um título sem vagas correspondentes no centro de oportunidades
def ct009():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.visibility_of_element_located((By.ID, "W0012TEXTBLOCKBOASVINDAS")))
        driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[2]/div/div/div[1]/ul/li[3]/a").click()
        time.sleep(2)
        campo = driver.find_element(By.ID, "W0035vPESQUISA")
        campo.send_keys("zzzx_vaga_inexistente_20260930")
        campo.send_keys(Keys.RETURN)
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div[5]/div/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[5]/div/div/div[2]")
        assert "Nenhuma oportunidade encontrada." in msg.text
    finally:
        driver.quit()
ct009()

#11. Consultar detalhes da vaga 2284 sem sucesso
def ct011():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.visibility_of_element_located((By.ID, "W0012TEXTBLOCKBOASVINDAS")))
        time.sleep(2)
        driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div[7]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[3]/div/div/div/div/div/div[1]/span").click()
        time.sleep(1)
        driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div[7]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[3]/div/div/div/div/div/div[2]/span").click()
        time.sleep(1)
        driver.find_element(By.XPATH,"/html/body/form/div[2]/div[2]/div/div[3]/div/div/div/div/div[2]/div/div[7]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[1]/div/div[2]/div[1]/div/div/div/div/div[2]/div/div[4]/div/div/div[1]/div/div/div/div/table/tbody/tr/td[1]/p/span/a" ).click()
        time.sleep(2)
        driver.find_element(By.ID, "BTNDETALHES").click()
        time.sleep(2)
        aviso = driver.find_element(By.ID, "TEXTBLOCK2")
        assert "Vaga indisponível!" in aviso.text
    finally:
        driver.quit()
ct011()

#21. Desistir da candidatura da vaga 2380 com sucesso
def ct021():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        driver.find_element(By.ID, "Tab_W0024TAB1Containerpanel2").click()
        time.sleep(3)
        situacao = driver.find_element(By.ID, "span_W0024W0032vSITUACAO_0001")
        assert "Processo Seletivo Aberto" in situacao.text
        driver.find_element(By.ID, "W0024W0032vIMGCANCEL_0001").click()
        time.sleep(2)
        driver.switch_to.alert.accept()
        time.sleep(3)
        situacao = driver.find_element(By.ID, "span_W0024W0032vSITUACAO_0001")
        assert "Candidatura Pendente" in situacao.text
        driver.find_element(By.ID, "W0024W0032vIMGCANCEL_0001").click()
        time.sleep(2)
        driver.switch_to.alert.accept()
        time.sleep(3)
        situacao = driver.find_element(By.ID, "span_W0024W0032vSITUACAO_0001")
        assert "Processo Seletivo Aberto" in situacao.text
        driver.refresh()
        time.sleep(3)
        driver.find_element(By.ID, "Tab_W0024TAB1Containerpanel2").click()
        time.sleep(3)
        situacao = driver.find_element(By.ID, "span_W0024W0032vSITUACAO_0001")
        assert "Processo Seletivo Aberto" in situacao.text
    finally:
        driver.quit()
ct021()

#22. Alterar telefone com sucesso
def ct022():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_TEL_CELULAR")
        campo.clear()
        time.sleep(2)
        campo.send_keys("98999991111")
        time.sleep(2)
        assert "(98) 99999-1111" in campo.get_attribute("value")
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_TEL_CELULAR")
        assert "(98) 99999-1111" in campo.get_attribute("value")
    finally:
        driver.quit()
ct022()

#23. Alterar telefone com número incompleto sem sucesso
def ct023():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_TEL_CELULAR")
        campo.clear()
        time.sleep(2)
        campo.send_keys("98999")
        time.sleep(2)
        assert "(98) 999" in campo.get_attribute("value")
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.ID, "RSCUR_TEL_CELULAR_Balloon")
        assert "Celular deve ser informado" in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_TEL_CELULAR")
        assert "(98) 99999-1111" in campo.get_attribute("value")
    finally:
        driver.quit()
ct023()

#24. Alterar data de nascimento com sucesso
def ct024():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_DATA_NASCIMENTO")
        #clear() deixa a máscara vazia "  /  /    " no campo e bloqueia a digitação, por isso seleciona tudo e digita na mesma chamada
        campo.send_keys(Keys.CONTROL, "a", Keys.NULL, "15032005")
        driver.find_element(By.ID, "RSCUR_EMAIL").click()
        time.sleep(2)
        assert "15/03/2005" in campo.get_attribute("value")
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_DATA_NASCIMENTO")
        assert "15/03/2005" in campo.get_attribute("value")
    finally:
        driver.quit()
ct024()

#25. Alterar PCD de Não possui para Sim com sucesso
def ct025():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        pcd = Select(driver.find_element(By.ID, "GPNES_ID"))
        pcd.select_by_visible_text("Sim")
        time.sleep(2)
        assert driver.find_element(By.ID, "RSCUR_DES_NECESSIDADE").is_displayed()
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        assert driver.find_element(By.ID, "RSCUR_DES_NECESSIDADE").is_displayed()
        pcd = Select(driver.find_element(By.ID, "GPNES_ID"))
        assert "Sim" in pcd.first_selected_option.text
    finally:
        driver.quit()
ct025()

#26. Alterar endereço com sucesso
def ct026():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_ENDERECO")
        campo.clear()
        time.sleep(2)
        campo.send_keys("Avenida dos Holandeses")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_ENDERECO")
        assert "Avenida dos Holandeses" in campo.get_attribute("value")
    finally:
        driver.quit()
ct026()

#27. Alterar número com sucesso
def ct027():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_NUMERO")
        campo.clear()
        time.sleep(2)
        campo.send_keys("1500")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_NUMERO")
        assert "1500" in campo.get_attribute("value")
    finally:
        driver.quit()
ct027()

#28. Alterar complemento com sucesso
def ct028():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_COMPLEMENTO")
        campo.clear()
        time.sleep(2)
        campo.send_keys("Apartamento 302")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_COMPLEMENTO")
        assert "Apartamento 302" in campo.get_attribute("value")
    finally:
        driver.quit()
ct028()

#29. Alterar bairro com sucesso
def ct029():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_BAIRRO")
        campo.clear()
        time.sleep(2)
        campo.send_keys("Renascença")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        time.sleep(3)
        campo = driver.find_element(By.ID, "RSCUR_END_BAIRRO")
        assert "Renascença" in campo.get_attribute("value")
    finally:
        driver.quit()
ct029()

#30. Preencher nome social com sucesso
def ct030():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        time.sleep(3)
        driver.find_element(By.XPATH, "//label[@for='RSCUR_OPCAO_NOME2']").click()
        time.sleep(2)
        social = driver.find_element(By.ID, "RSCUR_NOME")
        civil = driver.find_element(By.ID, "RSCUR_CIVIL")
        social.clear()
        time.sleep(2)
        social.send_keys("Lucas Davi")
        civil.send_keys(Keys.CONTROL, "a", Keys.NULL, "Lucas Gilberto Davi")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        time.sleep(2)
        msg = driver.find_element(By.XPATH, "//div[contains(@class, 'gx-success-message')]")
        assert "Currículo atualizado com sucesso." in msg.text
        saudacao = driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[2]/div/div/div[4]/div/div/div[2]/span")
        assert "Bem-vindo, Lucas Davi" in saudacao.text
        driver.refresh()
        time.sleep(3)
        assert driver.find_element(By.ID, "RSCUR_OPCAO_NOME2").is_selected()
        social = driver.find_element(By.ID, "RSCUR_NOME")
        assert "Lucas Davi" in social.get_attribute("value")
        civil = driver.find_element(By.ID, "RSCUR_CIVIL")
        assert civil.get_attribute("value") == "Lucas Gilberto Davi"
    finally:
        driver.quit()
ct030()
#fim das CTs do lucassssss <333

