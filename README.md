# Calculateur IMC — Projet Python 2ème année

## Fonctionnalités
- Saisie : âge, taille (cm), poids (kg), sexe
- Calcul de l'IMC :  IMC = poids / taille²
- Catégorie : Dénutrition / Maigreur / Normal / Surpoids / Obésité I-II-III
- Poids idéal (formule de Lorentz)
- Barre visuelle colorée de l'IMC
- Interface sombre avec Tkinter (aucune dépendance externe)

## Formules utilisées
- IMC = poids (kg) / (taille (m))²
- Poids idéal Homme  : taille - 100 - (taille - 150) / 4
- Poids idéal Femme  : taille - 100 - (taille - 150) / 2.5

## Notions Python mobilisées
- Entrées utilisateur (Tkinter Entry + StringVar)
- Calculs arithmétiques
- Conditions (if / elif / for)
- Classes et POO (tkinter.Tk)
- Gestion d'erreurs (try/except)

## Lancer le script directement
    python imc_app.py

## Générer le .exe (Windows)
1. Double-cliquer sur `build.bat`
2. Attendre la fin de la compilation
3. Récupérer `dist\CalculateurIMC.exe`
   → Aucune installation Python requise sur l'ordinateur cible !

Prérequis : Python 3.8+ installé, connexion internet pour PyInstaller