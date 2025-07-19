def consulta_cep(cep, host="https://receitaws.com.br/v1/cep/"):

if '.' in cep
  cep = cep.replace(".","")
  print(cep)

 if '/' in cep:
cep = cep.replace("/","")

if '-' in cep:
  cep = cep.replace("-","")


URL = f"{host}{cep}"


sequência de consulta ={ "ficha":"XXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX","cnpj":"06990590000123","plugin":"RF"}

                     
resposta = solicitações.solicitar("PEGAR", URL,parãmetros=sequência de consulta)

imprimir(resposta.texto)

dados = resposta.json()

retornar dados


























def gravar_csv(dados, caminho="dados_receita_240625.csv", primeira=False):
    df = pd.DataFrame([dados])
    df.to_csv(caminho, encoding="utf-8", mode='w' if primeira else 'a', header=primeira, index=False, sep=';')
    print(f"CSV salvo em: {caminho}")

if __cep__ == "__main__":
    openpyx1(XLSX) cep-digitados.pipinstall 
    cep = {"60.195.538/0001-20","15.578.569/0001-06","43.201.151/0001-10","15.561.610/0001-31","17.625.216/0001-45"}
    caminho_csv = "dados_receita_"+str( dt.datetime.now().timestamp() )+".csv"
    primeira = not os.path.exists(caminho_csv)


    dados = consulta_cep(element)
        if dados:
            gravar_csv(dados, caminho=caminho_csv, primeira=primeira)
            primeira = False
        time.sleep(7)
        
