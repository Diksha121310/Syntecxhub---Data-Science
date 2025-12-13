import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import calculate_kpis
import io, base64

st.set_page_config(page_title="Sales Dashboard",page_icon="📊",layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

with open("templates/header.html") as f:
    st.markdown(f.read(),unsafe_allow_html=True)

def render_section(title,subtitle,fig=None):
    with open("templates/section.html") as f:
        section_template=f.read()

    if fig is not None:
        buf=io.BytesIO()
        fig.savefig(buf,format="png",bbox_inches="tight")
        buf.seek(0)
        img_base64=base64.b64encode(buf.read()).decode("utf-8")
        content=f'<img src="data:image/png;base64,{img_base64}" width="100%"/>'
    else:
        content="<p>No data available</p>"

    section_html=section_template.replace("{{ section_title }}",title)
    section_html=section_html.replace("{{ section_subtitle }}",subtitle)
    section_html=section_html.replace("{{ section_content }}",content)
    st.markdown(section_html,unsafe_allow_html=True)

uploaded_file=st.file_uploader("📂 Upload CSV File", type=["csv"])
if uploaded_file:

    df=pd.read_csv(uploaded_file)
    st.subheader("🔍 Preview of Uploaded Data")
    st.dataframe(df.head())

    st.sidebar.header("🧩 Column Mapping")
    columns=df.columns.tolist()
    order_col=st.sidebar.selectbox("Order ID Column",columns)
    date_col=st.sidebar.selectbox("Order Date Column",columns)
    product_col=st.sidebar.selectbox("Product Column",columns)
    qty_col=st.sidebar.selectbox("Quantity Column",columns)
    price_col=st.sidebar.selectbox("Price Column",columns)
    region_col=st.sidebar.selectbox("Region Column",columns)

    df["OrderDate"]=pd.to_datetime(df[date_col],errors="coerce")
    df[qty_col]=pd.to_numeric(df[qty_col],errors="coerce")
    df[price_col]=pd.to_numeric(df[price_col],errors="coerce")
    df = df.dropna(subset=["OrderDate",qty_col,price_col])
    df["Revenue"]=df[qty_col]*df[price_col]  

    st.sidebar.header("⚙️ Filters")
    regions=st.sidebar.multiselect(
        "Select Region",df[region_col].unique(),default=df[region_col].unique()
    )
    df=df[df[region_col].isin(regions)]
    if df.empty:
        st.warning("⚠️ No valid data available after filtering.")
        st.stop()

    total_revenue,avg_order_value,top_product=calculate_kpis(
        df,order_col,product_col,qty_col,price_col
    )

    col1,col2,col3=st.columns(3)
    kpi_data=[
        ("💰 Total Revenue", f"₹ {total_revenue:,.0f}"),
        ("🧾 Avg Order Value", f"₹ {avg_order_value:,.0f}"),
        ("🏆 Top Product", f"{top_product}"),
    ]
    for col, (title,value) in zip([col1,col2,col3],kpi_data):
        col.markdown(
            f"""
        <div class="metric-box">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    df["Month"]=df["OrderDate"].dt.to_period("M").astype(str)
    monthly_sales=df.groupby("Month")["Revenue"].sum().sort_index()
    if not monthly_sales.empty:
        fig,ax=plt.subplots(figsize=(12,4))
        ax.plot(monthly_sales.index,monthly_sales.values,marker="o",color="#4facfe")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        ax.set_title("Monthly Revenue Trend")
        ax.grid(True,alpha=0.3)
        plt.xticks(rotation=45)
        fig.tight_layout()
        render_section("📈 Monthly Sales Trend","Revenue over months",fig)

    top_products=df.groupby(product_col)["Revenue"].sum().sort_values(ascending=False).head(5)
    if not top_products.empty:
        fig,ax=plt.subplots(figsize=(10,4))
        top_products.plot(kind="bar",ax=ax,color="#00f2fe")
        ax.set_ylabel("Revenue")
        ax.set_title("Top 5 Products")
        fig.tight_layout()
        render_section("🏆 Top 5 Products","Highest revenue products",fig)

    region_sales=df.groupby(region_col)["Revenue"].sum()
    if not region_sales.empty:
        fig,ax=plt.subplots(figsize=(10,4))
        region_sales.plot(kind="bar",ax=ax,color="#4facfe")
        ax.set_ylabel("Revenue")
        ax.set_title("Revenue by Region")
        fig.tight_layout()
        render_section("🌍 Revenue by Region", "Sales across regions", fig)

    summary=pd.DataFrame({
        "Metric":["Total Revenue","Average Order Value","Top Product"],
        "Value":[total_revenue, avg_order_value,top_product]
    })

    render_section("📄 Summary Download","Key metrics CSV",fig=None)
    st.download_button(
        "⬇️ Download Summary CSV",
        summary.to_csv(index=False),
        file_name="sales_summary.csv",
        mime="text/csv"
    )
