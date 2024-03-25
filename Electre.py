import pandas as pd
import numpy as np

# Fonction pour calculer le degré de préférence univarié
def preference_degree(data_candidate1, data_candidate2, criterion_weight, criterion_objectif):
    preference_degreeSum = 0
    for criterion in criterion_weight:
        if criterion_objectif[criterion].iloc[0].lower() == 'max':
            preference_degreeSum += float(criterion_weight[criterion].iloc[0]) if data_candidate1[criterion] >= data_candidate2[criterion] else 0
        elif criterion_objectif[criterion].iloc[0].lower() == 'min':
            preference_degreeSum += float(criterion_weight[criterion].iloc[0]) if data_candidate1[criterion] <= data_candidate2[criterion] else 0
    return preference_degreeSum
        
    
# Fonction pour calculer le degré de préférence multicritère
def multicriteria_preference(data_df, criterion_weight, criterion_objectif):
    n = data_df.shape[0]
    preference_table = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            preference_table[i][j] = preference_degree(data_df.iloc[i], data_df.iloc[j], criterion_weight, criterion_objectif) if i != j else None
    
    return preference_table



def calcul_for_all_profil(data_df, lstProfil, data_weights, nameColumnWeight, data_objectives, nameColumnObjective):
    
    rsl_multicriteria_preference = {}
    
    for profil in lstProfil:
        rsl_multicriteria_preference[profil] = multicriteria_preference(data_df, data_weights[data_weights[nameColumnWeight] == profil], data_objectives[data_objectives[nameColumnObjective] == profil])
        
    return rsl_multicriteria_preference
    
    
    
def main():
    # data_path = 'Donnees/testdata.csv'
    data_path = 'Donnees/Fat_Data.csv'
    weights_path = 'Donnees/Fat_poids.csv'
    objectives_path = 'Donnees/Fat_objective.csv'

    data_df = pd.read_csv(data_path)
    weights_df = pd.read_csv(weights_path)
    objectives_df = pd.read_csv(objectives_path)

    # data = pd.read_csv(data_path)
    # data_objectif = data[data['categorie'] == 'objectif']
    # data_weight = data[data['categorie'] == 'poids']
    # data = data[data['categorie'] != 'objectif']
    # data = data[data['categorie'] != 'poids']

    candidates = data_df['Country']
    criteria = data_df.columns[1:] # La première colonne est celle des candidats
    lstProfils = weights_df['Poids']
    
    print(calcul_for_all_profil(data_df, lstProfils, weights_df, 'Poids', objectives_df, 'Poids')['Profil 1'])
    
    
main()