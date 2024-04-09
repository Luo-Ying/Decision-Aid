import pandas as pd

# Charger les données pour obtenir les valeurs maximales et minimales pour chaque critère
data_df = pd.read_csv("Donnees/Fat_Data.csv", index_col=0)
data_weight = pd.read_csv("Donnees/Fat_poids.csv", index_col=0)

# Calculer la plage des valeurs pour chaque critère
range_values = (data_df.median()).round(5)
# Profil 1 (plus grande importance sur les fruits et légumes) :
# les seuils doivent être faibles pour les critères relatifs aux fruits et légumes pour que même de petites différences
# puissent être significatives, et plus élevés pour les catégories de viande pour minimiser leur impact.

# Profil 2 (équilibré) : les seuils doivent être relativement uniformes pour tous les critères

# Profil 3 (plus de poids pour la viande) : les seuils doivent être plus faibles pour les critères relatifs à la
# viande pour mettre en évidence même les petites différences, et plus élevés pour les fruits et légumes pour réduire
# leur impact relatif.

# Définir les seuils en pourcentage pour chaque profil
seuil_profil1 = 0.05
seuil_profil2 = 0.10
seuil_profil3 = 0.05
default_seuil = 0.15

# Mapping des critères par catégorie (à adapter avec les vrais noms des critères)
categorie_mapping = {
    "Fruits": ["Fruits - Excluding Wine", "Treenuts"],
    "Legumes": [
        "Vegetables",
        "Starchy Roots",
        "Pulses",
        "Olives",
        "Oilcrops",
        "Cereals - Excluding Beer",
        "Spices",
        "Sugar Crops",
        "Vegetable Oils",
        "Vegetal Products",
    ],
    "Viande": [
        "Meat",
        "Offals",
        "Animal Products",
        "Fish, Seafood",
        "Animal fats",
        "Eggs",
    ],
}

# Définir les seuils en pourcentage pour chaque profil en fonction de enverser la proportion de leur préférence (poids)
seuil_profil1_favoris = data_weight.min(axis=1)["Profil 1"]
seuil_profil1_non_favoris = data_weight.max(axis=1)["Profil 1"]
seuil_profil3_favoris = data_weight.min(axis=1)["Profil 3"]
seuil_profil3_non_favoris = data_weight.max(axis=1)["Profil 3"]
default_seuil = data_weight.mean(axis=1)["Profil 2"]


# Fonction pour déterminer le seuil pour un critère donné
def determine_seuil(critere, profil):
    for categorie, criteres in categorie_mapping.items():
        if critere in criteres:
            if profil == 1 and categorie in ["Fruits", "Legumes"]:
                return range_values[critere] * seuil_profil1_favoris
            elif profil == 1 and categorie == "Viande":
                return range_values[critere] * seuil_profil1_non_favoris
            elif profil == 3 and categorie == "Viande":
                return range_values[critere] * seuil_profil3
            elif profil == 3 and categorie == ["Fruits", "Legumes"]:
                return range_values[critere] * seuil_profil3
    return range_values[critere] * default_seuil


# Calculer les seuils pour chaque profil et critère
seuils_profil1 = {
    critere: determine_seuil(critere, 1) for critere in data_df.columns[0:]
}
seuils_profil2 = {
    critere: determine_seuil(critere, 2) for critere in data_df.columns[0:]
}
seuils_profil3 = {
    critere: determine_seuil(critere, 3) for critere in data_df.columns[0:]
}

seuils_df = (
    pd.DataFrame(
        {
            "Profil 1": seuils_profil1,
            "Profil 2": seuils_profil2,
            "Profil 3": seuils_profil3,
        }
    )
    .round(5)
    .T
)
seuils_df.to_csv("Fat_seuils.csv", index_label="Seuils")
