# [SK] SFP + FVG / IFVG v5.4

Ta wersja łączy bieżący radar SFP, najbliższe strefy FVG/IFVG z 1H i opisy dni tygodnia w jednym wskaźniku. Panel Inputs ma pięć prostych przełączników: `SFP`, `SFP RAW`, `FVG / IFVG 1H`, `Dni tygodnia` i `Alerty`. Ustawienia zaawansowane są celowo stałe, żeby nie zaśmiecać panelu.

## Co oznacza linia, a co sygnał

- `SFP WATCH HIGH 1/2` (niebieski): potwierdzony swing high i aktualna pula płynności, na której **może** dopiero powstać bearish SFP. To nie jest sygnał.
- `SFP WATCH LOW 1/2` (turkusowy): potwierdzony swing low i aktualna pula płynności, na której **może** dopiero powstać bullish SFP. To nie jest sygnał.
- `WATCH HIGH/LOW — DOTKNIĘTY` (przygaszony, przerywany): poziom został już wykorzystany i nie generuje kolejnego setupu, ale pozostaje chwilowo widoczny jako kontekst reakcji.
- `SFP RAW SHORT/LONG` (cienki, przerywany): knot zamiata WATCH, świeca zamyka się z powrotem za poziomem, a cały korpus pozostaje po właściwej stronie. RAW powstaje wyłącznie na zamkniętej świecy i pozostaje widoczny przez maksymalnie 12 świec. Można go osobno wyłączyć.
- `SFP CONF SHORT/LONG` (gruby, ciągły): w ciągu 3 następnych świec close wybija przeciwne ekstremum świecy RAW. Wskaźnik zachowuje linię ostatniego potwierdzonego poziomu i mały tekst bez dużej chmurki zasłaniającej świece.

Na otwartej świecy dotknięty poziom nie znika: od razu zmienia się w przerywany `WATCH — DOTKNIĘTY`, a po zamknięciu świecy trafia do pamięci dotkniętych poziomów. Linia WATCH nie przewiduje pewnej reakcji. RAW oraz CONF powstają dopiero na zamkniętych świecach i nie przemalowują się intrabar.

## Domyślny filtr jakości

Wersja 5.4 działa stale w trybie selektywnym: swing 10/10, reakcja minimum 1,25 ATR, maksymalnie dwa poziomy WATCH nad ceną i dwa pod ceną. Parametry są celowo ukryte, żeby panel ustawień pozostał prosty i żeby przypadkowa zmiana nie rozluźniła definicji SFP.

## Potwierdzenie

Bearish RAW: high wybija aktywny WATCH high knotem, ale open i close kończą poniżej poziomu. Bullish RAW: low wybija aktywny WATCH low knotem, ale open i close kończą powyżej poziomu. Sweep ma co najmniej 0,1 ATR i maksymalnie 1 ATR, a świeca ma zakres minimum 1,2 ATR. Po pierwszym dotknięciu pula płynności jest zużyta i nie może generować kolejnych setupów, ale jej przygaszona linia pozostaje widoczna jeszcze przez maksymalnie 12 świec lub do oddalenia ceny o ponad 5 ATR.

W trybie `Break struktury` bearish CONF wymaga późniejszego close poniżej low świecy setupu, a bullish CONF close powyżej jej high. Setup wygasa po 3 świecach lub po wybiciu jego ekstremum z buforem 0,1 ATR. `Sam powrót świecy` przywraca luźną definicję v3, ale backtest nie wykazał dla niej samodzielnej przewagi.

Wskaźnik przechowuje najwyżej jeden ostatni potwierdzony sygnał i domyślnie ukrywa go po 72 świecach. Panel stanu jest domyślnie wyłączony.

## FVG i IFVG 1H

- Wszystkie strefy są liczone z zamkniętych świec godzinowych, niezależnie od interwału otwartego wykresu.
- Klasyczne wzrostowe FVG: minimum trzeciej świecy 1H jest powyżej maksimum pierwszej. Spadkowe działa odwrotnie.
- Wskaźnik rysuje do trzech najbliższych aktywnych stref nad ceną i do trzech pod ceną, zamiast wyświetlać całą historię.
- Granice boxu są dokładnie równe knotom pierwszej i trzeciej świecy klasycznego układu. Nie są liczone z korpusów, ATR ani przybliżonych poziomów.
- Box jest żółty, bez obramowania, zaczyna się dokładnie na otwarciu trzeciej świecy tworzącej układ i kończy na prawej krawędzi aktualnej świecy. Z każdą świecą wydłuża się razem z rynkiem, ale nie wystaje w pustą przyszłość.
- W środku boxu widnieje `FVG 1H` albo `IFVG 1H`.
- Pełne wypełnienie knotem usuwa strefę. Zamknięcie godzinowe przez przeciwną krawędź zmienia FVG w IFVG; pełne wypełnienie aktywnego IFVG również je usuwa. Stare IFVG wygasają po 72 godzinach, żeby dawna inwersja nie tworzyła ogromnego, nieaktualnego boxu.

## Dni tygodnia

Przełącznik `Dni tygodnia` dodaje na dole cienkie nazwy wszystkich siedmiu dni, wyśrodkowane pomiędzy dwiema kolejnymi północami, oraz krótkie półprzezroczyste separatory. Strefa `Europe/Warsaw` automatycznie uwzględnia zmianę czasu.

## Alerty i ograniczenia

Jeden przełącznik `Alerty` obsługuje następujące zdarzenia:

- `Dotknięcie SFP HIGH/LOW` — natychmiast przy pierwszym dotknięciu aktywnego poziomu; dynamiczna wiadomość ma format JSON przeznaczony dla webhooka Telegram.
- `Potwierdzony bearish/bullish SFP` — dopiero po zamknięciu świecy zgodnie z wybranym potwierdzeniem.
- `Nowa strefa FVG 1H` — po zamknięciu trzeciej świecy godzinowej tworzącej lukę.
- `Nowa inwersja IFVG 1H` — po godzinowym zamknięciu przez przeciwną krawędź FVG.

Dla dynamicznych wiadomości wybierz w TradingView warunek `Any alert() function call`. Alerty tworzenia stref i potwierdzenia SFP działają po zamknięciu, a alert dotknięcia SFP działa raz na świecę. Po aktualizacji kodu istniejący alert TradingView nadal używa starej kopii skryptu, dlatego trzeba go usunąć i utworzyć ponownie. Alerty tylko informują — nie składają zleceń.

To wskaźnik, nie strategia. Nie składa zleceń i nie zna przyszłości. Backtest 371 820 świec OKX pokazał, że SFP bez dodatkowego kontekstu nie jest samodzielnie rentowną strategią po kosztach. Linie należy traktować jako radar płynności, a CONF jako bardziej rygorystyczne potwierdzenie struktury — nadal wymagające kontekstu HTF, sesji i zarządzania ryzykiem.
