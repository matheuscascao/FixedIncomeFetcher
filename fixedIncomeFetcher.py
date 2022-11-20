import functions
import requests

if __name__ == "__main__":
    url = "https://www.btgpactualdigital.com/services/api/fixed-income/public/fixedIncome"  # URL da API
    jsonProducts = requests.get(url).json()  # Json com todos os produtos de RF do BTG

    assets = functions.filterAssetsByTime(jsonProducts)

    assets3m = assets['3m']
    assets6m = assets['6m']
    assets12m = assets['12m']

    print("\n\n3 MESES:")
    for i in range(len(assets3m)):
        item = functions.returnObjectAsset(assets3m[i])
        print(f'\n{item}')

    print("\n\n6 MESES:")
    for i in range(len(assets6m)):
        item = functions.returnObjectAsset(assets6m[i])
        print(f'\n{item}')

    print("\n\n12 MESES:")
    for i in range(len(assets12m)):
        item = functions.returnObjectAsset(assets12m[i])
        print(f'\n{item}')
