import pandas as pd

if __name__ == '__main__': 

    print("Enter the path of your data: ")
    dataset_path = input()

    countryData = pd.read_table(dataset_path, sep=",")

    print(countryData.shape)
    print(countryData.dtypes)

    for col in countryData: 
    if(countryData[col].dtype != "object"): print(f'colonne: {col}, nbr_zéro: {(countryData[col] == 0).sum()}, min: {countryData[col].min()}, max: {countryData[col].max()}, médian: {countryData[col].median()}, moyenne: {countryData[col].mean()}')