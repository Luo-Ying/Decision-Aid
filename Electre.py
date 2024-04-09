import pandas as pd
import numpy as np
import csv

"""Avec les données de test de TD2"""
# data_path = 'Donnees/testdata.csv'
# data_df = pd.read_csv(data_path)
# objectives_df = data_df[data_df['categorie'] == 'objectif']
# weights_df = data_df[data_df['categorie'] == 'poids']
# seuil_df = data_df[data_df['categorie'] == 'seuil']
# data_df = data_df[data_df['categorie'] != 'objectif']
# data_df = data_df[data_df['categorie'] != 'poids']
# data_df = data_df[data_df['categorie'] != 'seuil']

"""Avec les données de Fat_Data.csv"""
data_path = 'Donnees/Fat_Data.csv'
weights_path = 'Donnees/Fat_poids.csv'
objectives_path = 'Donnees/Fat_objective.csv'
seuil_path = 'Donnees/Fat_seuils.csv'

data_df = pd.read_csv(data_path)
weights_df = pd.read_csv(weights_path)
objectives_df = pd.read_csv(objectives_path)
seuil_df=pd.read_csv(seuil_path)

def distance_diff(data_candidate1_value, data_candidate2_value, criterion_weight_value, seuil_data_value):
    data_candidate1_value = float(data_candidate1_value)
    data_candidate2_value = float(data_candidate2_value)
    seuil_data_value = float(seuil_data_value)
    diff = abs(data_candidate1_value - data_candidate2_value)
    if (diff <= seuil_data_value):
        rslt = (1-(diff/seuil_data_value))*criterion_weight_value
    else:   rslt = 0
    return rslt
    

# Fonction pour calculer le degré de préférence univarié
def preference_degree(data_candidate1, data_candidate2, criterion_weight, criterion_objectif, seuil=False, seuil_value = 0):
    preference_degreeSum = 0
    for criterion in criterion_weight:
        if criterion_objectif[criterion].iloc[0].lower() == 'max':
            if float(data_candidate1[criterion]) >= float(data_candidate2[criterion]):
                preference_degreeSum += float(criterion_weight[criterion].iloc[0])
            else:
                if seuil: 
                    preference_degreeSum += distance_diff(data_candidate1[criterion], data_candidate2[criterion], float(criterion_weight[criterion].iloc[0]), seuil_value[criterion].iloc[0])
                else: 
                    preference_degreeSum +=0
        elif criterion_objectif[criterion].iloc[0].lower() == 'min':
            if float(data_candidate1[criterion]) <= float(data_candidate2[criterion]):
                preference_degreeSum += float(criterion_weight[criterion].iloc[0])
            else:
                if seuil: 
                    preference_degreeSum += distance_diff(data_candidate1[criterion], data_candidate2[criterion], float(criterion_weight[criterion].iloc[0]), seuil_value[criterion].iloc[0])
                else: 
                    preference_degreeSum +=0
    return preference_degreeSum
        
    
# Fonction pour calculer le degré de préférence multicritère
def multicriteria_preference(criterion_weight, criterion_objectif, seuil=False, data_seuil=0):
    n = data_df.shape[0]
    preference_table = np.zeros((n, n))
    
    for i in range(n):
        for j in range(n):
            preference_table[i][j] = preference_degree(data_df.iloc[i], data_df.iloc[j], criterion_weight,  criterion_objectif, seuil, data_seuil ) if i != j else None
    
    return preference_table



def calcul_for_all_profile(lstProfil, nameColumnWeight, nameColumnObjective, seuil=False, nameColumnSeuil="Seuils"):
    
    rsl_multicriteria_preference = {}
    
    for profil in lstProfil:
        rsl_multicriteria_preference[profil] = multicriteria_preference(weights_df[weights_df[nameColumnWeight] == profil], objectives_df[objectives_df[nameColumnObjective] == profil], seuil, seuil_df[seuil_df[nameColumnSeuil] == profil])
        
    return rsl_multicriteria_preference
    
    
    
def main():
 
    """Avec les données de test de TD2"""
    # test_data_rslt = multicriteria_preference(weights_df,objectives_df, False)
    # test_data_rslt_seuil = multicriteria_preference(weights_df,objectives_df,True, seuil_df)
    # print(test_data_rslt)
    # print()
    # print(test_data_rslt_seuil)


    """Avec les données de Fat_Data.csv"""
    candidates = data_df['Country']
    criteria = data_df.columns[1:] # La première colonne est celle des candidats
    lstProfils = weights_df['Poids']
    
    rslt = calcul_for_all_profile(lstProfils, 'Poids', 'Poids', False)
    rslt_with_seuil = calcul_for_all_profile(lstProfils, 'Poids', 'Poids', True, 'Seuils')
    
    print(rslt['Profil 1'])
    print(rslt['Profil 2'])
    print(rslt['Profil 3'])
    
    print(rslt_with_seuil['Profil 1'])
    print(rslt_with_seuil['Profil 2'])
    print(rslt_with_seuil['Profil 3'])


    
main()