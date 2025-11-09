import csv
import logging
import os

# Configure Logging
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="friends_analysis.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Safe CSV Loader

def load_friends_csv(filepath):
    """Load the friends CSV safely with error handling and logging."""
    try:
        with open(filepath, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            data = [row for row in reader]
            logging.info(f"Successfully loaded {len(data)} rows from {filepath}")
            return data

    except FileNotFoundError:
        logging.error(f"File not found: {filepath}")
        print("Error: The file path is incorrect or missing.")
    except Exception as e:
        logging.error(f"Error while loading CSV: {str(e)}")
        print("Error loading data:", e)
    finally:
        logging.info("Finished attempting to load CSV file.")

# Run this directly to test it
if __name__ == "__main__":
    filepath = "friends_data.csv"
    data = load_friends_csv(filepath)
    if data:
        print(f"Loaded {len(data)} records successfully.")
