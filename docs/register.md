# Register

JPU-8 har 11 register:

| Namn | Läs | Skriv | ID  | Anteckningar                                                |
|------|-----|-------|-----|-------------------------------------------------------------|
| A    | Y   | Y     | 000 | GP                                                          |
| B    | Y   | Y     | 001 | GP                                                          |
| C    | Y   | Y     | 010 | GP                                                          |
| D    | Y   | Y     | 011 | GP (Används ofta för temporära värden)                      |
| XI   | N   | Y     | 100 | ALU input 1                                                 |
| YI   | N   | Y     | 101 | ALU input 2                                                 |
| ZO   | Y   | N     | 100 | ALU output                                                  |
| IM   | Y   | N     | 101 | Intermediate-värden                                         |
| EX   | Y   | Y     | 110 | Expansions-port                                             |
| MEM  | Y   | Y     | 111 | Minne (XI: address)                                         |
| PC   | N   | Y     | xxx | Programräknare (Ingen address, styrs från SYS/kontrolenhet) |