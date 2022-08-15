import requests
from requests import TooManyRedirects, Timeout, ConnectionError
import banco
import json
from time import sleep
from collections import Counter
from operator import itemgetter


chave_api = 'RGAPI-29788844-acb1-4e33-999b-d9d38bdfd215'

def resetar_Lista_Invocadores():
    sql = f"DELETE FROM tb_invocador"
    banco.manipular_dados(sql)
    atualizar_Lista_Invocadores()

def atualizar_Lista_Invocadores():
    try:
        retorno = requests.get(f'https://br1.api.riotgames.com/lol/league/v4/challengerleagues/by-queue/RANKED_SOLO_5x5?api_key={chave_api}')
        invocador_lista = retorno.json()['entries']

        for invocador in invocador_lista:
            id_invocador = invocador.get('summonerId')
            nome_invocador = invocador.get('summonerName')
            sql = f"INSERT INTO tb_invocador (T_NOME_INVOCADOR, T_ID_INVOCADOR) VALUES ('{nome_invocador}', '{id_invocador}')"
            banco.manipular_dados(sql)

        adicionar_id_contas()
    except ConnectionError as ex:
        print(ex)

def adicionar_id_contas():
    try:
        sql = f"SELECT * FROM tb_invocador"
        invocadores = banco.selecionar(sql)

        contadorRequests = 0
        for dado_invocador in invocadores:
            id_invocador = dado_invocador[1]
            print(id_invocador)
            retorno = requests.get(
                f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/{id_invocador}?api_key={chave_api}')
            id_conta = retorno.json().get('accountId')
            sql = f"UPDATE tb_invocador SET T_ID_CONTA = '{id_conta}' WHERE T_ID_INVOCADOR = '{id_invocador}'"
            banco.manipular_dados(sql)
            contadorRequests += 1
            if contadorRequests == 90:
                print('MUITAS REQUISIÇÕES! AGUARDE 2 MINUTOS E RETOMAREMOS O TRABALHO!')
                sleep(121)
                contadorRequests = 0
    except ConnectionError as ex:
        print(ex)

def historico_de_partidas():
    try:
        sql = f"SELECT * FROM tb_invocador"
        todos_invocadores = banco.selecionar(sql)
        contadorRequests = 0
        for invocador in todos_invocadores:
            id_conta = invocador[2]
            retorno = requests.get(
                f'https://br1.api.riotgames.com/lol/match/v4/matchlists/by-account/{id_conta}?endIndex=10&api_key= {chave_api}')
            contadorRequests += 1
            historico_invocador = retorno.json()['matches']
            for partida in historico_invocador:
                modo_de_jogo = partida.get('queue')
                if modo_de_jogo == 420:
                   id_partida = partida.get('gameId')
                   sql = f"INSERT INTO tb_partidas(T_ID_PARTIDA) VALUES('{id_partida}')"
                   banco.manipular_dados(sql)
                   print('Adicionado com sucesso')
            if contadorRequests == 90:
                print('MUITAS REQUISIÇÕES! AGUARDE 2 MINUTOS E RETOMAREMOS O TRABALHO!')
                sleep(121)
                contadorRequests = 0

    except Exception as ex:
        print(ex)
        recall()

def atualizarHistorico():
    sql = f'DELETE FROM tb_partidas'
    banco.manipular_dados(sql)
    historico_de_partidas()

def dadosPartida():
    print('Chegou em DadosPartida')
    sql = f"SELECT * FROM tb_partidas"
    bancoPartidas = banco.selecionar(sql)

    for partida in bancoPartidas:
        id_partida = partida[0]
        retorno = requisicao_partida(id_partida, chave_api)
        dict_participantes = retorno
        if dict_participantes == None:
            print('Partida não encontrada')
        else:
            for participante in dict_participantes:
                lista_itens = []
                id_campeao = participante.get('championId')
                status_participante = participante['stats']

                for indice in range(7):
                    item = status_participante.get(f'item{indice}')
                    if item != 0:
                        lista_itens.append(item)
                sql = f'SELECT * FROM tb_champions WHERE T_IDCHAMPION = {id_campeao}'
                dados_campaeao = banco.selecionar(sql)

                for dados in dados_campaeao:
                    build = dados[3]
                    if build == '':
                        sql = f"UPDATE tb_champions SET L_ITEM = '{json.dumps(lista_itens[:])}'" \
                              f"WHERE T_IDCHAMPION = '{id_campeao}'"
                        banco.manipular_dados(sql)
                        lista_itens.clear()
                        print('Foi adicionado uma nova partida!')
                    elif build != '':
                        j_build = json.loads(build)
                        j_build.extend(lista_itens[:])
                        sql = f"UPDATE tb_champions SET L_ITEM = '{json.dumps(j_build)}'" \
                              f"WHERE T_IDCHAMPION = '{id_campeao}'"
                        banco.manipular_dados(sql)
                        lista_itens.clear()
                        print('Foi adicionado mais outra partida')

def requisicao_partida(id_partida, chave_api):
    requisicao = requests.get(
        f'https://br1.api.riotgames.com/lol/match/v4/matches/{id_partida}?api_key={chave_api}')
    status = requisicao.status_code
    try:
        verifica_chave_dicionario = requisicao.json()['participants']

    except Timeout as ex:
        print('Houve algum problema no servidor! Aguarde alguns segundos.', ex)
        sleep(15)
        requisicao_partida(id_partida, chave_api)

    except TooManyRedirects as ex:
        print('MUITAS REQUISIÇÕES! AGUARDE DOIS MINUTOS!', ex)
        sleep(121)
        requisicao_partida(id_partida, chave_api)

    except ConnectionError as ex:
        print('ERRO: ', ex)
        sleep(15)
        requisicao_partida(id_partida, chave_api)

    except Exception as ex:
        if status == 404:
            return None
        print('ERRO DESCONHECIDO! ', ex)
        sleep(30)
        requisicao_partida(id_partida, chave_api)

    else:
        return verifica_chave_dicionario

def build_campeao(): #Sepaara os 12 itens mais utilizados numa coluna nova em  tb_champions
    print('Cheguou em Build Campeao')
    sql = f"SELECT * FROM tb_champions"
    dados_campeao = banco.selecionar(sql)

    for campeao in dados_campeao:
        build = []
        str_global_builds = campeao[3]
        titulo_campeao = campeao[2]
        nome_campeao = campeao[1]
        id_campeao = campeao[0]
        lista_global_builds = json.loads(str_global_builds)
        dicionario_mais_usados = dict(Counter(lista_global_builds))
        lista_mais_usados = sorted(dicionario_mais_usados.items(), key=itemgetter(1), reverse=True)

        limitador = 0

        for item in lista_mais_usados:
            id_item = item[0]
            sql2 = f"SELECT * FROM tb_itens WHERE T_IDITEM={id_item}"
            dados_item = banco.selecionar(sql2)
            for item2 in dados_item:
                if limitador == 12:
                    break
                elif id_item == int(item2[0]) and item2[2] != '':
                    build.append(item2[0])
                    limitador += 1
        print(f'{nome_campeao}, {titulo_campeao}\nBuild = {build}')
        sql3 = f"UPDATE tb_champions SET L_MAISUSADOS = '{json.dumps(build)}' WHERE T_IDCHAMPION = '{id_campeao}'"
        banco.manipular_dados(sql3)

def atualizar_itens():
    sql = f"UPDATE tb_champions SET L_ITEM = ''"
    banco.manipular_dados(sql)
    sql2 = f"UPDATE tb_champions SET L_MAISUSADOS = ''"
    banco.manipular_dados(sql2)
    dadosPartida()
    build_campeao()

def resetar_DB():
    resetar_Lista_Invocadores()
    adicionar_id_contas()
    atualizarHistorico()
    atualizar_itens()

def recall():
    print('Entrando em RECALL')
    sleep(121)
    sql = "SELECT * FROM tb_invocador WHERE T_ID_CONTA = 'None'"
    nao_registrados = banco.selecionar(sql)
    for registro in nao_registrados:
        id_invocador = registro[1]
        retorno = requests.get(
            f'https://br1.api.riotgames.com/lol/summoner/v4/summoners/{id_invocador}?api_key={chave_api}')
        id_conta = retorno.json().get('accountId')
        sql2 = f"UPDATE tb_invocador SET T_ID_CONTA = '{id_conta}' WHERE T_ID_INVOCADOR = '{id_invocador}'"
        banco.manipular_dados(sql2)

    atualizarHistorico()
    dadosPartida()
    build_campeao()

def atualizar_DB():
    historico_de_partidas()
    dadosPartida()
    build_campeao()
