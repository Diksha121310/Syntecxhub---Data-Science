import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def load_or_generate_data():
    print("\nDo you want to load your own CSV? (y/n)")
    choice=input("> ").strip().lower()

    if choice=="y":
        path=input("\nEnter CSV file path: ")
        df=pd.read_csv(path)
        df["date"]=pd.to_datetime(df["date"])
        df.set_index("date",inplace=True)
        print("CSV loaded successfully!")
    else:
        print("\nGenerating sample data...")
        data={
            "date":pd.date_range(start="2024-01-01",periods=180,freq="D"),
            "sales":np.random.randint(1000,5000,180),
            "category":np.random.choice(["A","B","C","D"],180),
        }
        df=pd.DataFrame(data)
        df.set_index("date",inplace=True)
        print("Sample data created!")

    return df

def plot_line(df):
    plt.figure(figsize=(10,5))
    plt.plot(df.index, df["sales"])
    plt.title("Daily Sales Over Time")
    plt.xlabel("Date")
    plt.ylabel("Sales")
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    plt.savefig("line_chart.png",dpi=300)
    plt.close()
    print("Saved: line_chart.png")

def plot_monthly(df):
    monthly=df["sales"].resample("ME").sum()
    plt.figure(figsize=(10,5))
    plt.plot(monthly.index,monthly.values)
    plt.title("Monthly Sales")
    plt.xlabel("Month")
    plt.ylabel("Sales")
    plt.grid(True,alpha=0.3)
    plt.tight_layout()
    plt.savefig("monthly_chart.png",dpi=300)
    plt.close()
    print("Saved: monthly_chart.png")

def plot_quarterly(df):
    quarterly=df["sales"].resample("QE").sum()
    plt.figure(figsize=(8,5))
    plt.bar(quarterly.index.strftime("%Y-Q%q"),quarterly.values)
    plt.title("Quarterly Sales")
    plt.xlabel("Quarter")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("quarterly_chart.png",dpi=300)
    plt.close()
    print("Saved: quarterly_chart.png")

def plot_category_bar(df):
    category_sales=df.groupby("category")["sales"].sum()
    plt.figure(figsize=(8,5))
    plt.bar(category_sales.index,category_sales.values)
    plt.title("Sales by Category")
    plt.xlabel("Category")
    plt.ylabel("Sales")
    plt.tight_layout()
    plt.savefig("category_bar.png",dpi=300)
    plt.close()
    print("Saved: category_bar.png")

def plot_category_pie(df):
    category_sales=df.groupby("category")["sales"].sum()
    plt.figure(figsize=(6,6))
    plt.pie(category_sales.values,labels=category_sales.index,autopct="%1.1f%%")
    plt.title("Category Share")
    plt.tight_layout()
    plt.savefig("category_pie.png",dpi=300)
    plt.close()
    print("Saved: category_pie.png")

def generate_summary(df):
    monthly=df["sales"].resample("ME").sum()
    quarterly=df["sales"].resample("QE").sum()
    category_sales=df.groupby("category")["sales"].sum()

    q_index=quarterly.idxmax()
    q_year=q_index.year
    q_month=q_index.month
    q_number=(q_month-1)//3+1
    best_quarter_label=f"{q_year}-Q{q_number}"

    summary=f"""
Sales Summary Report
---------------------------------------
Date Range:{df.index.min().date()} to {df.index.max().date()}

Total Sales:{df['sales'].sum()}
Average Daily Sales:{df['sales'].mean():.2f}

Best Month:{monthly.idxmax().strftime('%B %Y')}({monthly.max()})
Best Quarter:{best_quarter_label}({quarterly.max()})

Top Category:{category_sales.idxmax()}({category_sales.max()})
Lowest Category:{category_sales.idxmin()}({category_sales.min()})
"""

    with open("summary.txt","w") as f:
        f.write(summary)

    print("Saved: summary.txt")

def menu():
    df=load_or_generate_data()
    while True:
        print("""
Choose what you want to generate:
1 : Line Chart (Sales Over Time)
2 : Monthly Sales Chart
3 : Quarterly Sales Chart
4 : Category Bar Chart
5 : Category Pie Chart
6 : Generate Summary Report
7 : Generate ALL Charts + Summary
0 : Exit
""")
        choice=input("> ").strip()

        if choice=="1": plot_line(df)
        elif choice=="2": plot_monthly(df)
        elif choice=="3": plot_quarterly(df)
        elif choice=="4": plot_category_bar(df)
        elif choice=="5": plot_category_pie(df)
        elif choice=="6": generate_summary(df)
        elif choice=="7":
            plot_line(df)
            plot_monthly(df)
            plot_quarterly(df)
            plot_category_bar(df)
            plot_category_pie(df)
            generate_summary(df)
        elif choice=="0":
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Try again.")

menu()
