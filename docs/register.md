# Register

JPU-8 har 11 register:

| Namn   | Läs-address | Skriv-address | Anteckningar                                      |
|--------|-------------|---------------|---------------------------------------------------|
| A      | 000         | 0000          | GP                                                |
| B      | 001         | 0001          | GP                                                |
| C      | 010         | 0010          | GP                                                |
| D      | 011         | 0011          | GP (Används ofta för temporära värden)            |
| XI     | X           | 0000          | ALU input 1                                       |
| YI     | X           | 0000          | ALU input 2                                       |
| ZO     | 000         | X             | ALU output                                        |
| IM     | 000         | X             | Intermediate-värden                               |
| EX     | 000         | 0000          | Expansions-port                                   |
| MEM    | 000         | 0000          | Minne (XI: address)                               |
| PC-LSB | X           | 1000          | Programräknare LSB                                |
| PC-MSB | X           | 1001          | Programräknare MSB (latchande, uppdaterar endast när PC-LSB skrivs till)                              |
| HLT    | X           | 1111          | Stoppa klockan                                    |