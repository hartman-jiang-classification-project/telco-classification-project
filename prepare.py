import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler, MinMaxScaler

def clean_total_charges(df):
    """
    This functions takes in the telco DataFrame, and returns a DataFrame where NaN values have been dropped and
    the total_charges variable is converted to a float type.
    """
    # total_charges is an object, needs to be a float. start by removing leading and trailing whitespace.
    df.total_charges = df.total_charges.str.strip()
    # replace blank strings with NaN value inplace of the existing DataFrame
    df.replace("", np.nan, inplace=True)
    # drop rows with NaN values inplace of the existing DataFrame
    df.dropna(inplace=True)
    # assigning the total charges field as a float
    df["total_charges"] = df.total_charges.astype("float")
    # resetting index inplace of existing DataFrame
    df.reset_index(inplace=True)
    # drop index column
    df.drop(columns="index", inplace=True)
    return df

def consolidate_columns(df):
    df["phone_service_type"] = np.where(df.multiple_lines == "No", "Single line", np.where(df.multiple_lines == "Yes", "Multiple lines", "None"))
    df["family"] = np.where((df.partner == "Yes") & (df.dependents == "Yes"), "Partner and dependents", np.where((df.partner == "Yes") & (df.dependents == "No"), "Partner", np.where((df.partner == "No") & (df.dependents == "Yes"), "Dependents", "Single")))
    df["streaming"] = np.where((df.streaming_tv == "Yes") & (df.streaming_movies == "Yes"), "TV and movies", np.where((df.streaming_tv == "Yes") & (df.streaming_movies == "No"), "TV", np.where((df.streaming_tv == "No") & (df.streaming_movies == "Yes"), "Movies", np.where((df.streaming_tv == "No") & (df.streaming_movies == "No"), "None", "No internet service"))))
    df["online_protection"] = np.where((df.online_security == "Yes") & (df.online_backup == "Yes"), "Security and backup", np.where((df.online_security == "Yes") & (df.online_backup == "No"), "Security", np.where((df.online_security == "No") & (df.online_backup == "Yes"), "Backup", np.where((df.online_security == "No") & (df.online_backup == "No"), "None", "No internet service"))))
    df.drop(columns=["phone_service", "multiple_lines", "partner", "dependents", "streaming_tv", "streaming_movies", "online_security", "online_backup"], inplace=True)
    return df

def calc_tenure_years(tenure, df, rounding=False):
    if rounding:
        df["tenure_years"] = np.round(tenure / 12)
        return df
    else:
        df["tenure_years"] = np.round(tenure // 12)
        return df

def encode_churn(train, validate, test):
    encoder = LabelEncoder()
    encoder.fit(train[["churn"]])
    train["churn"] = encoder.transform(train[["churn"]])
    validate["churn"] = encoder.transform(validate[["churn"]])
    test["churn"] = encoder.transform(test[["churn"]])
    return encoder, train, validate, test

def min_max_scaler(train, validate, test):
    scaler = MinMaxScaler()
    scaler.fit(train[["tenure", "monthly_charges"]])
    train[["tenure", "monthly_charges"]] = scaler.transform(train[["tenure", "monthly_charges"]])
    validate[["tenure", "monthly_charges"]] = scaler.transform(validate[["tenure", "monthly_charges"]])
    test[["tenure", "monthly_charges"]] = scaler.transform(test[["tenure", "monthly_charges"]])
    return scaler, train, validate, test

def prep_telco(df):
    
    # clean total_charges
    df = clean_total_charges(df)

    # consolidate columns
    df = consolidate_columns(df)
    
    # splitting df into train and test
    train, test = train_test_split(df, random_state=56, train_size=.8, stratify=df.churn)
    
    # splitting train into train and validate
    train, validate = train_test_split(train, random_state=56, train_size=.75, stratify=train.churn)

    # calculating tenure years rounded
    train = calc_tenure_years(train["tenure"], train, rounding=True)

    # encode churn
    encoder, train, validate, test = encode_churn(train, validate, test)
    
    return encoder, train, validate, test