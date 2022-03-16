import streamlit as st
import sqlite3
import datetime as dt
import streamlit_authenticator as stauth
import ssl
import pandas as pd
import numpy as np
import openpyxl

st.set_page_config(page_title='OT - FERRAMENTA ATIVOS', page_icon='📋', layout="wide", initial_sidebar_state="auto", menu_items=None)


def busca_svc(usernames):
    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT id_typelogin FROM login WHERE usuario = '{usernames}'")
    buscando_svc = cursor.fetchall()
    cursor.close()

    return buscando_svc


def buscando_dados(nome_setor):

    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT s.motorista, s.perfil, s.experiencia, s.status FROM drivers s inner join setor st on s.id_setor = st.id_setor where st.nome_setor = '{nome_setor}'")
    resultado = cursor.fetchall()
    cursor.close()

    return resultado


def buscando_dados_inativos(nome_setor):

    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT s.motorista, s.perfil, s.experiencia, s.status FROM drivers s inner join setor st on s.id_setor = st.id_setor where st.nome_setor = '{nome_setor}' and s.status = 'INATIVO'")
    resultado2 = cursor.fetchall()
    cursor.close()

    return resultado2


def tela_ativos():

    st.sidebar.title("PAINEL DE CONTROLE")
    st.sidebar.write("")
    painel = st.sidebar.slider("QUANTIDADE DE DRIVERS:", min_value=1, max_value=50)
    st.sidebar.write("")
    return painel


def inserir_dados(motorista, perfil, experiencia, status, setor):

    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT * FROM drivers WHERE motorista='{motorista.upper()}'")
    consulta = cursor.fetchone()
    cursor.close()
    if consulta:
        cursor2 = con.cursor()
        cursor2.execute(f"update drivers set perfil = '{perfil}', experiencia = '{experiencia}', status = '{status}' WHERE motorista = '{motorista}'")
        con.commit()
        cursor2.close()
        return 0
    else:
        cursor2 = con.cursor()
        cursor2.execute(f"SELECT id_setor FROM setor WHERE nome_setor = '{setor}'")
        id_setor = cursor2.fetchone()[0]
        cursor = con.cursor()
        cursor.execute(f"INSERT INTO drivers VALUES (null, '{motorista.upper()}', '{perfil.upper()}', '{experiencia.upper()}', '{status.upper()}', {id_setor})")
        con.commit()
        cursor.close()
        return 1


def quantidade(i):

    dicionario = {x: {'motorista': '', 'perfil': '', 'experiencia': '', 'status': ''} for x in range(1, i+1)}
    col1, col2, col3, col4 = st.columns(4)
    for a in range(1, i+1):
        with col1:
            motorista = st.text_input("MOTORISTA", key=a)
            dicionario.update({a: {'motorista': motorista}})

        with col2:
            perfil = st.selectbox("PERFIL", ("UTILITÁRIO", "PASSEIO", "VAN", "VUC", "TRICICLO ELÉTRICO", "RENTAL", "MOTO"), key=a)
            dicionario[a].update({'perfil': perfil})

        with col3:
            experiencia = st.selectbox("EXPERIÊNCIA", ("NOVATO", "EXPERIENTE"), key=a)
            dicionario[a].update({'experiencia': experiencia})

        with col4:
            status = st.selectbox("STATUS", ("TREINAMENTO", "ATIVO", "INATIVO", "EXPORÁDICO", "INDISPONÍVEL"), key=a)
            dicionario[a].update({'status': status})

    return dicionario


def disparo():

    de = 'pedrolins42@gmail.com'
    para = 'para qual email quer enviar'
    password = 'senha do seu e-mail'

    ssl.create_default_context()
    with smtplib.SMTP('smtp.gmail.com', 587) as conexao:
        conexao.ehlo()
        conexao.starttls()
        conexao.login(de, password)
        conexao.sendmail(de, para, 'Subject: assunto\n\nmensagem')


def atualiza_horario(nome_setor):
    hora = dt.datetime.now().strftime('%H: %M: %S')
    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"UPDATE setor set horario = '{hora}', nome_setor = '{nome_setor}'")
    resultado3 = cursor.fetchall()
    con.commit()
    cursor.close()

    return resultado3


def consultar_horario(nome_setor):
    
    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT horario FROM setor WHERE nome_setor = '{nome_setor}'")
    resultado4 = cursor.fetchone()
    cursor.close()

    return resultado4


hora = dt.datetime.now().strftime('%H: %M: %S')
hora2 = dt.time(15, 59, 00).strftime('%H: %M: %S')


def busca_permissoes(usuario):

    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT tl.total, tl.leitura, tl.privado, st.nome_setor FROM login lg inner join typelogin tl on lg.id_typelogin = tl.id_typelogin inner join setor st on st.id_setor = lg.id_setor WHERE lg.names = '{usuario.upper()}'")
    var1 = cursor.fetchone()
    return var1


def busca_login():
    names, usernames, passwords, id_typelogin = [], [], [], []
    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute(f"SELECT lg.names, lg.usuario, lg.senha, lg.id_typelogin FROM login lg")
    listaBanco = cursor.fetchall()
    for x in listaBanco:
        names.append(x[0])
        usernames.append(x[1])
        passwords.append(x[2])
        id_typelogin.append(x[3])
    cursor.close()

    return names, usernames, passwords, id_typelogin


def puxar_excel():
    con = sqlite3.connect("test.sqlite3")
    cursor = con.cursor()
    cursor.execute("SELECT st.nome_setor, dv.motorista, dv.perfil, dv.experiencia, dv.status FROM drivers dv inner join setor st on dv.id_setor = st.id_setor")
    excel1 = cursor.fetchall()
    return excel1


names, usernames, passwords, id_typelogin = busca_login()
hashed_passwords = stauth.hasher(passwords).generate()
authenticator = stauth.authenticate(names, usernames, hashed_passwords,
'some_cookie_name', 'some_signature_key', cookie_expiry_days=30)
name, authentication_status = authenticator.login('LOGIN - FERRAMENTA DE ATIVOS ', 'main')
if authentication_status:
    var2 = busca_permissoes(name)
    print(var2)
    unidades = ('SÃO BERNARDO DO CAMPO', 'ARENA BARUERI', 'BARRETOS',
        'CAMPINAS', 'CENTRO', 'GUARULHOS', 'IPATINGA', 'ITAPETININGA',
        'JUNDIAÍ', 'LIMEIRA', 'MOGI DAS CRUZES', 'ZONA OESTE',
        'POUSO ALEGRE', 'RIBEIRÃO PRETO', 'RIO DE JANEIRO', 'SANTOS',
        'SÃO CARLOS', 'SÃO JOSÉ DOS CAMPOS', 'SOROCABA', 'ZONA LESTE', 'ZONA SUL')
    if var2[3] and var2[0]:
        unidade = unidades
        ativar_botao = True
        ativar_salvar = True
    elif var2[3] and var2[1]:
        unidade = unidades
        ativar_botao = False
    elif var2[3] and var2[2]:
        unidade = []
        unidade.append(var2[3])
        ativar_botao = True
    window = tela_ativos()
    nome_setor = st.sidebar.selectbox("UNIDADE", unidade)
    check1 = st.sidebar.checkbox(f"MOTORISTAS DA OPERAÇÃO - MELI {nome_setor}")
    download1 = st.sidebar.download_button(label="⬇️", data="csv", file_name="ativos.csv", mime='text/csv', help='DOWNLOAD DOS ATIVOS EM EXCEL')
    row = puxar_excel()
    dados = pd.DataFrame(data=row)
    if ativar_botao:
        if download1:
            dados.to_excel('test.xlsx')
            st.sidebar.success(download1)
    check2 = st.sidebar.checkbox("MOTORISTAS INATIVOS")
    download2 = st.sidebar.download_button(label="⬇️", data="csv", file_name="ativos.csv", mime='text/csv', help='DOWNLOAD DOS INATIVOS EM EXCEL')
    if not check1:
        quant = quantidade(window)
        if ativar_botao:
            salvar = st.button("SALVAR")
            if salvar:
                if (hora < hora2):
                    update_hr = atualiza_horario(nome_setor)
                    for x, y in quant.items():
                        if y["motorista"]:
                            insert = inserir_dados(y["motorista"], y["perfil"], y["experiencia"], y["status"], nome_setor)
                            if insert == 1:
                                st.success(f"DADOS DO **{y['motorista']}**")
                            elif insert == 0:
                                st.success(f"DADOS DO **{y['motorista']}** ATUALIZADOS COM SUCESSO")
                            else:
                                st.error(f"MOTORISTA **{y['motorista']}** JÁ ESTÁ CADASTRADO")
                else:
                    st.error("O HORÁRIO PARA ATUALIZAÇÃO ESTÁ ESGOTADO. POR FAVOR,  ATUALIZAR AMANHÃ ATÉ ÀS **13h30!**")

        else:
            st.warning("VOCÊ NÃO TEM AUTORIZAÇÃO PARA SALVAR")

    else:
        busca = buscando_dados(nome_setor)
        col1, col2, col3, col4 = st.columns(4)
        chave = 0
        for dados in busca:
            with col1:
                st.text_input("MOTORISTA", value=dados[0], disabled=True, key=dados[0]+str(chave))
            with col2:
                st.text_input("PERFIL", value=dados[1], disabled=True, key=dados[1]+str(chave))
            with col3:
                st.text_input("EXPERIÊNCIA", value=dados[2], disabled=True, key=dados[2]+str(chave))
            with col4:
                st.text_input("STATUS", value=dados[3], disabled=True, key=dados[3]+str(chave))

            chave = chave + 1

    if not check2:
        pass

    else:
        busca2 = buscando_dados_inativos(nome_setor)
        col1, col2, col3, col4 = st.columns(4)
        chave1 = 0
        for dados1 in busca2:
            with col1:
                st.text_input("MOTORISTA", value=dados1[0], disabled=True, key=dados1[0]+str(chave1))
            with col2:
                st.text_input("PERFIL", value=dados1[1], disabled=True, key=dados1[1]+str(chave1))
            with col3:
                st.text_input("EXPERIÊNCIA", value=dados1[2], disabled=True, key=dados1[2]+str(chave1))
            with col4:
                st.text_input("STATUS", value=dados1[3], disabled=True, key=dados1[3]+str(chave1))

            chave1 = chave1 + 1


    st.sidebar.write("")
    st.sidebar.write("ÚLTIMA ATUALIZAÇÃO:")
    busca_update = consultar_horario(nome_setor)

    if busca_update and busca_update[0] is not None:
        st.sidebar.success(f"HORÁRIO: {busca_update[0]} ")
    else:
        st.sidebar.error("PRECISA SER ATUALIZADO")


row = puxar_excel()

dados = pd.DataFrame(data=row)

dados.to_excel('test.xlsx')




