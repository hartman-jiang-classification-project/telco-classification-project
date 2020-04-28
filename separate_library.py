import pandas as pd
from env import host, user, password
import os.path
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler  

def url(db_name):
    from env import host, user, password
    url = f'mysql+pymysql://{user}:{password}@{host}/{db_name}'
    return url

def telco_data():
    query = '''
        SELECT *
        FROM customers
    '''
    df = pd.read_sql(query, url('telco_churn'))
    df.to_csv('telco_churn_1.csv')
    return df

#check if there is a csv file, if not run squl query
def acquire_data():
    if os.path.exists('telco_churn_1.csv'):
        df = pd.read_csv('telco_churn_1.csv', index_col=0)
    else:
        df = telco_data()
    return df
                         
def encoder(x):
    if x == 'Yes':
        return 1
    else:
        return 0

def prep_data():
    df = acquire_data()
    # drop unnecessary columns
    # total_charges are highly correlated with montly_charges, so it is redundant
    df = df.drop(columns = ['customer_id', 'gender','total_charges'])
    # drop tenure less than a month
    df = df[df.tenure != 0]
    # encode all the collumns with 'yes' and 'no' answers. 
    # those with no phone or no internet serive are all counted as no
    for i in df.drop(columns = ['tenure', 
                               'senior_citizen',
                               'monthly_charges', 
                               'internet_service_type_id',
                               'contract_type_id',
                               'payment_type_id'
                              ]).columns:
        df[i] = df[i].apply(encoder)
    return df

def split_data(df, size = .8):
    train, test = train_test_split(df, train_size = size, random_state=123)
    train, validate = train_test_split(train, train_size = size, random_state = 123)
    return train, validate, test
    
def scale_data(train, validate, test):
    scaler = MinMaxScaler()
    scaler.fit(train[["tenure", "monthly_charges"]])
    train[["tenure", "monthly_charges"]] = scaler.transform(train[["tenure", "monthly_charges"]])
    validate[["tenure", "monthly_charges"]] = scaler.transform(validate[["tenure", "monthly_charges"]])
    test[["tenure", "monthly_charges"]] = scaler.transform(test[["tenure", "monthly_charges"]])
    return scaler, train, validate, test                       