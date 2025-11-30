import pandas as pd
import matplotlib.pyplot as plt

def load_data():
    file_path=input("Enter CSV file path: ")
    return pd.read_csv(file_path)

def choose_column(df,message):
    print(f"\nAvailable columns:{list(df.columns)}")
    col=input(f"{message}: ")
    while col not in df.columns:
        col=input("Invalid column. Enter again: ")
    return col

def plot_histogram(df,value_col):
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    plt.figure(figsize=(8,5))
    plt.hist(df[value_col].dropna(),bins=20)
    plt.title(f"Histogram of {value_col}")
    plt.xlabel(value_col)
    plt.ylabel("Frequency")
    plt.savefig("histogram.png")
    plt.close()
    print("Histogram saved as histogram.png")

def plot_kde(df,value_col):
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    plt.figure(figsize=(8,5))
    df[value_col].dropna().plot(kind='kde')
    plt.title(f"KDE of {value_col}")
    plt.xlabel(value_col)
    plt.savefig("kde.png")
    plt.close()
    print("KDE saved as kde.png")

def plot_boxplot(df,column,group=None,log_scale=False):
    df[column]=pd.to_numeric(df[column],errors="coerce")
    df=df.dropna(subset=[column])

    plt.figure(figsize=(8,5))

    if group and group in df.columns:
        df.boxplot(column=column,by=group)
        plt.title(f"Boxplot of {column} grouped by {group}")
        plt.suptitle("")
        filename="boxplot_grouped.png"
    else:
        plt.boxplot(df[column])
        plt.title(f"Boxplot of {column}")
        filename="boxplot.png"

    if log_scale:
        plt.yscale("log")

    plt.xlabel(group if group else column)
    plt.ylabel(column)
    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

    print(f"Boxplot saved as {filename}")

def plot_grouped(df,value_col, group_col):
    if group_col not in df.columns:
        print("Group column not found.")
        return

    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")

    plt.figure(figsize=(8,5))
    for key, grp in df.groupby(group_col):
        grp[value_col].dropna().plot(kind='kde',label=str(key))
    plt.title(f"KDE by {group_col}")
    plt.legend()
    plt.savefig("kde_by_group.png")
    plt.close()
    print("Grouped KDE saved as kde_by_group.png")

    plt.figure(figsize=(8,5))
    df.boxplot(column=value_col,by=group_col)
    plt.title(f"Boxplot of {value_col} by {group_col}")
    plt.suptitle("")
    plt.savefig("boxplot_by_group.png")
    plt.close()
    print("Grouped Boxplot saved as boxplot_by_group.png")

def detect_outliers(df,value_col):
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    Q1=df[value_col].quantile(0.25)
    Q3=df[value_col].quantile(0.75)
    IQR=Q3-Q1
    
    lower=Q1-1.5*IQR
    upper=Q3+1.5*IQR
    
    outliers=df[(df[value_col]<lower)|(df[value_col]>upper)]
    
    print(f"\nOutliers:\n{outliers[[value_col]]}\n")

    outliers.to_csv("outliers.csv",index=False)
    print("Outliers saved as outliers.csv")

def summary_statistics(df,value_col):
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    stats=df[value_col].describe()

    print("\n--- Summary Statistics ---")
    print(stats)

    stats.to_csv("summary_statistics.csv")
    print("Summary statistics saved as summary_statistics.csv")

def interpretation(df,value_col):
    df[value_col]=pd.to_numeric(df[value_col],errors="coerce")
    skewness=df[value_col].skew()
    spread=df[value_col].std()

    if skewness>0:
        direction="right-skewed (tail toward higher values)"
    elif skewness<0:
        direction="left-skewed (tail toward lower values)"
    else:
        direction="symmetric"

    text=(
        f"The distribution of {value_col} is {direction}, with a spread (std dev) of "
        f"approximately {spread:.2f}. Histogram and KDE plots show concentration of values, "
        f"while the boxplot highlights potential outliers and overall data spread.\n"
    )

    print("\n--- Interpretation ---")
    print(text)

    with open("interpretation.txt","w") as f:
        f.write(text)

    print("Interpretation saved as interpretation.txt")

def menu():
    df = load_data()
    value_col = choose_column(df,"Enter numeric column to analyze")
    
    group_choice=input("Do you want to select a group column? (y/n): ").lower()
    group_col=None
    if group_choice=="y":
        group_col=choose_column(df,"Enter group column")
    
    while True:
        print("""
===== Statistical Distribution Analysis =====
1. Histogram
2. KDE Plot
3. Boxplot
4. Grouped KDE & Boxplot
5. Detect Outliers
6. Summary Statistics
7. Interpretation
8. Run All Analysis
9. Exit
""")
        choice=input("Enter your choice: ")

        if choice=="1":
            plot_histogram(df,value_col)

        elif choice=="2":
            plot_kde(df,value_col)

        elif choice=="3":
            plot_boxplot(df,value_col)

        elif choice=="4":
            if group_col:
                plot_grouped(df,value_col,group_col)
            else:
                print("No group column selected.")

        elif choice=="5":
            detect_outliers(df,value_col)

        elif choice=="6":
            summary_statistics(df,value_col)

        elif choice=="7":
            interpretation(df,value_col)

        elif choice=="8":
            plot_histogram(df,value_col)
            plot_kde(df,value_col)
            plot_boxplot(df,value_col)
            if group_col:
                plot_grouped(df,value_col,group_col)
            detect_outliers(df,value_col)
            summary_statistics(df,value_col)
            interpretation(df,value_col)

        elif choice=="9":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Try again.")
menu()
