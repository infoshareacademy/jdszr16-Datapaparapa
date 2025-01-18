import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, silhouette_samples
from joblib import dump, load
import streamlit as st

# Ustawienia strony
st.set_page_config(page_title="K-Means Clustering for Cosmetics", layout="wide")

# Sekcja wczytywania danych
st.title("K-Means Clustering for Cosmetics")
st.sidebar.header("Dane i parametry")

folder_path = st.sidebar.text_input("Ścieżka do folderu z danymi", 
                                    'C:/Users/nazwa/Documents/datascience/infoshare/big_data_project/jdszr16-datapaparapa/data/raw/cosmetics/')
files = [file for file in os.listdir(folder_path) if file.endswith('.csv')]

# Wczytanie danych
@st.cache_data
def load_data(folder_path, files):
    df_list = [pd.read_csv(os.path.join(folder_path, file)) for file in files]
    df = pd.concat(df_list, ignore_index=True)
    return df

df = load_data(folder_path, files)
st.write("Wczytano dane:", df.head())

# Filtracja danych
df_filtered = df[(df['event_type'] == 'purchase') & (df['price'] > 0)]
df_filtered['event_time'] = pd.to_datetime(df_filtered['event_time'])

# Obliczanie RFM
df_rfm = df_filtered.groupby('user_id').agg(
    recency=('event_time', lambda x: (x.max() - x.min()).days),
    frequency=('user_id', 'count'),
    monetary=('price', 'sum')
).reset_index()

df_rfm['monetary_log'] = np.log(df_rfm['monetary'] + 1)

# Skalowanie cech
scaler = StandardScaler()
df_rfm_scaled = scaler.fit_transform(df_rfm[['recency', 'frequency', 'monetary_log']])
df_rfm_scaled = pd.DataFrame(df_rfm_scaled, columns=['recency', 'frequency', 'monetary_log'])

# K-Means - liczba klastrów
num_clusters = st.sidebar.slider("Liczba klastrów", min_value=2, max_value=10, value=5)

# Klasteryzacja
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
df_rfm['cluster'] = kmeans.fit_predict(df_rfm_scaled)

# Silhouette score
silhouette_avg = silhouette_score(df_rfm_scaled, df_rfm['cluster'])
st.sidebar.write(f"Silhouette Score: {silhouette_avg:.2f}")

# Wizualizacja wyników
st.subheader("Wyniki klastrowania")
st.write(df_rfm.groupby('cluster').mean())

# Elbow Method
SSE = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, random_state=42)
    kmeans.fit(df_rfm_scaled)
    SSE.append(kmeans.inertia_)

fig, ax = plt.subplots(figsize=(8, 6))
ax.plot(range(1, 11), SSE, marker='o', linestyle='--')
ax.set_title("Elbow Method for Optimal K")
ax.set_xlabel("Number of Clusters")
ax.set_ylabel("Sum of Squared Errors (SSE)")
st.pyplot(fig)

# Rozkład silhouette scores
silhouette_values = silhouette_samples(df_rfm_scaled, df_rfm['cluster'])

fig, ax = plt.subplots(figsize=(8, 6))
sns.histplot(silhouette_values, bins=30, kde=True, color='blue', ax=ax)
ax.set_title("Silhouette Score Distribution")
ax.set_xlabel("Silhouette Score")
ax.set_ylabel("Frequency")
st.pyplot(fig)

# Eksploracja klastrów
st.subheader("Eksploracja klastrów")
selected_cluster = st.selectbox("Wybierz klaster", df_rfm['cluster'].unique())
st.write(df_rfm[df_rfm['cluster'] == selected_cluster])

# Zapis modelu
save_model = st.sidebar.button("Zapisz model")
if save_model:
    base_dir = folder_path
    models_dir = os.path.join(base_dir, 'models')
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, f'model_kmeans_{num_clusters}.joblib')
    dump(kmeans, model_path)
    st.sidebar.success(f"Model zapisano w: {model_path}")
