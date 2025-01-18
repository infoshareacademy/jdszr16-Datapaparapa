## Wersja 2: Analiza K-means (Druga Iteracja)
(kmeans_cosmetic_03.ipynb)
### Dane wejściowe

1. Dane wejściowe: Znormalizowane wartości RFM przy użyciu `MinMaxScaler`.
2. Liczba klientów: Spadła z 110,518 do 107,507 z powodu usunięcia outlierów.

### Przekształcenia danych

#### Kod:

```python
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
normalized_data = scaler.fit_transform(data[["recency", "frequency", "monetary"]])
```

### Klasteryzacja

#### Parametry modelu:

- Liczba klastrów: 3
- Algorytm: KMeans z `random_state=0`.

#### Kod:

```python
kmeans = KMeans(n_clusters=3, random_state=0)
kmeans.fit(normalized_data)
labels = kmeans.labels_
```

#### Etykiety klastrów:

- Cluster 0: New Customers
- Cluster 1: At-Risk
- Cluster 2: Loyal Customers

#### Dodanie segmentów:

```python
segments = {0: "New Customers", 1: "At-Risk", 2: "Loyal Customers"}
data["segments"] = data["clusters"].map(segments)
```

### Wyniki

| Segment         | Median Recency | Median Frequency | Median Monetary | Liczba klientów |
| --------------- | -------------- | ---------------- | --------------- | --------------- |
| New Customers   | 30             | 4                | 29              | 11,222          |
| At-Risk         | 115            | 5                | 30              | 50,987          |
| Loyal Customers | 28             | 21               | 117             | 45,298          |

---

## Tabela Porównawcza Wersji Klasteryzacji

| **Etap**                | **Pierwsza wersja**       | **Druga wersja**         | **Trzecia wersja**          |
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