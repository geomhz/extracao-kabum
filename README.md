# Raspagem de dados Kabum

## Sobre o projeto

Este script é uma automação de coleta de dados do website Kabum onde extraimos: Nome, Valor e Link do produto. Em poucos segundos é possível fazer uma extensa coleta de dados.

### Funcionalidades

- **DADOS COLETADOS:** Todos os dados coletados serão adicionados ao arquivo "Produto - SEUPRODUTO" com a extensão ".xlsx" e ".csv".
- **SEGUNDO PLANO:** Para rodar a aplicação em segundo plano altere o parâmetro "headless=False" para "headless=True" na linha 14.
- **DELETE .XLSX OU NÃO:** Para deletar o arquivo ".xlsx" após a criação do ".csv" altere o parâmetro "deletar_xlsx=False" para "deletar_xlsx=True"
- **PRODUTO Á SER PESQUISADO:** Na linha 14 escolha "produto=None" para declarar no terminal o produto que quer pesquisar ao iniciar a aplicação ou declare para "produto='SEUPRODUTO'" para iniciar direto!
- **LOGS:** Ao iniciar a aplicação um arquivo de log será criado na pasta raiz do projeto onde é possível verificar e validar os processos de sucesso, avisos e erros detalhados da aplicação.

## Do inicio!

Siga o passo á passo para rodar a aplicação! 

### Pré-Requisitos

É necessário ter instalado corretamente em seu computador:

- Python 3.8+

### Instalação

Siga o passo a passo para instalar a aplicação:

1. Clone o repositório abrindo o Git Bash:
```bash
git clone https://github.com/geomhz/extracao-kabum.git
```

2. Crie um Ambiente Virtual (venv) e ative:
```bash
Windows: python -m venv venv
         venv/scripts/activate

Linux/Mac: python3 -m venv venv
           source venv/bin/activate
```

3. Instale as dependências necessárias após ativar a venv:
```bash
pip install -r requirements.txt
```
4. Ajuste os parâmetros á seu favor no INIT:
```bash
headless=False ou True # False = Navegador visível, True = Navegador oculto
deletar_xlsx=False ou True # False = Deletar .xlsx, True = Manter .xlsx
```

5. Defina o seu produto á ser pesquisado na linha 14:
```bash
produto="SEUPRODUTO" # Troque "SEUPRODUTO" para produto que deseja pesquisar 
ou
produto=None # Insira o nome do produto á pesquisar no terminal ao iniciar a aplicação
```

### Dependências

Lista de dependências do projeto:
```bash
attrs==23.2.0
certifi==2024.2.2
cffi==1.16.0
et-xmlfile==1.1.0
h11==0.14.0
idna==3.6
numpy==1.26.4
openpyxl==3.1.2
outcome==1.3.0.post0
pandas==2.2.1
pycparser==2.21
PySocks==1.7.1
python-dateutil==2.8.2
pytz==2024.1
selenium==4.18.1
six==1.16.0
sniffio==1.3.0
sortedcontainers==2.4.0
trio==0.24.0
trio-websocket==0.11.1
typing_extensions==4.9.0
tzdata==2024.1
urllib3==2.2.1
wsproto==1.2.0
```

## Uso

Após configurado da sua maneira inicie a automação e veja a mágica acontecer!
OBS: Não esqueça de colocar produtos válidos que tem no site 🤘🏼

## Contato
Meu nome é Geovanne Murata!

Website - [Visite meu website!](https://geomurata.com/)

Linked In - [Visite meu LinkedIn!](https://www.linkedin.com/in/geovanne-murata/)

WhatsApp - [Me chame no Whats](https://api.whatsapp.com/send/?phone=5511952842140)

Project Link: [car-store-django](https://github.com/geomhz/car-store-django/)