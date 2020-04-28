# Telco Classification Project

## Purpose
This repository holds all resources used in the attainment of the goals established for the Telco Classification Project.

## Research Question: Why are our customers churning?

## Goals
- Determine the drivers of churn
- Create a model to predict churn for each customer
- 

## Need to Haves
- A report in the form of a jupyter notebook
- A .csv file that predicts churn for each customer using our best model
- Python scripts for replicability
    - acquire.py
    - prepare.py
    - model.py
- A presentation in the form of [Google slides](https://docs.google.com/presentation/d/1hjDQED2eNU-k_RryLbJG70J1u-wI8Lm08Jd-mGUlmBM/edit?usp=sharing)


# Nice to Haves




---

- Role playing: What are reason's for getting a new ISP?
    - Alec: Price (monthly charges), better pricing for additional lines on contract (family plan), security (lower priority), online billing
    - Allen: Loyalty discount (calculated field: rate of decrease of monthly charges over time), quality of service (reliablity), service type (highly correlated with price?) , service offerings quality (encode services and sum by row)

- Initial model features:
    - multiple_lines
    - contract_type
    - tenure
    - monthly_charges
    - churn
    - internet_service_type

- Lower priority features (in addition to above):
    - online_security
    - 

- The number of lines on a contract is independent of monthly charges

- Tenure is independent of churn 

- Hypothesis:
    - The rate of increase of monthly charges over time is independent of churn

- Threshold for classification model == price for specific service where the likelihood of churn increases once price exceeds that point
    - What price for each service?

- Is there a difference in churn rate between a month-to-month contract type with a tenure of 12 months and a 1-year contract type?
    - Create subgroups:
        1. At least 12 months with no contract (month-to-month)
        2. 1-year contracts
    - Null Hypothesis: (t-test: one continuous var {churn rate} for each subgroup)
        - The churn rate between month-to-month customers with a tenure of 12 months and 1-year contract customers is the same
    - Alt. Hypothesis:
        - The churn rate between month-to-month customers with a tenure of 12 months and 1-year contract customers is different
            - Allen's intuition is that 1-year contracts have a lower churn rate, and Alec agrees.
