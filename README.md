# Gerador de Propostas e Boletos (Staging)

Este projeto realiza a automação completa do fluxo de contratação no ambiente de staging. 
O script preenche todos os dados cadastrais necessários, finaliza a proposta e realiza o download do boleto bancário criptografado para conferência local.

Ele foi desenvolvido para agilizar a criação de massas de dados e testes de fluxo que seriam demorados de realizar manualmente.

## 🚀 Funcionalidades

- Acessa o ambiente de staging automaticamente
- Realiza o fluxo de compra/contratação completo
- Preenche dados de identificação (CPF, Nome, Telefone)
- Preenche dados de endereço automaticamente via CEP
- Seleciona opções de formulário (Gênero, Estado, Origem)
- Finaliza a contratação via modalidade **Boleto**
- Captura o link do boleto em nova aba (popup)
- Baixa o PDF e salva em pasta local com nome padronizado
- Exibe a senha de abertura do PDF no terminal

## 🧰 Tecnologias utilizadas

- Python 3.13
- Playwright (Automação Web)
- OS e Time (Manipulação de arquivos e pausas)
- Requests (via context do Playwright para download)

## 📂 Estrutura esperada de arquivos

/seu-projeto
 ├─ gerador_proposta.py
 └─ C:/automacoes/propostas_boletos/ (Gerada automaticamente)

## 📥 Configuração de Entrada

As variáveis principais estão no topo do arquivo para fácil edição:
- `URL`: Link do ambiente de staging
- `CPF`: Documento utilizado no teste
- `EMAIL`: E-mail para recebimento da confirmação
- `download_path`: Caminho onde os boletos serão armazenados

## 📤 Saída do sistema

O script gera um arquivo PDF na pasta de destino com o seguinte formato:
`boleto_12345678901_202401091030_CRIPTO.pdf`

No console, você verá o log de cada etapa:
`SUCESSO! Arquivo PDF salvo em: C:\automacoes\propostas_boletos\boleto_...`
`Use a senha '12345' para abrir o arquivo.`

## 🔧 Instalação e uso

1) **Clonar o repositório**
git clone https://github.com/seu-usuario/seu-repositorio.git

2) **Entrar na pasta**
cd seu-repositorio

3) **Instalar o Playwright**
pip install playwright

4) **Instalar o navegador (Chromium)**
playwright install chromium

5) **Executar o script**
python gerador_proposta.py

## 🧠 Lógica principal utilizada

O script:
1. Inicia o navegador com `headless=False` para acompanhamento visual
2. Localiza e clica nos botões de fluxo (Comprar/Continuar)
3. Preenche os seletores de ID e classe (`#id_cpf_cnpj`, `#id_name`, etc)
4. Utiliza uma função auxiliar `fill()` para tratar erros de preenchimento
5. Monitora a abertura de novas abas com `expect_popup()` para capturar o boleto
6. Realiza o download do PDF através do contexto de requisição do navegador para garantir a sessão

## ⚠️ Observações importantes

- O script possui `slow_mo=300` para garantir que os elementos carreguem antes da interação
- É necessário que a pasta de destino tenha permissão de escrita
- O ambiente deve ser Staging; o script utiliza seletores específicos desse fluxo
- Certifique-se de que o CPF utilizado é válido para o ambiente de teste

## ✔️ Exemplo de execução

Iniciando navegador...
Acessando URL...
Página carregada!
Preenchendo CPF: 12345678901...
Nome preenchido: Usuario Teste
...
--- Processando Boleto ---
Link do PDF obtido: https://pdf-provider.suaempresa.com.br/...
SUCESSO! Arquivo PDF salvo em: C:\automacoes\propostas_boletos\boleto_12345678901_CRIPTO.pdf
Use a senha '12345' para abrir o arquivo.

## 🧾 Licença

Projeto para uso interno e automação de testes.
