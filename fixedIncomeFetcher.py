import requests
from datetime import datetime

def converDate(date):
    newDate = date.split("T")[0]
    return newDate

def calculateMaturity(maturityDate):
    todayDate = datetime.today().strftime('%Y-%m-%d')

    todayDateObject = datetime.strptime(todayDate, '%Y-%m-%d')
    maturityDateObject = datetime.strptime(maturityDate, '%Y-%m-%d')

    daysToMaturity = maturityDateObject - todayDateObject

    return daysToMaturity.days

def filterAssetsByTime(objeto): #receives and object and returns the filtered data for 3, 6 and 12 months
    titulos90d = []
    titulos180d = []
    titulos360d = []

    for i in range(len(objeto)): #loop through the Json
        data = converDate(objeto[i]['applicationDeadline'])
        diasVencimento = calculateMaturity(data)

        if(85 < diasVencimento < 95):
            titulos90d.append(objeto[i])
        elif(175 < diasVencimento < 185):
            titulos180d.append(objeto[i])
        elif(355 < diasVencimento < 368):
            titulos360d.append(objeto[i])

    assets = {
        '3m': titulos90d,
        '6m': titulos180d,
        '12m': titulos360d,
    }

    return assets

def fillNone(data): #fill data that contains 'None' in it
    for x in range(len(data)):
        if data[x]['cdbCdiIndexEquivalent'] == None:
            data[x]['cdbCdiIndexEquivalent'] = 0

def filterByRate(data): #sort the objects by the "cdbCdiIndexEquivalent" attribute, then return the 3 "best options"
    fillNone(data)
    filtered = sorted(data, key = lambda k: k['cdbCdiIndexEquivalent'], reverse = True)
    filtered = filtered[:3]

    return filtered

def returnObjectAsset(asset):
    tipoProduto = asset['productName']
    tipoInv = asset['taxaCaptacaoName']
    emissor = asset['issuerName']

    taxaEq = asset['cdbCdiIndexEquivalent']

    name = f'{tipoProduto} - {tipoInv}\n{emissor}'
    taxa = f'\nTaxa equivalente: {taxaEq}'

    text = f'{name}{taxa}'
    return text

url = "https://www.btgpactualdigital.com/services/api/fixed-income/public/fixedIncome" #URL da API
jsonProducts = requests.get(url).json() #Json com todos os produtos de RF do BTG

assets = filterAssetsByTime(jsonProducts)

assets3m = assets['3m']
assets6m = assets['6m']
assets12m = assets['12m']

print("\n\n3 MESES:")
for i in range(len(assets3m)):
    item = returnObjectAsset(assets3m[i])
    print(f'\n{item}')

print("\n\n6 MESES:")
for i in range(len(assets6m)):
    item = returnObjectAsset(assets6m[i])
    print(f'\n{item}')

print("\n\n12 MESES:")
for i in range(len(assets12m)):
    item = returnObjectAsset(assets12m[i])
    print(f'\n{item}')
