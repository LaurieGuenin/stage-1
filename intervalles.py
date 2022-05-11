import random
import matplotlib.pyplot as plt
import numpy as np

random.seed(12)


def creer_intervalle(n,nbr_etape):
    e=[]
    for i in range(n):
        a=random.randint(0,nbr_etape)
        b=random.randint(0,nbr_etape)
        while a==b:
            b=random.randint(0,nbr_etape)
        mini=min(a,b)
        maxi=max(a,b)
        e.append(np.array([mini,maxi]))
    return e

def creer_demande(nbr_etape):
    a=random.randint(0,intervalle)
    b=random.randint(0,intervalle)
    mini=min(a,b)
    maxi=max(a,b)
    return(mini,maxi)

def affichage(intervalles):
    for i in range (len(intervalles)):
        plt.plot(intervalles[i],[i,i])
    plt.show()


def clique(intervalles,nb_vehicules,nbr_etapes):
    e=[]
    clique=[]
    for i in range(nbr_etapes):
        for j in range(len(intervalles)):
            mini,maxi=intervalles[j]
            if mini<=i and i<=maxi:
                e.append(j)
        if len(e)>nb_vehicules:
            clique.append([i,e])
        e=[]
    return clique

def matrice(intervalles,n):
    mat=np.zeros((n,n))
    for i in range(len(intervalles)):
        minii,maxii=intervalles[i]
        for j in range(i+1,len(intervalles)):
            minij,maxij=intervalles[j]
            if (minii<=minij and minij<=maxii) or (minii<=maxij and maxij<=maxii) or  (minij<=minii and minii<=maxij) or (minij<=maxii and maxii<=maxij) :
                mat[i][j]=1
                mat[j][i]=1
    return mat

def liste(intervalles,n):        #Attention passage par la matrice peut-être pas optimale
    liste=[]
    mat=matrice(intervalles,n)
    for i in range(len(intervalles)):
        l=[]
        for j in range(len(intervalles)):
            if mat[i][j]==1:
                l.append(j)
        liste.append(l)
    return liste


def distance_initiaux(int1,int2):
    d=abs(int1[0]-int2[0])/(max(int1[1],int2[1])-min(int1[0],int2[0]))
    return d

def distance_finaux(int1,int2):
    d=abs(int1[1]-int2[1])/(max(int1[1],int2[1])-min(int1[0],int2[0]))
    return d

def distance_longueurs(int1,int2):
    d=1-(min(int1[1]-int1[0],int2[1]-int2[0]))/(max(int1[1]-int1[0],int2[1]-int2[0]))
    return d

def distance_chevauchement(int1,int2):
    mini=min(int1[1],int2[1])
    maxi=max(int1[0],int2[0])
    if mini<maxi:
        return 1
    else:
        d=1-(mini-maxi)/(min(int1[1]-int1[0],int2[1]-int2[0]))
        return d

def distance_ecart(int1,int2):
    mini=min(int1[1],int2[1])
    maxi=max(int1[0],int2[0])
    if mini<maxi:
        d=(min(int1[1]-int2[0],int2[1]-int1[0]))/(max(int1[1],int2[1])-min(int1[0],int2[0]))
        return d
    else:
        return 0


def distance_temporelle(ints1,ints2,nb_vehicules,nbr_etapes):
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

def dist_ens_egaux(ints1,ints2,nb_vehicules,nbr_etapes,T1=[1/7,1/7,1/7,1/7,1/7], D1=[distance_initiaux,distance_finaux,distance_longueurs,distance_chevauchement,distance_ecart],T2=[distance_temporelle,taux_de_remplissage]):
    mat=np.zeros([len(ints1),len(ints2)])
    for i in range(len(ints1)):
        for j in range(len(ints2)):
            d=0
            for k in range(len(T1)):
                d+=T1[k]*(D1[k](ints1[i],ints2[j]))
            mat[i][j]=d
    D=algo_hongrois                                # a voir avec dominique
    for k in range(len(T2)):
        D+=T2[k]*(D2[k](ints1,ints2))
    return D


def algo_hongrois(matrice):                        # a voir avec dominique
    for i in range(len(matrice)):
        min=1
        for j in range(len(matrice[0])):
            if matrice[i][j]<min:
                min=matrice[i][j]
        for j in range(len(matrice[0])):
            matrice[i][j]-=min
    for j in range(len(matrice)):
        min=1
        for i in range(len(matrice[0])):
            if matrice[i][j]<min:
                min=matrice[i][j]
        for i in range(len(matrice[0])):
            matrice[i][j]-=min

def X()

#def ordre_elimination_robuste():

#def transformation_ordre():

#def ensemble_transversal():


















