# Download data from kaggle.com
print('............................')
print('............................')
print('1. Getting and saving the data.')
print('............................')
print('............................')
import get_n_save_data as get 

# Light data processing
print('............................')
print('............................')
print('2. Read in the data and cursory level cleaning.')
print('............................')
print('............................')
import make_dataset as make

# Pare down scope to just California
print('............................')
print('............................')
print('3. Scoping the data down to the Golden State--California.')
print('3. Preprocess data for modeling.')
print('............................')
print('............................')
import california_only as ca

# Model Preprocessing
print('............................')
print('............................')
print('4. Generate predictions for buy and rent values.')
print('............................')
print('............................')
import model

