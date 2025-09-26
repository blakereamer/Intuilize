# Intuilize-QB

## Project Overview
This project was built for Intuilize to help them group customers into different tiers using sales data, and then predict how customers might move between those tiers over time.

We used customer transaction data from 2022 to 2024 (full calendar years) to build both the segmentation and prediction models.

## What we did
1. Cleaned and explored the data
2. Engineered features from transaction patterns
3. Segmented customers using:
    K-Means
    Hierarchical Clustering
    Fuzzy C-Means
4. Predicted movement between tiers using:
    Markov Chains
    Monthly tracking

## File Structure
INTUILIZE-CLUSTER-COMMANDERS/
│── models
│── data
│   │── cleaned         # Cleaned and processed data
│   │── raw             # Original raw transaction data
│── noteboks            # Jupyter Notebooks for feature engineering and modeling
│── .gitignore
│── envirnomental.yml   # Conda environment setup

##  NoteBooks
- data_file_creation monthly.ipynb: Aggregates monthly data
- half_year_segments.ipynb: Analyzes data in half-year chunks
- feature_selection.ipynb: Automated feature selection
- fuzzy_cmeans.ipynb: Fuzzy C Means clustering
- hierarchical.ipynb: Hierarchical clustering
- Markov_Chain.ipynb: Predicts tier movement based on markov properties
- monthly_cluster_prediction.ipynd: Predicts tier movement based on one month prediction model

## Tools and Libraries used
1. Python
2. Jupyter
3. Pandas, Numpy, Sklearn, Scipy, Matplotlib, Seaborn
4. Scikit-fuzzy, Joblib, Tensorflow

## How to Run
* Step 1: git clone https://github.com/AndrewHjulberg/Intuilize-Cluster-Commanders.git
* Step 2: cd Intuilize-Cluster-Commanders
* Step 3: conda env create -f environmental.yml
* Step 4: conda activate intuilize-env
* Step 5: jupyter notebook