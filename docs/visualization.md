# Wizualizacja wyników

## Cel

Wizualizacje są kluczowym elementem analizy, umożliwiającym przedstawienie wyników w sposób zrozumiały dla użytkowników biznesowych.

## Kroki

1. **Wizualizacja rozkładów**:
   - Histogramy dla cech RFM.

2. **Wizualizacja klastrów**:
   - Wykresy 2D i 3D przedstawiające podział klientów na grupy.

3. **Grafy reguł asocjacyjnych**:
   - Przedstawienie top 10 reguł w formie sieci grafowej.

## Przykład kodu

```python
def draw_graph(rules, top_n=10):
    import networkx as nx
    G = nx.DiGraph()
    for i in range(top_n):
        for antecedent in rules.iloc[i]['antecedents']:
            G.add_edge(antecedent, f"Rule {i}")
        for consequent in rules.iloc[i]['consequents']:
            G.add_edge(f"Rule {i}", consequent)
    nx.draw(G, with_labels=True, node_size=700, font_size=10)
    plt.show()
```

## Kod

Znajduje się w: `notebooks/visualization/`.

## Wyniki
- Histogramy, wykresy słupkowe, oraz sieci grafowe dla reguł asocjacyjnych.