import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler

def detect_column_types(df):
    """Detect numerical, categorical, datetime, and text columns."""
    types = {}
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            types[col] = 'Datetime'
        elif pd.api.types.is_numeric_dtype(df[col]):
            types[col] = 'Numerical'
        elif df[col].nunique() < 20 or df[col].nunique() < len(df) * 0.5:
            types[col] = 'Categorical'
        else:
            types[col] = 'Text'
    return types

def get_dataset_health_score(df):
    """Calculate health score based on missing, duplicate, and outlier percentages."""
    try:
        total_cells = np.prod(df.shape)
        if total_cells == 0: return 0
        missing_pct = (df.isnull().sum().sum() / total_cells) * 100
        
        duplicate_pct = (df.duplicated().sum() / len(df)) * 100
        
        num_cols = df.select_dtypes(include=[np.number]).columns
        outlier_total = 0
        for col in num_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            outlier_total += len(outliers)
            
        outlier_pct = (outlier_total / total_cells) * 100
        
        score = 100 - (missing_pct * 0.4) - (duplicate_pct * 0.3) - (outlier_pct * 0.3)
        return max(0, min(100, score))
    except Exception:
        return 0

def handle_missing_values(df, columns, method, custom_value=None):
    """Handle missing values for selected columns using specified method."""
    df_copy = df.copy()
    try:
        if method == "Drop rows with nulls":
            df_copy = df_copy.dropna(subset=columns)
            msg = f"Dropped rows with nulls in {len(columns)} columns"
        elif method == "Fill with Mean":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df_copy[col]):
                    df_copy[col] = df_copy[col].fillna(df_copy[col].mean())
            msg = f"Filled missing values with Mean in {len(columns)} columns"
        elif method == "Fill with Median":
            for col in columns:
                if pd.api.types.is_numeric_dtype(df_copy[col]):
                    df_copy[col] = df_copy[col].fillna(df_copy[col].median())
            msg = f"Filled missing values with Median in {len(columns)} columns"
        elif method == "Fill with Mode":
            for col in columns:
                df_copy[col] = df_copy[col].fillna(df_copy[col].mode()[0])
            msg = f"Filled missing values with Mode in {len(columns)} columns"
        elif method == "Fill with Custom Value":
            for col in columns:
                df_copy[col] = df_copy[col].fillna(custom_value)
            msg = f"Filled missing values with Custom Value '{custom_value}' in {len(columns)} columns"
        else:
            msg = "No specific method selected."
        return df_copy, msg
    except Exception as e:
        return df, f"Error handling missing values: {str(e)}"

def remove_duplicates(df):
    """Remove duplicate rows from dataframe."""
    initial_len = len(df)
    try:
        df_copy = df.drop_duplicates()
        removed = initial_len - len(df_copy)
        msg = f"Removed {removed} duplicate rows. New shape: {df_copy.shape[0]} × {df_copy.shape[1]}"
        return df_copy, msg
    except Exception as e:
         return df, f"Error removing duplicates: {str(e)}"

def encode_categorical(df, columns, method):
    """Encode selected categorical columns."""
    df_copy = df.copy()
    try:
        if method == "Label Encoding":
            le = LabelEncoder()
            for col in columns:
                # Handle possible NaN values correctly before label encoding
                df_copy[col] = df_copy[col].astype(str)
                df_copy[col] = le.fit_transform(df_copy[col])
            msg = f"Applied Label Encoding to {len(columns)} columns"
        elif method == "One-Hot Encoding":
            df_copy = pd.get_dummies(df_copy, columns=columns, drop_first=False)
            msg = f"Applied One-Hot Encoding to {len(columns)} columns"
        else:
            msg = "No specific encoding method selected."
        return df_copy, msg
    except Exception as e:
        return df, f"Error encoding: {str(e)}"

def scale_numerical(df, columns, method):
    """Scale selected numerical columns."""
    df_copy = df.copy()
    try:
        if method == "Min-Max Normalization":
            scaler = MinMaxScaler()
            df_copy[columns] = scaler.fit_transform(df_copy[columns])
            msg = f"Applied Min-Max Normalization to {len(columns)} columns"
        elif method == "Standard Scaling (Z-score)":
            scaler = StandardScaler()
            df_copy[columns] = scaler.fit_transform(df_copy[columns])
            msg = f"Applied Standard Scaling to {len(columns)} columns"
        else:
             msg = "No specific scaling method selected."
        return df_copy, msg
    except Exception as e:
         return df, f"Error scaling: {str(e)}"
