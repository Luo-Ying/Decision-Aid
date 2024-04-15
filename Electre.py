import pandas as pd
import numpy as np
import csv

"""Avec les données de test de TD2"""
# data_path = 'Donnees/Test_Data.csv'
# weights_path = 'Donnees/Test_poids.csv'
# objectives_path = 'Donnees/Test_objective.csv'
# seuil_path = 'Donnees/Test_seuils.csv'
# veto_path = 'Donnees/Test_veto.csv'

"""Avec les données de Fat_Data.csv"""
data_path = 'Donnees/Fat_Data.csv'
weights_path = 'Donnees/Fat_poids.csv'
objectives_path = 'Donnees/Fat_objective.csv'
seuil_path = 'Donnees/Fat_seuils.csv'

data_df = pd.read_csv(data_path)
weights_df = pd.read_csv(weights_path)
objectives_df = pd.read_csv(objectives_path)
seuil_df=pd.read_csv(seuil_path)
# veto_df=pd.read_csv(veto_path)

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
    criterion_weight = criterion_weight.iloc[:, 1:]
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

def get_veto(data_candidate1, data_candidate2, criterion_weight, criterion_objectif, criterion_veto):
    veto = False
    criterion_weight = criterion_weight.iloc[:, 1:]
    for criterion in criterion_weight:
        diff = abs(float(data_candidate1[criterion]) - float(data_candidate2[criterion]))
        if criterion_objectif[criterion].iloc[0].lower() == 'max':
            if float(data_candidate1[criterion]) < float(data_candidate2[criterion]) and diff > float(criterion_veto[criterion]):
                veto = True
        elif criterion_objectif[criterion].iloc[0].lower() == 'min':
            if float(data_candidate1[criterion]) > float(data_candidate2[criterion]) and diff > float(criterion_veto[criterion]):
                veto = True
    return veto

def multicriteria_veto(criterion_weight, criterion_objectif, criterion_veto):
    n = data_df.shape[0]
    veto_table = np.full((n, n), None)
    for i in range(n):
        for j in range(n):
            print(f"{i}, {j}")
            veto_table[i][j] = get_veto(data_df.iloc[i], data_df.iloc[j], criterion_weight, criterion_objectif, criterion_veto) if i != j else None
    return veto_table

def calcul_for_all_profile(lstProfil, nameColumnWeight, nameColumnObjective, seuil=False, nameColumnSeuil="Seuils", veto=False, nameColumnVeto="Veto"):
    
    rsl_multicriteria_preference = {}
    rsl_veto = {}
    
    for profil in lstProfil:
        rsl_multicriteria_preference[profil] = multicriteria_preference(weights_df[weights_df[nameColumnWeight] == profil], objectives_df[objectives_df[nameColumnObjective] == profil], seuil, seuil_df[seuil_df[nameColumnSeuil] == profil])
        if veto:
            rsl_veto[profil] = multicriteria_veto(weights_df[weights_df[nameColumnWeight] == profil],objectives_df[objectives_df[nameColumnObjective] == profil], veto_df[veto_df[nameColumnVeto] == profil])
    return rsl_multicriteria_preference, rsl_veto
    

def outranking_method(matrix, items):
    outrank = []
    
    for i in range (len(matrix)):
        for j in range (len(matrix[i])):
            if float(matrix[i][j]) > 0.5: outrank.append([i, j])

    for i in range (len(outrank)):
        for j in range (len(outrank[i])): 
            outrank[i][j] = items[outrank[i][j]]
            
    return outrank
    
    
def getCore(outrank):
    items_core = []
    items_not_core = []
    
    for items in outrank:
        if items[1] not in items_not_core: items_not_core.append(items[1])
        
    for items in outrank:
        if items[0] not in items_not_core and items[0] not in items_core: items_core.append(items[0])
        
    return items_core
    
    
    
def main():
 
    """Avec les données de test de TD2"""
    # lstProfils = weights_df['Poids']
    # print(weights_df['Poids'])
    # # rslt = calcul_for_all_profile(lstProfils, 'Poids', 'Objectif', False)
    # rslt_with_seuil = calcul_for_all_profile(lstProfils, 'Poids', 'Objectif', True, 'Seuils', False, 'Veto')
    # # print(rslt)
    # print()
    # print(rslt_with_seuil[0]["Profil 1"])
    
    # # print(data_df["Candidats"])
    # outrank = outranking_method(rslt_with_seuil[0]["Profil 1"], data_df["Candidats"])
    # print(outrank)
    
    # core = getCore(outrank)
    # print(core)
    


    """Avec les données de Fat_Data.csv"""
    candidates = data_df['Country']
    criteria = data_df.columns[1:] # La première colonne est celle des candidats
    lstProfils = weights_df['Poids']
    
    # rslt = calcul_for_all_profile(lstProfils, 'Poids', 'Poids', False)
    rslt_with_seuil = calcul_for_all_profile(lstProfils, 'Poids', 'Poids', True, 'Seuils')
    
    
    outrank = {}
    core = {}
    for profil in lstProfils:
    
        outrank[profil] = outranking_method(rslt_with_seuil[0][profil], candidates)
        
        core[profil] = getCore(outrank[profil])
        
        df_outrank = pd.DataFrame(outrank[profil], columns=['start', 'end'])
        df_outrank.to_csv(f'Resultats/Electre/{profil}_outrank.csv', index=False)
        
        df_core = pd.DataFrame(core[profil], columns=['core'])
        df_core.to_csv(f'Resultats/Electre/{profil}_df_core.csv', index=False)

    
main()