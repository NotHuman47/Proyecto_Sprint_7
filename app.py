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
    Esta aplicación permite explorar un conjunto de datos de anuncios de venta
    de vehículos usados. Puedes filtrar los datos por tipo de vehículo,
    condición y rango de precio para analizar patrones de mercado.
    """
)


@st.cache_data
def load_data():
    df = pd.read_csv("vehicles_us.csv")

    df["date_posted"] = pd.to_datetime(df["date_posted"])
    df["is_4wd"] = df["is_4wd"].fillna(0).astype(int)
    df["paint_color"] = df["paint_color"].fillna("unknown")

    df["model_year"] = df["model_year"].fillna(df["model_year"].median())
    df["cylinders"] = df["cylinders"].fillna(df["cylinders"].median())
    df["odometer"] = df["odometer"].fillna(df["odometer"].median())

    df["model_year"] = df["model_year"].astype(int)
    df["cylinders"] = df["cylinders"].astype(int)

    return df


df = load_data()

st.sidebar.header("Filtros del dashboard")

selected_type = st.sidebar.multiselect(
    "Tipo de vehículo",
    options=sorted(df["type"].dropna().unique()),
    default=sorted(df["type"].dropna().unique())
)

selected_condition = st.sidebar.multiselect(
    "Condición",
    options=sorted(df["condition"].dropna().unique()),
    default=sorted(df["condition"].dropna().unique())
)

price_range = st.sidebar.slider(
    "Rango de precio",
    min_value=int(df["price"].min()),
    max_value=int(df["price"].max()),
    value=(int(df["price"].min()), int(df["price"].max()))
)

filtered_df = df[
    (df["type"].isin(selected_type))
    & (df["condition"].isin(selected_condition))
    & (df["price"].between(price_range[0], price_range[1]))
]

st.subheader("Indicadores principales")

col1, col2, col3 = st.columns(3)

col1.metric("Total de anuncios", f"{len(filtered_df):,}")
col2.metric("Precio promedio", f"${filtered_df['price'].mean():,.0f}")
col3.metric("Odómetro promedio", f"{filtered_df['odometer'].mean():,.0f} mi")

st.subheader("Vista previa del dataset filtrado")

if st.checkbox("Mostrar tabla de datos"):
    st.dataframe(filtered_df)

st.subheader("Histograma de precios")

fig_hist = px.histogram(
    filtered_df,
    x="price",
    nbins=50,
    title="Distribución de precios"
)

st.plotly_chart(fig_hist, use_container_width=True)

st.write(
    """
    Este histograma permite observar en qué rangos de precio se concentran
    la mayoría de los vehículos anunciados.
    """
)

st.subheader("Relación precio vs kilometraje")

fig_scatter = px.scatter(
    filtered_df,
    x="odometer",
    y="price",
    color="condition",
    title="Precio vs kilometraje por condición",
    opacity=0.5
)

st.plotly_chart(fig_scatter, use_container_width=True)

st.write(
    """
    Este gráfico de dispersión ayuda a observar si existe una relación entre
    el kilometraje del vehículo y su precio de venta.
    """
)

st.subheader("Cantidad de vehículos por tipo")

type_data = filtered_df["type"].value_counts().reset_index()
type_data.columns = ["type", "count"]

fig_bar = px.bar(
    type_data,
    x="type",
    y="count",
    title="Vehículos por tipo"
)

st.plotly_chart(fig_bar, use_container_width=True)

st.write(
    """
    Este gráfico muestra qué tipos de vehículos aparecen con mayor frecuencia
    dentro del conjunto de anuncios filtrado.
    """
)