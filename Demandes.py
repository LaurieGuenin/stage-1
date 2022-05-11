# -*- coding: utf-8 -*-
"""
Created on Tue May  3 08:38:02 2022

@author: laurie
"""
import random
import matplotlib.pyplot as plt
import numpy as np
import Agents
import Distances
import copy


class Demande:
    def __init__(self,t_d,deb,fin,typ,carac=None,PMax=None,Pref=None,strat=None,orig=None,dest=None):
        self.t_d=t_d  #moment où la demande a été enregistré
        self.deb=deb  #début de la location
        self.fin=fin  #fin de la location
        self.typ=typ  #typ de la location
        self.PMax=PMax  #prix max accépté par le client
        self.Pref=Pref  #préférences du client sous forme liste ou de matrice de ratio
        self.strat=strat  #strategie du client sous forme de chaine de caractere
        self.orig=orig   #lieu de départ
        self.dest=dest   #lieu d'arrivée
        self.intervalle=[deb,fin]  #intervalle de location
        self.carac=carac
        
        
