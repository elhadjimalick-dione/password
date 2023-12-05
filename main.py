import re
import hashlib
import json
import os
import random
import string

def verifier_mot_de_passe(mot_de_passe):
    return (
        len(mot_de_passe) >= 8 and
        any(c.isupper() for c in mot_de_passe) and
        any(c.islower() for c in mot_de_passe) and
        any(c.isdigit() for c in mot_de_passe) and
        any(c in '!@#$%^&*' for c in mot_de_passe)
    )

def hasher_mot_de_passe(mot_de_passe):
    hasher = hashlib.sha256()
    hasher.update(mot_de_passe.encode('utf-8'))
    return hasher.hexdigest()

def generer_mot_de_passe():
    caracteres = string.ascii_letters + string.digits + '!@#$%^&*'
    return ''.join(random.choice(caracteres) for _ in range(12))  

def mot_de_passe_deja_present(mot_de_passe_hashe, fichier):
    if not os.path.exists(fichier):
        return False

    with open(fichier, 'r') as file:
        data = json.load(file)

    return mot_de_passe_hashe in data['mots_de_passe']

def enregistrer_mot_de_passe(mot_de_passe_hashe, fichier):
    if not os.path.exists(fichier):
        with open(fichier, 'w') as file:
            json.dump({"mots_de_passe": []}, file)

    if not mot_de_passe_deja_present(mot_de_passe_hashe, fichier):
        with open(fichier, 'r') as file:
            data = json.load(file)
        data['mots_de_passe'].append(mot_de_passe_hashe)
        with open(fichier, 'w') as file:
            json.dump(data, file)
        return True
    else:
        return False

def afficher_mots_de_passe(fichier):
    if not os.path.exists(fichier):
        print("Aucun mot de passe enregistré.")
        return

    with open(fichier, 'r') as file:
        data = json.load(file)
    print("Mots de passe enregistrés (hachés) :")
    for mot_de_passe_hashe in data['mots_de_passe']:
        print(mot_de_passe_hashe)

while True:
    choix = input("Voulez-vous ajouter un nouveau mot de passe (A) ou afficher les mots de passe enregistrés (F)? ").lower()

    if choix == 'a':
        mot_de_passe = generer_mot_de_passe()

        while not verifier_mot_de_passe(mot_de_passe):
            mot_de_passe = generer_mot_de_passe()

        print("Mot de passe généré :", mot_de_passe)

        mot_de_passe_hashe = hasher_mot_de_passe(mot_de_passe)

        if enregistrer_mot_de_passe(mot_de_passe_hashe, 'mots_de_passe.json'):
            print("Mot de passe enregistré avec succès.")
            print("Mot de passe haché (SHA-256) :", mot_de_passe_hashe)
        else:
            print("Le mot de passe est déjà enregistré.")
    elif choix == 'f':
        afficher_mots_de_passe('mots_de_passe.json')
    else:
        print("Choix invalide. Veuillez entrer 'A' pour ajouter un nouveau mot de passe ou 'F' pour afficher les mots de passe.")