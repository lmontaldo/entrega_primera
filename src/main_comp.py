import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import DATA_BASE_PATH
from config import image_path
from utils import data_loader 
#from utils.ADF_tests import adf_test 
import sqlite3
import sys
import numbers
import time
import math
import pandas as pd
import numpy as np
import datetime as dt
from sklearn.preprocessing import StandardScaler
from utils.eda_decomposition import decompose_dataframe, perform_seasonal_adjustment
from utils.unitroot import *
from utils.pruebas_KPSS import *
from utils.validators import *
import plotly.graph_objects as go
import dash
from dash import dcc
from dash import html
from statsmodels.tsa.seasonal import seasonal_decompose
from plotly.subplots import make_subplots
from statsmodels.tsa.stattools import acf, pacf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from arch.unitroot import ADF
import warnings
from statsmodels.tools.sm_exceptions import InterpolationWarning
import seaborn as sns
import matplotlib.pyplot as plt

warnings.simplefilter('ignore', InterpolationWarning)
#############################################
# Retrieve the DataFrames from data_loader
#############################################
# Retrieve the DataFrames from data_loader
#df_clases, df_univariado, df_fmi, df_clases_filter = data_loader.get_data(path)
tables_list= ['Datosipc', 'CLASES_IPC','IPC_gral']
df_dict = data_loader.get_data(DATA_BASE_PATH, tables_list)
# to df
df=df_dict['CLASES_IPC']
df_raw=df_dict['Datosipc']

############################################
# COMPONENTES IPC
############################################
df['ymd'] = pd.to_datetime(df['ymd']).dt.normalize()

#
is_valid, message = validate_df(df)
print(is_valid, message)
#
filtered_df = df_raw[df_raw['c_codigo'].astype(str).str.len() == 3]
div_df=filtered_df.iloc[:, :3]
prefixes = div_df['c_codigo'].tolist()
# Create a dictionary of DataFrames
dfs = {prefix: df[df.columns[df.columns.str.startswith(prefix) | df.columns.str.startswith('ymd')]] for prefix in prefixes}

def create_dfs(df, prefixes):
    prefixes = div_df['c_codigo'].tolist()
    return {prefix: df[df.columns[df.columns.str.startswith(prefix) | df.columns.str.startswith('ymd')]] for prefix in prefixes}

dfs = create_dfs(df, prefixes)
#
# Create a line plot for each group
for prefix, df in dfs.items():
    plt.figure(figsize=(10, 6))
    sns.lineplot(data=df)
    plt.title(f'Group: {prefix}')
    plt.xlabel('ymd')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
    
    
# Create subplots for each series in each group
for prefix, df in dfs.items():
    n = df.shape[1] - 1  # number of series (excluding 'ymd')
    fig, axs = plt.subplots(n, 1, figsize=(10, 6*n))
    
    for i, col in enumerate(df.columns):
        if col != 'ymd':
            sns.lineplot(x='ymd', y=col, data=df, ax=axs[i])
            axs[i].set_title(f'Series: {col}')
            axs[i].set_xlabel('ymd')
            axs[i].set_xticks(rotation=45)
    
    plt.tight_layout()
    plt.suptitle(f'Group: {prefix}', y=1.02, fontsize=16)
    plt.show()    

