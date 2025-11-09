import pandas as pd
import logging
import os

# Logging Setup

logging.basicConfig(
    filename="friends_analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load and Explore Data

def load_and_explore(filepath):
    """Load the friends CSV and print basic information."""
    try:
        df = pd.read_csv(filepath)
        logging.info("DataFrame loaded successfully.")
        
        print("\n--- Basic Info ---")
        print(df.info())

        print("\n--- Missing Values ---")
        print(df.isna().sum())

        print("\n--- Sample Rows ---")
        print(df.head())

        return df

    except Exception as e:
        logging.error(f"Error loading DataFrame: {str(e)}")
        print("Error:", e)
        return None

# Clean Data

def clean_data(df):
    """Handle missing data and remove duplicates."""
    try:
        df = df.drop_duplicates()
        df = df.fillna("")  # fill blanks safely
        logging.info("🧹 Cleaned data (duplicates removed, missing filled).")
        return df
    except Exception as e:
        logging.error(f" Error cleaning data: {str(e)}")
        print("Error:", e)
        return df

# Test Code (run standalone)
if __name__ == "__main__":
    path = "friends_data.csv"
    df = load_and_explore(path)
    if df is not None:
        df = clean_data(df)
        print(f"\nFinal dataset shape: {df.shape}")
