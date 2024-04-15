import pandas as pd

# dataset = countryData, indexData = 'Country', dataWeight = poids

def weightedSum(dataset, indexData, dataWeight):
  
  rslt_allProfils = {}
  for n in range(len(dataWeight)):

    sumEachCandidate_profil = {}
    
    for numCandidate in range(dataset.shape[0]):
      sum = 0
      for col in dataset:
        if(col != indexData and col in dataWeight and col in dataset):
          sum += float(dataWeight.iloc[n][col]) * dataset.iloc[numCandidate][col].item()
      sumEachCandidate_profil[dataset[indexData][numCandidate]] = sum

    rslt_allProfils['profil '+str(n+1)] = {}
    rslt_allProfils['profil '+str(n+1)]['asc'] = sorted(sumEachCandidate_profil.items(), key=lambda x:x[1])
    rslt_allProfils['profil '+str(n+1)]['desc'] = sorted(sumEachCandidate_profil.items(), key=lambda x:x[1], reverse=True)
    
  return rslt_allProfils


def main():
  dataset_path = 'Donnees/Fat_Data.csv'
  weight_path = 'Donnees/Fat_poids.csv'

  indexData = 'Country'
  countryData = pd.read_table(dataset_path, sep=",")
  weightData = pd.read_table(weight_path, sep=",")

  rslt_allProfils = weightedSum(countryData, indexData, weightData)
  for profile in rslt_allProfils:
    df = pd.DataFrame(rslt_allProfils[profile]["desc"], columns=['Country', 'Value'])
    df.to_csv(f'Resultats/WeightedSum/{profile}_Classement.csv', index=False)
  
  
main()