# SK SFP + FVG / IFVG + RSI

Publiczny wskaźnik TradingView napisany w Pine Script v6. Łączy radar aktualnych poziomów SFP, najbliższe strefy FVG/IFVG z interwału 1H, oznaczenia dni tygodnia i klasyczne RSI 14.

## Funkcje

- dwa najbliższe poziomy SFP nad i pod ceną,
- zachowanie wykorzystanych poziomów jako `DOTKNIĘTY HIGH/LOW`,
- potwierdzenia SFP po wybiciu struktury,
- najbliższe FVG i IFVG wyliczane z zamkniętych świec 1H,
- krótkie separatory i nazwy dni tygodnia,
- klasyczne RSI 14 w dolnym panelu,
- alerty dotknięcia i potwierdzenia SFP oraz zmian FVG/IFVG.

## Instalacja

1. Otwórz wykres w TradingView i przejdź do **Pine Editor**.
2. Skopiuj całą zawartość pliku [`SK_SFP_Najblizsze_Poziomy.pine`](./SK_SFP_Najblizsze_Poziomy.pine).
3. Wklej kod do nowego skryptu Pine.
4. Zapisz skrypt i wybierz **Add to chart / Dodaj do wykresu**.

Pełny opis poziomów, ustawień i alertów znajduje się w [`SFP_WSKAZNIK_INSTRUKCJA.md`](./SFP_WSKAZNIK_INSTRUKCJA.md).

## Stan projektu

Aktualna wersja: **5.2**. Kod kompiluje się w Pine Script v6 bez błędów i ostrzeżeń.

Najważniejsza rzecz do dalszego dopracowania to geometria i selekcja stref FVG/IFVG. Obecna implementacja celowo pokazuje tylko najbliższe strefy, ale nie każda strefa pokrywa się idealnie z ręcznym odczytem rynku. Zmiany będziemy rozwijać wersjami i weryfikować na różnych instrumentach oraz interwałach.

## Ważne

To narzędzie analityczne, nie rekomendacja inwestycyjna ani gotowa strategia. Linie SFP wskazują obszary płynności warte obserwacji; nie gwarantują reakcji ceny. Wskaźnik nie składa zleceń.

## Licencja

Projekt jest udostępniony na licencji MIT.
