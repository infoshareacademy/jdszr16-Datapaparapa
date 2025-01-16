import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import plotly.express as px
import plotly.graph_objects as go
import os

# Funkcja do ładowania danych
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"Błąd podczas ładowania danych: {e}")
        return None

# Funkcja do ładowania modelu
@st.cache_resource
def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Błąd podczas ładowania modelu: {e}")
        return None

# Funkcja do wizualizacji 2D klastrów
def visualize_clusters_2d(data, labels):
    try:
        plt.figure(figsize=(10, 6))
        plt.scatter(data['recency'], data['frequency'], c=labels, cmap='viridis', alpha=0.7)
        plt.colorbar(label="Segment")
        plt.xlabel("Recency")
        plt.ylabel("Frequency")
        plt.title("Wizualizacja klastrów (2D)")
        st.pyplot(plt)
    except Exception as e:
        st.error(f"Błąd podczas wizualizacji klastrów 2D: {e}")

# Funkcja do wizualizacji 3D klastrów statycznych
def visualize_clusters_3d(data, labels):
    try:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(data['recency'], data['frequency'], data['monetary'], c=labels, cmap='viridis', alpha=0.7)
        ax.set_xlabel("Recency")
        ax.set_ylabel("Frequency")
        ax.set_zlabel("Monetary")
        ax.set_title("Wizualizacja klastrów (3D - statyczna)")
        fig.colorbar(scatter, label="Segment")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Błąd podczas wizualizacji klastrów 3D: {e}")

# Funkcja do wizualizacji 3D dynamicznej
def visualize_clusters_3d_dynamic(data, labels):
    try:
        fig = px.scatter_3d(
            data, x='recency', y='frequency', z='monetary',
            color=labels.astype(str),
            title="Wizualizacja klastrów (3D - dynamiczna)",
            labels={'color': 'Segment'}
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Błąd podczas dynamicznej wizualizacji klastrów 3D: {e}")

# Funkcja do podsumowania klastrów
def summarize_clusters(data, labels):
    try:
        data['Segment'] = labels
        summary = data.groupby('Segment').agg(
            recency_mean=('recency', 'mean'),
            frequency_mean=('frequency', 'mean'),
            monetary_mean=('monetary', 'mean'),
            user_count=('Segment', 'count')
        ).reset_index()
        st.subheader("Podsumowanie klastrów")
        st.dataframe(summary)
        return summary
    except Exception as e:
        st.error(f"Błąd podczas podsumowania klastrów: {e}")
        return None

# Główna funkcja aplikacji
def main():
    st.title("Aplikacja do analizy RFM i segmentacji klientów")
    st.sidebar.header("Konfiguracja")

    # Ścieżki do danych
    rfm_file = st.sidebar.text_input(
        "Ścieżka do pliku CSV z danymi RFM", 
        value="C:/Users/nazwa/Documents/datascience/infoshare/big_data_project/jdszr16-datapaparapa/data/processed/rfm_data_05_org.csv"
    )
    model_file = st.sidebar.text_input(
        "Ścieżka do modelu K-Means", 
        value="C:/Users/nazwa/Documents/datascience/infoshare/big_data_project/jdszr16-datapaparapa/models/model_kmeans_cosmetic_05_org.joblib"
    )

    # Przycisk do załadowania danych i modelu
    if st.sidebar.button("Załaduj dane i model"):
        rfm_data = load_data(rfm_file)  # Wczytaj dane RFM
        model = load_model(model_file)  # Wczytaj model K-Means

        if rfm_data is not None and model is not None:
            st.write("**Podgląd danych RFM:**")
            st.dataframe(rfm_data.head())

            try:
                # Weryfikacja obecności wymaganych kolumn
                required_columns = ['recency', 'frequency', 'monetary']
                if all(col in rfm_data.columns for col in required_columns):
                    # Predykcja segmentów
                    labels = model.predict(rfm_data[required_columns])
                    rfm_data['Segment'] = labels

                    st.write("**Dane z przypisanymi segmentami:**")
                    st.dataframe(rfm_data.head())

                    # Wizualizacja
                    st.subheader("Wizualizacja klastrów (2D)")
                    visualize_clusters_2d(rfm_data, labels)

                    st.subheader("Wizualizacja klastrów (3D - statyczna)")
                    visualize_clusters_3d(rfm_data, labels)

                    st.subheader("Wizualizacja klastrów (3D - dynamiczna)")
                    visualize_clusters_3d_dynamic(rfm_data, labels)

                    # Podsumowanie klastrów
                    summarize_clusters(rfm_data, labels)
                else:
                    st.error(f"Dane nie zawierają wymaganych kolumn: {required_columns}")
            except Exception as e:
                st.error(f"Błąd podczas predykcji lub wizualizacji: {e}")

if __name__ == "__main__":
    main()
