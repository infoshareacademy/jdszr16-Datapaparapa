import streamlit as st
import pandas as pd

st.title("Dashboard - Analiza Danych")

# Możliwość wgrania pliku
uploaded_file = st.file_uploader("Wgraj plik CSV", type=["csv"])

if not uploaded_file:
    st.warning("Proszę wgrać plik, aby zobaczyć dane.")
else:
    try:
        # Wczytanie danych
        df_sales = pd.read_csv(uploaded_file)

        # Konwersja event_time na datetime
        df_sales['event_time'] = pd.to_datetime(df_sales['event_time'])

        # Wybór zakresu dat
        min_date = df_sales['event_time'].min().date()
        max_date = df_sales['event_time'].max().date()

        start_date, end_date = st.date_input(
            "Wybierz zakres dat",
            [min_date, max_date],
            min_value=min_date,
            max_value=max_date
        )

        if start_date > end_date:
            st.error("Data początkowa nie może być późniejsza niż data końcowa.")
        else:
            # Filtrowanie danych po zakresie dat
            filtered_df = df_sales[(df_sales['event_time'].dt.date >= start_date) & 
                                   (df_sales['event_time'].dt.date <= end_date)]

            if filtered_df.empty:
                st.warning("Brak danych dla wybranego zakresu dat.")
            else:
                # Obliczenia podstawowych metryk
                total_transactions = filtered_df.shape[0]
                total_revenue = filtered_df['price'].sum()
                average_transaction_value = filtered_df['price'].mean()
                unique_users = filtered_df['user_id'].nunique()
                average_transactions_per_user = total_transactions / unique_users
                ltv = total_revenue / unique_users

                # Wyświetlenie metryk w 3 kolumnach
                col1, col2, col3 = st.columns(3)

                with col1:
                    st.metric("Całkowita liczba transakcji", total_transactions)
                    st.divider()
                    st.metric("Średnia liczba zakupów na użytkownika", f"{average_transactions_per_user:.2f}")

                with col2:
                    st.metric("Całkowita wartość transakcji", f"${total_revenue:,.2f}")
                    st.divider()
                    st.metric("Customer Lifetime Value (LTV)", f"${ltv:,.2f}")

                with col3:
                    st.metric("Średnia wartość jednej transakcji", f"${average_transaction_value:,.2f}")
                    st.divider()
                    st.metric("Liczba unikalnych użytkowników", unique_users)

    except Exception as e:
        st.error(f"Nie udało się przetworzyć pliku: {str(e)}")

st.divider()

