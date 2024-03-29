# rent-v-buy

## OBJECTIVE
The purpose of our app is to provide an intuitive "look-ahead" tool that helps users choose the financially optimal option between renting an apartment and buying a home in the state of California. 

### Team 235: Tufte-Love
* Omer Ansari
* Richard Levine
* Felipe Lopez
* Skye Sheffield
* Sylvia Tran

### APPLICATION ARCHITECTURE: 
![](https://github.com/rage-against-the-machine-learning/rent-v-buy/blob/master/reports/figures/app_arch.png)

### I. USING THIS REPOSITORY:
### [Demo Video Link](https://youtu.be/Lw3U7w5Ds6E)
> These instructions assume the user has a Linux or Mac OS. <br>
> For Windows, different instructions are required. <br>
> If you're not inclined to build the app, [CLICK HERE](https://rentvbuy.herokuapp.com/) : https://rentvbuy.herokuapp.com/

#### IA. Setting up a VirtualEnv & Flask
1. Download the repository to your local machine.
2. Change directories into the repository project folder
3. Set up virtual environment:
    ```
    [rent-v-buy]$
    [rent-v-buy]$ python3.7 -m venv venv
    ```
4. Activate virtual environment:
    ```
    [rent-v-buy]$ . venv/bin/activate
    (venv) [rent-v-buy]$
    ```
5. Install all requirements:
    ```
    (venv) [rent-v-buy]$ pip install -r requirements.txt
    ```
Note: we intentionally did not upload the virtual env directory to git. You are required to create a fresh venv/ locally.

#### IB. How to run (in dev environment)
```
(venv) [rent-v-buy]$ export FLASK_APP=rentvbuy.py
(venv) [rent-v-buy]$ flask run
 * Serving Flask app "dbtest.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
For tips set up and run this in Pycharm, please [watch this video](https://www.youtube.com/watch?v=bZUokrYanFM&feature=youtu.be).

#### Bibliography
- https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-pycharm
- https://devcenter.heroku.com/articles/github-integration


### II. [Downloading Data](https://github.com/rage-against-the-machine-learning/rent-v-buy/tree/master/src/)<br>
It is optional to run the entire data pipeline from data download to prediction generation. This is **not required in order to launch the app**. The outputs from the predictions generated by time series forecasting is available in the `app/maps/` directory as `UI_output.json`.

### REPOSITORY STRUCTURE:

```
├── README.md          <- The top-level README for developers using this project.
├── Procfile           <- needed for heroku app to run
├── financialAnalysis.py  <- Python script with formulas to calculate rent-v-buy outputs to surface to front-end
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
