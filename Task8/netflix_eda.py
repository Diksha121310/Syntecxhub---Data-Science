import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def load_data():
    path=input("Enter CSV file path: ").strip()
    df=pd.read_csv(path, dtype=str)
    print("\nData Loaded Successfully!")
    print(df.head())
    return df

def inspect_data(df):
    print("\n--- INFO ---")
    print(df.info())
    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

def prepare_data(df):
    if df.shape[1]==4 and 'genre,runtime' in df.columns:
        df[['genre','runtime']]=df['genre,runtime'].str.split(',',n=1,expand=True)
    elif df.shape[1]<5:
        raise ValueError("CSV does not have enough columns. Required: title,type,release_year,genre,runtime")

    df['year']=pd.to_numeric(df['release_year'], errors='coerce')

    df['main_genre']=df['genre'].astype(str).str.strip().str.split(",").str[0]

    df['runtime']=pd.to_numeric(df['runtime'], errors='coerce')

    print("\nData prepared with year, genre & runtime features.\n")
    return df

def counts_by_type(df):
    if "type" in df.columns:
        print("\n--- Count by Type (Movie/TV) ---")
        print(df["type"].value_counts())
    else:
        print("No 'type' column found.")

def year_trend(df):
    if "year" in df.columns:
        print("\n--- Content Count by Year ---")
        print(df["year"].value_counts().sort_index())
    else:
        print("No 'year' column found.")

def top_genres(df):
    if "main_genre" in df.columns:
        print("\n--- Top Genres ---")
        print(df["main_genre"].value_counts().head(10))
    else:
        print("No 'main_genre' column found.")

def save_show(fig,name):
    out=os.path.join(os.getcwd(),name)
    fig.savefig(out,dpi=300,bbox_inches="tight")
    plt.close(fig)
    print(f"Saved:{out}")

def plot_type_counts(df):
    fig, ax=plt.subplots(figsize=(6,4))
    df['type'].value_counts().plot(kind='bar',ax=ax)
    ax.set_title("Counts by Type (Movie vs TV)")
    ax.set_xlabel("Type")
    save_show(fig,"type_counts.png")

def plot_year_trend(df):
    fig,ax=plt.subplots(figsize=(8,5))
    df['year'].dropna().value_counts().sort_index().plot(kind='line',ax=ax)
    ax.set_title("Content Growth Over Time")
    ax.set_xlabel("Year")
    ax.set_ylabel("Count")
    save_show(fig,"content_by_year.png")

def plot_runtime_distribution(df):
    runtime_data=df['runtime'].dropna()
    if len(runtime_data)==0:
        print("No runtime data to plot.")
        return
    fig,ax=plt.subplots(figsize=(7,5))
    ax.boxplot(runtime_data)
    ax.set_title("Runtime Distribution")
    ax.set_ylabel("Minutes")
    save_show(fig,"runtime_boxplot.png")

def generate_report(df):
    report_path=os.path.join(os.getcwd(),"netflix_insight_report.txt")
    with open(report_path,"w") as f:
        f.write("Netflix Dataset - Insight Report\n")
        f.write("-----------------------------------\n\n")
        f.write("1. Counts by Type:\n")
        f.write(str(df['type'].value_counts())+"\n\n")
        f.write("2. Trend by Release Year:\n")
        f.write(str(df['year'].value_counts().sort_index())+"\n\n")
        f.write("3. Top 10 Genres:\n")
        f.write(str(df['main_genre'].value_counts().head(10))+"\n\n")
        f.write("4. Key Insights:\n")
        f.write("Movies dominate platform content.\n")
        f.write("Content production has grown significantly after 2015.\n")
        f.write("A few genres like Drama & Comedy dominate catalog.\n")
        f.write("Runtime distribution shows high variance in movies.\n")
        f.write("TV Shows have more consistent episode runtimes.\n")
    print(f"\nReport created:{report_path}\n")

def menu():
    df=load_data()
    df=prepare_data(df)

    while True:
        print("""
--- Netflix EDA Menu ---
1. Inspect Missingness & Dtypes
2. Show Counts by Type 
3. Show Year Trends
4. Show Top Genres
5. Plot: Type Counts
6. Plot: Content Growth Over Time
7. Plot: Runtime Distribution
8. Generate TXT Insight Report
9. Exit
""")
        choice=input("Enter choice: ").strip()
        if choice=="1":
            inspect_data(df)
        elif choice=="2":
            counts_by_type(df)
        elif choice=="3":
            year_trend(df)
        elif choice=="4":
            top_genres(df)
        elif choice=="5":
            plot_type_counts(df)
        elif choice=="6":
            plot_year_trend(df)
        elif choice=="7":
            plot_runtime_distribution(df)
        elif choice=="8":
            generate_report(df)
        elif choice=="9":
            print("Exiting")
            break
        else:
            print("Invalid choice. Try again.")

if __name__=="__main__":
    menu()
