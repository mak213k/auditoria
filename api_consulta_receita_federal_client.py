import requests 
import json
import pandas as pd
import time
import os

import datetime as dt


def consulta_cnpj(cnpj, host="https://receitaws.com.br/v1/cnpj/"):
    
    if '.' in cnpj:
        cnpj = cnpj.replace(".","")
        print(cnpj)

    if '/' in cnpj:
        cnpj = cnpj.replace("/","")

    if '-' in cnpj:
        cnpj = cnpj.replace("-","")

    
    url = f"{host}{cnpj}"
    
    querystring = {"token":"XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

    response = requests.request("GET", url, params=querystring)

    print(response.text)

    dados = response.json()

    return dados


def gravar_csv(dados, caminho="dados_receita_240625.csv", primeira=False):
    df = pd.DataFrame([dados])
    df.to_csv(caminho, encoding="utf-8", mode='w' if primeira else 'a', header=primeira, index=False, sep=';')
    print(f"CSV salvo em: {caminho}")

if __name__ == "__main__":
    #CNPJ de empresas reais para simulação. Apenas para teste e finss educacionais.
    cnpjs = {"60.195.538/0001-20","15.578.569/0001-06","43.201.151/0001-10","15.561.610/0001-31","17.625.216/0001-45"}
    caminho_csv = "dados_receita_"+str( dt.datetime.now().timestamp() )+".csv"
    primeira = not os.path.exists(caminho_csv)

    for element in cnpjs:
        dados = consulta_cnpj(element)
        if dados:
            gravar_csv(dados, caminho=caminho_csv, primeira=primeira)
            primeira = False
        time.sleep(7)
        

    
    
    