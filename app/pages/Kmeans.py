import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import plotly.express as px


@st.cache_data
def load_data(uploaded_file):

    try:
        data = pd.read_csv(uploaded_file)
        return data
    except Exception as e:
        st.error(f"Błąd podczas ładowania danych: {e}")
        return None

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

def visualize_clusters_3d(data, labels):

    try:
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        scatter = ax.scatter(
            data['recency'],
            data['frequency'],
            data['monetary'],
            c=labels,
            cmap='viridis',
            alpha=0.7
        )
        ax.set_xlabel("Recency")
        ax.set_ylabel("Frequency")
        ax.set_zlabel("Monetary")
        ax.set_title("Wizualizacja klastrów (3D - statyczna)")
        fig.colorbar(scatter, label="Segment")
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Błąd podczas wizualizacji klastrów 3D: {e}")

def visualize_clusters_3d_dynamic(data, labels):

    try:
        fig = px.scatter_3d(
            data,
            x='recency',
            y='frequency',
            z='monetary',
            color=labels.astype(str),
            title="Wizualizacja klastrów (3D - dynamiczna)",
            labels={'color': 'Segment'}
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Błąd podczas dynamicznej wizualizacji klastrów 3D: {e}")

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

def main():
    st.title("Wizualizacja klastrów z gotowego modelu K-Means")

    # 1. Ładowanie modelu .joblib (z konkretnej ścieżki)
    try:
        loaded_model = joblib.load('C:\jdszr16-datapaparapa\models\model_kmeans_cosmetic_05_org.joblib')
        st.success("Pomyślnie załadowano model K-Means z pliku .joblib!")
    except Exception as e:
        st.error(f"Nie udało się załadować modelu: {e}")
        st.stop()

    # 2. Wgranie pliku CSV z danymi RFM
    uploaded_file = st.file_uploader("Wgraj plik CSV z danymi RFM (kolumny: recency, frequency, monetary)", type=["csv"])

    if uploaded_file is not None:
        # 2a. Wczytanie danych
        rfm_data = load_data(uploaded_file)
        if rfm_data is not None:
            if all(col in rfm_data.columns for col in ['recency', 'frequency', 'monetary']):
                st.write("**Podgląd danych RFM (pierwsze 5 wierszy):**")
                st.dataframe(rfm_data.head())

                # 3. Predykcja klastrów
                try:
                    labels = loaded_model.predict(rfm_data[['recency', 'frequency', 'monetary']])
                    rfm_data['Segment'] = labels
                    st.write("**Dane z przypisanymi segmentami:**")
                    st.dataframe(rfm_data.head())

                    # 4. Wizualizacje
                    st.subheader("Wizualizacja klastrów (2D)")
                    visualize_clusters_2d(rfm_data, labels)

                    st.subheader("Wizualizacja klastrów (3D - statyczna)")
                    visualize_clusters_3d(rfm_data, labels)

                    st.subheader("Wizualizacja klastrów (3D - dynamiczna)")
                    visualize_clusters_3d_dynamic(rfm_data, labels)

                    # 5. Podsumowanie klastrów
                    summarize_clusters(rfm_data, labels)

                except Exception as e:
                    st.error(f"Błąd podczas predykcji lub wizualizacji: {e}")

            else:
                st.error("Dane nie zawierają kolumn [recency, frequency, monetary].")
    else:
        st.info("Wgraj plik CSV, aby zobaczyć wizualizacje klastrów.")

if __name__ == "__main__":
    main()
