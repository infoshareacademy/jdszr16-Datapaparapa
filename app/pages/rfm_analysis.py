import streamlit as st
import pandas as pd
import os
import plotly.express as px

# Tytuł aplikacji
st.title("Aplikacja do analizy RFM i więcej")
st.write("Załaduj plik CSV, a następnie kliknij przycisk, aby przeprowadzić analizę RFM.")

# Uploader pliku
uploaded_file = st.file_uploader("Wgraj plik CSV", type="csv")

if uploaded_file is not None:
    # Wczytaj plik do DataFrame
    df_sales = pd.read_csv(uploaded_file)

    # Konwersja kolumny user_id na string
    df_sales['user_id'] = df_sales['user_id'].astype(str)
    # Konwersja kolumny "event_time" na datetime (jeśli nie jest w tym formacie)
    df_sales['event_time'] = pd.to_datetime(df_sales['event_time'])

    # Wyświetl podgląd danych
    st.write("Podgląd danych:")
    st.dataframe(df_sales.head())

    # Przycisk do uruchomienia analizy
    if st.button("Przeprowadź analizę RFM"):

        # Obliczenie Recency, Frequency i Monetary
        df_sales.loc[:,'Recency'] = (df_sales["event_time"].max() - df_sales["event_time"]).dt.days
        df_R=df_sales.groupby('user_id')['Recency'].min().reset_index().rename(columns={"0":"Recency"})
        df_F = df_sales.groupby('user_id')['event_type'].count().reset_index().rename(columns={"event_type": "Frequency"})
        df_M = df_sales.groupby('user_id')['price'].sum().reset_index().rename(columns={"price": "Monetary"})

        # Połączenie danych w jeden DataFrame
        df_RF = pd.merge(df_R, df_F, on='user_id')
        df_RFM = pd.merge(df_RF, df_M, on='user_id')

        # Obliczenie kwantyli jako skalarów
        quantiles_R = df_RFM['Recency'].quantile([0.25, 0.50, 0.75]).to_dict()
        quantiles_F = df_RFM['Frequency'].quantile([0.25, 0.50, 0.75]).to_dict()
        quantiles_M = df_RFM['Monetary'].quantile([0.25, 0.50, 0.75]).to_dict()

        # Funkcje do scoringu RFM
        def recency_scoring(rfm):
            if rfm.Recency <= quantiles_R[0.25]:
                return 4
            elif rfm.Recency <= quantiles_R[0.50]:
                return 3
            elif rfm.Recency <= quantiles_R[0.75]:
                return 2
            else:
                return 1

        def frequency_scoring(rfm):
            if rfm.Frequency >= quantiles_F[0.75]:
                return 4
            elif rfm.Frequency >= quantiles_F[0.50]:
                return 3
            elif rfm.Frequency >= quantiles_F[0.25]:
                return 2
            else:
                return 1

        def monetary_scoring(rfm):
            if rfm.Monetary >= quantiles_M[0.75]:
                return 4
            elif rfm.Monetary >= quantiles_M[0.50]:
                return 3
            elif rfm.Monetary >= quantiles_M[0.25]:
                return 2
            else:
                return 1

        # Dodanie kolumn scoringowych
        df_RFM['Recency_Score'] = df_RFM.apply(recency_scoring, axis=1)
        df_RFM['Frequency_Score'] = df_RFM.apply(frequency_scoring, axis=1)
        df_RFM['Monetary_Score'] = df_RFM.apply(monetary_scoring, axis=1)


        # Tworzenie ogólnego RFM Score
        df_RFM['Customer_RFM_Score'] = df_RFM['Recency_Score'].astype(str) + df_RFM['Frequency_Score'].astype(str) + df_RFM['Monetary_Score'].astype(str)

        # Funkcja do kategoryzacji klientów
        def categorizer(rfm):
            if (rfm[0] in ['2', '3', '4']) and (rfm[1] in ['4']) and (rfm[2] in ['4']):
                return 'Champion'
            elif (rfm[0] in ['3']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['3', '4']):
                return 'Top Loyal Customer'
            elif (rfm[0] in ['3']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['1', '2']):
                return 'Loyal Customer'
            elif (rfm[0] in ['4']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['3', '4']):
                return 'Top Recent Customer'
            elif (rfm[0] in ['4']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['1', '2']):
                return 'Recent Customer'
            elif (rfm[0] in ['2', '3']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['3', '4']):
                return 'Top Customer Needed Attention'
            elif (rfm[0] in ['2', '3']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['1', '2']):
                return 'Customer Needed Attention'
            elif (rfm[0] in ['1']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['3', '4']):
                return 'Top Lost Customer'
            elif (rfm[0] in ['1']) and (rfm[1] in ['1', '2', '3', '4']) and (rfm[2] in ['1', '2']):
                return 'Lost Customer'
            else:
                return 'Other'

        # Dodanie kolumny z kategorią klienta
        df_RFM['Customer_Category'] = df_RFM['Customer_RFM_Score'].apply(categorizer)

        # Wyświetlenie wyników
        st.write("Wyniki analizy RFM:")
        st.dataframe(df_RFM)

        # Obliczanie ilości użytkowników i procentowego udziału
        Size_RFM_Label = df_RFM['Customer_Category'].value_counts()
        Size_RFM_Label_df = pd.DataFrame(Size_RFM_Label).reset_index()
        Size_RFM_Label_df.columns = ['Customer_Category', 'Count']
        Size_RFM_Label_df['Percentage'] = (Size_RFM_Label_df['Count'] / Size_RFM_Label_df['Count'].sum()) * 100
        Size_RFM_Label_df['Label'] = Size_RFM_Label_df['Customer_Category'] + \
            '<br>' + Size_RFM_Label_df['Percentage'].round(2).astype(str) + '%'

        # Wizualizacja za pomocą Plotly
        st.write("Wizualizacja segmentacji klientów:")
        fig = px.treemap(
            Size_RFM_Label_df,
            path=['Label'],  # Wyświetlenie nazwy grupy z procentami
            values='Count',
            title="Segmentacja klientów (procentowy udział)",
            width=800, height=600
        )
        st.plotly_chart(fig)


        # Możliwość zapisania wyników
        if st.button("Zapisz wyniki do pliku CSV"):
            df_RFM.to_csv("wyniki_rfm.csv", index=False)
            st.success("Wyniki zostały zapisane jako 'wyniki_rfm.csv'.")


