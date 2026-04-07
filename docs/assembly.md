# Assembly

JPU-8 programmeras i JPU-8-assembly, som har tillägget `<namn>.jsm`, eller `<namn>.jlib` för bibliotek. 
På varje rad finns det maximalt en instruktion. Instruktionerna kan läsas mer om i `instruktioner.md`.
Rader kan även ha kommentarer, som indikeras med `;`.
```
; Detta är en kommentar
MV A B ; Detta är också en kommentar
```
För "if-satser", dvs branching, används `|`. Om flaggan är satt kommer det efter `|`-tecknet köras.
Om flaggan inte är satt kommer det före `|` att köras. Om det är tomt på en sida tolkas det som en `NOP`.
Exempel: `| MV A B` kommer kopiera `A` in i `B` om och endast om flaggan är satt, och det är samma sak som att skriva: 
`NOP | MV A B`. 
Om det inte finns ett `|`-tecken kommer det tolkas som att koden står både före och efter `|`-tecknet.
Exempel: `ADD SET_FLG` kommer att alltid att addera och sätta flaggan till hurvida det blev en overflow eller inte.
Det är samma sak som `ADD SET_FLG | ADD SET_FLG`. För ett praktiskt exempel, se `examples/branching.md`
