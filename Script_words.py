# -*- coding: utf-8 -*-
"""
Created on Sat May 21 16:18:46 2022

@author: ludo_
"""
from collections import Counter
from gensim.models import KeyedVectors
import hashlib
import re
from pathlib import Path
import requests

def get_cac40(cac_file = "input/cac40.txt"):

    path = Path(cac_file)
    if path.exists() and path.is_file() :
    
        with open(cac_file, "r", encoding="utf8") as data :
        
            for line in data :
                line = line.rstrip()
                comp = line.split(',')
            return comp
    
    else: print(f"No txt file found at {cac_file}. Please provide suitable path.")

def get_model(model_path = "input/model_fr.bin"):
    #Check if model exists, if not, download it and write it on disk
    model_file = Path(model_path)
    if model_file.exists() and model_file.is_file():
        
        model = KeyedVectors.load_word2vec_format(model_path, binary=True, unicode_errors="ignore")
    
    else : 
        
        check = False
        #Hahslib permet de vérifier que le fichier n'est pas corrompu ou modifié, conformémemnt au md5
        #donné par Mr. Fauconnier sur son site : https://embeddings.net/embeddings/md5sum.txt
        while check == False:
            link = "https://embeddings.net/embeddings/frWac_postag_no_phrase_700_skip_cut50.bin"
            response = requests.get(link)
            if hashlib.md5(response.content).hexdigest() == "0695f811c5f76a51bc335633213d2aa8" :
                check = True
        
        print("Safe model file downloaded")
        open("input/model_fr.bin", "wb").write(response.content)
        model = KeyedVectors.load_word2vec_format(model_path, binary=True, unicode_errors="ignore")
    
    return model

def get_close_words(word, model):

    liste_mots = model.most_similar(topn=50,positive=[word.casefold()+"_n"])
    
    dict_mots = {}
    for mot, score in liste_mots :
        dict_mots[mot] = model.most_similar(topn=30,positive=[mot])
        
    liste_mots_similaires = []
    for sim in dict_mots.values():
        for pair in sim :
            m = re.search(r'(.*)(_.*)', pair[0])
            w = m.group(1)
            liste_mots_similaires.append(w)
        
    occurences = Counter(liste_mots_similaires)
    occurences_best = occurences.most_common()
    most_common = []
    for word in occurences_best:
        most_common.append(word[0])
    best_words = most_common[:30]
    
    return best_words
