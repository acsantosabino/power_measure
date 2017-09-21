# file: pruio.pxd

cdef extern from "pruio.h":
    ctypedef struct adcUdt:
        int *Value
        int Samples  #!< number of samples (specifies run mode: 0 = config, 1 = IO mode, >1 = MM (or RB) mode)

    ctypedef struct pruIo:
        adcUdt* Adc
        char* Errr

    cdef enum activateDevice:
        PRUIO_ACT_PRU1  =   1    , #//!< activate PRU-1 (= default, instead of PRU-0)
        PRUIO_ACT_ADC   = 1 << 1 , #//!< activate ADC
        PRUIO_ACT_GPIO0 = 1 << 2 , #//!< activate GPIO-0
        PRUIO_ACT_GPIO1 = 1 << 3 , #//!< activate GPIO-1
        PRUIO_ACT_GPIO2 = 1 << 4 , #//!< activate GPIO-2
        PRUIO_ACT_GPIO3 = 1 << 5 , #//!< activate GPIO-3
        PRUIO_ACT_PWM0  = 1 << 6 , #//!< activate PWMSS-0 (including eCAP, eQEP, ePWM)
        PRUIO_ACT_PWM1  = 1 << 7 , #//!< activate PWMSS-1 (including eCAP, eQEP, ePWM)
        PRUIO_ACT_PWM2  = 1 << 8 , #//!< activate PWMSS-2 (including eCAP, eQEP, ePWM)
        PRUIO_DEF_ACTIVE = 0xFFFF  #//!< activate all devices


    pruIo* pruio_new(int Act, int Av, int OpD, int SaD);
    char* pruio_config(pruIo* Io, int Samp, int Mask, int Tmr, int Mds);
    char* pruio_mm_start(pruIo* Io, int Trg1, int Trg2, int Trg3, int Trg4);
    char* pruio_rb_start(pruIo* Io);
    void pruio_destroy(pruIo* Io);
