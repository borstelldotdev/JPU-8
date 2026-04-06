# include <core.jlib>
# entrypoint .main

; XOR-a två inputs

.main
    SYS SDEV [DEVICE_NUM_DECIMAL] ; Konfigurera expansionsporten för att använda tal

    ; Ladda inputvärden
    MV IM XI [0b00101110]
    MV IM YI [0b10111000]

    ; Genomför XOR
    ALU OR
    MV ZO D
    ALU NAND
    MV ZO XI
    MV C YI
    ALU AND

    ; Skriv ut resultatet
    MV ZO EX

.end
    SYS HLT