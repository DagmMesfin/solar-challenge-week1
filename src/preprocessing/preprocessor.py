import pandas as pd

def load_and_preview(filepath):
    df = pd.read_csv(filepath)
    print("First few rows of the dataset:")
    print(df.head())
    return df

def save_cleaned_data(df, country):
    output_path = f"../data/{country}_clean.csv"
    df.to_csv(output_path, index=False)
    print(f"Cleaned data exported to: {output_path}")