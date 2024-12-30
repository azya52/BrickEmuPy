class MSM50XXdasm():

    def __init__(self):
        self._addrbase = '%0.3X'
        self._opbase = '%0.4X'

        self._instructions = (
            MSM50XXdasm._nop,                          #00 0000 0000 0000
            MSM50XXdasm._dummy,
            MSM50XXdasm._ror_a0,                       #00 0000 0010 AAAA
            MSM50XXdasm._asr_a0,                       #00 0000 0011 AAAA
            MSM50XXdasm._add_acc_a0,                   #00 0000 0100 AAAA
            MSM50XXdasm._adc_acc_a0,                   #00 0000 0101 AAAA
            MSM50XXdasm._bis_acc_a0,                   #00 0000 0110 AAAA
            MSM50XXdasm._xor_acc_a0,                   #00 0000 0111 AAAA
            MSM50XXdasm._dummy,
            MSM50XXdasm._clc,                          #00 0000 1001 0000
            MSM50XXdasm._clz,                          #00 0000 1010 0000
            MSM50XXdasm._cla,                          #00 0000 1011 0000
            MSM50XXdasm._dummy,
            MSM50XXdasm._jmp_a0,                       #00 0000 1101 AAAA
            MSM50XXdasm._bit_acc_a0,                   #00 0000 1110 AAAA
            *([MSM50XXdasm._dummy] * 3),
            MSM50XXdasm._ror_ap,                       #00 0001 0010 AAAA
            MSM50XXdasm._asr_ap,                       #00 0001 0011 AAAA
            MSM50XXdasm._add_acc_ap,                   #00 0001 0100 AAAA
            MSM50XXdasm._adc_acc_ap,                   #00 0000 0101 AAAA
            MSM50XXdasm._bis_acc_ap,                   #00 0001 0110 AAAA
            MSM50XXdasm._xor_acc_ap,                   #00 0001 0111 AAAA
            *([MSM50XXdasm._dummy] * 5),
            MSM50XXdasm._jmp_ap,                       #00 0001 1101 AAAA
            MSM50XXdasm._bit_acc_ap,                   #00 0001 1110 AAAA
            *([MSM50XXdasm._dummy] * 4),
            MSM50XXdasm._asl_a0,                       #00 0010 0011 AAAA
            MSM50XXdasm._sub_acc_a0,                   #00 0010 0100 AAAA
            MSM50XXdasm._sbc_acc_a0,                   #00 0010 0101 AAAA
            MSM50XXdasm._bic_acc_a0,                   #00 0010 0110 AAAA
            *([MSM50XXdasm._dummy] * 2),
            MSM50XXdasm._sec,                          #00 0010 1001 0000
            MSM50XXdasm._sez,                          #00 0010 1010 0000
            MSM50XXdasm._sea,                          #00 0010 1011 0000
            MSM50XXdasm._dummy,
            MSM50XXdasm._jmpio_a0,                     #00 0010 1101 AAAA
            MSM50XXdasm._cmp_acc_a0,                   #00 0010 1110 AAAA
            *([MSM50XXdasm._dummy] * 4),
            MSM50XXdasm._asl_ap,                       #00 0011 0011 AAAA
            MSM50XXdasm._sub_acc_ap,                   #00 0011 0100 AAAA
            MSM50XXdasm._sbc_acc_ap,                   #00 0011 0101 AAAA
            MSM50XXdasm._bic_acc_ap,                   #00 0011 0110 AAAA
            *([MSM50XXdasm._dummy] * 6),
            MSM50XXdasm._jmpio_ap,                     #00 0011 1101 AAAA
            MSM50XXdasm._cmp_acc_ap,                   #00 0011 1110 AAAA
            MSM50XXdasm._dummy,
            MSM50XXdasm._halt,                         #00 0100 0000 0000
            MSM50XXdasm._lmp_bkp_on_off,               #00 0100 0001 BBLL
            MSM50XXdasm._matrix_mn,                    #00 0100 0010 MMMM
            MSM50XXdasm._format_n,                     #00 0100 0011 NNNN
            MSM50XXdasm._int_16,                       #00 0100 0100 00ED
            MSM50XXdasm._page_n,                       #00 0100 0101 NNNN
            MSM50XXdasm._adrs_n,                       #00 0100 0110 NNNN
            MSM50XXdasm._dummy,
            MSM50XXdasm._rstrate,                      #00 0100 1000 1000
            *([MSM50XXdasm._dummy] * 2),
            MSM50XXdasm._int_32,                       #00 0100 1011 ED00
            MSM50XXdasm._buzzer_freq_sound,            #00 0100 1100 BBBB
            MSM50XXdasm._freq_n,                       #00 0100 1101 NNNN
            *([MSM50XXdasm._dummy] * 18),
            *([MSM50XXdasm._bcs_n] * 2),               #00 0110 000N NNNN
            *([MSM50XXdasm._dummy] * 2),
            *([MSM50XXdasm._bze_n] * 2),               #00 0110 010N NNNN
            *([MSM50XXdasm._ble_n] * 2),               #00 0110 011N NNNN
            *([MSM50XXdasm._bcc_n] * 2),               #00 0110 100N NNNN
            *([MSM50XXdasm._dummy] * 2),
            *([MSM50XXdasm._bnz_n] * 2),               #00 0110 110N NNNN
            *([MSM50XXdasm._bgt_n] * 2),               #00 0110 111N NNNN
            *([MSM50XXdasm._dummy] * 16),
            *([MSM50XXdasm._dsp_digit_a0] * 16),       #00 1000 DDDD AAAA
            *([MSM50XXdasm._dsp_digit_ap] * 16),       #00 1001 DDDD AAAA
            *([MSM50XXdasm._dsph_digit_a0] * 16),      #00 1010 DDDD AAAA
            *([MSM50XXdasm._dsph_digit_ap] * 16),      #00 1011 DDDD AAAA
            *([MSM50XXdasm._dspf_digit_a0] * 16),      #00 1100 DDDD AAAA
            *([MSM50XXdasm._dspf_digit_ap] * 16),      #00 1101 DDDD AAAA
            *([MSM50XXdasm._dspfh_digit_a0] * 16),     #00 1110 DDDD AAAA
            *([MSM50XXdasm._dspfh_digit_ap] * 16),     #00 1111 DDDD AAAA
            *([MSM50XXdasm._bis_d_a0] * 16),           #01 0000 DDDD AAAA
            *([MSM50XXdasm._bis_d_ap] * 16),           #01 0001 DDDD AAAA
            *([MSM50XXdasm._bic_d_a0] * 16),           #01 0010 DDDD AAAA
            *([MSM50XXdasm._bic_d_ap] * 16),           #01 0011 DDDD AAAA
            *([MSM50XXdasm._bit_d_a0] * 16),           #01 0100 DDDD AAAA
            *([MSM50XXdasm._bit_d_ap] * 16),           #01 0101 DDDD AAAA
            *([MSM50XXdasm._cmp_d_a0] * 16),           #01 0110 DDDD AAAA
            *([MSM50XXdasm._cmp_d_ap] * 16),           #01 0111 DDDD AAAA
            *([MSM50XXdasm._add_d_a0] * 16),           #01 1000 DDDD AAAA
            *([MSM50XXdasm._add_d_ap] * 16),           #01 1001 DDDD AAAA
            #MSM50XXdasm._inc_ap,                      #01 100P 0001 AAAA
            *([MSM50XXdasm._sub_d_a0] * 16),           #01 1010 DDDD AAAA
            *([MSM50XXdasm._sub_d_ap] * 16),           #01 1011 DDDD AAAA
            #MSM50XXdasm._dec_ap,                      #01 101P 0001 AAAA
            *([MSM50XXdasm._mov_d_a0] * 16),           #01 1100 DDDD AAAA
            *([MSM50XXdasm._mov_d_ap] * 16),           #01 1101 DDDD AAAA
            *([MSM50XXdasm._xor_d_a0] * 16),           #01 1110 DDDD AAAA
            *([MSM50XXdasm._xor_d_ap] * 16),           #01 1111 DDDD AAAA
            *([MSM50XXdasm._jmp_adrs] * 256),          #10 AAAA AAAA AAAA
            *([MSM50XXdasm._adjust_n_a0] * 16),        #11 0000 NNNN AAAA
            *([MSM50XXdasm._adjust_n_ap] * 16),        #11 0001 NNNN AAAA
            *([MSM50XXdasm._dummy] * 33),
            MSM50XXdasm._switch_a0,                    #11 0100 0001 AAAA
            MSM50XXdasm._kswitch_a0,                   #11 0100 0010 AAAA
            MSM50XXdasm._dummy,
            MSM50XXdasm._intmode_a0,                   #11 0100 0100 AAAA
            *([MSM50XXdasm._dummy] * 4),
            MSM50XXdasm._rate_a0,                      #11 0100 1001 AAAA
            *([MSM50XXdasm._dummy] * 7),
            MSM50XXdasm._switch_ap,                    #11 0101 0001 AAAA
            MSM50XXdasm._kswitch_ap,                   #11 0101 0010 AAAA
            MSM50XXdasm._dummy,
            MSM50XXdasm._intmode_ap,                   #11 0101 0100 AAAA
            *([MSM50XXdasm._dummy] * 4),
            MSM50XXdasm._rate_ap,                      #11 0101 1001 AAAA
            *([MSM50XXdasm._dummy] * 8),
            MSM50XXdasm._matrix_a0,                    #11 0110 0010 AAAA
            MSM50XXdasm._format_a0,                    #11 0110 0011 AAAA
            MSM50XXdasm._dummy,
            MSM50XXdasm._page_a0,                      #11 0110 0101 AAAA
            MSM50XXdasm._adrs_a0,                      #11 0110 0110 AAAA
            *([MSM50XXdasm._dummy] * 11),
            MSM50XXdasm._matrix_ap,                    #11 0111 0010 AAAA
            MSM50XXdasm._format_ap,                    #11 0111 0011 AAAA
            *([MSM50XXdasm._dummy] * 2),
            MSM50XXdasm._adrs_ap,                      #11 0111 0110 AAAA
            *([MSM50XXdasm._dummy] * 9),
            *([MSM50XXdasm._chg_ax] * 8),              #11 1000 0XXX AAAA
            *([MSM50XXdasm._dummy] * 8),
            MSM50XXdasm._chg_ap,                       #11 1001 0000 AAAA
            *([MSM50XXdasm._dummy] * 47),
            *([MSM50XXdasm._mov_acc_ax] * 8),          #11 1100 0XXX AAAA
            *([MSM50XXdasm._dummy] * 8),
            MSM50XXdasm._mov_acc_ap,                   #11 1101 0000 AAAA
            *([MSM50XXdasm._dummy] * 15),
            *([MSM50XXdasm._mov_ax_acc] * 8),          #11 1110 0XXX AAAA
            *([MSM50XXdasm._dummy] * 8),
            MSM50XXdasm._mov_ap_acc,                   #11 1111 0000 AAAA
            *([MSM50XXdasm._dummy] * 15)
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            return {"LISTING": tuple(self._disassemble(0, rom))}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, rom):
        listing = []
        while ((pc * 2) < rom.size()):
            opcode = rom.getWord(pc * 2)
            listing.append((self._opbase % opcode, self._instructions[opcode >> 4](self, pc, opcode)))
            pc += 1
        return listing

    def _nop(self, pc, opcode):
        #00 0000 0000 0000
        return "nop"

    def _ror_a0(self, pc, opcode):
        #00 0000 0010 AAAA
        return "ror (0x%0.1X)" % (opcode & 0xF)

    def _asr_a0(self, pc, opcode):
        #00 0000 0011 AAAA
        return "asr (0x%0.1X)" % (opcode & 0xF)

    def _add_acc_a0(self, pc, opcode):
        #00 0000 0100 AAAA
        return "add ACC, (0x%0.1X)" % (opcode & 0xF)

    def _adc_acc_a0(self, pc, opcode):
        #00 0000 0101 AAAA
        return "adc ACC, (0x%0.1X)" % (opcode & 0xF)

    def _bis_acc_a0(self, pc, opcode):
        #00 0000 0110 AAAA
        return "bis ACC, (0x%0.1X)" % (opcode & 0xF)

    def _xor_acc_a0(self, pc, opcode):
        #00 0000 0111 AAAA
        return "xor ACC, (0x%0.1X)" % (opcode & 0xF)

    def _clc(self, pc, opcode):
        #00 0000 1001 0000
        return "clc"

    def _clz(self, pc, opcode):
        #00 0000 1010 0000
        return "clz"

    def _cla(self, pc, opcode):
        #00 0000 1011 0000
        return "cla"

    def _jmp_a0(self, pc, opcode):
        #00 0000 1101 AAAA
        return "jmp +(0x%0.1X)" % (opcode & 0xF)

    def _bit_acc_a0(self, pc, opcode):
        #00 0000 1110 AAAA
        return "bit ACC, (0x%0.1X)" % (opcode & 0xF)

    def _ror_ap(self, pc, opcode):
        #00 0001 0010 AAAA
        return "ror P(0x%0.1X)" % (opcode & 0xF)

    def _asr_ap(self, pc, opcode):
        #00 0001 0011 AAAA
        return "asr P(0x%0.1X)" % (opcode & 0xF)

    def _add_acc_ap(self, pc, opcode):
        #00 0001 0100 AAAA
        return "add ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _adc_acc_ap(self, pc, opcode):
        #00 0001 0101 AAAA
        return "adc ACC, (0x%0.1X)" % (opcode & 0xF)

    def _bis_acc_ap(self, pc, opcode):
        #00 0001 0110 AAAA
        return "bis ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _xor_acc_ap(self, pc, opcode):
        #00 0001 0111 AAAA
        return "xor ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _jmp_ap(self, pc, opcode):
        #00 0001 1101 AAAA
        return "jmp +P(0x%0.1X)" % (opcode & 0xF)

    def _bit_acc_ap(self, pc, opcode):
        #00 0001 1110 AAAA
        return "bit ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _asl_a0(self, pc, opcode):
        #00 0010 0011 AAAA
        return "asl (0x%0.1X)" % (opcode & 0xF)

    def _sub_acc_a0(self, pc, opcode):
        #00 0010 0100 AAAA
        return "sub ACC, (0x%0.1X)" % (opcode & 0xF)

    def _sbc_acc_a0(self, pc, opcode):
        #00 0010 0101 AAAA
        return "sbc ACC, (0x%0.1X)" % (opcode & 0xF)

    def _bic_acc_a0(self, pc, opcode):
        #00 0010 0110 AAAA
        return "bic ACC, (0x%0.1X)" % (opcode & 0xF)

    def _sec(self, pc, opcode):
        #00 0010 1001 0000
        return "sec"

    def _sez(self, pc, opcode):
        #00 0010 1010 0000
        return "sez"

    def _sea(self, pc, opcode):
        #00 0010 1011 0000
        return "sea"

    def _jmpio_a0(self, pc, opcode):
        #00 0010 1101 AAAA
        return "jmpio +(0x%0.1X) & 0x7" % (opcode & 0xF)

    def _cmp_acc_a0(self, pc, opcode):
        #00 0010 1110 AAAA
        return "cmp ACC, (0x%0.1X)" % (opcode & 0xF)

    def _asl_ap(self, pc, opcode):
        #00 0011 0011 AAAA
        return "asl P(0x%0.1X)" % (opcode & 0xF)

    def _sub_acc_ap(self, pc, opcode):
        #00 0011 0100 AAAA
        return "sub ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _sbc_acc_ap(self, pc, opcode):
        #00 0011 0101 AAAA
        return "sbc ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _bic_acc_ap(self, pc, opcode):
        #00 0011 0110 AAAA
        return "bic ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _jmpio_ap(self, pc, opcode):
        #00 0011 1101 AAAA
        return "jmpio +P(0x%0.1X) & 0x7" % (opcode & 0xF)

    def _cmp_acc_ap(self, pc, opcode):
        #00 0011 1110 AAAA
        return "cmp ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _halt(self, pc, opcode):
        #00 0100 0000 0000
        return "halt"

    def _lmp_bkp_on_off(self, pc, opcode):
        #00 0100 0001 BBLL
        if (opcode & 0x3):
            return "lamp on/off"
        return "backup on/off"

    def _matrix_mn(self, pc, opcode):
        #00 0100 0010 MMMM
        return "matrix 0x%0.1X" % (opcode & 0xF)

    def _format_n(self, pc, opcode):
        #00 0100 0011 NNNN
        return "format 0x%0.1X" % (opcode & 0xF)

    def _int_16(self, pc, opcode):
        #00 0100 0100 00ED
        if (opcode & 0x1):
            return "intds 16"
        return "inten 16"

    def _page_n(self, pc, opcode):
        #00 0100 0101 NNNN
        return "page 0x%0.1X" % (opcode & 0xF)

    def _adrs_n(self, pc, opcode):
        #00 0100 0110 NNNN
        return "adrs 0x%0.1X" % (opcode & 0xF)
    
    def _rstrate(self, pc, opcode):
        #00 0100 1000 1000
        return "rstrate"

    def _int_32(self, pc, opcode):
        #00 0100 1011 ED00
        if (opcode & 0x4):
            return "intds 32"
        return "inten 32"

    def _buzzer_freq_sound(self, pc, opcode):
        #00 0100 1100 BBBB
        return "buzzer 0x%0.1X" % (opcode & 0xF)

    def _freq_n(self, pc, opcode):
        #00 0100 1101 BBBB
        return "freq 0x%0.1X" % (opcode & 0xF)
    
    def _bcs_n(self, pc, opcode):
        #00 0110 000N NNNN
        return "bcs %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _bze_n(self, pc, opcode):
        #00 0110 010N NNNN
        return "bze %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _ble_n(self, pc, opcode):
        #00 0110 011N NNNN
        return "ble %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _bcc_n(self, pc, opcode):
        #00 0110 100N NNNN
        return "bcc %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _bnz_n(self, pc, opcode):
        #00 0110 110N NNNN
        return "bnz %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _bgt_n(self, pc, opcode):
        #00 0110 111N NNNN
        return "bgt %0.3X" % (pc + (opcode & 0x1F) + 1)

    def _dsp_digit_a0(self, pc, opcode):
        #00 1000 DDDD AAAA
        return "dsp 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _dsp_digit_ap(self, pc, opcode):
        #00 1001 DDDD AAAA
        return "dsp 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)
    
    def _dsph_digit_a0(self, pc, opcode):
        #00 1010 DDDD AAAA
        return "dspf 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _dsph_digit_ap(self, pc, opcode):
        #00 1011 DDDD AAAA
        return "dspf 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)
    
    def _dspf_digit_a0(self, pc, opcode):
        #00 1100 DDDD AAAA
        return "dspf 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _dspf_digit_ap(self, pc, opcode):
        #00 1101 DDDD AAAA
        return "dspf 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _dspfh_digit_a0(self, pc, opcode):
        #00 1110 DDDD AAAA
        return "dspfh 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _dspfh_digit_ap(self, pc, opcode):
        #00 1111 DDDD AAAA
        return "dspfh 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)
    
    def _bis_d_a0(self, pc, opcode):
        #01 0000 DDDD AAAA
        return "bis 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _bis_d_ap(self, pc, opcode):
        #01 0001 DDDD AAAA
        return "bis 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _bic_d_a0(self, pc, opcode):
        #01 0010 DDDD AAAA
        return "bic 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _bic_d_ap(self, pc, opcode):
        #01 0011 DDDD AAAA
        return "bic 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _bit_d_a0(self, pc, opcode):
        #01 0100 DDDD AAAA
        return "bit 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _bit_d_ap(self, pc, opcode):
        #01 0101 DDDD AAAA
        return "bit 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _cmp_d_a0(self, pc, opcode):
        #01 0110 DDDD AAAA
        return "cmp 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _cmp_d_ap(self, pc, opcode):
        #01 0111 DDDD AAAA
        return "cmp 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _add_d_a0(self, pc, opcode):
        #01 1000 DDDD AAAA
        d = (opcode >> 4) & 0xF
        if (d == 1):
            return "inc (0x%0.1X)" % (opcode & 0xF)
        return "add 0x%0.1X, (0x%0.1X)" % (d, opcode & 0xF)

    def _add_d_ap(self, pc, opcode):
        #01 1001 DDDD AAAA
        d = (opcode >> 4) & 0xF
        if (d == 1):
            return "inc P(0x%0.1X)" % (opcode & 0xF)
        return "add 0x%0.1X, P(0x%0.1X)" % (d, opcode & 0xF)

    def _sub_d_a0(self, pc, opcode):
        #01 1010 DDDD AAAA
        d = (opcode >> 4) & 0xF
        if (d == 1):
            return "dec (0x%0.1X)" % (opcode & 0xF)
        return "sub 0x%0.1X, (0x%0.1X)" % (d, opcode & 0xF)

    def _sub_d_ap(self, pc, opcode):
        #01 1011 DDDD AAAA
        d = (opcode >> 4) & 0xF
        if (d == 1):
            return "dec P(0x%0.1X)" % (opcode & 0xF)
        return "sub 0x%0.1X, P(0x%0.1X)" % (d, opcode & 0xF)

    def _mov_d_a0(self, pc, opcode):
        #01 1100 DDDD AAAA
        return "mov 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _mov_d_ap(self, pc, opcode):
        #01 1101 DDDD AAAA
        return "mov 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _xor_d_a0(self, pc, opcode):
        #01 1110 DDDD AAAA
        return "xor 0x%0.1X, (0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _xor_d_ap(self, pc, opcode):
        #01 1111 DDDD AAAA
        return "xor 0x%0.1X, P(0x%0.1X)" % ((opcode >> 4) & 0xF, opcode & 0xF)

    def _jmp_adrs(self, pc, opcode):
        #10 AAAA AAAA AAAA
        return "jmp %0.3X" % (opcode & 0xFFF)

    def _adjust_n_a0(self, pc, opcode):
        #11 0000 NNNN AAAA
        return "adjust 0x%0.1X, (0x%0.1X)" % (~((opcode >> 4) - 1) & 0xF, opcode & 0xF)

    def _adjust_n_ap(self, pc, opcode):
        #11 0001 NNNN AAAA
        return "adjust 0x%0.1X, P(0x%0.1X)" % (~((opcode >> 4) - 1) & 0xF, opcode & 0xF)

    def _switch_a0(self, pc, opcode):
        #11 0100 0001 AAAA
        return "switch (0x%0.1X)" % (opcode & 0xF)

    def _kswitch_a0(self, pc, opcode):
        #11 0100 0010 AAAA
        return "kswitch (0x%0.1X)" % (opcode & 0xF)

    def _intmode_a0(self, pc, opcode):
        #11 0100 0100 AAAA
        return "intmode (0x%0.1X)" % (opcode & 0xF)

    def _rate_a0(self, pc, opcode):
        #11 0100 1001 AAAA
        return "rate (0x%0.1X)" % (opcode & 0xF)

    def _switch_ap(self, pc, opcode):
        #11 0101 0001 AAAA
        return "switch P(0x%0.1X)" % (opcode & 0xF)

    def _kswitch_ap(self, pc, opcode):
        #11 0101 0010 AAAA
        return "kswitch P(0x%0.1X)" % (opcode & 0xF)

    def _intmode_ap(self, pc, opcode):
        #11 0101 0100 AAAA
        return "intmode P(0x%0.1X)" % (opcode & 0xF)

    def _rate_ap(self, pc, opcode):
        #11 0101 1001 AAAA
        return "rate P(0x%0.1X)" % (opcode & 0xF)

    def _matrix_a0(self, pc, opcode):
        #11 0110 0010 AAAA
        return "matrix (0x%0.1X)" % (opcode & 0xF)

    def _format_a0(self, pc, opcode):
        #11 0110 0011 AAAA
        return  "format (0x%0.1X)" % (opcode & 0xF)

    def _page_a0(self, pc, opcode):
        #11 0110 0101 AAAA
        return  "page (0x%0.1X)" % (opcode & 0xF)
    
    def _adrs_a0(self, pc, opcode):
        #11 0110 0110 AAAA
        return  "adrs (0x%0.1X)" % (opcode & 0xF)
    
    def _matrix_ap(self, pc, opcode):
        #11 0111 0010 AAAA
        return "matrix P(0x%0.1X)" % (opcode & 0xF)

    def _format_ap(self, pc, opcode):
        #11 0111 0011 AAAA
        return "format P(0x%0.1X)" % (opcode & 0xF)
    
    def _adrs_ap(self, pc, opcode):
        #11 0111 0110 AAAA
        return  "adrs (0x%0.1X)" % (opcode & 0xF)

    def _chg_ax(self, pc, opcode):
        #11 1000 0XXX AAAA
        return "chg %0.1X(0x%0.1X)" % ((opcode >> 4) & 0x7, opcode & 0xF)

    def _chg_ap(self, pc, opcode):
        #11 1001 0000 AAAA
        return "chg P(0x%0.1X)" % (opcode & 0xF)

    def _mov_acc_ax(self, pc, opcode):
        #11 1100 0XXX AAAA
        return "mov ACC, %0.1X(0x%0.1X)" % ((opcode >> 4) & 0x7, opcode & 0xF)

    def _mov_acc_ap(self, pc, opcode):
        #11 1101 0000 AAAA
        return "mov ACC, P(0x%0.1X)" % (opcode & 0xF)

    def _mov_ax_acc(self, pc, opcode):
        #11 1110 0XXX AAAA
        return "mov %0.1X(0x%0.1X), ACC" % ((opcode >> 4) & 0x7, opcode & 0xF)

    def _mov_ap_acc(self, pc, opcode):
        #11 1111 0000 AAAA
        return "mov P(0x%0.1X), ACC" % (opcode & 0xF)

    def _dummy(self, pc, opcode):
        #11 1111 0000 AAAA
        return "undefine"
