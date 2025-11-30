import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os

file_path=input("Enter CSV file path: ")
df=pd.read_csv(file_path)
numeric_df=df.select_dtypes(include=np.number)

output_folder="analysis_outputs"
os.makedirs(output_folder,exist_ok=True)

def correlation_heatmap():
    corr=numeric_df.corr(method='pearson')
    plt.figure(figsize=(10,8))
    mask=np.triu(np.ones_like(corr,dtype=bool))
    sns.heatmap(corr,mask=mask,annot=True,fmt=".2f",cmap='coolwarm',linewidths=0.5)
    plt.title("Correlation Heatmap")
    
    heatmap_file=os.path.join(output_folder,"correlation_heatmap.png")
    plt.savefig(heatmap_file,bbox_inches='tight')
    plt.close()
    print(f"Heatmap saved as:{heatmap_file}")
    return corr

def pairplot():
    pairplot_fig=sns.pairplot(df[numeric_df.columns.tolist()])
    pairplot_file=os.path.join(output_folder,"pairplot.png")
    pairplot_fig.savefig(pairplot_file)
    plt.close()
    print(f"Pairplot saved as:{pairplot_file}")

def strongest_correlations(corr):
    corr_pairs=corr.unstack()
    corr_pairs=corr_pairs[corr_pairs!=1]  
    strongest_pos = corr_pairs.sort_values(ascending=False).head(5)
    strongest_neg = corr_pairs.sort_values().head(5)

    summary_file=os.path.join(output_folder,"strongest_correlations.txt")
    with open(summary_file,"w") as f:
        f.write("Strongest positive correlations:\n")
        f.write(str(strongest_pos))
        f.write("\n\nStrongest negative correlations:\n")
        f.write(str(strongest_neg))
    
    print(f"Strongest correlations saved as: {summary_file}")

while True:
    print("\nChoose an option:")
    print("1. Correlation Heatmap")
    print("2. Pairplot / Scatter Matrix")
    print("3. Strongest Correlations")
    print("4. Exit")
    
    choice=input("Enter your choice: ")
    
    if choice=="1":
        corr=correlation_heatmap()
    elif choice=="2":
        pairplot()
    elif choice=="3":
        if 'corr' not in locals():
            corr=numeric_df.corr()
        strongest_correlations(corr)
    elif choice=="4":
        print("Exiting")
        break
    else:
        print("Invalid choice. Try again.")
