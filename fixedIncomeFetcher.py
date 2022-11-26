import functions
import requests

if __name__ == "__main__":
    url = "https://www.btgpactualdigital.com/services/api/fixed-income/public/fixedIncome"  # URL da API
    jsonProducts = requests.get(url).json()  # Json com todos os produtos de RF do BTG

    assets = functions.filterAssetsByTime(jsonProducts)

    out = functions.printaHTML(assets, 3, "pos") + functions.printaHTML(assets, 6, "pos") + functions.printaHTML(assets, 12, "pos") #itens to be exported into the html

    text = f'''
        <!doctype html>
        <html lang="en">
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