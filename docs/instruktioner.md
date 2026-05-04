# Instruktioner

JPU-8 har två olika instruktionsklasser.
Varje instruktion är 8 bitar lång, ibland med en 8-bitars intermediate. Därmed tar varje instruktion upp 16 bitar minne i ROM:en.
För att hantera branching lagrar instruktionsminnet två kopior av varje instruktion: en om flaggan är satt, och en om den inte är det. Så varje instruktionspar tar upp 32 bitar.

De två instruktionsklasserna är
 - `MV` (flytta/kopiera)
 - `ALU` (använd aritmetik och logikenheten)

Den första biten i en instruktion representerar vilken instruktionsklass den tillhör.


## MV

MV (förkortning för `move`) kopierar datan från ett register eller pseudo-register till ett annat.
Alla register och psudeo-register kan användas. 

Instruktionslayout:

`0 a a a b b b b`

- `0`: Konstant, representerar `MV`
- `a a a`: 3 bitar som representerar registret som datan ska kopieras ifrån
- `b b b b`: 4 bitar som representerar registret som datan ska kopieras till


## ALU

ALU (förkortning för arithmetic and logic unit, dvs aritmetik och logikenhet) använder JPU-8:ans aritmetik och logikenhet.
Den kan genomföra aritmetikoperationer (t.ex. `ADD`) och logikoperationer (t.ex. `XOR`).
Operationerna genomförs mellan register `XI` och `YI`. Resultatet hamnar i `ZO`.
ALU:n sätter även flaggan som används för branching.

Instruktionslayout:

`1 X! YMUX Y! OP CRY Z! FLG_MODE`

- `1`: Konstant, representerar `ALU`
- `X!`: Huruvida input `XI` ska inverteras. Internt en massa XOR-gates
- `YMYX`: Hurvida `YI` eller `IM` ska användas som y-input
- `Y!`: Samma som `X!`, fast för `YI`
- `OP`: Operationen. `0` representerar aritmetik, `1` representerar logik
- `CRY`: Bestämmer carry-in signalen på adderaren. `1` representerar carry in, dvs +1 på resultatet. Används bara vid aritmetikoperationer.
- `Z!`: Hurvida outputen `ZO` ska inverteras, liknande `X!` och `Y!`
- `FLG_MODE`: Vad flaggan ska sättas till. 0 -> `ZO == 0`, 1 -> `Carry out`.



## Expansionsports-enheter
| Mnemonic           | DEV-id | Beskrivning           |
|--------------------|---------|----------------------|
| DEVICE_NUM_DECIMAL | 0       | Vanliga (bas 10) tal |
| DEVICE_NUM_BIN     | 1       | Binära tal           |
| DEVICE_NUM_HEX     | 2       | Hexadecimala tal     |
| DEVICE_TEXT_ASCII  | 8       | ASCII-text           |