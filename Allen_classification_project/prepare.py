import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from acquire import acquire_data

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
    