#include <core.jlib>
#entrypoint .main

; Skriv ut "Hello World!" med pekare


.load_hello_world
    MV IM XI [0]
    MV IM MEM [72]  ; H
    MV IM XI [1]
    MV IM MEM [101] ; e
    MV IM XI [2]
    MV IM MEM [108] ; l
    MV IM XI [3]
    MV IM MEM [108] ; l
    MV IM XI [4]
    MV IM MEM [111] ; o
    MV IM XI [5]
    MV IM MEM [32]  ; ` `
    MV IM XI [6]
    MV IM MEM [119] ; W
    MV IM XI [7]
    MV IM MEM [111] ; o
    MV IM XI [8]
    MV IM MEM [114] ; r
    MV IM XI [9]
    MV IM MEM [108] ; l
    MV IM XI [10]
    MV IM MEM [100] ; d
    MV IM XI [11]
    MV IM MEM [33]  ; !
    MV IM XI [12]
    MV IM MEM [10]  ; <ny rad>
    SYS JMP .print

.print
    MV IM XI [0]
    MV IM YI [1]

.loop_begin
    MV MEM EX
    ADD SET_FLG
    MV ZO XI
    JMP .loop_begin | JMP .end

.main
    SYS SDEV [DEVICE_TEXT_ASCII] ; Konfigurera expansionsporten för att använda text
    JMP .load_hello_world


.end
    SYS HLT