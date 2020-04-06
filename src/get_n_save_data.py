'''
get_n_save_data.py

This file serves to: 
1. establish the ./data/ directory in the repository project directory 
The data files were NOT pushed into the git repository as they are too large, and therefore the ./data/ directory
remains as an untracked directory in the `.gitignore` file.

2. get data from kaggle.com's zillow/zecon URL: https://www.kaggle.com/zillow/zecon
It utilizes the Kaggle API to retreive the data, and unzips the zipfiles in a specified directory in the repo
'''

import os 
import sys 
import pathlib
sys.path.append(str(pathlib.Path().absolute().parent))

import subprocess
from zipfile import ZipFile

# 1. SETTING UP THE REPO DATA FILE DIRECTORY
# 1A. Check to see if the 'data/' folder exists in the repo; create if it doesn't exist
data_dir = str(pathlib.Path().absolute().parent) + '/data/'

if not os.path.isdir(data_dir):
    os.mkdir(data_dir)
if not os.path.isdir(data_dir + 'raw/'):
    os.mkdir(data_dir + 'raw/')
if not os.path.isdir(data_dir + 'interim/'):
    os.mkdir(data_dir + 'interim/')
if not os.path.isdir(data_dir + 'processed/'):
    os.mkdir(data_dir + 'processed/')
if not os.path.isdir(data_dir + 'predictions/'):
    os.mkdir(data_dir + 'predictions/')

# 2. Download the files from Kaggle.com
# AFTER setting up the kaggle.com API key per the README.md
if 'kaggle.json' not in os.listdir(str(pathlib.Path().home()) + '/.kaggle/'): 
    print('Check that you have setup your Kaggle API key and the key!. Follow the instructions on the README.md for Authentication setup.')

if 'zecon.zip' not in os.listdir('../data/raw'):
    print('Preview the data from kaggle.com: ' + '\n')
    list_files = subprocess.run([
        'kaggle',
        'datasets',  
        'list',
        '-s', 
        'zecon'
    ])
    print("The exit code was: %d" % list_files.returncode)

    # Change working directory in ./data/raw/
    # Then Download the zipfile from kaggle
    print('Download the data from kaggle.com: ' + '\n')
    os.chdir('../data/raw/')
    download_files = subprocess.run([
        'kaggle',
        'datasets',
        'download',
        '-d', 
        'zillow/zecon'
    ])
    print("The exit code was: %d" % download_files.returncode)


# 3 Unzip the zipfile that was downloaded
files = os.listdir(f'{data_dir}raw/')

for f in files: 
    if '.zip' in f:
        with ZipFile(f'{data_dir}raw/{f}', 'r') as a_zip:
            a_zip.extractall(f'{data_dir}raw/{f[:-4]}')
        
    else:
        pass