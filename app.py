import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="Análisis de vehículos usados",
    page_icon="🚗",
    layout="wide"
)

st.title("🚗 Panel de análisis de anuncios de vehículos usados")

st.write(
    """
    Esta aplicación permite explorar un conjunto de datos
    de anuncios de venta de vehículos usados.
    """
)


@st.cache_data
def load_data():

    df = pd.read_csv("vehicles_us.csv")

    df["date_posted"] = pd.to_datetime(df["date_posted"])

    df["is_4wd"] = df["is_4wd"].fillna(0).astype(int)

    df["paint_color"] = df["paint_color"].fillna("unknown")

    df["model_year"] = df["model_year"].fillna(
        df["model_year"].median()
    )

    df["cylinders"] = df["cylinders"].fillna(
        df["cylinders"].median()
    )

    df["odometer"] = df["odometer"].fillna(
        df["odometer"].median()
    )

    df["model_year"] = df["model_year"].astype(int)

    df["cylinders"] = df["cylinders"].astype(int)

    return df


df = load_data()

st.subheader("Vista previa del dataset")

if st.checkbox("Mostrar tabla de datos"):
    st.dataframe(df)

st.subheader("Histograma de precios")

fig_hist = px.histogram(
    df,
    x="price",
    nbins=50,
    title="Distribución de precios"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.subheader("Relación precio vs kilometraje")

fig_scatter = px.scatter(
    df,
    x="odometer",
    y="price",
    color="condition",
    title="Precio vs kilometraje",
    opacity=0.5
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.subheader("Cantidad de vehículos por tipo")

type_data = df["type"].value_counts().reset_index()

type_data.columns = ["type", "count"]

fig_bar = px.bar(
    type_data,
    x="type",
    y="count",
    title="Vehículos por tipo"
)

st.plotly_chart(fig_bar, use_container_width=True)