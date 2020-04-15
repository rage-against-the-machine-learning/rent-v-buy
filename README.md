# rent-v-buy

### USING THIS REPOSITORY:
1. [Downloading Data](https://github.com/rage-against-the-machine-learning/rent-v-buy/wiki/Getting-Started-in-Jupyter-Notebook)
2. [Setting up a VirtualEnv & Flask](https://github.com/rage-against-the-machine-learning/rent-v-buy/wiki/Setting-up-Virtual-Environment-&-Flask)

### REPOSITORY STRUCTURE

```
├── README.md          <- The top-level README for developers using this project.
├── Procfile           <- needed for heroku app to run
├── app.json           <- flask 
│
├── app                <- All files related to front-end app build
│   ├── static         
│   │   ├── css        <- main.css file in this directory
│   │   ├── js         <- JavaScript files for front-end build of choropleth etc.
│   │   │                 (GRADE: financialSliders.js and main.js)
│   │   ├── maps       <- topo.json files etc for choropleth build  
│   │   └── favicon.ico   
│   │
│   ├── templates      <- (GRADE).hmtl files for front-end build 
│   │
│   ├── __init__.py    
│   └── homeRoute.py   <- (GRADE) Script to generate outputs from our financial calculator for rent v. buy
│
├── data               <- Hidden folder in .gitignore / directory is created upon executing `/src/main.py`
│   ├── external       <- Data from third party sources (non-Zillow).
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump (from https://www.kaggle.com/zillow/zecon).
│
├── notebooks          <- Jupyter notebooks
│   └── Archive        <- Folder holding exploratory notebooks for methods/techniques not used & other scratch work
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials
│
├── reports            <- Project Deliverables
│   └── figures        <- Generated graphics and figures to be used in reporting
│   └── proposal       <- All proposal documents submitted on 2020-02-29
│   └── progress_rpt   <- All progress-report related documents submitted weekend of 2020-03-27
│   └── poster         <- All final report related files (due 2020-04-17)
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                <- (GRADE) Source code for entire data ETL & model pipeline (from download to model predictions).
    ├── README.md      <- Instructions on obtaining Kaggle API Key for data download to work
    ├── __init__.py    <- Makes src a Python module
    │
    ├── get_n_save_data.py     <- Script to download data from Kaggle.com & save to local machine
    ├── make_dataset.py        <- Script to do cursory cleaning in preparation for data pre-processing
    ├── california_only.py     <- Script to pare down scope of downloaded data to California
    ├── model.py               <- Script to generate time series forecast predictions for each zip code in California
    │
    ├── main.py                <- Script to EXCECUTE the entire Data Pipeline 
    └── helper.py              <- Script to aid in notebook explorations

```
