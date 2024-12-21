import streamlit as st
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from mlxtend.frequent_patterns import apriori, association_rules


# Tytuł strony
st.title("📊 Analiza Koszykowa")

# Sprawdzenie, czy plik został wgrany
if 'df_sales' not in st.session_state:
    st.warning("🚫 Proszę wgrać plik CSV na stronie głównej.")
    st.stop()

df_sales = st.session_state['df_sales']


# Funkcja do tworzenia gęstej macierzy
def create_dense_matrix(data, column):
    grouped_data = data.groupby('user_id')[column].apply(lambda x: ' '.join(map(str, x.unique())))
    vectorizer = CountVectorizer(binary=True, dtype=bool)
    sparse_matrix = vectorizer.fit_transform(grouped_data.astype(str))
    return pd.DataFrame(sparse_matrix.toarray(), columns=vectorizer.get_feature_names_out())


# Funkcja do generowania reguł asocjacyjnych
def generate_association_rules(data_df, min_support, min_confidence):
    frequent_itemsets = apriori(data_df, min_support=min_support, use_colnames=True)
    if frequent_itemsets.empty:
        return pd.DataFrame()  # Zwróć pustą ramkę danych, jeśli brak wyników
    rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=min_confidence)
    rules['antecedents'] = rules['antecedents'].apply(lambda x: ', '.join(list(x)))
    rules['consequents'] = rules['consequents'].apply(lambda x: ', '.join(list(x)))
    return rules


# Funkcja do zmiany nazw kolumn i skalowania do procentów
COLUMN_MAPPING = {
    "antecedents": "Produkty bazowe",
    "consequents": "Produkty rekomendowane",
    "antecedent support": "Popularność produktów bazowych",
    "consequent support": "Popularność produktów rekomendowanych",
    "support": "Wsparcie reguły",
    "confidence": "Pewność reguły",
    "lift": "Wzrost sprzedaży",
    "leverage": "Wkład reguły w sprzedaż",
    "conviction": "Siła zależności",
    "zhangs_metric": "Waga reguły"
}


def rename_and_scale_columns(rules):
    rules = rules.rename(columns=COLUMN_MAPPING)
    # Skalowanie wybranych kolumn do procentów
    percentage_columns = [
        "Popularność produktów bazowych",
        "Popularność produktów rekomendowanych",
        "Wsparcie reguły",
        "Pewność reguły"
    ]
    rules[percentage_columns] = rules[percentage_columns] * 100
    return rules


# Funkcja do formatowania kolumn procentowych
def format_percent(df, columns):
    df_formatted = df.copy()
    for col in columns:
        df_formatted[col] = df_formatted[col].map(lambda x: f"{x:.2f}%")
    return df_formatted


# Sekcja wyboru analizy
analysis_type = st.selectbox(
    "🔍 Wybierz rodzaj analizy:",
    ("Produkty", "Marki", "Kategorie")
)

# Przycisk do uruchomienia analizy
if st.button("🔍 Przeprowadź analizę koszykową"):
    # Dopasowanie danych do wyboru użytkownika
    column_mapping_analysis = {
        "Produkty": "product_id",
        "Marki": "brand",
        "Kategorie": "category_id"
    }

    selected_column = column_mapping_analysis.get(analysis_type)

    if selected_column in df_sales.columns:
        analysis_data = df_sales[df_sales['event_type'] == 'purchase'][['user_id', selected_column]].dropna()
        analysis_data[selected_column] = analysis_data[selected_column].astype(str)
        dense_matrix = create_dense_matrix(analysis_data, selected_column)

        # Generowanie reguł asocjacyjnych
        association_rules_result = generate_association_rules(dense_matrix, min_support=0.002, min_confidence=0.01)

        if not association_rules_result.empty:
            # Zmiana nazw kolumn i skalowanie
            association_rules_result = rename_and_scale_columns(association_rules_result)

            # Przechowanie wyników w session_state
            st.session_state['association_rules_result'] = association_rules_result
            st.session_state['analysis_done_koszykowa'] = True

            st.success("✅ Analiza koszykowa została przeprowadzona pomyślnie!")
        else:
            st.warning(f"⚠️ Brak reguł asocjacyjnych dla {analysis_type.lower()} przy podanych parametrach.")
            st.session_state['association_rules_result'] = None
            st.session_state['analysis_done_koszykowa'] = False
    else:
        st.error(f"❌ Plik nie zawiera wymaganej kolumny: '{selected_column}'.")
        st.session_state['association_rules_result'] = None
        st.session_state['analysis_done_koszykowa'] = False

# Wyświetlanie wyników analizy koszykowej
if 'analysis_done_koszykowa' in st.session_state and st.session_state['analysis_done_koszykowa']:
    association_rules_result = st.session_state['association_rules_result']

    # Sekcja wyboru kolumn
    st.write("### 📋 Wybierz kolumny do wyświetlenia:")
    all_columns = list(COLUMN_MAPPING.values())

    # Inicjalizacja session_state dla wybranych kolumn, jeśli nie istnieje
    if 'selected_columns_koszykowa' not in st.session_state:
        st.session_state['selected_columns_koszykowa'] = all_columns.copy()


    # Funkcja resetująca wybór kolumn
    def reset_columns_koszykowa():
        st.session_state['selected_columns_koszykowa'] = all_columns.copy()


    # Przycisk resetujący wybór kolumn
    st.button("🔄 Przywróć wszystkie kolumny", on_click=reset_columns_koszykowa)

    # Multiselect dla wyboru kolumn, z wartością domyślną z session_state
    selected_columns = st.multiselect(
        "🗂️ Wybierz kolumny:",
        options=all_columns,
        default=st.session_state['selected_columns_koszykowa'],
        key='multiselect_columns_koszykowa'
    )

    # Aktualizacja session_state z wybranymi kolumnami
    if selected_columns:
        st.session_state['selected_columns_koszykowa'] = selected_columns

        # Dodanie sekcji filtrów na głównej stronie
        st.header("🔍 Filtry poszczególnych wartości kolumn")

        # Ustal zakresy dla suwaków na podstawie danych
        min_antecedent_support = float(association_rules_result["Popularność produktów bazowych"].min())
        max_antecedent_support = float(association_rules_result["Popularność produktów bazowych"].max())
        antecedent_support_range = st.slider(
            "Popularność produktów bazowych (%)",
            min_value=0.0,
            max_value=100.0,
            value=(min_antecedent_support, max_antecedent_support),
            step=0.1
        )

        min_consequent_support = float(association_rules_result["Popularność produktów rekomendowanych"].min())
        max_consequent_support = float(association_rules_result["Popularność produktów rekomendowanych"].max())
        consequent_support_range = st.slider(
            "Popularność produktów rekomendowanych (%)",
            min_value=0.0,
            max_value=100.0,
            value=(min_consequent_support, max_consequent_support),
            step=0.1
        )

        min_support_val = float(association_rules_result["Wsparcie reguły"].min())
        max_support_val = float(association_rules_result["Wsparcie reguły"].max())
        support_range = st.slider(
            "Wsparcie reguły (%)",
            min_value=0.0,
            max_value=100.0,
            value=(min_support_val, max_support_val),
            step=0.1
        )

        min_confidence_val = float(association_rules_result["Pewność reguły"].min())
        max_confidence_val = float(association_rules_result["Pewność reguły"].max())
        confidence_range = st.slider(
            "Pewność reguły (%)",
            min_value=0.0,
            max_value=100.0,
            value=(min_confidence_val, max_confidence_val),
            step=0.1
        )

        min_lift = float(association_rules_result["Wzrost sprzedaży"].min())
        max_lift = float(association_rules_result["Wzrost sprzedaży"].max())
        lift_range = st.slider(
            "Wzrost sprzedaży",
            min_value=min_lift,
            max_value=max_lift,
            value=(min_lift, max_lift),
            step=0.1
        )

        # Filtracja danych na podstawie suwaków
        filtered_rules = association_rules_result[
            (association_rules_result["Popularność produktów bazowych"] >= antecedent_support_range[0]) &
            (association_rules_result["Popularność produktów bazowych"] <= antecedent_support_range[1]) &
            (association_rules_result["Popularność produktów rekomendowanych"] >= consequent_support_range[0]) &
            (association_rules_result["Popularność produktów rekomendowanych"] <= consequent_support_range[1]) &
            (association_rules_result["Wsparcie reguły"] >= support_range[0]) &
            (association_rules_result["Wsparcie reguły"] <= support_range[1]) &
            (association_rules_result["Pewność reguły"] >= confidence_range[0]) &
            (association_rules_result["Pewność reguły"] <= confidence_range[1]) &
            (association_rules_result["Wzrost sprzedaży"] >= lift_range[0]) &
            (association_rules_result["Wzrost sprzedaży"] <= lift_range[1])
            ]

        # Opcjonalne formatowanie kolumn procentowych z znakiem %
        filtered_rules_display = format_percent(filtered_rules, [
            "Popularność produktów bazowych",
            "Popularność produktów rekomendowanych",
            "Wsparcie reguły",
            "Pewność reguły"
        ])

        st.write("### 📈 Wyniki analizy koszykowej (po filtracji):")
        st.dataframe(filtered_rules_display[selected_columns])

        # Dodanie przycisku do pobrania filtrowanych danych
        # Pobieramy dane z wybranymi kolumnami
        filtered_selected = filtered_rules[selected_columns]
        csv = filtered_selected.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')  # Dodanie BOM

        st.download_button(
            label="📥 Pobierz dane jako CSV",
            data=csv,
            file_name='filtered_rules.csv',
            mime='text/csv'
        )


    else:
        st.warning("⚠️ Wybierz przynajmniej jedną kolumnę do wyświetlenia.")

    # Dodanie Dokumentacji Kolumn
    with st.expander("📄 Dokumentacja Kolumn"):
        st.markdown("""
        ### Produkty bazowe (antecedents)
        Produkty, które klienci kupują w pierwszej kolejności.

        ### Produkty rekomendowane (consequents)
        Produkty, które najczęściej są kupowane razem z produktami bazowymi.

        ### Popularność produktów bazowych (antecedent support)
        Częstość występowania produktów bazowych w transakcjach.

        ### Popularność produktów rekomendowanych (consequent support)
        Częstość występowania produktów rekomendowanych w transakcjach.

        ### Wsparcie reguły (support)
        Odsetek transakcji zawierających zarówno produkty bazowe, jak i rekomendowane.

        ### Pewność reguły (confidence)
        Prawdopodobieństwo, że klient kupi produkt rekomendowany, jeśli kupił produkt bazowy.

        ### Wzrost sprzedaży (lift)
        Ile razy większe jest prawdopodobieństwo zakupu produktu rekomendowanego w porównaniu do przypadku losowego.

        ### Wkład reguły w sprzedaż (leverage)
        Miara zwiększenia sprzedaży dzięki tej regule w porównaniu do przypadkowego współwystępowania.

        ### Siła zależności (conviction)
        Jak bardzo zakup produktu rekomendowanego zależy od zakupu produktu bazowego.

        ### Waga reguły (zhangs_metric)
        Miara równowagi między wsparciem a pewnością reguły, pomagająca wybrać najbardziej istotne reguły.
        """)


