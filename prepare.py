import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split

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

def calc_tenure_years(tenure, df, rounding=False):
    if rounding:
        df["tenure_years"] = np.round(tenure / 12)
        return df
    else:
        df["tenure_years"] = np.round(tenure // 12)
        return df

def prep_telco(df):
    
    # clean total_charges
    df = clean_total_charges(df)
    
    # removing unnecessary variables
    # df.drop(columns=[], inplace=True)
    
    # splitting df into train and test
    train, test = train_test_split(df, random_state=56, train_size=.8)
    
    # splitting train into train and validate
    train, validate = train_test_split(train, random_state=56, train_size=.75)

    # calculating tenure years rounded
    train = calc_tenure_years(train["tenure"], train, rounding=True)
    
    return train, validate, test