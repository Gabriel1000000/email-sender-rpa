import os
import smtplib
import email.message
import configparser
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog


def le_config():
    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8') # Lendo o config file
    return config

def ler_corpo_arquivo():
    try:
        with open('corpo_e-mail.txt', 'r', encoding='utf-8') as arquivo:
            return arquivo.read()
    except FileNotFoundError:
        raise FileNotFoundError("Arquivo de corpo do e-mail não encontrado: corpo_e-mail.txt")

def encontrar_arquivo_pdf():
    documento= filedialog.askopenfilename()
    # filtrando a bunca por arquivos em PDF
    # documento= filedialog.askopenfilename(filetypes=[("Arquivos PDF", "*.pdf")])
    print(f"{documento}")
    return documento

def e_mail():

    config = le_config()
    corpo = ler_corpo_arquivo()
    # Destinatários do e-mail
    destinatarios = eval(config['GERAL']['destinatarios'])
    # Convertendo a string de destinatários de volta para uma lista
    # Encontrar o caminho do arquivo PDF na pasta
    caminho_arquivo_pdf = encontrar_arquivo_pdf()

    # Verificar se encontrou o arquivo PDF
    if caminho_arquivo_pdf:
        # Lendo o conteúdo do arquivo PDF
        with open(caminho_arquivo_pdf, 'rb') as arquivo_pdf:
            conteudo_arquivo = arquivo_pdf.read()
        assunto = config['GERAL']['assunto_normal']
        
                
        # Criando a mensagem
        mensagem = email.message.EmailMessage()
        mensagem['Subject'] = assunto
        mensagem['From'] = 'gmail do remetente'
        mensagem['To'] = ','.join(destinatarios)
        password = 'Senha de app'
        # Adicionado o corpo do e-mail
        mensagem.set_content(corpo)
        # Adicionando o PDF como anexo
        mensagem.add_attachment(conteudo_arquivo, maintype='application', subtype='octet-stream', filename=os.path.basename(caminho_arquivo_pdf))

        # Conectando ao servidor SMTP e enviando o e-mail
        seguranca = smtplib.SMTP('smtp.gmail.com:587')
        seguranca.starttls()
        seguranca.login(mensagem['From'], password)
        seguranca.send_message(mensagem)
        seguranca.quit()

        # Caixa de diálogo após o envio do e-mail
        messagebox.showinfo('Status do envio do e-mail!', 'E-mail foi enviado com sucesso!') 
    else:
        # Caixa de diálogo para caso nenhum arquivo PDF seja encontrado
        messagebox.showerror('Status do envio do e-mail!', 'Nenhum arquivo PDF encontrado na pasta.')

e_mail()
