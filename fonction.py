from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import warnings
import re
from io import BytesIO
import zipfile

import matplotlib.pyplot as plt

from matplotlib.patches import Rectangle
from matplotlib.patches import Arc
from matplotlib.patches import ConnectionPatch

import io
from PIL import Image

def draw_pitch_horizontal():
    # focus on only half of the pitch
    #Pitch Outline & Centre Line
    fig=plt.figure() #set up the figures
    fig.set_size_inches(10, 7)
    ax=fig.add_subplot(1,1,1)
    
    Pitch = Rectangle([0,0], width = 120, height = 70, fill = False)
    essai1 = Rectangle([0,0], width = 10, height = 70, fill = False, color='gray',hatch='/')
    essai2 = Rectangle([110,0], width = 1070, height = 70, fill = False, color='gray',hatch='/')
    en_but1 = ConnectionPatch([10,0], [10,80], "data", "data")
    en_but2 = ConnectionPatch([110,0], [110,70], "data", "data")
    cinq_metres1 = ConnectionPatch([15,0], [15,70], "data", "data",ls='--',color='gray')
    cinq_metres2 = ConnectionPatch([105,0], [105,70], "data", "data",ls='--',color='gray')
    midline = ConnectionPatch([60,0], [60,70], "data", "data")
    vingtdeux_metres1 = ConnectionPatch([32,0], [32,70], "data", "data")
    vingtdeux_metres2 = ConnectionPatch([88,0], [88,70], "data", "data")
    dix_metres1 = ConnectionPatch([50,0], [50,70], "data", "data",ls='--',color='gray')
    dix_metres2 = ConnectionPatch([70,0], [70,70], "data", "data",ls='--',color='gray')
    centreCircle = plt.Circle((60,35),0.5,color="black", fill = True)
    poteau1a = plt.Circle((10,32.2),0.5,color="black", fill = True)
    poteau1b = plt.Circle((10,37.8),0.5,color="black", fill = True)
    poteau2a = plt.Circle((110,32.2),0.5,color="black", fill = True)
    poteau2b = plt.Circle((110,37.8),0.5,color="black", fill = True)

    element = [essai1, essai2, Pitch, en_but1, en_but2, cinq_metres1, cinq_metres2, midline, vingtdeux_metres1, 
    vingtdeux_metres2,centreCircle,poteau1a,poteau1b,poteau2a,poteau2b,dix_metres1,dix_metres2]
    for i in element:
        ax.add_patch(i)

    rectangle1 = Rectangle([88,60],width= 22, height = 10, fill = True, color='darkred',alpha=0.5)
    rectangle2 = Rectangle([100,10],width= 10, height = 50, fill = True, color='darkred',alpha=0.5)
    rectangle3 = Rectangle([88,0],width= 22, height = 10, fill = True, color='darkred',alpha=0.5)
    
    for rect in [rectangle1, rectangle2, rectangle3]:
        ax.add_patch(rect)

    rectangle1 = Rectangle([10,0],width= 78, height = 10, fill = True, color='darkblue',alpha=0.15)
    rectangle2 = Rectangle([10,60],width= 78, height = 10, fill = True, color='darkblue',alpha=0.15)

    for rect in [rectangle1, rectangle2]:
        ax.add_patch(rect)

    return fig,ax

dico_color = {'AIGLE':'black','AIGLE 10':'black','AIGLE 15':'black','AIGLE 9':'black','COLOMBE':'mediumvioletred','PIE':'lightsalmon','POULE':'tan','TOUCHE':'cadetblue','PHENIX':'seagreen','GAP':'red'}

def kicking_plot(dataset,dico_player):

    dataset = dataset[dataset.Row.str.contains('17.JAP')].reset_index(drop=True)
    dataset = dataset[dataset.Row.str.contains("Racing 92")].reset_index(drop=True)

    dataset['Distance X'] = dataset['X jap fin'] - dataset['X']
    dataset['Distance Y'] = (dataset['Y jap fin'] - dataset['Y'])*(-1)

    dataset[['New X','New Y']] = ''

    for i in range(len(dataset)):

        dataset['New X'][i] = dataset.X[i] + 10 
        dataset['New Y'][i] = 70 - dataset.Y[i] 

    (fig,ax) = draw_pitch_horizontal() 
    plt.ylim(-2, 72)
    plt.xlim(-2, 120.4)
    plt.axis('off')

    print(dataset)

    for i in range(len(dataset)):

        if dataset['Type de jeu au pied'][i] in ['PENALTOUCHE',"COUP D'ENVOI",'PENALTOUCHE, PENALTOUCHE','RENVOI EN BUT','PENALTOUCHE, GAP']:
            pass

        else:
            if dataset['Type de jeu au pied'][i] in list(dico_color.keys()):
                plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
                color = dico_color[dataset['Type de jeu au pied'][i]])
            else:
                plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
                color = 'grey')
                
            joueurs = dataset['Joueurs'][i]
            #initiales = joueurs[joueurs.index(' ')+1] + '.' + joueurs[0]  
            
            #if initiales == 'G.L':
            #    initiales = "N.LG"

            plt.annotate(str(dico_player[joueurs]),(dataset['New X'][i]-2,dataset['New Y'][i]))
        
    plt.title('Kicking Game - ' + dataset['Timeline'][i] + '\n\n' + "Racing 92" + '\n',fontweight='semibold',fontsize=11)
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return img

def kicking_plot_adv(dataset):

    dataset = dataset[dataset.Row.str.contains('17.JAP')].reset_index(drop=True)
    dataset = dataset[dataset.Row.str.contains("Racing 92") == False].reset_index(drop=True)

    dataset['Distance X'] = dataset['X jap fin'] - dataset['X']
    dataset['Distance Y'] = (dataset['Y jap fin'] - dataset['Y'])*(-1)

    dataset[['New X','New Y']] = ''

    for i in range(len(dataset)):

        dataset['New X'][i] = dataset.X[i] + 10 
        dataset['New Y'][i] = 70 - dataset.Y[i] 

    (fig,ax) = draw_pitch_horizontal() 
    plt.ylim(-2, 72)
    plt.xlim(-2, 120.4)
    plt.axis('off')

    print(dataset)

    for i in range(len(dataset)):

        if dataset['Type de jeu au pied'][i] in ['PENALTOUCHE',"COUP D'ENVOI",'PENALTOUCHE, PENALTOUCHE','RENVOI EN BUT','PENALTOUCHE, GAP']:
            pass

        else:
            
            if dataset['Type de jeu au pied'][i] in list(dico_color.keys()):
                plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
                color = dico_color[dataset['Type de jeu au pied'][i]])
            else:
                plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
                color = 'grey')
        
    plt.title('Kicking Game - ' + dataset['Timeline'][i] + '\n\n' + "Adversaire" + '\n',fontweight='semibold',fontsize=11)
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return img

def df_from_request(joueur,liste_url):

    df_global = pd.DataFrame()
    
    if type(liste_url) == str:
        
        url = liste_url
        numbers = re.findall('\d+', url)[0]
        url_international = f'https://www.itsrugby.fr/joueur-internationale-{numbers}.html'
        
        liste_url = [liste_url,url_international]
        
    for url in liste_url:
        
        response = requests.get(url)
        data = response.content

        soup = BeautifulSoup(data, 'lxml')

        div_element = soup.find('div', class_='table-responsive-md')

        if div_element:
            tbody = div_element.find('tbody')
            if tbody:

                df = pd.DataFrame()

                for tr in tbody.find_all('tr'):

                    liste_td = []

                    for td in tr.find_all('td'):

                        if td.text != '' : 

                            text = td.text.replace('\n\t\t\xa0\xa0','')
                            liste_td.append(text)  

                    if len(liste_td) == 13:

                        df1 = pd.DataFrame(liste_td).T
                        df = pd.concat([df,df1])

                    elif len(liste_td) == 11:

                        liste_td = ['',''] + liste_td
                        df1 = pd.DataFrame(liste_td).T
                        df = pd.concat([df,df1])
            else:
                print("No tbody found in the specified div.")
        else:
            print("No div with class 'table-responsive-md' found.")
            
        if len(df) > 0:

            df.columns = ['Saison','Club','Compétition','Pts','J.','Tit.','E.','P.','Dp.','Tr.','CJ','CR','Min.']

            df = df.replace('',np.nan).reset_index(drop=True)

            df['Saison'], df['Club'] = df['Saison'].ffill(),  df['Club'].ffill()

            df['Joueur'] = joueur

            df = df[['Joueur'] + list(df.columns)[:-1]]

            if 'internationale' in url:
                df.insert(4,'Club/Nation','Nation')
            else:
                df.insert(4,'Club/Nation','Club')

            df = df[df['Compétition'].str.contains('7') == False]
            
            df_global = pd.concat([df_global,df]).reset_index(drop=True)
        
    print(f'Données de {joueur} téléchargés.')
    
    df_global = df_global.replace('-',0)
            
    return df_global


def df_exp_compo(url):

    response = requests.get(url)
    data = response.content

    soup = BeautifulSoup(data, 'lxml')

    elements = soup.find_all(class_='col-5 text-center itsfontsize')

    liste_equipe = []

    for element in elements:

        text = element.get_text(strip=True)  
        if text : liste_equipe.append(text)

    table = soup.find_all('div',class_='table-responsive-md')
    compos = table[0]

    compos = compos.find_all('tr')

    hometeam, hometeam_ref, awayteam, awayteam_ref = [], [], [], []

    for elt in compos:

        player = elt.find('div')

        if player:

            players = elt.find_all('a')

            for i in range(len(players)):

                player = players[i]
                player_name = player.text
                player_href = 'https://www.itsrugby.fr/'+ player['href']

                if i == 0 : 

                    hometeam.append(player_name)
                    hometeam_ref.append(player_href)

                if i == 1 :

                    awayteam.append(player_name)
                    awayteam_ref.append(player_href)

    df_compo = pd.DataFrame({liste_equipe[0]:hometeam,liste_equipe[0]+'_Href':hometeam_ref,liste_equipe[1]:awayteam,liste_equipe[1]+'_Href':awayteam_ref})

    df_experience_match = pd.DataFrame()

    for equipe in liste_equipe:

        df_equipe = df_compo[[equipe,equipe+'_Href']].reset_index(drop=True)

        for i in range(len(df_equipe)):

            player, href = df_equipe[equipe][i], df_equipe[equipe+'_Href'][i]

            df_player = df_from_request(player,href)

            df_player['Equipe'] = equipe

            df_experience_match = pd.concat([df_experience_match,df_player]).reset_index(drop=True)
        
    for col in ['Pts','J.','Tit.','E.','P.','Dp.','Tr.','CJ','CR','Min.']:
    
        df_experience_match[col] = df_experience_match[col].astype('int')
    
    matchs_pro = df_experience_match.groupby('Equipe').sum()[['J.','Tit.']].T
    matchs_pro.index = ['Matchs Pros','Titularisations Pros']

    sélections_internationales = df_experience_match[df_experience_match['Club/Nation'] == 'Nation'].groupby('Equipe').sum()[['J.']].T
    sélections_internationales.index = ['Sélections internationales']

    matchs_top14 =  df_experience_match[df_experience_match['Compétition'] == 'Top 14'].groupby('Equipe').sum()[['J.']].T
    matchs_top14.index = ['Matchs Top 14']

    matchs_club = df_experience_match[df_experience_match['Club'] == df_experience_match['Equipe']].groupby('Equipe').sum()[['J.']].T
    matchs_club.index = ['Matchs au sein du club']

    df_summary = pd.concat([matchs_pro,sélections_internationales,matchs_top14,matchs_club])[liste_equipe]

    return df_experience_match, df_summary   

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    writer.save()
    processed_data = output.getvalue()
    return processed_data








