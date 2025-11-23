import pandas as pd
import os
from datetime import datetime
import warnings

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)


def load_file():
    fname = input("Enter CSV filename: ").strip()
    if not fname:
        print("No filename provided.")
        return None, None

    if not os.path.exists(fname):
        print("File not found:", fname)
        return None, None

    try:
        df = pd.read_csv(fname, na_values=["", " "], keep_default_na=True)
        print("\nFile loaded successfully!\n")
        print("=== FULL DATA ===")
        print(df)         
        print()
        return df, fname

    except Exception as e:
        print("Error loading file:", e)
        return None, None


def standardize_columns(df):
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    return df


def is_date_column(series):
    sample = series.dropna().astype(str).head(6)
    if sample.empty:
        return False
    return sample.str.contains(r"\d{4}|[-/]", regex=True).any()


def parse_dates(df):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        for col in df.columns:
            if is_date_column(df[col]):
                df[col] = pd.to_datetime(df[col], errors="coerce", dayfirst=True)
    return df


def convert_numeric(df):
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            continue
        sample = df[col].dropna().astype(str).head(6)
        if sample.str.contains(r"\d", regex=True).any():
            converted = pd.to_numeric(df[col], errors="coerce")
            if converted.notna().sum() > 0:
                df[col] = converted
    return df


def handle_missing(df):
    print("\nMissing Values Handling:")
    print("1. Drop rows with missing")
    print("2. Fill ALL missing with constant")
    print("3. Fill numeric missing with mean")
    print("4. Fill numeric missing with median")
    print("5. numeric → 0, text → 'NA'")
    print("6. Skip")

    choice = input("Enter choice [1-6]: ").strip()

    if choice == "1":
        df = df.dropna()
        print("Dropped rows with missing values.")

    elif choice == "2":
        val = input("Enter constant: ")
        df = df.fillna(val)
        print("Filled missing with:", val)

    elif choice == "3":
        for col in df.select_dtypes(include="number"):
            df[col] = df[col].fillna(df[col].mean())
        print("Filled numeric missing with mean.")

    elif choice == "4":
        for col in df.select_dtypes(include="number"):
            df[col] = df[col].fillna(df[col].median())
        print("Filled numeric missing with median.")

    elif choice == "5":
        for col in df.select_dtypes(include="number"):
            df[col] = df[col].fillna(0)
        for col in df.select_dtypes(include="object"):
            df[col] = df[col].fillna("NA")
        print("Filled numeric → 0 and text → 'NA'.")

    else:
        print("Skipped missing value handling.")

    return df


def remove_duplicates(df):
    return df.drop_duplicates()


def save_output(df, original):
    out_name = "cleaned_" + os.path.basename(original)
    df.to_csv(out_name, index=False)

    log_name = "cleaning_log_" + os.path.splitext(original)[0] + ".txt"
    with open(log_name, "w", encoding="utf-8") as f:
        f.write("Cleaning completed successfully.\n")
        f.write("Rows after cleaning: " + str(len(df)) + "\n")

    print("\nSaved cleaned data as:", out_name)
    print("Saved cleaning log as:", log_name)

    print("\n=== FULL CLEANED DATA ===")
    print(df)        


def main():
    print("=== SIMPLE DATA CLEANER ===")

    df = None
    fname = None

    while True:
        print("\nMenu:")
        print("1. Load CSV")
        print("2. Clean data")
        print("3. Save current data")
        print("4. Show head/tail")
        print("0. Exit")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            df, fname = load_file()

        elif choice == "2":
            if df is None:
                print("Load CSV first!")
                continue

            df = df.replace(r"^\s*$", pd.NA, regex=True)

            df = standardize_columns(df)
            df = convert_numeric(df)
            df = parse_dates(df)
            df = handle_missing(df)
            df = remove_duplicates(df)

            save_output(df, fname)

        elif choice == "3":
            if df is None:
                print("No data to save.")
                continue

            out = input("Enter filename (or press enter): ").strip()
            if not out:
                out = "export_" + fname

            df.to_csv(out, index=False)
            print("Saved to", out)

        elif choice == "4":
            if df is None:
                print("No data loaded.")
            else:
                print("\nHEAD :")
                print(df.head(5))

                print("\nTAIL :")
                print(df.tail())

        elif choice == "0":
            print("Goodbye!")
            break

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
