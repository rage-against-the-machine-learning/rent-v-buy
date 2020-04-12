# rent-v-buy

### USING THIS REPOSITORY:
1. [Downloading Data](https://github.com/rage-against-the-machine-learning/rent-v-buy/wiki/Getting-Started-in-Jupyter-Notebook)
2. [Setting up a VirtualEnv & Flask](https://github.com/rage-against-the-machine-learning/rent-v-buy/wiki/Setting-up-Virtual-Environment-&-Flask)

### REPOSITORY STRUCTURE

```
├── README.md          <- The top-level README for developers using this project.
│
├── data               <- Hidden folder in .gitignore 
│   ├── external       <- Data from third party sources (non-Zillow).
│   ├── interim        <- Intermediate data that has been transformed.
│   ├── processed      <- The final, canonical data sets for modeling.
│   └── raw            <- The original, immutable data dump (from https://www.kaggle.com/zillow/zecon).
│
├── models             <- Trained and serialized models, model predictions, or model summaries
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials, project deliverables.
│
├── reports            <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in reporting
│   └── proposal       <- All proposal documents submitted on 2020-02-29
│   └── progress_rpt   <- All progress-report related documents (due 2020-03-27)
│   └── final_poster   <- All poster presentation related files (due 2020-04-17)
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
├── setup.py           <- Make this project pip installable with `pip install -e`
│
└── src                <- Source code for use in this project.
    ├── __init__.py    <- Makes src a Python module
    │
    ├── make_dataset.py     <- Scripts to download or generate data
    ├── build_features.py   <- Scripts to turn raw data into features for modeling
    ├── predict_model.py    <- Scripts to make predictions (run after train_model.py)
    ├── train_model.py      <- Scripts to train models 
    │
    └── visualize.py        <- Scripts to create exploratory and results oriented visualizations
```
