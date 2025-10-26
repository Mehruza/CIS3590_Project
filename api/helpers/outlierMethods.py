from scipy import stats as scipyStats
import numpy as np


def iqr(df,column, k):
        Q1 = df[column].quantile(0.25)
        Q3 = df[column].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - k * IQR
        upper_bound = Q3 + k * IQR
        
        outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
        return outliers
    
def zScore(df, column, zTreshold):
    z_scores = np.abs(np.asarray(scipyStats.zscore(df[column], nan_policy='omit')))
    outliers = df[z_scores > zTreshold]
    return outliers

__all__ = ['iqr', 'zScore']