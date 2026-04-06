#include <core.jlib>
#entrypoint .main

.main
    SYS SDEV [DEVICE_NUM_DECIMAL] ; Konfigurera expansionsporten för att använda tal

    MV EX XI
    MV IM YI [50]
    SUBC SET_FLG

    MV IM EX [0] | MV IM EX [1]

.end
    HLT