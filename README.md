# 🩺 Détection du Cancer du Sein par Machine Learning

## Présentation du projet
Le cancer du sein est l’une des principales causes de mortalité chez les femmes dans le monde.
Une détection précoce permet d’augmenter considérablement les chances de guérison.

Ce projet propose une solution basée sur le Machine Learning afin d’assister les
professionnels de santé dans la classification des tumeurs mammaires en bénignes
ou malignes à partir du jeu de données Wisconsin Diagnostic Breast Cancer.

---

## Objectifs
- Détecter le cancer du sein avec une haute précision
- Comparer plusieurs algorithmes de Machine Learning
- Réduire le temps de diagnostic
- Limiter les erreurs humaines
- Proposer une interface utilisateur simple et intuitive

---


## Jeu de données
- Nom : Wisconsin Diagnostic Breast Cancer Dataset (WDBC)
- Nombre d’échantillons : 569
  - 357 tumeurs bénignes
  - 212 tumeurs malignes
- Nombre de caractéristiques : 30
- Variable cible : diagnosis (B → 0, M → 1)

---

## Prétraitement des données
- Suppression des colonnes non pertinentes (id, Unnamed: 32)
- Encodage de la variable cible
- Normalisation avec StandardScaler
- Séparation des données :
  - 70 % entraînement
  - 30 % test

---

## Modèles de Machine Learning

### 🔹 Perceptron Multicouche (MLP)
- Réseau de neurones avec plusieurs couches cachées
- Fonction d’activation ReLU
- Très bonne performance pour la classification binaire

### 🔹 GRU + SVM
- Combinaison de réseaux neuronaux et de SVM
- Amélioration de la généralisation

### 🔹 Arbre de Décision
- Modèle simple et interprétable
- Rapide à entraîner
- Sensible au surapprentissage

### 🔹 Voting Classifier
- Combinaison de plusieurs modèles :
  - Random Forest
  - AdaBoost
  - XGBoost
- Amélioration de la robustesse et de la précision

---

## Apprentissage par Renforcement
Une approche expérimentale basée sur l’apprentissage par renforcement a été utilisée
pour améliorer les arbres de décision :
- Les décisions de découpage sont vues comme des actions
- L’agent reçoit une récompense selon la performance du modèle
- Objectif : maximiser la précision globale

---

## Évaluation
- Accuracy
- Precision
- Recall
- F1-score
- Matrice de confusion

Résultat : une précision pouvant atteindre environ 98 % avec les modèles d’ensemble.

---

## Déploiement
- Backend : FastAPI
- Frontend : Streamlit / Web (HTML, CSS, JavaScript)

Fonctionnalités :
- Saisie manuelle des caractéristiques
- Prédiction du type de tumeur
- Affichage du résultat et du score de confiance

---

## Technologies utilisées
- Python
- Scikit-learn
- TensorFlow / Keras
- FastAPI
- Streamlit
- Pandas
- NumPy

---

## Avertissement
Ce projet est destiné à un usage académique et pédagogique uniquement.
Il ne remplace en aucun cas un diagnostic médical professionnel.

---

## Auteurs
- Mohamed Ali Jabri 
- Feryel Ifaoui  
- Mohamed Khalil Kamessi   
- Najeh Benrebeh  
- Ines Ben Dhifallah  

Année universitaire : 2025 – 2026


