import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from scipy.signal import find_peaks

def load_data():
    path=input("Enter CSV file path: ").strip()
    df=pd.read_csv(path, parse_dates=["date"])
    print("\nData Loaded Successfully!")
    print(df.head())
    return df

def inspect_data(df):
    print("\n--- INFO ---")
    print(df.info())
    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

def compute_daily_cases(df):
    df=df.sort_values(["country", "date"])
    df["daily_confirmed"]=df.groupby("country")["confirmed"].diff().fillna(df["confirmed"])
    df["daily_deaths"]=df.groupby("country")["deaths"].diff().fillna(df["deaths"])
    df["daily_recovered"]=df.groupby("country")["recovered"].diff().fillna(df["recovered"])
    print("\nDaily cases computed!")
    return df

def rolling_average(df,window=7):
    df["confirmed_roll"]=df.groupby("country")["daily_confirmed"].transform(lambda x:x.rolling(window,min_periods=1).mean())
    df["deaths_roll"]=df.groupby("country")["daily_deaths"].transform(lambda x:x.rolling(window,min_periods=1).mean())
    print(f"\nRolling average ({window}-day) computed!")
    return df

def plot_country_comparison(df,metric="daily_confirmed"):
    countries=df["country"].unique()
    fig,ax=plt.subplots(figsize=(10,6))
    for c in countries:
        subset=df[df["country"]==c]
        ax.plot(subset["date"],subset[metric],label=c)
    ax.set_title(f"COVID-19 {metric.replace('_',' ').title()} Comparison")
    ax.set_xlabel("Date")
    ax.set_ylabel(metric.replace("_"," ").title())
    ax.legend()
    file_name=f"{metric}_comparison.png"
    fig.savefig(os.path.join(os.getcwd(),file_name),dpi=300,bbox_inches="tight")
    plt.close(fig)
    print(f"Saved plot: {file_name}")

def detect_peaks(df,metric="daily_confirmed"):
    peaks_info={}
    countries=df["country"].unique()
    for c in countries:
        subset=df[df["country"]==c]
        values=subset[metric].values
        peaks,_=find_peaks(values, distance=3) 
        peaks_info[c]={"dates": subset.iloc[peaks]["date"].tolist(),"values": values[peaks].tolist()}
    return peaks_info

def generate_report(df,peaks_info):
    report_path=os.path.join(os.getcwd(),"covid_analysis_report.txt")
    with open(report_path,"w") as f:
        f.write("COVID-19 Data Analysis Report\n")
        f.write("----------------------------\n\n")
        f.write("Key Insights:\n")
        for country, info in peaks_info.items():
            f.write(f"\nCountry: {country}\n")
            if len(info["dates"])==0:
                f.write("No clear peaks detected.\n")
            else:
                for d,v in zip(info["dates"],info["values"]):
                    f.write(f"Peak on {d.date()} with {int(v)} cases\n")
    print(f"\nReport saved: {report_path}")

def menu():
    df=load_data()
    df=compute_daily_cases(df)
    df=rolling_average(df)

    while True:
        print("""
--- COVID-19 EDA Menu ---
1. Inspect Data
2. Show Daily Cases
3. Show Rolling Averages
4. Plot Country Comparison (Daily Confirmed)
5. Plot Country Comparison (7-day Rolling)
6. Detect Peaks
7. Generate Insight Report
8. Exit
""")
        choice=input("Enter choice: ").strip()
        if choice=="1":
            inspect_data(df)
        elif choice=="2":
            print(df[["date","country","daily_confirmed","daily_deaths","daily_recovered"]].head(20))
        elif choice=="3":
            print(df[["date","country","confirmed_roll","deaths_roll"]].head(20))
        elif choice=="4":
            plot_country_comparison(df, "daily_confirmed")
        elif choice=="5":
            plot_country_comparison(df, "confirmed_roll")
        elif choice=="6":
            peaks=detect_peaks(df)
            for c,info in peaks.items():
                print(f"\n{c} Peaks:")
                for d,v in zip(info["dates"],info["values"]):
                    print(f"{d.date()} -> {int(v)} cases")
        elif choice=="7":
            peaks=detect_peaks(df)
            generate_report(df,peaks)
        elif choice=="8":
            print("Exiting")
            break
        else:
            print("Invalid choice. Try again.")

if __name__=="__main__":
    menu()
