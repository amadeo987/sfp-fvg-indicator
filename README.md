# SK SFP + FVG / IFVG

Publiczny wskaźnik TradingView napisany w Pine Script v6. Łączy radar aktualnych poziomów SFP, najbliższe strefy FVG/IFVG z interwału 1H oraz oznaczenia dni tygodnia.

## Funkcje

- dwa najbliższe poziomy `SFP WATCH` nad i pod ceną,
- zachowanie wykorzystanych poziomów jako `WATCH — DOTKNIĘTY`,
- cienki, opcjonalny `SFP RAW` po prawidłowym sweepie i powrocie korpusu,
- mocny `SFP CONF` dopiero po późniejszym wybiciu struktury,
- do trzech najbliższych aktywnych FVG/IFVG nad ceną i do trzech pod ceną,
- klasyczne, trzyświecowe FVG wyliczane wyłącznie z zamkniętych świec 1H,
- dokładne granice stref według knotów pierwszej i trzeciej świecy,
- krótkie separatory i nazwy dni tygodnia,
- alerty dotknięcia i potwierdzenia SFP oraz zmian FVG/IFVG.

## Instalacja

1. Otwórz wykres w TradingView i przejdź do **Pine Editor**.
2. Skopiuj całą zawartość pliku [`SK_SFP_Najblizsze_Poziomy.pine`](./SK_SFP_Najblizsze_Poziomy.pine).
3. Wklej kod do nowego skryptu Pine.
4. Zapisz skrypt i wybierz **Add to chart / Dodaj do wykresu**.

Pełny opis poziomów, ustawień i alertów znajduje się w [`SFP_WSKAZNIK_INSTRUKCJA.md`](./SFP_WSKAZNIK_INSTRUKCJA.md).

## Stan projektu

Aktualna wersja: **5.4**. Kod kompiluje się w Pine Script v6 bez błędów i ostrzeżeń.

W wersji 5.4 warstwa SFP ma jednoznaczną hierarchię `WATCH → RAW → CONF`. WATCH nie udaje gotowego SFP, RAW pokazuje zamknięty setup po sweepie, a CONF wymaga późniejszego wybicia struktury. RAW ma osobny przełącznik i nie zmienia istniejącej logiki alertów potwierdzenia.

## Ważne

To narzędzie analityczne, nie rekomendacja inwestycyjna ani gotowa strategia. Linie SFP wskazują obszary płynności warte obserwacji; nie gwarantują reakcji ceny. Wskaźnik nie składa zleceń.

## Licencja

Projekt jest udostępniony na licencji MIT.
