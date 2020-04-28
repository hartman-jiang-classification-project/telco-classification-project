import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import acquire as ac
import prepare as pr

import warnings
warnings.filterwarnings("ignore")


def model_and_prediction():
    # acquire data
    df = ac.get_telco_data()
    #  prepare data
    encoder, train, validate, test = pr.prep_telco(df)
    scaler, train, validate, test = pr.min_max_scaler(train, validate, test)
    # select desired features
    X = ['tenure','monthly_charges','contract_type_id','senior_citizen']
    y = ['churn']
    X_train = train[X]
    y_train = train[y]
    X_test = test[X]
    y_test = test[y]
    #scale the whole dataset
    df[["tenure", "monthly_charges"]] = scaler.transform(df[["tenure", "monthly_charges"]])
    # create a model trained from train dataset
    rf = RandomForestClassifier(bootstrap=True, 
                            class_weight=None, 
                            criterion='gini',
                            min_samples_leaf=3,
                            n_estimators=100,
                            max_depth=20, 
                            random_state=123)
    rf.fit(X_train, y_train)
    # Make prediction of each customer
    df['predicted']= rf.predict(df[['tenure',
                                    'monthly_charges',
                                    'contract_type_id',
                                    'senior_citizen']])
    #Show prediction of each customer
    df["probability"]= rf.predict_proba(df[['tenure',
                    'monthly_charges',
                    'contract_type_id',
                    'senior_citizen']])[:, 1]
    # encode int to string
    df['predicted'] = df.predicted.apply(lambda x: 'Yes' if x == 1 else 'No')
    # Select columns for csv file
    df = df.rename(columns = {'churn': 'actual'})
    df = df[['customer_id','actual','predicted', "probability"]]
    # write dataframe to a csv file
    df.to_csv('prediction.csv')