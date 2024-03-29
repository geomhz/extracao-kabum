import os
import logging
import pandas as pd
from time import sleep
from openpyxl import Workbook
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as condicao_esperada

class InformacoesAplicativo:
    def exibir_cabecalho(self, nome_desenvolvedor="Geovanne Murata", contato_whatsapp="+55 11 95284-2140"):
        """Exibe informações do desenvolvedor e contato no console."""
        print('==================================')
        print('*****    Desenvolvido por:   *****')
        print(f'*****    {nome_desenvolvedor}     *****')
        print('==================================')
        print(f'=====> Whatsapp: {contato_whatsapp}\n')

class KabumScrapy(InformacoesAplicativo):
    def __init__(self, produto='i5', headless=True,  navegador_anonimo=False, deletar_xlsx=True) -> None:
        """
        Inicializador da classe e definição de parametros

        produto=None (input para declarar o produto ao iniciar o script)
        produto="i7" (exemplo de declaração do produto á ser pesquisado. Não abre input e inicia direto)

        headless=False (abre o navegador e a automação fica aparente)
        headless=True (inicia com o navegador oculto)
        
        navegador_anonimo=False (inicia o navegador em modo normal)
        navegador_anonimo=True (inicia o navegador em modo anônimo)

        deletar_xlsx=False (mantém tanto o arquivo ".xlsx" quanto o arquivo ".csv")
        deletar_xlsx=True (deleta o arquivo ".xlsx" e mantém apenas o ".csv")
        """
        
        self.exibir_cabecalho()

        self.produto = produto
        self.navegador_anonimo = navegador_anonimo
        self.headless = headless
        self.deletar_xlsx = deletar_xlsx

        if produto is None:
            produto = input('\nDigite o nome do produto a pesquisar: ').strip()
        self.produto = produto

        print('Coleta de dados iniciado!\n')

        """Criação de logs que ficarão salvos no arquivo 'logs.log' na raiz do projeto"""
        logging.basicConfig(format='%(levelname)s [%(asctime)s]: %(message)s (Linha: %(lineno)d) [%(filename)s])',
                            datefmt='%d/%m/%Y %I:%M:%S %p',
                            level=logging.INFO,
                            filename='logs.log',
                            filemode='w')

        logging.warning('ATENCAO: NAO MEXA NO ARQUIVO EXCEL ENQUANTO O BOT ESTA RODANDO.')
        
        self.website_inicial = 'https://www.kabum.com.br/'

    def xpath_geral(self):
        """XPATH geral da aplicação para interação do site e extração dos dados"""

        self.xpath_pesquisar = {
            'input_busca': '(//*[@id="input-busca"])',
            'botao_submit': '(//*[@aria-label="Buscar"])'
        }

        self.xpath_extracao = {
            'extracao_nome': '(//*[@class="sc-cdc9b13f-11 bZLJcB"]//h2)',
            'extracao_valor': '(//*[@class="sc-620f2d27-2 bMHwXA priceCard"])',
            'extracao_link': '//*[@class="sc-cdc9b13f-10 jaPdUR productLink"]',
            'proxima_pagina': '(//*[@class="next"])'
        }

    def iniciaizador_bot(self):
        """Executar funções gerais"""

        self.xpath_geral()
        self.iniciar_navegador()
        self.extracao_kabum()
        self.converter_xlsx_csv()
        print('\nRaspagem de dados finalizada!\n')
        logging.info('BOT FINALIZADO COM SUCESSO. AGORA VOCE PODE ABRIR O EXCEL NA PASTA RAIZ!')

    def iniciar_navegador(self):
        """Carregar os argumentos do navegador e iniciar"""

        options = Options()
        options.add_argument("--start-maximized")
        options.add_argument("--log-level=3")
        options.add_argument("--ignore-certificate-errors")

        if self.navegador_anonimo:
            options.add_argument("--incognito")

        if self.headless:
            options.add_argument("--headless")

        try:
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, 1)
            self.wait1 = WebDriverWait(self.driver, 5)
            self.driver.get(self.website_inicial)
            logging.info('NAVEGADOR INICIADO COM SUCESSO')
        except Exception as e:
            logging.critical('ERRO AO ABRIR O NAVEGADOR')

    def pesquisar_produto(self, produto):
        """Localizar campos de pesquisa"""

        try:
            input_pesquisa = self.wait1.until(
                condicao_esperada.presence_of_element_located((By.XPATH, self.xpath_pesquisar['input_busca']))).send_keys(produto)
            enviar_pesquisa = self.wait1.until(
                condicao_esperada.presence_of_element_located((By.XPATH, self.xpath_pesquisar['botao_submit']))).click()
        except TimeoutException:
            logging.warning('TEMPO DE ESPERA EXCEDIDO! VERIFIQUE SUA CONEXAO')
        except NoSuchElementException:
            logging.critical('ELEMENTO NAO ENCONTRADO')

    def extracao_kabum(self):
        """Função extracao_kabum() para extrair nome, valor e link de cada produto"""

        self.pesquisar_produto(self.produto)
        self.criar_excel()

        """Loop Infinito enquanto encontra itens no site"""
        contagem_pagina = 1
        while True:
            try:
                carregamento_pagina = self.wait1.until(
                    condicao_esperada.presence_of_element_located((By.XPATH, self.xpath_extracao['extracao_nome'])))
                sleep(1.5)
                
                extrair_nomes = self.driver.find_elements(By.XPATH, self.xpath_extracao['extracao_nome'])
                extrair_valor = self.driver.find_elements(By.XPATH, self.xpath_extracao['extracao_valor'])
                extrair_link = self.driver.find_elements(By.XPATH, self.xpath_extracao['extracao_link'])
                """Loop para passar por cada item encontrado"""
                for i in range(len(extrair_valor)):
                    if carregamento_pagina:
                        nome = extrair_nomes[i].text
                        valor = extrair_valor[i].text
                        atributo_link = extrair_link[i]
                        link = atributo_link.get_attribute('href')

                    self.ws.append([nome, valor, link])

                try:
                    self.nome_excel = f'Produto - {self.produto}.xlsx'
                    self.wb.save(self.nome_excel)
                    logging.info(f'DADOS DA PAGINA {contagem_pagina} EXTRAIDO COM SUCESSO')
                except:
                    logging.critical(f'POR FAVOR NAO ABRA O EXCEL DURANTE A EXECUCAO DO BOT. INFORMACOES DA PAGINA {contagem_pagina} NAO EXTRAIDO.')

                try:
                    prox_pagina = self.wait.until(
                        condicao_esperada.presence_of_element_located((By.XPATH, self.xpath_extracao['proxima_pagina']))).click()
                    contagem_pagina += 1
                except NoSuchElementException:
                    logging.critical('ELEMENTO NAO ENCONTRADO')
                    break
            except:
                break

    def criar_excel(self):
        """Criação do arquivo .xlsx"""
        self.wb = Workbook()
        self.ws = self.wb.active
        self.ws.title = "Extração Kabum"

        headers = ["NOME PRODUTO", "VALOR PRODUTO", "LINK PRODUTO"]
        self.ws.append(headers)

    def converter_xlsx_csv(self):
        """Conversão de .xlsx para .csv"""

        excel_xlsx = self.nome_excel
        excel_csv = excel_xlsx.replace(".xlsx", ".csv")

        df = pd.read_excel(excel_xlsx)
        df.to_csv(excel_csv, index=False, encoding='latin-1', sep=';')
        logging.info('NOVO .CSV CRIADO COM SUCESSO')

        if self.deletar_xlsx:
            if os.path.exists(excel_xlsx):
                os.remove(excel_xlsx)
                logging.info('ARQUIVO .XSLX DELETADO COM SUCESSO')
            else:
                logging.warning('ARQUIVO .XLSX NÃO DELETADO')

if __name__ == '__main__':
    iniciar = KabumScrapy()
    iniciar.iniciaizador_bot()