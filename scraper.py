import bs4
import urllib.request as urllib_request
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request

response = urlopen('https://www.serebii.net/pokemon/nationalpokedex.shtml')
html = response.read().decode('latin-1')
soup = BeautifulSoup(html, 'html.parser')

pokedex = soup.find('table', {'class' : 'dextable'}).findAll('tr',recursive=False)

allPkm = []

for row in pokedex[2:]:
    pokemon = {}
    pkm = row.findAll('td', {'class': 'fooinfo'})

    pokemon['id']  = pkm[0].getText()
    pokemon['id'] = pokemon['id'].replace('\t', '').replace('\n', '').replace('\r', '')
    
    pokemon['img'] = pkm[1].find('img')['src']
    pokemon['nome'] = pkm[2].find('a').getText()
    types = pkm[3].findAll('img')
    cont = 0

    for type in types:
        types[cont] = type['src'][17:-4]
        pokemon['types'] = types[cont]
        cont = cont + 1
        
    
    cont = 0
    abilities = pkm[4].findAll('a')
    
    for ability in abilities:
        abilities[cont] = ability.getText()
        pokemon['abilities'] = abilities[cont]
        cont = cont + 1
    
    pokemon['hp']  = pkm[5].getText()
    pokemon['atk']  = pkm[6].getText()
    pokemon['def']  = pkm[7].getText()
    pokemon['spa']  = pkm[8].getText()
    pokemon['spd']  = pkm[9].getText()
    pokemon['spe']  = pkm[10].getText()
    
    allPkm.append(pokemon)
    
dataset = pd.DataFrame(allPkm)
dataset.to_json('./data.json', orient = 'split',index = False)