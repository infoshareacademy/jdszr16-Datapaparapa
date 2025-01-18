# Analiza koszykowa

## Cel

Identyfikacja reguł asocjacyjnych między produktami na podstawie zakupów klientów.

## Parametry wejściowe

- Dane zakupów, przekształcone w macierz rzadką.

## Kroki

1. **Tworzenie macierzy rzadkiej**:
   - Grupowanie danych na podstawie użytkowników i ich zakupów.

2. **Generowanie reguł asocjacyjnych**:
   - Wykorzystanie algorytmu Apriori do znalezienia wzorców.

3. **Wizualizacja reguł**:
   - Tworzenie grafów dla najważniejszych reguł.
s
## Iteracje

- Analizowano zarówno marki, jak i kategorie produktów.
- Testowano różne minimalne wsparcia (`support`) i ufności (`confidence`).


### Przykład kodu

```python
from mlxtend.frequent_patterns import apriori, association_rules

sparse_matrix = create_sparse_matrix(data, 'brand')
frequent_itemsets = apriori(sparse_matrix, min_support=0.01, use_colnames=True)
rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.5)
```

## Wynik
- Reguły asocjacyjne, takie jak: „Jeśli klient kupił A, to z pewnym prawdopodobieństwem kupi B”.