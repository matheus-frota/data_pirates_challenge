# Importando biblioteca
import requests
import pandas as pd
import json
from bs4 import BeautifulSoup

def gerador_links():
    # Var. Auxiliar
    #url_ = 'https://www.imdb.com/search/title/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b9121fa8-b7bb-4a3e-8887-aab822e0b5a7&pf_rd_r=B8SXG6NH2MBERJ86XZG1&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_gnr_1&genres=action&explore=title_type,genres'
    url_ = "https://www.imdb.com/chart/top?ref_=nv_mv_250"
    url = "https://www.imdb.com"

    links = []

    # Solicitação HTTP
    req = requests.get(url_)

    # Verificação
    if req.status_code == 200:
        print('Requisição bem sucedida!')
        content = req.content

        # Gerando os links de acesso para todas as páginas de gênero.
        soup = BeautifulSoup(content, 'html.parser')
        # Filtra apenas pela tag "li"
        container_generos = soup.find_all("li", class_="subnav_item_main")
        print("Pegando os links")
        for link in container_generos:
            # Filtra apenas pela tag "a", onde estão presentes os links
            link = link.find("a")
            if link.get("href").count("/search/title?genres=") == 1:
                links.append(url+link.get("href"))
        #print(links)
        print("Todos os links foram coletados!")
        return links
    else:
        print("{}".format(req.status_code))


def info(numero_filmes = 500):
    # Chamando a função para gerar os links de cada gênero
    generos = gerador_links()
    # Criando lista contendo a quantidade de links
    qtd_film = [x+1 for x in range(0,numero_filmes,50)]
    # Url
    url = "https://www.imdb.com"
    
    for genero in generos:
        print(genero)
        # Variável de controle da quantidade de iterações
        controle = 0
        # Dicionário utilizado para criar o JSONL por gênero
        json_genero = {}
        while True:
            try:
                # Condição, se caso o algoritmo requisitar o tanto de filmes que foi setado ele
                # pula para o próximo genero
                if controle == numero_filmes:
                    # Cria um arquivo json com os filmes de cada gênero separadamente
                    with open('teste.json', 'w') as json_file:
                        json.dump(json_genero, json_file)
                    break
                # Solicitando acesso
                req = requests.get(genero)

                if req.status_code == 200:
                    content = req.content
                    soup = BeautifulSoup(content, 'html.parser')
                    # Iterando por div do filme
                    for container in soup.find_all("div", class_="lister-item-content"):
                        # Nome do filme
                        nome_filme = container.find("h3").text.split("\n")[2]
                        # Dicionário criado a partir do nome de cada filme
                        json_genero ["{}".format(nome_filme)] = {}
                        # Armazenando o ano do filme
                        json_genero["{}".format(nome_filme)]["ano"] = container.find("h3").text.split("\n")[3]
                        # Armazenando a duração do filme
                        json_genero["{}".format(nome_filme)]["duracao"] = container.select("p > .runtime")
                        # Armazenando o genero de cada filme
                        json_genero["{}".format(nome_filme)]["tipo"] = container.select("p > .genre")
                        # Armazenando a pontuação de cada filme IMDB
                        json_genero["{}".format(nome_filme)]["pontuacao"] = container.select("div > strong")
                        # COntador de filmes
                        controle+=1
                    # Pegar links da próxima página - até o máximo ou até atingir 500
                    link_next = soup.find_all("div", class_="desc")[0]
                    print(link_next)
                    # Condicionais para controlar as páginas que possuem link de next e
                    # as outras páginas que não tem link next.
                    if link_next.find("a", class_ = "lister-page-next next-page") != None:
                        genero = url + link_next.find("a", class_ = "lister-page-next next-page").get("href")
                    if link_next.find("a", class_ = "lister-page-next next-page") == None:
                        break
                else:
                    print("{}".format(req.status_code))
            except ConnectionError:
                break
    
info()
