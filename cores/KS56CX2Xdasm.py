class KS56CX2Xdasm():

    def __init__(self):
        self._base = '0x%X'
        self._nibbase = '0x%0.1X'
        self._bytebase = '0x%0.2X'
        self._rambase = '0x%0.3X'
        self._addrbase = '%00.4X'
        self._opbase = '%0.3X'

        self._reg_tbl = (
            "A",
            "X",
            "L",
            "H",
            "E",
            "D",
            "C",
            "B"
        )

        self._rpe_tbl = (
            "XA",
            "XA'",
            "HL",
            "HL'",
            "DE",
            "DE'",
            "BC",
            "BC'"
        )

        self._clr_fmem_tbl = {
            0b10110010: "di",
            0b10011000: "di IEBT",
            0b10011010: "di IEW",
            0b10011011: "di IETPG",
            0b10011100: "di IET0",
            0b10011101: "di IECSI0",
            0b10011110: "di IE0",
            0b10011111: "di IE2",
            0b10111000: "di IE4",
            0b10111011: "di IEKS",
            0b10111110: "di IE1"
        }

        self._set_fmem_tbl = {
            0b10110010: "ei",
            0b10100011: "halt",
            0b10110011: "stop",
            0b10011000: "ei IEBT",
            0b10011010: "ei IEW",
            0b10011011: "ei IETPG",
            0b10011100: "ei IET0",
            0b10011101: "ei IECSI0",
            0b10011110: "ei IE0",
            0b10011111: "ei IE2",
            0b10111000: "ei IE4",
            0b10111011: "ei IEKS",
            0b10111110: "ei IE1"
        }

        self._io_tbl = {
            0xF80: "SPl",
            0xF81: "SPh",
            0xF82: "RBS",
            0xF83: "MBS",
            0xF84: "SBS",
            0xF85: "BS",
            0xF86: "BTl",
            0xF87: "BTh",
            0xF88: "TMOD2Hl",
            0xF89: "TMOD2Hh",
            0xF8B: "WDTM",
            0xF8C: "LCDMl",
            0xF8D: "LCDMh",
            0xF8E: "LCDC",
            0xF8F: "LPS",
            0xF90: "TM2l",
            0xF91: "TM2h",
            0xF92: "TC2l",
            0xF93: "TC2h",
            0xF94: "T2l",
            0xF95: "T2h",
            0xF96: "TMOD2l",
            0xF97: "TMOD2h",
            0xF98: "WMl",
            0xF99: "WMh",
            0xFA0: "TM0l",
            0xFA1: "TM0h",
            0xFA2: "TOE0",
            0xFA4: "T0l",
            0xFA5: "T0h",
            0xFA6: "TMOD0l",
            0xFA7: "TMOD0h",
            0xFA8: "TM1l",
            0xFA9: "TM1h",
            0xFAA: "TOE1",
            0xFAC: "T1l",
            0xFAD: "T1h",
            0xFAE: "TMOD1l",
            0xFAF: "TMOD1h",
            0xFB0: "PSWl",
            0xFB1: "PSWh",
            0xFB2: "IPS",
            0xFB3: "PCC",
            0xFB4: "IM0",
            0xFB5: "IM1",
            0xFB6: "IM2",
            0xFB7: "SCC",
            0xFB8: "INTA",
            0xFBA: "INTC",
            0xFBC: "INTE",
            0xFBD: "INTF",
            0xFBE: "INTG",
            0xFBF: "INTH",
            0xFC0: "BSB0",
            0xFC1: "BSB1",
            0xFC2: "BSB2",
            0xFC3: "BSB3",
            0xFCF: "SOS",
            0xFD0: "CLOM",
            0xFDC: "POGAl",
            0xFDD: "POGAh",
            0xFDE: "POGBl",
            0xFDF: "POGBh",
            0xFE0: "CSIMl",
            0xFE1: "CSIMh",
            0xFE2: "SBICl",
            0xFE3: "SBICh",
            0xFE4: "SIOl",
            0xFE5: "SIOh",
            0xFE6: "SVAl",
            0xFE7: "SVAh",
            0xFE8: "PMGAl",
            0xFE9: "PMGAh",
            0xFEC: "PMGBl",
            0xFED: "PMGBh",
            0xFEE: "PMGCl",
            0xFEF: "PMGCh",
            0xFF0: "PORT0",
            0xFF1: "PORT1",
            0xFF2: "PORT2",
            0xFF3: "PORT3",
            0xFF5: "PORT5",
            0xFF6: "PORT6",
            0xFF8: "PORT8",
            0xFF9: "PORT9",
        }

        self._instruction_tbl = (
            *([KS56CX2Xdasm._br_raddr] * 16),             #0000 A3 A2 A1 A0
            *([KS56CX2Xdasm._geti_taddr] * 48),           #00 T5 T4 T3 T2 T1 T0
            *([KS56CX2Xdasm._callf_faddr] * 8),           #01000 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            KS56CX2Xdasm._pop_xa,                         #01001000
            KS56CX2Xdasm._push_xa,                        #01001001
            KS56CX2Xdasm._pop_hl,                         #01001010
            KS56CX2Xdasm._push_hl,                        #01001011
            KS56CX2Xdasm._pop_de,                         #01001100
            KS56CX2Xdasm._push_de,                        #01001101
            KS56CX2Xdasm._pop_bc,                         #01001110
            KS56CX2Xdasm._push_bc,                        #01001111
            *([KS56CX2Xdasm._brcb_caddr] * 16),           #0101 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            #KS56CX2Xdasm._nop,                           #01100000
            *([KS56CX2Xdasm._adds_a_n4] * 16),            #0110 I3 I2 I1 I0
            *([KS56CX2Xdasm._mov_a_n4] * 16),             #0111 I3 I2 I1 I0
            KS56CX2Xdasm._ske_a_ahl,                      #10000000
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._incs_mem,                       #10000010 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._clr1_mem0,                      #10000100 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._set1_mem0,                      #10000101 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skf_mem0,                       #10000110 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skt_mem0,                       #10000111 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._mov_xa_n8,                      #10001001 | I7 I6 I5 I4 I3 I2 I1 I0
            KS56CX2Xdasm._incs_hl,                        #10001010
            KS56CX2Xdasm._mov_hl_n8,                      #10001011 | I7 I6 I5 I4 I3 I2 I1 I0
            KS56CX2Xdasm._incs_de,                        #10001100
            KS56CX2Xdasm._mov_de_n8,                      #10001101 | I7 I6 I5 I4 I3 I2 I1 I0
            KS56CX2Xdasm._incs_bc,                        #10001110
            KS56CX2Xdasm._mov_bc_n8,                      #10001111 | I7 I6 I5 I4 I3 I2 I1 I0
            KS56CX2Xdasm._and_a_ahl,                      #10010000
            KS56CX2Xdasm._dummy,
            #KS56CX2Xdasm._out_portn_xa,                  #10010010 | 1111 N3 N2 N1 N0
            KS56CX2Xdasm._mov_mem_xa,                     #10010010 | D7 D6 D5 D4 D3 D2 D1 0
            #KS56CX2Xdasm._out_portn_a,                   #10010011 | 1111 N3 N2 N1 N0
            KS56CX2Xdasm._mov_mem_a,                      #10010011 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._clr1_mem1,                      #10010100 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._set1_mem1,                      #10010101 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skf_mem1,                       #10010110 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skt_mem1,                       #10010111 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._rorc_a,                         #10011000
            KS56CX2Xdasm._instruction_10011001,           #10011001
            KS56CX2Xdasm._instruction_10011010,           #10011010
            KS56CX2Xdasm._instruction_10011011,           #10011011
            KS56CX2Xdasm._instruction_10011100,           #10011100
            KS56CX2Xdasm._instruction_10011101,           #10011101
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._instruction_10011111,           #10011111
            KS56CX2Xdasm._or_a_ahl,                       #10100000
            KS56CX2Xdasm._dummy,
            #KS56CX2Xdasm._in_xa,portn,                   #10100010 | 1111 N3 N2 N1 N0
            KS56CX2Xdasm._mov_xa_mem,                     #10100010 | D7 D6 D5 D4 D3 D2 D1 0
            #KS56CX2Xdasm._in_a_portn,                    #10100011 | 1111 N3 N2 N1 N0
            KS56CX2Xdasm._mov_a_mem,                      #10100011 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._clr1_mem2,                      #10100100 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._set1_mem2,                      #10100101 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skf_mem2,                       #10100110 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skt_mem2,                       #10100111 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._subs_a_ahl,                     #10101000
            KS56CX2Xdasm._addc_a_ahl,                     #10101001
            KS56CX2Xdasm._instruction_10101010,           #10101010
            KS56CX2Xdasm._instruction_10101011,           #10101011
            KS56CX2Xdasm._instruction_10101100,           #10101100
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._instruction_10101110,           #10101110
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._xor_a_ahl,                      #10110000
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._xch_xa_mem,                     #10110010 | D7 D6 D5 D4 D3 D2 D1 0
            KS56CX2Xdasm._xch_a_mem,                      #10110011 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._clr1_mem3,                      #10110100 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._set1_mem3,                      #10110101 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skf_mem3,                       #10110110 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._skt_mem3,                       #10110111 | D7 D6 D5 D4 D3 D2 D1 D0
            KS56CX2Xdasm._subc_a_ahl,                     #10111000
            KS56CX2Xdasm._adds_xa_n8,                     #10111001 | I7 I6 I5 I4 I3 I2 I1 I0
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._instruction_10111100,           #10111100
            KS56CX2Xdasm._instruction_10111101,           #10111101
            KS56CX2Xdasm._instruction_10111110,           #10111110
            KS56CX2Xdasm._instruction_10111111,           #10111111
            *([KS56CX2Xdasm._incs_reg] * 8),              #11000 R2 R1 R0
            *([KS56CX2Xdasm._decs_reg] * 8),              #11001 R2 R1 R0
            KS56CX2Xdasm._movt_xa_pcxa,                   #11010000
            KS56CX2Xdasm._movt_xa_bcxa,                   #11010001
            KS56CX2Xdasm._adds_a_ahl,                     #11010010
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._movt_xa_pcde,                   #11010100
            KS56CX2Xdasm._movt_xa_bcde,                   #11010101
            KS56CX2Xdasm._not1_cy,                        #11010110
            KS56CX2Xdasm._skt_cy,                         #11010111
            *([KS56CX2Xdasm._xch_a_reg1] * 8),            #11011 R2 R1 R0
            KS56CX2Xdasm._rets,                           #11100000
            KS56CX2Xdasm._mov_a_ahl,                      #11100001
            KS56CX2Xdasm._mov_a_ahli,                     #11100010
            KS56CX2Xdasm._mov_a_ahld,                     #11100011
            KS56CX2Xdasm._mov_a_ade,                      #11100100
            KS56CX2Xdasm._mov_a_adl,                      #11100101
            KS56CX2Xdasm._clr1_cy,                        #11100110
            KS56CX2Xdasm._set1_cy,                        #11100111
            KS56CX2Xdasm._mov_ahl_a,                      #11101000
            KS56CX2Xdasm._xch_a_ahl,                      #11101001
            KS56CX2Xdasm._xch_a_ahli,                     #11101010
            KS56CX2Xdasm._xch_a_ahld,                     #11101011
            KS56CX2Xdasm._xch_a_ade,                      #11101100
            KS56CX2Xdasm._xch_a_adl,                      #11101101
            KS56CX2Xdasm._ret,                            #11101110
            KS56CX2Xdasm._reti,                           #11101111
            *([KS56CX2Xdasm._br_mraddr] * 16)             #1111 S3 S2 S1 S0
        )

        self._instruction_10101011_tbl = (
            KS56CX2Xdasm._br_addr,                        #10101011 | 00 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
            KS56CX2Xdasm._call_addr                       #10101011 | 01 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        )

        self._instruction_10011001_tbl = (
            KS56CX2Xdasm._br_pcxa,                        #10011001 | 00000000
            KS56CX2Xdasm._br_bcxa,                        #10011001 | 00000001
            KS56CX2Xdasm._incs_ahl,                       #10011001 | 00000010
            KS56CX2Xdasm._dummy,
            KS56CX2Xdasm._br_pcde,                        #10011001 | 00000100
            KS56CX2Xdasm._br_bcde,                        #10011001 | 00000101
            KS56CX2Xdasm._pop_bs,                         #10011001 | 00000110
            KS56CX2Xdasm._push_bs,                        #10011001 | 00000111
            *([KS56CX2Xdasm._ske_a_reg] * 8),             #10011001 | 00001 R2 R1 R0
            *([KS56CX2Xdasm._sel_mbn] * 16),              #10011001 | 0001 N3 N2 N1 N0
            *([KS56CX2Xdasm._sel_rbn] * 4),               #10011001 | 001000 N1 N0
            *([KS56CX2Xdasm._dummy] * 12),
            *([KS56CX2Xdasm._and_a_n4] * 16),             #10011001 | 0011 I3 I2 I1 I0
            *([KS56CX2Xdasm._or_a_n4] * 16),              #10011001 | 0100 I3 I2 I1 I0
            #KS56CX2Xdasm._not_a,                         #10011001 | 01011111
            *([KS56CX2Xdasm._xor_a_n4] * 16),             #10011001 | 0101 I3 I2 I1 I0
            *([KS56CX2Xdasm._ske_ahl_n4] * 16),           #10011001 | 0110 I3 I2 I1 I0
            *([KS56CX2Xdasm._mov_reg1_a] * 8),            #10011001 | 01110 R2 R1 R0
            *([KS56CX2Xdasm._mov_a_reg] * 8)              #10011001 | 01111 R2 R1 R0
        )

        self._instruction_10011010_tbl = (
            KS56CX2Xdasm._ske_reg_n4,                     #10011010 | I3 I2 I1 I0 0 R2 R1 R0
            KS56CX2Xdasm._mov_reg1_n4                     #10011010 | I3 I2 I1 I0 1 R2 R1 R0
        )

        self._instruction_10011011_tbl = (
            KS56CX2Xdasm._mov1_hmembit_cy,                #10011011 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._mov1_pmeml_cy,                  #10011011 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._mov1_fmembit_cy,                #10011011 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._mov1_fmembit_cy                 #10011011 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10011100_tbl = (
            KS56CX2Xdasm._clr1_hmembit,                   #10011100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._clr1_pmeml,                     #10011100 | 0100 G3 G2 G1 G0
            #KS56CX2Xdasm._di,                            #10011100 | 10110010
            #KS56CX2Xdasm._di_iexxx,                      #10011100 | 10 N5 1 1 N2 N1 N0
            KS56CX2Xdasm._clr1_fmembit,                   #10011100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._clr1_fmembit                    #10011100 | 11 B1 B0 F3 F2 F1 F0
        )
        
        self._instruction_10011101_tbl = (
            KS56CX2Xdasm._set1_hmembit,                   #10011101 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._set1_pmeml,                     #10011101 | 0100 G3 G2 G1 G0
            #KS56CX2Xdasm._ei,                            #10011101 | 10110010
            #KS56CX2Xdasm._ei_iexxx,                      #10011101 | 10 N5 1 1 N2 N1 N0
            #KS56CX2Xdasm._halt,                          #10011101 | 10100011
            #KS56CX2Xdasm._stop                           #10011101 | 10110011
            KS56CX2Xdasm._set1_fmembit,                   #10011101 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._set1_fmembit                    #10011101 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10011111_tbl = (
            KS56CX2Xdasm._sktclr_hmembit,                 #10011111 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._sktclr_pmeml,                   #10011111 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._sktclr_fmembit,                 #10011111 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._sktclr_fmembit                  #10011111 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10101010_tbl = (
            *([KS56CX2Xdasm._dummy] * 16),
            KS56CX2Xdasm._mov_ahl_xa,                     #10101010 | 00010000
            KS56CX2Xdasm._xch_xa_ahl,                     #10101010 | 00010001
            *([KS56CX2Xdasm._dummy] * 6),
            KS56CX2Xdasm._mov_xa_ahl,                     #10101010 | 00011000
            KS56CX2Xdasm._ske_xa_ahl,                     #10101010 | 00011001
            *([KS56CX2Xdasm._dummy] * 38),
            *([KS56CX2Xdasm._xch_xa_rpe] * 8),            #10101010 | 01000 P2 P1 P0
            *([KS56CX2Xdasm._ske_xa_rpe] * 8),            #10101010 | 01001 P2 P1 P0
            *([KS56CX2Xdasm._mov_rpe1_xa] * 8),           #10101010 | 01010 P2 P1 P0
            *([KS56CX2Xdasm._mov_xa_rpe] * 8),            #10101010 | 01011 P2 P1 P0
            *([KS56CX2Xdasm._dummy] * 8),
            *([KS56CX2Xdasm._decs_rpe] * 8),              #10101010 | 01101 P2 P1 P0
            *([KS56CX2Xdasm._dummy] * 32),
            *([KS56CX2Xdasm._and_rpe1_xa] * 8),           #10101010 | 10010 P2 P1 P0
            *([KS56CX2Xdasm._and_xa_rpe] * 8),            #10101010 | 10011 P2 P1 P0
            *([KS56CX2Xdasm._or_rpe1_xa] * 8),            #10101010 | 10100 P2 P1 P0
            *([KS56CX2Xdasm._or_xa_rpe] * 8),             #10101010 | 10101 P2 P1 P0
            *([KS56CX2Xdasm._xor_rpe1_xa] * 8),           #10101010 | 10110 P2 P1 P0
            *([KS56CX2Xdasm._xor_xa_rpe] * 8),            #10101010 | 10111 P2 P1 P0
            *([KS56CX2Xdasm._adds_rpe1_xa] * 8),          #10101010 | 11000 P2 P1 P0
            *([KS56CX2Xdasm._adds_xa_rpe] * 8),           #10101010 | 11001 P2 P1 P0
            *([KS56CX2Xdasm._addc_rpe1_xa] * 8),          #10101010 | 11010 P2 P1 P0
            *([KS56CX2Xdasm._addc_xa_rpe] * 8),           #10101010 | 11011 P2 P1 P0
            *([KS56CX2Xdasm._subs_rpe1_xa] * 8),          #10101010 | 11100 P2 P1 P0
            *([KS56CX2Xdasm._subs_xa_rpe] * 8),           #10101010 | 11101 P2 P1 P0
            *([KS56CX2Xdasm._subc_rpe1_xa] * 8),          #10101010 | 11110 P2 P1 P0
            *([KS56CX2Xdasm._subc_xa_rpe] * 8),           #10101010 | 11111 P2 P1 P0
        )

        self._instruction_10101100_tbl = (
            KS56CX2Xdasm._and1_cy_hmembit,                #10101100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._and1_cy_pmeml,                  #10101100 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._and1_cy_fmembit,                #10101100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._and1_cy_fmembit                 #10101100 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10101110_tbl = (
            KS56CX2Xdasm._or1_cy_hmembit,                 #10101110 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._or1_cy_pmeml,                   #10101110 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._or1_cy_fmembit,                 #10101110 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._or1_cy_fmembit                  #10101110 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10111100_tbl = (
            KS56CX2Xdasm._xor1_cy_hmembit,                #10111100 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._xor1_cy_pmeml,                  #10111100 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._xor1_cy_fmembit,                #10111100 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._xor1_cy_fmembit                 #10111100 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10111101_tbl = (
            KS56CX2Xdasm._mov1_cy_hmembit,                #10111101 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._mov1_cy_pmeml,                  #10111101 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._mov1_cy_fmembit,                #10111101 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._mov1_cy_fmembit                 #10111101 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10111110_tbl = (
            KS56CX2Xdasm._skf_hmembit,                    #10111110 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._skf_pmeml,                      #10111110 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._skf_fmembit,                    #10111110 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._skf_fmembit                     #10111110 | 11 B1 B0 F3 F2 F1 F0
        )

        self._instruction_10111111_tbl = (
            KS56CX2Xdasm._skt_hmembit,                    #10111111 | 00 B1 B0 D3 D2 D1 D0
            KS56CX2Xdasm._skt_pmeml,                      #10111111 | 0100 G3 G2 G1 G0
            KS56CX2Xdasm._skt_fmembit,                    #10111111 | 10 B1 B0 F3 F2 F1 F0
            KS56CX2Xdasm._skt_fmembit                     #10111111 | 11 B1 B0 F3 F2 F1 F0
        )

    def disassemble(self, rom):
        if (rom.size() > 0):
            listing = [None] * rom.size()
            vector = rom.getWord(0) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(2) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(4) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(6) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(8) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)
            vector = rom.getWord(10) & 0x3FFF
            listing = self._disassemble(vector, listing, rom)

            for i in range(len(listing)):
                if (listing[i] is None):
                    byte = rom.getByte(i)
                    listing[i] = (1, byte, 'db ' + self._bytebase % byte)
                listing[i] = (self._opbase % listing[i][1], listing[i][2])
            
            return {"LISTING": tuple(listing)}
        else:
            return {}
    
    def disassemble2text(self, rom, file_path):
        listing = self.disassemble(rom)["LISTING"]
        result = ""
        for i, line in enumerate(listing):
            if (line[1]):
                result += (self._addrbase % i) + ":\t" + (line[1] + "\t;" + line[0]).expandtabs(30) + "\n"
        with open(file_path, 'w') as f:
            f.write(result)
    
    def _disassemble(self, pc, listing, rom):
        while (pc < len(listing) and listing[pc] is None):
            opcode = rom.getByte(pc)
            next_pcs, listing[pc] = self._instruction_tbl[opcode](self, pc, opcode, rom)
            instruction_size = listing[pc][0]
            while (instruction_size > 1  and (pc + 1) < len(listing)):
                instruction_size -= 1
                pc += 1
                listing[pc] = (1, rom.getByte(pc), '')
            pc = next_pcs[0]
            if (len(next_pcs) > 1):
                listing = self._disassemble(next_pcs[1], listing, rom)
        return listing

    def _instruction_10101011(self, pc, opcode, rom):
        #10101011
        op = rom.getByte(pc + 1)
        return self._instruction_10101011_tbl[(op >> 6) & 0x1](self, pc, opcode, rom)

    def _instruction_10011001(self, pc, opcode, rom):
        #10011001
        op = rom.getByte(pc + 1)
        return self._instruction_10011001_tbl[op & 0x7F](self, pc, opcode, rom)
        
    def _instruction_10011010(self, pc, opcode, rom):
        #10011010
        op = rom.getByte(pc + 1)
        return self._instruction_10011010_tbl[(op >> 3) & 0x1](self, pc, opcode, rom)

    def _instruction_10011011(self, pc, opcode, rom):
        #10011011
        op = rom.getByte(pc + 1)
        return self._instruction_10011011_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10011100(self, pc, opcode, rom):
        #10011100
        op = rom.getByte(pc + 1)
        return self._instruction_10011100_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10011101(self, pc, opcode, rom):
        #10011101
        op = rom.getByte(pc + 1)
        return self._instruction_10011101_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10011111(self, pc, opcode, rom):
        #10011111
        op = rom.getByte(pc + 1)
        return self._instruction_10011111_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10101010(self, pc, opcode, rom):
        #10101010
        op = rom.getByte(pc + 1)
        return self._instruction_10101010_tbl[op](self, pc, opcode, rom)

    def _instruction_10101100(self, pc, opcode, rom):
        #10101100
        op = rom.getByte(pc + 1)
        return self._instruction_10101100_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10101110(self, pc, opcode, rom):
        #10101110
        op = rom.getByte(pc + 1)
        return self._instruction_10101110_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)
    
    def _instruction_10111100(self, pc, opcode, rom):
        #10111100
        op = rom.getByte(pc + 1)
        return self._instruction_10111100_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10111101(self, pc, opcode, rom):
        #10111101
        op = rom.getByte(pc + 1)
        return self._instruction_10111101_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10111110(self, pc, opcode, rom):
        #10111110
        op = rom.getByte(pc + 1)
        return self._instruction_10111110_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _instruction_10111111(self, pc, opcode, rom):
        #10111111
        op = rom.getByte(pc + 1)
        return self._instruction_10111111_tbl[(op >> 6) & 0x3](self, pc, opcode, rom)

    def _br_raddr(self, pc, opcode, rom):
        #0000 A3 A2 A1 A0
        a = pc + opcode + 1
        return (pc + 1, a), (1, opcode, "br " + self._addrbase % a)

    def _br_mraddr(self, pc, opcode, rom):
        #1111 A3 A2 A1 A0
        a = pc - (15 - (opcode & 0x0F))
        return (pc + 1, a), (1, opcode, "br " + self._addrbase % a)

    def _geti_taddr(self, pc, opcode, rom):
        #00 T5 T4 T3 T2 T1 T0
        a = opcode << 1
        return (pc + 1, a), (1, opcode, "geti " + self._addrbase % a)

    def _callf_faddr(self, pc, opcode, rom):
        #01000 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        op = rom.getByte(pc + 1)
        a = ((opcode & 0x7) << 8) | op
        return (pc + 2, a), (2, (opcode << 8) | op, "callf " + self._addrbase % a)

    def _pop_xa(self, pc, opcode, rom):
        #01001000
        return (pc + 1,), (1, opcode, "pop XA")

    def _push_xa(self, pc, opcode, rom):
        #01001001
        return (pc + 1,), (1, opcode, "push XA")

    def _pop_hl(self, pc, opcode, rom):
        #01001010
        return (pc + 1,), (1, opcode, "pop HL")

    def _push_hl(self, pc, opcode, rom):
        #01001011
        return (pc + 1,), (1, opcode, "push HL")

    def _pop_de(self, pc, opcode, rom):
        #01001100
        return (pc + 1,), (1, opcode, "pop DE")

    def _push_de(self, pc, opcode, rom):
        #01001101
        return (pc + 1,), (1, opcode, "push DE")

    def _pop_bc(self, pc, opcode, rom):
        #01001110
        return (pc + 1,), (1, opcode, "pop BC")

    def _push_bc(self, pc, opcode, rom):
        #01001111
        return (pc + 1,), (1, opcode, "push BC")

    def _brcb_caddr(self, pc, opcode, rom):
        #0101 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        op = rom.getByte(pc + 1)
        a = (pc & 0xF000) | ((opcode & 0xF) << 8) | op
        return (pc + 2, a), (2, (opcode << 8) | op, "brcb " + self._addrbase % a)

    def _adds_a_n4(self, pc, opcode, rom):
        #0110 I3 I2 I1 I0
        i = opcode & 0xF
        return (pc + 1,), (1, opcode, ("adds A, " + self._nibbase % i) if i else "nop")

    def _mov_a_n4(self, pc, opcode, rom):
        #0111 I3 I2 I1 I0
        i = opcode & 0xF
        return (pc + 1,), (1, opcode, "mov A, " + self._nibbase % i)

    def _ske_a_ahl(self, pc, opcode, rom):
        #10000000
        return (pc + 1,), (1, opcode, "ske A, @HL")

    def _incs_mem(self, pc, opcode, rom):
        #10000010 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "incs RAM[" + self._nibbase % op + "]")

    def _clr1_mem0(self, pc, opcode, rom):
        #10000100 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._nibbase % op + "].0")

    def _set1_mem0(self, pc, opcode, rom):
        #10000101 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._nibbase % op + "].0")

    def _skf_mem0(self, pc, opcode, rom):
        #10000110 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._nibbase % op + "].0")

    def _skt_mem0(self, pc, opcode, rom):
        #10000111 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._nibbase % op + "].0")

    def _mov_xa_n8(self, pc, opcode, rom):
        #10001001 | I7 I6 I5 I4 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov XA, " + self._bytebase % op)

    def _incs_hl(self, pc, opcode, rom):
        #10001010
        return (pc + 1,), (1, opcode, "incs HL")

    def _mov_hl_n8(self, pc, opcode, rom):
        #10001011 | I7 I6 I5 I4 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov HL, " + self._bytebase % op)
        
    def _incs_de(self, pc, opcode, rom):
        #10001100
        return (pc + 1,), (1, opcode, "incs DE")

    def _mov_de_n8(self, pc, opcode, rom):
        #10001101 | I7 I6 I5 I4 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov DE, " + self._bytebase % op)

    def _incs_bc(self, pc, opcode, rom):
        #10001110
        return (pc + 1,), (1, opcode, "incs BC")

    def _mov_bc_n8(self, pc, opcode, rom):
        #10001111 | I7 I6 I5 I4 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov BC, " + self._bytebase % op)

    def _and_a_ahl(self, pc, opcode, rom):
        #10010000
        return (pc + 1,), (1, opcode, "and A, @HL")

    def _mov_mem_xa(self, pc, opcode, rom):
        #10010010 | D7 D6 D5 D4 D3 D2 D1 0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov RAM[" + self._bytebase % op + "], XA")

    def _mov_mem_a(self, pc, opcode, rom):
        #10010011 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov RAM[" + self._bytebase % op + "], A")

    def _clr1_mem1(self, pc, opcode, rom):
        #10010100 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._bytebase % op + "].1")

    def _set1_mem1(self, pc, opcode, rom):
        #10010101 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._bytebase % op + "].1")

    def _skf_mem1(self, pc, opcode, rom):
        #10010110 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._bytebase % op + "].1")

    def _skt_mem1(self, pc, opcode, rom):
        #10010111 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._bytebase % op + "].1")

    def _rorc_a(self, pc, opcode, rom):
        #10011000
        return (pc + 1,), (1, opcode, "rorc A")

    def _or_a_ahl(self, pc, opcode, rom):
        #10100000
        return (pc + 1,), (1, opcode, "or A, @HL")

    def _mov_xa_mem(self, pc, opcode, rom):
        #10100010 | D7 D6 D5 D4 D3 D2 D1 0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov XA, RAM[" + self._bytebase % op + "]")

    def _mov_a_mem(self, pc, opcode, rom):
        #10100011 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "mov A, RAM[" + self._bytebase % op + "]")

    def _clr1_mem2(self, pc, opcode, rom):
        #10100100 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._bytebase % op + "].2")

    def _set1_mem2(self, pc, opcode, rom):
        #10100101 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._bytebase % op + "].2")

    def _skf_mem2(self, pc, opcode, rom):
        #10100110 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._bytebase % op + "].2")

    def _skt_mem2(self, pc, opcode, rom):
        #10100111 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._bytebase % op + "].2")

    def _subs_a_ahl(self, pc, opcode, rom):
        #10101000
        return (pc + 1,), (1, opcode, "subs A, @HL")

    def _addc_a_ahl(self, pc, opcode, rom):
        #10101001
        return (pc + 1,), (1, opcode, "addc A, @HL")

    def _br_addr(self, pc, opcode, rom):
        #10101011 | 00 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        a = rom.getWord(pc + 1)
        return (pc + 3, a), (3, (opcode << 16) | a, "br " + self._addrbase % a)

    def _call_addr(self, pc, opcode, rom):
        #10101011 | 01 A13 A12 A11 A10 A9 A8 | A7 A6 A5 A4 A3 A2 A1 A0
        a = rom.getWord(pc + 1) & 0x3FFF
        return (pc + 3, a), (3, (opcode << 16) | a, "call " + self._addrbase % a)

    def _xor_a_ahl(self, pc, opcode, rom):
        #10110000
        return (pc + 1,), (1, opcode, "xor A, @HL")

    def _xch_xa_mem(self, pc, opcode, rom):
        #10110010 | D7 D6 D5 D4 D3 D2 D1 0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "xch XA, RAM[" + self._bytebase % op + "]")

    def _xch_a_mem(self, pc, opcode, rom):
        #10110011 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "xch A, RAM[" + self._bytebase % op + "]")

    def _clr1_mem3(self, pc, opcode, rom):
        #10110100 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._bytebase % op + "].3")

    def _set1_mem3(self, pc, opcode, rom):
        #10110101 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._bytebase % op + "].3")

    def _skf_mem3(self, pc, opcode, rom):
        #10110110 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._bytebase % op + "].3")

    def _skt_mem3(self, pc, opcode, rom):
        #10110111 | D7 D6 D5 D4 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._bytebase % op + "].3")

    def _subc_a_ahl(self, pc, opcode, rom):
        #10111000
        return (pc + 1,), (1, opcode, "subc A, @HL")

    def _adds_xa_n8(self, pc, opcode, rom):
        #10111001 | I7 I6 I5 I4 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        return (pc + 2,), (2, (opcode << 8) | op, "adds XA, " + self._bytebase % op)

    def _incs_reg(self, pc, opcode, rom):
        #11000 R2 R1 R0
        r = opcode & 0x7
        return (pc + 1,), (1, opcode, "incs " + self._reg_tbl[r])

    def _decs_reg(self, pc, opcode, rom):
        #11001 R2 R1 R0
        r = opcode & 0x7
        return (pc + 1,), (1, opcode, "decs " + self._reg_tbl[r])

    def _movt_xa_pcxa(self, pc, opcode, rom):
        #11010000
        return (pc + 1,), (1, opcode, "movt XA, @PCXA")

    def _movt_xa_bcxa(self, pc, opcode, rom):
        #11010001
        return (pc + 1,), (1, opcode, "movt XA, @BCXA")

    def _adds_a_ahl(self, pc, opcode, rom):
        #11010010
        return (pc + 1,), (1, opcode, "adds A, @HL")

    def _movt_xa_pcde(self, pc, opcode, rom):
        #11010100
        return (pc + 1,), (1, opcode, "movt XA, @PCDE")

    def _movt_xa_bcde(self, pc, opcode, rom):
        #11010101
        return (pc + 1,), (1, opcode, "movt XA, @BCDE")

    def _not1_cy(self, pc, opcode, rom):
        #11010110
        return (pc + 1,), (1, opcode, "not1 CY")

    def _skt_cy(self, pc, opcode, rom):
        #11010111
        return (pc + 1,), (1, opcode, "skt CY")

    def _xch_a_reg1(self, pc, opcode, rom):
        #11011 R2 R1 R0
        r = opcode & 0x7
        return (pc + 1,), (1, opcode, "xch A, " + self._reg_tbl[r])

    def _rets(self, pc, opcode, rom):
        #11100000
        return (pc + 1,), (1, opcode, "rets")

    def _mov_a_ahl(self, pc, opcode, rom):
        #11100001
        return (pc + 1,), (1, opcode, "mov A, @HL")

    def _mov_a_ahli(self, pc, opcode, rom):
        #11100010
        return (pc + 1,), (1, opcode, "mov A, @HL+")

    def _mov_a_ahld(self, pc, opcode, rom):
        #11100011
        return (pc + 1,), (1, opcode, "mov A, @HL-")

    def _mov_a_ade(self, pc, opcode, rom):
        #11100100
        return (pc + 1,), (1, opcode, "mov A, @DE")

    def _mov_a_adl(self, pc, opcode, rom):
        #11100101
        return (pc + 1,), (1, opcode, "mov A, @DL")

    def _clr1_cy(self, pc, opcode, rom):
        #11100110
        return (pc + 1,), (1, opcode, "clr1 CY")

    def _set1_cy(self, pc, opcode, rom):
        #11100111
        return (pc + 1,), (1, opcode, "set1 CY")

    def _mov_ahl_a(self, pc, opcode, rom):
        #11101000
        return (pc + 1,), (1, opcode, "mov @HL, A")

    def _xch_a_ahl(self, pc, opcode, rom):
        #11101001
        return (pc + 1,), (1, opcode, "xch A, @HL")

    def _xch_a_ahli(self, pc, opcode, rom):
        #11101010
        return (pc + 1,), (1, opcode, "xch A, @HL+")

    def _xch_a_ahld(self, pc, opcode, rom):
        #11101011
        return (pc + 1,), (1, opcode, "xch A, @HL-")

    def _xch_a_ade(self, pc, opcode, rom):
        #11101100
        return (pc + 1,), (1, opcode, "xch A, DE")

    def _xch_a_adl(self, pc, opcode, rom):
        #11101101
        return (pc + 1,), (1, opcode, "xch A, DL")

    def _ret(self, pc, opcode, rom):
        #11101110
        return (pc + 1,), (1, opcode, "ret")

    def _reti(self, pc, opcode, rom):
        #11101111
        return (pc + 1,), (1, opcode, "reti")

    def _br_pcxa(self, pc, opcode, rom):
        #10011001 | 00000000
        return (pc + 2,), (2, (opcode << 8) | 0, "br PCXA")

    def _br_bcxa(self, pc, opcode, rom):
        #10011001 | 00000001
        return (pc + 2,), (2, (opcode << 8) | 0b00000001, "br BCXA")

    def _incs_ahl(self, pc, opcode, rom):
        #10011001 | 00000010
        return (pc + 2,), (2, (opcode << 8) | 0b00000010, "incs @HL")

    def _br_pcde(self, pc, opcode, rom):
        #10011001 | 00000100
        return (pc + 2,), (2, (opcode << 8) | 0b00000100, "br PCDE")

    def _br_bcde(self, pc, opcode, rom):
        #10011001 | 00000101
        return (pc + 2,), (2, (opcode << 8) | 0b00000101, "br BCDE")

    def _pop_bs(self, pc, opcode, rom):
        #10011001 | 00000110
        return (pc + 2,), (2, (opcode << 8) | 0b00000110, "pop bs")

    def _push_bs(self, pc, opcode, rom):
        #10011001 | 00000111
        return (pc + 2,), (2, (opcode << 8) | 0b00000111, "push bs")

    def _ske_a_reg(self, pc, opcode, rom):
        #10011001 | 00001 R2 R1 R0
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "ske A, " + self._reg_tbl[r])

    def _sel_mbn(self, pc, opcode, rom):
        #10011001 | 0001 N3 N2 N1 N0
        op = rom.getByte(pc + 1)
        n = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "sel MB" + str(n))

    def _sel_rbn(self, pc, opcode, rom):
        #10011001 | 001000 N1 N0
        op = rom.getByte(pc + 1)
        n = op & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "sel RB" + str(n))

    def _and_a_n4(self, pc, opcode, rom):
        #10011001 | 0011 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "and A, " + self._nibbase % i)

    def _or_a_n4(self, pc, opcode, rom):
        #10011001 | 0100 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "or A, " + self._nibbase % i)

    def _xor_a_n4(self, pc, opcode, rom):
        #10011001 | 0101 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "xor A, " + self._nibbase % i)

    def _ske_ahl_n4(self, pc, opcode, rom):
        #10011001 | 0110 I3 I2 I1 I0
        op = rom.getByte(pc + 1)
        i = op & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "ske @HL, " + self._nibbase % i)

    def _mov_reg1_a(self, pc, opcode, rom):
        #10011001 | 01110 R2 R1 R0
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "mov " + self._reg_tbl[r] + ", A")

    def _mov_a_reg(self, pc, opcode, rom):
        #10011001 | 01111 R2 R1 R0
        op = rom.getByte(pc + 1)
        r = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "mov A, " + self._reg_tbl[r])

    def _ske_reg_n4(self, pc, opcode, rom):
        #10011010 | I3 I2 I1 I0 0 R2 R1 R0
        op = rom.getByte(pc + 1)
        r = op & 0x7
        i = (op >> 4) & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "ske " + self._reg_tbl[r] + ", " + self._nibbase % i)

    def _mov_reg1_n4(self, pc, opcode, rom):
        #10011010 | I3 I2 I1 I0 1 R2 R1 R0
        op = rom.getByte(pc + 1)
        r = op & 0x7
        i = (op >> 4) & 0xF
        return (pc + 2,), (2, (opcode << 8) | op, "mov " + self._reg_tbl[r] + ", " + self._nibbase % i)

    def _mov1_hmembit_cy(self, pc, opcode, rom):
        #10011011 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "mov1 RAM[@H + " + self._nibbase % d + "]." + str(b) + ", CY")

    def _mov1_pmeml_cy(self, pc, opcode, rom):
        #10011011 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "mov1 RAM[" + self._rambase % pmem + " + @L3-2].@L1-0, CY")

    def _mov1_fmembit_cy(self, pc, opcode, rom):
        #10011011 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "mov1 " + self._io_tbl[fmem] + "." + str(b) + ", CY")
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "mov1 RAM[" + self._rambase % fmem + "]." + str(b) + ", CY")

    def _clr1_hmembit(self, pc, opcode, rom):
        #10011100 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _clr1_pmeml(self, pc, opcode, rom):
        #10011100 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _clr1_fmembit(self, pc, opcode, rom):
        #10011100 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (op in self._clr_fmem_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, self._clr_fmem_tbl[op])
        elif (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "clr1 " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "clr1 RAM[" + self._rambase % fmem + "]." + str(b))

    def _set1_hmembit(self, pc, opcode, rom):
        #10011101 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _set1_pmeml(self, pc, opcode, rom):
        #10011101 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _set1_fmembit(self, pc, opcode, rom):
        #10011101 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (op in self._set_fmem_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, self._set_fmem_tbl[op])
        elif (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "set1 " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "set1 RAM[" + self._rambase % fmem + "]." + str(b))

    def _sktclr_hmembit(self, pc, opcode, rom):
        #10011111 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "sktclr RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _sktclr_pmeml(self, pc, opcode, rom):
        #10011111 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "sktclr RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _sktclr_fmembit(self, pc, opcode, rom):
        #10011111 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "sktclr " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "sktclr RAM[" + self._rambase % fmem + "]." + str(b))

    def _mov_ahl_xa(self, pc, opcode, rom):
        #10101010 | 00010000
        return (pc + 2,), (2, (opcode << 8) | 0b00010000, "mov @HL, XA")

    def _xch_xa_ahl(self, pc, opcode, rom):
        #10101010 | 00010001
        return (pc + 2,), (2, (opcode << 8) | 0b00010001, "xch XA, @HL")

    def _mov_xa_ahl(self, pc, opcode, rom):
        #10101010 | 00011000
        return (pc + 2,), (2, (opcode << 8) | 0b00011000, "mov XA, @HL")

    def _ske_xa_ahl(self, pc, opcode, rom):
        #10101010 | 00011001
        return (pc + 2,), (2, (opcode << 8) | 0b00011001, "ske XA, @HL")

    def _xch_xa_rpe(self, pc, opcode, rom):
        #10101010 | 01000 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "xch XA, " + self._rpe_tbl[p])

    def _ske_xa_rpe(self, pc, opcode, rom):
        #10101010 | 01001 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "ske XA, " + self._rpe_tbl[p])

    def _mov_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 01010 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "mov " + self._rpe_tbl[p] + ", XA")

    def _mov_xa_rpe(self, pc, opcode, rom):
        #10101010 | 01011 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "mov XA, " + self._rpe_tbl[p])

    def _decs_rpe(self, pc, opcode, rom):
        #10101010 | 01101 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "decs " + self._rpe_tbl[p])

    def _and_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 10010 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "and " + self._rpe_tbl[p] + ", XA")

    def _and_xa_rpe(self, pc, opcode, rom):
        #10101010 | 10011 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "and XA, " + self._rpe_tbl[p])

    def _or_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 10100 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "or " + self._rpe_tbl[p] + ", XA")

    def _or_xa_rpe(self, pc, opcode, rom):
        #10101010 | 10101 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "or XA, " + self._rpe_tbl[p])

    def _xor_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 10110 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "xor " + self._rpe_tbl[p] + ", XA")

    def _xor_xa_rpe(self, pc, opcode, rom):
        #10101010 | 10111 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "xor XA, " + self._rpe_tbl[p])

    def _adds_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 11000 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "adds " + self._rpe_tbl[p] + ", XA")

    def _adds_xa_rpe(self, pc, opcode, rom):
        #10101010 | 11001 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "adds XA, " + self._rpe_tbl[p])

    def _addc_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 11010 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "addc " + self._rpe_tbl[p] + ", XA")

    def _addc_xa_rpe(self, pc, opcode, rom):
        #10101010 | 11011 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "addc XA, " + self._rpe_tbl[p])

    def _subs_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 11100 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "subs " + self._rpe_tbl[p] + ", XA")

    def _subs_xa_rpe(self, pc, opcode, rom):
        #10101010 | 11101 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "subs XA, " + self._rpe_tbl[p])

    def _subc_rpe1_xa(self, pc, opcode, rom):
        #10101010 | 11110 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "subc " + self._rpe_tbl[p] + ", XA")

    def _subc_xa_rpe(self, pc, opcode, rom):
        #10101010 | 11111 P2 P1 P0
        op = rom.getByte(pc + 1)
        p = op & 0x7
        return (pc + 2,), (2, (opcode << 8) | op, "subc XA, " + self._rpe_tbl[p])

    def _and1_cy_hmembit(self, pc, opcode, rom):
        #10101100 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "and1 CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _and1_cy_pmeml(self, pc, opcode, rom):
        #10101100 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "and1 CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _and1_cy_fmembit(self, pc, opcode, rom):
        #10101100 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "and1 CY, " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "and1 CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _or1_cy_hmembit(self, pc, opcode, rom):
        #10101110 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "or1 CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _or1_cy_pmeml(self, pc, opcode, rom):
        #10101110 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "or1 CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _or1_cy_fmembit(self, pc, opcode, rom):
        #10101110 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "or1 CY, " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "or1 CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _xor1_cy_hmembit(self, pc, opcode, rom):
        #10111100 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "xor1 CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _xor1_cy_pmeml(self, pc, opcode, rom):
        #10111100 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "xor1 CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _xor1_cy_fmembit(self, pc, opcode, rom):
        #10111100 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "xor1 CY, " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "xor1 CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _mov1_cy_hmembit(self, pc, opcode, rom):
        #10111101 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "mov1 CY, RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _mov1_cy_pmeml(self, pc, opcode, rom):
        #10111101 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "mov1 CY, RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _mov1_cy_fmembit(self, pc, opcode, rom):
        #10111101 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "mov1 CY, " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "mov1 CY, RAM[" + self._rambase % fmem + "]." + str(b))

    def _skf_hmembit(self, pc, opcode, rom):
        #10111110 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _skf_pmeml(self, pc, opcode, rom):
        #10111110 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _skf_fmembit(self, pc, opcode, rom):
        #10111110 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "skf " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "skf RAM[" + self._rambase % fmem + "]." + str(b))

    def _skt_hmembit(self, pc, opcode, rom):
        #10111111 | 00 B1 B0 D3 D2 D1 D0
        op = rom.getByte(pc + 1)
        d = op & 0xF
        b = (op >> 4) & 0x3
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[@H + " + self._nibbase % d + "]." + str(b))

    def _skt_pmeml(self, pc, opcode, rom):
        #10111111 | 0100 G3 G2 G1 G0
        op = rom.getByte(pc + 1)
        g = op & 0xF
        pmem =  0xFC0 + (g << 2)
        return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._rambase % pmem + " + @L3-2].@L1-0")

    def _skt_fmembit(self, pc, opcode, rom):
        #10111111 | 1 X B1 B0 F3 F2 F1 F0
        op = rom.getByte(pc + 1)
        b = (op >> 4) & 0x3
        fmem = 0xFB0 | (op & 0b01001111)
        if (fmem in self._io_tbl):
            return (pc + 2,), (2, (opcode << 8) | op, "skt " + self._io_tbl[fmem] + "." + str(b))
        else:
            return (pc + 2,), (2, (opcode << 8) | op, "skt RAM[" + self._rambase % fmem + "]." + str(b))

    def _dummy(self, pc, opcode, rom):
        return (pc + 1,), (1, opcode, "db " + self._bytebase % opcode)
