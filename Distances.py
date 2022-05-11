# -*- coding: utf-8 -*-
"""
Created on Tue May  3 08:35:53 2022

@author: laurie
"""
import numpy as np

def distance_initiaux(int1,int2):
    # calcule la distance entre les points initiaux des deux intervalles
    d=abs(int1[0]-int2[0])/(max(int1[1],int2[1])-min(int1[0],int2[0]))
    return d

def distance_finaux(int1,int2):
    # calcule la distance entre les points finaux des deux intervalles
    d=(abs(int1[1]-int2[1]))/(max(int1[1],int2[1])-min(int1[0],int2[0]))
    return d

def distance_longueurs(int1,int2):
    # calcule la distance en fonction des longueurs des deux intervalles
    d=1-((min(int1[1]-int1[0],int2[1]-int2[0]))/(max(int1[1]-int1[0],int2[1]-int2[0])))
    return d

def distance_chevauchement(int1,int2):
    # calcule la distance en fonction du chevauchement entre les deux intervalles
    mini=min(int1[1],int2[1])
    maxi=max(int1[0],int2[0])
    if mini<maxi:
        return 1.
    else:
        d=1-((mini-maxi)/(min(int1[1]-int1[0],int2[1]-int2[0])))
        return d

def distance_ecart(int1,int2):
    # calcule la distance en fonction de l'écart entre les deux intervalles
    mini=min(int1[1],int2[1])
    maxi=max(int1[0],int2[0])
    if mini<maxi:
        d=(min(int1[1]-int2[0],int2[1]-int1[0]))/(max(int1[1],int2[1])-min(int1[0],int2[0]))
        return d
    else:
        return 0


def distance_temporelle(ints1,ints2,nb_vehicules,nbr_etapes):
    # calcule la distance entre deux ensembles d' intervalles en fonction de la différence qu'il y a à chaque période
    d=0
    e1=0
    e2=0
    for i in range(nbr_etapes):
        for j in range(len(ints1)):
            mini,maxi=ints1[j]
            if mini<=i and i<=maxi:
                e1+=1
        for j in range(len(ints2)):
            mini,maxi=ints2[j]
            if mini<=i and i<=maxi:
                e2+=1
        d+=abs(e1-e2)/max(e1,e2)
        e1=0
        e2=0
    return d/nbr_etapes

def taux_de_remplissage(ints1,ints2,nb_vehicules,nbr_etapes):
    # calcule la différence de taux de remplissage
    s1=0
    s2=0
    for i in range(nbr_etapes):
        for j in range(len(ints1)):
            mini,maxi=ints1[j]
            if mini<=i and i<=maxi:
                s1+=1
        for j in range(len(ints2)):
            mini,maxi=ints2[j]
            if mini<=i and i<=maxi:
                s2+=1
    d=abs(s1-s2)/(nb_vehicules*nbr_etapes)
    return d

def dist_ens(ints1,ints2,nb_vehicules,nbr_etapes,T1=[1/7,1/7,1/7,1/7,1/7], D1=[distance_initiaux,distance_finaux,distance_longueurs,distance_chevauchement,distance_ecart],D2=[distance_temporelle,taux_de_remplissage],T2=[1/7,1/7]):
    #calcule la distance entre deux ensembles d'intervalles avec toutes les distances précédentes sans décalage
    mat=np.zeros([len(ints1),len(ints2)])
    for i in range(len(ints1)):
        for j in range(len(ints2)):
            d=0
            for k in range(len(T1)):
                d+=T1[k]*(D1[k](ints1[i],ints2[j]))
            mat[i][j]=d
    liste=algo_hongrois(mat)
    D=0
    for i in range(len(liste)):
        D+=mat[liste[i][0]][liste[i][1]]
    for k in range(len(T2)):
        D+=T2[k]*(D2[k](ints1,ints2,nb_vehicules,nbr_etapes))
    return D


def algo_hongrois(mat):
    # premet de calculer le couplage maximum de poids minimum
    matrice=mat.copy()
    for i in range(len(matrice)):
        min=100   #taille
        for j in range(len(matrice[0])):
            if matrice[i][j]<min:
                min=matrice[i][j]
        for j in range(len(matrice[0])):
            matrice[i][j]-=min
    for j in range(len(matrice[0])):
        min=100   #TAILLE
        for i in range(len(matrice)):
            if matrice[i][j]<min:
                min=matrice[i][j]
        for i in range(len(matrice)):
            matrice[i][j]-=min
    L=[]
    mini=100                 #taille
    ligne_mini=-1
    for i in range(len(matrice)):
        l=0
        emp=[]
        for j in range(len(matrice[0])):
            if matrice[i][j]==0:
                l+=1
                emp.append(j)
        L.append([l,emp])
        if l<mini and l!=0:
            mini=l
            ligne_mini=i
    k=0
    while k<len(matrice)*len(matrice[0]):
        print(k)
        k+=1
        choisi=[]
        barré=[]
        while ligne_mini!=-1:
            emp=L[ligne_mini][1]
            c=L[ligne_mini][1][0]
            choisi.append([ligne_mini,c])
            if len(emp)>1:
                barré.extend([[ligne_mini,emp[i]] for i in range(1,len(emp))])
            L[ligne_mini]=[0,[]]
            mini=100                  #TAILLE
            ligne_mini=-1
            for i in range(len(L)):
                if L[i][0]!=0:
                    n=L[i][1].count(c)
                    if n==1:
                        L[i][1].remove(c)
                        L[i][0]-=1
                        barré.append([i,c])
                if L[i][0]<mini and L[i][0]!=0:
                    mini=L[i][0]
                    ligne_mini=i
        if len(choisi) == len(matrice):
            return choisi
        else:

            colonne_barrée=[0 for i in range(len(matrice[0]))]
            ligne_barrée=[1 for i in range(len(matrice))]
            for [a,b] in choisi:
                ligne_barrée[a]=0
            change=True
            while change:
                change=False
                for [a,b] in barré:
                    if ligne_barrée[a]==1 and colonne_barrée[b]==0:
                        colonne_barrée[b]=1
                        change=True
                for [a,b] in choisi:
                    if colonne_barrée[b]==1 and ligne_barrée[a]==0:
                        ligne_barrée[a]=1
                        change=True
            mini=-1.
            for i in range(len(matrice)):
                for j in range(len(matrice[0])):
                    if ligne_barrée[i]==1 and colonne_barrée[j]==0:
                        if mini==-1.:
                           mini=matrice[i][j]
                        elif matrice[i][j]<mini:
                            mini=matrice[i][j]
            for i in range(len(matrice)):
                for j in range(len(matrice[0])):
                    if ligne_barrée[i]==1 and colonne_barrée[j]==0:
                        matrice[i][j]=matrice[i][j] - mini
                    elif ligne_barrée[i]==0 and colonne_barrée[j]==1:
                        matrice[i][j]=matrice[i][j] + mini
            L=[]
            mini=100                 #taille
            ligne_mini=-1
            for i in range(len(matrice)):
                l=0
                emp=[]
                for j in range(len(matrice[0])):
                    if matrice[i][j]==0:
                        l+=1
                        emp.append(j)
                L.append([l,emp])
                if l<mini and l!=0:
                    mini=l
                    ligne_mini=i
    return "probleme"