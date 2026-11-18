from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import os
import time

erro_login_msg = "/html/body/form/div[2]/div[2]/div/div[1]/div/div/div/div[2]/div/div[3]/div/div/div/div/div[4]/div/div/div/div/span/div"
#checkbox de uma opção da pergunta de idiomas (o texto da opção é um span na mesma linha do checkbox, não um label)
idioma_checkbox = "//div[contains(@id, 'GRID2TABLE') and .//span[normalize-space()='Quais idiomas você tem conhecimento?']]//span[normalize-space()='{}']/ancestor::div[contains(@id, 'GRID3TABLE')]//input[@type='checkbox']"
#onde clicar para marcar/desmarcar a opção (o input fica escondido, quem recebe o clique é o label que envolve ele)
idioma_clique = idioma_checkbox + "/parent::label"
pergunta_idiomas = "//span[normalize-space()='Quais idiomas você tem conhecimento?']"
#campo de data da pergunta de previsão de formatura
formatura_data = "//div[contains(@id, 'GRID2TABLE') and .//span[normalize-space()='Qual sua previsão de formatura?']]//input[contains(@id, 'vRESPOSTA_DATA')]"
#select do Estado Civil e campo do LinkedIn em Dados Adicionais
estado_civil = "//div[contains(@id, 'GRID2TABLE') and .//span[normalize-space()='Estado Civil']]//select[contains(@id, 'vUNICA_ESCOLHA')]"
linkedin = "//div[contains(@id, 'GRID2TABLE') and .//span[normalize-space()='Insira o link do seu perfil no LinkedIn']]//input[contains(@id, 'vRESPOSTA_CURTA')]"
#checkbox de uma opção da pergunta de turno (no portal a pergunta tem "de estudo" repetido mesmo)
pergunta_turno = "//span[normalize-space()='Qual o seu turno de estudo de estudo?']"
turno_checkbox = "//div[contains(@id, 'GRID2TABLE') and .//span[normalize-space()='Qual o seu turno de estudo de estudo?']]//span[normalize-space()='{}']/ancestor::div[contains(@id, 'GRID3TABLE')]//input[@type='checkbox']"
turno_clique = turno_checkbox + "/parent::label"

#funcão: login
def login(driver):
    wait = WebDriverWait(driver, 10)
    driver.get('https://admin.ielcarreiras.com.br/logincandidato.aspx')
    campo_login = wait.until(EC.element_to_be_clickable((By.ID, "vLOGIN")))
    campo_senha = wait.until(EC.element_to_be_clickable((By.ID, "vSENHA")))
    time.sleep(1)  
    campo_login.clear()
    campo_login.send_keys("lucasgomesantunes85@gmail.com")
    campo_senha.clear()
    campo_senha.send_keys("98765lucastest")
    assert campo_login.get_attribute("value") == "lucasgomesantunes85@gmail.com"
    campo_senha.send_keys(Keys.RETURN)

#função: abrir a aba Dados Adicionais do Meu Currículo
def abrir_dados_adicionais(driver):
    wait = WebDriverWait(driver, 10)
    wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
    time.sleep(3)
    wait.until(EC.element_to_be_clickable((By.ID, "Tab_TAB1Containerpanel2"))).click()
    wait.until(EC.visibility_of_element_located((By.XPATH, pergunta_idiomas)))
    time.sleep(2)

#função: reabrir a aba Dados Adicionais depois de salvar
#refresh() depois de salvar volta a aba sem as perguntas, por isso abre de novo pela página inicial
def reabrir_dados_adicionais(driver):
    driver.get('https://admin.ielcarreiras.com.br/hetpaginainicialcurriculo.aspx')
    abrir_dados_adicionais(driver)

#função: conferir quais idiomas estão marcados
def conferir_idiomas(driver, ing, esp, out):
    pergunta = driver.find_element(By.XPATH, pergunta_idiomas)
    assert "Quais idiomas você tem conhecimento?" in pergunta.text
    assert driver.find_element(By.XPATH, idioma_checkbox.format("Inglês")).is_selected() == ing
    assert driver.find_element(By.XPATH, idioma_checkbox.format("Espanhol")).is_selected() == esp
    assert driver.find_element(By.XPATH, idioma_checkbox.format("Outro")).is_selected() == out

#função auxiliar para garantir a pré-condição de idiomas salva no banco
def preparar_idiomas(driver, ing, esp, out):
    wait = WebDriverWait(driver, 10)
    alterou = False
    for opcao, marcar in (("Inglês", ing), ("Espanhol", esp), ("Outro", out)):
        checkbox = driver.find_element(By.XPATH, idioma_checkbox.format(opcao))
        if checkbox.is_selected() != marcar:
            driver.find_element(By.XPATH, idioma_clique.format(opcao)).click()
            time.sleep(1)
            alterou = True
    if alterou:
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)

#função: conferir quais turnos de estudo estão marcados
def conferir_turnos(driver, manha, tarde, noite):
    pergunta = driver.find_element(By.XPATH, pergunta_turno)
    assert "Qual o seu turno de estudo de estudo?" in pergunta.text
    assert driver.find_element(By.XPATH, turno_checkbox.format("Manhã")).is_selected() == manha
    assert driver.find_element(By.XPATH, turno_checkbox.format("Tarde")).is_selected() == tarde
    assert driver.find_element(By.XPATH, turno_checkbox.format("Noite")).is_selected() == noite

#função auxiliar para garantir a pré-condição de turnos salva no banco
def preparar_turnos(driver, manha, tarde, noite):
    wait = WebDriverWait(driver, 10)
    alterou = False
    for opcao, marcar in (("Manhã", manha), ("Tarde", tarde), ("Noite", noite)):
        checkbox = driver.find_element(By.XPATH, turno_checkbox.format(opcao))
        if checkbox.is_selected() != marcar:
            driver.find_element(By.XPATH, turno_clique.format(opcao)).click()
            time.sleep(1)
            alterou = True
    if alterou:
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)

#função auxiliar para garantir a pré-condição de estado civil salva no banco
def preparar_estado_civil(driver, opcao):
    wait = WebDriverWait(driver, 10)
    civil = Select(driver.find_element(By.XPATH, estado_civil))
    if civil.first_selected_option.text != opcao:
        civil.select_by_visible_text(opcao)
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)

#função auxiliar para garantir a pré-condição do LinkedIn salva no banco
def preparar_linkedin(driver, texto):
    wait = WebDriverWait(driver, 10)
    campo = driver.find_element(By.XPATH, linkedin)
    if campo.get_attribute("value") != texto:
        campo.clear()
        campo.send_keys(texto)
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)

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
        login(driver)
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
        driver.find_element(By.ID, "W0035TABLE2_0001").click()
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "gxp0_ifrm")))
        titulo = wait.until(EC.visibility_of_element_located((By.ID, "TEXTBLOCKVAGA")))
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
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.ID, "gxp0_ifrm")))
        aviso = wait.until(EC.visibility_of_element_located((By.ID, "TEXTBLOCK2")))
        assert "Vaga indisponível!" in aviso.text
    finally:
        driver.quit()
ct011()
#fim das CTs do lucassssss <333
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

#31. Alterar estado civil com sucesso
def ct031():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_estado_civil(driver, "Solteiro(a)")
        civil = Select(driver.find_element(By.XPATH, estado_civil))
        assert "Solteiro(a)" in civil.first_selected_option.text
        civil.select_by_visible_text("Casado(a)")
        time.sleep(2)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        civil = Select(driver.find_element(By.XPATH, estado_civil))
        assert "Casado(a)" in civil.first_selected_option.text
    finally:
        driver.quit()
ct031()

#32. Preencher LinkedIn com texto inválido com sucesso
def ct032():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_linkedin(driver, "")
        campo = driver.find_element(By.XPATH, linkedin)
        assert campo.get_attribute("value") == ""
        campo.send_keys("linkedin-invalido")
        time.sleep(2)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, linkedin)
        assert "linkedin-invalido" in campo.get_attribute("value")
    finally:
        driver.quit()
ct032()

#33. Preencher LinkedIn com URL válida com sucesso
def ct033():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_linkedin(driver, "linkedin-invalido")
        campo = driver.find_element(By.XPATH, linkedin)
        assert "linkedin-invalido" in campo.get_attribute("value")
        campo.clear()
        time.sleep(1)
        campo.send_keys("https://www.linkedin.com/in/lucas-teste-iel")
        time.sleep(2)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, linkedin)
        assert "https://www.linkedin.com/in/lucas-teste-iel" in campo.get_attribute("value")
    finally:
        driver.quit()
ct033()

#34. Selecionar Noite como turno de estudo com sucesso
def ct034():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, True, False, False)
        conferir_turnos(driver, True, False, False)
        driver.find_element(By.XPATH, turno_clique.format("Manhã")).click()
        time.sleep(1)
        driver.find_element(By.XPATH, turno_clique.format("Noite")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, False, False, True)
    finally:
        driver.quit()
ct034()

#35. Selecionar Tarde e Noite como turno de estudo com sucesso
def ct035():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, False, True, False)
        conferir_turnos(driver, False, True, False)
        driver.find_element(By.XPATH, turno_clique.format("Noite")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, False, True, True)
    finally:
        driver.quit()
ct035()

#36. Selecionar Manhã e Tarde e Noite como turno de estudo sem sucesso
def ct036():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, False, True, False)
        conferir_turnos(driver, False, True, False)
        driver.find_element(By.XPATH, turno_clique.format("Manhã")).click()
        time.sleep(1)
        driver.find_element(By.XPATH, turno_clique.format("Noite")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Selecione no máximo 2 opções.')]")))
        assert "Selecione no máximo 2 opções." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, False, True, False)
    finally:
        driver.quit()
ct036()

#37. Selecionar Manhã e Tarde como turno de estudo com sucesso
def ct037():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, False, True, False)
        conferir_turnos(driver, False, True, False)
        driver.find_element(By.XPATH, turno_clique.format("Manhã")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, True, True, False)
    finally:
        driver.quit()
ct037()

#38. Selecionar Manhã como turno de estudo com sucesso
def ct038():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, True, True, False)
        conferir_turnos(driver, True, True, False)
        driver.find_element(By.XPATH, turno_clique.format("Tarde")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, True, False, False)
    finally:
        driver.quit()
ct038()

#39. Selecionar Tarde como turno de estudo com sucesso
def ct039():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, False, False, True)
        conferir_turnos(driver, False, False, True)
        driver.find_element(By.XPATH, turno_clique.format("Noite")).click()
        time.sleep(1)
        driver.find_element(By.XPATH, turno_clique.format("Tarde")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, False, True, False)
    finally:
        driver.quit()
ct039()

#40. Selecionar nenhum turno como turno de estudo sem sucesso
def ct040():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        time.sleep(3)
        abrir_dados_adicionais(driver)
        preparar_turnos(driver, False, False, True)
        conferir_turnos(driver, False, False, True)
        driver.find_element(By.XPATH, turno_clique.format("Noite")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Pergunta obrigatória')]")))
        assert "Pergunta obrigatória" in msg.text
        reabrir_dados_adicionais(driver)
        conferir_turnos(driver, False, False, True)
    finally:
        driver.quit()
ct040()
#cts 31-40 do Davi

#41. Selecionar Inglês em conhecimentos de idioma com sucesso
def ct041():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, True, True, False)
        conferir_idiomas(driver, True, True, False)
        driver.find_element(By.XPATH, idioma_clique.format("Espanhol")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, True, False, False)
    finally:
        driver.quit()
ct041()

#42. Selecionar Inglês e Espanhol em conhecimentos de idioma com sucesso
def ct042():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, True, True, True)
        conferir_idiomas(driver, True, True, True)
        driver.find_element(By.XPATH, idioma_clique.format("Outro")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, True, True, False)
    finally:
        driver.quit()
ct042()

#43. Selecionar Inglês e Espanhol e Outro em conhecimentos de idioma com sucesso
def ct043():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, False, False, True)
        conferir_idiomas(driver, False, False, True)
        driver.find_element(By.XPATH, idioma_clique.format("Inglês")).click()
        time.sleep(1)
        driver.find_element(By.XPATH, idioma_clique.format("Espanhol")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, True, True, True)
    finally:
        driver.quit()
ct043()

#44. Selecionar Espanhol e Outro em conhecimentos de idioma com sucesso
def ct044():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, False, True, False)
        conferir_idiomas(driver, False, True, False)
        driver.find_element(By.XPATH, idioma_clique.format("Outro")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, False, True, True)
    finally:
        driver.quit()
ct044()

#45. Selecionar Outro em conhecimentos de idioma com sucesso
def ct045():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, False, True, True)
        conferir_idiomas(driver, False, True, True)
        driver.find_element(By.XPATH, idioma_clique.format("Espanhol")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, False, False, True)
    finally:
        driver.quit()
ct045()

#46. Selecionar Espanhol em conhecimentos de idioma com sucesso
def ct046():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, True, False, False)
        conferir_idiomas(driver, True, False, False)
        driver.find_element(By.XPATH, idioma_clique.format("Inglês")).click()
        time.sleep(1)
        driver.find_element(By.XPATH, idioma_clique.format("Espanhol")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, False, True, False)
    finally:
        driver.quit()
ct046()

#47. Selecionar nenhum idioma em conhecimentos de idioma sem sucesso
def ct047():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, True, False, False)
        conferir_idiomas(driver, True, False, False)
        driver.find_element(By.XPATH, idioma_clique.format("Inglês")).click()
        time.sleep(1)
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Pergunta obrigatória')]")))
        assert "Pergunta obrigatória" in msg.text
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, True, False, False)
    finally:
        driver.quit()
ct047()

#48. Salvar previsão de formatura anterior à data atual com sucesso
def ct048():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, formatura_data)
        campo.send_keys(Keys.CONTROL, "a", Keys.NULL, "01012026")
        driver.find_element(By.XPATH, "//span[normalize-space()='Qual sua previsão de formatura?']").click()
        time.sleep(2)
        assert "01/01/2026" in campo.get_attribute("value")
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, formatura_data)
        assert "01/01/2026" in campo.get_attribute("value")
    finally:
        driver.quit()
ct048()

#49. Salvar previsão de formatura futura com sucesso
def ct049():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, formatura_data)
        campo.send_keys(Keys.CONTROL, "a", Keys.NULL, "01122029")
        driver.find_element(By.XPATH, "//span[normalize-space()='Qual sua previsão de formatura?']").click()
        time.sleep(2)
        assert "01/12/2029" in campo.get_attribute("value")
        driver.find_element(By.ID, "W0216BTNCONFIRMARPERGUNTA").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Informações atualizadas com sucesso." in msg.text
        reabrir_dados_adicionais(driver)
        campo = driver.find_element(By.XPATH, formatura_data)
        assert "01/12/2029" in campo.get_attribute("value")
    finally:
        driver.quit()
ct049()

#50. Acessar a área do candidato após sair da conta sem sucesso
def ct050():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.visibility_of_element_located((By.ID, "W0012TEXTBLOCKBOASVINDAS")))
        time.sleep(2)
        wait.until(EC.element_to_be_clickable((By.XPATH, "//img[@alt='Foto de perfil']"))).click()
        time.sleep(1)
        meus_dados = wait.until(EC.visibility_of_element_located((By.XPATH, "//*[normalize-space()='Meus dados']")))
        sair = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[normalize-space()='Sair']")))
        assert "Meus dados" in meus_dados.text
        assert "Sair" in sair.text
        sair.click()
        assert wait.until(EC.visibility_of_element_located((By.ID, "vLOGIN"))).is_displayed()
        driver.get('https://admin.ielcarreiras.com.br/hetpaginainicialcurriculo.aspx')
        assert wait.until(EC.visibility_of_element_located((By.ID, "vLOGIN"))).is_displayed()
        driver.get('https://admin.ielcarreiras.com.br/HSgpAcessoCurriculo.aspx?hetpaginainicial.aspx')
        assert wait.until(EC.visibility_of_element_located((By.ID, "vLOGIN"))).is_displayed()
        driver.back()
        assert wait.until(EC.visibility_of_element_located((By.ID, "vLOGIN"))).is_displayed()
    finally:
        driver.quit()
ct050()
#cts 41-50 do Gabriel <3

#CTs de restauração da conta: rodam por último para deixar a conta no estado inicial e todos os CTs passarem na próxima execução
#51. Restaurar o Nome Civil como nome de exibição com sucesso (desfaz o CT030 e garante o CT006)
def ct051():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//label[@for='RSCUR_OPCAO_NOME1']"))).click()
        time.sleep(2)
        campo = driver.find_element(By.ID, "RSCUR_NOME")
        campo.clear()
        campo.send_keys("Lucas Gilberto Davi")
        driver.find_element(By.ID, "BTNSALVAR").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        wait.until(EC.visibility_of_element_located((By.ID, "RSCUR_NOME")))
        assert driver.find_element(By.ID, "RSCUR_OPCAO_NOME1").is_selected()
        assert driver.find_element(By.ID, "RSCUR_NOME").get_attribute("value") == "Lucas Gilberto Davi"
        saudacao = driver.find_element(By.XPATH, "/html/body/form/div[2]/div[2]/div/div[2]/div/div/div[4]/div/div/div[2]/span")
        assert "Bem-vindo, Lucas Gilberto Davi" in saudacao.text
    finally:
        driver.quit()
ct051()

#52. Restaurar PCD para Não possui com sucesso (desfaz o CT025)
def ct052():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        wait.until(EC.element_to_be_clickable((By.ID, "W0012TEXTBLOCK2"))).click()
        pcd = Select(wait.until(EC.visibility_of_element_located((By.ID, "GPNES_ID"))))
        pcd.select_by_visible_text("Não possui")
        time.sleep(2)
        driver.find_element(By.ID, "BTNSALVAR").click()
        msg = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[contains(@class, 'gx-success-message')]")))
        assert "Currículo atualizado com sucesso." in msg.text
        driver.refresh()
        pcd = Select(wait.until(EC.visibility_of_element_located((By.ID, "GPNES_ID"))))
        assert "Não possui" in pcd.first_selected_option.text
    finally:
        driver.quit()
ct052()

#53. Restaurar os idiomas para Inglês e Espanhol com sucesso (pré-condição do CT041)
def ct053():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)
        abrir_dados_adicionais(driver)
        preparar_idiomas(driver, True, True, False)
        reabrir_dados_adicionais(driver)
        conferir_idiomas(driver, True, True, False)
    finally:
        driver.quit()
ct053()
#fim dos CTs de restauração