import pandas as pd
from env import url
import os.path

def telco_data():
    query = '''
        SELECT *
        FROM customers
    '''
    df = pd.read_sql(query, url('telco_churn'))
    df.to_csv('telco_churn.csv')
    return df

#check if there is a csv file, if not run squl query
def acquire_data():
    if os.path.exists('telco_churn.csv'):
        df = pd.read_csv('telco_churn.csv',  index_col=0)
    else:
        df = telco_data()
    return df