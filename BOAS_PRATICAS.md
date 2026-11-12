# Boas práticas para IAs neste projeto

Este projeto automatiza casos de teste (CTs) do Portal do Candidato do IEL com **Selenium + Python**.
Todo o código vive em `program.py`. Ao alterar ou adicionar testes, **mantenha a lógica e a arquitetura
que já existem**. Não reorganize o projeto por conta própria.

---

## 1. Regra de ouro

> Faça o que foi pedido, no estilo que já existe em `program.py`.

- **Não** converta para `pytest`, classes, Page Object, `unittest` ou qualquer outro padrão, a menos que o usuário peça.
- **Não** divida `program.py` em vários arquivos, a menos que o usuário peça.
- **Não** refatore CTs existentes que não fazem parte do pedido.
- **Não** renumere CTs. A numeração acompanha a planilha/documento de casos de teste do usuário
  (por exemplo, o CT010 não existe hoje e o próximo após o CT009 é o CT011). Não "preencha" números faltando.
- Responda e comente em **português do Brasil**.

---

## 2. Arquitetura de `program.py`

Ordem do arquivo, de cima para baixo:

1. **Imports** (`selenium`, `By`, `Keys`, `WebDriverWait`, `expected_conditions as EC`, `time`).
2. **Constantes compartilhadas**, como XPaths repetidos (ex.: `erro_login_msg`).
3. **Funções auxiliares**, como `login(driver)`, antes dos CTs.
4. **CTs**, um por função, em ordem numérica, cada um com a chamada logo abaixo.

### Estrutura padrão de um CT

```python
#12. Descrição do caso de teste em uma linha
def ct012():
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    try:
        login(driver)                      # só se o CT precisar estar logado
        time.sleep(3)
        driver.find_element(By.ID, "ID_DO_ELEMENTO").click()
        time.sleep(2)
        msg = driver.find_element(By.ID, "ID_DA_MENSAGEM")
        assert "Texto exato esperado" in msg.text
    finally:
        driver.quit()
ct012()
```

Regras dessa estrutura:

- **Um comentário `#N. descrição`** acima de cada `def`, igual aos existentes.
- **Nome `ctNNN`** com 3 dígitos (`ct001`, `ct011`).
- **Cada CT cria o próprio `driver`** (`webdriver.Chrome()`) e **o encerra no `finally` com `driver.quit()`**.
  Nunca reaproveite um `driver` entre CTs. O `quit()` do CT anterior já encerrou a sessão e isso causa
  `ConnectionRefusedError`.
- **A chamada `ctNNN()` fica logo abaixo da função**, sem linha em branco entre elas, como no resto do arquivo.
- **Uma linha em branco** entre um CT e o comentário do próximo.
- Mantenha `wait = WebDriverWait(driver, 10)` no começo de cada CT, mesmo que o CT use só `time.sleep`.
  É o padrão do arquivo e o `wait` fica disponível se for preciso.
- **O `assert` é a última verificação do CT**, sempre sobre `elemento.text`, com `in`
  (`assert "texto" in elemento.text`). Nunca compare o elemento direto com uma string.
- O texto do `assert` deve ser **o texto exato exibido pelo sistema**, com acentos e pontuação.
  Não invente nem "melhore" mensagens. Se não souber o texto, peça ao usuário ou leia na tela.

### Funções auxiliares

- Reutilize `login(driver)` em vez de repetir o bloco de login em CTs novos.
- Uma auxiliar recebe **`driver` como parâmetro**. Ela nunca usa um `driver` global.
- Se um passo se repetir em 3 ou mais CTs, sugira uma função auxiliar ou uma constante, mas só crie se o usuário aprovar.
- XPaths longos usados em mais de um lugar viram constante no topo (como `erro_login_msg`).

---

## 3. Esperas: priorize `time.sleep`

O usuário quer **acompanhar visualmente cada etapa** no navegador. Por isso:

- **Prefira `time.sleep(2)` ou `time.sleep(3)`** entre as etapas (depois de abrir página, clicar, enviar um formulário ou pesquisar).
- Use `time.sleep(1)` apenas entre cliques rápidos em sequência, como abrir menus e submenus.
- **Não use `time.sleep` maior que 3 s** sem motivo. Se a página for lenta, avise o usuário em vez de aumentar o tempo.
- **Não use `driver.implicitly_wait`.** Ele se soma ao `WebDriverWait` e deixa o tempo imprevisível.
- `wait.until(EC...)` continua válido e já existe nos CTs mais antigos (CT001 a CT007). Em **código novo**, dê preferência a `time.sleep`.
  Use `wait.until` só quando houver um bom motivo, por exemplo, quando o elemento pode demorar de forma imprevisível.
- **Não troque os `wait.until` existentes por `sleep` (nem o contrário)** sem o usuário pedir.
- `import time` já está no topo. Não duplique.

Onde colocar a pausa:

```python
driver.find_element(By.ID, "BTNSALVAR").click()
time.sleep(2)                                   # pausa DEPOIS da ação, antes de ler o resultado
msg = driver.find_element(By.ID, "RSCUR_NOME_Balloon")
```

Depois de **toda navegação ou ação que recarrega a tela**, faça uma pausa antes de procurar o próximo elemento.
Sem a pausa, o `find_element` roda antes de a página carregar e dá `NoSuchElementException`.

---

## 4. Localizadores

Ordem de preferência:

1. **`By.ID`**. É o padrão do projeto (`vLOGIN`, `vSENHA`, `BTNSALVAR`, `RSCUR_NOME`, etc.).
2. **`By.CSS_SELECTOR`** quando não há `id` mas existe um atributo estável, como `[data-id="sidebarItem_1"]`.
3. **`By.XPATH`** só quando não houver alternativa. Já é usado no projeto para mensagens e links sem `id`.

Regras:

- **Nunca invente IDs, XPaths ou textos.** Use apenas o que o usuário informou ou o que aparece no código atual.
  Se faltar um localizador, peça para o usuário inspecionar o elemento (F12 → botão direito → Copy → XPath ou ID).
- **`By.ID` só aceita o atributo `id`.** Para `data-id`, `name`, `href` etc., use `By.CSS_SELECTOR`.
- Pegar texto: `elemento.text`. Para valor de `<input>`: `campo.get_attribute("value")`.
- Limpar um campo: `campo.clear()`. **Não** use `Keys.BACKSPACE` (apaga um caractere) nem `Keys.CLEAR`.
- Enviar formulário: `send_keys(Keys.RETURN)` ou `.click()` no botão. Os dois já aparecem no projeto, use o que o CT original usa.
- Se `.click()` for interceptado por outro elemento, use `driver.execute_script("arguments[0].click();", elemento)` e avise o usuário.

---

## 5. Dados de teste e segurança

- Os e-mails e senhas existentes no código (`lucasgomesantunes85@gmail.com`, `lucas123test456@gmail.com` etc.)
  são **contas de teste do usuário**. **Não os copie para a documentação, commits, issues ou mensagens** além do estritamente necessário.
- Em CTs novos que precisem de credenciais, **reutilize `login(driver)`**, em vez de escrever e-mail e senha de novo.
- **Não crie contas novas, não altere dados reais de candidatos e não clique em ações irreversíveis** (excluir, enviar, candidatar-se)
  sem o usuário pedir. O ambiente testado é o `admin.ielcarreiras.com.br`, que é um site real.
- Para cadastros, siga o padrão dos e-mails de teste já usados (`AAAAMMDD@example.com`, domínio `example.com`).
- Se algum dia o código for publicado (GitHub etc.), avise o usuário que as senhas estão em texto puro e sugira mover para
  variáveis de ambiente. Faça isso **só se ele pedir**.

---

## 6. Estilo de código

- **Indentação de 4 espaços** em todo código novo.
  (A função `login` hoje usa 8 espaços no corpo. Isso funciona. Não "conserte" sem pedirem, mas **não copie** essa indentação.)
- **Aspas:** `'...'` para URLs e `"..."` para o resto já estão misturadas no arquivo. Mantenha a que o trecho vizinho usa.
- Nomes de variáveis curtos e em português/inglês simples, como no arquivo: `msg`, `campo`, `titulo`, `aviso`.
- Cada linha de ação em uma linha própria. Não encadeie vários passos em uma linha.
- Mantenha os comentários de separação existentes (`#Começo das CTs...`, `#fim das CTs...`). Novos CTs entram **antes** do comentário de fim.
- Não adicione docstrings, type hints, logging ou `print` de depuração permanentes. `print(elemento.text)` temporário para depurar é aceitável, mas **remova antes de entregar**.

---

## 7. Como rodar e depurar

- Os CTs **rodam ao importar/executar o arquivo**, porque cada `ctNNN()` é chamado logo após a definição.
  Para testar só um CT, comente temporariamente as outras chamadas e **avise o usuário** para restaurá-las.
- Execute com o Python do `venv`: `.\venv\Scripts\python.exe program.py`.
- Um `assert` que falha encerra o script e os CTs seguintes **não rodam**. Isso é esperado no estilo atual. Não mude para "continuar mesmo com falha" sem pedirem.
- Se o script travar ou der `ConnectionRefusedError`, verifique:
  1. Um CT está reutilizando um `driver` já fechado.
  2. Sobraram processos `chromedriver.exe` / `chrome.exe` presos (`taskkill /F /IM chromedriver.exe`).
  3. Windows ARM: o Selenium pode baixar um chromedriver x64. Considere `webdriver.Edge()` se o usuário concordar.
- Se `NoSuchElementException`: falta pausa (`time.sleep`) antes do `find_element`, ou o elemento está dentro de um `iframe`.

---

## 8. Checklist antes de entregar uma alteração

- [ ] O CT novo segue a estrutura padrão da seção 2 (comentário `#N.`, `driver`/`wait`, `try`/`finally`, `quit`, chamada logo abaixo).
- [ ] Usei `time.sleep(2)` ou `time.sleep(3)` entre as etapas.
- [ ] Os localizadores e textos de `assert` vieram do usuário ou do código existente, sem invenção.
- [ ] O `assert` usa `.text` e o texto exato do sistema.
- [ ] Não alterei, renumerei ou reformatei CTs fora do pedido.
- [ ] Não deixei `print` de depuração nem chamadas de CTs comentadas.
- [ ] `import time` continua uma única vez no topo e o arquivo não tem erro de sintaxe.
