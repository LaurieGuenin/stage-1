# -*- coding: utf-8 -*-
"""
Created on Fri May  6 15:16:14 2022

@author: laurie
"""
import numpy as np

def ordre(matrice):
    N=len(matrice)
    ordre=[[i for i in range(N)]]
    r=0
    c=0
    cpt=0
    while r<len(ordre) and c<len(ordre) and cpt<N**2:
        cpt+=1
        R=ordre[r]
        C=ordre[c]
        t=[[matrice[r1][c1] for c1 in C] for r1 in R]
        t=np.array(t) 
        if np.count_nonzero(t==0)==0 or np.count_nonzero(t==1)==0 or len(C)==1:
            if r<len(ordre)-1:
                r=r+1
            else:
                r=0
                c=c+1
        else: 
            for i in range(len(t)):
                if np.count_nonzero(t[i]==0)!=0 and np.count_nonzero(t[i]==1)!=0:
                    zeros=[]
                    ones=[]
                    for j in range(len(t[i])):
                        if t[i][j]==0:
                            zeros.append(ordre[c][j])
                        else:
                            ones.append(ordre[c][j])
                    ordre.pop(c)
                    ordre.insert(c,zeros)
                    ordre.insert(c,ones)
                    break
    return ordre

#matrice=[[1,0,0,0,0,1,1],
#          [0,1,1,1,1,1,0],
#          [0,1,1,1,1,1,0],
#          [0,1,1,1,1,1,0],
#          [0,1,1,1,1,1,1],
#          [1,1,1,1,1,1,1],
#          [1,0,0,0,1,1,1]]
# print(ordre(matrice))
                