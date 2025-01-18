## Opis przepływu danych

1. **Etap wstępny**:
    - Dane wejściowe: surowe pliki CSV zawierające zdarzenia.
    - Procesy: Ładowanie danych, usuwanie błędnych rekordów (np. negatywne ceny), konwersja dat.
    - Wynik: Oczyszczony zbiór danych gotowy do analizy.

2. **Eksploracyjna analiza danych (EDA)**:
    - Dane wejściowe: Oczyszczony zbiór danych.
    - Procesy: Analiza brakujących wartości, wizualizacja rozkładów, analiza trendów czasowych.
    - Wynik: Statystyki opisowe, identyfikacja problematycznych danych.

3. **Inżynieria cech**:
    - Dane wejściowe: Dane po EDA.
    - Procesy: Tworzenie nowych cech (np. liczba akcji na sesję, czas zdarzeń w układzie biegunowym).
    - Wynik: Wzbogacony zbiór danych z dodatkowymi cechami.

4. **Analiza RFM**:
    - Dane wejściowe: Dane zakupowe (z nowymi cechami).
    - Procesy: Obliczenie metryk RFM, standaryzacja, podział klientów na segmenty.
    - Wynik: Kategoryzacja klientów w oparciu o metryki RFM.

5. **Klasteryzacja K-Means**:
    - Dane wejściowe: Dane RFM po standaryzacji.
    - Procesy: Grupowanie klientów na podstawie podobieństwa cech.
    - Wynik: Podział klientów na klastery.

6. **Analiza koszykowa**:
    - Dane wejściowe: Dane zakupowe (marki, kategorie).
    - Procesy: Generowanie reguł asocjacyjnych za pomocą algorytmu Apriori.
    - Wynik: Reguły wskazujące zależności między produktami.

7. **Wizualizacja wyników**:
    - Dane wejściowe: Wyniki wszystkich poprzednich etapów.
    - Procesy: Tworzenie wykresów, raportów i grafów.
    - Wynik: Zrozumiałe wizualizacje dla użytkowników biznesowych.

## Struktura folderów
/data/
  /raw/       -> surowe dane
  /processed/ -> dane przetworzone
  /features/  -> dane wzbogacone
  /results/   -> wyniki analizy
  /visualizations/ -> pliki graficzne


## Diagram przepływu danych

Taki diagram można przedstawić za pomocą narzędzi do wizualizacji, takich jak **Mermaid**, **Draw.io**, czy **Diagrams.net**. Oto przykład w formie tekstowej (możesz wkleić go do narzędzi wspierających Mermaid):

```mermaid
flowchart TD
    A[Pliki CSV (surowe dane)] --> B[Wstępne przetwarzanie danych]
    B --> C[Eksploracyjna analiza danych (EDA)]
    C --> D[Inżynieria cech]
    D --> E[Analiza RFM]
    E --> F[Klasteryzacja K-Means]
    D --> G[Analiza koszykowa]
    E --> H[Wizualizacja wyników]
    F --> H
    G --> H
```


## Jak dodać diagram do dokumentacji MkDocs?

1. Zainstaluj wtyczkę **Mermaid** w MkDocs, dodając do pliku `mkdocs.yml`:

```yaml
   markdown_extensions:
     - pymdownx.superfences
```
2. W plikach `.md` użyj składni Mermaid (jak powyżej).


## Alternatywnie: Opis kroków ze związkami

Możesz także dodać tabelę, która pokazuje relacje między etapami:

| Etap                   | Dane wejściowe               | Wynik                |
|------------------------|-----------------------------|----------------------|
| Wstępne przetwarzanie  | Surowe pliki CSV            | Oczyszczony zbiór   |
| EDA                    | Oczyszczony zbiór danych    | Statystyki i rozkłady|
| Inżynieria cech        | Dane po EDA                 | Dane wzbogacone      |
| Analiza RFM            | Dane zakupowe               | Klasyfikacja klientów|
| Klasteryzacja K-Means  | Dane RFM                    | Grupy klientów       |
| Analiza koszykowa      | Dane zakupowe               | Reguły asocjacyjne   |
| Wizualizacja wyników   | Wszystkie wyniki            | Raporty i wykresy    |