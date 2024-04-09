import pandas as pd
import numpy as np

data_path = 'Donnees/Fat_Data.csv'
weights_path = 'Donnees/Fat_poids.csv'
objectives_path = 'Donnees/Fat_objective.csv'

data_df = pd.read_csv(data_path)
weights_df = pd.read_csv(weights_path)
objectives_df = pd.read_csv(objectives_path)
scores_df = pd.DataFrame(data_df['Country'])

# Fonction pour calculer les scores TOPSIS pour un profil donné
def calculate_topsis_scores(data, weights, objectives):
    weighted_data = data * weights
    A_plus = np.where(objectives == 'max', weighted_data.max(), weighted_data.min())
    A_minus = np.where(objectives == 'min', weighted_data.max(), weighted_data.min())
    distance_plus = np.sqrt(((weighted_data - A_plus) ** 2).sum(axis=1))
    distance_minus = np.sqrt(((weighted_data - A_minus) ** 2).sum(axis=1))
    scores = distance_minus / (distance_plus + distance_minus)
    return scores


for profile_id in range(len(weights_df)):
    profile_name = weights_df.iloc[profile_id, 0]
    weights = weights_df.iloc[profile_id, 1:].values.astype(float)
    objectives = objectives_df.iloc[profile_id, 1:].values
    
    
    objectives = np.array(['max' if obj.lower() == 'max' else 'min' for obj in objectives])
    scores = calculate_topsis_scores(data_df.iloc[:, 1:], weights, objectives)
    # print(scores)
    scores_df[f'Score_{profile_name}'] = scores

# Pour chaque profil, trier les candidats selon le score et afficher le classement
for profile_name in weights_df['Poids']:
    ranked_df = scores_df[['Country', f'Score_{profile_name}']].sort_values(by=f'Score_{profile_name}', ascending=False).reset_index(drop=True)
    base_path = 'Resultats/Topsis/'
    filename = f'{base_path}{profile_name}_Classement.csv'
    ranked_df.to_csv(filename, index=False, header=True)
    print(f'Les classements pour {profile_name} ont été enregistrés.')