# CSE 6242 Data Visualization and Analytics (DVA)

## Rent vs Buy 
- Semester: Spring 202020<br>
- Team: 245 : tufte-love

## Purpose
To provide an intuitive “look-ahead”  tool which helps users choose the most financially optimum option between  buying or renting a home.

## Team

## Application components
![rent vs buy applicatio architecture](media/app_arch.jpg)

## How to set up development environment

Set up virtual environment:
```
knail1s-MBP.home [rent-v-buy]$
knail1s-MBP.home [rent-v-buy]$ python3.7 -m venv venv
```

Activate virtual environment:
```
knail1s-MBP.home [rent-v-buy]$ . venv/bin/activate
(venv) knail1s-MBP.home [rent-v-buy]$
```

Install all requirements:
```
(venv) knail1s-MBP.home [rent-v-buy]$ pip install -r requirements.txt
```


Note: we purposely don't upload the virtual env directory to git. You are required to create a fresh venv/ locally.

## How to run (in dev environment)

```
(venv) knail1s-MBP.home [rent-v-buy]$ export FLASK_APP=rentvbuy.py
(venv) knail1s-MBP.home [rent-v-buy]$ flask run
 * Serving Flask app "dbtest.py"
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

```

For tips set up and run this in Pycharm, please check out this [link](https://www.youtube.com/watch?v=bZUokrYanFM&feature=youtu.be)


## Running system online (Primary approach)

- Database: We have hosted our databased on magenta.myhosted.com website which provides a paid mysql service
    - recommended systems to create and populate the database are mysql workbench from Oracle
- Front-end: for the front-end we are using free online services from Heroku.
    - we have integrated this github repo such that a change (merge, push etc) triggers an automated build in heroko and deploy to this end point.


## Running system offline (Backup approach)
- by simply updating `mydbconfig.py` you can specify the local data source
- we have hosted the database on a LAMP or MAMP server downloaded from bitnami, with exactly the same data and schema as the online version.
- for running the front-end, we do it directly through PyCharm, or from the CLI. the steps are listed above in the "How to run (in dev environment)" section.



## Bibliography
- https://blog.miguelgrinberg.com/post/setting-up-a-flask-application-in-pycharm
- https://devcenter.heroku.com/articles/github-integration
