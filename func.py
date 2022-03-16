from math import ceil, trunc
import requests
from bs4 import BeautifulSoup


geladeira = {
    'ostra': {
        'Ostra': 3,
        'Creme de Leite': 1,
        'Sal': 2,
        'Pimenta': 2,
        'Manteiga': 2,
        'Cebola': 1,
        'Alho': 1,
        'Custo': 1250
    },
    'atum':{
        'Atum': 5,
        'Manteiga': 2,
        'Folhas Verdes': 2,
        'Alface': 4,
        'Limão': 2,
        'Vinho Branco': 1,
        'Pimenta': 2,
        'Alho': 2,
        'Azeite': 2,
        'Custo': 1420
    },
    'paella':{
        'Lagosta Crua': 3,
        'Camarão Cru':5,
        'Peixe Cru':1,
        'Folhas Verdes':1,
        'Tomates':1,
        'Água':3,
        'Sal':1,
        'Pimenta':1,
        'Arroz':2,
        'Azeite':1,
        'Custo': 2460
    },
    'wagyu':{
        'Bife Cru Premium': 6,
        'Folhas verdes': 4, 
        'Limão': 2,
        'Vinho Branco': 1,
        'Cogumelo': 5,
        'Trufa Branca': 2,
        'Sal': 4,
        'Pimenta': 3,
        'Alho': 2,
        'Azeite': 6,
        'Cebola': 3,
        'Custo': 2805}  
}

################################################################################################################



def webscrapper():
    req = requests.get("https://wiki.gla.com.br/")

    if req.status_code == 200:
        content = req.content

    soup = BeautifulSoup(content, 'html.parser')
    next_event = soup.find(name='div', class_="content-event")

    return [next_event.img['src'], next_event.span['data-clock']]


def getFood(food: str, quantidade: int):
    food = food

    if food in geladeira.keys():
        resultado = dict()
        for keys in geladeira[food].keys():
            resultado[keys] = geladeira[food][keys] * quantidade
        
        mensagem = ''
        for itens in resultado.items():
            mensagem = mensagem + (f"{itens[0]}: {itens[1]}\n")

        return mensagem

    else:
        return "Erro"


def getlvl(current: int, desired: int, tier: str):
    lvc = current - 1
    lvd = desired - 1
    lvlc = ((50 * lvc * lvc * lvc) - (150 * lvc * lvc) + (400 * lvc)) / 3
    lvld = ((50 * lvd * lvd * lvd) - (150 * lvd * lvd) + (400 * lvd)) / 3

    needed = lvld - lvlc

    tier = tier.lower()
    if tier == 'bronze':
        multiplier = 3
    elif tier == 'prata':
        multiplier = 2
    elif tier == 'ouro':
        multiplier = 1
    elif tier == 'diamante':
        multiplier = 0.5

    pot ={
            'small': 1000*multiplier, 
            'med': 10000*multiplier, 
            'big': 100000*multiplier
         }

    big_needed = trunc(needed / pot['big'])
    med_needed = trunc(needed % pot['big'] / pot['med'])
    small_needed = ceil(needed % pot['med'] / pot['small'])

    return [big_needed, med_needed, small_needed] 