# -*- coding: utf-8 -*-
### Input: dataframe 
### Output: plot and % missing column 
### ignore n_largest or top ... variables
def percent_missings(df, n_largest=None):
    missings = df.isna().sum() * 100 / len(df)
    df = pd.DataFrame([missings.values], columns=missings.index.to_list())
    if n_largest is not None:
       sorted_missings = df.squeeze().sort_values(ascending=False).nlargest(n_largest)
       df.squeeze().sort_values(ascending=False).nlargest(n_largest).plot(kind="barh")
    else:
       sorted_missings = df.squeeze().sort_values(ascending=False).nlargest(10)
       df.squeeze().sort_values(ascending=False).nlargest(10).plot(kind="barh")
    return sorted_missings

    
percent_missings(X)
