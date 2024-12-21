# Inżynieria cech

## Cel

Tworzenie nowych cech w celu poprawy wyników analizy danych.

## Parametry wejściowe

- Dane wyjściowe z etapu EDA.

## Kroki

1. **Czas zdarzeń w układzie biegunowym**: Konwersja czasu zdarzeń na współrzędne biegunowe.
2. **Akcje na sesję**: Obliczenie liczby akcji w jednej sesji.
3. **Średnia liczba akcji na użytkownika**: Grupowanie danych i obliczanie statystyk.

## Iteracje

- Wypróbowano różne metryki sesji (np. liczba zdarzeń, czas trwania sesji).
- Przekształcenia czasu zdarzeń testowano również w kontekście miesięcy i dni tygodnia.


## Nowe cechy

- Liczba akcji na sesję (`actions_per_session`).
- Czas zdarzenia w układzie biegunowym (`event_time_polar`).

## Kod

Znajduje się w: `notebooks/pre-dendogram.ipynb`.

## Wynik

- Dane wzbogacone o 4 nowe cechy.
