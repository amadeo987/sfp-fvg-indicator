# [SK] SFP + FVG / IFVG + RSI v5.2

Ta wersja łączy bieżący radar SFP, najbliższe strefy FVG/IFVG z 1H, opisy dni tygodnia i klasyczne RSI 14 w jednym wskaźniku. Panel Inputs ma wyłącznie cztery przełączniki: `SFP`, `FVG / IFVG 1H`, `Dni tygodnia` i `Alerty`. RSI działa stale z klasycznymi parametrami, a ustawienia zaawansowane nie zaśmiecają panelu.

## Co oznacza linia, a co sygnał

- `SFP HIGH 1/2` (niebieski): potwierdzony swing high i aktualny poziom płynności, na którym **może** powstać bearish SFP.
- `SFP LOW 1/2` (turkusowy): potwierdzony swing low i aktualny poziom płynności, na którym **może** powstać bullish SFP.
- `DOTKNIĘTY HIGH/LOW` (przygaszony, przerywany): poziom został już wykorzystany i nie generuje kolejnego setupu, ale pozostaje chwilowo widoczny jako kontekst reakcji.
- Sweep knotem i zamknięcie z powrotem tworzą setup SFP.
- Potwierdzenie `SFP CONF SHORT/LONG` powstaje dopiero wtedy, gdy w ciągu 3 następnych świec close wybije przeciwne ekstremum świecy setupu. Wskaźnik zachowuje kolorową linię ostatniego potwierdzonego poziomu i alert, ale nie rysuje dużej etykiety zasłaniającej świece.

Na otwartej świecy dotknięty poziom nie znika: od razu zmienia się w przerywany `DOTKNIĘTY`, a po zamknięciu świecy trafia do pamięci dotkniętych poziomów. Linia nie przewiduje pewnej reakcji. Pokazuje miejsce warte obserwacji; etykieta potwierdzonego sygnału powstaje dopiero na zamknięciu świecy i nie przemalowuje się intrabar.

## Tryby dokładności

- `Czuły`: lokalne swingi 3/3, reakcja minimum 0,6 ATR; więcej poziomów i szumu.
- `Standard`: swingi 5/5, reakcja minimum 1 ATR; kompromis między liczbą poziomów a szumem.
- `Selektywny`: swingi 10/10, reakcja minimum 1,25 ATR; mniej poziomów i mniej lokalnego szumu. Jest ustawieniem domyślnym po audycie.
- `Własny`: ręcznie ustawiasz siłę swingu, minimalną reakcję oraz łączenie bliskich poziomów.

Jeżeli wykres nadal jest zbyt pełny, ustaw `Poziomy nad ceną` i `Poziomy pod ceną` na `1` albo wybierz `Selektywny`. Jeżeli poziomów jest za mało, wybierz `Czuły` lub zwiększ `Maksymalna odległość od ceny (ATR)`.

## Potwierdzenie

Bearish setup: high wybija aktywny swing high, ale zamknięcie wraca poniżej. Bullish setup: low wybija aktywny swing low, ale zamknięcie wraca powyżej. Domyślnie cały korpus musi zostać po właściwej stronie, sweep ma co najmniej 0,1 ATR i maksymalnie 1 ATR, a świeca ma zakres minimum 1,2 ATR. Po pierwszym dotknięciu pula płynności jest zużyta i nie może generować kolejnych setupów, ale domyślnie jej linia pozostaje widoczna jeszcze przez 12 świec. Znika wcześniej, gdy cena oddali się o ponad 5 ATR. Czas, odległość i liczbę takich linii można zmienić w sekcji `2. SFP — poziomy`.

W trybie `Break struktury` bearish CONF wymaga późniejszego close poniżej low świecy setupu, a bullish CONF close powyżej jej high. Setup wygasa po 3 świecach lub po wybiciu jego ekstremum z buforem 0,1 ATR. `Sam powrót świecy` przywraca luźną definicję v3, ale backtest nie wykazał dla niej samodzielnej przewagi.

Wskaźnik przechowuje najwyżej jeden ostatni potwierdzony sygnał i domyślnie ukrywa go po 72 świecach. Panel stanu jest domyślnie wyłączony.

## FVG i IFVG 1H

- Wszystkie strefy są liczone z zamkniętych świec godzinowych, niezależnie od interwału otwartego wykresu.
- Klasyczne wzrostowe FVG: minimum trzeciej świecy 1H jest powyżej maksimum pierwszej. Spadkowe działa odwrotnie.
- Wskaźnik rysuje najwyżej najbliższą wzrostową i najbliższą spadkową strefę, zamiast wyświetlać całą historię.
- Box jest żółty, bez obramowania, zaczyna się dokładnie na otwarciu świecy tworzącej układ i kończy na prawej krawędzi aktualnej świecy. Z każdą świecą wydłuża się razem z rynkiem, ale nie wystaje w pustą przyszłość.
- W środku boxu widnieje `FVG 1H` albo `IFVG 1H`.
- Pełne wypełnienie knotem usuwa strefę. Zamknięcie godzinowe przez przeciwną krawędź zmienia FVG w IFVG; pełne wypełnienie aktywnego IFVG również je usuwa.

## Dni tygodnia

Przełącznik `Dni tygodnia` dodaje na dole cienkie nazwy wszystkich siedmiu dni, wyśrodkowane pomiędzy dwiema kolejnymi północami, oraz krótkie półprzezroczyste separatory. Strefa `Europe/Warsaw` automatycznie uwzględnia zmianę czasu.

## Klasyczne RSI

RSI jest liczone z ceny zamknięcia i ma stały okres `14`. Fioletowa linia znajduje się w osobnym dolnym panelu, z poziomami `70`, `50` i `30` oraz delikatnie zaznaczonym zakresem 30–70. SFP, FVG/IFVG i dni pozostają na głównym wykresie dzięki `force_overlay`, więc cały pakiet nadal liczy się jako jeden wskaźnik TradingView.

## Alerty i ograniczenia

Jeden przełącznik `Alerty` obsługuje następujące zdarzenia:

- `Dotknięcie SFP HIGH/LOW` — natychmiast przy pierwszym dotknięciu aktywnego poziomu; dynamiczna wiadomość ma format JSON przeznaczony dla webhooka Telegram.
- `Potwierdzony bearish/bullish SFP` — dopiero po zamknięciu świecy zgodnie z wybranym potwierdzeniem.
- `Nowa strefa FVG 1H` — po zamknięciu trzeciej świecy godzinowej tworzącej lukę.
- `Nowa inwersja IFVG 1H` — po godzinowym zamknięciu przez przeciwną krawędź FVG.

Dla dynamicznych wiadomości wybierz w TradingView warunek `Any alert() function call`. Alerty tworzenia stref i potwierdzenia SFP działają po zamknięciu, a alert dotknięcia SFP działa raz na świecę. Po aktualizacji kodu istniejący alert TradingView nadal używa starej kopii skryptu, dlatego trzeba go usunąć i utworzyć ponownie. Alerty tylko informują — nie składają zleceń.

To wskaźnik, nie strategia. Nie składa zleceń i nie zna przyszłości. Backtest 371 820 świec OKX pokazał, że SFP bez dodatkowego kontekstu nie jest samodzielnie rentowną strategią po kosztach. Linie należy traktować jako radar płynności, a CONF jako bardziej rygorystyczne potwierdzenie struktury — nadal wymagające kontekstu HTF, sesji i zarządzania ryzykiem.
