"""
This code saves the optimal weights combination and the correlation matrix in an .xlsx file

@author: Enrico Pasquariello
@mail: enrico.pasquariello94@gmail.com   
"""

import os
import pandas as pd

def excel(df_weights:pd.DataFrame,
          df_corr:pd.DataFrame):
    
    if not os.path.exists(os.path.abspath(r'output')):
        os.makedirs('output')
    
    with pd.ExcelWriter\
        (os.path.abspath(r'output'+'\Efficient_Frontier.xlsx')) as writer:
        df_weights.to_excel(writer,sheet_name='Weights')
        df_corr.to_excel(writer,sheet_name='Corr_matrix')
    
    return
