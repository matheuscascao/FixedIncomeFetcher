from datetime import datetime
from dateutil.relativedelta import relativedelta

pos = "cdbCdiIndexEquivalent"
pre = "cdbYearIndexEquivalent"

def converDate(date):
    newDate = date.split("T")[0]
    return newDate

def filterAssetsByTime(objeto): #receives and object and returns the filtered data for 3, 6 and 12 months
    titulos90d = []
    titulos180d = []
    titulos360d = []

    dateFormat = '%Y-%m-%d'
    todayDate = datetime.today().strftime(dateFormat)
    todayDateObject = datetime.strptime(todayDate, dateFormat)

    for i in range(len(objeto)): #loop through the Json
        data = converDate(objeto[i]['applicationDeadline'])

        if((todayDateObject + relativedelta(months=3, days=-5)).strftime(dateFormat) < data < (todayDateObject + relativedelta(months=3, days=8)).strftime(dateFormat)):
            titulos90d.append(objeto[i])
        elif((todayDateObject + relativedelta(months=6, days=-5)).strftime(dateFormat) < data < (todayDateObject + relativedelta(months=6, days=5)).strftime(dateFormat)):
            titulos180d.append(objeto[i])
        elif((todayDateObject + relativedelta(months=12, days=-5)).strftime(dateFormat) < data < (todayDateObject + relativedelta(months=12, days=5)).strftime(dateFormat)):
            titulos360d.append(objeto[i])
    assets = {
        '3': titulos90d,
        '6': titulos180d,
        '12': titulos360d,
    }

    return assets

def fillNone(data, taxaCap = "pos"): #fill data that contains 'None' in it
    dataFilled = []

    if taxaCap == "pre":
        taxa = pre
    else:
        taxa = pos

    for x in range(len(data)):
        if data[x][taxa] != None:
            dataFilled.append(data[x])

    return dataFilled

def filterByRate(data, taxaCap = "pos"): #sort the objects by the "cdbCdiIndexEquivalent" attribute, then return the 3 "best options"; 3 = number of objects
    if taxaCap == "pre":
        taxa = pre
    else:
        taxa = pos

    filtered = sorted(data, key = lambda k: k[taxa], reverse = True)
    filtered = filtered[0:3]

    return filtered

def returnObjectAsset(asset, taxaCap="pos"):
    if taxaCap == "pre":
        taxa = pre
    else:
        taxa = pos

    tipoProduto = asset['productName']
    tipoInv = asset['taxaCaptacaoName']
    emissor = asset['issuerName']
    juros = asset['tipoJuros']
    apMinima = asset['minAplicationValue']
    vencimento = converDate(asset['applicationDeadline'])

    if taxaCap == "pre":
        taxaEq = f'{asset[taxa]}% a.a.'

    else:
        taxaEq = f'{asset[taxa]}% do CDI'

    produto = f'{tipoProduto} - {tipoInv} - {emissor}'

    infos = {
        'produto': produto,
        'vencimento': vencimento,
        'taxaEq': taxaEq,
        'juros': juros,
        'apMinima': f'R$ {apMinima},00'
    }

    return infos


def printa(assets, vencimento, taxaCap = "pos"): #print on the terminal, for debugging purposes

    assets3m = assets[f'{vencimento}']
    assetsFilled = fillNone(assets3m, taxaCap)
    assetsSorted = filterByRate(assetsFilled, taxaCap)

    print(f"\n\n{vencimento} MESES {taxaCap}:")
    for i in range(len(assetsSorted)):
        item = returnObjectAsset(assetsSorted[i], taxaCap)
        print(f'\n{item}')

def printaHTML(assets, vencimento, taxaCap="pos"): #generates and "item" with html formatation

    assets3m = assets[f'{vencimento}']
    assetsFilled = fillNone(assets3m, taxaCap)
    assetsSorted = filterByRate(assetsFilled, taxaCap)

    itens = ""

    for i in range(len(assetsSorted)):
        itemObj = returnObjectAsset(assetsSorted[i], taxaCap)
        item = f'''<div class="item">
              <h3 class="item_elemento" class="produto">{itemObj['produto']}</h3>
              <h3 class="item_elemento">{itemObj['vencimento']}</h3>
              <h3 class="item_elemento">{itemObj['taxaEq']}</h3>
              <h3 class="item_elemento">{itemObj['juros']}</h3>
              <h3 class="item_elemento">{itemObj['apMinima']}</h3>
            </div>'''
        itens += item

    dataOutput = f'''
    <div class="sectionTitulos">
       <div class="header">
        <h2 class="headerH2">{vencimento} meses - {taxaCap} fixado</h2>
        <div class="descricao">
          <h3 class="descricao_elemento" class="produto">Produto</h3>
          <h3 class="descricao_elemento">Vencimento</h3>
          <h3 class="descricao_elemento">Taxa EQ. CDB </h3>
          <h3 class="descricao_elemento">Juros</h3>
          <h3 class="descricao_elemento">Aplica&#231;&atilde;o M&iacute;nima</h3>
        </div>

        {itens}    

      </div>
    </div>'''

    return dataOutput