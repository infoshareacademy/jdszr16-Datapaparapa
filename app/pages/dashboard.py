import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

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

                # Analiza zakupów wg godzin, dni tygodnia i miesięcy
                cart_data = filtered_df[filtered_df['event_type'] == 'purchase']

                if not cart_data.empty:
                    cart_data['hour'] = cart_data['event_time'].dt.hour
                    cart_data['day_of_week'] = cart_data['event_time'].dt.day_name()
                    cart_data['month'] = cart_data['event_time'].dt.month_name()

                    # Sortowanie dni tygodnia
                    day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
                    cart_data['day_of_week'] = pd.Categorical(cart_data['day_of_week'], categories=day_order, ordered=True)

                    # Suma wartości zakupów wg godzin (Plotly)
                    hourly_revenue = cart_data.groupby('hour')['price'].sum().reset_index()
                    fig_hourly = px.bar(hourly_revenue, x='hour', y='price', labels={'hour': 'Godzina', 'price': 'Suma wartości zakupów'},
                                        title="Suma wartości zakupów wg godzin", color_discrete_sequence=["#636EFA"])
                    st.plotly_chart(fig_hourly)

                    # Suma wartości zakupów wg dni tygodnia (Plotly)
                    daily_revenue = cart_data.groupby('day_of_week')['price'].sum().reset_index()
                    fig_daily = px.bar(daily_revenue, x='day_of_week', y='price', labels={'day_of_week': 'Dzień tygodnia', 'price': 'Suma wartości zakupów'},
                                       title="Suma wartości zakupów wg dni tygodnia", color_discrete_sequence=["#EF553B"])
                    st.plotly_chart(fig_daily)

                    # Suma wartości zakupów wg miesięcy (Plotly)
                    monthly_revenue = cart_data.groupby('month')['price'].sum().reset_index()
                    fig_monthly = px.bar(monthly_revenue, x='month', y='price', labels={'month': 'Miesiąc', 'price': 'Suma wartości zakupów'},
                                         title="Suma wartości zakupów wg miesięcy", color_discrete_sequence=["#00CC96"])
                    st.plotly_chart(fig_monthly)

    except Exception as e:
        st.error(f"Nie udało się przetworzyć pliku: {str(e)}")

st.divider()
