import numpy as np
import pandas as pd

import os.path
from os import path

from env import host, user, password

def get_db_url(dbname) -> str:
    url = 'mysql+pymysql://{}:{}@{}/{}'
    return url.format(user, password, host, dbname)

def get_telco_data():
    # query
    telco_query = """
    SELECT c.customer_id, c.gender, c.senior_citizen, c.partner, c.dependents, c.tenure, c.phone_service, c.multiple_lines, c.internet_service_type_id, i.internet_service_type, c.online_security, c.online_backup, c.device_protection, c.tech_support, c.streaming_tv, c.streaming_movies, c.contract_type_id, ct.contract_type, c.paperless_billing, c.payment_type_id, p.payment_type, c.monthly_charges, c.total_charges, c.churn
    FROM customers AS c
    JOIN internet_service_types AS i ON c.internet_service_type_id = i.internet_service_type_id
    JOIN contract_types AS ct ON c.contract_type_id = ct.contract_type_id
    JOIN payment_types AS p ON c.payment_type_id = p.payment_type_id;
    """

    # url
    telco_url = get_db_url("telco_churn")

    # create or read .csv file
    if path.exists("hartman-jiang_telco_data.csv"):
        df = pd.read_csv("hartman-jiang_telco_data.csv", index_col=0)
    else:
        df = pd.read_sql(telco_query, telco_url)
        df.to_csv("hartman-jiang_telco_data.csv")
    return df