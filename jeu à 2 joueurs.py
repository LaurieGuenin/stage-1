# -*- coding: utf-8 -*-
"""
Created on Mon May  9 15:17:24 2022

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
        return np.argmin(np.array([prix1,prix2]))
    
def stratégie(historique,d,distances):  # stratégie de choix de prix 
    j=Types.index(d.typ)
    i=d.carac
    if historique[i][j]==[]:
        return 10
    elif historique[i][j][-1][2]:
        return historique[i][j][-1][1]+10 #remonte le prix
    else:
        return historique[i][j][-1][1]-2
    
def stratégie2(historique,d,distances,lastT,lastF):  # marche pas pour deux agents 
    #stratégie en forme de dichotomie
    j=Types.index(d.typ)
    if d.fin-d.deb<= distances[0][1]:
        i=0
    else:
        i=1
    if historique[i][j]==[] or (lastT[i][j]==-1 and lastF[i][j]==-1):
        return 200
    elif lastT[i][j]==-1:
        return 0
    elif lastF[i][j]==-1:
        return lastT[i][j]*2
    else:
        return (lastT[i][j]+lastF[i][j])/2
    
def stratégie3(historique,d,distances,lastT,lastF):  # marche pas pour deux agents 
    #stratégie en forme de dichotomie 
    j=Types.index(d.typ)
    if d.fin-d.deb<= distances[0][1]:
        i=0
    else:
        i=1
    if historique[i][j]==[] or (lastT[i][j]==-1 and lastF[i][j]==-1):
        return 200
    elif lastT[i][j]==-1:
        return 0
    elif lastF[i][j]==-1:
        return lastT[i][j]*2
    else:
        return (lastT[i][j]+lastF[i][j])/2

    
    
def jeu(tri,ens_dem1,ens_dem2,P1,P2,distances): 
    #déroulement du jeu 
    lastT2=[[-1 for j in range(len(Types))]for i in range(len(distances))]
    lastF2=[[-1 for j in range(len(Types))]for i in range(len(distances))]
    lastT1=[[-1 for j in range(len(Types))]for i in range(len(distances))]
    lastF1=[[-1 for j in range(len(Types))]for i in range(len(distances))]
    ens1=[]
    profit1=0
    prof1=[]
    ens2=[]
    profit2=0
    prof2=[]
    pr1=0
    pr2=0
    Pr1=[]
    Pr2=[]
    X=[]
    k=0
    prix1=0
    prix2=0
    historique1=[[[] for j in range(len(Types))]for i in range(len(distances))]
    historique2=[[[] for j in range(len(Types))]for i in range(len(distances))]
    for i in range(len(tri)):
        if tri[i]!=[-1]:
            for j in range(len(tri[i])):
                k+=1
                if k%50==0:
                    X.append(k)
                    print(k,profit1,profit2)
                    prof1.append(profit1)
                    prof2.append(profit2)
                    Pr1.append(pr1/50)
                    Pr2.append(pr2/50)
                    prix1=0
                    prix2=0
                if tri[i][j]>=n:
                    d=ens_dem2[tri[i][j]-n]
                else:
                    d=ens_dem1[tri[i][j]]
                prix2=stratégie2(historique2,d,distances,lastT2,lastF2)
                prix1=stratégie2(historique1,d,distances,lastT1,lastF1)
                #prix1=Prix1(d)
                c=choix_agent(prix1,prix2)
                if c==0:
                    ens1.append(d)
                    profit1+=prix1
                    b=False
                    pr1+=prix1
                else:
                    ens2.append(d)
                    profit2+=prix2
                    b=True
                    pr2+=prix2
                if d.carac==0:
                    historique2[0][Types.index(d.typ)].append([d,prix2,b])
                    historique1[0][Types.index(d.typ)].append([d,prix1,not b])
                    if b:
                        lastT2[0][Types.index(d.typ)]=prix2
                        lastF1[0][Types.index(d.typ)]=prix1
                    else:
                        lastF2[0][Types.index(d.typ)]=prix2
                        lastT1[0][Types.index(d.typ)]=prix1
                else:
                    historique2[1][Types.index(d.typ)].append([d,prix2,b])
                    historique1[1][Types.index(d.typ)].append([d,prix1,not b])
                    if b:
                        lastT2[1][Types.index(d.typ)]=prix2
                        lastF1[1][Types.index(d.typ)]=prix1
                    else:
                        lastF2[1][Types.index(d.typ)]=prix2
                        lastT1[1][Types.index(d.typ)]=prix1
    diff=[prof2[i]-prof1[i] for i in range(len(prof1))]
    diff2=[0]+[10*(diff[i]-diff[i-1]) for i in range(1,len(prof1))]
    #plt.plot(X,diff,color='red')
    #plt.plot(X,diff2,color='purple')
    plt.plot(X,prof1,color='blue')
    plt.plot(X,prof2,color='orange')
    plt.show()
    plt.plot(X,Pr1,color='red')
    plt.plot(X,Pr2,color='green')
    plt.show()
    return profit1,profit2 



start=time.time()
n=10000
nbr_etapes=350
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
print(jeu(tri,ens_dem1,ens_dem2,P1,P2,distances))
end=time.time()
print(end-start)



















