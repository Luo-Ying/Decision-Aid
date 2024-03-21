# dataset = countryData, indexData = 'Country', dataWeight = poids

def weightedSum(dataset, indexData, dataWeight):
  
  rslt_allProfils = {}
  for n in range(len(dataWeight)):

    sumEachCandidate_profil = {}
    
    for numCandidate in range(dataset.shape[0]):
      sum = 0
      for col in dataset:
        if(col != indexData and col in dataWeight and col in dataset):
          sum += float(dataWeight.iloc[n][col].replace(",",".")) * dataset.iloc[numCandidate][col].item()
      sumEachCandidate_profil[dataset[indexData][numCandidate]] = sum

    rslt_allProfils['profil_'+str(n+1)] = {}
    rslt_allProfils['profil_'+str(n+1)]['asc'] = sorted(sumEachCandidate_profil.items(), key=lambda x:x[1])
    rslt_allProfils['profil_'+str(n+1)]['desc'] = sorted(sumEachCandidate_profil.items(), key=lambda x:x[1], reverse=True)
    
    return rslt_allProfils
