# -*- coding: utf-8 -*-
"""
Created on Tue May  3 08:38:00 2022

@author: laurie
"""

import random
import matplotlib.pyplot as plt
import numpy as np

class Agent:
    def __init__(self,Nb_V,types,ordre_types,adresses=None,minP=None,maxP=None):
        self.adresses=adresses  # adresses de prise et de depot de véhicules
        self.Nb_V=Nb_V     # nombre de véhicules par types et par périodes
        self.types=types  # types des véhicules
        self.minP=minP   # Prix minimum de chaque demande
        self.maxP=maxP   # prix maximum de chaque demande 
        self.ordre_types=ordre_types # ordre partiel sur les types de véhicules
        self.profit=0  #profit de l'agent 
        self.demandes_acceptées=[]  #ensemble des demandes accéptées
        