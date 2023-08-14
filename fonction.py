
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

    dataset = dataset[dataset.Row.str.contains('17.')].reset_index(drop=True)
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

            plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
            color = dico_color[dataset['Type de jeu au pied'][i]])

            joueurs = dataset['Joueurs'][i]
            initiales = joueurs[joueurs.index(' ')+1] + '.' + joueurs[0]  
            
            if initiales == 'G.L':
                initiales = "N.LG"

            plt.annotate(str(dico_player[joueurs]),(dataset['New X'][i]-2,dataset['New Y'][i]))
        
    plt.title('Kicking Game - ' + dataset['Timeline'][i] + '\n\n' + "Racing 92" + '\n',fontweight='semibold',fontsize=11)
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return img

def kicking_plot_adv(dataset):

    dataset = dataset[dataset.Row.str.contains('17.')].reset_index(drop=True)
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

            plt.arrow(dataset['New X'][i],dataset['New Y'][i],dataset['Distance X'][i],dataset['Distance Y'][i],head_width = 1,width = 0.05,
            color = dico_color[dataset['Type de jeu au pied'][i]])
        
    plt.title('Kicking Game - ' + dataset['Timeline'][i] + '\n\n' + "Adversaire" + '\n',fontweight='semibold',fontsize=11)
    
    buf = io.BytesIO()
    fig.savefig(buf)
    buf.seek(0)
    img = Image.open(buf)

    return img

