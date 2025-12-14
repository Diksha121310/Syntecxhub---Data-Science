import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io, base64
from utils import calculate_health_kpis
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet

st.set_page_config(page_title="Health Dashboard", layout="wide")

with open("styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

with open("templates/header.html") as f:
    st.markdown(f.read(), unsafe_allow_html=True)

def render_section(title, subtitle, fig=None):
    with open("templates/section.html") as f:
        template = f.read()

    if fig:
        buf = io.BytesIO()
        fig.savefig(buf, format="png", bbox_inches="tight", dpi=120)
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode()
        content = f'<img src="data:image/png;base64,{img_base64}" width="100%"/>'
    else:
        content = "<p>No data available</p>"

    html = (
        template.replace("{{ section_title }}", title)
                .replace("{{ section_subtitle }}", subtitle)
                .replace("{{ section_content }}", content)
    )
    st.markdown(html, unsafe_allow_html=True)

uploaded_file = st.file_uploader("Upload Health Dataset (CSV)", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.sidebar.header("Column Mapping")
    disease_col = st.sidebar.selectbox("Disease Column (0/1)", df.columns)

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns.tolist()
    feature_col = st.sidebar.selectbox("Health Metric", numeric_cols)

    df[disease_col] = pd.to_numeric(df[disease_col], errors="coerce")
    df[feature_col] = pd.to_numeric(df[feature_col], errors="coerce")
    df = df.dropna(subset=[disease_col, feature_col])
    df["Disease_Label"] = df[disease_col].map({0: "No Disease", 1: "Disease"})

    total, rate, avg, high = calculate_health_kpis(
        df, feature_col, feature_col, disease_col
    )

    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("Total Patients", total),
        ("Disease Rate (%)", f"{rate:.2f}"),
        (f"Avg {feature_col}", f"{avg:.2f}"),
        (f"High {feature_col}", high),
    ]

    for col, (title, value) in zip([col1, col2, col3, col4], kpis):
        col.markdown(
            f"""
            <div class="metric-box">
                <div class="metric-title">{title}</div>
                <div class="metric-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    fig, ax = plt.subplots(figsize=(6, 4))
    df["Disease_Label"].value_counts().plot(kind="bar", ax=ax)
    ax.set_title("Disease Distribution")
    ax.set_xlabel("Status")
    ax.set_ylabel("Patients")
    fig.tight_layout()
    render_section("Disease Distribution", "Overall health condition spread", fig)

    fig, ax = plt.subplots(figsize=(6, 4))
    df.boxplot(column=feature_col, by="Disease_Label", ax=ax)
    ax.set_title(f"{feature_col} vs Disease")
    ax.set_xlabel("Disease Status")
    ax.set_ylabel(feature_col)
    plt.suptitle("")
    fig.tight_layout()
    render_section(
        f"{feature_col} Analysis",
        f"Distribution of {feature_col} across disease status",
        fig
    )

    try:
        df["Risk_Group"] = pd.qcut(
            df[feature_col], 4, labels=["Low", "Medium", "High", "Very High"]
        )
        risk = df.groupby("Risk_Group")["Disease_Label"].value_counts().unstack()

        fig, ax = plt.subplots(figsize=(6, 4))
        risk.plot(kind="bar", ax=ax)
        ax.set_title("Disease Prevalence by Risk Group")
        ax.set_ylabel("Patients")
        fig.tight_layout()
        render_section("Risk Group Analysis", "Disease prevalence by feature level", fig)
    except:
        pass

    st.markdown("Actionable Insights")

    st.markdown(f"""
    - Patients with **higher {feature_col} values** show increased disease prevalence.
    - Overall disease rate is **{rate:.2f}%**, indicating moderate risk across population.
    - Preventive screenings should focus on **High & Very High risk groups**.
    """)

    if st.button("Generate Health Report"):
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        elements = []

        elements.append(Paragraph("Health Analytics Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Total Patients: {total}", styles['Normal']))
        elements.append(Paragraph(f"Disease Rate: {rate:.2f}%", styles['Normal']))
        elements.append(Paragraph(f"Average {feature_col}: {avg:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))

        for fig in plt.get_fignums():
            buf = io.BytesIO()
            plt.figure(fig).savefig(buf, format="png", bbox_inches="tight")
            buf.seek(0)
            elements.append(Image(buf, width=400, height=250))
            elements.append(Spacer(1, 12))

        doc.build(elements)
        buffer.seek(0)

        st.download_button(
            "Download PDF",
            buffer,
            file_name="health_report.pdf",
            mime="application/pdf"
        )
