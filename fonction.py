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

def draw_pitch_horizontal_v2():

    fig=plt.figure() 
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

    return fig,ax

dico_color = {'AIGLE':'black','AIGLE 10':'black','AIGLE 15':'black','AIGLE 9':'black','COLOMBE':'mediumvioletred','PIE':'lightsalmon','POULE':'tan','TOUCHE':'cadetblue','PHENIX':'seagreen','GAP':'red'}

def kicking_plot(dataset,dico_player):

    dataset = dataset[dataset.Row.str.contains('Jeu au Pied',na=False)].reset_index(drop=True)
    dataset = dataset[dataset.Row.str.contains("Racing",na=False)].reset_index(drop=True)

    dataset['X'], dataset['Y'] = dataset['X'].astype('float'), dataset['Y'].astype('float')
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

def kicking_plot_players(dataset,list_player,liste_jap):

    dataset = dataset[dataset['Type de jeu au pied'].isin(liste_jap)].reset_index(drop=True)
    dataset['X'], dataset['Y'] = dataset['X'].astype('float'), dataset['Y'].astype('float')

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

        if dataset['Type de jeu au pied'][i] in list(dico_color.keys()):
            plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
            color = dico_color[dataset['Type de jeu au pied'][i]])
        else:
            plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
            color = 'grey')
                        
    plt.title('Kicking Game - ' + str(list_player),fontweight='semibold',fontsize=11)
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return img

def kicking_plot_adv(dataset,opta):

    if opta == False:
        
        dataset = dataset[dataset.Row.str.contains('17.JAP',na=False)].reset_index(drop=True)
        dataset = dataset[dataset.Row.str.contains("Racing 92",na=False) == False].reset_index(drop=True)
        dataset['X'], dataset['Y'] = dataset['X'].astype('float'), dataset['Y'].astype('float')

        dataset['Distance X'] = dataset['X jap fin'] - dataset['X']
        dataset['Distance Y'] = (dataset['Y jap fin'] - dataset['Y'])*(-1)

    else:

        dataset['X'], dataset['Y'] = dataset['X'].astype('float'), dataset['Y'].astype('float')
        dataset['Distance X'] = dataset['X End'] - dataset['X']
        dataset['Distance Y'] = (dataset['Y End'] - dataset['Y'])*(-1)

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
        
    if opta == False:
        plt.title('Kicking Game - ' + dataset['Timeline'][i] + '\n\n' + "Adversaire" + '\n',fontweight='semibold',fontsize=11)
    else:

        plt.title('Kicking Game - ' + list(dataset['Row'].unique())[0] + '\n',fontweight='semibold',fontsize=11)

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

def rearrange_name(name):
    parts = name.split()  
    if len(parts) > 1:
        return parts[-1] + ' ' + ' '.join(parts[:-1])  
    return name 

def keep_capitals(name):
    return ''.join([char for char in name if char.isupper()])

def function_df_match(df):
        
    ## filters
    df_match = df[df.Row == '17.JAP Racing 92'].reset_index(drop=True)
    df_match = df_match[df_match['Type de jeu au pied'] != "COUP D'ENVOI"].reset_index(drop=True)

    df_match = df_match[['Timeline','Period','Row','GameTime','Joueurs','Resultat jap','Résultat','Type de jeu au pied']]


    ## résultat processing
    df_match['Résultat'] = np.select([df_match['Résultat'] == "Positif"],[1],[-1])
    df_match['Résultat_Color'] = np.select([df_match['Résultat'] == 1],["#008001"],default="darkred")

    ## joueurs processing
    df_match['Joueurs'] = df_match['Joueurs'].apply(rearrange_name)
    df_match['Capitals'] = df_match['Joueurs'].apply(keep_capitals)

    ## type de jeu au pied
    '''
    df_match['Type de jeu au pied'] = df_match['Type de jeu au pied'].str.replace('PENALTOUCHE','PT')
    df_match['Type de jeu au pied'] = df_match['Type de jeu au pied'].str.replace('TOUCHE','T')
    df_match['Type de jeu au pied'] = df_match['Type de jeu au pied'].str.replace('RENVOI EN BUT','RENV')
    '''

    return df_match

def function_points_flow(df):
        
    df_points = df[df.Row.str.contains('30.Points')].reset_index(drop=True)
    df_points = df_points[['Timeline','Row','GameTime','Points']]
    df_points = df_points.sort_values(by='GameTime').reset_index(drop=True)

    df_points['Team'] = np.select([df_points['Row'] == "30.Points Racing 92"],['Racing 92'],['Adversaire'])

    df_points['Points_Number'] = np.select([df_points['Points'] == "CPP +",df_points['Points'] == "Essai",df_points['Points'] == "Transfo +"],[3,5,2],default=0)

    df_points['Points_Racing'] = np.select([df_points['Team'] == 'Racing 92'],[df_points['Points_Number']],default=0)
    df_points['Cumul_Points_Racing'] = np.cumsum(df_points['Points_Racing'])

    df_points['Points_Adversaire'] = np.select([df_points['Team'] == 'Adversaire'],[df_points['Points_Number']],default=0)
    df_points['Cumul_Points_Adversaire'] = np.cumsum(df_points['Points_Adversaire'])

    df_points['Ecart_Score'] = df_points['Cumul_Points_Racing'] - df_points['Cumul_Points_Adversaire']

    df_points = df_points[['GameTime','Ecart_Score']]

    debut = pd.DataFrame({'GameTime':[0],'Ecart_Score':[0]})
    fin = pd.DataFrame({'GameTime':[80],'Ecart_Score':[df_points['Ecart_Score'].iloc[-1]]})

    df_points = pd.concat([debut,df_points]).reset_index(drop=True)
    df_points = pd.concat([df_points, fin]).reset_index(drop=True)

    df_points['Ecart_Score'] = df_points['Ecart_Score']/abs(df_points['Ecart_Score']).max()

    return df_points

def gametime_graph1(df):

    df['GameTime'] = df['GameTime'].astype('string')
    df['Minutes'], df['Secondes'] = df['GameTime'].str[3:5].fillna('0'), df['GameTime'].str[6:8].fillna('0')
    df['Minutes'] = pd.to_numeric(df['Minutes'], errors='coerce').fillna(0).astype(int)
    df['Secondes'] = pd.to_numeric(df['Secondes'], errors='coerce').fillna(0).astype(float) / 60
    df.loc[(df['Period'] == 2) | (df['Period'] == '2'), 'Minutes'] = df['Minutes'] + 40
    df['GameTime'] = df['Minutes'] + df['Secondes']

    df_match = function_df_match(df)

    df_points = function_points_flow(df)

    fig, ax = plt.subplots(figsize=(15,6))  

    ax.axhspan(0.8, 1.2, xmin=0, xmax=80, facecolor='#008001', alpha=0.3)
    ax.axhspan(-1.2, -0.8, xmin=0, xmax=80, facecolor='darkred', alpha=0.3)
    
    ax.scatter(df_match['GameTime'],df_match['Résultat'],s=100,color=df_match['Résultat_Color'])
    ax.plot(df_match['GameTime'],df_match['Résultat'],color='darkgrey',linewidth=0.3)
    
    for i in range(len(df_match)):
        ax.annotate(df_match['Capitals'][i],(df_match['GameTime'][i] - 0.5,df_match['Résultat'][i] + 0.1),fontsize=6)
        if df_match['Type de jeu au pied'][i] == 'PENALTOUCHE':
            ax.annotate('PT',(df_match['GameTime'][i] - 0.35,df_match['Résultat'][i] + 0.05),fontsize=5)
        elif df_match['Type de jeu au pied'][i] == 'PIE':
            ax.annotate(df_match['Type de jeu au pied'][i],(df_match['GameTime'][i] - 0.35,df_match['Résultat'][i] + 0.05),fontsize=5)
        elif df_match['Type de jeu au pied'][i] == 'POULE':
            ax.annotate(df_match['Type de jeu au pied'][i],(df_match['GameTime'][i] - 0.9,df_match['Résultat'][i] + 0.05),fontsize=5)
        elif df_match['Type de jeu au pied'][i] == 'TOUCHE':
            ax.annotate(df_match['Type de jeu au pied'][i],(df_match['GameTime'][i] - 0.9,df_match['Résultat'][i] + 0.05),fontsize=5)
        elif df_match['Type de jeu au pied'][i] == 'RENVOI EN BUT':
            ax.annotate("RENVOI",(df_match['GameTime'][i] - 0.9,df_match['Résultat'][i] + 0.05),fontsize=5)
        elif df_match['Type de jeu au pied'][i] == 'AIGLE':
            ax.annotate(df_match['Type de jeu au pied'][i],(df_match['GameTime'][i] - 0.7,df_match['Résultat'][i] + 0.05),fontsize=5)
        else:
            ax.annotate(df_match['Type de jeu au pied'][i],(df_match['GameTime'][i] - 0.5,df_match['Résultat'][i] + 0.05),fontsize=6)
    
    ax.axhline(0,linewidth=0.5,color='darkgrey')
    ax.step(df_points['GameTime'],df_points['Ecart_Score'],color='black',where='post')
    
    ax.set_xlim(-1,81)
    ax.set_ylim(-1.2,1.2)

    try:
        title = df_match['Timeline'][0]
        title = title[:title.index('(') - 1]
    except:
        title = ''
    
    ax.set_title('\n' + title + '\n\n',fontsize=8,fontweight='semibold')
    ax.set_yticks([])
    
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    buf = io.BytesIO()
    fig.savefig(buf)  # Save the figure to the buffer
    buf.seek(0)
    img = Image.open(buf)

    return img

def gametime_graph2(df):

    df['GameTime'] = df['GameTime'].astype('string')
    df['Minutes'], df['Secondes'] = df['GameTime'].str[3:5].fillna('0'), df['GameTime'].str[6:8].fillna('0')
    df['Minutes'] = pd.to_numeric(df['Minutes'], errors='coerce').fillna(0).astype(int)
    df['Secondes'] = pd.to_numeric(df['Secondes'], errors='coerce').fillna(0).astype(float) / 60
    df.loc[(df['Period'] == 2) | (df['Period'] == '2'), 'Minutes'] = df['Minutes'] + 40
    df['GameTime'] = df['Minutes'] + df['Secondes']

    df_match = function_df_match(df)

    df_points = function_points_flow(df)

    fig, ax = plt.subplots(figsize=(15,6))  # Create figure and axis
    
    ax.axhspan(0, 1.0, xmin=0, xmax=80, facecolor='#008001', alpha=0.15)
    ax.axhspan(0, -1.0, xmin=0, xmax=80, facecolor='darkred', alpha=0.15)
    
    ax.scatter(df_match['GameTime'],[0 for value in df_match['GameTime']],s=100,color=df_match['Résultat_Color'])
    
    for i in range(len(df_match)):
        ax.annotate(df_match['Capitals'][i],(df_match['GameTime'][i] - 0.5,0.08),fontsize=6)
    
    ax.axhline(0,linewidth=0.5,color='darkgrey')
    ax.step(df_points['GameTime'],df_points['Ecart_Score'],color='black',where='post')
    
    ax.set_xlim(-1,81)
    ax.set_ylim(-1.05,1.1)

    try:
        title = df_match['Timeline'][0]
        title = title[:title.index('(') - 1]
    except:
        title = ''
    
    ax.set_title('\n' + title,fontsize=8,fontweight='semibold')
    ax.set_yticks([])
    
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    buf = io.BytesIO()
    fig.savefig(buf)  # Save the figure to the buffer
    buf.seek(0)
    img = Image.open(buf)

    return img










