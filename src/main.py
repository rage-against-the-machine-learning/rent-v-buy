#run our model
import pandas as pd
import make_zip_pair

data = pd.read_csv('../data/raw/unzipped/Zip_time_series.csv')
print(make_zip_pair.make_main(data,91770))