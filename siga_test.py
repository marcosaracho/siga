import time
import unittest

import self as self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def start_chrome():
    driver_path = 'driver/chromedriver'  # ou o caminho para o driver do navegador que você está usando

    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  # Opcional: maximizar a janela do navegador

    # Inicializar o navegador Chrome
    driver = webdriver.Chrome(options=options)

    # URL do site
    url = 'https://siga.marcacaodeatendimento.pt/Marcacao/MarcacaoInicio'

    # Abrir a URL no navegador
    driver.get(url)
    return driver


def close_chrome():
    driver.quit()


def iniciar_agendamento():
    iniciar_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-entidade-assunto'))
    )

    # Clicar no botão "Iniciar"
    iniciar_button.click()

    print("Botão 'Iniciar' clicado com sucesso!")


def insere_texto_pesquisa():
    # Aguardar até que o campo de pesquisa seja visível na página
    pesquisa_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'tbPesquisa'))
    )

    # Inserir o texto "renovação de residencia" no campo de pesquisa
    pesquisa_input.send_keys("Residence permit")

    print("Texto inserido com sucesso no campo de pesquisa!")


def seleciona_pesquisar():
    # Localizar o botão de pesquisa pelo ID
    pesquisar_assunto_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, 'btnPesquisarAssunto'))
    )

    # Clicar no botão de pesquisa
    pesquisar_assunto_button.click()

    print("Botão de pesquisa clicado com sucesso!")


def seleciona_resultado_pesquisa():
    # elemento do botao de resultado da pesquisa
    selecionar_button = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-pesquisa-results'))
    )

    # Clicar no botão de seleção
    selecionar_button.click()

    print("Botão selecionar clicado com sucesso!")


def avanca_pagina_intermediaria():
    # Aguardar até que o botão 'proximoButton' seja visível
    next_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]"))
    )

    # Clicar no botão 'proximoButton'
    next_button.click()

    print("Botão 'Next' clicado com sucesso!")


def seleciona_distrito(p_distrito):
    # Aguardar até que o elemento 'IdDistrito' seja visível
    id_distrito_select = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdDistrito'))
    )

    select = Select(id_distrito_select)
    select.select_by_visible_text(p_distrito)

    print('Opção ' + p_distrito + ' selecionada com sucesso!'
          )


def seleciona_localidade(p_localidade):
    id_localidade = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdLocalidade'))
    )

    select = Select(id_localidade)
    time.sleep(1)
    select.select_by_visible_text(p_localidade)
    print('Opção ' + p_localidade + ' selecionada com sucesso!'
          )


def seleciona_local_atendimento(p_local_atendimento):
    # Aguardar até que o elemento 'IdLocalAtendimento' seja visível
    id_local_atendimento_select = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.ID, 'IdLocalAtendimento'))
    )

    select_local_atendimento = Select(id_local_atendimento_select)
    time.sleep(1)
    select_local_atendimento.select_by_visible_text(p_local_atendimento)

    print('Opção ' + p_local_atendimento + ' selecionada com sucesso!')


def avanca_para_ultima_pagina():
    last_button = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.XPATH, "//*[contains(text(), 'Next')]"))
    )

    # Clicar no botão 'proximoButton'
    last_button.click()
    print("Botão 'Next' clicado com sucesso!")


def valida_message_error(local):
    # Aguardar até que o elemento seja visível
    error_message_div = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'error-message'))
    )

    h5_element = error_message_div.find_element(By.TAG_NAME, 'h5')

    # Imprimir a mensagem com base na presença do elemento
    if h5_element.text == "There are no appointment shedules available for the selected criteria.":
        print("Não há horários em " + local)
    else:
        print("Existe horário em " + local)


# Cenários de teste
def verifica_lisboa(p_distrito, p_localidade):
    try:
        print('------ ' + p_distrito + ' / ' + p_localidade + ' ------')
        start_chrome()
        iniciar_agendamento()
        insere_texto_pesquisa()
        seleciona_pesquisar()
        seleciona_resultado_pesquisa()
        avanca_pagina_intermediaria()
        seleciona_distrito(p_distrito)
        seleciona_localidade(p_localidade)
        avanca_para_ultima_pagina()
        valida_message_error(p_localidade)
        print('')
    finally:
        close_chrome()


# Start Lisboa / TODAS AS LOCALIDADES
driver = start_chrome()
verifica_lisboa('LISBOA', 'ALL PLACES')


# # Start Lisboa / Marvila
# driver = start_chrome()
# verifica_lisboa('LISBOA', 'Loja de Cidadão Marvila', 'Marvila')
#
# # Start Coimbra / Loja Cidadão
# driver = start_chrome()
# verifica_lisboa('COIMBRA', 'Loja de Cidadão Coimbra', 'Coimbra')
