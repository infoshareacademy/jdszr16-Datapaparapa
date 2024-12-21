# Eksploracyjna analiza danych

## Cel

Analiza EDA pozwala zrozumieć strukturę i rozkład danych, trendów czasowych, zidentyfikować problemy (np. brakujące wartości), oraz zdefiniować potencjalne cechy do dalszej analizy.

## Parametry wejściowe
- Oczyszczona tabela danych po etapie wstępnego przetwarzania.

## Kroki

1. Analiza brakujących wartości.
2. Rozkład cen i liczby/typów zdarzeń.
3. Trendy czasowe (godzinowe, dzienne, tygodniowe).

## Iteracje

- Kilkakrotnie analizowano rozkład cen (np. z uwzględnieniem wartości poniżej pewnych progów, np. 1000 zł).
- Dane godzinowe analizowano z różnymi przedziałami czasowymi (np. godzinami szczytu).


## Przykładowe wizualizacje

- **Histogram rozkładu cen**:
```python
  data['price'].plot(kind='hist', bins=50, title='Rozkład cen')
```
- **Trendy czasowe**:
```python
data['event_time'].dt.hour.value_counts().sort_index().plot(kind='bar', title='Aktywność godzinowa')
```

## Wyniki
- Większość transakcji miała miejsce wieczorem.
- Brakujące wartości w kolumnach brand i category_id.
- Szczegółowe wykresy rozkładów, wskazujące godziny największej aktywności klientów (18:00–22:00) oraz dominujące marki.

