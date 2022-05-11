# -*- coding: utf-8 -*-
"""
Created on Tue May  3 13:58:29 2022

@author: laurie
"""
import random
import matplotlib.pyplot as plt
import numpy as np
import Agents as A
import Distances as Di
import Demandes as D
import copy
import prédiction as p
import time
import ordre as O

Types=["Economy","Compact","Mid","Stan","Full"] # ordonné de tel manière que si l'on prend deux types celui le plus à droite ne peut être plus petit que celui de gauche
ordre_types=[[0,1,1,1,1],[0,0,0,1,1],[0,0,0,1,1],[0,0,0,0,1],[0,0,0,0,0]]

def créer_demande(nbr_etapes,types=Types):
    # crée une demande aléatoirement de manière à avoir t_d,deb et fin dans nbr_etapes
    t_d=random.randint(0,nbr_etapes-2)
    deb=random.randint(t_d,nbr_etapes-2)
    fin=random.randint(deb+1,nbr_etapes-1)
    typ=random.choice(types)
    return D.Demande(t_d, deb, fin, typ)

def créer_agent(nbr_etapes,nbmax_v,types=Types,ordre_types=ordre_types):
    #crée un agent avec un nombre aléatoire de véhicule plus petit que nbmax_v et un sous-ensemble de types
    t=[]
    for i in range(len(types)):
        if random.random()<0.9:
            t.append(types[i])
    Nb_V=np.zeros((len(t),nbr_etapes))
    for i in range(len(Nb_V)):
        for j in range(len(Nb_V[0])):
            Nb_V[i][j]=random.randint(int(nbmax_v/2),nbmax_v)
    mat=np.zeros((len(t),len(t)))
    for i in range(len(t)):
        indi=types.index(t[i])
        for j in range(i,len(t)):
            indj=types.index(t[j])
            mat[i][j]=ordre_types[indi][indj]
    return A.Agent(Nb_V, t,mat)

def créer_prédiction(nbr_etapes,nbmax_v,types=Types):
    #crée une prédiction aléatoire qui respecte le nombre de véhicule de l'agent que l'on crée dans la fonction
    agent=créer_agent(nbr_etapes, nbmax_v)
    ens_dem=[]
    w=[]
    t=agent.types
    Nb_V=agent.Nb_V
    mat=np.zeros((len(Nb_V),len(Nb_V[0])))
    mat_bis=copy.copy(mat)
    b=True
    k=0
    c=True
    while b or k<2*nbr_etapes:
        d=créer_demande(nbr_etapes,types=t)
        int_d=d.intervalle
        typ=d.typ
        for i in range(int_d[0],int_d[1]+1):
            if mat[t.index(typ),i]==Nb_V[t.index(typ),i]:
                b=False
                c=False
            mat[t.index(typ),i]+=1
        if c:
            ens_dem.append(d)
            w.append(int_d[1]-int_d[0])
            mat_bis=copy.copy(mat)
        else:
            mat=copy.copy(mat_bis)
        if not b:
            k+=1
        c=True
    return p.Prediction(ens_dem, agent, nbr_etapes, w)
        
def créer_prédiction_d(nbr_etapes,nbmax_v,types=Types):
    # crée un ensemble d'une demande, d'une prédiction et d'un agent
    prediction=créer_prédiction(nbr_etapes, nbmax_v)  
    t=prediction.types
    demande=créer_demande(nbr_etapes,t)
    print(demande.intervalle,demande.typ)
    return p.Prediction_d(prediction, demande)

#def choix_prix(impact):

#def choix_demande(demande,Prix):
    
def déroulement(nbr_arrivées,nbr_etapes,list_prediction,Types=Types):
    # Itère le processus de choix de prix dès qu'une demande arrive et ensuite le choix d'un agent par la demande et pour finir la mise à jour de l'agent et de la prédiction
    Prix=[]
    for i in range(nbr_arrivées):
        demande=créer_demande(nbr_etapes,Types)
        for j in range(len(list_prediction)):
            agent=list_prediction[j].agent
            b=True
            for i in range(demande.intervalle[0],demande.intervalle[1]+1):
                if agent.Nb_V[Types.index(demande.typ)][i]==0:
                    b=False
            if b:
                pred_d=D.Prediction_d(list_prediction[j], demande)
                [typ2,impact,X,ordre_H]=pred_d.impact()
                prix=choix_prix(impact)   #existe pas encore
                Prix.append(prix)
            else:
                Prix.append(2*nbr_etapes)
        num_agent=choix_demade(demande,Prix) #existe pas encore
        agent=list_prediction[num_agent].agent    # ca dépend si c'est une copie 
        agent.demandes_acceptées.append(demande)
        for i in range(demande.intervalle[0],demande.intervalle[1]+1):
            agent.Nb_V[Types.index(demande.typ)][i]-=1
        agent.profit+=Prix[num_agent]     #-cout_i ?
        ens_dem=list_prediction[num_agent].ens_dem
        w=list_prediction[num_agent].w
        for i in range(len(X)):
            if X[i]==1:
                ens_dem.pop(ordre_H[i])
                w.pop(ordre_H[i])
        pred=p.Prediction(ens_dem, agent, nbr_etapes, w)
        list_prediction[num_agent]=pred
    return(list_prediction)
        
        
        
start = time.time()        
P=créer_prédiction_d(100, 10) 
# end = time.time()
# print(format(end-start))
# start=end
# typ=P.typ_d
# ens_d=P.ens_d(typ)
# clic=P.clique_d(typ)
# pres=P.pres_X(clic, typ)
# print(ens_d)
# print(P.intervalles)
# print(P.mat_d(ens_d,typ))
# print(P.prediction.affichage())
# print(P.ens_X(pres,ens_d,typ))   
# ens_X=P.ens_X(pres,ens_d,typ)
# mat_d=P.mat_d(ens_d, typ)
# mat_X=P.mat_X(ens_d,ens_X,mat_d, typ)
# print(mat_X)
# start=end
# print(P.trans_ordre(O.ordre(mat_X),ens_X))
# end = time.time()
# print(format(end-start))
# start=end
# ordre=O.ordre(mat_d)
# trans=P.trans_ordre(ordre,ens_d)
# print(trans)
# ordre_X=P.ordre_X(trans,pres,ens_d,typ)
# print(ordre_X)   
# end = time.time()
# print(format(end-start))
# start=end
print(P.impact_min())
end = time.time()
print(format(end-start))
        
        
        
        
        
        
        
        
        
        