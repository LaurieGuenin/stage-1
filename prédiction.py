# -*- coding: utf-8 -*-
"""
Created on Thu May  5 15:20:05 2022

@author: laurie

"""

import random
import matplotlib.pyplot as plt
import numpy as np
import Agents
import Distances
import copy
import ordre as O


class Prediction:
    def __init__(self,ens_dem,agent,nbr_etapes,w=None):
        self.ens_dem=ens_dem  #ensemble de demandes sous forme de liste de demandes
        self.agent=agent  #agent dont l'on regarde la prédiction
        self.nbr_etapes=nbr_etapes  #nombre d'étapes que l'on regarde
        self.Nb_V=agent.Nb_V  #nombre de véhicules par types par période sous forme de matrice Nb_V[typ][periode]
        self.types=agent.types #liste des types de véhicules
        self.n=len(ens_dem) #nombre de demandes
        self.w=w #prix de chaque demandes
        
        self.intervalles=[] #ensembles des intervalles rangés par types avec leur numéro de demande
        for i in range(len(self.types)):
            self.intervalles.append([self.types[i]])
        for i in range(len(ens_dem)):
            typ=ens_dem[i].typ
            self.intervalles[self.types.index(typ)].append([i,ens_dem[i].intervalle])
            
        self.matrice=self.matrice() # matrice d'adjacence
    
    
        
        
    def affichage(self):
        # Affiche l'ensemble des intervalles sur un graphique en fonction de temps
        for jtyp in range(len(self.types)):
            for i in range (1,len(self.intervalles[jtyp])):
                k=self.intervalles[jtyp][i][0]
                plt.plot(self.intervalles[jtyp][i][1],[k,k])
                k+=1
        plt.show()


    def clique(self):
        # trouve les cliques qui sont de cardinal plus grand que le nombre de véhicules
        ens=[]
        clic=[]
        ens_bis=[-1]
        for jtyp in range(len(self.types)):
            for i in range(self.nbr_etapes):
                for j in range(1,len(self.intervalles[jtyp])):
                    mini,maxi=self.intervalles[jtyp][j][1]
                    if mini<=i and i<=maxi:
                        ens.append(self.intervalles[jtyp][j][0])
                if len(ens)>=self.Nb_V[jtyp][i] and ens_bis!=ens:
                    clic.append([i,ens])
                elif len(ens)>=self.Nb_V[jtyp][i] and ens_bis==ens:
                    clic[-1].insert(-2,i)
                ens_bis=ens
                if ens_bis==[]:
                    ens_bis.append(-1)
                ens=[]
        return clic

    def matrice(self):
        # Créer la matrice d'adjacence du graphe d'intervalles avec 2 si le type est identique et 1 sinon
        mat=np.zeros((self.n,self.n))
        pose=0
        for ityp in range(len(self.types)):
            for i in range(1,len(self.intervalles[ityp])):
                minii,maxii=self.intervalles[ityp][i][1]
                for j in range(i,len(self.intervalles[ityp])):
                    minij,maxij=self.intervalles[ityp][j][1]
                    if (minii<=minij and minij<=maxii) or (minii<=maxij and maxij<=maxii) or  (minij<=minii and minii<=maxij) or (minij<=maxii and maxii<=maxij) :
                        mat[self.intervalles[ityp][i][0]][self.intervalles[ityp][j][0]]=1
                        mat[self.intervalles[ityp][j][0]][self.intervalles[ityp][i][0]]=1
            pose+=len(self.intervalles[ityp])-1
        return mat

    def liste(self):        #Attention passage par la matrice peut-être pas optimale
    # créer la liste d'adjacence    
        liste=[]
        mat=self.matrice()
        for i in range(len(mat)):
            l=[]
            for j in range(len(mat[0])):
                if mat[i][j]==1:
                    l.append(j)
            liste.append(l)
        return liste
    

class Prediction_d:
    def __init__(self,prediction,demande):
        self.prediction=prediction  #prédiction
        self.ens_dem=self.prediction.ens_dem  #ensemble de demandes prédites sous forme de liste de demandes
        self.agent=self.prediction.agent  #agent dont l'on regarde la prédiction
        self.nbr_etapes=self.prediction.nbr_etapes  #nombre d'étapes que l'on regarde
        self.Nb_V=self.prediction.agent.Nb_V  #nombre de véhicules par types par période sous forme de matrice Nb_V[typ][periode] pour l'agent
        self.types=self.prediction.agent.types #liste des types de véhicules pour l'agent
        self.n=len(self.ens_dem) #nombre de demandes prédites
        self.intervalles=self.prediction.intervalles
        self.matrice=self.prediction.matrice #matrice d'adjacence de la prédiction
        self.w=self.prediction.w #prix de chaque demandes
        self.ordre=self.prediction.agent.ordre_types # ordre partiel sur les types de véhicules
        
        self.d=demande  #demande
        self.typ_d=self.d.typ #type de la demande
        self.intervalle_d=self.d.intervalle #intervalle de la demande
        
    def ens_d(self,typ):
        # ensemble des intervalles qui intersectent la demande et du même type. Ils sont renvoyés dans l'ordre dans lequel ils apparaissent dans intervalles. La fonction prend en argument le typ de la demande
        ens_d=[]
        for i in range(1,len(self.intervalles[self.types.index(typ)])):
            minii,maxii=self.intervalles[self.types.index(typ)][i][1]
            if (minii<=self.intervalle_d[0] and self.intervalle_d[0] <=maxii) or (minii<=self.intervalle_d[1]  and self.intervalle_d[1] <=maxii) or  (self.intervalle_d[0] <=minii and minii<=self.intervalle_d[1] ) or (self.intervalle_d[0] <=maxii and maxii<=self.intervalle_d[1] ) :
                ens_d.append(self.intervalles[self.types.index(typ)][i][0])
        return ens_d

    def mat_d(self,ens,typ):
        # matrice d'adjacence entre les intervalles de ens_d
        mat=np.zeros((len(ens),len(ens)))
        for i in range(len(ens)):
            for j in range(i,len(ens)):
                k=self.matrice[ens[i]][ens[j]]
                if k==1:
                    mat[i][j]=1
                    mat[j][i]=1
        return mat

    def liste_d(self,mat,ens_d,typ):
        # liste d'adjacence entre les intervalles de ens_d
        liste=[]
        for i in range(len(mat)):
            l=[]
            for j in range(len(mat)):
                if mat[i][j]==1:
                    l.append(ens_d[j])
            liste.append([ens_d[i],l])
        return liste
    
    def clique_d(self,typ):
        # trouve les cliques qui sont de cardinal plus grand que le nombre de véhicules qui pose problème avec d
        ens=[]
        clic=[]
        for i in range(self.intervalle_d[0],self.intervalle_d[1]+1):
            for j in range(1,len(self.intervalles[self.types.index(typ)])):
                mini,maxi=self.intervalles[self.types.index(typ)][j][1]
                if mini<=i and i<=maxi:
                    ens.append(self.intervalles[self.types.index(typ)][j][0])
            if clic==[]:
                if len(ens)>=self.Nb_V[self.types.index(typ)][i]:
                    clic.append([i,ens])
            else:
                Ens=clic[-1][-1]
                if len(ens)>=self.Nb_V[self.types.index(typ)][i] and Ens!=ens:
                    clic.append([i,ens])
                elif len(ens)>=self.Nb_V[self.types.index(typ)][i] and Ens==ens:
                    clic[-1].insert(-2,i)                                         
            ens=[]
        return clic


    def pres_X(self,clic,typ):
        # liste de présence des sommets de ens_d dans X, c'est une liste de 0 et 1, 1 quand le sommet est présent 0 quand il est absent
        l=[]
        for i in range(len(clic)):
            if len(clic[i])>0:                               #utile?
                for j in range(len(clic[i][-1])):
                    l.append(clic[i][-1][j])
        pres=np.zeros(len(self.ens_d(typ)))
        for i in l:
            pres[self.ens_d(typ).index(i)]=1
        return pres


    def ens_X(self,pres,ens_d,typ):
        # ensemble des sommets présents dans X
        liste=[]
        for i in range(len(ens_d)):
            if pres[i]==1:
                liste.append(ens_d[i])
        return liste
        

    def mat_X(self,ens_d,ens_X,matrice,typ):
        # matrice d'adjacence entre les sommets de X avec matrice la matrice d'adjacence dans ens_d
        mat=np.zeros((len(ens_X),len(ens_X)))
        for i in range(len(ens_X)):
            for j in range(len(ens_X)):
                if matrice[ens_d.index(ens_X[i])][ens_d.index(ens_X[j])]==1:  
                    mat[i][j]=1
        return mat

    def liste_X(self,mat,ens_X,typ):
        # liste d'adjacence entre les sommets de X
        liste=[]
        for i in range(len(mat)):
            l=[]
            for j in range(len(mat)):
                if mat[i][j]==1:
                    l.append(ens_X[j])
            liste.append([ens_X[i],l])
        return liste

    def trans_ordre(self,ordre,ens):
        L=[]
        for i in range(len(ordre)):
            for j in range(len(ordre[i])):
                L.append(ens[ordre[i][j]])
        L.reverse()
        return L

    def ordre_X(self,ordre,pres,ens_d,typ):          # en fonction d'une fonction pas faite   
    # pas utile 
        # donne l'ordre d'élimination robuste de X en fonction de celui de G
        ordre_X=ordre
        for i in range(len(ordre_X)-1,-1,-1):
            if pres[ens_d.index(ordre_X[i])]==0:
                ordre_X.pop(i)
        return(ordre_X)
    
    def adj_clique(self,clic,ordre_X,typ):          #idem
        # liste tel que l[j] soit egal à l'ensemble des cliques auquel appartient j
        l=[[-1] for i in range(len(ordre_X))]
        for i in range(len(clic)):
            for j in clic[i][-1]:
                if l[ordre_X.index(j)]==[-1]:
                    l[ordre_X.index(j)][0]=i
                else:
                    l[ordre_X.index(j)].append(i)
        return l

    def ordre_H(self,ordre_X,adj_clique,clique,typ):           #idem
        # donne l'ordre d'élimination robuste de H en fonction de celui de X
        ordre_H=[]
        c_pris=np.zeros(len(clique))
        for i in range(len(ordre_X)):
            for j in adj_clique[i]:
                if c_pris[j]==0:
                    ordre_H.append(self.n+j)
                    c_pris[j]=1
            ordre_H.append(ordre_X[i])
        return ordre_H

    def ensemble_transversal(self,ordre_H,liste_X,ens_X,adj_clique,clique,typ):
        # donne l'ensemble transversal des cliques maximums de poids minimal
        def h(k,Y):
            #calcul la fonction h 
            if ordre_H[k]>=self.n:
                h=self.n*self.n
            else:
                h=self.w[ordre_H[k]]
            liste=voisin_H(k,liste_X,ens_X,adj_clique,clique,typ)
            for i in liste:
                h+=Y[ordre_H.index(i)]
            return h

        def voisin_H(k,liste_X,ens_X,adj_clique,clique,typ):
            # liste d'adjacence de H (peut etre)
            if ordre_H[k] <self.n:
                liste=liste_X[ens_X.index(ordre_H[k])][1]
                adj_clique=adj_clique[ens_X.index(ordre_H[k])]    # attention je sais pas si c'est vraiment k
                for i in adj_clique:
                    liste.append(self.n+i)
                return liste
            else:
                return clique[ordre_H[k]-self.n][-1]

        def inclus(Ti,T):
            # vérifie si Ti est inclus dans T
            for i in range(len(T)):
                if T[i]==0 and Ti[i]==1:
                    return False
            return True

        def Ti(i,ordre_H,liste_X,ens_X,adj_clique,clique,typ):
            #calcule Ti
            T_i=np.zeros(len(ordre_H))
            liste=voisin_H(i,liste_X,ens_X,adj_clique,clique,typ)
            for k in liste:
                if Y[ordre_H.index(k)]>0:
                    T_i[ordre_H.index(k)]=1
            return T_i                       


        voisin=[]
        for j in range(len(ordre_H)):
            voisin.append(voisin_H(j,liste_X,ens_X,adj_clique,clique, typ))
        
        X=np.zeros(len(ordre_H))
        Y=np.zeros(len(ordre_H))
        T=np.ones(len(ordre_H))
        for j in range(len(ordre_H)):
            H=0
            for k in voisin[j]:
                if H==0:
                    H=h(ordre_H.index(k),Y)
                elif h(ordre_H.index(k),Y)<H:
                    H=h(ordre_H.index(k),Y)
            Y[j]=H
        for i in range(len(ordre_H)-1,-1,-1):
            T_i=Ti(i,ordre_H,liste_X,ens_X,adj_clique,clique,typ)
            if h(i,Y)==0 and inclus(T_i,T):
                X[i]=1
                T-=T_i
        return X
    
    def impact_min(self):
        # calcule l'impact minimum de d et donne le type de d qui est optimal
        typ=self.typ_d
        l=[]
        for typ2 in self.types:
            if self.ordre[self.types.index(typ)][self.types.index(typ2)]==1 or typ2==typ:
                ens_d=self.ens_d(typ2)
                mat_d=self.mat_d(ens_d, typ2)
                ordre=self.trans_ordre(O.ordre(mat_d),ens_d)
                clic=self.clique_d(typ2)
                pres=self.pres_X(clic, typ2)
                ens_X=self.ens_X(pres, ens_d, typ2)
                mat_X=self.mat_X(ens_d, ens_X, mat_d, typ2)
                ordre_X=self.ordre_X(ordre, pres,ens_d, typ2)
                liste_X=self.liste_X(mat_X, ens_X, typ2)
                adj_clique=self.adj_clique(clic, ordre_X, typ2)
                ordre_H=self.ordre_H(ordre_X, adj_clique, clic, typ2)
                
                X=self.ensemble_transversal(ordre_H,liste_X,ens_X,adj_clique,clic, typ2)
                W=0
                for i in range(len(X)):
                    if ordre_H[i]<self.n:
                        W+=X[i]*self.w[ordre_H[i]]
                l.append([typ2,W,X,ordre_H])
        L=[l[i][1] for i in range(len(l))]
        k=np.argmin(L)
        return l[k]
            
        



    
        