import pandas as pd

def calculate_kpis(df,order_col,product_col,qty_col,price_col):
    df["Revenue"]=df[qty_col]*df[price_col]
    total_revenue=df["Revenue"].sum()
    avg_order_value=df.groupby(order_col)["Revenue"].sum().mean()
    product_revenue=df.groupby(product_col)["Revenue"].sum()
    top_product=product_revenue.idxmax() if not product_revenue.empty else "N/A"
    return total_revenue,avg_order_value,top_product
