import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from pathlib import Path

RAW_DATA_PATH = Path("data/openfoodfacts.csv")
CLEAN_DATA_PATH = Path("data/cleaned_openfoodfacts.csv")
CATEGORY_DATA_PATH = Path("data/cleaned_openfoodfacts_with_categories.csv.gz")
CATEGORY_GAP_PATH = Path("data/category_gap_summary.csv")
CATEGORY_RECOMMENDATION_PATH = Path("data/category_recommendation.txt")


@st.cache_data
def load_data():
    if CATEGORY_DATA_PATH.exists():
        data_path = CATEGORY_DATA_PATH
        df = pd.read_csv(data_path, compression="gzip", low_memory=False)
    elif CLEAN_DATA_PATH.exists():
        data_path = CLEAN_DATA_PATH
        df = pd.read_csv(data_path, low_memory=False)
    elif RAW_DATA_PATH.exists():
        data_path = RAW_DATA_PATH
        df = pd.read_csv(data_path, low_memory=False)
    else:
        raise FileNotFoundError(
            f"No dataset found. Place a cleaned dataset in {CATEGORY_DATA_PATH} or {CLEAN_DATA_PATH}, or the raw dataset in {RAW_DATA_PATH}.")

    return df, data_path


def compute_quadrants(df):
    protein_threshold = df["proteins_100g"].quantile(0.75)
    sugar_threshold = df["sugars_100g"].quantile(0.25)

    conditions = [
        (df["proteins_100g"] >= protein_threshold) & (df["sugars_100g"] <= sugar_threshold),
        (df["proteins_100g"] >= protein_threshold) & (df["sugars_100g"] > sugar_threshold),
        (df["proteins_100g"] < protein_threshold) & (df["sugars_100g"] <= sugar_threshold),
    ]

    choices = [
        "High Protein / Low Sugar",
        "High Protein / High Sugar",
        "Low Protein / Low Sugar",
    ]

    df = df.copy()
    df["quadrant"] = np.select(conditions, choices, default="Low Protein / High Sugar")
    return df, protein_threshold, sugar_threshold


@st.cache_data
def load_category_gap():
    if CATEGORY_GAP_PATH.exists():
        return pd.read_csv(CATEGORY_GAP_PATH)
    return None


@st.cache_data
def load_recommendation():
    if CATEGORY_RECOMMENDATION_PATH.exists():
        return CATEGORY_RECOMMENDATION_PATH.read_text()
    return None


def main():
    st.set_page_config(page_title="Snack Market Gap Analysis", layout="wide")
    st.title("Snack Market Gap Analysis")
    st.markdown(
        "Use this dashboard to explore the snack category opportunity uncovered in the Open Food Facts dataset. "
        "The charts and metrics are based on the notebook-cleaned dataset and the same category mapping logic.")

    try:
        df, data_path = load_data()

        if "primary_category" not in df.columns:
            st.warning(
                "The loaded dataset does not contain `primary_category`. "
                "Please use the category-assigned cleaned dataset or rerun User Story 2 in the notebook.")

        st.sidebar.header("Filters")
        categories = ["All"] + sorted(df["primary_category"].dropna().unique().tolist())
        selected_category = st.sidebar.selectbox("Primary category", categories, index=0)

        if selected_category != "All":
            df = df[df["primary_category"] == selected_category]

        df, protein_threshold, sugar_threshold = compute_quadrants(df)
        quadrant_counts = df["quadrant"].value_counts().reindex([
            "High Protein / Low Sugar",
            "High Protein / High Sugar",
            "Low Protein / Low Sugar",
            "Low Protein / High Sugar",
        ], fill_value=0)

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader("Dataset overview")
            st.metric("Rows loaded", f"{len(df):,}")
            st.metric("Categories available", f"{df['primary_category'].nunique():,}")
            st.write(f"**Source file:** `{data_path.name}`")
        with col2:
            st.subheader("Thresholds")
            st.metric("High protein threshold", f"{protein_threshold:.2f} g/100g")
            st.metric("Low sugar threshold", f"{sugar_threshold:.2f} g/100g")

        st.markdown("---")

        st.subheader("Quadrant counts")
        st.bar_chart(quadrant_counts)

        st.subheader("Sugar vs Protein Nutrient Matrix")
        fig = px.scatter(
            df,
            x="sugars_100g",
            y="proteins_100g",
            color="primary_category" if "primary_category" in df.columns else None,
            hover_data=["product_name", "primary_category", "sugars_100g", "proteins_100g", "quadrant"],
            title="Protein vs Sugar by Primary Category",
            width=1100,
            height=650,
            opacity=0.7,
        )
        fig.add_shape(
            type="line",
            x0=sugar_threshold,
            x1=sugar_threshold,
            y0=0,
            y1=df["proteins_100g"].max(),
            line=dict(color="black", dash="dash"),
        )
        fig.add_shape(
            type="line",
            x0=0,
            x1=df["sugars_100g"].max(),
            y0=protein_threshold,
            y1=protein_threshold,
            line=dict(color="black", dash="dash"),
        )
        fig.update_layout(legend_title_text="Primary Category")
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        st.subheader("Category opportunity ranking")
        category_gap = load_category_gap()
        if category_gap is not None:
            st.dataframe(category_gap.head(10))
        else:
            st.info(
                "Category gap summary is not available. Run the Category Market Gap Explorer in the notebook to generate `data/category_gap_summary.csv`."
            )

        recommendation_text = load_recommendation()
        if recommendation_text:
            st.subheader("Top category recommendation")
            st.info(recommendation_text)
        else:
            st.warning(
                "Category recommendation is not available. Run the Category Market Gap Explorer in the notebook to generate `data/category_recommendation.txt`."
            )

        st.markdown("---")
        with st.expander("View raw data sample"):
            st.dataframe(df.head(15))

    except FileNotFoundError as exc:
        st.error(str(exc))
        st.info("Place the notebook-generated dataset in the `data/` folder and rerun the app.")


if __name__ == "__main__":
    main()
