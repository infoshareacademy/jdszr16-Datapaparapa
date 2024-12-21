# Klasteryzacja K-Means

## Cel
Algorytm K-Means umożliwia podział klientów na grupy na podstawie ich cech RFM.

## Parametry wejściowe

- Zestandaryzowane dane z analizy RFM.


## Kroki

1. **Normalizacja danych**:
   - Przekształcenie danych do skali jednorodnej.
   
2. **Wyznaczanie optymalnej liczby klastrów**:
   - Zastosowanie metody "łokcia".

3. **Przeprowadzenie klasteryzacji**:
   - Grupowanie klientów na podstawie podobieństwa ich cech.

4. **Analiza klastrów**:
   - Określenie charakterystyki każdej grupy klientów.


### Przykład kodu

```python
# Standaryzacja danych
scaler = StandardScaler()
rfm_normalized = scaler.fit_transform(rfm_df[['Recency', 'Frequency', 'Monetary']])

def find_Optimal_n_clusters(data, max_clusters=10):
    inertias = []
    for k in range(1, max_clusters + 1):
        kmeans = KMeans(n_clusters=k, n_init='auto', random_state=1).fit(data)
        inertias.append(kmeans.inertia_)
    plt.plot(range(1, max_clusters + 1), inertias, 'bx-')
    plt.title('Metoda łokcia')
    plt.show()
```

## Wersje

1. **Wersja 1**: 5 klastrów na podstawie podstawowych cech RFM (standaryzacja i logarytmowanie). [Szczegóły](kmeans_cosmetic_02.md)
2. **Wersja 2**: 3 klastry po normalizacji danych i usunięciu outlierów. [Szczegóły](kmeans_cosmetic_03.md)
3. **Wersja 3**: 4 klastry z użyciem dodatkowych cech takich jak czas zdarzeń w układzie biegunowym. [Szczegóły](kmeans_cosmetic_05_org.md)

## Tabela wyników

| Iteracja               | Dane wejściowe               | Liczba klastrów | Silhouette Score | Główne wnioski                 |
|------------------------|-----------------------------|----------------|------------------|---------------------------------|
| Wersja 1 (kmeans_cosmetic_02.md) | Dane kosmetyków (standaryzacja) | 5              | 0.4447           | Segmentacja z podstawowymi cechami RFM. |
| Wersja 2 (kmeans_cosmetic_03.md) | Dane kosmetyków (filtrowane)     | 3              | 0.46             | Zmniejszenie liczby klastrów dla prostoty interpretacji. |
| Wersja 3 (kmeans_cosmetic_05_org.md) | Dane kosmetyków (dodatkowe cechy) | 4              | 0.4237           | Identyfikacja bardziej zaawansowanych klastrów. |


Porównanie trzech metod klastrowania użytkowników sklepu internetowego:

### 1. **Pierwsza metoda: Klasteryzacja na podstawie RFM + KMeans**
#### Opis:
W tej metodzie wykorzystano klasyczny model RFM (Recency, Frequency, Monetary) do segmentacji klientów. Klastrowanie przeprowadzono za pomocą algorytmu KMeans, który grupuje użytkowników na podstawie trzech wskaźników:
- **Recency (R)**: Liczba dni od ostatniej transakcji.
- **Frequency (F)**: Liczba dokonanych transakcji.
- **Monetary (M)**: Suma wydanych środków.

Po obliczeniu tych trzech wskaźników, dane zostały przeskalowane (standardyzowane), a następnie poddane klastrowaniu. W końcowej analizie wykorzystywano głównie histograms i scatter plots do wizualizacji wyników. Wykorzystano również metodę „łokcia” do ustalenia optymalnej liczby klastrów.

#### Plusy:
- Prosta i łatwa do zrozumienia metoda.
- Użycie wskaźników RFM pozwala na bardzo praktyczną segmentację klientów z uwagi na ich zachowanie zakupowe.
- Łatwa interpretacja wyników dzięki prostym wskaźnikom.

#### Minusy:
- Zależność od wskaźników RFM, które mogą nie uwzględniać innych zmiennych wpływających na zachowanie klientów.
- Ograniczenie do trzech wymiarów (Recency, Frequency, Monetary).
- KMeans nie radzi sobie dobrze z nieliniowymi relacjami między danymi.

---

### 2. **Druga metoda: Klastrowanie przy użyciu RFM oraz dodatkowych cech (np. Polar Coordinates, Average Actions per Session)**
#### Opis:
Ta metoda rozszerza pierwszą metodę, dodając dodatkowe cechy, takie jak:
- **`event_time_polar`**: Czas wydarzenia (godzina) przekształcony na współrzędne biegunowe, co umożliwia uwzględnienie zmienności zachowań użytkowników w zależności od pory dnia.
- **`actions_per_session`**: Liczba działań wykonanych przez użytkownika w jednej sesji.
- **`user_avg_actions_per_session`**: Średnia liczba działań na sesję dla każdego użytkownika.

Po dodaniu tych cech, użytkownicy zostali klastrowani przy użyciu algorytmu KMeans. Metoda ta wykorzystuje bardziej złożone cechy do lepszego zrozumienia zachowań użytkowników.

#### Plusy:
- Bardziej złożona analiza, uwzględniająca dodatkowe cechy (np. czasowe zachowania użytkowników).
- Lepsze uchwycenie niuansów w zachowaniach użytkowników.
- Możliwość dalszego rozszerzania cech (np. kategorie produktów, czas na stronie).

#### Minusy:
- Zwiększona złożoność procesu przygotowania danych.
- Możliwość nadmiernego skomplikowania modelu, co prowadzi do trudniejszej interpretacji.
- Potrzebna jest większa moc obliczeniowa ze względu na dodatkowe obliczenia.

---

### 3. **Trzecia metoda: Klastrowanie na podstawie zdarzeń użytkowników (Event Log) i cech zebranych z tych zdarzeń**
#### Opis:
W tej metodzie celem było klastrowanie użytkowników na podstawie ich zdarzeń (np. zakupy, dodanie do koszyka, oglądanie produktów) oraz różnych cech opisujących te zdarzenia (np. liczba działań w sesji). W tej metodzie szczególną uwagę poświęcono różnym typom zdarzeń, co pozwoliło na segmentację użytkowników na podstawie ich interakcji z platformą. Zastosowano również procesy takie jak analiza konwersji między różnymi rodzajami zdarzeń (np. od dodania do koszyka do zakupu) i tworzenie cech na podstawie tych danych.

#### Plusy:
- Bardzo szczegółowa analiza zachowań użytkowników.
- Możliwość uwzględnienia szerokiego zakresu działań użytkowników na platformie.
- Dokładniejsze wykrywanie segmentów użytkowników o bardziej specyficznych wzorcach zachowań.

#### Minusy:
- Bardzo złożony proces wstępnej obróbki danych i stworzenia cech.
- Potrzebna jest znaczna moc obliczeniowa przy analizie dużych zbiorów danych.
- Potrzebna jest dogłębna znajomość interakcji użytkowników z platformą, by odpowiednio zaprojektować cechy.

---

### **Porównanie metod:**

| **Aspekt**                       | **Pierwsza metoda (RFM + KMeans)**            | **Druga metoda (RFM + KMeans + Dodatkowe cechy)**           | **Trzecia metoda (Event Log + KMeans)**               |
|-----------------------------------|----------------------------------------------|-----------------------------------------------------------|-------------------------------------------------------|
| **Złożoność modelu**              | Niska, opiera się na trzech prostych wskaźnikach | Średnia, uwzględnia dodatkowe cechy czasowe i sesyjne      | Wysoka, uwzględnia różne zdarzenia użytkowników i ich interakcje |
| **Rodzaj danych**                 | Dane o transakcjach (RFM)                    | Dane o transakcjach + dodatkowe cechy sesji i czasowe      | Dane o różnych typach zdarzeń (koszyk, zakup, itp.)   |
| **Łatwość interpretacji**         | Wysoka, prosty model RFM                     | Średnia, bardziej złożony model                           | Niska, wymaga zaawansowanej analizy interakcji użytkowników |
| **Precyzja segmentacji**          | Ograniczona przez prostotę RFM               | Bardziej precyzyjna dzięki dodatkowym cechom               | Najwyższa, ponieważ opiera się na szczegółowych interakcjach |
| **Moc obliczeniowa**              | Niska                                        | Średnia, zależna od liczby cech                            | Wysoka, wymaga obróbki dużych zbiorów danych          |
| **Wykorzystanie danych**          | Wykorzystuje tylko dane o zakupach           | Wykorzystuje dane o zakupach + dodatkowe informacje        | Wykorzystuje pełen zestaw danych o zachowaniach użytkowników |

### **Podsumowanie:**
- **Pierwsza metoda** jest prostsza i szybka w implementacji, ale ma swoje ograniczenia w kontekście dokładności segmentacji, ponieważ bazuje tylko na podstawowych wskaźnikach RFM.
- **Druga metoda** wprowadza więcej cech, co pozwala na dokładniejszą segmentację, ale wymaga większej liczby zasobów obliczeniowych i może stać się trudniejsza w interpretacji.
- **Trzecia metoda** jest najbardziej zaawansowana, uwzględniając wszystkie rodzaje interakcji użytkownika z platformą, ale wiąże się z dużą złożonością przetwarzania danych i koniecznością zaawansowanej analizy.

Wybór metody zależy od dostępnych zasobów obliczeniowych, celów analizy oraz tego, jak szczegółowo chcemy segmentować użytkowników.

## Tabela Porównawcza Wersji  Klasteryzacji

| **Etap**                | **Pierwsza Wersja**       | **Druga Wersja**         | **Trzecia Wersja**          |
| ----------------------- | --------------------------- | -------------------------- | ----------------------------- |
| **Rozmiar przed RFM**   | 1,286,880 wierszy, 9 kolumn | 908,656 wierszy, 5 kolumn  | 20,692,709 wierszy, 13 kolumn |
| **Liczba klientów**     | 110,500 klientów            | 107,507 klientów           | 108,320 klientów              |
| **Liczba klastrów (K)** | 5                           | 3                          | 4                             |
| **SSE**                 | 3,500                       | 3,200                      | 2,700                         |
| **Silhouette Score**    | 0.4447                      | 0.46                       | 0.4237                        |
| **Największy segment**  | Loyal Customers (41%)       | At-Risk (47%)              | Loyal Customers (40%)         |
| **Liczebność segmentów**| - Loyal: 45,000             | - Loyal: 45,298            | - Loyal: 42,500               |
|                        | - New: 15,000              | - New: 11,222             | - New: 12,000                |
|                        | - At-Risk: 50,500          | - At-Risk: 50,987         | - At-Risk: 40,000            |
|                        | - VIP: 10,000              | - VIP: N/A                | - VIP: 13,820                |
|                        | - Dormant: 30,000          | - Dormant: N/A            | - Dormant: N/A               |


## Wynik
- Podział klientów na 3-5 grup
- **New Customers**: Klienci, którzy dokonali niedawno pojedynczego zakupu, ale nie są jeszcze lojalni.
- **Loyal Customers**: Najbardziej wartościowi klienci z wysoką częstotliwością zakupów i znaczącymi wydatkami.
- **At-Risk**: Klienci, którzy wykazują spadek aktywności zakupowej. Wymagają działań re-aktywacyjnych.
- **VIP Customers**: Klienci premium o najwyższej wartości zakupowej i częstotliwości.
- **Dormant Customers**: Klienci, którzy przestali kupować i są bliscy całkowitej utraty.
