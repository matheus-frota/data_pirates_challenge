# Importando biblioteca
import requests
import pandas as pd
from bs4 import BeautifulSoup

def gerador_links():
    # Var. Auxiliar
    url_ = 'https://www.imdb.com/search/title/?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=b9121fa8-b7bb-4a3e-8887-aab822e0b5a7&pf_rd_r=B8SXG6NH2MBERJ86XZG1&pf_rd_s=right-6&pf_rd_t=15506&pf_rd_i=moviemeter&ref_=chtmvm_gnr_1&genres=action&explore=title_type,genres'

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
        page = soup.find_all("a")
        print("Pegando os links")
        for link in page:
            if link.get("href").count("/search/title/?genres=action&genres=") == 1:
                links.append(url+link.get("href"))
        print("Todos os links foram coletados!")

        return links
    else:
        print("{}".format(req.status_code))


links = gerador_links()
