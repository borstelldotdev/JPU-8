#include <core.jlib>
#entrypoint .main

.main
    SYS SDEV [DEVICE_NUM_DECIMAL] ; Konfigurera expansionsporten för att använda tal

    MV EX XI      ; Få input från användaren
    MV IM YI [50] ; Ladda 50
    ALU SUBC SET_FLG  ; Subtrahera, och sätt flaggan ifall resultatet blir negativt (då input > 50)

    MV IM EX [0] | MV IM EX [1] ; Skriv ut 1 om flaggan är satt (dvs om input > 50), annars 0

.end
    SYS HLT