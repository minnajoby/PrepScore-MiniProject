# In clean_data.py
import pandas as pd

# Define the input and output filenames
INPUT_CSV = 'training_data.csv'
OUTPUT_CSV = 'training_data_cleaned.csv'

def clean_dataset():
    """
    Loads the raw training data, cleans it, and saves a new CSV file.
    Cleaning steps include:
    1. Handling missing values.
    2. Ensuring all data is in the correct numerical format.
    3. Verifying the structure.
    """
    print("--- Starting Data Cleaning Process ---")

    # 1. Load the Dataset
    try:
        df = pd.read_csv(INPUT_CSV)
        print(f"Successfully loaded '{INPUT_CSV}'. Shape: {df.shape}")
    except FileNotFoundError:
        print(f"ERROR: The file '{INPUT_CSV}' was not found. Please run export_data.py first.")
        return

    # 2. Initial Data Inspection (Good Practice)
    print("\n--- Data Inspection ---")
    print("Columns and data types:")
    print(df.info())
    
    missing_values = df.isnull().sum()
    print("\nChecking for missing values (NaNs)...")
    if missing_values.sum() == 0:
        print("No missing values found. Excellent!")
    else:
        print("Missing values found in the following columns:")
        print(missing_values[missing_values > 0])

    # 3. Clean the Data
    # Step 3a: Handle Missing Values
    # For this project, a missing value logically means '0'. For example, if 'num_skills'
    # is missing, it means the user has 0 skills. We will fill all NaNs with 0.
    if missing_values.sum() > 0:
        print("\nFilling missing values with 0...")
        df.fillna(0, inplace=True)
        print("Missing values handled.")

    # Step 3b: Ensure All Feature Columns are Integers
    # This prevents errors if a column was accidentally read as a float or object.
    print("\nEnsuring all columns are integer data types...")
    for col in df.columns:
        # We convert to float first to handle any potential non-integer numbers, then to int.
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
    print("Data types corrected.")

    # 4. Save the Cleaned Dataset
    try:
        df.to_csv(OUTPUT_CSV, index=False)
        print(f"\n--- Cleaning complete! ---")
        print(f"Cleaned data saved to '{OUTPUT_CSV}'. Shape: {df.shape}")
        print("\nFirst 5 rows of the cleaned data:")
        print(df.head())
    except Exception as e:
        print(f"\nERROR: Could not save the cleaned file. Reason: {e}")

if __name__ == '__main__':
    clean_dataset()