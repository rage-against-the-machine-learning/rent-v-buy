import pandas as pd 
import numpy as np 


def high_level_inspect_df (df: pd.DataFrame): 
    display(df.head(3))
    display(df.info())
    display(df.describe().T)
    
    # Get categorical columns
    category_cols = [col for col in df.columns if df[col].dtype == 'O']
    
    for category in category_cols:
        print(category, f": {df[category].nunique()} unique values.")