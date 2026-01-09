from playwright.sync_api import sync_playwright
import os
import time

URL = "https://staging-exemplo.suaempresa.com.br/fluxo-teste"
CPF = "12345678901"
EMAIL = "teste.automacao@exemplo.com"
BOLETO_SENHA = "12345"

# Pasta local genérica para salvar os boletos
download_path = r"C:\automacoes\propostas_boletos"
os.makedirs(download_path, exist_ok=True)

with sync_playwright() as p:
    print("Iniciando navegador...")
    browser = p.chromium.launch(headless=False, slow_mo=300)
    context = browser.new_context(accept_downloads=True)
    page = context.new_page()

    print("Acessando URL...")
    page.goto(URL)
    page.wait_for_selector("body")
    time.sleep(3)
    print("Página carregada!")

    # --- Comprar ---
    print("Clicando em 'Comprar'...")
    page.locator("button").nth(5).click(force=True)
    time.sleep(2)
    print("Botão 'Comprar' clicado!")

    # --- Continuar ---
    print("Clicando em 'Continuar'...")
    page.locator("#id_go_step1").click(force=True)
    time.sleep(1)
    print("Botão 'Continuar' clicado!")

    # --- CPF ---
    print(f"Preenchendo CPF: {CPF}...")
    page.locator("#id_cpf_cnpj").fill(CPF)
    time.sleep(0.5)

    # --- Botão seta ---
    print("Clicando no botão seta...")
    page.locator("button:has(i.eva-arrow-forward-outline)").click(force=True)
    time.sleep(1)
    print("Botão seta clicado!")

    # --- Função auxiliar para preencher campos ---
    def fill(selector, value, name=""):
        try:
            page.locator(selector).fill(value)
            print(f"{name} preenchido: {value}")
        except:
            print(f"Erro preenchendo {name}")
        time.sleep(0.3)

    fill("input#id_name", "Usuario Teste", "Nome")
    fill("input#id_telefone", "11999999999", "Telefone")
    fill("input#id_birth_date", "01012000", "Data Nascimento")
    fill("input#id_income", "5000", "Renda")
    fill("input#id_mother_name", "Mae Teste", "Nome da mãe")
    fill("input#id_cep", "00000000", "CEP")
    time.sleep(3)
    fill("input#id_address_number", "100", "Número")
    fill("input#id_address_complement", "Apto 01", "Complemento")

    print("Selecionando gênero: Masculino...")
    page.locator("select#id_gender").select_option("M")
    time.sleep(0.5)

    print("Selecionando estado: Estado genérico...")
    page.locator("select#id_address_state").select_option("MG")
    time.sleep(0.5)

    print("Onde nos conheceu: Whatsapp...")
    page.locator("select").nth(-1).select_option(label="Whatsapp")
    time.sleep(0.5)

    print("Preenchendo e-mail e confirmação...")
    page.locator("input#id_email").nth(0).fill(EMAIL)
    page.locator("input#id_email").nth(1).fill(EMAIL)
    time.sleep(0.5)

    print("Clicando em 'Avançar'...")
    page.evaluate("document.querySelector('#id_go_step2').click()")
    time.sleep(1)

    print("Marcando checkbox de concordância...")
    page.locator("text='Declaro que li e estou de acordo com os termos do contrato.'").click(force=True)
    time.sleep(0.5)

    print("Clicando em 'Contratar agora'...")
    page.locator("button:has-text('Contratar agora')").click(force=True)
    time.sleep(1)

    print("Marcando opção 'Boleto'...")
    page.locator("div.q-radio__label", has_text="Boleto").click(force=True)
    time.sleep(0.5)

    print("\n--- Processando Boleto ---")
    pdf_url = ""

    try:
        with page.expect_popup() as popup_info:
            print("Clicando em 'Baixar boleto' para obter o link do PDF.")
            page.locator("button:has-text('Baixar boleto')").click(force=True)

        boleto_page = popup_info.value
        boleto_page.wait_for_load_state("load", timeout=10000)

        pdf_url = boleto_page.url
        print(f"Link do PDF obtido: {pdf_url[:70]}...")

        boleto_page.close()
        print("Aba do boleto fechada.")

        print("\n--- Baixando Arquivo via Request Client ---")

        response = context.request.get(pdf_url)

        if response.ok and 'application/pdf' in response.headers.get('content-type', ''):
            pdf_content = response.body()

            save_path = os.path.join(
                download_path,
                f"boleto_{CPF}_{time.strftime('%Y%m%d%H%M%S')}_CRIPTO.pdf"
            )

            with open(save_path, "wb") as f:
                f.write(pdf_content)

            print(f"SUCESSO! Arquivo PDF salvo em: {save_path}")
            print(f"Use a senha '{BOLETO_SENHA}' para abrir o arquivo.")
        else:
            print(f"Falha na requisição. Status: {response.status}")
            print("O servidor não retornou um arquivo
