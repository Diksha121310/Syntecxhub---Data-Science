import pandas as pd

def menu():
    print("\n-----------------------------")
    print("     PANDAS DATA EXPLORER")
    print("-----------------------------")
    print("1. Load CSV file")
    print("2. View head")
    print("3. View tail")
    print("4. View data types")
    print("5. Summary statistics")
    print("6. Select columns")
    print("7. Filter rows")
    print("8. Save filtered data")
    print("0. Exit")
    print("------------------------------")

def main():
    df=None
    filtered_df=None

    while True:
        menu()
        choice=input("Enter choice: ")

        if choice=="1":
            filename=input("Enter CSV filename: ").strip()
            try:
                df=pd.read_csv(filename)
                print("\nFile loaded successfully!")
                print(df.head())
            except Exception as e:
                print("Error loading file:",e)

        elif choice=="2":
            if df is None:
                print("Load a CSV first!")
            else:
                print("\n----- HEAD -----")
                print(df.head())

        elif choice=="3":
            if df is None:
                print("Load a CSV first!")
            else:
                print("\n----- TAIL -----")
                print(df.tail())

        elif choice=="4":
            if df is None:
                print("Load a CSV first!")
            else:
                print("\n----- DATA TYPES -----")
                print(df.dtypes)

        elif choice=="5":
            if df is None:
                print("Load a CSV first!")
            else:
                print("\n----- SUMMARY STATISTICS -----")
                print(df.describe(include="all"))

        elif choice=="6":
            if df is None:
                print("Load a CSV first!")
            else:
                cols=input("Enter column names separated by commas: ").split(",")
                cols=[c.strip() for c in cols]

                try:
                    filtered_df=df[cols]
                    print("\nSelected columns:")
                    print(filtered_df.head())
                except Exception as e:
                    print("Invalid column name!",e)

        elif choice=="7":
            if df is None:
                print("Load a CSV first!")
            else:
                col=input("Enter column to filter: ").strip()
                val=input("Enter value to match: ").strip()

                try:
                    filtered_df=df[df[col].astype(str)==val]
                    print("\nFiltered rows:")
                    print(filtered_df.head())
                    print(f"Total rows matched:{len(filtered_df)}")
                except Exception as e:
                    print("Error filtering rows:",e)

        elif choice=="8":
            if filtered_df is None:
                print("No filtered data! Use option 6 or 7 first.")
            else:
                out=input("Enter output file name (with .csv): ").strip()
                try:
                    filtered_df.to_csv(out, index=False)
                    print(f"Filtered data saved as{out}")
                except Exception as e:
                    print("Error saving file:",e)

        elif choice=="0":
            print("Exiting...")
            break

        else:
            print("Invalid option! Try again.")

if __name__=="__main__":
    main()
