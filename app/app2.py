import os
import pandas as pd
from joblib import load
import streamlit as st
from sklearn.metrics import silhouette_score, silhouette_samples
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import chardet

# Ustawienia Streamlit
st.set_page_config(page_title="K-Means Clustering - Load Model", layout="wide")

# Ścieżki domyślne
rfm_dir = "C:/Users/nazwa/Documents/datascience/infoshare/big_data_project/jdszr16-datapaparapa/data/processed"
model_dir = "C:/Users/nazwa/Documents/datascience/infoshare/big_data_project/jdszr16-datapaparapa/models"

# Wczytywanie plików z katalogów
st.sidebar.header("Wczytaj dane")

rfm_files = os.listdir(rfm_dir)
model_files = os.listdir(model_dir)

selected_rfm_file = st.sidebar.selectbox("Wybierz plik RFM (CSV)", rfm_files + ["Prześlij plik..."])
selected_model_file = st.sidebar.selectbox("Wybierz model K-Means (joblib)", model_files + ["Prześlij plik..."])

# Obsługa przesyłania plików
rfm_file = None
model_file = None

if selected_rfm_file == "Prześlij plik...":
    rfm_file = st.sidebar.file_uploader("Prześlij plik RFM (CSV)", type=["csv"])
else:
    rfm_file = os.path.join(rfm_dir, selected_rfm_file)

if selected_model_file == "Prześlij plik...":
    model_file = st.sidebar.file_uploader("Prześlij model K-Means (joblib)", type=["joblib"])
else:
    model_file = os.path.join(model_dir, selected_model_file)

# Jeśli użytkownik załadował pliki
if rfm_file and model_file:
    # Wczytywanie danych RFM z obsługą błędów kodowania
    try:
        df_rfm = pd.read_csv(rfm_file)
    except UnicodeDecodeError:
        st.warning("Nie udało się wczytać pliku z kodowaniem UTF-8. Próbuję wykryć kodowanie...")
        with open(rfm_file, 'rb') as f:
            result = chardet.detect(f.read())
            detected_encoding = result['encoding']
        st.info(f"Wykryte kodowanie: {detected_encoding}")
        df_rfm = pd.read_csv(rfm_file, encoding=detected_encoding)

    st.write("Wczytane dane RFM:", df_rfm.head())

    # Wczytywanie modelu K-Means
    kmeans = load(model_file)
    st.sidebar.success("Model K-Means załadowano!")

    # Sprawdzanie liczby klastrów w modelu
    st.sidebar.write(f"Liczba klastrów w modelu: {kmeans.n_clusters}")
    if kmeans.n_clusters <= 1:
        st.error("Model został wytrenowany z liczbą klastrów <= 1. Aby obliczyć Silhouette Score, liczba klastrów musi być większa niż 1.")
        st.stop()

    # Pobranie wymaganych kolumn z modelu
    if hasattr(kmeans, "feature_names_in_"):
        required_features = list(kmeans.feature_names_in_)
        st.sidebar.write(f"Model oczekuje kolumn: {required_features}")
    else:
        required_features = ['recency', 'frequency', 'monetary']
        st.sidebar.warning("Model nie zawiera informacji o nazwach cech. Używam domyślnego zestawu: recency, frequency, monetary")

    # Dynamiczne przekształcanie danych
    for feature in required_features:
        if feature == 'monetary_log' and feature not in df_rfm.columns:
            if 'monetary' in df_rfm.columns:
                monetary_max = df_rfm['monetary'].max()
                if monetary_max > 10:
                    st.warning(f"Dane w kolumnie 'monetary' nie są logarytmowane (max: {monetary_max:.2f}). Wykonuję logarytmowanie...")
                    df_rfm['monetary_log'] = np.log1p(df_rfm['monetary'])
                else:
                    st.info(f"Dane w kolumnie 'monetary' są już logarytmowane (max: {monetary_max:.2f}).")
                    df_rfm['monetary_log'] = df_rfm['monetary']
            else:
                st.error("Dane nie zawierają wymaganej kolumny 'monetary' lub 'monetary_log'.")
                st.stop()

    # Wyświetlenie zakresu danych wejściowych
    st.subheader("Zakres danych wejściowych")
    for col in required_features:
        if col in df_rfm.columns:
            st.write(f"{col}: min={df_rfm[col].min():.2f}, max={df_rfm[col].max():.2f}")
        else:
            st.error(f"Kolumna {col} jest wymagana, ale nie została znaleziona w danych.")
            st.stop()

    # Przetwarzanie danych do modelu
    df_rfm_scaled = df_rfm[required_features].values
    st.write("Dane wejściowe dopasowane do modelu:", pd.DataFrame(df_rfm_scaled, columns=required_features).head())

    # Przewidywanie klastrów dla załadowanych danych
    df_rfm['cluster'] = kmeans.predict(df_rfm_scaled)
    st.write("Dane z przypisanymi klastrami:", df_rfm.head())

    # Obliczanie silhouette score
    unique_clusters = np.unique(df_rfm['cluster'])
    if len(unique_clusters) > 1:
        silhouette_avg = silhouette_score(df_rfm_scaled, df_rfm['cluster'])
        st.sidebar.write(f"Silhouette Score: {silhouette_avg:.2f}")

        # Wizualizacja rozkładu silhouette scores
        silhouette_values = silhouette_samples(df_rfm_scaled, df_rfm['cluster'])

        st.subheader("Rozkład silhouette scores")
        fig, ax = plt.subplots(figsize=(8, 6))
        sns.histplot(silhouette_values, bins=30, kde=True, color='blue', ax=ax)
        ax.set_title("Silhouette Score Distribution")
        ax.set_xlabel("Silhouette Score")
        ax.set_ylabel("Frequency")
        st.pyplot(fig)

        # Wizualizacja 3D klastrów
        st.subheader("Wizualizacja klastrów 3D")
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(
            df_rfm_scaled[:, 0],
            df_rfm_scaled[:, 1],
            df_rfm_scaled[:, 2],
            c=df_rfm['cluster'],
            cmap='viridis',
            s=50
        )
        ax.set_title("Klastry 3D")
        ax.set_xlabel("Feature 1")
        ax.set_ylabel("Feature 2")
        ax.set_zlabel("Feature 3")
        st.pyplot(fig)
    else:
        st.error(f"Model przypisał wszystkie próbki do jednego klastra ({unique_clusters[0]}). Obliczenie Silhouette Score jest niemożliwe.")

    # Eksploracja klastrów
    st.subheader("Eksploracja klastrów")
    selected_cluster = st.selectbox("Wybierz klaster", df_rfm['cluster'].unique())
    st.write(df_rfm[df_rfm['cluster'] == selected_cluster])
else:
    st.info("Załaduj plik RFM (CSV) i model K-Means (joblib), aby rozpocząć.")