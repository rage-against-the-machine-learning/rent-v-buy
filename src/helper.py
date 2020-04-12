import pandas as pd 
import numpy as np 
from datetime import datetime
from dateutil import relativedelta


def high_level_inspect_df (df: pd.DataFrame): 
    print(df.head(3))
    print(df.info())
    print(df.describe().T)
    
    # Get categorical columns
    category_cols = [col for col in df.columns if df[col].dtype == 'O']
    
    for category in category_cols:
        print(category, f": {df[category].nunique()} unique values.")


def months_til_today (df:pd.DataFrame) -> int:
    assert 'ds' in df.columns, "'ds' column needs to be in the input DataFrame"

    today = datetime.now()
    r = relativedelta.relativedelta(today, df.ds.max())
    
    years = r.years
    months = r.months
    return int((years * 12) + months)