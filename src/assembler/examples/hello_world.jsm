#include <core.jlib>
#entrypoint .main

; Skriv ut "Hello World!"


.main
    SYS SDEV [DEVICE_TEXT_ASCII] ; Konfigurera expansionsporten för att använda text

    MV IM EX [72]  ; H
    MV IM EX [101] ; e
    MV IM EX [108] ; l
    MV IM EX [108] ; l
    MV IM EX [111] ; o
    MV IM EX [32]  ; ` `
    MV IM EX [119] ; W
    MV IM EX [111] ; o
    MV IM EX [114] ; r
    MV IM EX [108] ; l
    MV IM EX [100] ; d
    MV IM EX [33]  ; !
    MV IM EX [10]  ; <ny rad>

.end
    SYS HLT