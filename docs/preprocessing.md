# Wstępne przetwarzanie danych

## Cel

Etap wstępnego przetwarzania danych obejmuje ładowanie, czyszczenie i przekształcanie surowych danych e-commerce, aby były one gotowe do analizy.

## Parametry wejściowe

- Pliki CSV zawierające dane o zdarzeniach (np. zakupy, przeglądanie produktów) z informacjami takimi jak `event_time`, `price`, `category_id`.


## Kroki

1. **Ładowanie danych**: z katalogu `data/raw/`, wczytanie danych z wielu plików CSV do jednej tabeli.
2. **Transformacja daty**: Konwersja kolumny `event_time` na typ datetime.
3. Usunięcie braków
4. Usunięcie wartości negatywnych (Wartości price mniejsze niż 0 są eliminowane).

## Przykładowy kod

```python
import pandas as pd
from pathlib import Path
# Ładowanie danych
raw_path = Path('data/raw/cosmetics/')
data = pd.concat([pd.read_csv(file) for file in raw_path.glob('*.csv')])

# Konwersja czasowa i usuwanie wartości skrajnych
data['event_time'] = pd.to_datetime(data['event_time'])
data = data[data['price'] >= 0]

# Zapis przetworzonych danych
data.to_parquet('data/processed/processed_data.parquet')
```

## Wynik
- Oczyszczona tabela danych z 20 mln zdarzeń, gotowa do eksploracyjnej analizy.