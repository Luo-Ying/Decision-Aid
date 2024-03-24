import pandas as pd
import numpy as np

# Charger les fichiers CSV dans des DataFrames pandas
# data_path = 'Test_Data.csv'
# weights_path = 'Test_poids.csv'
# objectives_path = 'Test_objective.csv'
# threshold_path = 'Test_seuils.csv'

data_path = 'Fat_Data.csv'
weights_path = 'Fat_poids.csv'
objectives_path = 'Fat_objective.csv'
threshold_path = 'Fat_seuils.csv'


# Lecture des fichiers CSV
data_df = pd.read_csv(data_path)
weights_df = pd.read_csv(weights_path)
objectives_df = pd.read_csv(objectives_path)
threshold_df = pd.read_csv(threshold_path)

# print(data_df)
# print(weights_df)
# print(objectives_df)

# Extraire les noms des candidats et des critères sans connaître les headers 
candidates = data_df.iloc[:, 0].values
criteria = data_df.columns[1:] # La première colonne est celle des candidats


# Fonction pour calculer le degré de préférence univarié
def preference_degree(x, y, weight, objective, threshold):
    if objective.lower() == 'max':
        if(x > y):
            absolute = abs(x-y)
            if(absolute >= threshold):
                return weight
            else:
                return ((absolute/threshold)*weight)
        else:
            return 0
    elif objective.lower() == 'min':
        if(x < y):
            absolute = abs(x-y)
            if(absolute >= threshold):
                return weight
            else:
                return ((absolute/threshold)*weight)
        else:
            return 0

# Fonction pour calculer le degré de préférence multicritère
def multicriteria_preference(data, weights, objectives,threshold):
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
                        objectives[criterion],
                        threshold[criterion]
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
    thresholds = threshold_df.iloc[profile_id, 1:].to_dict()

    # Calculer la table de préférences pour le profil actuel
    preference_table = multicriteria_preference(data_df, weights, objectives,thresholds)

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

# Afficher les classements pour chaque profil
for profile, rankings in rankings_profiles.items():
    print(f'Classement pour {profile}:')
    print('Classement Flux Positif:')
    print(rankings['Positive Flow Ranking'])
    print('Classement Flux Négatif:')
    print(rankings['Negative Flow Ranking'])
    print('Classement Flux Net:')
    print(rankings['Net Flow Ranking'])
    print('\n')
