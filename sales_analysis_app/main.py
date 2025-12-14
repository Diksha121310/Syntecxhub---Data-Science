import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from utils import calculate_kpis
import io
import base64
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Sales Dashboard", page_icon="📊", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

def render_section(title, subtitle, fig=None):
    with open("templates/section.html") as f:
        section_template = f.read()

    if fig is not None:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight")
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode("utf-8")
        content = f'<img src="data:image/png;base64,{img_base64}" width="100%"/>'
    else:
        content = "<p>No data available</p>"

    section_html = section_template.replace("{{ section_title }}", title)
    section_html = section_html.replace("{{ section_subtitle }}", subtitle)
    section_html = section_html.replace("{{ section_content }}", content)
    st.markdown(section_html, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file:

    df = pd.read_csv(uploaded_file)
    st.subheader("Preview of Uploaded Data")
    st.dataframe(df.head())

    st.sidebar.header("Column Mapping")
    columns = df.columns.tolist()
    order_col = st.sidebar.selectbox("Order ID Column", columns)
    date_col = st.sidebar.selectbox("Order Date Column", columns)
    product_col = st.sidebar.selectbox("Product Column", columns)
    qty_col = st.sidebar.selectbox("Quantity Column", columns)
    price_col = st.sidebar.selectbox("Price Column", columns)
    region_col = st.sidebar.selectbox("Region Column", columns)

    df["OrderDate"] = pd.to_datetime(df[date_col], errors="coerce")
    df[qty_col] = pd.to_numeric(df[qty_col], errors="coerce")
    df[price_col] = pd.to_numeric(df[price_col], errors="coerce")
    df = df.dropna(subset=["OrderDate", qty_col, price_col])
    df["Revenue"] = df[qty_col] * df[price_col]

    st.sidebar.header("Filters")
    regions = st.sidebar.multiselect(
        "Select Region", df[region_col].unique(), default=df[region_col].unique()
    )
    df = df[df[region_col].isin(regions)]
    if df.empty:
        st.warning("No valid data available after filtering.")
        st.stop()

    total_revenue, avg_order_value, top_product = calculate_kpis(
        df, order_col, product_col, qty_col, price_col
    )

    # Display KPIs
    col1, col2, col3 = st.columns(3)
    kpi_data = [
        ("Total Revenue", f"₹ {total_revenue:,.0f}"),
        ("Average Order Value", f"₹ {avg_order_value:,.0f}"),
        ("Top Product", f"{top_product}"),
    ]
    for col, (title, value) in zip([col1, col2, col3], kpi_data):
        col.markdown(
            f"""
        <div class="metric-box">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
        </div>
        """,
            unsafe_allow_html=True,
        )

    # Monthly Sales Trend
    df["Month"] = df["OrderDate"].dt.to_period("M").astype(str)
    monthly_sales = df.groupby("Month")["Revenue"].sum().sort_index()
    monthly_sales_fig = None
    if not monthly_sales.empty:
        fig, ax = plt.subplots(figsize=(12, 4))
        ax.plot(monthly_sales.index, monthly_sales.values, marker="o", color="#4facfe")
        ax.set_xlabel("Month")
        ax.set_ylabel("Revenue")
        ax.set_title("Monthly Revenue Trend")
        ax.grid(True, alpha=0.3)
        plt.xticks(rotation=45)
        fig.tight_layout()
        render_section("Monthly Sales Trend", "Revenue over months", fig)
        monthly_sales_fig = fig

    # Seasonality insight
    peak_month, low_month = None, None
    if not monthly_sales.empty:
        peak_month = monthly_sales.idxmax()
        low_month = monthly_sales.idxmin()
        st.markdown(f"**Seasonality Insight:** Highest revenue in {peak_month}, lowest in {low_month}.")

    # Top Products
    top_products = df.groupby(product_col)["Revenue"].sum().sort_values(ascending=False).head(5)
    top_products_fig = None
    if not top_products.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        top_products.plot(kind="bar", ax=ax, color="#00f2fe")
        ax.set_ylabel("Revenue")
        ax.set_title("Top 5 Products")
        fig.tight_layout()
        render_section("Top 5 Products", "Highest revenue products", fig)
        top_products_fig = fig

    # Revenue by Region
    region_sales = df.groupby(region_col)["Revenue"].sum()
    region_sales_fig = None
    if not region_sales.empty:
        fig, ax = plt.subplots(figsize=(10, 4))
        region_sales.plot(kind="bar", ax=ax, color="#4facfe")
        ax.set_ylabel("Revenue")
        ax.set_title("Revenue by Region")
        fig.tight_layout()
        render_section("Revenue by Region", "Sales across regions", fig)
        region_sales_fig = fig

    # Recommendations
    recommendations = []
    if avg_order_value < 500:
        recommendations.append("- Consider offering bundle discounts to increase average order value.")
    recommendations.append(f"- Focus marketing on the top product: {top_product}.")
    if not region_sales.empty and region_sales.max() / region_sales.min() > 2:
        recommendations.append("- Expand sales efforts in underperforming regions.")

    st.markdown("**Recommendations:**")
    for rec in recommendations:
        st.markdown(rec)

    # Generate PDF report with summary
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    elements = []

    # Summary Section
    elements.append(Paragraph("Sales Summary", styles['Heading1']))
    elements.append(Spacer(1, 12))
    elements.append(Paragraph(f"Total Revenue: ₹ {total_revenue:,.0f}", styles['Heading2']))
    elements.append(Paragraph(f"Average Order Value: ₹ {avg_order_value:,.0f}", styles['Heading2']))
    elements.append(Paragraph(f"Top Product: {top_product}", styles['Heading2']))
    elements.append(Spacer(1, 12))

    if peak_month and low_month:
        elements.append(Paragraph(f"Seasonality Insight: Highest revenue in {peak_month}, lowest in {low_month}", styles['Normal']))
        elements.append(Spacer(1, 12))

    elements.append(Paragraph("Recommendations:", styles['Heading2']))
    for rec in recommendations:
        elements.append(Paragraph(rec, styles['Normal']))
    elements.append(Spacer(1, 12))

    # Add Charts
    for fig in [monthly_sales_fig, top_products_fig, region_sales_fig]:
        if fig is not None:
            buf = io.BytesIO()
            fig.savefig(buf, format='png', bbox_inches='tight', dpi=150)
            buf.seek(0)
            img = Image(buf, width=500, height=250)
            elements.append(img)
            elements.append(Spacer(1, 12))

    doc.build(elements)

    st.download_button(
        label="Download PDF Report",
        data=pdf_buffer.getvalue(),
        file_name="sales_report.pdf",
        mime="application/pdf"
    )
