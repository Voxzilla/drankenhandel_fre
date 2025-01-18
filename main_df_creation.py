#TODO: Aantal opties en Mapping parametriseren en refactoren
import sys



import numpy as np
import pandas as pd
import pyreadstat
import re
from collections import defaultdict
import plotly.express as px
import ipywidgets as widgets
from IPython.display import display
from tqdm import tqdm
import os
import ast
from datetime import datetime

wave = 'wave4' # AANPASSEN: welke wave
data = f"data/sav_{wave}.sav"  # Dynamically construct the file path
df_respondent, meta_respondent =  pyreadstat.read_sav(data) 
build_directory = "build" # AANPASSEN: de naam van de map waarin je alle excel files wilt krijgen (stap 3)
file_path = f"df_{wave}_draaitabel"


############################################################################################################################################
##                                                         AANTAL OPTIES                                                                  ##
############################################################################################################################################


# AANPASSEN: hier moeten het aantal opties per vraag (doe steeds het aantal opties vanuit spss + 1!) (stap 5)

# wave3
#hoeveelheid dat ze hebben gedronken
aantal_opties_V005C = 28
aantal_opties_Q28 = 73
aantal_opties_Q24 = 68

# merken
aantal_opties_V021A = 74
aantal_opties_V032A = 69
aantal_opties_V021A_hekje = 75   #V021A#68@DRINKS#a1

# verpakking bieren
aantal_opties_Q21 = 78

# plaats
aantal_opties_Q10 = 6
aantal_opties_Q27 = 74

# warme dranken
aantal_opties_V015D = 14
aantal_opties_V018D = 8


############################################################################################################################################
##                                                         MAPPINGS                                                                       ##
############################################################################################################################################

# alle mappings (stap 4)

# alle locatie codes met hun label
location_mapping = {
    'L1': 'Brasserie',
    'L2': 'Restaurant',
    'L3': 'Familierestaurant',
    'L4': 'Restaurant Buitenl',
    'L5': 'SnelwegRestaurant',
    'L6': 'Frituur',
    'L7': 'Fastfoodrestaurant',
    'L8': 'Kebabzaak/Pizzeria',
    'L9': 'Broodjeszaak',
    'L10': 'Cafe',
    'L11': 'Koffiebar',
    'L12': 'Discotheek',
    'L13': 'Ijssalon',
    'L14': 'Hotel',
    'L15': 'Camping',
    'L16': 'Bed and Breakfast',
    'L17': 'Werk',
    'L18': 'School',
    'L19': 'Openbaar Vervoer',
    'L20': 'Tankstation',
    'L21': 'Krantenwinkel',
    'L22': 'Treinstation',
    'L23': 'Bus/Metro/Tramstation',
    'L24': 'Luchthaven',
    'L25': 'Zwembad',
    'L26': 'Sportcomplex',
    'L27': 'Kartbaan/Biljart',
    'L28': 'Pretpark',
    'L29': 'Bioscoop',
    'L30': 'Museum',
    'L31': 'Feestzaal',
    'L32': 'Sportevenement',
    'L33': 'Evenement',
    'L34': 'Congres',
    'L35': 'Zorginstelling',
    'L36': 'Eethoek Warenhuis',
    'L37': 'Meubelzaak',
    'L38': 'Tuincentrum',
    'L39': 'Kledingzaak',
    'L40': 'Bakker/Slager'
}

# alle drank codes met hun label

drink_mapping = {
    'D1': 'Cola',
    'D2': 'Limonade',
    'D3': 'Ice tea / ijsthee',
    'D4': 'Bitter lemon of tonic',
    'D5': 'Water',
    'D6': 'Gearomatiseerd water (water met fruitsmaak)',
    'D7': 'Vruchtensap',
    'D8': 'Sportdrank of energiedrank (bv. Red Bull, Monster, …)',
    'D9': 'Koude koffiedrank',
    'D10': 'Koude zuiveldrank (bv. chocolademelk, fruitdrank zoals Fristi, …)',
    'D11': 'Koffie/espresso',
    'D12': 'Cappuccino / latte of andere koffie met melkbereiding',
    'D13': 'Koffie met alcohol (bv. Irish coffee)',
    'D14': 'Thee',
    'D15': 'Warme chocolademelk',
    'D16': 'Andere warme drank (bv. instant soep)',
    'D17': 'Pilsbier',
    'D18': 'Fruitbier',
    'D19': 'Witbier',
    'D20': 'Abdijbier/trappistbier/dubbel/tripel',
    'D21': 'Geuze/lambiek',
    'D22': 'Bier met toevoeging (bv. Tequila of rum)',
    'D23': 'Cider',
    'D24': 'Alcoholvrij bier',
    'D25': 'Ander bier (bv. Stout, IPA, amberkleurige bieren, ...)',
    'D26': 'Rode wijn',
    'D27': 'Cava',
    'D28': 'Champagne',
    'D29': 'Prosecco',
    'D30': 'Spumante',
    'D31': 'Andere mousserende wijn',
    'D32': 'Cocktail/mixer (bv. gin-tonic, whisky-cola, wodka-orange, pornstar-martini, … )',
    'D33': 'Mocktail (alcoholvrije cocktail)',
    'D34': 'Spirits/gedestilleerd (bv. jenever, whisky, cognac, …)',
    'D35': 'Aperitiefdrank (bv. port, sherry, martini, …)',
    'D36': 'Likeur (bv. Baileys, Passoa, Amaretto, Drambuie, …)',
    'D37': 'Hard seltzer',
    'D38': 'Witte wijn',
    'D39': 'Rosé wijn',
    'D40': 'Dessertwijn',
    'D41': 'Alcoholvrije wijn',
    'D42': 'Blond bier/sterk blond bier',
}

# alle time codes met hun label
time_mapping = {
    'T1': 'Ochtend', 
    'T2': 'Voormiddag', 
    'T3': 'Middag', 
    'T4': 'Namiddag', 
    'T5': 'Avond', 
    'T6': 'Nacht',
    'T7': 'Ochtend', 
    'T8': 'Voormiddag', 
    'T9': 'Middag', 
    'T10': 'Namiddag', 
    'T11': 'Avond', 
    'T12': 'Nacht',
    'T13': 'Ochtend', 
    'T14': 'Voormiddag', 
    'T15': 'Middag', 
    'T16': 'Namiddag', 
    'T17': 'Avond', 
    'T18': 'Nacht'
}

spirits_mapping = {
    1: 'Wodka',
    2: 'Rum',
    3: 'Gin',
    4: 'Whisky',
    5: 'Tequila',
    6: 'Cognac',
    7: 'Jenever'
}

# socio-demo codes met hun label 
geslacht_mapping = {
    2.0: 'Vrouw',
    1.0: 'Man'
}

regio_mapping = {
    2000: 'Vlaanderen',
    3000: 'Wallonië',
    4000: 'Brussel'
}

leeftijd_mapping = {
    1: '-34',
    2: '34-55',
    3: '55+'
}

beroep_mapping = {
    1: 'Arbeider',
    2: 'Bediende',
    3: 'Ambtenaar',
    4: 'Onderwijzend personeel',
    5: 'Middenkader/staffunctie',
    6: 'Hoger kader/directie',
    7: 'Vrij beroep (advocaat, dokter)',
    8: 'Middenstander (winkelier, kleinhandelaar)',
    9: 'Zelfstandige (landbouwer, ondernemer) zonder personeel',
    10: 'Zaakvoerder met 1 - 5 personeelsleden',
    11: 'Zaakvoerder met 6 - 50 personeelsleden',
    12: 'Zaakvoerder met meer dan 50 personeelsleden',
    13: 'Huisvrouw / huisman',
    14: 'Zonder beroep (invalide,...)',
    15: '(Brug)gepensioneerd',
    16: 'Werkzoekend',
    17: 'Student',
    18: 'Andere'
    
}

drink_option_mapping_kids = {
    1: 'Cola',
    2: 'Limonade',
    3: 'Ice tea / ijsthee',
    4: 'Bitter lemon of tonic',
    5: 'Water',
    6: 'Gearomatiseerd water (water met fruitsmaak)',
    7: 'Vruchtensap',
    8: 'Sportdrank of energiedrank (bv. Red Bull, Monster, …)',
    9: 'Koude zuiveldrank (bv. chocolademelk, fruitdrank zoals Fristi, …)',
    10: 'Warme chocolademelk',
    11: 'Andere drank',
    12: 'Geen drank',
    13: 'Geen idee'
}

merk_mappings = {
    1.0: 'coca_cola',
     2.0: 'Pepsi',
     3.0: 'Dr_Pepper',
     6.0: 'Ander merk glas',
     7.0: 'Weet niet',
     8.0: 'Fanta',
     9.0: 'Sprite',
     10.0: 'Schweppes',
     11.0: 'Spa_Fruit',
     12.0: '7up',
     13.0: 'Gini',
     14.0: 'Orangina',
     15.0: 'Chaudfontaine',
     16.0: 'Oasis',
     17.0: 'Bionade',
     18.0: 'Royal Bliss',
     19.0: 'San Pellegrino',
     20.0: 'Canada Dry',
     21.0: 'Gerolsteiner',
     22.0: 'Tonissteiner',
     23.0: 'Perrier',
     24.0: 'Appletiser',
     25.0: 'Homemade limonade',
     26.0: 'Lipton',
     27.0: 'Fuze_Tea',
     28.0: 'Arizona',
     29.0: 'May_Tea',
     30.0: 'Pure_Leaf',
     31.0: 'Bos',
     32.0: 'Tao',
     33.0: 'Vit hit',
     34.0: 'Homemade ice tea',
     35.0: 'Fever tree',
     36.0: 'Franklin',
     37.0: 'Double Dutch',
     38.0: 'Thomas Henry',
     39.0: 'London Essence',
     40.0: 'Evian',
     41.0: 'Spa',
     42.0: 'Vittel',
     43.0: 'Bru',
     44.0: 'Contrex',
     45.0: 'Badoit',
     46.0: 'Valvert',
     47.0: 'Nestle Pure Life',
     48.0: 'Granini',
     49.0: 'Minute Maid',
     50.0: 'Appelsientje',
     51.0: 'Capri Sun',
     52.0: 'Looza',
     53.0: 'Tropicana',
     54.0: 'Innocent',
     55.0: 'MySmoothie',
     56.0: 'Smoothie vers geperst of gemixt',
     57.0: 'Red Bull',
     58.0: 'Nalu',
     59.0: 'Aquarius',
     60.0: 'Monster',
     61.0: 'Coca Cola energy',
     62.0: 'AA Drink',
     63.0: 'Yula',
     64.0: 'Starbucks',
     65.0: 'Emmi',
     66.0: 'Alpro',
     67.0: 'Douwe Egberts',
     68.0: 'Danone Gerlati',
     69.0: 'Nutroma',
     70.0: 'Cecemel',
     71.0: 'Nesquik',
     72.0: 'Campina',
     73.0: 'Fristi',
     74.0: 'Chocovit',
     75.0: 'Hipro',
     76.0: 'La Fermiere',
     77.0: 'Dan up',
     78.0: 'Lavazza',
     79.0: 'Nespresso',
     80.0: 'Illy',
     81.0: 'Chaqwa',
     82.0: 'Caffe_vergnano',
     83.0: 'Costa_Coffee',
     84.0: 'Java',
     85.0: 'Segafredo',
     86.0: 'Ander_merk_tas',
     87.0: 'Pickwick',
     88.0: 'Twinings',
     89.0: 'Pukka',
     90.0: 'Teamasters',
     91.0: 'Clipper',
     92.0: 'Hotcemel',
     93.0: 'Callebaut',
     94.0: 'Royco',
     95.0: 'Cupasoup',
     96.0: 'Freixenet',
     97.0: 'Codorniu',
     98.0: 'Moet_Chandon',
     99.0: 'Dom_Perignon',
     100.0: 'Pommery',
     101.0: 'Veuve_Clicquot',
     102.0: 'Krug',
     103.0: 'Ruinart',
     104.0: 'Piper_Heidsieck',
     105.0: 'Vranken',
     106.0: 'Laurent_perrier',
     107.0: 'Taittinger',
     108.0: 'Bottega',
     109.0: 'ScaviRay',
     110.0: 'Mionetto',
     111.0: 'Martini',
     112.0: 'Lux',
     113.0: 'Ander_merk_Cava',
     114.0: 'Topo_Chico',
     115.0: 'Mikes',
     116.0: 'White_Claw',
     117.0: 'Frank_Seltzer',
     118.0: 'Steltz',
     119.0: 'Masalto',
     120.0: 'Rombouts',
     121.0: 'Fritz',
     122.0: 'Ritchie',
     123.0: 'Mirinda',
     124.0: 'Almdudler',
     125.0: 'Lemonaid',
     126.0: 'Chari Tea',
     127.0: 'Ordal',
     128.0: 'Kraanwater',
     129.0: 'Tapinstallatie',
     130.0: 'Aqua Panna',
     131.0: 'Grote Bidons',
     132.0: 'Rodeo',
     133.0: 'Rockstar',
     134.0: 'Nocco',
     135.0: 'Buddy',
     136.0: 'Actimel',
     137.0: 'Danonino',
     138.0: 'Melkunie',
     139.0: 'Livli',
     140.0: 'Inex',
     143.0: 'Or Coffee',
     145.0: 'Izy',
     146.0: 'Miko',
     147.0: 'Puro',
     148.0: 'Chalo',
     149.0: 'Baru',
     150.0: 'Lallier',
     151.0: 'Volvic',
     152.0: 'Zyla'
    }

dict_biermerken = {
    '1': 'Jupiler',
    '2': 'Maes',
    '3': 'Stella_Artois',
    '4': 'Carlsberg',
    '5': 'Super_8',
    '6': 'Vedett',
    '7': 'Cristal',
    '8': 'Primus',
    '9': 'Heineken',
    '10': 'Corona',
    '11': 'Boon',
    '12': 'Timmermans',
    '13': 'Oud_Beersel',
    '14': 'Mort_Subite',
    '15': 'Belle-vue',
    '16': 'Liefmans',
    '17': 'La_Chouffe',
    '18': 'Hoegaarden',
    '19': 'Rodenbach',
    '20': 'Lindemans',
    '21': 'Steenbrugge',
    '22': 'Blanche_de_Namur',
    '23': 'Ename',
    '24': 'Maredsous',
    '25': 'Affligem',
    '26': 'Leffe',
    '27': 'Westmalle',
    '28': 'Tongerlo',
    '29': 'Grimbergen',
    '30': 'Chimay',
    '31': 'Averbode',
    '32': 'Achel',
    '33': 'Rochefort',
    '34': 'Val_Dieu',
    '35': 'La_Trappe',
    '36': 'Postel',
    '37': 'St_Bernardus',
    '38': 'Hubertus',
    '39': 'Tre_Fontane',
    '40': 'Augustijn',
    '41': 'Orval',
    '42': '3fonteinen',
    '43': 'Gueuzerie_Tilquin',
    '44': 'Desperados',
    '45': 'Cubanisto',
    '46': 'Maes_Radler',
    '47': 'Stassen',
    '48': 'Strongbow',
    '49': 'Somersby',
    '50': 'Palm',
    '51': 'Brugse_zot',
    '52': 'Cornet',
    '53': 'Duvel',
    '54': 'Kwak',
    '55': 'Karmeliet',
    '56': 'Goose',
    '57': 'De_Koninck',
    '58': 'Ginette',
    '59': 'Hapkin',
    '60': 'Kasteelbier',
    '61': 'Victoria',
    '62': 'Ander_merk_Bier',
    '63': 'Weet niet',
    '64': 'Omer',
    '65': 'Triple_Anvers',
    '66': 'Bavik',
    '67': 'Bel',
    '68': 'Estaminet',
    '69': 'Bockor',
    '70': 'Brugs Tarwebier',
    '71': 'Kwaremont',
    '72': 'Tripel Lefort',
    '73': 'Charles Quint'
}

dict_sterke_dranken = {
    1: 'Gin tonic',
    2: 'Whisky Cola',
    3: 'Wodka Orange',
    4: 'Passoa (Orange)',
    5: 'Malibu (Orange)',
    6: 'Pisang Ambon (Orange)',
    7: 'Rum Cola',
    8: 'Manhattan',
    9: 'Margarita',
    10: 'Espresso Martini',
    11: 'Dry Martini',
    12: 'Negroni',
    13: 'Old fashioned',
    14: 'Aperol Spritz',
    15: 'Pina Colada',
    16: 'Moscow Mule',
    17: 'Dark & Stormy',
    18: 'Tequila Sunrise',
    19: 'Scroppino',
    20: 'Pornstar Martini',
    21: 'Mojito',
    22: 'Mojito Razz',
    23: 'Daiguiri',
    24: 'Long Island Ice Tea',
    25: 'Caipirinha',
    26: 'Whisky Sour',
    27: 'Amaretto Sour',
    28: 'Liquor 43 Sour',
    29: 'Alcoholvrije Gin Tonic',
    30: 'Alcoholvrije aperol Spritz',
    31: 'Alcoholvrije Pina Colada',
    32: 'Alcoholvrije Moscow Mule',
    33: 'Alcoholvrije Dark & Stormy',
    34: 'Alcoholvrije Pornstar Martini',
    35: 'Alcoholvrije Mojito',
    36: 'Alcoholvrije Daiquiri',
    37: 'Alcoholvrije Caipirinha',
    38: 'Wodka',
    39: 'Rum',
    40: 'Gin',
    41: 'Whisky',
    42: 'Tequila',
    43: 'Cognac',
    44: 'Jenever',
    45: 'Porto',
    46: 'Vermouth',
    47: 'Aperol',
    48: 'Ricard',
    49: 'Picon',
    50: 'Campari',
    51: 'Crodino',
    52: 'Lillet',
    53: 'Gluhwein',
    54: 'Sangria',
    55: 'Cointreau',
    56: 'Baileys',
    57: 'Amaretto',
    58: 'Limoncello',
    59: 'Advocaat',
    60: 'Triple sec',
    61: 'Sambuca',
    62: 'Kahlua',
    63: 'Grand Marnier',
    64: 'Licor 43',
    65: 'Mandarine Napoleon',
    66: 'Jägermeister',
    67: 'Andere [DRINK]',
    68: 'Weet niet'
}

tijden = ['Ochtend','Voormiddag','Middag','Namiddag','Avond','Nacht']


############################################################################################################################################
##                                                         HELPER FUNCTIES                                                                ##
############################################################################################################################################

def split_string_eerste_deel(input_string):
    """ Deze functie returned het deel voor de eerste '-' of '[' die soms in de labels voorkomen """
    split_string = re.split(r'[\-\[]', input_string, maxsplit=1)[0]
    return split_string.strip()

def gewogenSom(df_x):
    return round(df_x['Weging'].sum())
    
def procent(x, totaal):
    result = str(round((x/totaal)*100)) + '%'
    return result

############################################################################################################################################
##                                                         FUNCTIES LOCTIMEDRINK                                                          ##
############################################################################################################################################

def maak_loctimedrink_df_voor_draaitabel(df_respondent):
    """van de df van de respondent, maak een df voor loctime drink met: loctimedrink waarden, socio demografische waarden, 
        hoeveelheid, merk en plaats  van de gedronken drankjes
        - Weging = Weging respondent
        - Hoeveelheid = aantal drankjes gedronken aangeduid 
        - loctimedrinkweging =  hetzelfde voor elke loctimedrink ( plaatsen aangeduid/ plaatsen in random) * (drankjes aangeduid/ drankjes in random)
        - Gewogen_hoeveelheid = loctimedrinkweging * het aantal drankjes * weging respondent   
        - Socio-demo dingen zoals regio, geslahht,... (kan nog extra erbij)
        """
    loc_time_drink_columns= [col for col in df_respondent.columns if col.startswith("LOCTIMEDRINKS_a")] # Dit zijn maar 25 colums
    
    identifier_columns = ['ID','Weging', 'Leeftijd3N', 'Geslacht', 'REGIO', 'Beroep', 'end_date']
    
    # Filter de kolommen om alleen de kolommen met niet-lege waarden te behouden
    non_zero_loc_time_drink_columns = [col for col in loc_time_drink_columns if df_respondent[col].notna().any()]
    # in de praktijk worden er geen colommen verwijder!

    LOCTIMEDRINK = pd.melt(df_respondent, id_vars=identifier_columns, value_vars=non_zero_loc_time_drink_columns, 
                        var_name='LOCTIMEDRINK', value_name='LOCTIMEDRINK_Value')

    df_loctimedrink = pd.DataFrame(LOCTIMEDRINK[LOCTIMEDRINK['LOCTIMEDRINK_Value'] != ''])

    #splits loctimedrink in drie verschillende kolommen
    df_loctimedrink[['Loc', 'Time', 'Drink']] = df_loctimedrink['LOCTIMEDRINK_Value'].str.split('-', n=2, expand=True)
    df_loctimedrink['Drink'] = df_loctimedrink['Drink'].str.split('-', n=2, expand=True)[1]  #verwijder  het streepje

    #geef elke code de waarde van hun label (L1 = brasserie etc.)
    df_loctimedrink['Loc'] = df_loctimedrink['Loc'].map(location_mapping)
    df_loctimedrink['Time'] = df_loctimedrink['Time'].map(time_mapping)
    df_loctimedrink['Drink'] = df_loctimedrink['Drink'].map(drink_mapping)
    df_loctimedrink['Geslacht'] = df_loctimedrink['Geslacht'].map(geslacht_mapping)
    df_loctimedrink['REGIO'] = df_loctimedrink['REGIO'].map(regio_mapping)
    df_loctimedrink['Leeftijd3N'] = df_loctimedrink['Leeftijd3N'].map(leeftijd_mapping)
    # df_loctimedrink['Beroep'] = df_loctimedrink['Beroep'].map(beroep_mapping)




    # Drop rows where any of the mapped columns have NaN
    df_loctimedrink = df_loctimedrink.dropna(subset=['Loc', 'Time', 'Drink'])

    # Converteer de kolom 'end_date' naar datetime en voeg een nieuwe kolom 'Maand_Jaar' toe met maand en jaar
    df_loctimedrink['end_date'] = pd.to_datetime(df_loctimedrink['end_date'], format="%d/%m/%Y %H:%M:%S")
    df_loctimedrink['Maand_Jaar'] = df_loctimedrink['end_date'].dt.to_period('M')
    
    # Voeg een nieuwe kolom toe met maand en jaar als string formaat
    # Bijvoorbeeld: 'Januari 2025'
    df_loctimedrink['Maand_Jaar'] = df_loctimedrink['end_date'].dt.strftime('%B %Y')
    # Verwijder de kolom 'end_date'
    df_loctimedrink.drop(columns=['end_date'], inplace=True)

    print('Start het toevoegen van de kolom loctimedrink weging')

    df_loctimedrink = add_loctimedrink_weging(df_loctimedrink, df_respondent, 'TOTAAL')


    # ### FRE ###
    # print("df_loctimedrink, eerste 300 lijnen")
    # #desired_columns = ["Loc", "Time", "Drink", "Merk"]  # only these columns
    # #df_visual = df_loctimedrink[desired_columns].head(100)
    # df_visual = df_loctimedrink.head(100)
    # print(df_visual.to_string(index=False))
    # sys.exit()  # The script stops here.

     # #maak extra kolom met welk merk ze hebben gedronken
    print('start Merk ')
    df_loctimedrink['Merk'] = df_loctimedrink.progress_apply(get_merk, axis=1)  # For each row in df_loctimedrink, the get_merk function is called, passing the row as a pandas Series (row).
    df_loctimedrink = df_loctimedrink.loc[df_loctimedrink['Merk']!='/']
    # Explode 'Merk' kolom
    df_loctimedrink = df_loctimedrink.explode('Merk')



    


    #maak extra kolom met hoeveel eenheden ze hebben gedronken
    print('start Hoeveelheid ') 
    df_loctimedrink['Hoeveelheid'] = df_loctimedrink.progress_apply(get_hoeveelheid, axis=1)
    df_loctimedrink['Verpakking'] = df_loctimedrink.progress_apply(get_verpakking, axis=1)
    df_loctimedrink['Plaats'] = df_loctimedrink.progress_apply(get_drink_plaats, axis=1)

    ## GESLACHT
    # dataframes kopies van de delen van de accurate respondenten in de groep
    df_mannen = df_respondent[df_respondent['Geslacht'] == 1].copy()
    df_LTD_mannen = df_loctimedrink[df_loctimedrink['Geslacht'] == 'Man'].copy()
    df_loctimedrink_mannen = add_loctimedrink_weging(df_LTD_mannen, df_mannen, 'MAN')
    df_vrouwen = df_respondent[df_respondent['Geslacht'] == 2].copy()
    df_LTD_vrouwen = df_loctimedrink[df_loctimedrink['Geslacht'] == 'Vrouw'].copy()
    df_loctimedrink_vrouwen = add_loctimedrink_weging(df_LTD_vrouwen, df_vrouwen, 'VROUW')
    # Voeg de waarden toe op basis van de indices van mannen en vrouwen
    df_loctimedrink.loc[df_loctimedrink['Geslacht'] == 'Man', 'LTD_GESLACHT'] = df_loctimedrink_mannen['LTD_MAN']
    df_loctimedrink.loc[df_loctimedrink['Geslacht'] == 'Vrouw', 'LTD_GESLACHT'] = df_loctimedrink_vrouwen['LTD_VROUW']

    ## LEEFTIJD
    df_min34 = df_respondent[df_respondent['Leeftijd3N'] == 1].copy()
    df_LTD_min34 = df_loctimedrink[df_loctimedrink['Leeftijd3N'] == '-34'].copy()
    df_loctimedrink_min34  = add_loctimedrink_weging(df_LTD_min34, df_min34, 'MIN34')
    df_tussen34en55 = df_respondent[df_respondent['Leeftijd3N'] == 2].copy()
    df_LTD_tussen34en55 = df_loctimedrink[df_loctimedrink['Leeftijd3N'] == '34-55'].copy()
    df_loctimedrink_tussen34en55 = add_loctimedrink_weging(df_LTD_tussen34en55, df_tussen34en55, 'TUSSEN')
    df_plus55 = df_respondent[df_respondent['Leeftijd3N'] == 3].copy()
    df_LTD_plus55 = df_loctimedrink[df_loctimedrink['Leeftijd3N'] == '55+'].copy()
    df_loctimedrink_plus55 = add_loctimedrink_weging(df_LTD_plus55, df_plus55, 'PLUS')
    
    # Voeg de waarden toe op basis van de indices van LEEFTIJD
    df_loctimedrink.loc[df_loctimedrink['Leeftijd3N'] == '-34', 'LTD_LEEFTIJD'] = df_loctimedrink_min34['LTD_MIN34']
    df_loctimedrink.loc[df_loctimedrink['Leeftijd3N'] == '34-55', 'LTD_LEEFTIJD'] = df_loctimedrink_tussen34en55['LTD_TUSSEN']
    df_loctimedrink.loc[df_loctimedrink['Leeftijd3N'] == '55+', 'LTD_LEEFTIJD'] = df_loctimedrink_plus55['LTD_PLUS']

    ## REGIO
    df_vlamingen = df_respondent[df_respondent['REGIO'] == 2000].copy()
    df_LTD_vlamingen = df_loctimedrink[df_loctimedrink['REGIO'] == 'Vlaanderen'].copy()
    df_loctimedrink_vlamingen = add_loctimedrink_weging(df_LTD_vlamingen, df_vlamingen, 'VLAM')
    df_walen = df_respondent[df_respondent['REGIO'] == 3000].copy()
    df_LTD_walen = df_loctimedrink[df_loctimedrink['REGIO'] == 'Wallonië'].copy()
    df_loctimedrink_walen = add_loctimedrink_weging(df_LTD_walen, df_walen, 'WAL')
    df_brussel = df_respondent[df_respondent['REGIO'] == 4000].copy()
    df_LTD_brussel = df_loctimedrink[df_loctimedrink['REGIO'] == 'Brussel'].copy()
    df_loctimedrink_brussel = add_loctimedrink_weging(df_LTD_brussel, df_brussel, 'BRU')
    df_loctimedrink.loc[df_loctimedrink['REGIO'] == 'Vlaanderen', 'LTD_REGIO'] = df_loctimedrink_vlamingen['LTD_VLAM']
    df_loctimedrink.loc[df_loctimedrink['REGIO'] == 'Wallonië', 'LTD_REGIO'] = df_loctimedrink_walen['LTD_WAL']
    df_loctimedrink.loc[df_loctimedrink['REGIO'] == 'Brussel', 'LTD_REGIO'] = df_loctimedrink_brussel['LTD_BRU']

    #weging2 = hoeveelheid * weging respondent
    # we wegen de hoeveelheden van de drinks per respondent
    df_loctimedrink['Hoeveelheid_Totaal'] = df_loctimedrink['Hoeveelheid']*df_loctimedrink['Weging']*df_loctimedrink['LTD_TOTAAL']
    df_loctimedrink['Hoeveelheid_Merk'] = df_loctimedrink['Hoeveelheid']*df_loctimedrink['Weging']
    
    ## voor de socio demos
    df_loctimedrink['Hoeveelheid_Geslacht'] = df_loctimedrink['Hoeveelheid']*df_loctimedrink['Weging']*df_loctimedrink['LTD_GESLACHT']
    df_loctimedrink['Hoeveelheid_Regio'] = df_loctimedrink['Hoeveelheid']*df_loctimedrink['Weging']*df_loctimedrink['LTD_REGIO']
    df_loctimedrink['Hoeveelheid_Leeftijd'] = df_loctimedrink['Hoeveelheid']*df_loctimedrink['Weging']*df_loctimedrink['LTD_LEEFTIJD']

    df_loctimedrink['Wave'] = wave
    
    columns_to_keep = ['Loc', 'Time', 'Drink', 'Hoeveelheid_Totaal','Merk','Hoeveelheid_Merk', 'Verpakking', 'Plaats', 'Geslacht', 'Hoeveelheid_Geslacht', 'REGIO', 'Hoeveelheid_Regio', 'Leeftijd3N', 'Hoeveelheid_Leeftijd', 'Wave']

    df_result = df_loctimedrink[columns_to_keep]
    return df_result 

#########################################################

# functies voor de loctimedrink df aan te maken
def get_hoeveelheid(row):
    """voor deze row, neem de waarde in de kolom die de hoeveelheid gedronken van de drank in de loctime value weergeeft """
    drink = row['Drink']
    match = re.search(r'a(\d+)', row['LOCTIMEDRINK'])  # Look for 'a' followed by digits
    a = match.group(1)  # Extract the number after 'a'
    id = row['ID']  # Store the ID for reference
    merk = row['Merk']
    # Create a reverse mapping (beer name to number)
    reverse_dict_biermerken = {value: key for key, value in dict_biermerken.items()}
    merk_nr = reverse_dict_biermerken.get(merk)
    
    reverse_dict_sterke = {value: key for key, value in dict_sterke_dranken.items()}
    sterke_nr = reverse_dict_sterke.get(merk)
    # Predefine all possible column patterns
    columns_to_check = [f'V005C_O{o}_a1#DRINKS#a{a}' for o in range(1, aantal_opties_V005C)] # HARDCODED: kolom variabele
    # columns_to_check += [f'Q28_O{optie_num}_a1#DRINKS#a{a}' for optie_num in range(1, aantal_opties_Q28)] # HARDCODED: kolom variabele
    # columns_to_check += [f'Q24_O{sterke_nr}_a1#DRINKS#a{a}' for optie_num in range(1, aantal_opties_Q24)] # HARDCODED: kolom variabele
    columns_to_check += [f'Q28_O{merk_nr}_a1#DRINKS#a{a}'] # HARDCODED: kolom variabele
    columns_to_check += [f'Q24_O{sterke_nr}_a1#DRINKS#a{a}'] # HARDCODED: kolom variabele
    columns_to_check.append(f'Q24#O68#a1@DRINKS#a{a}') # HARDCODED: kolom variabele

    # Filter existing columns in the dataframe
    existing_columns = [col for col in columns_to_check if col in df_respondent.columns]

    # Find the first valid value in the selected columns for the given ID
    hoeveelheid = df_respondent.loc[df_respondent['ID'] == id, existing_columns].bfill(axis=1).iloc[0].dropna()
    if not hoeveelheid.empty:
        # AANPASSEN: ALS WE OOK MINSTENS 1 WILLEN? HIER AANPASSEN (soms is er nul aangeduid als hoeveelheid)
        return min(40, hoeveelheid.iloc[0]) # AANPASSEN: waarde hoeveelheid wordt afgetopt op 40
    else:
        return 1  # AANPASSEN: waarde hoeveelheid is 1 als er niks is aangeduid

def get_merk(row):
    """Voor deze row, neem de labels van alle kolommen waar een waarde groter dan nul in staat"""
    match = re.search(r'a(\d+)', row['LOCTIMEDRINK'])  # Zoek naar 'a' gevolgd door cijfers
    a = match.group(1)  # Haal het nummer na 'a' op => a=1..25
    id = row['ID']  # Bewaar het ID voor referentie

    # Vooraf gedefinieerde mogelijke kolompatronen
    columns_to_check = [f'V005A#DRINKS#a{a}']  # HARDCODED: variabele namen frisdranken
    columns_to_check += [f'V032A_{optie_num}#DRINKS#a{a}' for optie_num in range(1, aantal_opties_V032A)]  # HARDCODED: variabele namen cocktails, etc
    columns_to_check += [f'V021A_{optie_num}#DRINKS#a{a}' for optie_num in range(1, aantal_opties_V021A)]  # HARDCODED: variabele namen bieren, etc
    columns_to_check += [f'V021A#{optie_num}@DRINKS#a{a}' for optie_num in range(1, aantal_opties_V021A_hekje)]  # HARDCODED: variabele namen bieren, etc
    # Uitzondering voor wave3
    #columns_to_check.append(f'V032A#69@DRINKS#a{a}')  # Alleen voor wave3: jama heeft geen label
    columns_to_check += [f'V032A#69@DRINKS#a{a}']  # HARDCODED: variabele namen bieren, etc

    # Filter bestaande kolommen in de dataframe
    existing_columns = [col for col in columns_to_check if col in df_respondent.columns]

    # Zoek naar waarden groter dan nul in de geselecteerde kolommen voor het gegeven ID
    merk_values = df_respondent.loc[df_respondent['ID'] == id, existing_columns].iloc[0]
    #print(merk_values)
    
    # Filter op waarden groter dan nul
    merk_values = merk_values[merk_values > 0]
    
    # Maak een lijst om alle gevonden labels op te slaan
    merk_labels = []

    # Loop door alle gevonden waarden groter dan nul
    for column, merk_value in merk_values.items():
        if isinstance(column, str) and column.startswith('V032A#69@DRINKS'):
            merk_label = "Martini" #HARDCODED uitzondering
        else: 
            if isinstance(column, str) and column.startswith('V005A#DRINKS'):  # HARDCODED: bij de kolommen V005A#DRINKS zit de namen in de opties label
                ## dit is nieuw!!!
                # merk_label = meta_respondent.variable_value_labels[column].get(merk_value, 'Unknown')
                merk_label = merk_mappings.get(merk_value)
                merk_label = split_string_eerste_deel(merk_label)
            
            else:
                merk_label = meta_respondent.column_names_to_labels.get(column, 'Unknown') # bij de andere in de gewone label
                merk_label = split_string_eerste_deel(merk_label)

            # Voeg het merk_label toe aan de lijst
            merk_labels.append(merk_label)

    return merk_labels

def initialize_dict_loctime():
    """Initialize de loctime dicts, die voor elke loc-time een waarde nul hebben"""
    keys = [f'{location}-{time}' for location in location_mapping.values() for time in time_mapping.values()]
    
    return defaultdict(float, {key: 0 for key in keys})

def initialize_dict_loctimedrink():
    """Initialize de loctime dicts, die voor elke loc-time een dict hebben met voor alle dranken de waarde nul"""
    all_drinks = list(drink_mapping.values())
    keys = [f'{location}-{time}' for location in location_mapping.values() for time in time_mapping.values()]
    drinks_dict_template = {drink: 0 for drink in all_drinks}
    default_drinks_dict = lambda: drinks_dict_template.copy()
    
    return defaultdict(default_drinks_dict, {key: drinks_dict_template.copy() for key in keys})

#########################


#####
def frequency_gekocht_loctime(loctime_frequency, df_respondent):
    """vul de dict in  loctime_frequency, die staat voor het aantal keer dat er iets is gekocht op deze loctime"""
    for location_code, location_name in location_mapping.items():
        location_number = location_code[1:]  # Extract the number part of the location code
        for time_code, time_name in time_mapping.items():
            time_number = time_code[1:]
            column_name = f'V003_{time_number}#LOCATIONS#{location_number}'
            
            if column_name in df_respondent.columns:
                # Sum the 'Weging' column where the specified condition is met
                loctime_key = f'{location_name}-{time_name}'
                loctime_frequency[loctime_key] += df_respondent[df_respondent[column_name] == 1]['Weging'].sum()

def frequency_drink_loctime(loctimedrink_frequency, loctime_random, df_respondent):
    """vul de dicts in loctimedrink_frequency en loctime_random, die staat voor het aantal keer dat een bepaald drankje is gekocht op deze loctime 
        en voor het aantal keer dat deze loctime voorkomt in de random loctime"""
    # Vooraf filteren van de DataFrame voor de relevante kolommen
    relevant_columns = [f'LOCTIME_a{a}' for a in range(1, 6)] + [
        f'V004_{drink_code[1:]}#LOCATION_TIME#a{a}'
        for drink_code in drink_mapping.keys()
        for a in range(1, 6)
    ]

    # Filter de DataFrame om alleen relevante kolommen te houden
    filtered_df = df_respondent[relevant_columns + ['Weging']].copy()

    # Loop door elke rij van de gefilterde DataFrame
    for _, row in filtered_df.iterrows():
        for a in range(1, 6):
            loctime_column = f'LOCTIME_a{a}'
            if pd.notna(row[loctime_column]):
                # Extract location en time
                loctime_value = row[loctime_column]
                if loctime_value:
                    location, time = loctime_value.split('-')[:2]
                    location = location_mapping.get(location)
                    time = time_mapping.get(time)
                    loctime_key = f'{location}-{time}'
                    loctime_random[loctime_key] += row['Weging']
                    
                    # Verwerk alle dranken voor deze loctime
                    for drink_code, drink_name in drink_mapping.items():
                        drink_number = drink_code[1:]
                        column_name = f'V004_{drink_number}#LOCATION_TIME#a{a}'
                        
                        if column_name in row.index and row[column_name] == 1:
                            loctimedrink_frequency[loctime_key][drink_name] += row['Weging']

def frequency_drink_loctime_random(loctime_drink_random, df_loctimedrink, df_respondent):
    """vul de dict loctime_drink_random in die telt hoe vaak de loctimedrink in random voorkomt"""
    for _, row in df_loctimedrink.iterrows():
        loc = str(row['Loc'])
        time = str(row['Time'])
        drink = str(row['Drink'])
        loctime = loc+'-'+time
        # loc = row['Loc']
        # time = row['Time']
        # drink = row['Drink']
        # loctime = loc+'-'+time
        # Verhoog de teller voor deze combinatie
        loctime_drink_random[loctime][drink] += row['Weging']

###################################################

def add_loctimedrink_weging(df_loctimedrink, df_respondent_deel, socio):
    """ Loctimedrink_Weging is de waarde waarmee de hoeveelheid per loctimedrink wordt gewogen (is dus hetwelfde voor elke zelfde loctimedrink)"""
    df_result = df_loctimedrink.copy()

    loctime_frequency = initialize_dict_loctime()
    loctime_random = initialize_dict_loctime()
    loctime_drink_random = initialize_dict_loctimedrink()
    loctimedrink_frequency = initialize_dict_loctimedrink()
        
    #bereken de dicts   
    frequency_gekocht_loctime(loctime_frequency, df_respondent_deel)
    frequency_drink_loctime_random(loctime_drink_random,df_result, df_respondent_deel)
    # frequency_drink_loctime_random(loctime_drink_random,df_result, df_respondent_deel)
    frequency_drink_loctime(loctimedrink_frequency,loctime_random, df_respondent_deel)

    df_result[f'LTD_{socio}'] = df_result.progress_apply(add_loctimedrink_weging_per_row, axis=1, args=(loctime_frequency,loctime_random,loctimedrink_frequency,loctime_drink_random))
    
    return df_result
    
def add_loctimedrink_weging_per_row(row,loctime_frequency,loctime_random,loctimedrink_frequency,loctime_drink_random):
    """maak een extra kolom met een tweede weging voor elke loctimedrink"""
    loc = str(row['Loc'])
    time = str(row['Time'])
    drink = str(row['Drink'])
    
    loctime = loc+'-'+time
    
    loctime_frequency_value = loctime_frequency[loctime]
    loctime_random_value = loctime_random[loctime]
    loctimedrink_frequency_value = loctimedrink_frequency[loctime][drink]
    loctime_drink_random_value = loctime_drink_random[loctime][drink]
    if (loctime_drink_random_value == 0) or (loctime_random_value == 0) or (loctime_frequency_value==0) or (loctimedrink_frequency_value==0):
        Loctimedrink_Weging = 0
    else:
        Loctimedrink_Weging = (loctime_frequency_value/loctime_random_value) * (loctimedrink_frequency_value/loctime_drink_random_value)
    return Loctimedrink_Weging


def get_verpakking(row):
    """voor deze row, neem de waarde in de kolom die de verpakking van de drank in de loctime value weergeeft """
    drink = row['Drink']
    match = re.search(r'a(\d+)', row['LOCTIMEDRINK'])  # Look for 'a' followed by digits
    a = match.group(1)  # Extract the number after 'a'
    id = row['ID']  # Store the ID for reference

    merk = row['Merk']
    # Create a reverse mapping (beer name to number)
    reverse_dict_biermerken = {value: key for key, value in dict_biermerken.items()}
    merk_nr = reverse_dict_biermerken.get(merk)
    
    ##HIER MOET JE DE JUISTE KOLOM HEBBEN
    # Predefine all possible column patterns
    columns_to_check = [f'V005B#DRINKS#a{a}']                    # HARDCODED: variabele kolomnaam 
    columns_to_check += [f'Q21_O{merk_nr}#DRINKS#a{a}']  # HARDCODED: variabele kolomnaam 

    # Filter existing columns in the dataframe
    existing_columns = [col for col in columns_to_check if col in df_respondent.columns]

    # Zoek naar waarden groter dan nul in de geselecteerde kolommen voor het gegeven ID
    verpakking_values = df_respondent.loc[df_respondent['ID'] == id, existing_columns].iloc[0]
    
    # Get the first valid value and the corresponding column
    verpakking_values = verpakking_values[verpakking_values > 0]
    if not verpakking_values.empty:
        column = verpakking_values.index[0]
        verpakking_value = verpakking_values.iloc[0]
        verpakking_label = meta_respondent.variable_value_labels[column].get(verpakking_value)  # HARDCODED: hier zit de waarde van de verpakking in de optie label
        return verpakking_label
    else:
        return '/'
        
def get_drink_plaats(row):
    """Voor deze row, neem de waarde in de kolom die de plaats van de drank in de loctime value weergeeft."""
    match = re.search(r'a(\d+)', row['LOCTIMEDRINK'])  # Zoek naar 'a' gevolgd door cijfers
    a = match.group(1)  # Haal het nummer na 'a' op
    id = row['ID']  # Bewaar het ID voor referentie
    merk = row['Merk']
    # reverse_dict_biermerken = {value: key for key, value in dict_biermerken.items()}
    # merk_nr = reverse_dict_biermerken.get(merk)
    # print(f"merk: {merk}, merknr: {merk_nr}")
    
    # Vooraf gedefinieerde mogelijke kolompatronen
    columns_to_check = [f'Q10_{optie_num}#DRINKS#a{a}' for optie_num in range(1, aantal_opties_Q10)]  # HARDCODED: variabele voor de kolom van Q10
    columns_to_check += [f'Q27_O{optie_num}#DRINKS#a{a}' for optie_num in range(1, aantal_opties_Q27)] # HARDCODED: variabele voor de kolom van Q27

    # Filter bestaande kolommen in de dataframe
    existing_columns = [col for col in columns_to_check if col in df_respondent.columns]

    # Zoek de waarden in de geselecteerde kolommen voor het gegeven ID
    plaats_values = df_respondent.loc[df_respondent['ID'] == id, existing_columns].iloc[0]
    
    # Filter op waarden groter dan nul
    plaats_values = plaats_values[plaats_values > 0]
    
    # Maak een lijst om alle gevonden labels op te slaan
    plaats_labels = []

    # Loop door alle gevonden waarden groter dan nul
    for column, plaats_value in plaats_values.items():
        # Check de labelbron op basis van het kolompatroon
        col_label = meta_respondent.column_names_to_labels.get(column, 'Unknown')
        col_label = split_string_eerste_deel(col_label)
        if isinstance(column, str) and column.startswith('Q27') and (col_label == merk) :  # HARDCODED: bij de kolommen V005A#DRINKS zit de namen in de opties label
            plaats_label = meta_respondent.variable_value_labels[column].get(plaats_value, 'Unknown')
            plaats_label = split_string_eerste_deel(plaats_label)
            # Voeg het merk_label toe aan de lijst
            plaats_labels.append(plaats_label)
        elif isinstance(column, str) and column.startswith('Q10'):
            plaats_label = col_label # HARDCODED: bij de andere in de gewone label
            # Voeg het merk_label toe aan de lijst
            plaats_labels.append(plaats_label)
        
    return plaats_labels

##################################################################


def main():
    """ De main functie die eerst alle dataframes maakt en dan deze allemaal opslaat in excel """
    tqdm.pandas()
    
    print('start loctimedrink_df ')
    # df_loctimedrink = maak_loctimedrink_df_merken(df_respondent)
    df_loctimedrink = maak_loctimedrink_df_voor_draaitabel(df_respondent)
    df_loctimedrink.to_json(file_path, orient='records') # bewaar in JSON zodat lijsten lijsten blijven 
    print(f'Dataframe opgeslagen in {file_path}')
    

# START HIER DE MAIN FUCNTIE
main()

# ISSUES
# 1: OK: De volgende merken komen niet in het tabellen rapport (noch in de draaitabel), lijkt een fout te zijn. => opgelost
# Bavik Super Pils
# Bel Pils
# Estaminet
# Bockor

# 2: OK: Deze zijn waarschijnlijk geschrapt vanaf wave 3
# Steenbrugge
# Martini
# Lux

# 3: TODO: Unknown bij Gin en bij Whisky => die zitten er zelfs niet in... (Voolopig doen we dit niet)
# Gin: Gordon, Bombay, Tanqueray, Thomas Henry, Unknown, Ander merk glas, Weet niet
# Whisky: Johnie_walker, william_lawsons, jack_daniels, Glenfiddich, ander merk glas, Unknwon, Weet niet. 

# 4: OK: drankje 69 nog vinden => Claire?

# 5: TODO: Draaitabel maken 
# 6: TODO: STAPELEN (in de mate van het mogelijke)