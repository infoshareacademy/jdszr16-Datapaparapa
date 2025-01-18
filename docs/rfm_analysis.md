# Analiza RFM

## Cel

Analiza RFM (Recency, Frequency, Monetary) umożliwia kategoryzację klientów na podstawie ich ostatniej aktywności, częstotliwości zakupów oraz wydatków.

1. Recency: Czas od ostatniego zakupu.
2. Frequency: Liczba zakupów.
3. Monetary: Suma wydatków.

## Parametry wejściowe

- Dane z tabeli zakupów po inżynierii cech.

### Kroki

1. **Obliczenie metryk RFM**:
   - Recency: czas od ostatniego zakupu.
   - Frequency: liczba zakupów.
   - Monetary: całkowita wartość zakupów.

2. **Logarytmiczne skalowanie**: Zastosowanie logarytmu w celu normalizacji danych.

3. **Standaryzacja danych**: Przekształcenie cech do jednorodnej skali przy użyciu `StandardScaler`.

## Iteracje

- Testowano różne zakresy czasowe dla obliczeń (np. ostatnie 3, 6, 12 miesięcy).
- Skalowano dane zarówno logarytmicznie, jak i przy użyciu standaryzacji.


### Przykład kodu

```python
latest_date = data['event_time'].max()
rfm_df = data[data['event_type'] == 'purchase'].groupby('user_id').agg({
    'event_time': lambda date: (latest_date - date.max()).seconds,
    'product_id': 'count',
    'price': 'sum'
}).reset_index()

rfm_df.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']
rfm_df[['Frequency', 'Monetary']] = np.log1p(rfm_df[['Frequency', 'Monetary']])
```

## Wynik
- Klasyfikacja klientów na 5 grup, np. „VIP”, „Nowy potencjalny klient”, „Stracony klient”.
- Dane gotowe do klasteryzacji klientów.