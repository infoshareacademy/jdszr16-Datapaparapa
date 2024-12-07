import streamlit as st

# Tytuł strony
st.title("Home")
st.write("Załaduj plik CSV")

# Uploader pliku
uploaded_file = st.file_uploader("Wgraj plik CSV", type="csv")

if uploaded_file is not None:
    # Wczytaj plik do DataFrame
    df_sales = pd.read_csv(uploaded_file)

    # Wyświetl podgląd danych
    st.write("Podgląd danych:")
    st.dataframe(df_sales.head())