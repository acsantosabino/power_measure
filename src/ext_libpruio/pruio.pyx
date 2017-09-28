cimport cpruio

cdef class Pruio:

    cdef cpruio.pruIo* _c_pruio
    cdef public int mask

    def __cinit__(self, int Act, int Av, int OpD, int SaD):
        print "Pruio init"
        self._c_pruio = cpruio.pruio_new(Act, Av, OpD, SaD)
        if (self._c_pruio.Errr):
            print "constructor failed ", self._c_pruio.Errr
        self.mask = 0x1FE #// &b111111110 (steps 1 to 8 for AIN0 to AIN7, no charge step)


    def config(self, int Samp, int Mask, int Tmr, int Mds):
        ans = cpruio.pruio_config(self._c_pruio, Samp, Mask, Tmr, Mds)
        if (ans):
            print "config failed ", self._c_pruio.Errr
            return 1

        self.mask = Mask if Samp>1 else 0x1FE

    def mm_start(self, int Trg1, int Trg2, int Trg3, int Trg4):
        ans = cpruio.pruio_mm_start(self._c_pruio, Trg1, Trg2, Trg3, Trg4)
        if (ans):
            print "mm_start failed ", self._c_pruio.Errr
            return 1

    def rb_start(self):
        ans = cpruio.pruio_rb_start(self._c_pruio)
        if (ans):
            print "rb_start failed ", self._c_pruio.Errr
            return 1

    def get_adc_actived_ch(self):

        ch_dict = {}
        for i in range(8):
            if self.mask & (1<<(i+1)):
                ch_dict["AIN{}".format(i)]=[]
        return ch_dict

    def get_adc_value(self, int samps):
        v = []

        for i in range(samps):
            v.append(self._c_pruio.Adc.Value[i])

        return v

    def read_adc_ch(self):

        data = self.get_adc_actived_ch()
        data_size = 8 if self._c_pruio.Adc.Samples==1 else self._c_pruio.Adc.Samples
        data_map = data.keys()
        data_map.sort()
        value = self.get_adc_value(data_size)

        for i in range(data_size):
            data[data_map[i%len(data)]].append(value[i])
        return data

    def __dealloc__(self):
        if self._c_pruio is not NULL:
            cpruio.pruio_destroy(self._c_pruio);
