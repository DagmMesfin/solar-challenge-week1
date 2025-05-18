from scipy import stats
import pandas as pd
import numpy as np

def summarize_and_check_missing(df, threshold=0.05):
    print("Summary Statistics & Missing-Value Report:")
    print(df.describe())
    print()
    print("Missing Values:")
    print(df.isna().sum())

    print("Checking the columns containing missing values rate greater than 5%:")
    missing_percent = df.isna().mean()
    high_missing = missing_percent[missing_percent > threshold]
    return high_missing

def detect_and_remove_outliers(df, columns):
    z_scores = np.abs(stats.zscore(df[columns]))
    outlier_mask = (z_scores > 3).any(axis=1)
    print(f"Number of outliers: {outlier_mask.sum()}")

    print("removing outliers...")
    return df[~outlier_mask]

def normalize_negative_to_zero(df, columns):
    for col in columns:
        invalid_count = (df[col] < 0).sum()
        print(f"{col}: {invalid_count} values < 0")
        df[col] = df[col].clip(lower=0)

    return df