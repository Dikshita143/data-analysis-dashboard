import pandas as pd
import numpy as np

def clean_data(df):
    """Basic data cleaning: drop duplicates, handle missing values."""
    df = df.copy()
    
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    
    # Handle missing values
    for col in df.columns:
        if df[col].dtype == 'object':
            df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else "Unknown", inplace=True)
        else:
            df[col].fillna(df[col].mean(), inplace=True)
            
    return df

def detect_outliers(df, column):
    """Detect outliers using IQR method."""
    if column not in df.columns or not np.issubdtype(df[column].dtype, np.number):
        return pd.Series([False] * len(df))
    
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    return (df[column] < lower_bound) | (df[column] > upper_bound)

def validate_dataset(df, expected_columns):
    """Check if the dataframe has all expected columns."""
    missing = [col for col in expected_columns if col not in df.columns]
    return len(missing) == 0, missing
