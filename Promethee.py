import pandas as pd
import numpy as np

# Charger les fichiers CSV dans des DataFrames pandas
# data_path = 'Donnees/Test_Data.csv'
# weights_path = 'Donnees/Test_poids.csv'
# objectives_path = 'Donnees/Test_objective.csv'

data_path = 'Donnees/Fat_Data.csv'
weights_path = 'Donnees/Fat_poids.csv'
objectives_path = 'Donnees/Fat_objective.csv'


# Lecture des fichiers CSV
data_df = pd.read_csv(data_path)
weights_df = pd.read_csv(weights_path)
objectives_df = pd.read_csv(objectives_path)

# print(data_df)
# print(weights_df)
# print(objectives_df)

# Extraire les noms des candidats et des critères sans connaître les headers 
candidates = data_df.iloc[:, 0].values
criteria = data_df.columns[1:] # La première colonne est celle des candidats


# Fonction pour calculer le degré de préférence univarié
def preference_degree(x, y, weight, objective):
    if objective.lower() == 'max':
        return weight if x > y else 0
    elif objective.lower() == 'min':
        return weight if x < y else 0

# Fonction pour calculer le degré de préférence multicritère
def multicriteria_preference(data, weights, objectives):
    n = data.shape[0]
    preference_table = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            if i != j:
                preference_sum = 0
                for criterion in criteria:
                    preference_sum += preference_degree(
                        data.iloc[i][criterion],
                        data.iloc[j][criterion],
                        weights[criterion],
                        objectives[criterion]
                    )
                preference_table[i, j] = preference_sum
    return preference_table


# Initialiser un dictionnaire pour stocker les tables de préférences pour chaque profil et les classements des flux positifs et négatifs de chaque profil
preferences_profiles = {}
rankings_profiles = {}

# Itérer sur chaque profil
for profile_id in range(len(weights_df)):
    # Extraire les poids et objectifs pour le profil actuel
    weights = weights_df.iloc[profile_id, 1:].to_dict()
    objectives = objectives_df.iloc[profile_id, 1:].to_dict()

    # Calculer la table de préférences pour le profil actuel
    preference_table = multicriteria_preference(data_df, weights, objectives)

    # Transformer en DataFrame pour une meilleure visualisation
    preference_df = pd.DataFrame(preference_table, index=candidates, columns=candidates)
    preferences_profiles[f'Profil {profile_id + 1}'] = preference_df

    # Calculer les flux positifs et négatifs
    positive_flow = preference_df.sum(axis=1)
    negative_flow = preference_df.sum(axis=0)
    net_flow = positive_flow - negative_flow
    
    sorted_positive_flow = positive_flow.sort_values(ascending=False)
    sorted_negative_flow = negative_flow.sort_values(ascending=True)
    sorted_net_flow = net_flow.sort_values(ascending=False)

    # Stocker les classements dans le dictionnaire
    rankings_profiles[f'Profil {profile_id + 1}'] = {
        'Positive Flow Ranking': sorted_positive_flow,
        'Negative Flow Ranking': sorted_negative_flow,
        'Net Flow Ranking': sorted_net_flow
    }

# Afficher la table de préférences pour chaque profil
for profile, pref_df in preferences_profiles.items():
    print(f'Table de préférences pour {profile}:')
    print(pref_df)
    print('\n')

for profile, rankings in rankings_profiles.items():
    base_path = 'Resultats/Promethee_I/'
    
    # Nom des fichiers basé sur le profil
    positive_flow_filename = f'{base_path}{profile}_Classement_Flux_Positif.csv'
    negative_flow_filename = f'{base_path}{profile}_Classement_Flux_Négatif.csv'
    net_flow_filename = f'{base_path}{profile}_Classement_Flux_Net.csv'
    
    # Enregistrer les DataFrame dans des fichiers CSV
    rankings['Positive Flow Ranking'].to_csv(positive_flow_filename, index=True, header=["Score"], index_label="Country")
    rankings['Negative Flow Ranking'].to_csv(negative_flow_filename, index=True, header=["Score"], index_label="Country")
    rankings['Net Flow Ranking'].to_csv(net_flow_filename, index=True, header=["Score"], index_label="Country")

    print(f'Les classements pour {profile} ont été enregistrés.')