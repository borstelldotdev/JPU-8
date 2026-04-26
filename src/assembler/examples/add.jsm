#include <core.jlib>
#entrypoint .main

; Addera två tal från användaren


.main
    SYS SDEV [DEVICE_NUM_DECIMAL] ; Konfigurera expansionsporten för att använda tal

    ; Hämta input-tal
    MV EX XI
    MV EX YI

    ; Addera
    ALU ADD

    ; Skriv ut resultatet
    MV ZO EX

.end
    SYS HLT