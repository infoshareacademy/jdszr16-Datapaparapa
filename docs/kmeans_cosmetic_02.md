## Iteracja 1: Analiza K-means (Pierwsza Iteracja)
(kmeans_cosmetic_02.ipynb)
### Dane wejściowe

1. Dane wejściowe: Standaryzowane cechy RFM (Recency, Frequency, Monetary).
2. Proces logarytmowania:
   - Wartości **Frequency** i **Monetary** zostały poddane transformacji logarytmicznej w celu redukcji wpływu wartości odstających.

### Przekształcenia danych

#### Kod:

```python
from sklearn.preprocessing import StandardScaler
import numpy as np

# Logarytmowanie
data["log_monetary"] = np.log1p(data["monetary"])

# Standaryzacja
scaler = StandardScaler()
standardized_data = scaler.fit_transform(data[["recency", "frequency", "log_monetary"]])
```

### Klasteryzacja

#### Parametry modelu:

- Liczba klastrów: 5
- Algorytm: KMeans z `random_state=42`.

#### Kod:

```python
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=5, random_state=42)
kmeans.fit(standardized_data)
labels = kmeans.labels_
```

#### Etykiety klastrów:

- Cluster 0: New Customers
- Cluster 1: Loyal Customers
- Cluster 2: At-Risk
- Cluster 3: VIP Customers
- Cluster 4: Dormant Customers

### Wyniki

| Cluster | Segment Name       | User ID Range | Median Recency | Median Frequency | Median Monetary | Monetary Log |
| ------- | ------------------ | ------------- | -------------- | ---------------- | --------------- | ------------ |
| 0       | New Customers      | 5.31e+08      | 2.06           | 8.12             | 45.44           | 3.77         |
| 1       | Loyal Customers    | 4.78e+08      | 86.91          | 24.08            | 117.98          | 4.56         |
| 2       | At-Risk            | 5.26e+08      | 11.03          | 26.29            | 133.73          | 4.78         |
| 3       | VIP Customers      | 4.79e+08      | 89.22          | 101.08           | 440.62          | 5.95         |
| 4       | Dormant Customers  | 5.40e+08      | 0.34           | 3.57             | 14.03           | 2.63         |

#### Silhouette Score: 0.4447257366937


## Tabela Porównawcza Wersji Klasteryzacji

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