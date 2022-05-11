import random
import matplotlib.pyplot as plt
import numpy as np




class Ens_d_intervalles:
    def __init__(self,nbr_etapes,para,nbr_v=0,n=0):
        if para=='random':   #Génération aléatoire de n intervalles sur un espace temps de nbr_etapes
            a=random.randint(0,nbr_etapes)
            b=random.randint(0,nbr_etapes)
            mini=min(a,b)
            maxi=max(a,b)
            self.d=(mini,maxi)      # la demande à ajouter

            self.intervalles=[]     #ensemble des intervalles décrits par un tableau numpy avec le minimum et maximum
            for i in range(n):
                a=random.randint(0,nbr_etapes)
                b=random.randint(0,nbr_etapes)
                while a==b:
                    b=random.randint(0,nbr_etapes)
                mini=min(a,b)
                maxi=max(a,b)
                self.intervalles.append(np.array([mini,maxi]))

            self.n=n               #le nombre d'intervalles
            self.nbr_etapes=nbr_etapes   #le nombre d'étapes
            self.nbr_v=0               #le nombre de véhicules nécessaires pour réaliser ces intervalles
            clic=self.clique()
            c=clic[0][-1]
            self.nbr_v=len(c)
            for i in range(len(clic)):
                if len(clic[i][-1])>self.nbr_v:
                    self.nbr_v=len(clic[i][-1])
            self.w=[random.random() for i in range(self.n)]  # le bénéfice de chaque intervalle
        
        
        elif para=='random2': #Génération aléatoire d'intervalles sur un espace temps de nbr_etapes et qui sont réalisables avec nbr_v véhicules
            self.d=(0,nbr_etapes)  # la demande étant tout l'intervalles que l'on étudie 
            self.nbr_v=nbr_v      # le nombre de véhicules
            self.nbr_etapes=nbr_etapes  #le nombre d'étapes

            self.intervalles=[]  #ensemble des intervalles décrits par un tableau numpy avec le minimum et maximum
            B=True
            l=np.zeros(nbr_etapes)
            while B:
                a=random.randint(0,nbr_etapes-2)
                b=random.randint(a+1,nbr_etapes-1)
                for i in range(a,b+1):
                    if l[i]==nbr_v:
                        B=False
                    l[i]+=1
                if B:
                    self.intervalles.append(np.array([a,b]))
            self.n=len(self.intervalles)   # le nombre d'intervalles créés
            self.w=[random.random() for i in range(self.n)]  # le bénéfice de chaque intervalle

    def affichage(self):
        # Affiche l'ensemble des intervalles sur un graphique en fonction de temps
        for i in range (len(self.intervalles)):
            plt.plot(self.intervalles[i],[i,i])
        plt.show()


    def clique(self):
        # trouve les cliques qui sont de cardinal plus grand que le nombre de véhicules
        ens=[]
        clic=[]
        ens_bis=[-1]
        for i in range(self.nbr_etapes):
            for j in range(len(self.intervalles)):
                mini,maxi=self.intervalles[j]
                if mini<=i and i<=maxi:
                    ens.append(j)
            if len(ens)>=self.nbr_v and ens_bis!=ens:
                clic.append([i,ens])
            elif len(ens)>=self.nbr_v and ens_bis==ens:
                clic[-1].insert(-2,i)
            ens_bis=ens
            if ens_bis==[]:
                ens_bis.append(-1)
            ens=[]
        return clic

    def matrice(self):
        # Créer la matrice d'adjacence du graphe d'intervalles
        mat=np.zeros((self.n,self.n))
        for i in range(len(self.intervalles)):
            minii,maxii=self.intervalles[i]
            for j in range(i+1,len(self.intervalles)):
                minij,maxij=self.intervalles[j]
                if (minii<=minij and minij<=maxii) or (minii<=maxij and maxij<=maxii) or  (minij<=minii and minii<=maxij) or (minij<=maxii and maxii<=maxij) :
                    mat[i][j]=1
                    mat[j][i]=1
        return mat

    def liste(self):        #Attention passage par la matrice peut-être pas optimale
    # créer la liste d'adjacence    
        liste=[]
        mat=self.matrice()
        for i in range(len(self.intervalles)):
            l=[]
            for j in range(len(self.intervalles)):
                if mat[i][j]==1:
                    l.append(j)
            liste.append(l)
        return liste

    def ens_dem(self):
        # ensemble des intervalles qui intersectent la demande pour random2 cest self.intervalles
        ens_dem=[]
        for i in range(len(self.intervalles)):
            minii,maxii=self.intervalles[i]
            if (minii<=self.d[0] and self.d[0] <=maxii) or (minii<=self.d[1]  and self.d[1] <=maxii) or  (self.d[0] <=minii and minii<=self.d[1] ) or (self.d[0] <=maxii and maxii<=self.d[1] ) :
                ens_dem.append(i)
        return ens_dem

    def mat_dem(self):
        # matrice d'adjacence entre les intervalles de ens_dem
        ens=self.ens_dem()
        mat=np.zeros((len(ens),len(ens)))
        for i in range(len(ens)):
            for j in range(len(ens)):
                if self.matrice()[ens[i]][ens[j]]==1:
                    mat[i][j]=1
        return mat

    def liste_dem(self):
        # liste d'adjacence entre les intervalles de ens_dem
        liste=[]
        mat=self.mat_dem()
        ens_dem=self.ens_dem()
        for i in range(len(mat)):
            l=[]
            for j in range(len(mat)):
                if mat[i][j]==1:
                    l.append(ens_dem[j])
            liste.append([ens_dem[i],l])
        return liste


    def pres_X(self):
        # liste de présence des sommets de n dans X, c'est une liste de 0 et 1, 0 quand le sommet est présent 1 quand il est absent
        # peut être mettre que les sommets de ens_dem
        l=[]
        clic=self.clique()
        for i in range(len(clic)):
            for j in range(len(clic[i][-1])):
                l.append(clic[i][-1][j])
        pres=np.zeros(self.n)
        for i in l:
            pres[i]=1
        return pres


    def ens_X(self):
        # ensemble des sommets présents dans X
        liste=[]
        pres=self.pres_X()
        for i in range(self.n):
            if pres[i]==1:
                liste.append(i)
        return liste

    def mat_X(self):
        # matrice d'adjacence entre les sommets de X
        ens_X=self.ens_X()
        matrice=self.matrice()
        mat=np.zeros((len(ens_X),len(ens_X)))
        for i in range(len(ens_X)):
            for j in range(len(ens_X)):
                if matrice[ens_X[i]][ens_X[j]]==1:
                    mat[i][j]=1
        return mat

    def liste_X(self):
        # liste d'adjacence entre les sommets de X
        liste=[]
        mat=self.mat_X()
        ens_X=self.ens_X()
        for i in range(len(mat)):
            l=[]
            for j in range(len(mat)):
                if mat[i][j]==1:
                    l.append(j)
            liste.append([ens_X[i],l])
        return liste

    def ordre_X(self):          # en fonction d'une fonction pas faite
        # donne l'ordre d'élimination robuste de X en fonction de celui de G
        ordre_X=self.ordre_elimination_robuste()
        pres=self.pres_X()
        for i in range(len(ordre_X)-1,-1,-1):
            if pres[ordre_X[i]]==0:
                ordre_X.pop(i)
        return(ordre_X)

    def pos_X(self,k):        #idem
        # position de l'élément k dans l'ordre d'élimination robuste
        i=0
        ordre_X=self.ordre_X()
        while ordre_X[i]!=k:
            i+=1
        if ordre_X[i]==k:
            return i
        else:
            return -1



    #def ordre_elimination_robuste(self):

    def adj_clique(self):          #idem
        # liste tel que l[j] soit egal au x cliques auquel appartient j
        clic=self.clique()
        ordre_X=self.ordre_X()
        l=-1*np.ones((1,len(ordre_X)))
        for i in range(len(clic)):
            for j in clic[i][-1]:
                if l[j]==[-1]:
                    l[j].pop(0)
                l[j].append(i)
        return l

    def ordre_H(self):           #idem
        # donne l'ordre d'élimination robuste de H en fonction de celui de X
        ordre_X=self.ordre_X()
        adj_clique=self.adj_clique()
        ordre_H=[]
        clique=self.clique()
        c_pris=np.zeros(len(clique))
        for i in range(ordre_X):
            for j in adj_clique[i]:
                if c_pris[j]==0:
                    ordre_H.append(self.n+j)
                    c_pris[j]=1
            ordre_H.append(i)

    def ensemble_transversal(self):
        # donne l'ensemble transversal des cliques maximums de poids minimal
        def h(k,Y):
            #calcul la fonction h 
            if k>self.n:
                h=self.n*self.n
            else:
                h=self.w[k]
            liste=voisin_H(k)
            for i in liste:
                h+=Y[i]
            return h

        def voisin_H(k):
            # liste d'adjacence de H (peut etre)
            liste=self.liste_X()[self.pos_X(k)]
            adj_clique=self.adj_clique()[self.pos_X(k)]    # attention je sais pas si c'est vraiment k
            for i in adj_clique:
                liste.append(self.n+i)
            return liste

        def inclus(Ti,T):
            # vérifie si Ti est inclus dans T
            for i in range(len(T)):
                if T[i]==1 and Ti[i]==1:
                    return False
            return True

        def Ti(i):
            #calcule Ti
            ordre_H=self.ordre_H()
            Ti=np.zeros(len(ordre_H))
            liste=voisin_H(i)
            for k in liste:
                if Y[self.pos_X(k)]>0:
                    Ti[self.pos_X(k)]=1
            return Ti                        # peut etre position de k dans l'ordre



        ordre_H=self.ordre_H()
        X=np.zeros(len(ordre_H))
        Y=np.zeros(len(ordre_H))
        T=np.ones(len(ordre_H))
        for j in range(self.n):
            h=0
            for k in voisin_H(j):
                if h==0:
                    h=h[k,Y]
                elif h[k,Y]<h:
                    h=h[k,Y]
            Y[j]=h
        for i in range(self.n-1,-1,-1):
            Ti=Ti(i)
            if h(i,Y)==0 and inclus(Ti,T):
                X[i]=1
                T-=Ti
        return X





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





















