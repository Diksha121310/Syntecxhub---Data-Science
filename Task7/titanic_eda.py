import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def load_data():
    path=input("Enter CSV file path: ")
    df=pd.read_csv(path)
    print("\nData Loaded Successfully!")
    print(df.head())
    return df

def add_age_groups(df):
    df["age_group"]=pd.cut(
        df["age"],
        bins=[0,12,18,30,50,80],
        labels=["Child","Teen","Young Adult","Adult","Senior"]
    )
    print("\nAge groups added!")
    return df

def inspect_data(df):
    print("\n--- INFO ---")
    print(df.info())
    print("\n--- MISSING VALUES ---")
    print(df.isna().sum())

def survival_stats(df):
    print("\n--- Survival by Gender ---")
    print(df.groupby("gender",observed=False)["survived"].mean())

    print("\n--- Survival by Class ---")
    print(df.groupby("class",observed=False)["survived"].mean())

    if "age_group" in df.columns:
        print("\n--- Survival by Age Group ---")
        print(df.groupby("age_group",observed=False)["survived"].mean())

def save_and_show(fig,name):
    out_path=os.path.join(os.getcwd(),name)
    fig.savefig(out_path,dpi=300,bbox_inches="tight")
    print(f"Saved:{out_path}")

def plot_survival_by_gender(df):
    fig=plt.figure(figsize=(6,4))
    df.groupby("gender",observed=False)["survived"].mean().plot(kind="bar")
    plt.title("Survival Rate by Gender")
    plt.ylabel("Survival Rate")
    save_and_show(fig,"survival_by_gender.png")

def plot_survival_by_class(df):
    fig=plt.figure(figsize=(6,4))
    df.groupby("class",observed=False)["survived"].mean().plot(kind="bar")
    plt.title("Survival Rate by Class")
    plt.ylabel("Survival Rate")
    save_and_show(fig,"survival_by_class.png")

def plot_age_box(df):
    fig,ax=plt.subplots(figsize=(7,5))
    df.boxplot(column="age", by="survived",ax=ax)
    ax.set_title("Age Distribution by Survival")
    plt.suptitle("") 
    save_and_show(fig,"age_boxplot.png")


def plot_fare_distribution(df):
    fig=plt.figure(figsize=(7,5))
    plt.boxplot(df["fare"],vert=True)
    plt.title("Fare Distribution")
    save_and_show(fig,"fare_distribution.png")

def generate_report_file(df):
    surv_gender=df.groupby("gender",observed=False)["survived"].mean()
    surv_class=df.groupby("class",observed=False)["survived"].mean()
    surv_age=df.groupby("age_group",observed=False)["survived"].mean()

    report_path=os.path.join(os.getcwd(),"titanic_insight_report.txt")

    with open(report_path,"w") as f:
        f.write("Titanic Dataset - Insight Report\n")
        f.write("--------------------------------\n\n")

        f.write("1. Survival Rate by Gender:\n")
        f.write(str(surv_gender)+"\n\n")

        f.write("2. Survival Rate by Class:\n")
        f.write(str(surv_class)+"\n\n")

        f.write("3. Survival Rate by Age Group:\n")
        f.write(str(surv_age)+"\n\n")

        f.write("4. Key Insights:\n")
        f.write("Females show higher survival probability than males.\n")
        f.write("First-class passengers have the highest survival rate.\n")
        f.write("Children survive more often than adults and seniors.\n")
        f.write("Higher fares correlate with higher survival.\n")
        f.write("Seniors show lowest survival rates.\n")

    print(f"\nReport generated:{report_path}\n")

def menu():
    df=load_data()
    df=add_age_groups(df)

    while True:
        print("""
        Choose an option:
        1. Inspect Missingness & Dtypes
        2. Survival Analysis
        3. Plot: Survival by Gender
        4. Plot: Survival by Class
        5. Plot: Age Boxplot
        6. Plot: Fare Distribution
        7. Generate Insight Report
        8. Exit
        """)

        choice=input("Enter choice: ").strip()

        if choice=="1":
            inspect_data(df)

        elif choice=="2":
            survival_stats(df)

        elif choice=="3":
            plot_survival_by_gender(df)

        elif choice=="4":
            plot_survival_by_class(df)

        elif choice=="5":
            plot_age_box(df)

        elif choice=="6":
            plot_fare_distribution(df)

        elif choice=="7":
            generate_report_file(df)

        elif choice=="8":
            print("Exiting")
            break

        else:
            print("Invalid input. Try again.")

if __name__=="__main__":
    menu()
