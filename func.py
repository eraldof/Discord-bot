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

def getExp(lv):
    lv = lv-1
    return ((50 * lv * lv * lv) - (150 * lv * lv) + (400 * lv)) / 3

def getLvl(current: int, grande: int, media: int, pequena: int, tier: str):
    if tier == 'bronze':
        multiplicador = 3
    elif tier == 'prata':
        multiplicador = 2
    elif tier == 'ouro':
        multiplicador = 1
    elif tier == 'diamante':
        multiplicador = 0.5
    level = None
    exp_add = (grande*100000) + (media*10000) + (pequena*1000)
    total_exp = current+(exp_add*multiplicador)
    for i in range(0, 1001):
        if total_exp >= getExp(i) and total_exp <= getExp(i+1):
            level = i
            exp_to_up = getExp(i+1) - getExp(i)
            exceeded = total_exp - getExp(i)
            percent_lvl = (1 - exceeded / exp_to_up) * 100
            print(f"""```Exp Atingida: {total_exp}
                    Level Atingido: {level}
                    Exp P/ Upar: {exp_to_up-exceeded:0.0f}
                    Porcentagem P/ Upar: {percent_lvl:0.0f}```""")
    return (f"""Level maior que 1000.""")

def getPots(current: int, target: int, tier: str):
    if tier == 'bronze':
        multiplicador = 3
    elif tier == 'prata':
        multiplicador = 2
    elif tier == 'ouro':
        multiplicador = 1
    elif tier == 'diamante':
        multiplicador = 0.5

    pots = {'small': 1000*multiplicador, 'med': 10000 *
            multiplicador, 'big': 100000*multiplicador}
    true_needed = getExp(target)-getExp(current)
    needed = true_needed
    big_needed = 0
    med_needed = 0
    small_needed = 0
    while 1:
        if needed > pots['big']:
            big_needed += 1
            needed -= pots['big']
        elif needed > pots['med']:
            med_needed += 1
            needed -= pots['med']
        elif needed > 0:
            small_needed += 1
            needed -= pots['small']
        else:
            break
    return [big_needed, med_needed, small_needed]

def getFood(food: str, quantidade: int):
    food = food.lower()

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