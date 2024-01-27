001:	mov R1R0, 0xFF                ;5F0F
003:	call 617                      ;F617
005:	in A, PP                      ;34
006:	ja1 00A                       ;880A
008:	jmp 005                       ;E005
00A:	mov R1R0, 0xFF                ;5F0F
00C:	call 614                      ;F614
00E:	mov R1R0, 0x47                ;5704
010:	mov A, 0x1                    ;71
011:	mov [R1R0], A                 ;05
012:	call D23                      ;FD23
014:	mov R1R0, 0x8C                ;5C08
016:	mov A, [R1R0]                 ;04
017:	jnz A, 01E                    ;B81E
019:	inc R0                        ;10
01A:	jnz R0, 016                   ;A016
01C:	call D1B                      ;FD1B
01E:	call D6A                      ;FD6A
020:	mov R1R0, 0xC1                ;510C
022:	mov A, 0x8                    ;78
023:	or [R1R0], A                  ;1F
024:	mov R1R0, 0xB5                ;550B
026:	mov A, 0x8                    ;78
027:	or [R1R0], A                  ;1F
028:	call ADB                      ;FADB
02A:	call 529                      ;F529
02C:	call 621                      ;F621
02E:	call D6A                      ;FD6A
030:	mov R3R2, 0x85                ;6508
032:	mov R1R0, 0x47                ;5704
034:	mov A, 0xD                    ;7D
035:	readf R4A                     ;4D
036:	mov [R3R2], A                 ;07
037:	mov R1R0, 0x47                ;5704
039:	mov A, [R1R0]                 ;04
03A:	sub A, 0x5                    ;4105
03C:	jnc 0C0                       ;C8C0
03E:	jz A, 0BC                     ;B0BC
040:	mov A, [R1R0]                 ;04
041:	xor A, 0x6                    ;4306
043:	jz A, 045                     ;B045
045:	call 621                      ;F621
047:	mov A, TMRL                   ;3A
048:	mov R1R0, 0x67                ;5706
04A:	mov R4, A                     ;28
04B:	xor A, [R1R0]                 ;1B
04C:	inc [R1R0]                    ;0C
04D:	jz A, 051                     ;B051
04F:	mov A, R4                     ;29
050:	mov [R1R0], A                 ;05
051:	clc                           ;2A
052:	daa                           ;36
053:	mov R1R0, 0x1B                ;5B01
055:	mov [R1R0], A                 ;05
056:	mov R1R0, 0x82                ;5208
058:	inc A                         ;31
059:	mov [R1R0], A                 ;05
05A:	mov A, TMRL                   ;3A
05B:	clc                           ;2A
05C:	daa                           ;36
05D:	inc A                         ;31
05E:	mov R1R0, 0x86                ;5608
060:	mov [R1R0], A                 ;05
061:	mov R1R0, 0x1C                ;5C01
063:	mov A, 0xB                    ;7B
064:	mov [R1R0], A                 ;05
065:	call 9E5                      ;F9E5
067:	call 9D7                      ;F9D7
069:	mov R1R0, 0x39                ;5903
06B:	mov A, TMRL                   ;3A
06C:	and A, 0x3                    ;4203
06E:	mov [R1R0], A                 ;05
06F:	xor A, 0x3                    ;4303
071:	jnz A, 074                    ;B874
073:	dec [R1R0]                    ;0D
074:	mov A, [R1R0]                 ;04
075:	ja0 07A                       ;807A
077:	mov A, 0xB                    ;7B
078:	jmp 07B                       ;E07B
07A:	mov A, 0xA                    ;7A
07B:	mov R1R0, 0x3B                ;5B03
07D:	mov [R1R0], A                 ;05
07E:	dec R0                        ;11
07F:	mov A, TMRL                   ;3A
080:	mov [R1R0], A                 ;05
081:	mov R3R2, 0x3B                ;6B03
083:	mov R1R0, 0x44                ;5404
085:	mov A, [R3R2]                 ;06
086:	mov [R1R0], A                 ;05
087:	dec R2                        ;15
088:	dec R0                        ;11
089:	jnz R0, 085                   ;A085
08B:	mov R1R0, 0x70                ;5007
08D:	mov A, 0x0                    ;70
08E:	mov [R1R0], A                 ;05
08F:	mov R3R2, 0x3B                ;6B03
091:	mov R1R0, 0x44                ;5404
093:	mov A, [R1R0]                 ;04
094:	mov [R3R2], A                 ;07
095:	dec R2                        ;15
096:	dec R0                        ;11
097:	jnz R0, 093                   ;A093
099:	call 838                      ;F838
09B:	mov R1R0, 0x31                ;5103
09D:	mov A, 0x2                    ;72
09E:	mov [R1R0], A                 ;05
09F:	jmp F7A                       ;EF7A
0A1:	call B1C                      ;FB1C
0A3:	mov R1R0, 0x3A                ;5A03
0A5:	inc [R1R0]                    ;0C
0A6:	mov A, [R1R0]                 ;04
0A7:	jnz A, 0B2                    ;B8B2
0A9:	inc R0                        ;10
0AA:	inc [R1R0]                    ;0C
0AB:	mov A, [R1R0]                 ;04
0AC:	xor A, 0xC                    ;430C
0AE:	jnz A, 0B2                    ;B8B2
0B0:	dec [R1R0]                    ;0D
0B1:	dec [R1R0]                    ;0D
0B2:	mov R1R0, 0x31                ;5103
0B4:	inc [R1R0]                    ;0C
0B5:	mov A, [R1R0]                 ;04
0B6:	xor A, 0xA                    ;430A
0B8:	jnz A, 09F                    ;B89F
0BA:	jmp 107                       ;E107
0BC:	mov R1R0, 0x34                ;5403
0BE:	mov A, TMRL                   ;3A
0BF:	mov [R1R0], A                 ;05
0C0:	mov R1R0, 0x29                ;5902
0C2:	mov A, 0x0                    ;70
0C3:	mov [R1R0], A                 ;05
0C4:	mov R1R0, 0x28                ;5802
0C6:	mov A, TMRL                   ;3A
0C7:	mov [R1R0], A                 ;05
0C8:	mov R1R0, 0x2A                ;5A02
0CA:	mov [R1R0], A                 ;05
0CB:	mov R1R0, 0x82                ;5208
0CD:	mov A, 0x0                    ;70
0CE:	mov [R1R0], A                 ;05
0CF:	mov R1R0, 0x80                ;5008
0D1:	mov A, 0x5                    ;75
0D2:	mov [R1R0], A                 ;05
0D3:	mov R1R0, 0x10                ;5001
0D5:	mov R3R2, 0x47                ;6704
0D7:	mov A, [R3R2]                 ;06
0D8:	add A, 0x7                    ;4007
0DA:	mov [R1R0], A                 ;05
0DB:	mov A, 0xD                    ;7D
0DC:	readf R4A                     ;4D
0DD:	mov R1R0, 0x86                ;5608
0DF:	mov [R1R0], A                 ;05
0E0:	inc R0                        ;10
0E1:	mov A, R4                     ;29
0E2:	mov [R1R0], A                 ;05
0E3:	call 542                      ;F542
0E5:	mov R1R0, 0x47                ;5704
0E7:	mov A, [R1R0]                 ;04
0E8:	xor A, 0x5                    ;4305
0EA:	jnz A, 0F4                    ;B8F4
0EC:	mov R1R0, 0x36                ;5603
0EE:	mov A, [R1R0]                 ;04
0EF:	mov R1R0, 0x82                ;5208
0F1:	mov [R1R0], A                 ;05
0F2:	call 9E5                      ;F9E5
0F4:	call 9F3                      ;F9F3
0F6:	mov R1R0, 0x85                ;5508
0F8:	mov A, [R1R0]                 ;04
0F9:	dec R0                        ;11
0FA:	mov [R1R0], A                 ;05
0FB:	jz A, 107                     ;B107
0FD:	call 9D7                      ;F9D7
0FF:	mov R1R0, 0x84                ;5408
101:	dec [R1R0]                    ;0D
102:	mov A, [R1R0]                 ;04
103:	jz A, 107                     ;B107
105:	call 9CF                      ;F9CF
107:	mov R1R0, 0x5D                ;5D05
109:	mov A, [R1R0]                 ;04
10A:	jz A, 110                     ;B110
10C:	call D76                      ;FD76
10E:	call ADF                      ;FADF
110:	mov R1R0, 0x98                ;5809
112:	mov A, 0x8                    ;78
113:	add A, [R1R0]                 ;09
114:	jnc 11A                       ;C91A
116:	mov A, 0x0                    ;70
117:	mov [R1R0], A                 ;05
118:	jmp 3FB                       ;E3FB
11A:	call C97                      ;FC97
11C:	mov A, R3                     ;27
11D:	ja0 390                       ;8390
11F:	ja1 3B4                       ;8BB4
121:	ja2 3ED                       ;93ED
123:	mov A, R2                     ;25
124:	ja3 337                       ;9B37
126:	mov R1R0, 0x5D                ;5D05
128:	mov A, [R1R0]                 ;04
129:	jz A, 110                     ;B110
12B:	mov R1R0, 0x47                ;5704
12D:	mov A, [R1R0]                 ;04
12E:	sub A, 0x6                    ;4106
130:	jc 134                        ;C134
132:	jmp 772                       ;E772
134:	mov R1R0, 0x47                ;5704
136:	mov A, [R1R0]                 ;04
137:	sub A, 0x6                    ;4106
139:	jnc 167                       ;C967
13B:	mov R1R0, 0x1F                ;5F01
13D:	mov A, [R1R0]                 ;04
13E:	add A, 0x7                    ;4007
140:	jnc 143                       ;C943
142:	mov A, 0xF                    ;7F
143:	mov R1R0, 0x9A                ;5A09
145:	add A, [R1R0]                 ;09
146:	jnc 165                       ;C965
148:	mov A, 0x0                    ;70
149:	mov [R1R0], A                 ;05
14A:	mov R1R0, 0x31                ;5103
14C:	mov A, 0x9                    ;79
14D:	mov [R1R0], A                 ;05
14E:	call BAF                      ;FBAF
150:	mov R1R0, 0x67                ;5706
152:	mov A, [R1R0]                 ;04
153:	ja0 159                       ;8159
155:	call 75D                      ;F75D
157:	jmp 15B                       ;E15B
159:	call 748                      ;F748
15B:	call B1C                      ;FB1C
15D:	mov R1R0, 0x31                ;5103
15F:	dec [R1R0]                    ;0D
160:	mov A, [R1R0]                 ;04
161:	jnz A, 14E                    ;B94E
163:	jmp A67                       ;EA67
165:	jmp A46                       ;EA46
167:	mov R1R0, 0x60                ;5006
169:	mov A, [R1R0]                 ;04
16A:	jnz A, 185                    ;B985
16C:	mov R1R0, 0x71                ;5107
16E:	mov A, [R1R0]                 ;04
16F:	jnz A, 1A8                    ;B9A8
171:	mov A, 0xF                    ;7F
172:	mov R1R0, 0x68                ;5806
174:	add A, [R1R0]                 ;09
175:	jnc 1A8                       ;C9A8
177:	mov A, 0x0                    ;70
178:	mov [R1R0], A                 ;05
179:	mov R1R0, 0x54                ;5405
17B:	mov A, 0x0                    ;70
17C:	mov [R1R0], A                 ;05
17D:	mov R1R0, 0x71                ;5107
17F:	mov A, TMRL                   ;3A
180:	or A, 0x8                     ;4408
182:	mov [R1R0], A                 ;05
183:	jmp 859                       ;E859
185:	mov R1R0, 0x91                ;5109
187:	mov A, [R1R0]                 ;04
188:	add A, 0xC                    ;400C
18A:	jnc 1A8                       ;C9A8
18C:	mov A, 0x0                    ;70
18D:	mov [R1R0], A                 ;05
18E:	mov R1R0, 0x71                ;5107
190:	mov A, [R1R0]                 ;04
191:	jz A, 194                     ;B194
193:	inc [R1R0]                    ;0C
194:	mov R1R0, 0x51                ;5105
196:	mov A, [R1R0]                 ;04
197:	mov R1R0, 0x31                ;5103
199:	mov [R1R0], A                 ;05
19A:	call 586                      ;F586
19C:	mov R1R0, 0x51                ;5105
19E:	mov A, [R1R0]                 ;04
19F:	jz A, 3CC                     ;B3CC
1A1:	dec [R1R0]                    ;0D
1A2:	mov A, [R1R0]                 ;04
1A3:	mov R1R0, 0x31                ;5103
1A5:	mov [R1R0], A                 ;05
1A6:	call 58A                      ;F58A
1A8:	jmp E5E                       ;EE5E
1AA:	mov R1R0, 0x47                ;5704
1AC:	mov A, 0x5                    ;75
1AD:	xor A, [R1R0]                 ;1B
1AE:	jnz A, 1D0                    ;B9D0
1B0:	mov R1R0, 0x29                ;5902
1B2:	mov A, [R1R0]                 ;04
1B3:	jnz A, 1BF                    ;B9BF
1B5:	mov R1R0, 0x65                ;5506
1B7:	mov A, 0x8                    ;78
1B8:	add A, [R1R0]                 ;09
1B9:	jnc 1D0                       ;C9D0
1BB:	mov A, 0x0                    ;70
1BC:	mov [R1R0], A                 ;05
1BD:	jmp 933                       ;E933
1BF:	mov R1R0, 0x1F                ;5F01
1C1:	mov A, [R1R0]                 ;04
1C2:	add A, 0x1                    ;4001
1C4:	jnc 1C7                       ;C9C7
1C6:	mov A, 0xF                    ;7F
1C7:	mov R1R0, 0x32                ;5203
1C9:	add A, [R1R0]                 ;09
1CA:	jnc 1D0                       ;C9D0
1CC:	mov A, 0x0                    ;70
1CD:	mov [R1R0], A                 ;05
1CE:	jmp 967                       ;E967
1D0:	mov R1R0, 0x47                ;5704
1D2:	mov A, [R1R0]                 ;04
1D3:	xor A, 0x5                    ;4305
1D5:	jz A, 20F                     ;B20F
1D7:	mov R1R0, 0x82                ;5208
1D9:	mov A, [R1R0]                 ;04
1DA:	jnz A, 202                    ;BA02
1DC:	mov R1R0, 0x94                ;5409
1DE:	mov A, [R1R0]                 ;04
1DF:	add A, 0x6                    ;4006
1E1:	jnc 20F                       ;CA0F
1E3:	mov A, 0x0                    ;70
1E4:	mov [R1R0], A                 ;05
1E5:	mov R1R0, 0x4A                ;5A04
1E7:	mov A, [R1R0]                 ;04
1E8:	jz A, 1ED                     ;B1ED
1EA:	dec [R1R0]                    ;0D
1EB:	jmp 20F                       ;E20F
1ED:	mov A, TMRL                   ;3A
1EE:	mov R1R0, 0x2B                ;5B02
1F0:	mov [R1R0], A                 ;05
1F1:	ja0 1F6                       ;81F6
1F3:	mov A, 0x1                    ;71
1F4:	jmp 1F7                       ;E1F7
1F6:	mov A, 0xA                    ;7A
1F7:	mov R1R0, 0x82                ;5208
1F9:	mov [R1R0], A                 ;05
1FA:	call 9E5                      ;F9E5
1FC:	mov R1R0, 0x9B                ;5B09
1FE:	mov A, 0x0                    ;70
1FF:	mov [R1R0], A                 ;05
200:	jmp 20F                       ;E20F
202:	mov R1R0, 0x9B                ;5B09
204:	mov A, [R1R0]                 ;04
205:	add A, 0xC                    ;400C
207:	jnc 20F                       ;CA0F
209:	mov R1R0, 0x9B                ;5B09
20B:	mov A, 0x0                    ;70
20C:	mov [R1R0], A                 ;05
20D:	jmp 8F1                       ;E8F1
20F:	mov R1R0, 0x49                ;5904
211:	mov A, [R1R0]                 ;04
212:	jz A, 21A                     ;B21A
214:	mov R1R0, 0x6F                ;5F06
216:	mov A, 0xF                    ;7F
217:	mov [R1R0], A                 ;05
218:	jmp 46B                       ;E46B
21A:	mov R1R0, 0x6F                ;5F06
21C:	mov A, 0x0                    ;70
21D:	mov [R1R0], A                 ;05
21E:	mov R1R0, 0x1F                ;5F01
220:	mov A, [R1R0]                 ;04
221:	add A, 0x4                    ;4004
223:	jnc 226                       ;CA26
225:	mov A, 0xF                    ;7F
226:	mov R1R0, 0x95                ;5509
228:	add A, [R1R0]                 ;09
229:	jnc 2AC                       ;CAAC
22B:	mov A, 0x0                    ;70
22C:	mov [R1R0], A                 ;05
22D:	mov R1R0, 0x4B                ;5B04
22F:	mov A, [R1R0]                 ;04
230:	rl A                          ;01
231:	mov [R1R0], A                 ;05
232:	xor A, 0xF                    ;430F
234:	ja0 2AC                       ;82AC
236:	mov R1R0, 0x29                ;5902
238:	mov A, [R1R0]                 ;04
239:	jz A, 244                     ;B244
23B:	mov R1R0, 0x1C                ;5C01
23D:	mov A, [R1R0]                 ;04
23E:	sub A, 0x8                    ;4108
240:	jnc 244                       ;CA44
242:	call 834                      ;F834
244:	mov R1R0, 0x47                ;5704
246:	mov A, [R1R0]                 ;04
247:	sub A, 0x5                    ;4105
249:	jc 24E                        ;C24E
24B:	mov A, 0x9                    ;79
24C:	call B12                      ;FB12
24E:	mov R1R0, 0x28                ;5802
250:	mov A, [R1R0]                 ;04
251:	ja0 256                       ;8256
253:	mov A, 0x9                    ;79
254:	jmp 257                       ;E257
256:	mov A, 0x0                    ;70
257:	call DB3                      ;FDB3
259:	call AAC                      ;FAAC
25B:	mov R1R0, 0x0C                ;5C00
25D:	dec R0                        ;11
25E:	mov A, [R1R0]                 ;04
25F:	jnz A, 2D3                    ;BAD3
261:	jnz R0, 25D                   ;A25D
263:	mov R1R0, 0x37                ;5703
265:	mov A, [R1R0]                 ;04
266:	mov R1R0, 0x31                ;5103
268:	mov [R1R0], A                 ;05
269:	call BB6                      ;FBB6
26B:	mov R1R0, 0x28                ;5802
26D:	mov A, [R1R0]                 ;04
26E:	ja0 274                       ;8274
270:	call 748                      ;F748
272:	jmp 276                       ;E276
274:	call 75D                      ;F75D
276:	call B28                      ;FB28
278:	mov R1R0, 0x31                ;5103
27A:	dec [R1R0]                    ;0D
27B:	mov A, [R1R0]                 ;04
27C:	xor A, 0xF                    ;430F
27E:	jz A, 28A                     ;B28A
280:	mov R1R0, 0x37                ;5703
282:	mov A, [R1R0]                 ;04
283:	sub A, 0x4                    ;4104
285:	mov R1R0, 0x31                ;5103
287:	xor A, [R1R0]                 ;1B
288:	jnz A, 269                    ;BA69
28A:	mov R1R0, 0x29                ;5902
28C:	mov A, [R1R0]                 ;04
28D:	jz A, 298                     ;B298
28F:	mov R1R0, 0x1C                ;5C01
291:	mov A, [R1R0]                 ;04
292:	sub A, 0x8                    ;4108
294:	jnc 298                       ;CA98
296:	call 838                      ;F838
298:	mov R1R0, 0x47                ;5704
29A:	mov A, [R1R0]                 ;04
29B:	xor A, 0x5                    ;4305
29D:	jnz A, 2AC                    ;BAAC
29F:	mov R1R0, 0x28                ;5802
2A1:	mov A, [R1R0]                 ;04
2A2:	mov R1R0, 0x2B                ;5B02
2A4:	mov [R1R0], A                 ;05
2A5:	mov R1R0, 0x82                ;5208
2A7:	mov A, [R1R0]                 ;04
2A8:	jz A, 2AC                     ;B2AC
2AA:	jmp 8F1                       ;E8F1
2AC:	mov R1R0, 0x49                ;5904
2AE:	mov A, [R1R0]                 ;04
2AF:	jz A, 2CB                     ;B2CB
2B1:	mov R1R0, 0x48                ;5804
2B3:	mov A, 0xC                    ;7C
2B4:	add A, [R1R0]                 ;09
2B5:	jnc 2CB                       ;CACB
2B7:	mov A, 0x0                    ;70
2B8:	mov [R1R0], A                 ;05
2B9:	call 576                      ;F576
2BB:	mov R1R0, 0x64                ;5406
2BD:	mov A, 0xF                    ;7F
2BE:	xor [R1R0], A                 ;1E
2BF:	jmp 46B                       ;E46B
2C1:	mov R1R0, 0x64                ;5406
2C3:	mov A, [R1R0]                 ;04
2C4:	ja0 2BB                       ;82BB
2C6:	mov R1R0, 0x15                ;5501
2C8:	inc [R1R0]                    ;0C
2C9:	call 57A                      ;F57A
2CB:	jmp 110                       ;E110
2CD:	mov R1R0, 0x46                ;5604
2CF:	mov A, 0x1                    ;71
2D0:	mov [R1R0], A                 ;05
2D1:	jmp 62B                       ;E62B
2D3:	mov R3R2, 0x29                ;6902
2D5:	mov A, [R3R2]                 ;06
2D6:	jz A, 2DF                     ;B2DF
2D8:	mov A, R0                     ;21
2D9:	mov R4, A                     ;28
2DA:	mov R1R0, 0x1C                ;5C01
2DC:	xor A, [R1R0]                 ;1B
2DD:	jz A, 263                     ;B263
2DF:	mov R3R2, 0x47                ;6704
2E1:	mov A, [R3R2]                 ;06
2E2:	xor A, 0x5                    ;4305
2E4:	jz A, 331                     ;B331
2E6:	mov R1R0, 0x31                ;5103
2E8:	mov A, 0x0                    ;70
2E9:	mov [R1R0], A                 ;05
2EA:	call BB6                      ;FBB6
2EC:	mov R1R0, 0x0E                ;5E00
2EE:	mov A, [R1R0]                 ;04
2EF:	and A, 0x3                    ;4203
2F1:	mov [R1R0], A                 ;05
2F2:	mov A, [R1R0]                 ;04
2F3:	jnz A, 2CD                    ;BACD
2F5:	dec R0                        ;11
2F6:	mov A, R0                     ;21
2F7:	ja2 2F2                       ;92F2
2F9:	mov R1R0, 0x31                ;5103
2FB:	mov R3R2, 0x37                ;6703
2FD:	mov A, [R3R2]                 ;06
2FE:	sub A, 0x3                    ;4103
300:	mov [R1R0], A                 ;05
301:	inc [R3R2]                    ;0E
302:	call BB6                      ;FBB6
304:	mov R1R0, 0x31                ;5103
306:	dec [R1R0]                    ;0D
307:	call B28                      ;FB28
309:	mov R1R0, 0x31                ;5103
30B:	inc [R1R0]                    ;0C
30C:	inc [R1R0]                    ;0C
30D:	mov R3R2, 0x37                ;6703
30F:	mov A, [R3R2]                 ;06
310:	xor A, [R1R0]                 ;1B
311:	jnz A, 302                    ;BB02
313:	dec [R3R2]                    ;0F
314:	dec [R3R2]                    ;0F
315:	mov R4, 0x3                   ;4603
317:	mov R1R0, 0x0C                ;5C00
319:	mov A, 0x0                    ;70
31A:	mov [R1R0], A                 ;05
31B:	inc R0                        ;10
31C:	dec R4                        ;19
31D:	jnz R4, 31A                   ;DB1A
31F:	mov R1R0, 0x57                ;5705
321:	mov A, 0x3                    ;73
322:	mov [R1R0], A                 ;05
323:	mov R1R0, 0x0B                ;5B00
325:	mov [R1R0], A                 ;05
326:	mov R1R0, 0x31                ;5103
328:	dec [R1R0]                    ;0D
329:	call B28                      ;FB28
32B:	mov R1R0, 0x28                ;5802
32D:	mov A, 0x1                    ;71
32E:	xor [R1R0], A                 ;1E
32F:	jmp 110                       ;E110
331:	mov R1R0, 0x28                ;5802
333:	mov A, 0x1                    ;71
334:	xor [R1R0], A                 ;1E
335:	jmp 263                       ;E263
337:	mov R1R0, 0x47                ;5704
339:	mov A, [R1R0]                 ;04
33A:	sub A, 0x6                    ;4106
33C:	mov R1R0, 0x5D                ;5D05
33E:	mov A, [R1R0]                 ;04
33F:	jnc 343                       ;CB43
341:	jnz A, 383                    ;BB83
343:	jnz A, 35D                    ;BB5D
345:	mov A, 0x3                    ;73
346:	mov [R1R0], A                 ;05
347:	mov A, 0x0                    ;70
348:	call B12                      ;FB12
34A:	call DEB                      ;FDEB
34C:	mov R1R0, 0x1F                ;5F01
34E:	mov A, [R1R0]                 ;04
34F:	mov R1R0, 0x1E                ;5E01
351:	mov [R1R0], A                 ;05
352:	mov R1R0, 0x4C                ;5C04
354:	mov A, 0x0                    ;70
355:	mov [R1R0], A                 ;05
356:	inc R0                        ;10
357:	jnz R0, 355                   ;A355
359:	call D1B                      ;FD1B
35B:	jmp 107                       ;E107
35D:	mov R3R2, 0x80                ;6008
35F:	mov A, [R3R2]                 ;06
360:	mov R1R0, 0x86                ;5608
362:	xor A, [R1R0]                 ;1B
363:	jz A, 383                     ;B383
365:	inc R0                        ;10
366:	mov A, [R3R2]                 ;06
367:	xor A, [R1R0]                 ;1B
368:	jz A, 383                     ;B383
36A:	mov R1R0, 0x49                ;5904
36C:	mov A, [R1R0]                 ;04
36D:	jnz A, 383                    ;BB83
36F:	inc [R1R0]                    ;0C
370:	mov R1R0, 0x14                ;5401
372:	mov R3R2, 0x80                ;6008
374:	mov A, [R3R2]                 ;06
375:	dec A                         ;3F
376:	mov [R1R0], A                 ;05
377:	inc R0                        ;10
378:	mov A, 0x0                    ;70
379:	mov [R1R0], A                 ;05
37A:	mov A, 0x3                    ;73
37B:	call B12                      ;FB12
37D:	call 57A                      ;F57A
37F:	mov R1R0, 0x48                ;5804
381:	mov A, 0x0                    ;70
382:	mov [R1R0], A                 ;05
383:	jmp 12B                       ;E12B
385:	and A, 0x3                    ;4203
387:	mov R1R0, 0x12                ;5201
389:	mov [R1R0], A                 ;05
38A:	mov R1R0, 0x5D                ;5D05
38C:	mov A, [R1R0]                 ;04
38D:	jnz A, 427                    ;BC27
38F:	ret                           ;2E
390:	call 385                      ;F385
392:	mov R1R0, 0xBD                ;5D0B
394:	mov A, [R1R0]                 ;04
395:	ja3 3A1                       ;9BA1
397:	mov R1R0, 0x47                ;5704
399:	inc [R1R0]                    ;0C
39A:	mov A, [R1R0]                 ;04
39B:	xor A, 0x8                    ;4308
39D:	jnz A, 3A1                    ;BBA1
39F:	inc A                         ;31
3A0:	mov [R1R0], A                 ;05
3A1:	mov A, 0x8                    ;78
3A2:	call B12                      ;FB12
3A4:	call D6A                      ;FD6A
3A6:	call D91                      ;FD91
3A8:	call 609                      ;F609
3AA:	call 9D3                      ;F9D3
3AC:	call 9CB                      ;F9CB
3AE:	call 9EF                      ;F9EF
3B0:	call 9E1                      ;F9E1
3B2:	jmp 030                       ;E030
3B4:	call 385                      ;F385
3B6:	mov R1R0, 0xB5                ;550B
3B8:	mov A, [R1R0]                 ;04
3B9:	ja3 3C5                       ;9BC5
3BB:	mov R1R0, 0x46                ;5604
3BD:	inc [R1R0]                    ;0C
3BE:	mov A, [R1R0]                 ;04
3BF:	xor A, 0x6                    ;4306
3C1:	jnz A, 3C5                    ;BBC5
3C3:	mov A, 0x1                    ;71
3C4:	mov [R1R0], A                 ;05
3C5:	call D76                      ;FD76
3C7:	mov A, 0x8                    ;78
3C8:	call B12                      ;FB12
3CA:	jmp 110                       ;E110
3CC:	mov R1R0, 0x60                ;5006
3CE:	mov A, 0x0                    ;70
3CF:	mov [R1R0], A                 ;05
3D0:	mov R1R0, 0x71                ;5107
3D2:	mov [R1R0], A                 ;05
3D3:	mov R3R2, 0x50                ;6005
3D5:	inc [R3R2]                    ;0E
3D6:	mov A, [R3R2]                 ;06
3D7:	mov R1R0, 0x86                ;5608
3D9:	xor A, [R1R0]                 ;1B
3DA:	jz A, 3E7                     ;B3E7
3DC:	inc R0                        ;10
3DD:	mov A, [R3R2]                 ;06
3DE:	xor A, [R1R0]                 ;1B
3DF:	jz A, 3E7                     ;B3E7
3E1:	mov A, [R3R2]                 ;06
3E2:	mov R1R0, 0x80                ;5008
3E4:	xor A, [R1R0]                 ;1B
3E5:	jz A, 62B                     ;B62B
3E7:	mov A, 0x0                    ;70
3E8:	mov [R3R2], A                 ;07
3E9:	inc R2                        ;14
3EA:	mov [R3R2], A                 ;07
3EB:	jmp 1A8                       ;E1A8
3ED:	mov R1R0, 0x5D                ;5D05
3EF:	mov A, [R1R0]                 ;04
3F0:	jz A, 110                     ;B110
3F2:	mov R1R0, 0x47                ;5704
3F4:	mov A, [R1R0]                 ;04
3F5:	sub A, 0x6                    ;4106
3F7:	jnc 110                       ;C910
3F9:	jmp A56                       ;EA56
3FB:	mov R1R0, 0x85                ;5508
3FD:	mov A, [R1R0]                 ;04
3FE:	jz A, 425                     ;B425
400:	mov R1R0, 0x47                ;5704
402:	mov A, [R1R0]                 ;04
403:	dec A                         ;3F
404:	jz A, 425                     ;B425
406:	mov A, [R1R0]                 ;04
407:	xor A, 0x6                    ;4306
409:	jz A, 425                     ;B425
40B:	mov R1R0, 0x13                ;5301
40D:	mov A, 0x0                    ;70
40E:	mov [R1R0], A                 ;05
40F:	call 9D3                      ;F9D3
411:	mov R3R2, 0x86                ;6608
413:	call 44B                      ;F44B
415:	call 9D7                      ;F9D7
417:	mov R1R0, 0x85                ;5508
419:	mov A, [R1R0]                 ;04
41A:	dec A                         ;3F
41B:	jz A, 425                     ;B425
41D:	call 9CB                      ;F9CB
41F:	mov R3R2, 0x87                ;6708
421:	call 44B                      ;F44B
423:	call 9CF                      ;F9CF
425:	jmp 11A                       ;E11A
427:	mov R1R0, 0x47                ;5704
429:	mov A, [R1R0]                 ;04
42A:	sub A, 0x6                    ;4106
42C:	jnc 430                       ;CC30
42E:	jmp 800                       ;E800
430:	call 9F3                      ;F9F3
432:	mov A, R4                     ;29
433:	xor A, 0xF                    ;430F
435:	and [R1R0], A                 ;1D
436:	mov R3R2, 0x80                ;6008
438:	mov R1R0, 0x13                ;5301
43A:	mov A, 0xF                    ;7F
43B:	mov [R1R0], A                 ;05
43C:	call 44B                      ;F44B
43E:	call 9F3                      ;F9F3
440:	jmp 110                       ;E110
442:	mov R1R0, 0x13                ;5301
444:	mov A, [R1R0]                 ;04
445:	jnz A, 45C                    ;BC5C
447:	mov R1R0, 0x2A                ;5A02
449:	mov A, 0xF                    ;7F
44A:	xor [R1R0], A                 ;1E
44B:	mov R1R0, 0x13                ;5301
44D:	mov A, [R1R0]                 ;04
44E:	mov R1R0, 0x2A                ;5A02
450:	jz A, 454                     ;B454
452:	mov R1R0, 0x12                ;5201
454:	mov A, [R1R0]                 ;04
455:	ja1 45D                       ;8C5D
457:	mov A, [R3R2]                 ;06
458:	dec A                         ;3F
459:	jz A, 442                     ;B442
45B:	dec [R3R2]                    ;0F
45C:	ret                           ;2E
45D:	mov A, [R3R2]                 ;06
45E:	xor A, 0xA                    ;430A
460:	jz A, 442                     ;B442
462:	inc R2                        ;14
463:	mov A, [R3R2]                 ;06
464:	xor A, 0xA                    ;430A
466:	dec R2                        ;15
467:	jz A, 442                     ;B442
469:	inc [R3R2]                    ;0E
46A:	ret                           ;2E
46B:	mov R1R0, 0x29                ;5902
46D:	mov A, [R1R0]                 ;04
46E:	jz A, 48C                     ;B48C
470:	mov R1R0, 0x1B                ;5B01
472:	mov R3R2, 0x14                ;6401
474:	mov A, [R3R2]                 ;06
475:	xor A, [R1R0]                 ;1B
476:	jnz A, 48C                    ;BC8C
478:	inc R2                        ;14
479:	inc R0                        ;10
47A:	mov A, [R3R2]                 ;06
47B:	xor A, [R1R0]                 ;1B
47C:	jnz A, 48C                    ;BC8C
47E:	mov R1R0, 0x29                ;5902
480:	mov [R1R0], A                 ;05
481:	mov R1R0, 0x65                ;5506
483:	mov [R1R0], A                 ;05
484:	call 834                      ;F834
486:	mov R3R2, 0x03                ;6300
488:	call CF7                      ;FCF7
48A:	jmp 4B6                       ;E4B6
48C:	mov R1R0, 0x15                ;5501
48E:	mov A, [R1R0]                 ;04
48F:	xor A, 0xD                    ;430D
491:	jz A, 4C5                     ;B4C5
493:	mov A, [R1R0]                 ;04
494:	xor A, 0xC                    ;430C
496:	jz A, 4A9                     ;B4A9
498:	mov A, [R1R0]                 ;04
499:	mov R1R0, 0x31                ;5103
49B:	mov [R1R0], A                 ;05
49C:	call BB6                      ;FBB6
49E:	call AC1                      ;FAC1
4A0:	mov R1R0, 0x00                ;5000
4A2:	mov R3R2, 0x14                ;6401
4A4:	mov A, [R3R2]                 ;06
4A5:	mov R0, A                     ;20
4A6:	mov A, [R1R0]                 ;04
4A7:	jnz A, 4B0                    ;BCB0
4A9:	mov R1R0, 0x6F                ;5F06
4AB:	mov A, [R1R0]                 ;04
4AC:	jnz A, 21A                    ;BA1A
4AE:	jmp 2C1                       ;E2C1
4B0:	mov A, [R3R2]                 ;06
4B1:	mov R1R0, 0x30                ;5003
4B3:	mov [R1R0], A                 ;05
4B4:	call CF5                      ;FCF5
4B6:	mov A, 0x7                    ;77
4B7:	call B12                      ;FB12
4B9:	mov R1R0, 0x66                ;5606
4BB:	mov A, 0x1                    ;71
4BC:	mov [R1R0], A                 ;05
4BD:	call 834                      ;F834
4BF:	mov R1R0, 0x66                ;5606
4C1:	mov A, 0x0                    ;70
4C2:	mov [R1R0], A                 ;05
4C3:	jmp 4E0                       ;E4E0
4C5:	mov R1R0, 0x14                ;5401
4C7:	mov A, [R1R0]                 ;04
4C8:	inc A                         ;31
4C9:	mov R1R0, 0x82                ;5208
4CB:	xor A, [R1R0]                 ;1B
4CC:	jnz A, 4E0                    ;BCE0
4CE:	mov A, 0x6                    ;76
4CF:	call B12                      ;FB12
4D1:	call 9E1                      ;F9E1
4D3:	mov A, 0x0                    ;70
4D4:	mov R1R0, 0x82                ;5208
4D6:	mov [R1R0], A                 ;05
4D7:	mov R1R0, 0x94                ;5409
4D9:	mov [R1R0], A                 ;05
4DA:	call DEB                      ;FDEB
4DC:	mov R3R2, 0x05                ;6500
4DE:	call CF7                      ;FCF7
4E0:	call 576                      ;F576
4E2:	mov R1R0, 0x49                ;5904
4E4:	mov A, 0x0                    ;70
4E5:	mov [R1R0], A                 ;05
4E6:	mov R1R0, 0x6F                ;5F06
4E8:	mov A, [R1R0]                 ;04
4E9:	jnz A, 21A                    ;BA1A
4EB:	jmp 2CB                       ;E2CB
4ED:	mov R1R0, 0x38                ;5803
4EF:	inc [R1R0]                    ;0C
4F0:	mov A, [R1R0]                 ;04
4F1:	mov R1R0, 0x3A                ;5A03
4F3:	dec [R1R0]                    ;0D
4F4:	mov A, [R1R0]                 ;04
4F5:	jnz A, 567                    ;BD67
4F7:	mov R1R0, 0x47                ;5704
4F9:	mov A, [R1R0]                 ;04
4FA:	xor A, 0x5                    ;4305
4FC:	jnz A, 50C                    ;BD0C
4FE:	mov R1R0, 0x3B                ;5B03
500:	mov A, [R1R0]                 ;04
501:	sub A, 0x4                    ;4104
503:	jc 50C                        ;C50C
505:	mov R1R0, 0x35                ;5503
507:	dec [R1R0]                    ;0D
508:	dec [R1R0]                    ;0D
509:	mov R1R0, 0x36                ;5603
50B:	inc [R1R0]                    ;0C
50C:	mov R1R0, 0x35                ;5503
50E:	mov A, [R1R0]                 ;04
50F:	mov R1R0, 0x3A                ;5A03
511:	mov [R1R0], A                 ;05
512:	mov R1R0, 0x36                ;5603
514:	mov A, [R1R0]                 ;04
515:	mov R1R0, 0x38                ;5803
517:	mov [R1R0], A                 ;05
518:	mov R1R0, 0x39                ;5903
51A:	dec [R1R0]                    ;0D
51B:	mov R1R0, 0x3B                ;5B03
51D:	dec [R1R0]                    ;0D
51E:	mov A, [R1R0]                 ;04
51F:	jnz A, 567                    ;BD67
521:	mov R1R0, 0x08                ;5800
523:	mov A, [R1R0]                 ;04
524:	mov R2, A                     ;24
525:	inc R0                        ;10
526:	mov A, [R1R0]                 ;04
527:	mov R3, A                     ;26
528:	ret                           ;2E
529:	mov A, 0x0                    ;70
52A:	mov R1R0, 0x23                ;5302
52C:	mov [R1R0], A                 ;05
52D:	mov R1R0, 0x24                ;5402
52F:	mov [R1R0], A                 ;05
530:	mov R1R0, 0x4C                ;5C04
532:	mov [R1R0], A                 ;05
533:	inc R0                        ;10
534:	jnz R0, 532                   ;A532
536:	mov R1R0, 0x46                ;5604
538:	mov A, 0x3                    ;73
539:	mov [R1R0], A                 ;05
53A:	mov R1R0, 0x1F                ;5F01
53C:	mov A, 0x1                    ;71
53D:	mov [R1R0], A                 ;05
53E:	mov R1R0, 0x4B                ;5B04
540:	mov [R1R0], A                 ;05
541:	ret                           ;2E
542:	mov A, TMRL                   ;3A
543:	mov R4, A                     ;28
544:	sub A, 0x6                    ;4106
546:	jc 542                        ;C542
548:	mov A, R4                     ;29
549:	mov R1R0, 0x36                ;5603
54B:	mov [R1R0], A                 ;05
54C:	mov R1R0, 0x37                ;5703
54E:	mov A, 0xB                    ;7B
54F:	mov [R1R0], A                 ;05
550:	mov R1R0, 0x3A                ;5A03
552:	mov A, 0x5                    ;75
553:	mov [R1R0], A                 ;05
554:	mov R1R0, 0x35                ;5503
556:	mov [R1R0], A                 ;05
557:	mov R1R0, 0x3B                ;5B03
559:	mov A, 0x4                    ;74
55A:	mov [R1R0], A                 ;05
55B:	mov R1R0, 0x36                ;5603
55D:	mov A, [R1R0]                 ;04
55E:	mov R1R0, 0x38                ;5803
560:	mov [R1R0], A                 ;05
561:	mov R1R0, 0x37                ;5703
563:	mov A, [R1R0]                 ;04
564:	mov R1R0, 0x39                ;5903
566:	mov [R1R0], A                 ;05
567:	mov R1R0, 0x57                ;5705
569:	mov A, 0x2                    ;72
56A:	mov [R1R0], A                 ;05
56B:	mov R1R0, 0x0B                ;5B00
56D:	mov [R1R0], A                 ;05
56E:	mov R1R0, 0x05                ;5500
570:	mov A, 0x1                    ;71
571:	mov [R1R0], A                 ;05
572:	jmp B28                       ;EB28
574:	jmp 595                       ;E595
576:	mov R1R0, 0x22                ;5202
578:	mov A, 0x8                    ;78
579:	mov [R1R0], A                 ;05
57A:	mov R1R0, 0x14                ;5401
57C:	jmp 58C                       ;E58C
57E:	mov R1R0, 0x22                ;5202
580:	mov A, 0x8                    ;78
581:	mov [R1R0], A                 ;05
582:	mov R1R0, 0x52                ;5205
584:	jmp 58C                       ;E58C
586:	mov R1R0, 0x22                ;5202
588:	mov A, 0x8                    ;78
589:	mov [R1R0], A                 ;05
58A:	mov R1R0, 0x50                ;5005
58C:	mov A, [R1R0]                 ;04
58D:	mov R3R2, 0x38                ;6803
58F:	mov [R3R2], A                 ;07
590:	inc R0                        ;10
591:	mov R3R2, 0x39                ;6903
593:	mov A, [R1R0]                 ;04
594:	mov [R3R2], A                 ;07
595:	mov R1R0, 0x57                ;5705
597:	mov A, 0x1                    ;71
598:	mov [R1R0], A                 ;05
599:	mov R1R0, 0x0B                ;5B00
59B:	mov [R1R0], A                 ;05
59C:	mov R1R0, 0x5B                ;5B05
59E:	mov A, 0x1                    ;71
59F:	mov [R1R0], A                 ;05
5A0:	mov R1R0, 0x57                ;5705
5A2:	mov A, [R1R0]                 ;04
5A3:	xor A, 0x3                    ;4303
5A5:	jz A, 5B7                     ;B5B7
5A7:	mov R1R0, 0x38                ;5803
5A9:	mov A, [R1R0]                 ;04
5AA:	mov R1R0, 0x30                ;5003
5AC:	mov [R1R0], A                 ;05
5AD:	mov R1R0, 0x39                ;5903
5AF:	mov A, [R1R0]                 ;04
5B0:	mov R1R0, 0x31                ;5103
5B2:	mov [R1R0], A                 ;05
5B3:	mov R1R0, 0x0C                ;5C00
5B5:	mov A, 0x1                    ;71
5B6:	mov [R1R0], A                 ;05
5B7:	mov R1R0, 0x30                ;5003
5B9:	mov A, [R1R0]                 ;04
5BA:	sub A, 0x8                    ;4108
5BC:	jc 5DA                        ;C5DA
5BE:	mov A, [R1R0]                 ;04
5BF:	mov R4, A                     ;28
5C0:	mov R1R0, 0x10                ;5001
5C2:	mov A, 0xE                    ;7E
5C3:	readf MR0A                    ;4F
5C4:	mov [R1R0], A                 ;05
5C5:	mov R1R0, 0x31                ;5103
5C7:	mov A, 0x0                    ;70
5C8:	readf R4A                     ;4D
5C9:	mov R0, A                     ;20
5CA:	mov A, R4                     ;29
5CB:	mov R1, A                     ;22
5CC:	mov R3R2, 0x30                ;6003
5CE:	mov A, [R3R2]                 ;06
5CF:	sub A, 0x4                    ;4104
5D1:	jnc 5D4                       ;CDD4
5D3:	inc R0                        ;10
5D4:	mov R3R2, 0x10                ;6001
5D6:	mov A, [R3R2]                 ;06
5D7:	mov R4, A                     ;28
5D8:	jmp 5FB                       ;E5FB
5DA:	mov R1R0, 0x31                ;5103
5DC:	mov A, [R1R0]                 ;04
5DD:	mov A, 0x1                    ;71
5DE:	readf R4A                     ;4D
5DF:	mov R0, A                     ;20
5E0:	mov A, R4                     ;29
5E1:	mov R1, A                     ;22
5E2:	mov R3R2, 0x30                ;6003
5E4:	mov A, [R3R2]                 ;06
5E5:	xor A, 0x8                    ;4308
5E7:	jnz A, 5ED                    ;BDED
5E9:	mov R4, 0x2                   ;4602
5EB:	jmp 5EF                       ;E5EF
5ED:	mov R4, 0x8                   ;4608
5EF:	mov R3R2, 0x0B                ;6B00
5F1:	mov A, [R3R2]                 ;06
5F2:	dec A                         ;3F
5F3:	jnz A, 5F9                    ;BDF9
5F5:	mov A, R4                     ;29
5F6:	clc                           ;2A
5F7:	rr A                          ;00
5F8:	mov R4, A                     ;28
5F9:	jmp BF3                       ;EBF3
5FB:	mov R3R2, 0x0B                ;6B00
5FD:	mov A, [R3R2]                 ;06
5FE:	dec A                         ;3F
5FF:	jz A, 603                     ;B603
601:	jmp BF3                       ;EBF3
603:	inc R0                        ;10
604:	inc R0                        ;10
605:	jmp BF3                       ;EBF3
607:	db 0x0D                       ;0D
608:	db 0x2E                       ;2E
609:	mov R1R0, 0x57                ;5705
60B:	mov A, 0x3                    ;73
60C:	mov [R1R0], A                 ;05
60D:	mov A, 0x1                    ;71
60E:	mov R1R0, 0x0B                ;5B00
610:	mov [R1R0], A                 ;05
611:	mov A, 0xD                    ;7D
612:	jmp D99                       ;ED99
614:	mov A, 0x0                    ;70
615:	jmp 618                       ;E618
617:	mov A, 0xF                    ;7F
618:	mov [R1R0], A                 ;05
619:	dec R0                        ;11
61A:	jnz R0, 618                   ;A618
61C:	mov [R1R0], A                 ;05
61D:	dec R1                        ;13
61E:	jnz R1, 618                   ;AE18
620:	ret                           ;2E
621:	mov R1R0, 0x92                ;5209
623:	mov A, 0x0                    ;70
624:	mov [R1R0], A                 ;05
625:	inc R0                        ;10
626:	jnz R0, 624                   ;A624
628:	ret                           ;2E
629:	jmp C15                       ;EC15
62B:	mov R1R0, 0x56                ;5605
62D:	mov A, 0x5                    ;75
62E:	mov [R1R0], A                 ;05
62F:	mov R1R0, 0x81                ;5108
631:	mov A, 0x1                    ;71
632:	mov [R1R0], A                 ;05
633:	mov A, 0x7                    ;77
634:	call B12                      ;FB12
636:	mov A, 0x0                    ;70
637:	mov R1R0, 0x50                ;5005
639:	mov [R1R0], A                 ;05
63A:	mov R1R0, 0x47                ;5704
63C:	call D91                      ;FD91
63E:	mov R1R0, 0x81                ;5108
640:	mov A, [R1R0]                 ;04
641:	mov R1R0, 0x17                ;5701
643:	mov [R1R0], A                 ;05
644:	mov A, [R1R0]                 ;04
645:	mov R1R0, 0x16                ;5601
647:	mov [R1R0], A                 ;05
648:	mov R1R0, 0x18                ;5801
64A:	mov A, 0x0                    ;70
64B:	mov [R1R0], A                 ;05
64C:	mov R1R0, 0x16                ;5601
64E:	dec [R1R0]                    ;0D
64F:	mov A, [R1R0]                 ;04
650:	mov R3R2, 0x47                ;6704
652:	mov A, [R3R2]                 ;06
653:	sub A, 0x6                    ;4106
655:	jnc 65B                       ;CE5B
657:	mov A, [R3R2]                 ;06
658:	add A, [R1R0]                 ;09
659:	jmp 65C                       ;E65C
65B:	mov A, [R1R0]                 ;04
65C:	mov R1R0, 0x39                ;5903
65E:	mov [R1R0], A                 ;05
65F:	mov R1R0, 0x80                ;5008
661:	mov A, [R1R0]                 ;04
662:	dec A                         ;3F
663:	mov R1R0, 0x18                ;5801
665:	add A, [R1R0]                 ;09
666:	mov R1R0, 0x38                ;5803
668:	mov [R1R0], A                 ;05
669:	add A, 0x6                    ;4006
66B:	jc 66F                        ;C66F
66D:	call 574                      ;F574
66F:	mov R1R0, 0x80                ;5008
671:	mov A, [R1R0]                 ;04
672:	dec A                         ;3F
673:	mov R1R0, 0x18                ;5801
675:	sub A, [R1R0]                 ;0B
676:	jnc 6B2                       ;CEB2
678:	mov R1R0, 0x38                ;5803
67A:	mov [R1R0], A                 ;05
67B:	call 574                      ;F574
67D:	mov R1R0, 0x47                ;5704
67F:	mov A, [R1R0]                 ;04
680:	sub A, 0x6                    ;4106
682:	jnc 6B2                       ;CEB2
684:	mov R3R2, 0x39                ;6903
686:	mov A, [R1R0]                 ;04
687:	mov R1R0, 0x16                ;5601
689:	sub A, [R1R0]                 ;0B
68A:	mov [R3R2], A                 ;07
68B:	mov R1R0, 0x80                ;5008
68D:	mov A, [R1R0]                 ;04
68E:	dec A                         ;3F
68F:	mov R1R0, 0x18                ;5801
691:	add A, [R1R0]                 ;09
692:	mov R1R0, 0x38                ;5803
694:	mov [R1R0], A                 ;05
695:	call 574                      ;F574
697:	mov R1R0, 0x80                ;5008
699:	mov A, [R1R0]                 ;04
69A:	dec A                         ;3F
69B:	mov R1R0, 0x18                ;5801
69D:	sub A, [R1R0]                 ;0B
69E:	mov R1R0, 0x38                ;5803
6A0:	mov [R1R0], A                 ;05
6A1:	call 574                      ;F574
6A3:	mov R1R0, 0x56                ;5605
6A5:	mov A, [R1R0]                 ;04
6A6:	sub A, 0x3                    ;4103
6A8:	jc 6B0                        ;C6B0
6AA:	call 834                      ;F834
6AC:	call 831                      ;F831
6AE:	jmp 6B2                       ;E6B2
6B0:	call 838                      ;F838
6B2:	mov R1R0, 0x18                ;5801
6B4:	inc [R1R0]                    ;0C
6B5:	mov R1R0, 0x16                ;5601
6B7:	mov A, [R1R0]                 ;04
6B8:	jnz A, 64C                    ;BE4C
6BA:	mov A, 0x2                    ;72
6BB:	jtmr 629                      ;D629
6BD:	mov R1R0, 0x92                ;5209
6BF:	mov A, [R1R0]                 ;04
6C0:	add A, 0x4                    ;4004
6C2:	jnc 6BA                       ;CEBA
6C4:	call 609                      ;F609
6C6:	mov R1R0, 0x56                ;5605
6C8:	dec [R1R0]                    ;0D
6C9:	mov A, [R1R0]                 ;04
6CA:	sub A, 0x3                    ;4103
6CC:	jc 6D0                        ;C6D0
6CE:	call 9EF                      ;F9EF
6D0:	mov R1R0, 0x56                ;5605
6D2:	mov A, [R1R0]                 ;04
6D3:	mov R1R0, 0x17                ;5701
6D5:	inc [R1R0]                    ;0C
6D6:	jnz A, 644                    ;BE44
6D8:	mov R1R0, 0x46                ;5604
6DA:	dec [R1R0]                    ;0D
6DB:	call D76                      ;FD76
6DD:	mov R1R0, 0x1F                ;5F01
6DF:	inc [R1R0]                    ;0C
6E0:	mov A, [R1R0]                 ;04
6E1:	jnz A, 6E4                    ;BEE4
6E3:	dec [R1R0]                    ;0D
6E4:	mov R1R0, 0x70                ;5007
6E6:	mov A, [R1R0]                 ;04
6E7:	jnz A, 737                    ;BF37
6E9:	call 9EF                      ;F9EF
6EB:	call D91                      ;FD91
6ED:	call 609                      ;F609
6EF:	mov R1R0, 0x82                ;5208
6F1:	mov A, 0xA                    ;7A
6F2:	mov [R1R0], A                 ;05
6F3:	mov R1R0, 0x86                ;5608
6F5:	mov [R1R0], A                 ;05
6F6:	call 9E1                      ;F9E1
6F8:	call 9D3                      ;F9D3
6FA:	mov R1R0, 0x86                ;5608
6FC:	dec [R1R0]                    ;0D
6FD:	mov R1R0, 0x82                ;5208
6FF:	dec [R1R0]                    ;0D
700:	mov A, [R1R0]                 ;04
701:	jnz A, 6F6                    ;BEF6
703:	mov A, 0x0                    ;70
704:	mov R1R0, 0x49                ;5904
706:	mov [R1R0], A                 ;05
707:	mov R1R0, 0x60                ;5006
709:	mov [R1R0], A                 ;05
70A:	mov R1R0, 0x62                ;5206
70C:	mov [R1R0], A                 ;05
70D:	mov R1R0, 0x71                ;5107
70F:	mov [R1R0], A                 ;05
710:	mov R1R0, 0x29                ;5902
712:	mov [R1R0], A                 ;05
713:	mov R1R0, 0x82                ;5208
715:	mov [R1R0], A                 ;05
716:	mov R1R0, 0x80                ;5008
718:	mov [R1R0], A                 ;05
719:	mov R1R0, 0x1B                ;5B01
71B:	mov [R1R0], A                 ;05
71C:	inc R0                        ;10
71D:	mov [R1R0], A                 ;05
71E:	mov R1R0, 0x40                ;5004
720:	mov A, [R1R0]                 ;04
721:	jz A, 727                     ;B727
723:	mov A, 0x0                    ;70
724:	mov [R1R0], A                 ;05
725:	jmp 012                       ;E012
727:	mov R1R0, 0x46                ;5604
729:	mov A, [R1R0]                 ;04
72A:	jnz A, 030                    ;B830
72C:	call E45                      ;FE45
72E:	call D23                      ;FD23
730:	mov R1R0, 0x5D                ;5D05
732:	mov [R1R0], A                 ;05
733:	call AE3                      ;FAE3
735:	jmp 02A                       ;E02A
737:	mov R1R0, 0x46                ;5604
739:	mov A, [R1R0]                 ;04
73A:	jz A, 6E9                     ;B6E9
73C:	mov R1R0, 0x82                ;5208
73E:	mov A, [R1R0]                 ;04
73F:	dec A                         ;3F
740:	mov R1R0, 0x1B                ;5B01
742:	mov [R1R0], A                 ;05
743:	inc R0                        ;10
744:	mov A, 0xB                    ;7B
745:	mov [R1R0], A                 ;05
746:	jmp 08B                       ;E08B
748:	mov R4, 0x3                   ;4603
74A:	mov R1R0, 0x0E                ;5E00
74C:	mov A, 0x3                    ;73
74D:	and [R1R0], A                 ;1D
74E:	clc                           ;2A
74F:	mov A, [R1R0]                 ;04
750:	rrc A                         ;02
751:	mov [R1R0], A                 ;05
752:	dec R0                        ;11
753:	dec R4                        ;19
754:	jnz R4, 74F                   ;DF4F
756:	jnc 75C                       ;CF5C
758:	mov R1R0, 0x0E                ;5E00
75A:	mov A, 0x2                    ;72
75B:	or [R1R0], A                  ;1F
75C:	ret                           ;2E
75D:	mov R4, 0x3                   ;4603
75F:	mov R1R0, 0x0C                ;5C00
761:	clc                           ;2A
762:	mov A, [R1R0]                 ;04
763:	rlc A                         ;03
764:	mov [R1R0], A                 ;05
765:	inc R0                        ;10
766:	dec R4                        ;19
767:	jnz R4, 762                   ;DF62
769:	rlc A                         ;03
76A:	rlc A                         ;03
76B:	jnc 771                       ;CF71
76D:	mov R1R0, 0x0C                ;5C00
76F:	mov A, 0x1                    ;71
770:	or [R1R0], A                  ;1F
771:	ret                           ;2E
772:	mov R1R0, 0x31                ;5103
774:	mov A, 0xB                    ;7B
775:	mov [R1R0], A                 ;05
776:	call BB6                      ;FBB6
778:	mov R1R0, 0x0E                ;5E00
77A:	mov A, [R1R0]                 ;04
77B:	and A, 0x3                    ;4203
77D:	jnz A, 7A0                    ;BFA0
77F:	dec R0                        ;11
780:	mov A, [R1R0]                 ;04
781:	jnz A, 7A0                    ;BFA0
783:	dec R0                        ;11
784:	mov A, [R1R0]                 ;04
785:	jnz A, 7A0                    ;BFA0
787:	mov R1R0, 0x31                ;5103
789:	dec [R1R0]                    ;0D
78A:	mov A, [R1R0]                 ;04
78B:	xor A, 0xF                    ;430F
78D:	jnz A, 776                    ;BF76
78F:	mov R1R0, 0x47                ;5704
791:	mov A, [R1R0]                 ;04
792:	xor A, 0x5                    ;4305
794:	jnz A, 6DD                    ;BEDD
796:	mov R1R0, 0x82                ;5208
798:	mov A, [R1R0]                 ;04
799:	jnz A, 7A0                    ;BFA0
79B:	mov R1R0, 0x29                ;5902
79D:	mov A, [R1R0]                 ;04
79E:	jz A, 6DD                     ;B6DD
7A0:	jmp 134                       ;E134
7A2:	mov A, R0                     ;21
7A3:	mov R4, A                     ;28
7A4:	mov A, TMRL                   ;3A
7A5:	and A, 0x3                    ;4203
7A7:	jz A, 7B3                     ;B7B3
7A9:	inc R0                        ;10
7AA:	dec A                         ;3F
7AB:	jnz A, 7A9                    ;BFA9
7AD:	mov A, [R1R0]                 ;04
7AE:	jz A, 7B3                     ;B7B3
7B0:	mov A, R0                     ;21
7B1:	jmp 7B4                       ;E7B4
7B3:	mov A, R4                     ;29
7B4:	mov [R3R2], A                 ;07
7B5:	inc R2                        ;14
7B6:	mov R1R0, 0x31                ;5103
7B8:	mov A, [R1R0]                 ;04
7B9:	mov [R3R2], A                 ;07
7BA:	ret                           ;2E
7BB:	db 0x3E                       ;3E
7BC:	db 0x3E                       ;3E
7BD:	db 0x3E                       ;3E
7BE:	db 0x3E                       ;3E
7BF:	db 0x3E                       ;3E
7C0:	db 0x3E                       ;3E
7C1:	db 0x3E                       ;3E
7C2:	db 0x3E                       ;3E
7C3:	db 0x3E                       ;3E
7C4:	db 0x3E                       ;3E
7C5:	db 0x3E                       ;3E
7C6:	db 0x3E                       ;3E
7C7:	db 0x3E                       ;3E
7C8:	db 0x3E                       ;3E
7C9:	db 0x3E                       ;3E
7CA:	db 0x3E                       ;3E
7CB:	db 0x3E                       ;3E
7CC:	db 0x3E                       ;3E
7CD:	db 0x3E                       ;3E
7CE:	db 0x3E                       ;3E
7CF:	db 0x3E                       ;3E
7D0:	db 0x3E                       ;3E
7D1:	db 0x3E                       ;3E
7D2:	db 0x3E                       ;3E
7D3:	db 0x3E                       ;3E
7D4:	db 0x3E                       ;3E
7D5:	db 0x3E                       ;3E
7D6:	db 0x3E                       ;3E
7D7:	db 0x3E                       ;3E
7D8:	db 0x3E                       ;3E
7D9:	db 0x3E                       ;3E
7DA:	db 0x3E                       ;3E
7DB:	db 0x3E                       ;3E
7DC:	db 0x3E                       ;3E
7DD:	db 0x3E                       ;3E
7DE:	db 0x3E                       ;3E
7DF:	db 0x3E                       ;3E
7E0:	db 0x3E                       ;3E
7E1:	db 0x3E                       ;3E
7E2:	db 0x3E                       ;3E
7E3:	db 0x3E                       ;3E
7E4:	db 0x3E                       ;3E
7E5:	db 0x3E                       ;3E
7E6:	db 0x3E                       ;3E
7E7:	db 0x3E                       ;3E
7E8:	db 0x3E                       ;3E
7E9:	db 0x3E                       ;3E
7EA:	db 0x3E                       ;3E
7EB:	db 0x3E                       ;3E
7EC:	db 0x3E                       ;3E
7ED:	db 0x3E                       ;3E
7EE:	db 0x3E                       ;3E
7EF:	db 0x3E                       ;3E
7F0:	db 0x3E                       ;3E
7F1:	db 0x3E                       ;3E
7F2:	db 0x3E                       ;3E
7F3:	db 0x3E                       ;3E
7F4:	db 0x3E                       ;3E
7F5:	db 0x3E                       ;3E
7F6:	db 0x3E                       ;3E
7F7:	db 0x3E                       ;3E
7F8:	db 0x3E                       ;3E
7F9:	db 0x3E                       ;3E
7FA:	db 0x3E                       ;3E
7FB:	db 0x3E                       ;3E
7FC:	db 0x3E                       ;3E
7FD:	db 0x3E                       ;3E
7FE:	db 0x3E                       ;3E
7FF:	db 0x3E                       ;3E
800:	call 834                      ;F834
802:	mov R1R0, 0x12                ;5201
804:	mov A, [R1R0]                 ;04
805:	mov R1R0, 0x1B                ;5B01
807:	ja0 812                       ;8012
809:	inc [R1R0]                    ;0C
80A:	mov A, [R1R0]                 ;04
80B:	xor A, 0xA                    ;430A
80D:	jnz A, 819                    ;B819
80F:	dec [R1R0]                    ;0D
810:	jmp 819                       ;E819
812:	dec [R1R0]                    ;0D
813:	mov A, [R1R0]                 ;04
814:	xor A, 0xF                    ;430F
816:	jnz A, 819                    ;B819
818:	inc [R1R0]                    ;0C
819:	jmp A62                       ;EA62
81B:	db 0x52                       ;52
81C:	db 0x02                       ;02
81D:	db 0x78                       ;78
81E:	db 0x05                       ;05
81F:	db 0x70                       ;70
820:	db 0x5B                       ;5B
821:	db 0x00                       ;00
822:	db 0x05                       ;05
823:	db 0x57                       ;57
824:	db 0x05                       ;05
825:	db 0x71                       ;71
826:	db 0x05                       ;05
827:	db 0x5B                       ;5B
828:	db 0x05                       ;05
829:	db 0x05                       ;05
82A:	db 0x54                       ;54
82B:	db 0x00                       ;00
82C:	db 0x05                       ;05
82D:	db 0x10                       ;10
82E:	db 0x05                       ;05
82F:	db 0xE5                       ;E5
830:	db 0xB3                       ;B3
831:	mov A, 0x1                    ;71
832:	jmp 839                       ;E839
834:	mov R1R0, 0x22                ;5202
836:	mov A, 0x8                    ;78
837:	mov [R1R0], A                 ;05
838:	mov A, 0x0                    ;70
839:	mov R1R0, 0x0B                ;5B00
83B:	mov [R1R0], A                 ;05
83C:	mov R1R0, 0x57                ;5705
83E:	mov A, 0x1                    ;71
83F:	mov [R1R0], A                 ;05
840:	mov R1R0, 0x5B                ;5B05
842:	mov [R1R0], A                 ;05
843:	mov R1R0, 0x04                ;5400
845:	mov [R1R0], A                 ;05
846:	inc R0                        ;10
847:	mov [R1R0], A                 ;05
848:	mov R1R0, 0x66                ;5606
84A:	mov A, [R1R0]                 ;04
84B:	jnz A, 857                    ;B857
84D:	mov R1R0, 0x1B                ;5B01
84F:	mov R3R2, 0x30                ;6003
851:	mov A, [R1R0]                 ;04
852:	mov [R3R2], A                 ;07
853:	inc R2                        ;14
854:	inc R0                        ;10
855:	mov A, [R1R0]                 ;04
856:	mov [R3R2], A                 ;07
857:	jmp 5B3                       ;E5B3
859:	mov R1R0, 0x37                ;5703
85B:	mov A, [R1R0]                 ;04
85C:	sub A, 0x3                    ;4103
85E:	jc 868                        ;C068
860:	mov R3R2, 0x1F                ;6F01
862:	inc [R3R2]                    ;0E
863:	mov A, [R3R2]                 ;06
864:	jnz A, 867                    ;B867
866:	dec [R3R2]                    ;0F
867:	mov A, [R1R0]                 ;04
868:	mov R4, A                     ;28
869:	mov R3R2, 0x29                ;6902
86B:	mov A, [R3R2]                 ;06
86C:	jnz A, 8D8                    ;B8D8
86E:	mov A, R4                     ;29
86F:	mov R1R0, 0x31                ;5103
871:	mov [R1R0], A                 ;05
872:	call BB6                      ;FBB6
874:	call AC1                      ;FAC1
876:	mov A, [R1R0]                 ;04
877:	jnz A, 89A                    ;B89A
879:	mov A, R0                     ;21
87A:	inc R0                        ;10
87B:	xor A, 0xA                    ;430A
87D:	jnz A, 876                    ;B876
87F:	mov R1R0, 0x31                ;5103
881:	inc [R1R0]                    ;0C
882:	mov A, [R1R0]                 ;04
883:	dec A                         ;3F
884:	mov R1R0, 0x37                ;5703
886:	xor A, [R1R0]                 ;1B
887:	jnz A, 872                    ;B872
889:	mov R1R0, 0x29                ;5902
88B:	mov A, [R1R0]                 ;04
88C:	jnz A, 8D8                    ;B8D8
88E:	mov R1R0, 0x82                ;5208
890:	mov A, [R1R0]                 ;04
891:	jnz A, 8C6                    ;B8C6
893:	mov R1R0, 0x54                ;5405
895:	mov A, [R1R0]                 ;04
896:	jnz A, E9F                    ;BE9F
898:	jmp 1A8                       ;E1A8
89A:	mov R3R2, 0x50                ;6005
89C:	mov R3R2, 0x54                ;6405
89E:	mov A, [R3R2]                 ;06
89F:	mov R2, A                     ;24
8A0:	call 7A2                      ;F7A2
8A2:	mov R1R0, 0x00                ;5000
8A4:	mov R3R2, 0x80                ;6008
8A6:	mov A, [R3R2]                 ;06
8A7:	dec A                         ;3F
8A8:	mov R0, A                     ;20
8A9:	mov A, [R1R0]                 ;04
8AA:	jz A, 8B7                     ;B0B7
8AC:	mov A, [R3R2]                 ;06
8AD:	dec A                         ;3F
8AE:	mov R4, A                     ;28
8AF:	mov R3R2, 0x50                ;6005
8B1:	mov R1R0, 0x54                ;5405
8B3:	mov A, [R1R0]                 ;04
8B4:	mov R2, A                     ;24
8B5:	mov A, R4                     ;29
8B6:	mov [R3R2], A                 ;07
8B7:	mov R3R2, 0x60                ;6006
8B9:	mov R1R0, 0x54                ;5405
8BB:	mov A, [R1R0]                 ;04
8BC:	mov R2, A                     ;24
8BD:	mov A, 0xF                    ;7F
8BE:	mov [R3R2], A                 ;07
8BF:	mov R1R0, 0x54                ;5405
8C1:	mov A, [R1R0]                 ;04
8C2:	jnz A, E9D                    ;BE9D
8C4:	jmp 1A6                       ;E1A6
8C6:	mov R1R0, 0x82                ;5208
8C8:	mov A, [R1R0]                 ;04
8C9:	dec A                         ;3F
8CA:	mov R4, A                     ;28
8CB:	mov R3R2, 0x50                ;6005
8CD:	mov R1R0, 0x54                ;5405
8CF:	mov A, [R1R0]                 ;04
8D0:	mov R2, A                     ;24
8D1:	mov A, R4                     ;29
8D2:	mov [R3R2], A                 ;07
8D3:	mov A, 0xC                    ;7C
8D4:	inc R2                        ;14
8D5:	mov [R3R2], A                 ;07
8D6:	jmp 8B7                       ;E8B7
8D8:	mov R1R0, 0x1B                ;5B01
8DA:	mov A, [R1R0]                 ;04
8DB:	mov R4, A                     ;28
8DC:	mov R3R2, 0x50                ;6005
8DE:	mov R1R0, 0x54                ;5405
8E0:	mov A, [R1R0]                 ;04
8E1:	mov R2, A                     ;24
8E2:	mov A, R4                     ;29
8E3:	mov [R3R2], A                 ;07
8E4:	mov R3R2, 0x50                ;6005
8E6:	mov R1R0, 0x54                ;5405
8E8:	mov A, [R1R0]                 ;04
8E9:	inc A                         ;31
8EA:	mov R2, A                     ;24
8EB:	mov R1R0, 0x1C                ;5C01
8ED:	mov A, [R1R0]                 ;04
8EE:	mov [R3R2], A                 ;07
8EF:	jmp 8B7                       ;E8B7
8F1:	call 9E1                      ;F9E1
8F3:	mov R1R0, 0x2B                ;5B02
8F5:	mov A, [R1R0]                 ;04
8F6:	mov R3R2, 0x82                ;6208
8F8:	ja0 904                       ;8104
8FA:	inc [R3R2]                    ;0E
8FB:	mov A, [R3R2]                 ;06
8FC:	xor A, 0xB                    ;430B
8FE:	jnz A, 928                    ;B928
900:	dec [R3R2]                    ;0F
901:	dec [R3R2]                    ;0F
902:	jmp 90A                       ;E90A
904:	dec [R3R2]                    ;0F
905:	mov A, [R3R2]                 ;06
906:	jnz A, 928                    ;B928
908:	inc [R3R2]                    ;0E
909:	inc [R3R2]                    ;0E
90A:	mov R1R0, 0x2B                ;5B02
90C:	mov A, 0xF                    ;7F
90D:	xor [R1R0], A                 ;1E
90E:	mov R1R0, 0x47                ;5704
910:	mov A, [R1R0]                 ;04
911:	xor A, 0x5                    ;4305
913:	jz A, 91E                     ;B11E
915:	mov A, 0x0                    ;70
916:	mov [R3R2], A                 ;07
917:	mov R1R0, 0x94                ;5409
919:	mov [R1R0], A                 ;05
91A:	call DEB                      ;FDEB
91C:	jmp 20F                       ;E20F
91E:	mov R1R0, 0x2B                ;5B02
920:	mov A, [R1R0]                 ;04
921:	mov R1R0, 0x28                ;5802
923:	mov [R1R0], A                 ;05
924:	call 9E5                      ;F9E5
926:	jmp 2AC                       ;E2AC
928:	mov R1R0, 0x47                ;5704
92A:	mov A, [R1R0]                 ;04
92B:	xor A, 0x5                    ;4305
92D:	jz A, 924                     ;B124
92F:	call 9E5                      ;F9E5
931:	jmp 20F                       ;E20F
933:	mov R1R0, 0x29                ;5902
935:	mov A, 0x1                    ;71
936:	mov [R1R0], A                 ;05
937:	mov R1R0, 0x37                ;5703
939:	mov A, [R1R0]                 ;04
93A:	sub A, 0x3                    ;4103
93C:	mov R1R0, 0x31                ;5103
93E:	mov [R1R0], A                 ;05
93F:	call BB6                      ;FBB6
941:	call AC1                      ;FAC1
943:	mov R1R0, 0x00                ;5000
945:	mov A, [R1R0]                 ;04
946:	jnz A, 963                    ;B963
948:	mov A, R0                     ;21
949:	inc R0                        ;10
94A:	xor A, 0xA                    ;430A
94C:	jnz A, 945                    ;B945
94E:	mov R1R0, 0x31                ;5103
950:	inc [R1R0]                    ;0C
951:	mov A, [R1R0]                 ;04
952:	dec A                         ;3F
953:	mov R1R0, 0x37                ;5703
955:	xor A, [R1R0]                 ;1B
956:	jnz A, 93F                    ;B93F
958:	mov R1R0, 0x29                ;5902
95A:	mov A, 0x0                    ;70
95B:	mov [R1R0], A                 ;05
95C:	mov R1R0, 0x82                ;5208
95E:	mov A, [R1R0]                 ;04
95F:	jnz A, 9C7                    ;B9C7
961:	jmp 110                       ;E110
963:	mov R3R2, 0x1B                ;6B01
965:	call 7A2                      ;F7A2
967:	call 834                      ;F834
969:	mov R1R0, 0x1C                ;5C01
96B:	dec [R1R0]                    ;0D
96C:	mov A, [R1R0]                 ;04
96D:	xor A, 0xF                    ;430F
96F:	jnz A, 9A8                    ;B9A8
971:	mov R3R2, 0x1B                ;6B01
973:	mov A, [R3R2]                 ;06
974:	mov R1R0, 0x80                ;5008
976:	inc A                         ;31
977:	xor A, [R1R0]                 ;1B
978:	jz A, 9C9                     ;B1C9
97A:	mov A, 0xB                    ;7B
97B:	mov R1R0, 0x31                ;5103
97D:	mov [R1R0], A                 ;05
97E:	call BB6                      ;FBB6
980:	call AC1                      ;FAC1
982:	mov R1R0, 0x00                ;5000
984:	mov R3R2, 0x82                ;6208
986:	mov A, [R3R2]                 ;06
987:	dec A                         ;3F
988:	mov R0, A                     ;20
989:	mov A, [R1R0]                 ;04
98A:	jz A, 991                     ;B191
98C:	mov R1R0, 0x31                ;5103
98E:	dec [R1R0]                    ;0D
98F:	jmp 97E                       ;E97E
991:	mov R1R0, 0x82                ;5208
993:	mov A, [R1R0]                 ;04
994:	jz A, 99F                     ;B19F
996:	dec A                         ;3F
997:	mov R3R2, 0x1B                ;6B01
999:	mov [R3R2], A                 ;07
99A:	mov R1R0, 0x31                ;5103
99C:	mov A, [R1R0]                 ;04
99D:	inc R2                        ;14
99E:	mov [R3R2], A                 ;07
99F:	mov R1R0, 0x29                ;5902
9A1:	mov A, 0x0                    ;70
9A2:	mov [R1R0], A                 ;05
9A3:	mov R1R0, 0x65                ;5506
9A5:	mov [R1R0], A                 ;05
9A6:	jmp 9C5                       ;E9C5
9A8:	mov R3R2, 0x34                ;6403
9AA:	mov R1R0, 0x1B                ;5B01
9AC:	mov A, [R3R2]                 ;06
9AD:	ja0 9B9                       ;81B9
9AF:	inc [R1R0]                    ;0C
9B0:	mov A, [R1R0]                 ;04
9B1:	xor A, 0xA                    ;430A
9B3:	jnz A, 9C5                    ;B9C5
9B5:	dec [R1R0]                    ;0D
9B6:	dec [R1R0]                    ;0D
9B7:	jmp 9C1                       ;E9C1
9B9:	dec [R1R0]                    ;0D
9BA:	mov A, [R1R0]                 ;04
9BB:	xor A, 0xF                    ;430F
9BD:	jnz A, 9C5                    ;B9C5
9BF:	inc [R1R0]                    ;0C
9C0:	inc [R1R0]                    ;0C
9C1:	mov A, [R3R2]                 ;06
9C2:	xor A, 0x1                    ;4301
9C4:	mov [R3R2], A                 ;07
9C5:	call 838                      ;F838
9C7:	jmp 1D0                       ;E1D0
9C9:	jmp 62B                       ;E62B
9CB:	mov R1R0, 0x0A                ;5A00
9CD:	mov A, 0x1                    ;71
9CE:	mov [R1R0], A                 ;05
9CF:	mov R1R0, 0x87                ;5708
9D1:	jmp 9D9                       ;E9D9
9D3:	mov R1R0, 0x0A                ;5A00
9D5:	mov A, 0x1                    ;71
9D6:	mov [R1R0], A                 ;05
9D7:	mov R1R0, 0x86                ;5608
9D9:	mov A, [R1R0]                 ;04
9DA:	dec A                         ;3F
9DB:	mov R1R0, 0x83                ;5308
9DD:	mov [R1R0], A                 ;05
9DE:	mov A, 0x1                    ;71
9DF:	jmp 9FB                       ;E9FB
9E1:	mov R1R0, 0x0A                ;5A00
9E3:	mov A, 0x1                    ;71
9E4:	mov [R1R0], A                 ;05
9E5:	mov R1R0, 0x82                ;5208
9E7:	mov A, [R1R0]                 ;04
9E8:	dec A                         ;3F
9E9:	mov R1R0, 0x83                ;5308
9EB:	mov [R1R0], A                 ;05
9EC:	mov A, 0x2                    ;72
9ED:	jmp 9FB                       ;E9FB
9EF:	mov R1R0, 0x0A                ;5A00
9F1:	mov A, 0x1                    ;71
9F2:	mov [R1R0], A                 ;05
9F3:	mov R1R0, 0x80                ;5008
9F5:	mov A, [R1R0]                 ;04
9F6:	dec A                         ;3F
9F7:	mov R1R0, 0x83                ;5308
9F9:	mov [R1R0], A                 ;05
9FA:	mov A, 0x0                    ;70
9FB:	clc                           ;2A
9FC:	add A, 0x8                    ;4008
9FE:	mov R1R0, 0x10                ;5001
A00:	mov [R1R0], A                 ;05
A01:	mov A, 0xE                    ;7E
A02:	readf R4A                     ;4D
A03:	mov [R1R0], A                 ;05
A04:	clc                           ;2A
A05:	mov R3R2, 0x83                ;6308
A07:	mov A, [R3R2]                 ;06
A08:	add A, [R1R0]                 ;09
A09:	mov [R1R0], A                 ;05
A0A:	jnc A0D                       ;CA0D
A0C:	inc R4                        ;18
A0D:	inc R0                        ;10
A0E:	mov A, R4                     ;29
A0F:	mov [R1R0], A                 ;05
A10:	dec R0                        ;11
A11:	mov A, [R1R0]                 ;04
A12:	mov R4, A                     ;28
A13:	inc R0                        ;10
A14:	mov A, [R1R0]                 ;04
A15:	readf MR0A                    ;4F
A16:	mov R2, A                     ;24
A17:	mov A, [R1R0]                 ;04
A18:	and A, 0x3                    ;4203
A1A:	add A, 0xB                    ;400B
A1C:	dec R0                        ;11
A1D:	mov [R1R0], A                 ;05
A1E:	mov A, 0xE                    ;7E
A1F:	readf R4A                     ;4D
A20:	mov R3, A                     ;26
A21:	inc R0                        ;10
A22:	mov A, [R1R0]                 ;04
A23:	rr A                          ;00
A24:	and A, 0x6                    ;4206
A26:	mov R4, A                     ;28
A27:	mov A, R2                     ;25
A28:	mov R0, A                     ;20
A29:	mov A, R3                     ;27
A2A:	mov R1, A                     ;22
A2B:	mov A, R4                     ;29
A2C:	mov R4, 0x1                   ;4601
A2E:	jz A, A37                     ;B237
A30:	mov R4, A                     ;28
A31:	xor A, 0x6                    ;4306
A33:	jnz A, A37                    ;BA37
A35:	mov R4, 0x8                   ;4608
A37:	mov R3R2, 0x0A                ;6A00
A39:	mov A, [R3R2]                 ;06
A3A:	jnz A, A3F                    ;BA3F
A3C:	mov A, R4                     ;29
A3D:	or [R1R0], A                  ;1F
A3E:	ret                           ;2E
A3F:	mov A, R4                     ;29
A40:	xor A, 0xF                    ;430F
A42:	and [R1R0], A                 ;1D
A43:	mov A, 0x0                    ;70
A44:	mov [R3R2], A                 ;07
A45:	ret                           ;2E
A46:	mov R1R0, 0x1F                ;5F01
A48:	mov A, [R1R0]                 ;04
A49:	add A, 0x7                    ;4007
A4B:	jnc A4E                       ;CA4E
A4D:	mov A, 0xF                    ;7F
A4E:	clc                           ;2A
A4F:	sub A, 0x2                    ;4102
A51:	mov R1R0, 0x94                ;5409
A53:	add A, [R1R0]                 ;09
A54:	jnc A7C                       ;CA7C
A56:	mov R1R0, 0x94                ;5409
A58:	mov A, 0x0                    ;70
A59:	mov [R1R0], A                 ;05
A5A:	call 834                      ;F834
A5C:	mov R1R0, 0x1C                ;5C01
A5E:	mov A, [R1R0]                 ;04
A5F:	jz A, A82                     ;B282
A61:	dec [R1R0]                    ;0D
A62:	call 838                      ;F838
A64:	mov A, 0x3                    ;73
A65:	call B12                      ;FB12
A67:	mov R1R0, 0x1C                ;5C01
A69:	mov A, [R1R0]                 ;04
A6A:	mov R1R0, 0x31                ;5103
A6C:	mov [R1R0], A                 ;05
A6D:	mov R1R0, 0x30                ;5003
A6F:	mov A, 0x0                    ;70
A70:	mov [R1R0], A                 ;05
A71:	call BAF                      ;FBAF
A73:	call AC1                      ;FAC1
A75:	mov R3R2, 0x1B                ;6B01
A77:	mov A, [R3R2]                 ;06
A78:	mov R0, A                     ;20
A79:	mov A, [R1R0]                 ;04
A7A:	jnz A, A8B                    ;BA8B
A7C:	jmp 110                       ;E110
A7E:	call CF5                      ;FCF5
A80:	jmp 6DD                       ;E6DD
A82:	mov R1R0, 0x1B                ;5B01
A84:	mov A, [R1R0]                 ;04
A85:	inc A                         ;31
A86:	mov R1R0, 0x86                ;5608
A88:	xor A, [R1R0]                 ;1B
A89:	jz A, A7E                     ;B27E
A8B:	call 609                      ;F609
A8D:	call 834                      ;F834
A8F:	mov R3R2, 0x80                ;6008
A91:	mov A, 0x5                    ;75
A92:	mov [R3R2], A                 ;07
A93:	inc R2                        ;14
A94:	mov A, 0x2                    ;72
A95:	mov [R3R2], A                 ;07
A96:	mov R1R0, 0x56                ;5605
A98:	mov A, 0x4                    ;74
A99:	mov [R1R0], A                 ;05
A9A:	mov R1R0, 0x1B                ;5B01
A9C:	mov A, 0x4                    ;74
A9D:	mov [R1R0], A                 ;05
A9E:	inc R0                        ;10
A9F:	mov R3R2, 0x47                ;6704
AA1:	mov A, [R3R2]                 ;06
AA2:	mov [R1R0], A                 ;05
AA3:	mov R1R0, 0x70                ;5007
AA5:	mov [R1R0], A                 ;05
AA6:	jmp 633                       ;E633
AA8:	call D76                      ;FD76
AAA:	jmp 110                       ;E110
AAC:	mov R1R0, 0x0C                ;5C00
AAE:	clc                           ;2A
AAF:	mov R3R2, 0x0E                ;6E00
AB1:	mov A, [R3R2]                 ;06
AB2:	rrc A                         ;02
AB3:	mov [R3R2], A                 ;07
AB4:	dec R2                        ;15
AB5:	mov A, R2                     ;25
AB6:	ja2 AB1                       ;92B1
AB8:	dec R0                        ;11
AB9:	mov A, 0x0                    ;70
ABA:	jnc ABD                       ;CABD
ABC:	mov A, 0x1                    ;71
ABD:	mov [R1R0], A                 ;05
ABE:	jnz R0, AAF                   ;A2AF
AC0:	ret                           ;2E
AC1:	mov R1R0, 0x0A                ;5A00
AC3:	clc                           ;2A
AC4:	mov R3R2, 0x0E                ;6E00
AC6:	mov A, [R3R2]                 ;06
AC7:	and A, 0x3                    ;4203
AC9:	mov [R3R2], A                 ;07
ACA:	mov A, [R3R2]                 ;06
ACB:	rrc A                         ;02
ACC:	mov [R3R2], A                 ;07
ACD:	dec R2                        ;15
ACE:	mov A, R2                     ;25
ACF:	ja2 ACA                       ;92CA
AD1:	dec R0                        ;11
AD2:	mov A, 0x0                    ;70
AD3:	jnc AD6                       ;CAD6
AD5:	mov A, 0x1                    ;71
AD6:	mov [R1R0], A                 ;05
AD7:	jnz R0, AC4                   ;A2C4
AD9:	ret                           ;2E
ADA:	db 0x70                       ;70
ADB:	mov A, 0x1                    ;71
ADC:	mov R4, A                     ;28
ADD:	jmp AE5                       ;EAE5
ADF:	mov A, 0x0                    ;70
AE0:	mov R4, A                     ;28
AE1:	jmp AE5                       ;EAE5
AE3:	mov A, 0x2                    ;72
AE4:	mov R4, A                     ;28
AE5:	mov R1R0, 0xC1                ;510C
AE7:	mov A, [R1R0]                 ;04
AE8:	xor A, 0xF                    ;430F
AEA:	ja3 AEE                       ;9AEE
AEC:	mov A, R4                     ;29
AED:	sound A                       ;4B
AEE:	mov A, R4                     ;29
AEF:	mov R1R0, 0x10                ;5001
AF1:	mov [R1R0], A                 ;05
AF2:	mov A, 0xC                    ;7C
AF3:	readf R4A                     ;4D
AF4:	mov [R1R0], A                 ;05
AF5:	mov R1R0, 0x92                ;5209
AF7:	mov A, 0x0                    ;70
AF8:	mov [R1R0], A                 ;05
AF9:	inc R0                        ;10
AFA:	jnz R0, AF8                   ;A2F8
AFC:	mov A, 0x3                    ;73
AFD:	jtmr B10                      ;D310
AFF:	jmp AFC                       ;EAFC
B01:	mov R1R0, 0x9D                ;5D09
B03:	mov A, 0xF                    ;7F
B04:	add A, [R1R0]                 ;09
B05:	jnc AFC                       ;CAFC
B07:	mov A, 0x0                    ;70
B08:	mov [R1R0], A                 ;05
B09:	mov R1R0, 0x10                ;5001
B0B:	dec [R1R0]                    ;0D
B0C:	mov A, [R1R0]                 ;04
B0D:	jnz A, AFC                    ;BAFC
B0F:	ret                           ;2E
B10:	jmp C15                       ;EC15
B12:	mov R4, A                     ;28
B13:	mov R1R0, 0xC1                ;510C
B15:	mov A, [R1R0]                 ;04
B16:	ja3 B19                       ;9B19
B18:	ret                           ;2E
B19:	mov A, R4                     ;29
B1A:	sound A                       ;4B
B1B:	ret                           ;2E
B1C:	mov R1R0, 0x05                ;5500
B1E:	mov A, 0xA                    ;7A
B1F:	mov [R1R0], A                 ;05
B20:	mov R1R0, 0x0B                ;5B00
B22:	mov A, 0x1                    ;71
B23:	mov [R1R0], A                 ;05
B24:	mov R1R0, 0x57                ;5705
B26:	mov A, 0x3                    ;73
B27:	mov [R1R0], A                 ;05
B28:	mov R1R0, 0x57                ;5705
B2A:	mov A, 0x3                    ;73
B2B:	xor A, [R1R0]                 ;1B
B2C:	jnz A, B32                    ;BB32
B2E:	mov R1R0, 0x30                ;5003
B30:	mov A, 0x9                    ;79
B31:	mov [R1R0], A                 ;05
B32:	mov R1R0, 0x5B                ;5B05
B34:	mov A, 0x1                    ;71
B35:	mov [R1R0], A                 ;05
B36:	jmp BC8                       ;EBC8
B38:	mov R1R0, 0x03                ;5300
B3A:	jmp BDB                       ;EBDB
B3C:	mov R3R2, 0x0E                ;6E00
B3E:	mov A, [R3R2]                 ;06
B3F:	rrc A                         ;02
B40:	mov [R3R2], A                 ;07
B41:	dec R2                        ;15
B42:	mov A, R2                     ;25
B43:	ja2 B3E                       ;933E
B45:	mov R3R2, 0x22                ;6202
B47:	mov A, [R3R2]                 ;06
B48:	jz A, B4B                     ;B34B
B4A:	clc                           ;2A
B4B:	mov A, R4                     ;29
B4C:	or [R1R0], A                  ;1F
B4D:	jc B50                        ;C350
B4F:	xor [R1R0], A                 ;1E
B50:	mov R1R0, 0x57                ;5705
B52:	mov A, [R1R0]                 ;04
B53:	xor A, 0x3                    ;4303
B55:	jnz A, B5C                    ;BB5C
B57:	mov R1R0, 0x30                ;5003
B59:	dec [R1R0]                    ;0D
B5A:	jmp B65                       ;EB65
B5C:	mov R1R0, 0x02                ;5200
B5E:	dec [R1R0]                    ;0D
B5F:	mov A, [R1R0]                 ;04
B60:	inc A                         ;31
B61:	jnz A, B65                    ;BB65
B63:	inc R0                        ;10
B64:	dec [R1R0]                    ;0D
B65:	mov R1R0, 0x04                ;5400
B67:	dec [R1R0]                    ;0D
B68:	mov A, [R1R0]                 ;04
B69:	jnz A, B38                    ;BB38
B6B:	mov R1R0, 0x57                ;5705
B6D:	mov A, [R1R0]                 ;04
B6E:	jz A, B72                     ;B372
B70:	jmp B84                       ;EB84
B72:	ja1 B74                       ;8B74
B74:	mov R4, 0x2                   ;4602
B76:	mov R1R0, 0x05                ;5500
B78:	mov A, [R1R0]                 ;04
B79:	mov R1R0, 0x02                ;5200
B7B:	add A, [R1R0]                 ;09
B7C:	mov [R1R0], A                 ;05
B7D:	inc R0                        ;10
B7E:	jnc B81                       ;CB81
B80:	inc [R1R0]                    ;0C
B81:	dec R4                        ;19
B82:	jnz R4, B76                   ;DB76
B84:	mov R1R0, 0x08                ;5800
B86:	mov A, [R1R0]                 ;04
B87:	mov R2, A                     ;24
B88:	inc R0                        ;10
B89:	mov A, [R1R0]                 ;04
B8A:	mov R3, A                     ;26
B8B:	mov R1R0, 0x22                ;5202
B8D:	mov A, [R1R0]                 ;04
B8E:	jnz A, BA1                    ;BBA1
B90:	mov R1R0, 0x57                ;5705
B92:	mov A, [R1R0]                 ;04
B93:	jz A, B9F                     ;B39F
B95:	dec A                         ;3F
B96:	jz A, B9C                     ;B39C
B98:	dec A                         ;3F
B99:	jz A, B9D                     ;B39D
B9B:	dec A                         ;3F
B9C:	ret                           ;2E
B9D:	jmp 4ED                       ;E4ED
B9F:	jmp D62                       ;ED62
BA1:	ja3 BA8                       ;9BA8
BA3:	mov R3R2, 0x31                ;6103
BA5:	mov A, [R3R2]                 ;06
BA6:	jnz A, DA0                    ;BDA0
BA8:	mov R1R0, 0x22                ;5202
BAA:	mov A, 0x0                    ;70
BAB:	mov [R1R0], A                 ;05
BAC:	ret                           ;2E
BAD:	jmp F6C                       ;EF6C
BAF:	mov A, 0x1                    ;71
BB0:	mov R1R0, 0x0B                ;5B00
BB2:	mov [R1R0], A                 ;05
BB3:	mov A, 0x3                    ;73
BB4:	jmp BBA                       ;EBBA
BB6:	mov A, 0x3                    ;73
BB7:	mov R1R0, 0x0B                ;5B00
BB9:	mov [R1R0], A                 ;05
BBA:	mov R1R0, 0x57                ;5705
BBC:	mov [R1R0], A                 ;05
BBD:	mov R1R0, 0x05                ;5500
BBF:	mov A, 0xA                    ;7A
BC0:	mov [R1R0], A                 ;05
BC1:	mov R1R0, 0x1D                ;5D01
BC3:	mov A, 0x0                    ;70
BC4:	mov [R1R0], A                 ;05
BC5:	mov R1R0, 0x5B                ;5B05
BC7:	mov [R1R0], A                 ;05
BC8:	rr A                          ;00
BC9:	mov R1R0, 0x08                ;5800
BCB:	mov A, R2                     ;25
BCC:	mov [R1R0], A                 ;05
BCD:	inc R0                        ;10
BCE:	mov A, R3                     ;27
BCF:	mov [R1R0], A                 ;05
BD0:	mov R1R0, 0x05                ;5500
BD2:	mov A, [R1R0]                 ;04
BD3:	dec R0                        ;11
BD4:	mov [R1R0], A                 ;05
BD5:	jc B38                        ;C338
BD7:	mov R1R0, 0x30                ;5003
BD9:	mov A, 0x0                    ;70
BDA:	mov [R1R0], A                 ;05
BDB:	mov A, 0x1                    ;71
BDC:	jtmr C15                      ;D415
BDE:	mov R3R2, 0x57                ;6705
BE0:	mov A, [R3R2]                 ;06
BE1:	jz A, BAD                     ;B3AD
BE3:	jmp 5A0                       ;E5A0
BE5:	mov A, [R1R0]                 ;04
BE6:	mov R2, A                     ;24
BE7:	mov A, R4                     ;29
BE8:	rr A                          ;00
BE9:	rr A                          ;00
BEA:	and A, 0x3                    ;4203
BEC:	add A, 0xC                    ;400C
BEE:	mov [R1R0], A                 ;05
BEF:	mov A, 0xF                    ;7F
BF0:	readf R4A                     ;4D
BF1:	mov A, R2                     ;25
BF2:	mov [R1R0], A                 ;05
BF3:	mov R3R2, 0x5B                ;6B05
BF5:	mov A, [R3R2]                 ;06
BF6:	jz A, BFD                     ;B3FD
BF8:	dec A                         ;3F
BF9:	jz A, B3C                     ;B33C
BFB:	jmp DD3                       ;EDD3
BFD:	mov A, R4                     ;29
BFE:	and A, [R1R0]                 ;1A
BFF:	clc                           ;2A
C00:	jz A, C03                     ;B403
C02:	stc                           ;2B
C03:	mov R1R0, 0x0C                ;5C00
C05:	mov A, [R1R0]                 ;04
C06:	rlc A                         ;03
C07:	mov [R1R0], A                 ;05
C08:	inc R0                        ;10
C09:	jnz R0, C05                   ;A405
C0B:	mov R1R0, 0x30                ;5003
C0D:	inc [R1R0]                    ;0C
C0E:	mov R1R0, 0x04                ;5400
C10:	dec [R1R0]                    ;0D
C11:	mov A, [R1R0]                 ;04
C12:	jnz A, BDB                    ;BBDB
C14:	ret                           ;2E
C15:	mov R4, A                     ;28
C16:	mov R3R2, 0x33                ;6303
C18:	inc [R3R2]                    ;0E
C19:	mov R3R2, 0x92                ;6209
C1B:	inc [R3R2]                    ;0E
C1C:	inc R2                        ;14
C1D:	inc [R3R2]                    ;0E
C1E:	mov A, [R3R2]                 ;06
C1F:	xor A, 0x8                    ;4308
C21:	jnz A, C89                    ;BC89
C23:	mov [R3R2], A                 ;07
C24:	mov R3R2, 0x48                ;6804
C26:	inc [R3R2]                    ;0E
C27:	mov R3R2, 0x32                ;6203
C29:	inc [R3R2]                    ;0E
C2A:	mov R3R2, 0x94                ;6409
C2C:	mov R3R2, 0x95                ;6509
C2E:	inc [R3R2]                    ;0E
C2F:	inc R2                        ;14
C30:	inc [R3R2]                    ;0E
C31:	inc R2                        ;14
C32:	inc [R3R2]                    ;0E
C33:	mov A, [R3R2]                 ;06
C34:	xor A, 0x4                    ;4304
C36:	jnz A, C89                    ;BC89
C38:	mov [R3R2], A                 ;07
C39:	mov R3R2, 0x91                ;6109
C3B:	inc [R3R2]                    ;0E
C3C:	mov R3R2, 0x63                ;6306
C3E:	inc [R3R2]                    ;0E
C3F:	mov R3R2, 0x98                ;6809
C41:	inc [R3R2]                    ;0E
C42:	inc R2                        ;14
C43:	inc [R3R2]                    ;0E
C44:	mov A, [R3R2]                 ;06
C45:	xor A, 0x4                    ;4304
C47:	jnz A, C89                    ;BC89
C49:	mov [R3R2], A                 ;07
C4A:	mov R3R2, 0x94                ;6409
C4C:	inc [R3R2]                    ;0E
C4D:	mov R3R2, 0x90                ;6009
C4F:	inc [R3R2]                    ;0E
C50:	mov R3R2, 0x65                ;6506
C52:	inc [R3R2]                    ;0E
C53:	mov R3R2, 0x45                ;6504
C55:	mov A, [R3R2]                 ;06
C56:	xor A, 0xF                    ;430F
C58:	mov [R3R2], A                 ;07
C59:	mov R3R2, 0x9A                ;6A09
C5B:	inc [R3R2]                    ;0E
C5C:	inc R2                        ;14
C5D:	inc [R3R2]                    ;0E
C5E:	inc R2                        ;14
C5F:	inc [R3R2]                    ;0E
C60:	mov A, [R3R2]                 ;06
C61:	xor A, 0x2                    ;4302
C63:	jnz A, C89                    ;BC89
C65:	mov [R3R2], A                 ;07
C66:	mov R3R2, 0x61                ;6106
C68:	inc [R3R2]                    ;0E
C69:	mov R3R2, 0x68                ;6806
C6B:	inc [R3R2]                    ;0E
C6C:	mov R3R2, 0x9D                ;6D09
C6E:	inc [R3R2]                    ;0E
C6F:	mov A, [R3R2]                 ;06
C70:	xor A, 0x5                    ;4305
C72:	jnz A, C89                    ;BC89
C74:	mov [R3R2], A                 ;07
C75:	mov R3R2, 0x9E                ;6E09
C77:	inc [R3R2]                    ;0E
C78:	mov A, [R3R2]                 ;06
C79:	xor A, 0xC                    ;430C
C7B:	jnz A, C89                    ;BC89
C7D:	mov [R3R2], A                 ;07
C7E:	inc R2                        ;14
C7F:	inc [R3R2]                    ;0E
C80:	mov A, [R3R2]                 ;06
C81:	add A, 0x6                    ;4006
C83:	jnc C89                       ;CC89
C85:	jmp E27                       ;EE27
C87:	jmp 6BD                       ;E6BD
C89:	mov A, R4                     ;29
C8A:	jz A, C9A                     ;B49A
C8C:	dec A                         ;3F
C8D:	jz A, BDE                     ;B3DE
C8F:	dec A                         ;3F
C90:	jz A, C87                     ;B487
C92:	dec A                         ;3F
C93:	jz A, B01                     ;B301
C95:	jmp DD1                       ;EDD1
C97:	mov A, 0x0                    ;70
C98:	jtmr C15                      ;D415
C9A:	mov R3R2, 0x00                ;6000
C9C:	mov R1R0, 0x92                ;5209
C9E:	mov A, 0xC                    ;7C
C9F:	add A, [R1R0]                 ;09
CA0:	jnc CE8                       ;CCE8
CA2:	mov A, 0x0                    ;70
CA3:	mov [R1R0], A                 ;05
CA4:	mov R1R0, 0x23                ;5302
CA6:	mov A, 0xF                    ;7F
CA7:	xor A, [R1R0]                 ;1B
CA8:	mov R3, A                     ;26
CA9:	in A, PS                      ;33
CAA:	mov [R1R0], A                 ;05
CAB:	mov A, R3                     ;27
CAC:	or A, [R1R0]                  ;1C
CAD:	xor A, 0xF                    ;430F
CAF:	mov R3, A                     ;26
CB0:	mov R1R0, 0x24                ;5402
CB2:	mov A, 0xF                    ;7F
CB3:	xor A, [R1R0]                 ;1B
CB4:	mov R2, A                     ;24
CB5:	in A, PP                      ;34
CB6:	mov [R1R0], A                 ;05
CB7:	mov A, R2                     ;25
CB8:	or A, [R1R0]                  ;1C
CB9:	xor A, 0xF                    ;430F
CBB:	mov R2, A                     ;24
CBC:	ja0 DF5                       ;85F5
CBE:	ja1 E1A                       ;8E1A
CC0:	ja2 CE9                       ;94E9
CC2:	mov R1R0, 0x5D                ;5D05
CC4:	mov A, [R1R0]                 ;04
CC5:	jz A, CE4                     ;B4E4
CC7:	in A, PS                      ;33
CC8:	xor A, 0xF                    ;430F
CCA:	jz A, CD9                     ;B4D9
CCC:	and A, 0x7                    ;4207
CCE:	mov R4, A                     ;28
CCF:	mov R1R0, 0x25                ;5502
CD1:	dec [R1R0]                    ;0D
CD2:	mov A, [R1R0]                 ;04
CD3:	jnz A, CE8                    ;BCE8
CD5:	mov A, R4                     ;29
CD6:	mov R3, A                     ;26
CD7:	jmp CE4                       ;ECE4
CD9:	in A, PP                      ;34
CDA:	ja3 CE4                       ;9CE4
CDC:	mov R1R0, 0x25                ;5502
CDE:	dec [R1R0]                    ;0D
CDF:	mov A, [R1R0]                 ;04
CE0:	jnz A, CE8                    ;BCE8
CE2:	mov A, 0x8                    ;78
CE3:	mov R2, A                     ;24
CE4:	mov R1R0, 0x25                ;5502
CE6:	mov A, 0xF                    ;7F
CE7:	mov [R1R0], A                 ;05
CE8:	ret                           ;2E
CE9:	mov R1R0, 0xC1                ;510C
CEB:	mov A, 0x8                    ;78
CEC:	xor [R1R0], A                 ;1E
CED:	mov A, [R1R0]                 ;04
CEE:	ja3 CF2                       ;9CF2
CF0:	sound off                     ;4A
CF1:	ret                           ;2E
CF2:	sound 7                       ;4507
CF4:	ret                           ;2E
CF5:	mov R3R2, 0x01                ;6100
CF7:	mov R1R0, 0x4C                ;5C04
CF9:	mov R4, 0x1                   ;4601
CFB:	clc                           ;2A
CFC:	mov A, R2                     ;25
CFD:	adc A, [R1R0]                 ;08
CFE:	daa                           ;36
CFF:	mov [R1R0], A                 ;05
D00:	jnc D1B                       ;CD1B
D02:	mov A, R3                     ;27
D03:	mov R2, A                     ;24
D04:	mov A, 0x0                    ;70
D05:	mov R3, A                     ;26
D06:	inc R0                        ;10
D07:	jmp CFC                       ;ECFC
D09:	db 0x21                       ;21
D0A:	db 0x31                       ;31
D0B:	db 0xBC                       ;BC
D0C:	db 0xFC                       ;FC
D0D:	db 0xCC                       ;CC
D0E:	db 0xFC                       ;FC
D0F:	db 0x19                       ;19
D10:	db 0xA4                       ;A4
D11:	db 0xFC                       ;FC
D12:	db 0xDD                       ;DD
D13:	db 0x1B                       ;1B
D14:	db 0x5E                       ;5E
D15:	db 0x01                       ;01
D16:	db 0x79                       ;79
D17:	db 0x1B                       ;1B
D18:	db 0xB5                       ;B5
D19:	db 0x1B                       ;1B
D1A:	db 0x0C                       ;0C
D1B:	mov R1R0, 0xB9                ;590B
D1D:	mov A, 0x7                    ;77
D1E:	and [R1R0], A                 ;1D
D1F:	mov R3R2, 0x4C                ;6C04
D21:	jmp D29                       ;ED29
D23:	mov R1R0, 0xB9                ;590B
D25:	mov A, 0x8                    ;78
D26:	or [R1R0], A                  ;1F
D27:	mov R3R2, 0x8C                ;6C08
D29:	mov R1R0, 0xC5                ;550C
D2B:	mov A, 0x8                    ;78
D2C:	or [R1R0], A                  ;1F
D2D:	mov R1R0, 0x57                ;5705
D2F:	mov A, 0x0                    ;70
D30:	mov [R1R0], A                 ;05
D31:	mov R1R0, 0x0B                ;5B00
D33:	mov [R1R0], A                 ;05
D34:	mov R4, A                     ;28
D35:	mov A, 0xF                    ;7F
D36:	mov R1R0, 0x03                ;5300
D38:	readf MR0A                    ;4F
D39:	dec R0                        ;11
D3A:	mov [R1R0], A                 ;05
D3B:	mov A, 0x4                    ;74
D3C:	mov R4, A                     ;28
D3D:	mov R1R0, 0x1D                ;5D01
D3F:	mov [R1R0], A                 ;05
D40:	mov R1R0, 0x2C                ;5C02
D42:	mov A, [R3R2]                 ;06
D43:	mov [R1R0], A                 ;05
D44:	inc R0                        ;10
D45:	inc R2                        ;14
D46:	jnz R0, D42                   ;A542
D48:	dec R0                        ;11
D49:	mov A, [R1R0]                 ;04
D4A:	jnz A, D51                    ;BD51
D4C:	mov A, 0xA                    ;7A
D4D:	mov [R1R0], A                 ;05
D4E:	dec R4                        ;19
D4F:	jnz R4, D48                   ;DD48
D51:	mov A, 0x7                    ;77
D52:	mov R1R0, 0x05                ;5500
D54:	mov [R1R0], A                 ;05
D55:	mov R3R2, 0x2C                ;6C02
D57:	mov A, [R3R2]                 ;06
D58:	inc A                         ;31
D59:	mov R4, A                     ;28
D5A:	mov A, 0xF                    ;7F
D5B:	mov R1R0, 0x0D                ;5D00
D5D:	readf MR0A                    ;4F
D5E:	dec R0                        ;11
D5F:	mov [R1R0], A                 ;05
D60:	jmp B28                       ;EB28
D62:	inc R2                        ;14
D63:	mov R1R0, 0x1D                ;5D01
D65:	dec [R1R0]                    ;0D
D66:	mov A, [R1R0]                 ;04
D67:	jnz A, D57                    ;BD57
D69:	ret                           ;2E
D6A:	mov R1R0, 0xBD                ;5D0B
D6C:	mov A, 0x7                    ;77
D6D:	and [R1R0], A                 ;1D
D6E:	mov R1R0, 0xB5                ;550B
D70:	mov A, 0x8                    ;78
D71:	or [R1R0], A                  ;1F
D72:	mov R3R2, 0x47                ;6704
D74:	jmp D80                       ;ED80
D76:	mov R1R0, 0xB5                ;550B
D78:	mov A, 0x7                    ;77
D79:	and [R1R0], A                 ;1D
D7A:	mov R1R0, 0xBD                ;5D0B
D7C:	mov A, 0x8                    ;78
D7D:	or [R1R0], A                  ;1F
D7E:	mov R3R2, 0x46                ;6604
D80:	mov R1R0, 0x57                ;5705
D82:	mov A, 0x0                    ;70
D83:	mov [R1R0], A                 ;05
D84:	mov R1R0, 0x0B                ;5B00
D86:	mov [R1R0], A                 ;05
D87:	mov R1R0, 0x02                ;5200
D89:	mov A, 0xB                    ;7B
D8A:	mov [R1R0], A                 ;05
D8B:	inc R0                        ;10
D8C:	mov A, 0x6                    ;76
D8D:	mov [R1R0], A                 ;05
D8E:	mov A, 0x1                    ;71
D8F:	jmp D3D                       ;ED3D
D91:	mov R1R0, 0x57                ;5705
D93:	mov A, 0x3                    ;73
D94:	mov [R1R0], A                 ;05
D95:	mov R1R0, 0x0B                ;5B00
D97:	mov [R1R0], A                 ;05
D98:	mov A, 0xC                    ;7C
D99:	mov R3R2, 0x31                ;6103
D9B:	mov [R3R2], A                 ;07
D9C:	mov A, 0x1                    ;71
D9D:	mov R1R0, 0x22                ;5202
D9F:	mov [R1R0], A                 ;05
DA0:	mov R1R0, 0x0E                ;5E00
DA2:	mov A, 0x0                    ;70
DA3:	mov [R1R0], A                 ;05
DA4:	dec R0                        ;11
DA5:	mov A, R0                     ;21
DA6:	ja2 DA2                       ;95A2
DA8:	dec [R3R2]                    ;0F
DA9:	mov R1R0, 0x05                ;5500
DAB:	mov A, 0xA                    ;7A
DAC:	mov [R1R0], A                 ;05
DAD:	jmp B28                       ;EB28
DAF:	db 0x50                       ;50
DB0:	db 0x08                       ;08
DB1:	db 0x04                       ;04
DB2:	db 0x3F                       ;3F
DB3:	mov R3R2, 0x30                ;6003
DB5:	mov [R3R2], A                 ;07
DB6:	inc R2                        ;14
DB7:	mov A, 0x0                    ;70
DB8:	mov [R3R2], A                 ;07
DB9:	mov A, 0x3                    ;73
DBA:	mov R1R0, 0x0B                ;5B00
DBC:	mov [R1R0], A                 ;05
DBD:	mov R1R0, 0x57                ;5705
DBF:	mov [R1R0], A                 ;05
DC0:	mov R1R0, 0x05                ;5500
DC2:	mov A, 0xC                    ;7C
DC3:	mov [R1R0], A                 ;05
DC4:	dec R0                        ;11
DC5:	mov [R1R0], A                 ;05
DC6:	mov R1R0, 0x1D                ;5D01
DC8:	mov A, 0x0                    ;70
DC9:	mov [R1R0], A                 ;05
DCA:	mov R1R0, 0x5B                ;5B05
DCC:	mov A, 0x2                    ;72
DCD:	mov [R1R0], A                 ;05
DCE:	mov A, 0x4                    ;74
DCF:	jtmr C15                      ;D415
DD1:	jmp 5A0                       ;E5A0
DD3:	mov A, R4                     ;29
DD4:	and A, [R1R0]                 ;1A
DD5:	clc                           ;2A
DD6:	jz A, DD9                     ;B5D9
DD8:	stc                           ;2B
DD9:	mov R1R0, 0x0C                ;5C00
DDB:	mov A, [R1R0]                 ;04
DDC:	rlc A                         ;03
DDD:	mov [R1R0], A                 ;05
DDE:	inc R0                        ;10
DDF:	jnz R0, DDB                   ;A5DB
DE1:	mov R1R0, 0x31                ;5103
DE3:	inc [R1R0]                    ;0C
DE4:	mov R1R0, 0x04                ;5400
DE6:	dec [R1R0]                    ;0D
DE7:	mov A, [R1R0]                 ;04
DE8:	jnz A, DCE                    ;BDCE
DEA:	ret                           ;2E
DEB:	mov A, TMRL                   ;3A
DEC:	and A, 0x5                    ;4205
DEE:	jnz A, DF1                    ;BDF1
DF0:	inc A                         ;31
DF1:	mov R1R0, 0x4A                ;5A04
DF3:	mov [R1R0], A                 ;05
DF4:	ret                           ;2E
DF5:	mov R1R0, 0x5C                ;5C05
DF7:	mov A, 0xF                    ;7F
DF8:	xor [R1R0], A                 ;1E
DF9:	mov A, [R1R0]                 ;04
DFA:	jz A, AA8                     ;B2A8
DFC:	call C97                      ;FC97
DFE:	mov R1R0, 0x45                ;5504
E00:	mov A, [R1R0]                 ;04
E01:	ja0 E07                       ;8607
E03:	call D76                      ;FD76
E05:	jmp E09                       ;EE09
E07:	call D6A                      ;FD6A
E09:	call E0D                      ;FE0D
E0B:	jmp DFC                       ;EDFC
E0D:	mov R1R0, 0x5C                ;5C05
E0F:	mov A, [R1R0]                 ;04
E10:	ja3 E13                       ;9E13
E12:	ret                           ;2E
E13:	mov R1R0, 0x9F                ;5F09
E15:	mov A, 0x6                    ;76
E16:	add A, [R1R0]                 ;09
E17:	jc E27                        ;C627
E19:	ret                           ;2E
E1A:	mov R1R0, 0xC0                ;500C
E1C:	in A, PP                      ;34
E1D:	xor A, 0xF                    ;430F
E1F:	ja1 E1A                       ;8E1A
E21:	inc R0                        ;10
E22:	jnz R0, E1C                   ;A61C
E24:	inc R1                        ;12
E25:	jnz R1, E1C                   ;AE1C
E27:	halt                          ;37
E28:	nop                           ;3E
E29:	call 621                      ;F621
E2B:	mov R1R0, 0x5C                ;5C05
E2D:	mov A, [R1R0]                 ;04
E2E:	jnz A, DFC                    ;BDFC
E30:	mov A, 0x0                    ;70
E31:	mov R1R0, 0x24                ;5402
E33:	mov [R1R0], A                 ;05
E34:	mov R1R0, 0x46                ;5604
E36:	mov [R1R0], A                 ;05
E37:	mov R1R0, 0x5D                ;5D05
E39:	mov [R1R0], A                 ;05
E3A:	mov R1R0, 0x70                ;5007
E3C:	mov [R1R0], A                 ;05
E3D:	inc A                         ;31
E3E:	mov R1R0, 0x40                ;5004
E40:	mov [R1R0], A                 ;05
E41:	call 529                      ;F529
E43:	jmp 6E9                       ;E6E9
E45:	mov R3R2, 0x8F                ;6F08
E47:	mov R1R0, 0x4F                ;5F04
E49:	clc                           ;2A
E4A:	mov A, [R3R2]                 ;06
E4B:	sub A, [R1R0]                 ;0B
E4C:	jc E59                        ;C659
E4E:	mov R3R2, 0x8C                ;6C08
E50:	mov R1R0, 0x4C                ;5C04
E52:	mov A, [R1R0]                 ;04
E53:	mov [R3R2], A                 ;07
E54:	inc R0                        ;10
E55:	inc R2                        ;14
E56:	jnz R0, E52                   ;A652
E58:	ret                           ;2E
E59:	dec R0                        ;11
E5A:	dec R2                        ;15
E5B:	jz A, E4A                     ;B64A
E5D:	ret                           ;2E
E5E:	mov R1R0, 0x62                ;5206
E60:	mov A, [R1R0]                 ;04
E61:	jnz A, E7C                    ;BE7C
E63:	mov R1R0, 0x71                ;5107
E65:	mov A, [R1R0]                 ;04
E66:	jnz A, E9F                    ;BE9F
E68:	mov A, 0xF                    ;7F
E69:	mov R1R0, 0x61                ;5106
E6B:	add A, [R1R0]                 ;09
E6C:	jnc E9F                       ;CE9F
E6E:	mov A, 0x0                    ;70
E6F:	mov [R1R0], A                 ;05
E70:	mov R1R0, 0x54                ;5405
E72:	mov A, 0x2                    ;72
E73:	mov [R1R0], A                 ;05
E74:	mov R1R0, 0x71                ;5107
E76:	mov A, TMRL                   ;3A
E77:	or A, 0x8                     ;4408
E79:	mov [R1R0], A                 ;05
E7A:	jmp 859                       ;E859
E7C:	mov R1R0, 0x63                ;5306
E7E:	mov A, [R1R0]                 ;04
E7F:	add A, 0xC                    ;400C
E81:	jnc E9F                       ;CE9F
E83:	mov A, 0x0                    ;70
E84:	mov [R1R0], A                 ;05
E85:	mov R1R0, 0x71                ;5107
E87:	mov A, [R1R0]                 ;04
E88:	jz A, E8B                     ;B68B
E8A:	inc [R1R0]                    ;0C
E8B:	mov R1R0, 0x53                ;5305
E8D:	mov A, [R1R0]                 ;04
E8E:	mov R1R0, 0x31                ;5103
E90:	mov [R1R0], A                 ;05
E91:	call 57E                      ;F57E
E93:	mov R1R0, 0x53                ;5305
E95:	mov A, [R1R0]                 ;04
E96:	jz A, EA1                     ;B6A1
E98:	dec [R1R0]                    ;0D
E99:	mov A, [R1R0]                 ;04
E9A:	mov R1R0, 0x31                ;5103
E9C:	mov [R1R0], A                 ;05
E9D:	call 582                      ;F582
E9F:	jmp 1AA                       ;E1AA
EA1:	mov R1R0, 0x62                ;5206
EA3:	mov A, 0x0                    ;70
EA4:	mov [R1R0], A                 ;05
EA5:	mov R1R0, 0x71                ;5107
EA7:	mov [R1R0], A                 ;05
EA8:	mov R3R2, 0x52                ;6205
EAA:	inc [R3R2]                    ;0E
EAB:	mov A, [R3R2]                 ;06
EAC:	mov R1R0, 0x86                ;5608
EAE:	xor A, [R1R0]                 ;1B
EAF:	jz A, EBC                     ;B6BC
EB1:	inc R0                        ;10
EB2:	mov A, [R3R2]                 ;06
EB3:	xor A, [R1R0]                 ;1B
EB4:	jz A, EBC                     ;B6BC
EB6:	mov A, [R3R2]                 ;06
EB7:	mov R1R0, 0x80                ;5008
EB9:	xor A, [R1R0]                 ;1B
EBA:	jz A, 9C9                     ;B1C9
EBC:	mov A, 0x0                    ;70
EBD:	mov [R3R2], A                 ;07
EBE:	inc R2                        ;14
EBF:	mov [R3R2], A                 ;07
EC0:	jmp E9F                       ;EE9F
EC2:	db 0x3E                       ;3E
EC3:	db 0x3E                       ;3E
EC4:	db 0x3E                       ;3E
EC5:	db 0x3E                       ;3E
EC6:	db 0x3E                       ;3E
EC7:	db 0x3E                       ;3E
EC8:	db 0x3E                       ;3E
EC9:	db 0x3E                       ;3E
ECA:	db 0x3E                       ;3E
ECB:	db 0x3E                       ;3E
ECC:	db 0x3E                       ;3E
ECD:	db 0x3E                       ;3E
ECE:	db 0x3E                       ;3E
ECF:	db 0x3E                       ;3E
ED0:	db 0x3E                       ;3E
ED1:	db 0x3E                       ;3E
ED2:	db 0x3E                       ;3E
ED3:	db 0x3E                       ;3E
ED4:	db 0x3E                       ;3E
ED5:	db 0x3E                       ;3E
ED6:	db 0x3E                       ;3E
ED7:	db 0x3E                       ;3E
ED8:	db 0x3E                       ;3E
ED9:	db 0x3E                       ;3E
EDA:	db 0x3E                       ;3E
EDB:	db 0x3E                       ;3E
EDC:	db 0x3E                       ;3E
EDD:	db 0x3E                       ;3E
EDE:	db 0x3E                       ;3E
EDF:	db 0x3E                       ;3E
EE0:	db 0x3E                       ;3E
EE1:	db 0x3E                       ;3E
EE2:	db 0x3E                       ;3E
EE3:	db 0x3E                       ;3E
EE4:	db 0x3E                       ;3E
EE5:	db 0x3E                       ;3E
EE6:	db 0x3E                       ;3E
EE7:	db 0x3E                       ;3E
EE8:	db 0x3E                       ;3E
EE9:	db 0x3E                       ;3E
EEA:	db 0x3E                       ;3E
EEB:	db 0x3E                       ;3E
EEC:	db 0x3E                       ;3E
EED:	db 0x3E                       ;3E
EEE:	db 0x3E                       ;3E
EEF:	db 0x3E                       ;3E
EF0:	db 0x3E                       ;3E
EF1:	db 0x3E                       ;3E
EF2:	db 0x3E                       ;3E
EF3:	db 0x3E                       ;3E
EF4:	db 0x3E                       ;3E
EF5:	db 0x3E                       ;3E
EF6:	db 0x3E                       ;3E
EF7:	db 0x3E                       ;3E
EF8:	db 0x3E                       ;3E
EF9:	db 0x3E                       ;3E
EFA:	db 0x3E                       ;3E
EFB:	db 0x3E                       ;3E
EFC:	db 0x3E                       ;3E
EFD:	db 0x3E                       ;3E
EFE:	db 0x3E                       ;3E
EFF:	db 0x3E                       ;3E
F00:	db 0xF8                       ;F8
F01:	db 0xF4                       ;F4
F02:	db 0xF0                       ;F0
F03:	db 0xEC                       ;EC
F04:	db 0xE8                       ;E8
F05:	db 0xE4                       ;E4
F06:	db 0xE0                       ;E0
F07:	db 0xDC                       ;DC
F08:	db 0xD8                       ;D8
F09:	db 0xD4                       ;D4
F0A:	db 0xD0                       ;D0
F0B:	db 0xCC                       ;CC
F0C:	db 0xC8                       ;C8
F0D:	db 0x3E                       ;3E
F0E:	db 0x3E                       ;3E
F0F:	db 0x3E                       ;3E
F10:	db 0xC4                       ;C4
F11:	db 0xC2                       ;C2
F12:	db 0xC0                       ;C0
F13:	db 0xBE                       ;BE
F14:	db 0xBC                       ;BC
F15:	db 0xBA                       ;BA
F16:	db 0xB8                       ;B8
F17:	db 0xB6                       ;B6
F18:	db 0xB4                       ;B4
F19:	db 0xB2                       ;B2
F1A:	db 0xB0                       ;B0
F1B:	db 0xB1                       ;B1
F1C:	db 0xB3                       ;B3
F1D:	db 0x2E                       ;2E
F1E:	db 0x6E                       ;6E
F1F:	db 0xAE                       ;AE
F20:	db 0xEE                       ;EE
F21:	db 0x2F                       ;2F
F22:	db 0x6F                       ;6F
F23:	db 0xAF                       ;AF
F24:	db 0xEF                       ;EF
F25:	db 0x16                       ;16
F26:	db 0x96                       ;96
F27:	db 0x2C                       ;2C
F28:	db 0x6C                       ;6C
F29:	db 0xAC                       ;AC
F2A:	db 0xEC                       ;EC
F2B:	db 0x2D                       ;2D
F2C:	db 0x6D                       ;6D
F2D:	db 0xAD                       ;AD
F2E:	db 0xED                       ;ED
F2F:	db 0x56                       ;56
F30:	db 0xD6                       ;D6
F31:	db 0x18                       ;18
F32:	db 0x58                       ;58
F33:	db 0x98                       ;98
F34:	db 0xD8                       ;D8
F35:	db 0x19                       ;19
F36:	db 0x59                       ;59
F37:	db 0x99                       ;99
F38:	db 0xD9                       ;D9
F39:	db 0x43                       ;43
F3A:	db 0xC3                       ;C3
F3B:	db 0x3E                       ;3E
F3C:	db 0x3E                       ;3E
F3D:	db 0x3E                       ;3E
F3E:	db 0x3E                       ;3E
F3F:	db 0x3E                       ;3E
F40:	db 0x0A                       ;0A
F41:	db 0x1A                       ;1A
F42:	db 0x2A                       ;2A
F43:	db 0x09                       ;09
F44:	db 0x19                       ;19
F45:	db 0x29                       ;29
F46:	db 0x08                       ;08
F47:	db 0x18                       ;18
F48:	db 0x28                       ;28
F49:	db 0xD7                       ;D7
F4A:	db 0x97                       ;97
F4B:	db 0x57                       ;57
F4C:	db 0x17                       ;17
F4D:	db 0x15                       ;15
F4E:	db 0x95                       ;95
F4F:	db 0x55                       ;55
F50:	db 0xD3                       ;D3
F51:	db 0x93                       ;93
F52:	db 0x53                       ;53
F53:	db 0x13                       ;13
F54:	db 0x11                       ;11
F55:	db 0x91                       ;91
F56:	db 0x51                       ;51
F57:	db 0xCF                       ;CF
F58:	db 0x8F                       ;8F
F59:	db 0x4F                       ;4F
F5A:	db 0x0F                       ;0F
F5B:	db 0x0D                       ;0D
F5C:	db 0x8D                       ;8D
F5D:	db 0x4D                       ;4D
F5E:	db 0xCB                       ;CB
F5F:	db 0x8B                       ;8B
F60:	db 0x4B                       ;4B
F61:	db 0x0B                       ;0B
F62:	db 0x09                       ;09
F63:	db 0x89                       ;89
F64:	db 0x49                       ;49
F65:	db 0xC7                       ;C7
F66:	db 0x87                       ;87
F67:	db 0x47                       ;47
F68:	db 0x07                       ;07
F69:	db 0x05                       ;05
F6A:	db 0x85                       ;85
F6B:	db 0x45                       ;45
F6C:	mov A, [R1R0]                 ;04
F6D:	dec R0                        ;11
F6E:	read R4A                      ;4C
F6F:	mov R0, A                     ;20
F70:	mov A, R4                     ;29
F71:	or A, 0xC                     ;440C
F73:	mov R1, A                     ;22
F74:	dec R1                        ;13
F75:	mov R3R2, 0x57                ;6705
F77:	mov A, [R3R2]                 ;06
F78:	jmp BE5                       ;EBE5
F7A:	mov R1R0, 0x3B                ;5B03
F7C:	mov A, [R1R0]                 ;04
F7D:	mov R1R0, 0x3A                ;5A03
F7F:	read R4A                      ;4C
F80:	mov R1R0, 0x0C                ;5C00
F82:	mov [R1R0], A                 ;05
F83:	inc R0                        ;10
F84:	mov A, R4                     ;29
F85:	mov [R1R0], A                 ;05
F86:	jmp 0A1                       ;E0A1
F88:	db 0x3E                       ;3E
F89:	db 0x3E                       ;3E
F8A:	db 0x3E                       ;3E
F8B:	db 0x3E                       ;3E
F8C:	db 0x3E                       ;3E
F8D:	db 0x3E                       ;3E
F8E:	db 0x3E                       ;3E
F8F:	db 0x3E                       ;3E
F90:	db 0x3E                       ;3E
F91:	db 0x3E                       ;3E
F92:	db 0x3E                       ;3E
F93:	db 0x3E                       ;3E
F94:	db 0x3E                       ;3E
F95:	db 0x3E                       ;3E
F96:	db 0x3E                       ;3E
F97:	db 0x3E                       ;3E
F98:	db 0x3E                       ;3E
F99:	db 0x3E                       ;3E
F9A:	db 0x3E                       ;3E
F9B:	db 0x3E                       ;3E
F9C:	db 0x3E                       ;3E
F9D:	db 0x3E                       ;3E
F9E:	db 0x3E                       ;3E
F9F:	db 0x3E                       ;3E
FA0:	db 0x40                       ;40
FA1:	db 0x00                       ;00
FA2:	db 0x12                       ;12
FA3:	db 0x40                       ;40
FA4:	db 0x08                       ;08
FA5:	db 0x08                       ;08
FA6:	db 0x01                       ;01
FA7:	db 0x90                       ;90
FA8:	db 0x04                       ;04
FA9:	db 0x40                       ;40
FAA:	db 0x00                       ;00
FAB:	db 0x24                       ;24
FAC:	db 0x10                       ;10
FAD:	db 0x44                       ;44
FAE:	db 0x11                       ;11
FAF:	db 0x01                       ;01
FB0:	db 0x10                       ;10
FB1:	db 0x04                       ;04
FB2:	db 0x10                       ;10
FB3:	db 0x85                       ;85
FB4:	db 0x20                       ;20
FB5:	db 0x04                       ;04
FB6:	db 0x80                       ;80
FB7:	db 0x12                       ;12
FB8:	db 0x00                       ;00
FB9:	db 0x24                       ;24
FBA:	db 0x01                       ;01
FBB:	db 0x08                       ;08
FBC:	db 0x20                       ;20
FBD:	db 0x10                       ;10
FBE:	db 0x40                       ;40
FBF:	db 0x04                       ;04
FC0:	db 0x03                       ;03
FC1:	db 0x04                       ;04
FC2:	db 0x04                       ;04
FC3:	db 0x00                       ;00
FC4:	db 0x00                       ;00
FC5:	db 0x00                       ;00
FC6:	db 0x00                       ;00
FC7:	db 0x00                       ;00
FC8:	db 0x01                       ;01
FC9:	db 0x3E                       ;3E
FCA:	db 0x3E                       ;3E
FCB:	db 0x3E                       ;3E
FCC:	db 0x3E                       ;3E
FCD:	db 0x3E                       ;3E
FCE:	db 0x3E                       ;3E
FCF:	db 0x3E                       ;3E
FD0:	db 0x00                       ;00
FD1:	db 0x02                       ;02
FD2:	db 0x02                       ;02
FD3:	db 0x01                       ;01
FD4:	db 0x00                       ;00
FD5:	db 0x00                       ;00
FD6:	db 0x01                       ;01
FD7:	db 0x01                       ;01
FD8:	db 0x74                       ;74
FD9:	db 0x74                       ;74
FDA:	db 0x05                       ;05
FDB:	db 0x00                       ;00
FDC:	db 0x00                       ;00
FDD:	db 0x3E                       ;3E
FDE:	db 0x3E                       ;3E
FDF:	db 0x3E                       ;3E
FE0:	db 0x01                       ;01
FE1:	db 0x02                       ;02
FE2:	db 0x04                       ;04
FE3:	db 0x08                       ;08
FE4:	db 0x01                       ;01
FE5:	db 0x02                       ;02
FE6:	db 0x04                       ;04
FE7:	db 0x08                       ;08
FE8:	db 0x1D                       ;1D
FE9:	db 0x27                       ;27
FEA:	db 0x31                       ;31
FEB:	db 0x0B                       ;0B
FEC:	db 0x0C                       ;0C
FED:	db 0x0F                       ;0F
FEE:	db 0x3E                       ;3E
FEF:	db 0x3E                       ;3E
FF0:	db 0x4F                       ;4F
FF1:	db 0x7E                       ;7E
FF2:	db 0x30                       ;30
FF3:	db 0x6D                       ;6D
FF4:	db 0x79                       ;79
FF5:	db 0x33                       ;33
FF6:	db 0x5B                       ;5B
FF7:	db 0x5F                       ;5F
FF8:	db 0x70                       ;70
FF9:	db 0x7F                       ;7F
FFA:	db 0x7B                       ;7B
FFB:	db 0x00                       ;00
FFC:	db 0x10                       ;10
FFD:	db 0x22                       ;22
FFE:	db 0x46                       ;46
FFF:	db 0x87                       ;87
