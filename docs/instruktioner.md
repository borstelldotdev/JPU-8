# Instruktioner

JPU-8 har fyra olika instruktionsklasser.
Varje instruktion är 8 bitar lång, ibland med en 8-bitars intermediate. Därmed tar varje instruktion upp 16 bitar minne i ROM:en.
För att hantera branching lagrar instruktionsminnet två kopior av varje instruktion: en om flaggan är satt, och en om den inte är det. Så varje instruktionspar tar upp 32 bitar.

De fyra instruktionsklasserna är
 - `MV` (flytta/kopiera)
 - `ALU` (använd aritmetik och logikenheten)
 - `???` (Oanvänd)
 - `SYS` (System-instruktioner, dvs instruktioner som inte passar in någon annan instruktionsklass)

De första två bitarna i en instruktion representerar vilken instruktionsklass den tillhör.


## MV

MV (förkortning för `move`) kopierar datan från ett register eller pseudo-register till ett annat.
Alla register förutom `PC` kan användas. `PC` togs bort för att kunna representera instruktioner som ett trebitarsvärde.

Instruktionslayout:

`0 0 a a a b b b`

- `0 0`: Konstant, representerar `MV`
- `a a a`: 3 bitar som representerar registret som datan ska kopieras ifrån
- `b b b`: 3 bitar som representerar registret som datan ska kopieras till


## ALU

ALU (förkortning för arithmetic and logic unit, dvs aritmetik och logikenhet) använder JPU-8:ans aritmetik och logikenhet.
Den kan genomföra aritmetikoperationer (t.ex. `ADD`) och logikoperationer (t.ex. `XOR`).
Operationerna genomförs mellan register `XI` och `YI`. Resultatet hamnar i `ZO`.
ALU:n sätter även flaggan som används för branching.

Instruktionslayout:

`0 1 X! Y! OP CRY Z! FLG`

- `0 1`: Konstant, representerar `ALU`
- `X!`: Huruvida input `XI` ska inverteras. Internt en massa XOR-gates
- `Y!`: Samma som `X!`, fast för `YI`
- `OP`: Operationen. `0` representerar aritmetik, `1` representerar logik
- `CRY`: Bestämmer carry-in signalen på adderaren. `1` representerar carry in, dvs +1 på resultatet. Används bara vid aritmetikoperationer.
- `Z!`: Hurvida outputen `ZO` ska inverteras, liknande `X!` och `Y!`
- `FLG`: Om flaggan ska sättas eller inte. `0`: ska inte sättas, `1`: ska sättas. Om `OP=0` sätts flaggan till carry-out. Om `OP=1` blir flaggan hurvida outputen är lika med `0`.


## ???
Oanvänd

Instruktionslayout:

`1 0 ? ? ? ? ? ?`

## SYS

Instruktionslayout:

`1 1 s s s s s s`

- `1 1`: Konstant, representerar `SYS`
- `s s s s s s`: 6 bitar som representerar vilken systeminstruktion som ska användas

| Namn            | Mnemonic | Bitar  | Anteckningar                                       |
|-----------------|----------|--------|----------------------------------------------------|
| Halt            | HLT      | 000000 | Avsluta programmet                                 |
| Pause           | PAUSE    | 000001 | Stäng av den automatiska klockan                   |
| Reset flag      | R_FLG    | 000010 | Sätt flaggan till `0`                              |
| Set flag        | S_FLG    | 000011 | Sätt flaggan till `1`                              |
| Jump A          | JMPA     | 000100 | Sätt `PC` till `A`                                 |
| Jump B          | JMPB     | 001100 | Sätt `PC` till `B`                                 |
| Jump C          | JMPC     | 010100 | Sätt `PC` till `C`                                 |
| Jump D          | JMPD     | 011100 | Sätt `PC` till `D`                                 |
| Jump ZO         | JMPZ     | 100100 | Sätt `PC` till `ZO`                                |
| Jump            | JMP      | 101100 | Sätt `PC` till `IM`                                |
| Jump MEM        | JMPMEM   | 110100 | Sätt `PC` till `MEM[IM]`                           |
| Jump EX         | JMPEX    | 111100 | Sätt `PC` till `EX` **OSÄKERT!!!**                 |
| Read Pointer A  | RPTRA    | 000100 | Sätt `ZO` till `MEM[A]`                            |
| Read Pointer B  | RPTRB    | 001100 | Sätt `ZO` till `MEM[B]`                            |
| Read Pointer C  | RPTRC    | 010100 | Sätt `ZO` till `MEM[C]`                            |
| Read Pointer D  | RPTRD    | 011100 | Sätt `ZO` till `MEM[D]`                            |
| Write Pointer A | WPTRA    | 100100 | Sätt `MEM[A]` till `XI`                            |
| Write Pointer B | WPTRB    | 101100 | Sätt `MEM[A]` till `XI`                            |
| Write Pointer C | WPTRC    | 110100 | Sätt `MEM[A]` till `XI`                            |
| Write Pointer D | WPTRD    | 111100 | Sätt `MEM[A]` till `XI`                            |
| Set device      | SDEV     | 111101 | Välj vilken enhet `IM` som `EX` ska interagera med |
| No Opeartion    | NOP      | 111111 | Gör ingenting                                      |

