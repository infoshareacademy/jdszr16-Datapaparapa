## Wersja 3: Analiza K-means (Trzecia wersja)
(kmeans_cosmetic_05.ipynb)
### Dane wejściowe

1. Dane wejściowe: Znormalizowane wartości RFM po usunięciu outlierów.
2. Liczba klientów: 108,320  klientów po analizie RFM.

#### Szczegóły danych przed i po analizie RFM:
- rozmiar danych przed analizą: 20,692,709, 13
- rozmiar danych po analizie: 108,320, 3

### Klasteryzacja

#### Parametry modelu:

- Liczba klastrów: 4 (wybór na podstawie metody łokcia).
- Algorytm: KMeans z `random_state=1`.

#### Kod:

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=4, random_state=1)
kmeans.fit(standardized_data)
labels = kmeans.labels_
```

#### Etykiety klastrów:

- Cluster 0: Loyal Customers
- Cluster 1: New Customers
- Cluster 2: At-Risk
- Cluster 3: VIP Customers

### Wyniki

| Segment         | Median Recency | Median Frequency | Median Monetary | Liczba klientów |
| --------------- | -------------- | ---------------- | --------------- | --------------- |
| Loyal Customers | 20             | 15               | 200             | 42,500          |
| New Customers   | 50             | 3                | 30              | 12,000          |
| At-Risk         | 90             | 5                | 50              | 40,000          |
| VIP Customers   | 5              | 50               | 500             | 13,820          |

---

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

### Profil segmentów

- **New Customers**: Klienci, którzy dokonali niedawno pojedynczego zakupu, ale nie są jeszcze lojalni. Warto zwiększyć ich zaangażowanie poprzez specjalne oferty.
- **Loyal Customers**: Najbardziej wartościowi klienci z wysoką częstotliwością zakupów i znaczącymi wydatkami.
- **At-Risk**: Klienci, którzy wykazują spadek aktywności zakupowej. Wymagają działań re-aktywacyjnych.
- **VIP Customers**: Klienci premium o najwyższej wartości zakupowej i częstotliwości.
- **Dormant Customers**: Klienci, którzy przestali kupować i są bliscy całkowitej utraty.