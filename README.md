# Decision-Aid

Ce projet est une mise en pratique et une application des divers algorithmes d'optimisation multi-critères pour l'aide à la prise de décision. Notre objectif est de faire un classement des pays consommant le plus/moins de matières grasses pour de divers profils.

Le méthodes qui sont inclus dans ce projet sont notamment: la somme pondérée, la méthode PROMETHEE I et II avec et sans application des seuils de préférences, la méthode TOPSIS et finalement la méthode ELECTRE Is sans l'application des seuils de véto.

Le jeu de données sur lequel les divers méthodes ont pu être testé sont des données du site Kaggle. Il s'agit du [COVID-19 Healthy Diet Dataset](https://www.kaggle.com/datasets/mariaren/covid19-healthy-diet-dataset?select=Fat_Supply_Quantity_Data.csv).

Un rapport réalisé en analysant les résultats obtenus : [Rappport d'analyse](./Resultats/Rapport_Aide_a_la_decision_Marie_ZEPHIR_Yingqi_LUO.pdf)

## Organisation
- `Electre.py` : Méthode ELECTRE Is sans application des seuils de veto.

- `Promethee_seuil.py` : Méthode PROMETHEE I et II avec une application des seuils de préférences. 

- `Promethee.py` : Méthode PROMETHEE I et II sans seuils de préférences.

- `Topsis.py` : Méthode TOPSIS sans la phase de normalisation des données.

- `weightedSum.py` : Méthode de somme pondérée.

- `Create_seuils.py` : Fonctionnalité permettant de créer un fichier .csv contenant les seuils de préférences à utiliser dans la méthode PROMETHEE I et II. 

- `Donnees/`: Dossier contenant l'ensemble des données à utiliser en entrée des différentes méthodes et scripts.

- `Resultats/` : Dossier contenant l'ensemble des sorties/résultats de chacune des méthodes appliquées.

## Exécution du script

Afin d'exécuter les divers scripts, il suffit de le lancer en ligne de commande avec Python.
