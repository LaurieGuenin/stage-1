# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:09:58 2022

@author: laurie
"""

import random
import Demandes as D
import numpy as np
import Agents as A
import prédiction as p
import time
import matplotlib.pyplot as plt
import création_prédiction as Cp



Types=["Economy","Mid","Full"] # ordonné de tel manière que si l'on prend deux types celui le plus à droite ne peut être plus petit que celui de gauche
ordre_types=[[0,1,1],[0,0,1],[0,0,0]]


def Prix1(d):  # prix fixe pour le joueur1
    if d.carac==0:
        prix=10*(d.fin-d.deb)
    else:
        prix=7*(d.fin-d.deb)
    return prix



def choix_agent(prix1,prix2):   #choisi l'agent qui recoit la demande
    if prix1==prix2:
        return random.choices([0,1])[0]
    else:
        return np.argmin([prix1,prix2])
    
def stratégie(historique,d,distances):  # stratégie de choix de prix 
    j=Types.index(d.typ)
    i=d.carac
    if historique[i][j]==[]:
        return 6
    elif historique[i][j][-1][2]:
        return historique[i][j][-1][1]+10 #remonte le prix
    else:
        return historique[i][j][-1][1]-2
    
def est_possible(d,Nb_V):
    j=Types.index(d.typ)
    for k in range(d.deb,d.fin+1):
        if Nb_V[j][k]<=0:
            return False
    return True

def mis_à_jour(d,Nb_V):
    j=Types.index(d.typ)
    for k in range(d.deb,d.fin+1):
        Nb_V[j][k]-=1
    return Nb_V

    
    
def jeu(tri,ens_dem1,ens_dem2,Nb_V1,Nb_V2,P1,P2,distances,pas=1): 
    #déroulement du jeu 
    ens2=[]
    profit2=0
    prof2=[]
    ens1=[]
    profit1=0
    prof1=[]
    pr1=0
    pr2=0
    Pr2=[]
    Pr1=[]
    X=[]
    k=0
    prix2=0
    historique2=[[[] for j in range(len(Types))]for i in range(len(distances))]
    for i in range(len(tri)):
        if tri[i]!=[-1]:
            for j in range(len(tri[i])):
                k+=1
                if k%pas==0:
                    X.append(k)
                    print(k,profit1,profit2)
                    prof1.append(profit1)
                    prof2.append(profit2)
                    Pr1.append(pr1/pas)
                    Pr2.append(pr2/pas)
                    pr1=0
                    pr2=0
                if tri[i][j]>=n:
                    d=ens_dem2[tri[i][j]-n]
                else:
                    d=ens_dem1[tri[i][j]]
                if est_possible(d, Nb_V2):
                    prix2=stratégie(historique2,d,distances)
                else:
                    prix2=100000                               #à fixer
                if est_possible(d, Nb_V1):
                    prix1=Prix1(d)
                else:
                    prix1=100000
                c=choix_agent(prix1,prix2)
                if c==0:
                    ens1.append(d)
                    profit1+=prix1
                    b=False
                    pr1+=prix1
                    Nb_V1=mis_à_jour(d, Nb_V1)
                else:
                    ens2.append(d)
                    profit2+=prix2
                    b=True
                    pr2+=prix2
                    Nb_V2=mis_à_jour(d, Nb_V2)
                if d.carac==0:
                    historique2[0][Types.index(d.typ)].append([d,prix2,b])
                else:
                    historique2[1][Types.index(d.typ)].append([d,prix2,b])
    plt.plot(X,prof1,color='blue')
    plt.plot(X,prof2,color='orange')
    plt.xlabel("Nombre de demandes")
    plt.ylabel("Profit")
    plt.show()
    plt.plot(X,Pr2,color='red')
    plt.plot(X,Pr1,color='green')
    plt.xlabel("Nombre de demandes")
    plt.ylabel("gain moyen sur 50 demandes")
    plt.show()
    return profit1,profit2 



start=time.time()
n=1000
nbr_etapes=35
distances=[[1,6,30],[13,30,150]]
ens_dem1,maxi1,w1=Cp.créer_prédiction(nbr_etapes,n,[[0.3,0.1,0.1],[0.2,0.2,0.1]],distances)
Nb_V1=[[maxi1[j] for i in range(nbr_etapes)]for j in range(len(Types))]
agent1=A.Agent(Nb_V1, Types, ordre_types)
P1=p.Prediction(ens_dem1, agent1, nbr_etapes,w=w1)
ens_dem2,maxi2,w2=Cp.créer_prédiction(nbr_etapes,n,[[0.3,0.1,0.1],[0.2,0.2,0.1]],distances)
Nb_V2=[[maxi2[j] for i in range(nbr_etapes)]for j in range(len(Types))]
agent2=A.Agent(Nb_V2, Types, ordre_types)
P2=p.Prediction(ens_dem2, agent2, nbr_etapes,w=w2)
tri=Cp.tri(ens_dem1, ens_dem2, distances, nbr_etapes, n)
end=time.time()
print(end-start)
start=end
print(jeu(tri,ens_dem1,ens_dem2,Nb_V1,Nb_V2,P1,P2,distances))
end=time.time()
print(end-start)
