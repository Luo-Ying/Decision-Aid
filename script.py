import pandas as pd

if __name__ == '__main__': 

    print("Enter the path of your data: ")
    dataset_path = input()

    countryData = pd.read_table(dataset_path, sep=",")

    print(countryData.shape)
    print(countryData.dtypes)

    for col in countryData: 
        if(countryData[col].dtype != "object"): print('<@\\textcolor{cyan}{'+ col + 's}@> => nbr_zéro: <@\\textcolor{blue}{' + str((countryData[col] == 0).sum()) + '}@> , min: <@\\textcolor{blue}{' + str(countryData[col].min()) + '}@>, max: <@\\textcolor{blue}{' + str(countryData[col].max()) + '}@>, median: <@\\textcolor{blue}{' + str(countryData[col].median()) + '}@>, mean: <@\\textcolor{blue}{' + str(countryData[col].mean()) + '}@>')