# -*- coding: utf-8 -*-
"""
Created on Wed May 11 10:00:23 2022

@author: laurie
"""

import random
import Demandes as D
import numpy as np
import Agents as A
import prédiction as p
import time
import matplotlib.pyplot as plt

Types=["Economy","Mid","Full"] # ordonné de tel manière que si l'on prend deux types celui le plus à droite ne peut être plus petit que celui de gauche
ordre_types=[[0,1,1],[0,0,1],[0,0,0]]

def créer_demande(nbr_etapes,distance,typ,carac):
    # crée une demande aléatoirement de manière à avoir t_d,deb et fin dans nbr_etapes
    longueur=random.choice(distance[0:1])
    deb=random.randint(0,nbr_etapes-longueur-1)
    fin=deb+longueur
    t_d=deb-random.randint(0,distance[2])
    return D.Demande(t_d, deb, fin, typ,carac=carac)

def créer_prédiction(nbr_etapes,n,matP,distances,types=Types):  #pour chaque types distances contient logueur min, longueur max et durée max entre t_d et deb
    ens_dem=[]
    cpts=np.zeros((len(Types),nbr_etapes))
    w=[]
    for i in range(len(matP)):
        for j in range(len(matP[i])):
            prob=matP[i][j]
            nbr=int(prob*n)
            for k in range(nbr):
                d=créer_demande(nbr_etapes,distances[i],types[j],i)
                ens_dem.append(d)
                w.append(d.fin-d.deb)
                for l in range(d.deb,d.fin+1):
                    cpts[Types.index(d.typ)][l]+=1
    maxi=[0 for i in range(len(Types))]
    for i in range(len(Types)):
        for a in range(len(cpts[0])):
            if cpts[i][a]>maxi[i]:
                maxi[i]=cpts[i][a]
    return(ens_dem,maxi,w)

def tri(ens1,ens2,distances,nbr_etapes,n):  #range les demandes par ordre d'arrivée
    max_dis=max([distances[i][2] for i in range(len(distances))])
    tri=[[-1] for i in range(max_dis+nbr_etapes)]
    for i in range(n):
        d=ens1[i]
        t_d=d.t_d
        if tri[t_d+max_dis]==[-1]:
            tri[t_d+max_dis]=[i]
        else:
            tri[t_d+max_dis].append(i)
    for i in range(n):
        d=ens2[i]
        t_d=d.t_d
        if tri[t_d+max_dis]==[-1]:
            tri[t_d+max_dis]=[n+i]
        else:
            tri[t_d+max_dis].append(n+i)
    return tri 



