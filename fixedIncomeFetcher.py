import functions
import requests
import webbrowser

if __name__ == "__main__":
    url = "https://www.btgpactualdigital.com/services/api/fixed-income/public/fixedIncome"  # URL da API
    jsonProducts = requests.get(url).json()  # Json com todos os produtos de RF do BTG
    assets = functions.filterAssetsByTime(jsonProducts)

    out = ""
    i = 1;
    print("Digite 0 para sair\n")
    while True:
        print(f"\nOpção {i}:")
        i += 1
        try:
            venc = int(input("Digite o vencimento dos títulos (3, 6 ou 12): "))
            captacao = str(input("Digite a taxa de captação, pre ou pos?: "))
            out += functions.printaHTML(assets, venc, captacao)
        except KeyError or ValueError:
            if venc == 0 or captacao == 0:
                break
            print("Entradas inválidas.")

    text = f'''
        <!doctype html>
        <html lang="pt-BR">
        <head>
            <meta charset="UTF-8">
            <link rel="stylesheet" href="style.css">
            <title>Renda Fixa</title>
        </head>
        <body>
        <h1 id="mainH1">Lista de Ativos de Renda Fixa - BTG</h1>
            {out}
        </body>
        </html>
        ''' #HTML placeholder

    file = open("sample.html", "w")
    file.write(text)
    file.close()
    webbrowser.open_new_tab('sample.html')