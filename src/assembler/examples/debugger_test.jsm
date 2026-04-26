#include <core.jlib>
#entrypoint .main

.main
    SYS SDEV [DEVICE_NUM_DECIMAL]

    ; Hämta input-tal
    MV EX XI
    MV EX YI

    ; Addera
    ALU SUBC

    SYS PAUSE

    ; Skriv ut resultatet
    MV ZO EX

.end
    SYS HLT