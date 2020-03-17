import pandas as pd 
import numpy as np  
from zipfile import ZipFile

import pathlib
import sys
import os 
sys.path.append(str(pathlib.Path().absolute().parent))


# Unzip the files and read the csvs
csv_dfs = {}

for filename in sorted(os.listdir('../data/raw/')):
    if '.csv.zip' in filename: 
        with ZipFile(f'../data/raw/{filename}', 'r') as a_zip:
            a_zip.extractall(f'../data/raw/unzipped/{filename[:-4]}')
            
    elif '.csv' in filename:
        csv_dfs[filename] = pd.read_csv(f'../data/raw/{filename}')
        
# Read in the extracted zip files       
for filename in sorted(os.listdir('../data/raw/unzipped/')):
    csv_dfs[filename[:-4]] = (pd.read_csv(f'../data/raw/unzipped/{filename}/{filename}', engine='python'))

