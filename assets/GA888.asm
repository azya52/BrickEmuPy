001:	timer on                      ;38
002:	mov A, 0xE                    ;7E
003:	out PA, A                     ;30
004:	mov R1R0, 0xFF                ;5F0F
006:	in A, PP                      ;34
007:	ja0 04C                       ;804C
009:	mov A, 0xF                    ;7F
00A:	call E67                      ;FE67
00C:	jmp 002                       ;E002
00E:	mov A, TMRL                   ;3A
00F:	mov R1R0, 0x0C                ;5C00
011:	mov [R1R0], A                 ;05
012:	inc R0                        ;10
013:	mov A, TMRL                   ;3A
014:	mov [R1R0], A                 ;05
015:	inc R0                        ;10
016:	mov A, TMRL                   ;3A
017:	mov [R1R0], A                 ;05
018:	jmp 968                       ;E968
01A:	db 0x7C                       ;7C
01B:	db 0x00                       ;00
01C:	db 0x42                       ;42
01D:	db 0x44                       ;44
01E:	db 0x1C                       ;1C
01F:	db 0xE4                       ;E4
020:	db 0x7C                       ;7C
021:	db 0x80                       ;80
022:	db 0x6C                       ;6C
023:	db 0x64                       ;64
024:	db 0x82                       ;82
025:	db 0x42                       ;42
026:	db 0x86                       ;86
027:	db 0x92                       ;92
028:	db 0x24                       ;24
029:	db 0xA2                       ;A2
02A:	db 0x92                       ;92
02B:	db 0x86                       ;86
02C:	db 0x92                       ;92
02D:	db 0x92                       ;92
02E:	db 0x82                       ;82
02F:	db 0xFE                       ;FE
030:	db 0x8A                       ;8A
031:	db 0x92                       ;92
032:	db 0x44                       ;44
033:	db 0xA2                       ;A2
034:	db 0x92                       ;92
035:	db 0x98                       ;98
036:	db 0x92                       ;92
037:	db 0x92                       ;92
038:	db 0x82                       ;82
039:	db 0x02                       ;02
03A:	db 0x92                       ;92
03B:	db 0x92                       ;92
03C:	db 0xFE                       ;FE
03D:	db 0xA2                       ;A2
03E:	db 0x92                       ;92
03F:	db 0xA0                       ;A0
040:	db 0x92                       ;92
041:	db 0x92                       ;92
042:	db 0x7C                       ;7C
043:	db 0x00                       ;00
044:	db 0x62                       ;62
045:	db 0x6C                       ;6C
046:	db 0x04                       ;04
047:	db 0x9C                       ;9C
048:	db 0x4C                       ;4C
049:	db 0xC0                       ;C0
04A:	db 0x6C                       ;6C
04B:	db 0x7C                       ;7C
04C:	call E66                      ;FE66
04E:	mov R1R0, 0xBB                ;5B0B
050:	inc [R1R0]                    ;0C
051:	mov R1R0, 0xC3                ;530C
053:	inc [R1R0]                    ;0C
054:	mov R1R0, 0xB6                ;560B
056:	mov A, 0xC                    ;7C
057:	mov [R1R0], A                 ;05
058:	inc R0                        ;10
059:	mov A, 0x2                    ;72
05A:	mov [R1R0], A                 ;05
05B:	mov R1R0, 0xC5                ;550C
05D:	or [R1R0], A                  ;1F
05E:	mov R1R0, 0x91                ;5109
060:	inc [R1R0]                    ;0C
061:	call 811                      ;F811
063:	mov R1R0, 0x83                ;5308
065:	mov [R1R0], A                 ;05
066:	call 3BD                      ;F3BD
068:	mov R1R0, 0xB1                ;510B
06A:	mov A, 0x2                    ;72
06B:	or [R1R0], A                  ;1F
06C:	call 7DE                      ;F7DE
06E:	mov R1R0, 0x5D                ;5D05
070:	call E66                      ;FE66
072:	call 811                      ;F811
074:	call E3F                      ;FE3F
076:	call 0F2                      ;F0F2
078:	call AB3                      ;FAB3
07A:	mov R3R2, 0x92                ;6209
07C:	mov A, 0xA                    ;7A
07D:	mov R1R0, 0x33                ;5303
07F:	mov [R1R0], A                 ;05
080:	mov A, [R3R2]                 ;06
081:	inc R0                        ;10
082:	mov [R1R0], A                 ;05
083:	inc R0                        ;10
084:	mov A, 0x1                    ;71
085:	mov [R1R0], A                 ;05
086:	mov A, 0x2                    ;72
087:	call E76                      ;FE76
089:	mov R1R0, 0x33                ;5303
08B:	mov R3R2, 0x31                ;6103
08D:	mov A, [R1R0]                 ;04
08E:	mov [R3R2], A                 ;07
08F:	inc R2                        ;14
090:	mov A, 0x0                    ;70
091:	mov [R3R2], A                 ;07
092:	inc R0                        ;10
093:	call DFA                      ;FDFA
095:	mov A, [R1R0]                 ;04
096:	dec R0                        ;11
097:	read R4A                      ;4C
098:	mov R1R0, 0x36                ;5603
09A:	mov [R1R0], A                 ;05
09B:	mov A, R4                     ;29
09C:	inc R0                        ;10
09D:	mov [R1R0], A                 ;05
09E:	inc R0                        ;10
09F:	mov A, 0x7                    ;77
0A0:	mov [R1R0], A                 ;05
0A1:	mov R1R0, 0x37                ;5703
0A3:	mov A, [R1R0]                 ;04
0A4:	rrc A                         ;02
0A5:	mov [R1R0], A                 ;05
0A6:	dec R0                        ;11
0A7:	mov A, [R1R0]                 ;04
0A8:	rrc A                         ;02
0A9:	mov [R1R0], A                 ;05
0AA:	call 9E5                      ;F9E5
0AC:	call DFD                      ;FDFD
0AE:	mov R1R0, 0x38                ;5803
0B0:	dec [R1R0]                    ;0D
0B1:	mov A, [R1R0]                 ;04
0B2:	jnz A, 0A1                    ;B8A1
0B4:	mov R1R0, 0x30                ;5003
0B6:	inc [R1R0]                    ;0C
0B7:	mov A, 0x7                    ;77
0B8:	xor A, [R1R0]                 ;1B
0B9:	jnz A, 089                    ;B889
0BB:	mov R1R0, 0x33                ;5303
0BD:	mov A, 0x2                    ;72
0BE:	xor A, [R1R0]                 ;1B
0BF:	mov R4, A                     ;28
0C0:	mov R3R2, 0x91                ;6109
0C2:	mov A, 0x2                    ;72
0C3:	jnz R4, 07D                   ;D87D
0C5:	mov A, 0x0                    ;70
0C6:	call B07                      ;FB07
0C8:	call CC5                      ;FCC5
0CA:	mov A, R3                     ;27
0CB:	jz A, 0C5                     ;B0C5
0CD:	mov A, 0x7                    ;77
0CE:	call 7A3                      ;F7A3
0D0:	call 0D4                      ;F0D4
0D2:	jmp 0C5                       ;E0C5
0D4:	mov A, R3                     ;27
0D5:	ja0 0FE                       ;80FE
0D7:	clc                           ;2A
0D8:	ja1 103                       ;8903
0DA:	ja3 0E6                       ;98E6
0DC:	mov R1R0, 0x80                ;5008
0DE:	inc [R1R0]                    ;0C
0DF:	mov A, 0xA                    ;7A
0E0:	xor A, [R1R0]                 ;1B
0E1:	jnz A, 0F2                    ;B8F2
0E3:	mov A, 0x9                    ;79
0E4:	jmp 0EE                       ;E0EE
0E6:	mov R1R0, 0x81                ;5108
0E8:	inc [R1R0]                    ;0C
0E9:	mov A, 0xD                    ;7D
0EA:	xor A, [R1R0]                 ;1B
0EB:	jnz A, 0F2                    ;B8F2
0ED:	mov A, 0xC                    ;7C
0EE:	jc 0F1                        ;C0F1
0F0:	mov A, 0x0                    ;70
0F1:	mov [R1R0], A                 ;05
0F2:	mov R3R2, 0x80                ;6008
0F4:	mov R1R0, 0x02                ;5200
0F6:	mov A, 0xE                    ;7E
0F7:	mov [R1R0], A                 ;05
0F8:	inc R0                        ;10
0F9:	mov A, 0xC                    ;7C
0FA:	mov [R1R0], A                 ;05
0FB:	mov A, 0x2                    ;72
0FC:	jmp B4D                       ;EB4D
0FE:	mov R1R0, 0xB7                ;570B
100:	mov A, 0x3                    ;73
101:	xor [R1R0], A                 ;1E
102:	ret                           ;2E
103:	mov R1R0, 0x90                ;5009
105:	inc [R1R0]                    ;0C
106:	mov A, 0x7                    ;77
107:	and [R1R0], A                 ;1D
108:	inc R0                        ;10
109:	inc [R1R0]                    ;0C
10A:	mov A, [R1R0]                 ;04
10B:	daa                           ;36
10C:	mov [R1R0], A                 ;05
10D:	inc R0                        ;10
10E:	jnc 111                       ;C911
110:	inc [R1R0]                    ;0C
111:	dec R0                        ;11
112:	mov R3R2, 0xA0                ;600A
114:	call 362                      ;F362
116:	jnz R4, 11F                   ;D91F
118:	mov [R1R0], A                 ;05
119:	dec R0                        ;11
11A:	mov A, 0x1                    ;71
11B:	mov [R1R0], A                 ;05
11C:	dec R0                        ;11
11D:	mov A, 0x0                    ;70
11E:	mov [R1R0], A                 ;05
11F:	jmp 07A                       ;E07A
121:	mov R1R0, 0xB1                ;510B
123:	mov A, 0xD                    ;7D
124:	and [R1R0], A                 ;1D
125:	mov R1R0, 0x5D                ;5D05
127:	call E66                      ;FE66
129:	mov R1R0, 0x59                ;5905
12B:	dec [R1R0]                    ;0D
12C:	mov R1R0, 0x50                ;5005
12E:	inc [R1R0]                    ;0C
12F:	inc R0                        ;10
130:	mov A, 0x5                    ;75
131:	mov [R1R0], A                 ;05
132:	call AB3                      ;FAB3
134:	call AF6                      ;FAF6
136:	mov A, 0x8                    ;78
137:	mov R3R2, 0x53                ;6305
139:	mov [R3R2], A                 ;07
13A:	mov R1R0, 0x90                ;5009
13C:	mov A, 0xE                    ;7E
13D:	add A, [R1R0]                 ;09
13E:	jnc 145                       ;C945
140:	mov A, 0xC                    ;7C
141:	add A, [R1R0]                 ;09
142:	jc 520                        ;C520
144:	inc [R3R2]                    ;0E
145:	call 811                      ;F811
147:	mov R3R2, 0xC3                ;630C
149:	mov A, [R3R2]                 ;06
14A:	rrc A                         ;02
14B:	jnc 152                       ;C952
14D:	mov R1R0, 0x59                ;5905
14F:	inc [R1R0]                    ;0C
150:	sound 14                      ;450E
152:	call 822                      ;F822
154:	call 7F4                      ;F7F4
156:	mov R1R0, 0x53                ;5305
158:	mov A, [R1R0]                 ;04
159:	ja0 15D                       ;815D
15B:	call 7F9                      ;F7F9
15D:	mov R1R0, 0x81                ;5108
15F:	mov A, [R1R0]                 ;04
160:	mov R2, A                     ;24
161:	jmp 165                       ;E165
163:	call 00E                      ;F00E
165:	mov A, R2                     ;25
166:	dec R2                        ;15
167:	jnz A, 163                    ;B963
169:	mov R1R0, 0x42                ;5204
16B:	inc [R1R0]                    ;0C
16C:	mov R1R0, 0x85                ;5508
16E:	mov A, 0xE                    ;7E
16F:	and [R1R0], A                 ;1D
170:	mov R1R0, 0x3C                ;5C03
172:	mov R3R2, 0x33                ;6303
174:	call E73                      ;FE73
176:	call 822                      ;F822
178:	call E3F                      ;FE3F
17A:	call E21                      ;FE21
17C:	call E9C                      ;FE9C
17E:	mov R3R2, 0x1C                ;6C01
180:	call E15                      ;FE15
182:	mov A, 0x3                    ;73
183:	call E76                      ;FE76
185:	inc [R1R0]                    ;0C
186:	dec R0                        ;11
187:	dec R2                        ;15
188:	mov A, [R3R2]                 ;06
189:	jnz A, 18F                    ;B98F
18B:	dec R2                        ;15
18C:	inc [R1R0]                    ;0C
18D:	jmp 188                       ;E188
18F:	call E21                      ;FE21
191:	call 874                      ;F874
193:	call E2C                      ;FE2C
195:	call E13                      ;FE13
197:	jnc 22E                       ;CA2E
199:	call 90D                      ;F90D
19B:	mov R1R0, 0xB1                ;510B
19D:	mov A, 0x2                    ;72
19E:	or [R1R0], A                  ;1F
19F:	mov A, 0xA                    ;7A
1A0:	call 7BC                      ;F7BC
1A2:	mov A, 0xD                    ;7D
1A3:	call 7A9                      ;F7A9
1A5:	call D98                      ;FD98
1A7:	call 7F9                      ;F7F9
1A9:	call 808                      ;F808
1AB:	mov R1R0, 0x0A                ;5A00
1AD:	mov A, 0xF                    ;7F
1AE:	xor A, [R1R0]                 ;1B
1AF:	call 962                      ;F962
1B1:	mov R1R0, 0x00                ;5000
1B3:	mov R3R2, 0x10                ;6001
1B5:	call E17                      ;FE17
1B7:	mov R3R2, 0x3F                ;6F03
1B9:	inc [R3R2]                    ;0E
1BA:	mov R3R2, 0x1E                ;6E01
1BC:	mov R1R0, 0x58                ;5805
1BE:	mov A, 0x3                    ;73
1BF:	add A, [R1R0]                 ;09
1C0:	jz A, 1CB                     ;B1CB
1C2:	mov R3R2, 0x08                ;6800
1C4:	inc A                         ;31
1C5:	jnz A, 1CB                    ;B9CB
1C7:	jmp 2FE                       ;E2FE
1C9:	mov R3R2, 0x18                ;6801
1CB:	jmp 389                       ;E389
1CD:	mov R1R0, 0x10                ;5001
1CF:	mov R3R2, 0x00                ;6000
1D1:	call E17                      ;FE17
1D3:	mov R1R0, 0x03                ;5300
1D5:	mov A, 0x3                    ;73
1D6:	add A, [R1R0]                 ;09
1D7:	jnc 1A9                       ;C9A9
1D9:	dec [R1R0]                    ;0D
1DA:	dec R0                        ;11
1DB:	mov A, 0x7                    ;77
1DC:	mov [R1R0], A                 ;05
1DD:	mov R1R0, 0x0A                ;5A00
1DF:	mov A, 0xF                    ;7F
1E0:	xor [R1R0], A                 ;1E
1E1:	mov A, [R1R0]                 ;04
1E2:	jnz A, 1F5                    ;B9F5
1E4:	mov R1R0, 0x58                ;5805
1E6:	mov A, 0xD                    ;7D
1E7:	xor A, [R1R0]                 ;1B
1E8:	jz A, 06E                     ;B06E
1EA:	mov R1R0, 0x53                ;5305
1EC:	mov A, [R1R0]                 ;04
1ED:	ja1 68E                       ;8E8E
1EF:	ja2 530                       ;9530
1F1:	call DA1                      ;FDA1
1F3:	jmp 154                       ;E154
1F5:	mov R1R0, 0x58                ;5805
1F7:	mov A, 0x4                    ;74
1F8:	add A, [R1R0]                 ;09
1F9:	clc                           ;2A
1FA:	jz A, 219                     ;B219
1FC:	dec A                         ;3F
1FD:	mov R4, A                     ;28
1FE:	mov A, 0x4                    ;74
1FF:	jnz R4, 223                   ;DA23
201:	mov R1R0, 0x90                ;5009
203:	mov A, [R1R0]                 ;04
204:	mov R3R2, 0x7C                ;6C07
206:	ja2 209                       ;9209
208:	inc R3                        ;16
209:	mov R1R0, 0x4C                ;5C04
20B:	stc                           ;2B
20C:	mov A, [R3R2]                 ;06
20D:	sbc A, [R1R0]                 ;0A
20E:	inc R0                        ;10
20F:	inc R2                        ;14
210:	jnz R0, 20C                   ;A20C
212:	jc 219                        ;C219
214:	mov A, 0x8                    ;78
215:	mov R0, A                     ;20
216:	mov R2, A                     ;24
217:	call E18                      ;FE18
219:	mov A, 0xE                    ;7E
21A:	jnc 223                       ;CA23
21C:	clc                           ;2A
21D:	mov R1R0, 0x4F                ;5F04
21F:	mov A, [R1R0]                 ;04
220:	jnz A, 219                    ;BA19
222:	mov A, 0xC                    ;7C
223:	call 7BC                      ;F7BC
225:	jmp 1A9                       ;E1A9
227:	call E13                      ;FE13
229:	call EFA                      ;FEFA
22B:	mov R1R0, 0x0B                ;5B00
22D:	inc [R1R0]                    ;0C
22E:	call 90D                      ;F90D
230:	mov R1R0, 0x59                ;5905
232:	mov A, [R1R0]                 ;04
233:	ja2 244                       ;9244
235:	call CC5                      ;FCC5
237:	mov R1R0, 0x9A                ;5A09
239:	mov A, 0x6                    ;76
23A:	add A, [R1R0]                 ;09
23B:	jnc 230                       ;CA30
23D:	mov R1R0, 0x59                ;5905
23F:	dec [R1R0]                    ;0D
240:	mov R3R2, 0xF6                ;660F
242:	call 793                      ;F793
244:	mov R1R0, 0x80                ;5008
246:	mov A, 0xF                    ;7F
247:	xor A, [R1R0]                 ;1B
248:	mov R3, A                     ;26
249:	mov R1R0, 0x53                ;5305
24B:	mov A, 0x6                    ;76
24C:	and A, [R1R0]                 ;1A
24D:	jz A, 255                     ;B255
24F:	ja1 255                       ;8A55
251:	mov A, 0x0                    ;70
252:	mov R2, A                     ;24
253:	jmp 389                       ;E389
255:	mov A, R3                     ;27
256:	sub A, 0x5                    ;4105
258:	clc                           ;2A
259:	rrc A                         ;02
25A:	mov R3, A                     ;26
25B:	mov A, 0x0                    ;70
25C:	rrc A                         ;02
25D:	mov R2, A                     ;24
25E:	jmp 389                       ;E389
260:	mov R1R0, 0x53                ;5305
262:	mov A, [R1R0]                 ;04
263:	ja1 6C3                       ;8EC3
265:	ja2 56D                       ;956D
267:	call E21                      ;FE21
269:	call E07                      ;FE07
26B:	mov R1R0, 0x0B                ;5B00
26D:	inc [R1R0]                    ;0C
26E:	call 874                      ;F874
270:	mov R1R0, 0x44                ;5404
272:	mov R3R2, 0x2D                ;6D02
274:	call E17                      ;FE17
276:	mov R3R2, 0x10                ;6001
278:	call E15                      ;FE15
27A:	call E2C                      ;FE2C
27C:	jnc 227                       ;CA27
27E:	call E21                      ;FE21
280:	mov R1R0, 0x3F                ;5F03
282:	mov A, [R1R0]                 ;04
283:	ja3 28B                       ;9A8B
285:	mov A, 0x8                    ;78
286:	or [R1R0], A                  ;1F
287:	mov R3R2, 0x32                ;6203
289:	jmp 389                       ;E389
28B:	xor [R1R0], A                 ;1E
28C:	mov A, 0x3                    ;73
28D:	call 7A9                      ;F7A9
28F:	mov R1R0, 0x15                ;5501
291:	mov A, [R1R0]                 ;04
292:	xor [R1R0], A                 ;1E
293:	call 7F9                      ;F7F9
295:	call 9FA                      ;F9FA
297:	dec R4                        ;19
298:	jnz R4, 2D7                   ;DAD7
29A:	mov A, 0xB                    ;7B
29B:	call 7A9                      ;F7A9
29D:	call 7F9                      ;F7F9
29F:	call 9FA                      ;F9FA
2A1:	dec R4                        ;19
2A2:	mov A, R4                     ;29
2A3:	jz A, 2A9                     ;B2A9
2A5:	call 968                      ;F968
2A7:	jmp 29F                       ;E29F
2A9:	call 35A                      ;F35A
2AB:	mov A, R4                     ;29
2AC:	mov R3R2, 0x14                ;6401
2AE:	mov [R3R2], A                 ;07
2AF:	mov A, 0xA                    ;7A
2B0:	mov R2, A                     ;24
2B1:	call 961                      ;F961
2B3:	mov R1R0, 0x02                ;5200
2B5:	call E0C                      ;FE0C
2B7:	mov A, R2                     ;25
2B8:	dec R2                        ;15
2B9:	jnz A, 2B1                    ;BAB1
2BB:	call 9FA                      ;F9FA
2BD:	call 968                      ;F968
2BF:	call 35E                      ;F35E
2C1:	jc 2BB                        ;C2BB
2C3:	call 961                      ;F961
2C5:	mov R1R0, 0x15                ;5501
2C7:	inc [R1R0]                    ;0C
2C8:	dec R0                        ;11
2C9:	mov A, [R1R0]                 ;04
2CA:	jnz A, 293                    ;BA93
2CC:	mov R1R0, 0x53                ;5305
2CE:	mov A, [R1R0]                 ;04
2CF:	rrc A                         ;02
2D0:	jnc 293                       ;CA93
2D2:	call 0E6                      ;F0E6
2D4:	mov A, 0xC                    ;7C
2D5:	jmp 1A3                       ;E1A3
2D7:	call 35E                      ;F35E
2D9:	jc 295                        ;C295
2DB:	mov R1R0, 0x15                ;5501
2DD:	mov A, [R1R0]                 ;04
2DE:	jz A, 32A                     ;B32A
2E0:	mov A, 0x0                    ;70
2E1:	call 7BC                      ;F7BC
2E3:	mov R3R2, 0x15                ;6501
2E5:	mov A, [R3R2]                 ;06
2E6:	dec R3                        ;17
2E7:	mov R2, A                     ;24
2E8:	mov R1R0, 0x48                ;5804
2EA:	call 370                      ;F370
2EC:	mov R3R2, 0x15                ;6501
2EE:	mov A, [R3R2]                 ;06
2EF:	ja2 2FA                       ;92FA
2F1:	mov R4, A                     ;28
2F2:	mov A, 0x0                    ;70
2F3:	mov R3, A                     ;26
2F4:	stc                           ;2B
2F5:	rlc A                         ;03
2F6:	dec R4                        ;19
2F7:	jnz R4, 2F4                   ;DAF4
2F9:	mov R2, A                     ;24
2FA:	mov R1R0, 0x4D                ;5D04
2FC:	jmp 302                       ;E302
2FE:	mov R3R2, 0x01                ;6100
300:	mov R1R0, 0x4C                ;5C04
302:	call 370                      ;F370
304:	jnz R4, 30D                   ;DB0D
306:	stc                           ;2B
307:	call 0DC                      ;F0DC
309:	mov R3R2, 0xC8                ;680C
30B:	call 793                      ;F793
30D:	call AF6                      ;FAF6
30F:	mov R1R0, 0x3F                ;5F03
311:	mov A, [R1R0]                 ;04
312:	ja0 1C9                       ;81C9
314:	jz A, 318                     ;B318
316:	jmp C38                       ;EC38
318:	mov R1R0, 0x53                ;5305
31A:	mov A, 0x6                    ;76
31B:	and A, [R1R0]                 ;1A
31C:	jz A, 169                     ;B169
31E:	ja1 6FF                       ;8EFF
320:	mov R1R0, 0x3C                ;5C03
322:	call E09                      ;FE09
324:	mov A, 0x0                    ;70
325:	mov R1R0, 0x0A                ;5A00
327:	mov [R1R0], A                 ;05
328:	jmp 4BD                       ;E4BD
32A:	mov R1R0, 0x42                ;5204
32C:	mov A, 0xC                    ;7C
32D:	call 7EC                      ;F7EC
32F:	jnc 334                       ;CB34
331:	mov A, 0x4                    ;74
332:	jmp 356                       ;E356
334:	mov R1R0, 0x32                ;5203
336:	mov A, [R1R0]                 ;04
337:	inc A                         ;31
338:	jz A, 342                     ;B342
33A:	dec R0                        ;11
33B:	mov R3R2, 0x0D                ;6D00
33D:	call 362                      ;F362
33F:	mov A, 0x6                    ;76
340:	jnc 356                       ;CB56
342:	mov R1R0, 0x10                ;5001
344:	mov R3R2, 0x1C                ;6C01
346:	inc R0                        ;10
347:	mov A, [R3R2]                 ;06
348:	or [R1R0], A                  ;1F
349:	dec R0                        ;11
34A:	and [R1R0], A                 ;1D
34B:	xor A, [R1R0]                 ;1B
34C:	jnz A, 355                    ;BB55
34E:	inc R0                        ;10
34F:	inc R2                        ;14
350:	mov A, R2                     ;25
351:	jnz A, 346                    ;BB46
353:	jmp 169                       ;E169
355:	mov A, 0x8                    ;78
356:	call 7BC                      ;F7BC
358:	jmp 169                       ;E169
35A:	mov R3R2, 0x0A                ;6A00
35C:	jmp 360                       ;E360
35E:	mov R3R2, 0xC7                ;670C
360:	mov R1R0, 0x00                ;5000
362:	mov R4, 0x0                   ;4600
364:	mov A, R2                     ;25
365:	sub A, [R1R0]                 ;0B
366:	jz A, 369                     ;B369
368:	inc R4                        ;18
369:	inc R0                        ;10
36A:	mov A, R3                     ;27
36B:	sbc A, [R1R0]                 ;0A
36C:	jz A, 36F                     ;B36F
36E:	inc R4                        ;18
36F:	ret                           ;2E
370:	clc                           ;2A
371:	mov R4, 0x1                   ;4601
373:	mov A, R2                     ;25
374:	adc A, [R1R0]                 ;08
375:	daa                           ;36
376:	mov [R1R0], A                 ;05
377:	mov A, R3                     ;27
378:	mov R2, A                     ;24
379:	mov A, 0x0                    ;70
37A:	mov R3, A                     ;26
37B:	inc R0                        ;10
37C:	mov A, R0                     ;21
37D:	inc A                         ;31
37E:	jnz A, 383                    ;BB83
380:	jnc 373                       ;CB73
382:	dec R4                        ;19
383:	mov A, R0                     ;21
384:	and A, 0x3                    ;4203
386:	jnz A, 373                    ;BB73
388:	ret                           ;2E
389:	mov R1R0, 0x16                ;5601
38B:	mov A, R2                     ;25
38C:	mov [R1R0], A                 ;05
38D:	mov A, R3                     ;27
38E:	inc R0                        ;10
38F:	mov [R1R0], A                 ;05
390:	mov R1R0, 0x16                ;5601
392:	call E60                      ;FE60
394:	jz A, 3B2                     ;B3B2
396:	call CC5                      ;FCC5
398:	call 3BD                      ;F3BD
39A:	mov R1R0, 0x3F                ;5F03
39C:	mov A, [R1R0]                 ;04
39D:	ja0 3D6                       ;83D6
39F:	mov R1R0, 0x53                ;5305
3A1:	mov A, [R1R0]                 ;04
3A2:	ja1 41F                       ;8C1F
3A4:	ja2 45D                       ;945D
3A6:	mov A, R3                     ;27
3A7:	ja0 735                       ;8735
3A9:	jz A, 3C5                     ;B3C5
3AB:	call 7A8                      ;F7A8
3AD:	mov A, R3                     ;27
3AE:	ja2 75E                       ;975E
3B0:	ja3 765                       ;9F65
3B2:	mov R1R0, 0x3F                ;5F03
3B4:	mov A, 0x7                    ;77
3B5:	and A, [R1R0]                 ;1A
3B6:	jz A, 260                     ;B260
3B8:	xor [R1R0], A                 ;1E
3B9:	ja0 1CD                       ;81CD
3BB:	jmp C3C                       ;EC3C
3BD:	mov R1R0, 0xB7                ;570B
3BF:	mov A, [R1R0]                 ;04
3C0:	ja3 3C3                       ;9BC3
3C2:	ret                           ;2E
3C3:	call B07                      ;FB07
3C5:	mov R3R2, 0x59                ;6905
3C7:	mov A, [R3R2]                 ;06
3C8:	ja0 3D6                       ;83D6
3CA:	inc R2                        ;14
3CB:	mov A, [R3R2]                 ;06
3CC:	mov R1R0, 0x9A                ;5A09
3CE:	call 7EC                      ;F7EC
3D0:	jnc 3D6                       ;CBD6
3D2:	dec R2                        ;15
3D3:	inc [R3R2]                    ;0E
3D4:	call DA1                      ;FDA1
3D6:	mov R3R2, 0x5D                ;6D05
3D8:	mov A, [R3R2]                 ;06
3D9:	jz A, 3EA                     ;B3EA
3DB:	mov R1R0, 0x98                ;5809
3DD:	mov A, 0xD                    ;7D
3DE:	call 7EC                      ;F7EC
3E0:	jnc 3EA                       ;CBEA
3E2:	dec [R3R2]                    ;0F
3E3:	mov R1R0, 0xD3                ;530D
3E5:	mov A, 0xF                    ;7F
3E6:	xor [R1R0], A                 ;1E
3E7:	mov R1R0, 0xD1                ;510D
3E9:	xor [R1R0], A                 ;1E
3EA:	mov R1R0, 0x3F                ;5F03
3EC:	mov A, [R1R0]                 ;04
3ED:	ja0 401                       ;8401
3EF:	mov R1R0, 0x53                ;5305
3F1:	mov A, [R1R0]                 ;04
3F2:	ja0 3F8                       ;83F8
3F4:	ja1 408                       ;8C08
3F6:	jmp 401                       ;E401
3F8:	mov A, 0xA                    ;7A
3F9:	call 7EA                      ;F7EA
3FB:	jnc 401                       ;CC01
3FD:	mov R1R0, 0xFE                ;5E0F
3FF:	mov A, 0x8                    ;78
400:	xor [R1R0], A                 ;1E
401:	mov R1R0, 0xB7                ;570B
403:	mov A, [R1R0]                 ;04
404:	ja3 396                       ;9B96
406:	jmp 390                       ;E390
408:	mov A, 0xD                    ;7D
409:	call 7EA                      ;F7EA
40B:	jnc 41D                       ;CC1D
40D:	mov R1R0, 0x56                ;5605
40F:	mov A, 0x2                    ;72
410:	xor [R1R0], A                 ;1E
411:	mov A, [R1R0]                 ;04
412:	ja1 419                       ;8C19
414:	call 9E4                      ;F9E4
416:	mov A, 0x1                    ;71
417:	jmp 41B                       ;E41B
419:	call 9E1                      ;F9E1
41B:	call 9D9                      ;F9D9
41D:	jmp 401                       ;E401
41F:	mov A, R3                     ;27
420:	jz A, 3C5                     ;B3C5
422:	mov R4, 0x0                   ;4600
424:	ja2 42D                       ;942D
426:	inc R4                        ;18
427:	ja0 42D                       ;842D
429:	inc R4                        ;18
42A:	ja1 42D                       ;8C2D
42C:	inc R4                        ;18
42D:	mov A, R4                     ;29
42E:	mov R1R0, 0x20                ;5002
430:	add A, [R1R0]                 ;09
431:	xor A, 0x3                    ;4303
433:	jnz A, 6C7                    ;BEC7
435:	mov R1R0, 0x32                ;5203
437:	mov R3R2, 0x35                ;6503
439:	mov A, [R1R0]                 ;04
43A:	mov R4, A                     ;28
43B:	mov A, [R3R2]                 ;06
43C:	mov [R1R0], A                 ;05
43D:	mov A, R4                     ;29
43E:	mov [R3R2], A                 ;07
43F:	dec R2                        ;15
440:	mov A, R0                     ;21
441:	dec R0                        ;11
442:	jnz A, 439                    ;BC39
444:	mov R3R2, 0x20                ;6002
446:	call 819                      ;F819
448:	mov A, [R3R2]                 ;06
449:	xor A, 0x3                    ;4303
44B:	mov R4, A                     ;28
44C:	mov A, 0x3                    ;73
44D:	xor A, [R1R0]                 ;1B
44E:	mov [R3R2], A                 ;07
44F:	inc R2                        ;14
450:	inc R2                        ;14
451:	mov A, R2                     ;25
452:	mov [R1R0], A                 ;05
453:	mov A, R0                     ;21
454:	sub A, [R1R0]                 ;0B
455:	mov A, R4                     ;29
456:	mov [R1R0], A                 ;05
457:	jnc 3C5                       ;CBC5
459:	dec R2                        ;15
45A:	dec R0                        ;11
45B:	jmp 448                       ;E448
45D:	mov A, R3                     ;27
45E:	rrc A                         ;02
45F:	ja0 46E                       ;846E
461:	ja1 49C                       ;8C9C
463:	ja2 4AB                       ;94AB
465:	mov R1R0, 0x3F                ;5F03
467:	mov A, [R1R0]                 ;04
468:	ja1 3C5                       ;8BC5
46A:	jnc 4BF                       ;CCBF
46C:	jmp BA2                       ;EBA2
46E:	mov R1R0, 0x52                ;5205
470:	mov A, [R1R0]                 ;04
471:	jz A, 3C5                     ;B3C5
473:	ja0 3C5                       ;83C5
475:	dec R0                        ;11
476:	mov A, [R1R0]                 ;04
477:	jz A, 3C5                     ;B3C5
479:	dec [R1R0]                    ;0D
47A:	mov A, 0x9                    ;79
47B:	call 7A9                      ;F7A9
47D:	call 7F4                      ;F7F4
47F:	call 9FA                      ;F9FA
481:	inc R4                        ;18
482:	jnz R4, 48C                   ;DC8C
484:	call 968                      ;F968
486:	call 35E                      ;F35E
488:	jc 47F                        ;C47F
48A:	jmp 49A                       ;E49A
48C:	mov A, 0x5                    ;75
48D:	mov R2, A                     ;24
48E:	call 961                      ;F961
490:	mov R1R0, 0x03                ;5300
492:	mov A, 0xD                    ;7D
493:	xor A, [R1R0]                 ;1B
494:	jz A, 49A                     ;B49A
496:	dec R2                        ;15
497:	mov A, R2                     ;25
498:	jnz A, 48E                    ;BC8E
49A:	jmp 3C5                       ;E3C5
49C:	mov R1R0, 0x30                ;5003
49E:	mov A, 0x9                    ;79
49F:	xor A, [R1R0]                 ;1B
4A0:	jz A, 4BF                     ;B4BF
4A2:	call 9E4                      ;F9E4
4A4:	mov R1R0, 0x30                ;5003
4A6:	inc [R1R0]                    ;0C
4A7:	call 9F3                      ;F9F3
4A9:	jmp 4B7                       ;E4B7
4AB:	mov R1R0, 0x30                ;5003
4AD:	mov A, [R1R0]                 ;04
4AE:	jz A, 4BF                     ;B4BF
4B0:	call 9E4                      ;F9E4
4B2:	mov R1R0, 0x30                ;5003
4B4:	dec [R1R0]                    ;0D
4B5:	call 9F3                      ;F9F3
4B7:	jc 4F5                        ;C4F5
4B9:	call 9E1                      ;F9E1
4BB:	call 7A8                      ;F7A8
4BD:	call E79                      ;FE79
4BF:	mov R1R0, 0x3F                ;5F03
4C1:	mov A, [R1R0]                 ;04
4C2:	ja1 3C5                       ;8BC5
4C4:	mov R1R0, 0x52                ;5205
4C6:	mov A, [R1R0]                 ;04
4C7:	jnz A, 3C5                    ;BBC5
4C9:	mov R1R0, 0x60                ;5006
4CB:	mov A, [R1R0]                 ;04
4CC:	jz A, 3C5                     ;B3C5
4CE:	mov A, 0x4                    ;74
4CF:	call 7EA                      ;F7EA
4D1:	jnc 3C5                       ;CBC5
4D3:	call 9D9                      ;F9D9
4D5:	call E07                      ;FE07
4D7:	mov R3R2, 0x36                ;6603
4D9:	mov R1R0, 0x30                ;5003
4DB:	mov A, [R3R2]                 ;06
4DC:	sub A, [R1R0]                 ;0B
4DD:	jz A, 4E4                     ;B4E4
4DF:	dec [R3R2]                    ;0F
4E0:	jc 4E4                        ;C4E4
4E2:	inc [R3R2]                    ;0E
4E3:	inc [R3R2]                    ;0E
4E4:	mov R3R2, 0x38                ;6803
4E6:	mov A, [R3R2]                 ;06
4E7:	inc A                         ;31
4E8:	jnz A, 4EF                    ;BCEF
4EA:	mov R1R0, 0x60                ;5006
4EC:	mov [R1R0], A                 ;05
4ED:	jmp 3C5                       ;E3C5
4EF:	call 9D8                      ;F9D8
4F1:	call 858                      ;F858
4F3:	jnc 3C5                       ;CBC5
4F5:	mov A, 0xB                    ;7B
4F6:	call 7A9                      ;F7A9
4F8:	mov R1R0, 0x14                ;5401
4FA:	mov A, 0xA                    ;7A
4FB:	mov [R1R0], A                 ;05
4FC:	mov R3R2, 0x43                ;6304
4FE:	mov A, [R3R2]                 ;06
4FF:	ja1 504                       ;8D04
501:	mov A, [R1R0]                 ;04
502:	call 9E5                      ;F9E5
504:	call 0F2                      ;F0F2
506:	mov A, 0x8                    ;78
507:	call 7EA                      ;F7EA
509:	jnc 504                       ;CD04
50B:	mov R1R0, 0x14                ;5401
50D:	inc [R1R0]                    ;0C
50E:	mov A, [R1R0]                 ;04
50F:	jnz A, 4FC                    ;BCFC
511:	call 86A                      ;F86A
513:	jz A, 19B                     ;B19B
515:	mov R1R0, 0x43                ;5304
517:	mov A, [R1R0]                 ;04
518:	xor [R1R0], A                 ;1E
519:	jnz A, 1A5                    ;B9A5
51B:	mov A, 0x4                    ;74
51C:	call 7BC                      ;F7BC
51E:	jmp 55F                       ;E55F
520:	jz A, 68A                     ;B68A
522:	mov A, 0xC                    ;7C
523:	mov [R3R2], A                 ;07
524:	dec R2                        ;15
525:	mov A, 0xB                    ;7B
526:	add A, [R1R0]                 ;09
527:	jz A, 52E                     ;B52E
529:	rrc A                         ;02
52A:	inc [R3R2]                    ;0E
52B:	jc 52E                        ;C52E
52D:	inc [R3R2]                    ;0E
52E:	call 86A                      ;F86A
530:	call E64                      ;FE64
532:	mov R1R0, 0x52                ;5205
534:	mov A, [R1R0]                 ;04
535:	jz A, 53D                     ;B53D
537:	call 7F0                      ;F7F0
539:	call 00E                      ;F00E
53B:	jmp 55F                       ;E55F
53D:	mov R1R0, 0xD8                ;580D
53F:	mov A, 0xF                    ;7F
540:	call 814                      ;F814
542:	inc R1                        ;12
543:	dec [R1R0]                    ;0D
544:	inc R0                        ;10
545:	mov A, 0x3                    ;73
546:	mov [R1R0], A                 ;05
547:	mov R1R0, 0xC0                ;500C
549:	mov A, 0x9                    ;79
54A:	mov [R1R0], A                 ;05
54B:	mov R1R0, 0xC2                ;520C
54D:	dec [R1R0]                    ;0D
54E:	mov R1R0, 0xDD                ;5D0D
550:	mov A, 0x7                    ;77
551:	mov [R1R0], A                 ;05
552:	mov R1R0, 0xDF                ;5F0D
554:	mov [R1R0], A                 ;05
555:	mov R1R0, 0x34                ;5403
557:	dec [R1R0]                    ;0D
558:	mov R1R0, 0x3C                ;5C03
55A:	mov A, 0xA                    ;7A
55B:	mov [R1R0], A                 ;05
55C:	inc R0                        ;10
55D:	mov A, 0x2                    ;72
55E:	mov [R1R0], A                 ;05
55F:	call 7F9                      ;F7F9
561:	call 961                      ;F961
563:	mov A, 0x4                    ;74
564:	call E76                      ;FE76
566:	mov R1R0, 0x60                ;5006
568:	mov [R1R0], A                 ;05
569:	call 9E1                      ;F9E1
56B:	jmp 6A7                       ;E6A7
56D:	inc R0                        ;10
56E:	inc [R1R0]                    ;0C
56F:	inc R0                        ;10
570:	mov R3R2, 0x90                ;6009
572:	mov A, [R3R2]                 ;06
573:	or A, 0x8                     ;4408
575:	mov R4, A                     ;28
576:	mov A, 0xF                    ;7F
577:	readf MR0A                    ;4F
578:	mov A, [R1R0]                 ;04
579:	dec R0                        ;11
57A:	xor A, [R1R0]                 ;1B
57B:	jnz A, 244                    ;BA44
57D:	mov [R1R0], A                 ;05
57E:	mov R1R0, 0x52                ;5205
580:	mov A, [R1R0]                 ;04
581:	jz A, 618                     ;B618
583:	call 7F4                      ;F7F4
585:	call 9FA                      ;F9FA
587:	inc R4                        ;18
588:	mov A, R4                     ;29
589:	jz A, 594                     ;B594
58B:	mov R1R0, 0x02                ;5200
58D:	call E0C                      ;FE0C
58F:	call 968                      ;F968
591:	mov R1R0, 0x43                ;5304
593:	inc [R1R0]                    ;0C
594:	call 9FA                      ;F9FA
596:	call 968                      ;F968
598:	call 35E                      ;F35E
59A:	jc 594                        ;C594
59C:	mov R1R0, 0x43                ;5304
59E:	mov A, [R1R0]                 ;04
59F:	jnz A, 4F5                    ;BCF5
5A1:	mov R1R0, 0x52                ;5205
5A3:	mov A, [R1R0]                 ;04
5A4:	ja0 5BD                       ;85BD
5A6:	mov R1R0, 0x5C                ;5C05
5A8:	inc [R1R0]                    ;0C
5A9:	mov R3R2, 0x81                ;6108
5AB:	mov A, [R3R2]                 ;06
5AC:	xor A, 0xF                    ;430F
5AE:	inc A                         ;31
5AF:	clc                           ;2A
5B0:	rrc A                         ;02
5B1:	xor A, [R1R0]                 ;1B
5B2:	jnz A, 5B9                    ;BDB9
5B4:	mov [R1R0], A                 ;05
5B5:	call 961                      ;F961
5B7:	jmp 244                       ;E244
5B9:	call 00E                      ;F00E
5BB:	jmp 244                       ;E244
5BD:	mov R1R0, 0x20                ;5002
5BF:	call E60                      ;FE60
5C1:	jnz A, 602                    ;BE02
5C3:	mov A, TMRL                   ;3A
5C4:	and A, 0x7                    ;4207
5C6:	jnz A, 5B9                    ;BDB9
5C8:	mov A, 0x4                    ;74
5C9:	mov [R1R0], A                 ;05
5CA:	dec R0                        ;11
5CB:	inc [R1R0]                    ;0C
5CC:	mov R1R0, 0x60                ;5006
5CE:	call 813                      ;F813
5D0:	dec [R1R0]                    ;0D
5D1:	mov R1R0, 0x64                ;5406
5D3:	mov A, 0x9                    ;79
5D4:	mov [R1R0], A                 ;05
5D5:	mov R1R0, 0x68                ;5806
5D7:	mov [R1R0], A                 ;05
5D8:	mov R1R0, 0x6C                ;5C06
5DA:	dec [R1R0]                    ;0D
5DB:	mov A, TMRL                   ;3A
5DC:	and A, 0x7                    ;4207
5DE:	mov R4, A                     ;28
5DF:	xor A, 0x7                    ;4307
5E1:	jnz A, 5E4                    ;BDE4
5E3:	mov R4, A                     ;28
5E4:	mov R1R0, 0x36                ;5603
5E6:	mov A, R4                     ;29
5E7:	mov [R1R0], A                 ;05
5E8:	inc R0                        ;10
5E9:	mov A, 0x4                    ;74
5EA:	mov [R1R0], A                 ;05
5EB:	inc R0                        ;10
5EC:	mov A, 0x1                    ;71
5ED:	mov [R1R0], A                 ;05
5EE:	mov A, R4                     ;29
5EF:	xor A, 0xF                    ;430F
5F1:	sub A, 0x9                    ;4109
5F3:	mov R4, A                     ;28
5F4:	jmp 600                       ;E600
5F6:	mov R1R0, 0x60                ;5006
5F8:	clc                           ;2A
5F9:	mov A, [R1R0]                 ;04
5FA:	rlc A                         ;03
5FB:	mov [R1R0], A                 ;05
5FC:	inc R0                        ;10
5FD:	jnz R0, 5F9                   ;A5F9
5FF:	dec R4                        ;19
600:	jnz R4, 5F6                   ;DDF6
602:	call E07                      ;FE07
604:	mov R1R0, 0x21                ;5102
606:	mov A, [R1R0]                 ;04
607:	jz A, 5B9                     ;B5B9
609:	dec [R1R0]                    ;0D
60A:	mov A, [R1R0]                 ;04
60B:	mov R1R0, 0x60                ;5006
60D:	rr A                          ;00
60E:	rr A                          ;00
60F:	mov R0, A                     ;20
610:	mov R3R2, 0x0C                ;6C00
612:	call E17                      ;FE17
614:	call 968                      ;F968
616:	jmp 244                       ;E244
618:	mov R1R0, 0x3C                ;5C03
61A:	call E60                      ;FE60
61C:	jnz A, 625                    ;BE25
61E:	mov R1R0, 0x60                ;5006
620:	mov A, [R1R0]                 ;04
621:	jnz A, 688                    ;BE88
623:	jmp 2D4                       ;E2D4
625:	mov R1R0, 0x34                ;5403
627:	call E09                      ;FE09
629:	mov R1R0, 0x37                ;5703
62B:	mov A, [R1R0]                 ;04
62C:	dec A                         ;3F
62D:	jz A, 63A                     ;B63A
62F:	call 7F4                      ;F7F4
631:	call 9FA                      ;F9FA
633:	inc R4                        ;18
634:	mov A, R4                     ;29
635:	jz A, 63A                     ;B63A
637:	mov R1R0, 0x43                ;5304
639:	inc [R1R0]                    ;0C
63A:	mov R3R2, 0x33                ;6303
63C:	mov R4, 0xE                   ;460E
63E:	call BA6                      ;FBA6
640:	call 808                      ;F808
642:	mov R1R0, 0x00                ;5000
644:	mov R3R2, 0x02                ;6200
646:	call E73                      ;FE73
648:	mov R1R0, 0x02                ;5200
64A:	mov A, 0x9                    ;79
64B:	call E00                      ;FE00
64D:	call 9FA                      ;F9FA
64F:	call 9FA                      ;F9FA
651:	call 968                      ;F968
653:	call 35E                      ;F35E
655:	jc 64F                        ;C64F
657:	mov R1R0, 0x43                ;5304
659:	mov A, [R1R0]                 ;04
65A:	jnz A, 4F5                    ;BCF5
65C:	call 961                      ;F961
65E:	call 9E1                      ;F9E1
660:	mov R3R2, 0x60                ;6006
662:	mov A, [R3R2]                 ;06
663:	jnz A, 688                    ;BE88
665:	mov R1R0, 0x35                ;5503
667:	mov A, [R1R0]                 ;04
668:	inc A                         ;31
669:	jz A, 688                     ;B688
66B:	dec R0                        ;11
66C:	mov A, 0xD                    ;7D
66D:	add A, [R1R0]                 ;09
66E:	jnc 688                       ;CE88
670:	mov A, 0x0                    ;70
671:	inc [R3R2]                    ;0E
672:	inc R2                        ;14
673:	mov [R3R2], A                 ;07
674:	mov A, TMRL                   ;3A
675:	mov R4, A                     ;28
676:	sub A, 0xA                    ;410A
678:	jnc 67B                       ;CE7B
67A:	mov R4, A                     ;28
67B:	mov R3R2, 0x36                ;6603
67D:	mov A, R4                     ;29
67E:	mov [R3R2], A                 ;07
67F:	inc R2                        ;14
680:	mov A, [R1R0]                 ;04
681:	dec A                         ;3F
682:	mov [R3R2], A                 ;07
683:	inc R2                        ;14
684:	mov A, 0x0                    ;70
685:	mov [R3R2], A                 ;07
686:	call 9D8                      ;F9D8
688:	jmp 244                       ;E244
68A:	mov A, 0xA                    ;7A
68B:	mov [R3R2], A                 ;07
68C:	call 86A                      ;F86A
68E:	call E64                      ;FE64
690:	mov R1R0, 0x20                ;5002
692:	mov A, 0xF                    ;7F
693:	call 814                      ;F814
695:	call E7B                      ;FE7B
697:	mov R1R0, 0xFF                ;5F0F
699:	inc [R1R0]                    ;0C
69A:	dec R0                        ;11
69B:	mov A, 0xC                    ;7C
69C:	mov [R1R0], A                 ;05
69D:	mov R1R0, 0x30                ;5003
69F:	mov A, 0x5                    ;75
6A0:	mov [R1R0], A                 ;05
6A1:	mov R1R0, 0x33                ;5303
6A3:	mov A, 0x3                    ;73
6A4:	mov [R1R0], A                 ;05
6A5:	call ACF                      ;FACF
6A7:	call 811                      ;F811
6A9:	mov R1R0, 0xC3                ;530C
6AB:	mov A, [R1R0]                 ;04
6AC:	rrc A                         ;02
6AD:	jnc 6C1                       ;CEC1
6AF:	call CC5                      ;FCC5
6B1:	mov R1R0, 0x9A                ;5A09
6B3:	mov A, 0x2                    ;72
6B4:	xor A, [R1R0]                 ;1B
6B5:	jnz A, 6BB                    ;BEBB
6B7:	inc [R1R0]                    ;0C
6B8:	mov A, 0x8                    ;78
6B9:	call 7A9                      ;F7A9
6BB:	xor A, 0x4                    ;4304
6BD:	jnz A, 6A9                    ;BEA9
6BF:	call DA1                      ;FDA1
6C1:	jmp 244                       ;E244
6C3:	mov R1R0, 0x20                ;5002
6C5:	mov A, [R1R0]                 ;04
6C6:	mov R4, A                     ;28
6C7:	mov A, R4                     ;29
6C8:	mov R3R2, 0x3C                ;6C03
6CA:	mov [R3R2], A                 ;07
6CB:	call 9E1                      ;F9E1
6CD:	mov R3R2, 0x3C                ;6C03
6CF:	mov A, [R3R2]                 ;06
6D0:	mov R1R0, 0x30                ;5003
6D2:	call DEE                      ;FDEE
6D4:	mov R1R0, 0x30                ;5003
6D6:	mov A, 0x6                    ;76
6D7:	add A, [R1R0]                 ;09
6D8:	jc 72F                        ;C72F
6DA:	inc R0                        ;10
6DB:	mov R3R2, 0x13                ;6301
6DD:	call 362                      ;F362
6DF:	jnc 72F                       ;CF2F
6E1:	call 858                      ;F858
6E3:	jnc 70E                       ;CF0E
6E5:	mov R4, A                     ;28
6E6:	call 819                      ;F819
6E8:	mov A, R1                     ;23
6E9:	mov R3, A                     ;26
6EA:	inc R0                        ;10
6EB:	mov A, R0                     ;21
6EC:	mov R2, A                     ;24
6ED:	dec R0                        ;11
6EE:	mov A, [R1R0]                 ;04
6EF:	mov [R3R2], A                 ;07
6F0:	dec R2                        ;15
6F1:	jnz R0, 6ED                   ;A6ED
6F3:	mov R3R2, 0x3C                ;6C03
6F5:	mov A, [R3R2]                 ;06
6F6:	mov [R1R0], A                 ;05
6F7:	jnz R4, 71C                   ;DF1C
6F9:	call 9E1                      ;F9E1
6FB:	mov R3R2, 0x10                ;6001
6FD:	jmp 300                       ;E300
6FF:	mov R1R0, 0x2E                ;5E02
701:	mov A, [R1R0]                 ;04
702:	inc A                         ;31
703:	jnz A, 2D4                    ;BAD4
705:	mov A, 0x5                    ;75
706:	call 7A9                      ;F7A9
708:	call 9E1                      ;F9E1
70A:	call ACF                      ;FACF
70C:	jmp 6C1                       ;E6C1
70E:	mov R3R2, 0x30                ;6003
710:	mov R4, 0x3                   ;4603
712:	call BA6                      ;FBA6
714:	call 9FA                      ;F9FA
716:	jc 72F                        ;C72F
718:	mov R4, 0x1                   ;4601
71A:	jmp 6E6                       ;E6E6
71C:	call 9E1                      ;F9E1
71E:	call 9DD                      ;F9DD
720:	call 819                      ;F819
722:	mov A, [R1R0]                 ;04
723:	mov R4, A                     ;28
724:	mov A, 0xF                    ;7F
725:	mov [R1R0], A                 ;05
726:	mov R1R0, 0x33                ;5303
728:	mov A, R4                     ;29
729:	call DEE                      ;FDEE
72B:	call 7A8                      ;F7A8
72D:	jmp 6C1                       ;E6C1
72F:	mov R1R0, 0x43                ;5304
731:	mov A, 0x2                    ;72
732:	mov [R1R0], A                 ;05
733:	jmp 4F5                       ;E4F5
735:	mov A, 0xA                    ;7A
736:	call 7A9                      ;F7A9
738:	call E21                      ;FE21
73A:	mov R3R2, 0x3A                ;6A03
73C:	mov R1R0, 0xB7                ;570B
73E:	mov A, [R1R0]                 ;04
73F:	ja1 743                       ;8F43
741:	dec [R3R2]                    ;0F
742:	dec [R3R2]                    ;0F
743:	inc [R3R2]                    ;0E
744:	call E9C                      ;FE9C
746:	mov R1R0, 0x36                ;5603
748:	mov A, 0x8                    ;78
749:	xor A, [R1R0]                 ;1B
74A:	jnz A, 754                    ;BF54
74C:	mov R3R2, 0x1C                ;6C01
74E:	call E15                      ;FE15
750:	call 90A                      ;F90A
752:	jmp 767                       ;E767
754:	call E28                      ;FE28
756:	jc 791                        ;C791
758:	mov R3R2, 0x1C                ;6C01
75A:	call E15                      ;FE15
75C:	jmp 78D                       ;E78D
75E:	call 90A                      ;F90A
760:	mov R1R0, 0x36                ;5603
762:	inc [R1R0]                    ;0C
763:	jmp 76A                       ;E76A
765:	call 90A                      ;F90A
767:	mov R1R0, 0x36                ;5603
769:	dec [R1R0]                    ;0D
76A:	call 874                      ;F874
76C:	mov R3R2, 0x28                ;6802
76E:	call E15                      ;FE15
770:	call E2C                      ;FE2C
772:	mov R1R0, 0x58                ;5805
774:	mov A, [R1R0]                 ;04
775:	jnc 787                       ;CF87
777:	jz A, 783                     ;B783
779:	call E21                      ;FE21
77B:	call E9C                      ;FE9C
77D:	mov R3R2, 0x1C                ;6C01
77F:	call E15                      ;FE15
781:	jmp 78D                       ;E78D
783:	call E21                      ;FE21
785:	jmp 78F                       ;E78F
787:	mov R1R0, 0x28                ;5802
789:	mov R3R2, 0x44                ;6404
78B:	call E17                      ;FE17
78D:	call EFA                      ;FEFA
78F:	call 90D                      ;F90D
791:	jmp 3C5                       ;E3C5
793:	mov R1R0, 0x94                ;5409
795:	mov A, 0x0                    ;70
796:	mov [R1R0], A                 ;05
797:	inc R0                        ;10
798:	jnz R0, 796                   ;A796
79A:	mov R1R0, 0x5A                ;5A05
79C:	mov A, R2                     ;25
79D:	mov [R1R0], A                 ;05
79E:	dec R0                        ;11
79F:	mov A, 0xE                    ;7E
7A0:	and [R1R0], A                 ;1D
7A1:	dec R0                        ;11
7A2:	mov A, R3                     ;27
7A3:	mov R1R0, 0x58                ;5805
7A5:	mov [R1R0], A                 ;05
7A6:	jmp 7B1                       ;E7B1
7A8:	mov A, 0x0                    ;70
7A9:	mov R1R0, 0x58                ;5805
7AB:	mov [R1R0], A                 ;05
7AC:	inc R0                        ;10
7AD:	mov A, 0xF                    ;7F
7AE:	xor A, [R1R0]                 ;1B
7AF:	ja0 7BB                       ;87BB
7B1:	mov R1R0, 0xC3                ;530C
7B3:	mov A, 0xF                    ;7F
7B4:	xor A, [R1R0]                 ;1B
7B5:	ja0 7BB                       ;87BB
7B7:	mov R1R0, 0x58                ;5805
7B9:	mov A, [R1R0]                 ;04
7BA:	sound A                       ;4B
7BB:	ret                           ;2E
7BC:	mov R4, A                     ;28
7BD:	jnz A, 7C2                    ;BFC2
7BF:	mov R1R0, 0x42                ;5204
7C1:	mov [R1R0], A                 ;05
7C2:	mov R1R0, 0xC3                ;530C
7C4:	mov A, 0xF                    ;7F
7C5:	xor A, [R1R0]                 ;1B
7C6:	ja0 7DE                       ;87DE
7C8:	mov R3R2, 0x5D                ;6D05
7CA:	mov A, 0x8                    ;78
7CB:	mov [R3R2], A                 ;07
7CC:	mov A, 0xB                    ;7B
7CD:	mov R1R0, 0x87                ;5708
7CF:	and A, [R1R0]                 ;1A
7D0:	out PA, A                     ;30
7D1:	inc R0                        ;10
7D2:	jnz R0, 7D1                   ;A7D1
7D4:	inc R1                        ;12
7D5:	jnz R1, 7D1                   ;AFD1
7D7:	mov A, R2                     ;25
7D8:	xor A, 0x2                    ;4302
7DA:	mov R2, A                     ;24
7DB:	dec R4                        ;19
7DC:	jnz R4, 7CD                   ;DFCD
7DE:	mov A, 0xF                    ;7F
7DF:	mov R1R0, 0xD1                ;510D
7E1:	mov [R1R0], A                 ;05
7E2:	mov R1R0, 0xCF                ;5F0C
7E4:	mov [R1R0], A                 ;05
7E5:	mov R1R0, 0xD3                ;530D
7E7:	mov A, 0x0                    ;70
7E8:	mov [R1R0], A                 ;05
7E9:	ret                           ;2E
7EA:	mov R1R0, 0x97                ;5709
7EC:	add A, [R1R0]                 ;09
7ED:	jc 7E7                        ;C7E7
7EF:	ret                           ;2E
7F0:	mov R3R2, 0xC7                ;670C
7F2:	jmp 7FC                       ;E7FC
7F4:	mov A, 0xA                    ;7A
7F5:	mov R3R2, 0x13                ;6301
7F7:	jmp 7FC                       ;E7FC
7F9:	mov A, 0x0                    ;70
7FA:	mov R3R2, 0x09                ;6900
7FC:	mov R1R0, 0x00                ;5000
7FE:	mov [R1R0], A                 ;05
7FF:	inc R0                        ;10
800:	mov A, 0x0                    ;70
801:	mov [R1R0], A                 ;05
802:	mov A, R2                     ;25
803:	inc R0                        ;10
804:	mov [R1R0], A                 ;05
805:	inc R0                        ;10
806:	mov A, R3                     ;27
807:	mov [R1R0], A                 ;05
808:	mov R1R0, 0x05                ;5500
80A:	mov A, 0xA                    ;7A
80B:	mov [R1R0], A                 ;05
80C:	mov R1R0, 0x57                ;5705
80E:	mov A, 0x9                    ;79
80F:	mov [R1R0], A                 ;05
810:	ret                           ;2E
811:	mov R1R0, 0x94                ;5409
813:	mov A, 0x0                    ;70
814:	mov [R1R0], A                 ;05
815:	inc R0                        ;10
816:	jnz R0, 814                   ;A014
818:	ret                           ;2E
819:	mov R1R0, 0x2F                ;5F02
81B:	inc R0                        ;10
81C:	mov A, [R1R0]                 ;04
81D:	inc A                         ;31
81E:	jnz A, 81B                    ;B81B
820:	dec R0                        ;11
821:	ret                           ;2E
822:	mov R1R0, 0x82                ;5208
824:	inc [R1R0]                    ;0C
825:	mov A, TMRL                   ;3A
826:	xor [R1R0], A                 ;1E
827:	mov A, [R1R0]                 ;04
828:	mov R4, A                     ;28
829:	sub A, 0x7                    ;4107
82B:	jnc 832                       ;C832
82D:	mov R4, A                     ;28
82E:	sub A, 0x7                    ;4107
830:	jc 822                        ;C022
832:	mov R1R0, 0x50                ;5005
834:	inc [R1R0]                    ;0C
835:	mov R3R2, 0x90                ;6009
837:	mov A, [R3R2]                 ;06
838:	rrc A                         ;02
839:	jnc 844                       ;C844
83B:	mov A, 0x4                    ;74
83C:	xor A, [R1R0]                 ;1B
83D:	jnz A, 844                    ;B844
83F:	mov [R1R0], A                 ;05
840:	mov A, R4                     ;29
841:	add A, 0x7                    ;4007
843:	mov R4, A                     ;28
844:	mov A, TMRL                   ;3A
845:	mov R3R2, 0x3D                ;6D03
847:	mov R1R0, 0x3A                ;5A03
849:	mov [R1R0], A                 ;05
84A:	mov [R3R2], A                 ;07
84B:	dec R0                        ;11
84C:	dec R2                        ;15
84D:	mov A, R4                     ;29
84E:	mov [R1R0], A                 ;05
84F:	mov [R3R2], A                 ;07
850:	jmp E9C                       ;EE9C
852:	mov R3R2, 0x31                ;6103
854:	mov R1R0, 0x37                ;5703
856:	jmp 85C                       ;E85C
858:	mov R1R0, 0x36                ;5603
85A:	mov R3R2, 0x30                ;6003
85C:	clc                           ;2A
85D:	mov A, [R3R2]                 ;06
85E:	xor A, [R1R0]                 ;1B
85F:	jnz A, 869                    ;B869
861:	inc R0                        ;10
862:	inc R2                        ;14
863:	mov A, R0                     ;21
864:	xor A, 0x9                    ;4309
866:	jnz A, 85D                    ;B85D
868:	stc                           ;2B
869:	ret                           ;2E
86A:	mov R1R0, 0x50                ;5005
86C:	dec [R1R0]                    ;0D
86D:	mov A, 0xF                    ;7F
86E:	readf R4A                     ;4D
86F:	mov R3R2, 0xBE                ;6E0B
871:	mov [R3R2], A                 ;07
872:	jmp D98                       ;ED98
874:	mov R1R0, 0x2C                ;5C02
876:	mov A, 0xF                    ;7F
877:	mov [R1R0], A                 ;05
878:	inc R0                        ;10
879:	jnz R0, 876                   ;A076
87B:	mov R1R0, 0x41                ;5104
87D:	mov A, 0x1                    ;71
87E:	mov R4, 0x0                   ;4600
880:	mov [R1R0], A                 ;05
881:	mov R3R2, 0x06                ;6600
883:	mov A, 0x4                    ;74
884:	mov [R3R2], A                 ;07
885:	dec R2                        ;15
886:	mov [R3R2], A                 ;07
887:	mov R1R0, 0x36                ;5603
889:	mov A, 0x9                    ;79
88A:	add A, [R1R0]                 ;09
88B:	jnc 896                       ;C896
88D:	sub A, 0x5                    ;4105
88F:	jc 894                        ;C094
891:	xor A, 0xF                    ;430F
893:	dec A                         ;3F
894:	mov [R3R2], A                 ;07
895:	inc R2                        ;14
896:	inc R0                        ;10
897:	inc R0                        ;10
898:	mov A, [R1R0]                 ;04
899:	jz A, 8AB                     ;B0AB
89B:	inc A                         ;31
89C:	dec R0                        ;11
89D:	jnz A, 8A3                    ;B8A3
89F:	mov A, 0x3                    ;73
8A0:	and A, [R1R0]                 ;1A
8A1:	jmp 8A8                       ;E8A8
8A3:	mov A, 0xF                    ;7F
8A4:	xor A, [R1R0]                 ;1B
8A5:	and A, 0x3                    ;4203
8A7:	inc A                         ;31
8A8:	mov R3R2, 0x06                ;6600
8AA:	mov [R3R2], A                 ;07
8AB:	mov R3R2, 0x57                ;6705
8AD:	mov A, 0x0                    ;70
8AE:	mov [R3R2], A                 ;07
8AF:	mov R3R2, 0x07                ;6700
8B1:	mov [R3R2], A                 ;07
8B2:	mov R1R0, 0x36                ;5603
8B4:	mov A, 0x9                    ;79
8B5:	add A, [R1R0]                 ;09
8B6:	jnc 8BF                       ;C8BF
8B8:	sub A, 0x3                    ;4103
8BA:	jc 8BF                        ;C0BF
8BC:	sub A, 0xC                    ;410C
8BE:	mov [R3R2], A                 ;07
8BF:	jnz R4, 8CB                   ;D8CB
8C1:	mov A, 0x5                    ;75
8C2:	add A, [R1R0]                 ;09
8C3:	mov A, [R1R0]                 ;04
8C4:	jnc 8C7                       ;C8C7
8C6:	mov A, 0x0                    ;70
8C7:	mov R1R0, 0x00                ;5000
8C9:	jmp 8D6                       ;E8D6
8CB:	mov A, 0x3                    ;73
8CC:	add A, [R1R0]                 ;09
8CD:	mov R4, A                     ;28
8CE:	sub A, 0xA                    ;410A
8D0:	mov A, R4                     ;29
8D1:	jnc 8D4                       ;C8D4
8D3:	mov A, 0x9                    ;79
8D4:	mov R1R0, 0x02                ;5200
8D6:	mov R3R2, 0x36                ;6603
8D8:	mov R4, 0xF                   ;460F
8DA:	jmp BA9                       ;EBA9
8DC:	mov R3R2, 0x2C                ;6C02
8DE:	mov R1R0, 0x38                ;5803
8E0:	mov A, [R1R0]                 ;04
8E1:	inc A                         ;31
8E2:	jnz A, 8E9                    ;B8E9
8E4:	dec R0                        ;11
8E5:	mov A, 0x3                    ;73
8E6:	xor A, [R1R0]                 ;1B
8E7:	inc A                         ;31
8E8:	mov R2, A                     ;24
8E9:	mov R1R0, 0x41                ;5104
8EB:	mov A, [R1R0]                 ;04
8EC:	dec A                         ;3F
8ED:	jnz A, 92A                    ;B92A
8EF:	mov R1R0, 0x0B                ;5B00
8F1:	mov A, [R1R0]                 ;04
8F2:	jz A, 8F9                     ;B0F9
8F4:	xor [R1R0], A                 ;1E
8F5:	mov R1R0, 0x06                ;5600
8F7:	mov A, 0x1                    ;71
8F8:	mov [R1R0], A                 ;05
8F9:	jmp 9FA                       ;E9FA
8FB:	mov R1R0, 0x0C                ;5C00
8FD:	mov A, [R1R0]                 ;04
8FE:	mov [R3R2], A                 ;07
8FF:	inc R2                        ;14
900:	mov R1R0, 0x06                ;5600
902:	dec [R1R0]                    ;0D
903:	mov A, [R1R0]                 ;04
904:	jnz A, 8F9                    ;B8F9
906:	mov R1R0, 0x41                ;5104
908:	mov [R1R0], A                 ;05
909:	ret                           ;2E
90A:	clc                           ;2A
90B:	jmp 90E                       ;E90E
90D:	stc                           ;2B
90E:	mov R3R2, 0x44                ;6404
910:	mov R1R0, 0x2C                ;5C02
912:	mov A, [R3R2]                 ;06
913:	mov [R1R0], A                 ;05
914:	inc R0                        ;10
915:	inc R2                        ;14
916:	jnz R0, 912                   ;A112
918:	jnc 924                       ;C924
91A:	mov R1R0, 0x2C                ;5C02
91C:	mov R3R2, 0x1C                ;6C01
91E:	mov A, [R3R2]                 ;06
91F:	or [R1R0], A                  ;1F
920:	inc R0                        ;10
921:	inc R2                        ;14
922:	jnz R0, 91E                   ;A11E
924:	mov R1R0, 0x41                ;5104
926:	mov A, 0x2                    ;72
927:	mov R4, A                     ;28
928:	jmp 880                       ;E880
92A:	mov R1R0, 0x0B                ;5B00
92C:	mov A, [R1R0]                 ;04
92D:	jz A, 939                     ;B139
92F:	xor [R1R0], A                 ;1E
930:	mov R1R0, 0x38                ;5803
932:	mov A, [R1R0]                 ;04
933:	dec A                         ;3F
934:	jz A, 939                     ;B139
936:	mov R1R0, 0x06                ;5600
938:	inc [R1R0]                    ;0C
939:	mov A, [R3R2]                 ;06
93A:	mov R1R0, 0x0C                ;5C00
93C:	mov [R1R0], A                 ;05
93D:	mov A, 0x1                    ;71
93E:	mov R4, A                     ;28
93F:	mov R1R0, 0x07                ;5700
941:	mov A, [R1R0]                 ;04
942:	mov R3, A                     ;26
943:	jmp 94E                       ;E94E
945:	mov R1R0, 0x0C                ;5C00
947:	mov A, [R1R0]                 ;04
948:	rr A                          ;00
949:	jnz R4, 94D                   ;D94D
94B:	rl A                          ;01
94C:	rl A                          ;01
94D:	mov [R1R0], A                 ;05
94E:	mov A, R3                     ;27
94F:	dec R3                        ;17
950:	jnz A, 945                    ;B945
952:	mov A, 0x2                    ;72
953:	mov R3, A                     ;26
954:	jnz R4, 968                   ;D968
956:	jmp 8FB                       ;E8FB
958:	inc R2                        ;14
959:	mov R1R0, 0x06                ;5600
95B:	dec [R1R0]                    ;0D
95C:	mov A, [R1R0]                 ;04
95D:	jnz A, 939                    ;B939
95F:	jmp 906                       ;E906
961:	mov A, 0x0                    ;70
962:	mov R1R0, 0x0C                ;5C00
964:	mov [R1R0], A                 ;05
965:	inc R0                        ;10
966:	jnz R0, 964                   ;A164
968:	mov R1R0, 0x5B                ;5B05
96A:	mov A, 0x4                    ;74
96B:	or [R1R0], A                  ;1F
96C:	mov R4, A                     ;28
96D:	jmp A07                       ;EA07
96F:	mov R1R0, 0x0F                ;5F00
971:	mov A, [R1R0]                 ;04
972:	rrc A                         ;02
973:	mov [R1R0], A                 ;05
974:	dec R0                        ;11
975:	mov A, R0                     ;21
976:	ja2 971                       ;9171
978:	mov R1R0, 0x03                ;5300
97A:	jmp A2A                       ;EA2A
97C:	mov A, R4                     ;29
97D:	jc 983                        ;C183
97F:	xor A, 0xF                    ;430F
981:	and [R1R0], A                 ;1D
982:	mov A, 0x0                    ;70
983:	or [R1R0], A                  ;1F
984:	mov R1R0, 0x02                ;5200
986:	dec [R1R0]                    ;0D
987:	mov A, [R1R0]                 ;04
988:	inc A                         ;31
989:	jnz A, 98D                    ;B98D
98B:	inc R0                        ;10
98C:	dec [R1R0]                    ;0D
98D:	mov R1R0, 0x04                ;5400
98F:	dec [R1R0]                    ;0D
990:	mov A, [R1R0]                 ;04
991:	jnz A, 96F                    ;B96F
993:	mov R1R0, 0x57                ;5705
995:	mov A, [R1R0]                 ;04
996:	ja0 9A5                       ;81A5
998:	mov R1R0, 0x02                ;5200
99A:	mov A, 0xA                    ;7A
99B:	add A, [R1R0]                 ;09
99C:	mov [R1R0], A                 ;05
99D:	jnc 9A1                       ;C9A1
99F:	inc R0                        ;10
9A0:	inc [R1R0]                    ;0C
9A1:	mov R4, 0x1                   ;4601
9A3:	jmp 9AE                       ;E9AE
9A5:	ja1 9AC                       ;89AC
9A7:	mov R1R0, 0x0A                ;5A00
9A9:	mov A, [R1R0]                 ;04
9AA:	jnz A, 9BC                    ;B9BC
9AC:	mov R4, 0x2                   ;4602
9AE:	mov R1R0, 0x05                ;5500
9B0:	mov A, [R1R0]                 ;04
9B1:	mov R1R0, 0x02                ;5200
9B3:	add A, [R1R0]                 ;09
9B4:	mov [R1R0], A                 ;05
9B5:	inc R0                        ;10
9B6:	jnc 9B9                       ;C9B9
9B8:	inc [R1R0]                    ;0C
9B9:	dec R4                        ;19
9BA:	jnz R4, 9AE                   ;D9AE
9BC:	mov R1R0, 0x08                ;5800
9BE:	mov A, [R1R0]                 ;04
9BF:	mov R2, A                     ;24
9C0:	inc R0                        ;10
9C1:	mov A, [R1R0]                 ;04
9C2:	mov R3, A                     ;26
9C3:	mov R1R0, 0x41                ;5104
9C5:	mov A, [R1R0]                 ;04
9C6:	jz A, DF9                     ;B5F9
9C8:	dec A                         ;3F
9C9:	jz A, 93E                     ;B13E
9CB:	dec A                         ;3F
9CC:	jz A, 958                     ;B158
9CE:	dec A                         ;3F
9CF:	jz A, B99                     ;B399
9D1:	dec A                         ;3F
9D2:	jz A, 906                     ;B106
9D4:	mov A, 0x0                    ;70
9D5:	mov [R1R0], A                 ;05
9D6:	jc ACF                        ;C2CF
9D8:	mov A, 0x1                    ;71
9D9:	mov R3R2, 0x36                ;6603
9DB:	jmp 9E7                       ;E9E7
9DD:	mov R3R2, 0x33                ;6303
9DF:	jmp 9E7                       ;E9E7
9E1:	mov A, 0x1                    ;71
9E2:	jmp 9E5                       ;E9E5
9E4:	mov A, 0x0                    ;70
9E5:	mov R3R2, 0x30                ;6003
9E7:	mov R1R0, 0x0C                ;5C00
9E9:	mov [R1R0], A                 ;05
9EA:	mov R1R0, 0x02                ;5200
9EC:	mov R4, 0x1                   ;4601
9EE:	jmp BA8                       ;EBA8
9F0:	mov A, 0x4                    ;74
9F1:	jmp B94                       ;EB94
9F3:	mov R3R2, 0x00                ;6000
9F5:	mov A, [R1R0]                 ;04
9F6:	mov [R3R2], A                 ;07
9F7:	inc R2                        ;14
9F8:	mov A, 0x0                    ;70
9F9:	mov [R3R2], A                 ;07
9FA:	mov R1R0, 0x0C                ;5C00
9FC:	mov A, 0xF                    ;7F
9FD:	mov [R1R0], A                 ;05
9FE:	mov R1R0, 0x1B                ;5B01
A00:	mov A, 0x0                    ;70
A01:	mov [R1R0], A                 ;05
A02:	mov R1R0, 0x5B                ;5B05
A04:	mov A, 0xB                    ;7B
A05:	and [R1R0], A                 ;1D
A06:	mov R4, A                     ;28
A07:	mov R1R0, 0x08                ;5800
A09:	mov A, R2                     ;25
A0A:	mov [R1R0], A                 ;05
A0B:	inc R0                        ;10
A0C:	mov A, R3                     ;27
A0D:	mov [R1R0], A                 ;05
A0E:	mov R1R0, 0x05                ;5500
A10:	mov A, [R1R0]                 ;04
A11:	dec R0                        ;11
A12:	mov [R1R0], A                 ;05
A13:	mov A, R4                     ;29
A14:	ja2 96F                       ;916F
A16:	mov R1R0, 0x01                ;5100
A18:	mov R3R2, 0x53                ;6305
A1A:	mov A, [R3R2]                 ;06
A1B:	ja0 A1F                       ;821F
A1D:	jmp A2A                       ;EA2A
A1F:	mov R1R0, 0x01                ;5100
A21:	mov A, [R1R0]                 ;04
A22:	jnz A, A2A                    ;BA2A
A24:	dec R0                        ;11
A25:	mov A, 0x4                    ;74
A26:	xor A, [R1R0]                 ;1B
A27:	inc R0                        ;10
A28:	jz A, A58                     ;B258
A2A:	mov A, 0x1                    ;71
A2B:	jtmr DB7                      ;D5B7
A2D:	mov A, [R1R0]                 ;04
A2E:	dec R0                        ;11
A2F:	readf R4A                     ;4D
A30:	mov R0, A                     ;20
A31:	mov A, R4                     ;29
A32:	or A, 0xC                     ;440C
A34:	mov R1, A                     ;22
A35:	dec R1                        ;13
A36:	mov R3R2, 0x57                ;6705
A38:	mov A, [R3R2]                 ;06
A39:	ja1 A3C                       ;8A3C
A3B:	inc R1                        ;12
A3C:	mov A, R4                     ;29
A3D:	and A, 0xC                    ;420C
A3F:	mov R4, 0x1                   ;4601
A41:	jz A, A4E                     ;B24E
A43:	xor A, 0xC                    ;430C
A45:	inc R4                        ;18
A46:	ja3 A4E                       ;9A4E
A48:	mov R4, 0x8                   ;4608
A4A:	jz A, A4E                     ;B24E
A4C:	mov R4, 0x4                   ;4604
A4E:	mov R3R2, 0x5B                ;6B05
A50:	mov A, [R3R2]                 ;06
A51:	ja2 97C                       ;917C
A53:	mov A, R4                     ;29
A54:	and A, [R1R0]                 ;1A
A55:	clc                           ;2A
A56:	jz A, A5C                     ;B25C
A58:	stc                           ;2B
A59:	mov R1R0, 0x1B                ;5B01
A5B:	inc [R1R0]                    ;0C
A5C:	mov R1R0, 0x0C                ;5C00
A5E:	mov A, [R1R0]                 ;04
A5F:	rlc A                         ;03
A60:	mov [R1R0], A                 ;05
A61:	inc R0                        ;10
A62:	jnz R0, A5E                   ;A25E
A64:	mov R1R0, 0x00                ;5000
A66:	inc [R1R0]                    ;0C
A67:	mov A, [R1R0]                 ;04
A68:	jnz A, A6C                    ;BA6C
A6A:	inc R0                        ;10
A6B:	inc [R1R0]                    ;0C
A6C:	mov R1R0, 0x04                ;5400
A6E:	dec [R1R0]                    ;0D
A6F:	mov A, [R1R0]                 ;04
A70:	jnz A, A16                    ;BA16
A72:	mov R1R0, 0x57                ;5705
A74:	mov A, [R1R0]                 ;04
A75:	ja0 A89                       ;8289
A77:	mov R1R0, 0x00                ;5000
A79:	mov A, [R1R0]                 ;04
A7A:	mov R4, A                     ;28
A7B:	mov R1R0, 0x05                ;5500
A7D:	mov A, 0xA                    ;7A
A7E:	sub A, [R1R0]                 ;0B
A7F:	mov R1R0, 0x00                ;5000
A81:	mov [R1R0], A                 ;05
A82:	mov A, R4                     ;29
A83:	add A, [R1R0]                 ;09
A84:	mov [R1R0], A                 ;05
A85:	jnc A89                       ;CA89
A87:	inc R0                        ;10
A88:	inc [R1R0]                    ;0C
A89:	mov R1R0, 0x57                ;5705
A8B:	mov A, [R1R0]                 ;04
A8C:	jz A, 9BC                     ;B1BC
A8E:	ja2 AAD                       ;92AD
A90:	mov R4, 0xF                   ;460F
A92:	mov R1R0, 0x1B                ;5B01
A94:	mov A, [R1R0]                 ;04
A95:	jz A, A9D                     ;B29D
A97:	inc R4                        ;18
A98:	xor A, 0xA                    ;430A
A9A:	jnz A, A9D                    ;BA9D
A9C:	inc R4                        ;18
A9D:	mov R1R0, 0x0A                ;5A00
A9F:	mov A, [R1R0]                 ;04
AA0:	jz A, 9BC                     ;B1BC
AA2:	mov R1R0, 0x00                ;5000
AA4:	mov A, 0xC                    ;7C
AA5:	add A, [R1R0]                 ;09
AA6:	mov [R1R0], A                 ;05
AA7:	inc R0                        ;10
AA8:	mov A, 0xE                    ;7E
AA9:	adc A, [R1R0]                 ;08
AAA:	mov [R1R0], A                 ;05
AAB:	jmp 9BC                       ;E9BC
AAD:	mov R1R0, 0x0C                ;5C00
AAF:	mov A, [R1R0]                 ;04
AB0:	rrc A                         ;02
AB1:	jmp 9BC                       ;E9BC
AB3:	mov A, 0x0                    ;70
AB4:	mov R1R0, 0xC0                ;500C
AB6:	mov [R1R0], A                 ;05
AB7:	inc R0                        ;10
AB8:	inc R0                        ;10
AB9:	mov [R1R0], A                 ;05
ABA:	mov R4, 0x9                   ;4609
ABC:	inc R0                        ;10
ABD:	inc R0                        ;10
ABE:	jnz R0, AC1                   ;A2C1
AC0:	inc R1                        ;12
AC1:	mov A, 0xC                    ;7C
AC2:	and [R1R0], A                 ;1D
AC3:	dec R4                        ;19
AC4:	jnz R4, ABC                   ;DABC
AC6:	mov A, 0x0                    ;70
AC7:	mov [R1R0], A                 ;05
AC8:	inc R0                        ;10
AC9:	jnz R0, AC6                   ;A2C6
ACB:	inc R1                        ;12
ACC:	jnz R1, AC6                   ;AAC6
ACE:	ret                           ;2E
ACF:	mov R3R2, 0x36                ;6603
AD1:	mov A, TMRL                   ;3A
AD2:	mov R4, A                     ;28
AD3:	sub A, 0xA                    ;410A
AD5:	jnc AD8                       ;CAD8
AD7:	mov R4, A                     ;28
AD8:	mov A, R4                     ;29
AD9:	mov [R3R2], A                 ;07
ADA:	inc R2                        ;14
ADB:	mov A, TMRL                   ;3A
ADC:	mov R4, A                     ;28
ADD:	mov [R3R2], A                 ;07
ADE:	inc R2                        ;14
ADF:	mov A, 0x0                    ;70
AE0:	mov [R3R2], A                 ;07
AE1:	mov A, R4                     ;29
AE2:	sub A, 0x4                    ;4104
AE4:	jc AEA                        ;C2EA
AE6:	mov A, TMRL                   ;3A
AE7:	and A, 0x1                    ;4201
AE9:	mov [R3R2], A                 ;07
AEA:	mov R3R2, 0x36                ;6603
AEC:	mov R4, 0x2                   ;4602
AEE:	jmp BA6                       ;EBA6
AF0:	mov R1R0, 0x41                ;5104
AF2:	mov A, 0x5                    ;75
AF3:	mov [R1R0], A                 ;05
AF4:	jmp 9FA                       ;E9FA
AF6:	mov R3R2, 0x4C                ;6C04
AF8:	clc                           ;2A
AF9:	jmp B34                       ;EB34
AFB:	mov R3R2, 0x7C                ;6C07
AFD:	ja2 B00                       ;9300
AFF:	inc R3                        ;16
B00:	mov R1R0, 0xC3                ;530C
B02:	mov A, 0x4                    ;74
B03:	or [R1R0], A                  ;1F
B04:	clc                           ;2A
B05:	jmp B38                       ;EB38
B07:	mov R4, A                     ;28
B08:	mov R1R0, 0x9D                ;5D09
B0A:	mov A, 0xE                    ;7E
B0B:	add A, [R1R0]                 ;09
B0C:	jc CF1                        ;C4F1
B0E:	mov R1R0, 0x9A                ;5A09
B10:	mov A, 0x2                    ;72
B11:	xor A, [R1R0]                 ;1B
B12:	jnz A, DF9                    ;BDF9
B14:	mov [R1R0], A                 ;05
B15:	mov R1R0, 0x56                ;5605
B17:	mov A, 0x1                    ;71
B18:	xor [R1R0], A                 ;1E
B19:	mov A, [R1R0]                 ;04
B1A:	rrc A                         ;02
B1B:	mov R3R2, 0x90                ;6009
B1D:	jnz R4, B28                   ;DB28
B1F:	mov A, [R3R2]                 ;06
B20:	jnc AFB                       ;CAFB
B22:	ja2 AFB                       ;92FB
B24:	mov R3R2, 0x88                ;6808
B26:	jmp B33                       ;EB33
B28:	mov R1R0, 0xB7                ;570B
B2A:	mov A, 0x4                    ;74
B2B:	xor [R1R0], A                 ;1E
B2C:	jnc AF6                       ;CAF6
B2E:	mov A, [R3R2]                 ;06
B2F:	ja2 AF6                       ;92F6
B31:	mov R3R2, 0x48                ;6804
B33:	stc                           ;2B
B34:	mov R1R0, 0xC3                ;530C
B36:	mov A, 0xB                    ;7B
B37:	and [R1R0], A                 ;1D
B38:	mov R1R0, 0xC1                ;510C
B3A:	mov A, 0xA                    ;7A
B3B:	and [R1R0], A                 ;1D
B3C:	mov A, 0x4                    ;74
B3D:	jnc B40                       ;CB40
B3F:	mov A, 0x1                    ;71
B40:	or [R1R0], A                  ;1F
B41:	mov R1R0, 0xB1                ;510B
B43:	mov A, 0x3                    ;73
B44:	and [R1R0], A                 ;1D
B45:	mov R1R0, 0x02                ;5200
B47:	mov A, 0xC                    ;7C
B48:	mov [R1R0], A                 ;05
B49:	inc R0                        ;10
B4A:	mov A, 0xD                    ;7D
B4B:	mov [R1R0], A                 ;05
B4C:	mov A, 0x4                    ;74
B4D:	mov R4, A                     ;28
B4E:	mov R1R0, 0x1B                ;5B01
B50:	mov [R1R0], A                 ;05
B51:	mov R1R0, 0x78                ;5807
B53:	mov A, [R3R2]                 ;06
B54:	mov [R1R0], A                 ;05
B55:	inc R0                        ;10
B56:	inc R2                        ;14
B57:	mov A, R0                     ;21
B58:	xor A, 0xC                    ;430C
B5A:	jnz A, B53                    ;BB53
B5C:	mov A, R4                     ;29
B5D:	ja1 B6C                       ;8B6C
B5F:	dec R0                        ;11
B60:	mov A, [R1R0]                 ;04
B61:	jnz A, B7A                    ;BB7A
B63:	mov A, 0xA                    ;7A
B64:	mov [R1R0], A                 ;05
B65:	dec R4                        ;19
B66:	jnz R4, B5F                   ;DB5F
B68:	mov A, 0x0                    ;70
B69:	mov [R1R0], A                 ;05
B6A:	jmp B80                       ;EB80
B6C:	mov A, 0x9                    ;79
B6D:	mov R0, A                     ;20
B6E:	mov A, [R1R0]                 ;04
B6F:	clc                           ;2A
B70:	daa                           ;36
B71:	mov [R1R0], A                 ;05
B72:	mov R1R0, 0xD2                ;520D
B74:	mov A, 0xB                    ;7B
B75:	and [R1R0], A                 ;1D
B76:	jnc B80                       ;CB80
B78:	mov A, 0x4                    ;74
B79:	or [R1R0], A                  ;1F
B7A:	jc B80                        ;C380
B7C:	mov R1R0, 0xB1                ;510B
B7E:	mov A, 0x4                    ;74
B7F:	or [R1R0], A                  ;1F
B80:	mov A, 0x7                    ;77
B81:	mov R1R0, 0x05                ;5500
B83:	mov [R1R0], A                 ;05
B84:	mov R3R2, 0x78                ;6807
B86:	mov A, [R3R2]                 ;06
B87:	inc A                         ;31
B88:	inc A                         ;31
B89:	mov R4, A                     ;28
B8A:	mov A, 0xF                    ;7F
B8B:	mov R1R0, 0x0D                ;5D00
B8D:	readf MR0A                    ;4F
B8E:	dec R0                        ;11
B8F:	mov [R1R0], A                 ;05
B90:	mov R1R0, 0x57                ;5705
B92:	mov A, 0x3                    ;73
B93:	mov [R1R0], A                 ;05
B94:	mov R1R0, 0x41                ;5104
B96:	mov [R1R0], A                 ;05
B97:	jmp 968                       ;E968
B99:	inc R2                        ;14
B9A:	mov R1R0, 0x1B                ;5B01
B9C:	dec [R1R0]                    ;0D
B9D:	mov A, [R1R0]                 ;04
B9E:	jnz A, B86                    ;BB86
BA0:	jmp 906                       ;E906
BA2:	mov R3R2, 0x30                ;6003
BA4:	mov R4, 0x0                   ;4600
BA6:	mov R1R0, 0x00                ;5000
BA8:	mov A, [R3R2]                 ;06
BA9:	mov [R1R0], A                 ;05
BAA:	mov A, 0x0                    ;70
BAB:	inc R0                        ;10
BAC:	mov [R1R0], A                 ;05
BAD:	inc R2                        ;14
BAE:	inc R2                        ;14
BAF:	mov A, [R3R2]                 ;06
BB0:	jz A, BB7                     ;B3B7
BB2:	inc A                         ;31
BB3:	jz A, BC9                     ;B3C9
BB5:	mov A, 0xA                    ;7A
BB6:	mov [R1R0], A                 ;05
BB7:	dec R2                        ;15
BB8:	mov A, [R3R2]                 ;06
BB9:	mov R2, A                     ;24
BBA:	dec R0                        ;11
BBB:	jmp BC5                       ;EBC5
BBD:	mov A, 0xA                    ;7A
BBE:	add A, [R1R0]                 ;09
BBF:	mov [R1R0], A                 ;05
BC0:	jnc BC5                       ;CBC5
BC2:	inc R0                        ;10
BC3:	inc [R1R0]                    ;0C
BC4:	dec R0                        ;11
BC5:	mov A, R2                     ;25
BC6:	dec R2                        ;15
BC7:	jnz A, BBD                    ;BBBD
BC9:	mov A, R4                     ;29
BCA:	inc A                         ;31
BCB:	jz A, 8DC                     ;B0DC
BCD:	inc A                         ;31
BCE:	jz A, DF9                     ;B5F9
BD0:	mov A, 0x1                    ;71
BD1:	mov R1R0, 0x05                ;5500
BD3:	mov [R1R0], A                 ;05
BD4:	mov R1R0, 0x57                ;5705
BD6:	mov A, 0x5                    ;75
BD7:	mov [R1R0], A                 ;05
BD8:	mov A, R4                     ;29
BD9:	jz A, BE2                     ;B3E2
BDB:	dec A                         ;3F
BDC:	jz A, 9F0                     ;B1F0
BDE:	dec A                         ;3F
BDF:	jz A, AF0                     ;B2F0
BE1:	ret                           ;2E
BE2:	dec [R1R0]                    ;0D
BE3:	mov R1R0, 0x00                ;5000
BE5:	call DFA                      ;FDFA
BE7:	call DFD                      ;FDFD
BE9:	call 9FA                      ;F9FA
BEB:	jc BFB                        ;C3FB
BED:	call 35E                      ;F35E
BEF:	jc BE7                        ;C3E7
BF1:	mov R1R0, 0x52                ;5205
BF3:	mov A, [R1R0]                 ;04
BF4:	ja1 BFF                       ;8BFF
BF6:	mov A, 0x4                    ;74
BF7:	call 7A9                      ;F7A9
BF9:	jmp 4BD                       ;E4BD
BFB:	mov R1R0, 0x00                ;5000
BFD:	call E0C                      ;FE0C
BFF:	mov R1R0, 0x00                ;5000
C01:	mov R3R2, 0x02                ;6200
C03:	call E73                      ;FE73
C05:	mov R1R0, 0x52                ;5205
C07:	mov A, [R1R0]                 ;04
C08:	ja1 C75                       ;8C75
C0A:	rrc A                         ;02
C0B:	mov A, 0x4                    ;74
C0C:	call 7A9                      ;F7A9
C0E:	jnc C59                       ;CC59
C10:	call 852                      ;F852
C12:	jnc E3B                       ;CE3B
C14:	mov R1R0, 0x18                ;5801
C16:	call C6A                      ;FC6A
C18:	mov R1R0, 0x20                ;5002
C1A:	mov [R1R0], A                 ;05
C1B:	mov R1R0, 0x2C                ;5C02
C1D:	call 813                      ;F813
C1F:	call 924                      ;F924
C21:	mov R3R2, 0x6C                ;6C06
C23:	call 793                      ;F793
C25:	call E21                      ;FE21
C27:	mov R1R0, 0x60                ;5006
C29:	call 813                      ;F813
C2B:	call E79                      ;FE79
C2D:	mov R3R2, 0x14                ;6401
C2F:	mov [R3R2], A                 ;07
C30:	call 9D9                      ;F9D9
C32:	mov R1R0, 0x3F                ;5F03
C34:	mov A, 0x2                    ;72
C35:	mov [R1R0], A                 ;05
C36:	jmp 2FE                       ;E2FE
C38:	mov R3R2, 0x14                ;6401
C3A:	jmp 389                       ;E389
C3C:	mov R3R2, 0x14                ;6401
C3E:	inc [R3R2]                    ;0E
C3F:	mov A, [R3R2]                 ;06
C40:	ja0 C30                       ;8430
C42:	call 9D9                      ;F9D9
C44:	mov R1R0, 0x37                ;5703
C46:	call E60                      ;FE60
C48:	jz A, C4E                     ;B44E
C4A:	call E07                      ;FE07
C4C:	jmp C30                       ;EC30
C4E:	call 858                      ;F858
C50:	jnc C54                       ;CC54
C52:	jmp 4F5                       ;E4F5
C54:	mov A, 0xE                    ;7E
C55:	call 7BC                      ;F7BC
C57:	jmp C68                       ;EC68
C59:	call 858                      ;F858
C5B:	jnc E3B                       ;CE3B
C5D:	mov R1R0, 0x61                ;5106
C5F:	call C6A                      ;FC6A
C61:	dec R0                        ;11
C62:	mov [R1R0], A                 ;05
C63:	call 9D9                      ;F9D9
C65:	mov A, 0x9                    ;79
C66:	call 7A9                      ;F7A9
C68:	jmp 4BD                       ;E4BD
C6A:	inc [R1R0]                    ;0C
C6B:	mov R3R2, 0x81                ;6108
C6D:	mov A, [R3R2]                 ;06
C6E:	add A, 0x4                    ;4004
C70:	xor A, [R1R0]                 ;1B
C71:	jnz A, C68                    ;BC68
C73:	mov [R1R0], A                 ;05
C74:	ret                           ;2E
C75:	mov R1R0, 0x02                ;5200
C77:	call E0C                      ;FE0C
C79:	dec R0                        ;11
C7A:	mov R3R2, 0x09                ;6900
C7C:	call 362                      ;F362
C7E:	jc BF9                        ;C3F9
C80:	mov A, 0xF                    ;7F
C81:	call 962                      ;F962
C83:	mov A, 0x5                    ;75
C84:	call 7A9                      ;F7A9
C86:	mov R1R0, 0x30                ;5003
C88:	mov A, 0xF                    ;7F
C89:	xor A, [R1R0]                 ;1B
C8A:	mov R1R0, 0x02                ;5200
C8C:	call E0D                      ;FE0D
C8E:	dec R0                        ;11
C8F:	mov R3R2, 0x00                ;6000
C91:	call E73                      ;FE73
C93:	mov R1R0, 0x00                ;5000
C95:	mov A, 0x7                    ;77
C96:	call E0D                      ;FE0D
C98:	call 808                      ;F808
C9A:	mov R1R0, 0x0A                ;5A00
C9C:	inc [R1R0]                    ;0C
C9D:	call 9FA                      ;F9FA
C9F:	mov A, R4                     ;29
CA0:	dec A                         ;3F
CA1:	jnz A, E3D                    ;BE3D
CA3:	mov A, 0xF                    ;7F
CA4:	mov R2, A                     ;24
CA5:	call 961                      ;F961
CA7:	mov R1R0, 0x02                ;5200
CA9:	call DFA                      ;FDFA
CAB:	mov A, R2                     ;25
CAC:	dec R2                        ;15
CAD:	jnz A, CA5                    ;BCA5
CAF:	call 7BC                      ;F7BC
CB1:	jmp CB7                       ;ECB7
CB3:	call 9FA                      ;F9FA
CB5:	call 968                      ;F968
CB7:	mov R1R0, 0x00                ;5000
CB9:	call E60                      ;FE60
CBB:	jnz A, CB3                    ;BCB3
CBD:	call 961                      ;F961
CBF:	mov R3R2, 0x2F                ;6F02
CC1:	call 793                      ;F793
CC3:	jmp E3D                       ;EE3D
CC5:	mov A, 0x0                    ;70
CC6:	jtmr DB7                      ;D5B7
CC8:	mov R3R2, 0x00                ;6000
CCA:	mov R1R0, 0x93                ;5309
CCC:	mov A, 0xC                    ;7C
CCD:	add A, [R1R0]                 ;09
CCE:	jnc D69                       ;CD69
CD0:	mov A, 0x0                    ;70
CD1:	mov [R1R0], A                 ;05
CD2:	dec R1                        ;13
CD3:	mov A, 0xF                    ;7F
CD4:	xor A, [R1R0]                 ;1B
CD5:	mov R2, A                     ;24
CD6:	in A, PS                      ;33
CD7:	mov [R1R0], A                 ;05
CD8:	mov A, R2                     ;25
CD9:	or A, [R1R0]                  ;1C
CDA:	xor A, 0xF                    ;430F
CDC:	jz A, CF5                     ;B4F5
CDE:	ja0 D6A                       ;856A
CE0:	ja1 D8A                       ;8D8A
CE2:	call D98                      ;FD98
CE4:	mov R1R0, 0x00                ;5000
CE6:	in A, PS                      ;33
CE7:	xor A, 0xF                    ;430F
CE9:	ja2 CE4                       ;94E4
CEB:	inc R0                        ;10
CEC:	jnz R0, CE6                   ;A4E6
CEE:	inc R1                        ;12
CEF:	jnz R1, CE6                   ;ACE6
CF1:	halt                          ;37
CF2:	nop                           ;3E
CF3:	jmp 061                       ;E061
CF5:	inc R0                        ;10
CF6:	mov A, [R1R0]                 ;04
CF7:	mov R3, A                     ;26
CF8:	in A, PP                      ;34
CF9:	mov [R1R0], A                 ;05
CFA:	mov A, R3                     ;27
CFB:	or A, [R1R0]                  ;1C
CFC:	xor A, 0xF                    ;430F
CFE:	mov R4, A                     ;28
CFF:	and A, 0xC                    ;420C
D01:	mov R1R0, 0x95                ;5509
D03:	jnz A, D0A                    ;BD0A
D05:	mov [R1R0], A                 ;05
D06:	dec R1                        ;13
D07:	mov A, 0x7                    ;77
D08:	and [R1R0], A                 ;1D
D09:	inc R1                        ;12
D0A:	mov A, R4                     ;29
D0B:	ja0 D13                       ;8513
D0D:	inc R0                        ;10
D0E:	mov A, 0x0                    ;70
D0F:	mov [R1R0], A                 ;05
D10:	dec R1                        ;13
D11:	mov A, 0xE                    ;7E
D12:	and [R1R0], A                 ;1D
D13:	mov R1R0, 0x53                ;5305
D15:	mov A, [R1R0]                 ;04
D16:	jz A, D60                     ;B560
D18:	mov A, 0x6                    ;76
D19:	and A, [R1R0]                 ;1A
D1A:	jz A, D34                     ;B534
D1C:	ja1 D60                       ;8D60
D1E:	dec R0                        ;11
D1F:	mov A, [R1R0]                 ;04
D20:	ja1 D43                       ;8D43
D22:	mov R1R0, 0x86                ;5608
D24:	mov A, [R1R0]                 ;04
D25:	rr A                          ;00
D26:	mov A, 0xA                    ;7A
D27:	jnc D2A                       ;CD2A
D29:	mov A, 0xD                    ;7D
D2A:	inc R1                        ;12
D2B:	add A, [R1R0]                 ;09
D2C:	jnc D43                       ;CD43
D2E:	mov A, 0x0                    ;70
D2F:	mov [R1R0], A                 ;05
D30:	dec R1                        ;13
D31:	mov A, 0x1                    ;71
D32:	or [R1R0], A                  ;1F
D33:	mov R3, A                     ;26
D34:	mov R1R0, 0x85                ;5508
D36:	mov A, [R1R0]                 ;04
D37:	ja0 D3F                       ;853F
D39:	in A, PP                      ;34
D3A:	xor A, 0xF                    ;430F
D3C:	ja1 D43                       ;8D43
D3E:	inc [R1R0]                    ;0C
D3F:	mov A, R3                     ;27
D40:	or A, 0x2                     ;4402
D42:	mov R3, A                     ;26
D43:	mov R1R0, 0x85                ;5508
D45:	mov A, [R1R0]                 ;04
D46:	rl A                          ;01
D47:	mov A, 0xA                    ;7A
D48:	jnc D4B                       ;CD4B
D4A:	mov A, 0xE                    ;7E
D4B:	inc R1                        ;12
D4C:	add A, [R1R0]                 ;09
D4D:	jnc D60                       ;CD60
D4F:	mov A, 0x0                    ;70
D50:	mov [R1R0], A                 ;05
D51:	dec R1                        ;13
D52:	mov A, 0x8                    ;78
D53:	or [R1R0], A                  ;1F
D54:	mov A, R4                     ;29
D55:	ja2 D5C                       ;955C
D57:	mov A, R3                     ;27
D58:	or A, 0x8                     ;4408
D5A:	jmp D5F                       ;ED5F
D5C:	mov A, R3                     ;27
D5D:	or A, 0x4                     ;4404
D5F:	mov R3, A                     ;26
D60:	mov R1R0, 0x84                ;5408
D62:	mov A, R3                     ;27
D63:	xor A, 0xF                    ;430F
D65:	or A, [R1R0]                  ;1C
D66:	xor A, 0xF                    ;430F
D68:	mov R3, A                     ;26
D69:	ret                           ;2E
D6A:	mov R1R0, 0x53                ;5305
D6C:	mov A, [R1R0]                 ;04
D6D:	jnz A, D71                    ;BD71
D6F:	jmp 121                       ;E121
D71:	mov R1R0, 0xB7                ;570B
D73:	mov A, 0x8                    ;78
D74:	xor [R1R0], A                 ;1E
D75:	mov A, 0xB                    ;7B
D76:	and [R1R0], A                 ;1D
D77:	mov R1R0, 0x3F                ;5F03
D79:	mov A, 0x2                    ;72
D7A:	xor A, [R1R0]                 ;1B
D7B:	jnz A, D80                    ;BD80
D7D:	mov A, 0x1                    ;71
D7E:	call 9D9                      ;F9D9
D80:	call AF6                      ;FAF6
D82:	call 811                      ;F811
D84:	call D93                      ;FD93
D86:	call DA1                      ;FDA1
D88:	jmp 396                       ;E396
D8A:	mov R3R2, 0x00                ;6000
D8C:	mov R1R0, 0xC3                ;530C
D8E:	mov A, 0x1                    ;71
D8F:	xor [R1R0], A                 ;1E
D90:	mov A, [R1R0]                 ;04
D91:	ja0 D9F                       ;859F
D93:	sound off                     ;4A
D94:	mov R1R0, 0x59                ;5905
D96:	mov A, 0xF                    ;7F
D97:	mov [R1R0], A                 ;05
D98:	mov A, 0xE                    ;7E
D99:	mov R1R0, 0x87                ;5708
D9B:	mov [R1R0], A                 ;05
D9C:	out PA, A                     ;30
D9D:	mov A, [R3R2]                 ;06
D9E:	ret                           ;2E
D9F:	sound 7                       ;4507
DA1:	mov R1R0, 0xC3                ;530C
DA3:	mov A, 0x1                    ;71
DA4:	xor A, [R1R0]                 ;1B
DA5:	mov R1R0, 0x3F                ;5F03
DA7:	or A, [R1R0]                  ;1C
DA8:	ja0 D98                       ;8598
DAA:	mov R1R0, 0xB1                ;510B
DAC:	mov A, [R1R0]                 ;04
DAD:	rl A                          ;01
DAE:	rl A                          ;01
DAF:	mov R1R0, 0xB7                ;570B
DB1:	or A, [R1R0]                  ;1C
DB2:	ja3 D98                       ;9D98
DB4:	mov A, 0xF                    ;7F
DB5:	jmp D99                       ;ED99
DB7:	mov R4, A                     ;28
DB8:	mov R3R2, 0x93                ;6309
DBA:	inc [R3R2]                    ;0E
DBB:	inc R2                        ;14
DBC:	inc [R3R2]                    ;0E
DBD:	mov A, [R3R2]                 ;06
DBE:	xor A, 0x8                    ;4308
DC0:	jnz A, DDE                    ;BDDE
DC2:	mov [R3R2], A                 ;07
DC3:	inc R2                        ;14
DC4:	inc [R3R2]                    ;0E
DC5:	inc R2                        ;14
DC6:	inc [R3R2]                    ;0E
DC7:	inc R2                        ;14
DC8:	inc [R3R2]                    ;0E
DC9:	inc R2                        ;14
DCA:	inc [R3R2]                    ;0E
DCB:	inc R2                        ;14
DCC:	inc [R3R2]                    ;0E
DCD:	mov A, [R3R2]                 ;06
DCE:	jnz A, DDE                    ;BDDE
DD0:	inc R2                        ;14
DD1:	inc [R3R2]                    ;0E
DD2:	inc R2                        ;14
DD3:	inc [R3R2]                    ;0E
DD4:	mov A, [R3R2]                 ;06
DD5:	jnz A, DDE                    ;BDDE
DD7:	inc R2                        ;14
DD8:	inc [R3R2]                    ;0E
DD9:	mov A, [R3R2]                 ;06
DDA:	jnz A, DDE                    ;BDDE
DDC:	inc R2                        ;14
DDD:	inc [R3R2]                    ;0E
DDE:	mov R3R2, 0x16                ;6601
DE0:	mov A, [R3R2]                 ;06
DE1:	jnz A, DE9                    ;BDE9
DE3:	inc R2                        ;14
DE4:	mov A, [R3R2]                 ;06
DE5:	jz A, DEA                     ;B5EA
DE7:	dec [R3R2]                    ;0F
DE8:	dec R2                        ;15
DE9:	dec [R3R2]                    ;0F
DEA:	jnz R4, A2D                   ;DA2D
DEC:	jmp CC8                       ;ECC8
DEE:	jz A, E05                     ;B605
DF0:	dec A                         ;3F
DF1:	inc R0                        ;10
DF2:	jz A, DFF                     ;B5FF
DF4:	dec A                         ;3F
DF5:	jz A, E09                     ;B609
DF7:	dec R0                        ;11
DF8:	dec [R1R0]                    ;0D
DF9:	ret                           ;2E
DFA:	mov A, 0xA                    ;7A
DFB:	jmp E00                       ;EE00
DFD:	mov R1R0, 0x31                ;5103
DFF:	mov A, 0x1                    ;71
E00:	add A, [R1R0]                 ;09
E01:	mov [R1R0], A                 ;05
E02:	inc R0                        ;10
E03:	jnc E06                       ;CE06
E05:	inc [R1R0]                    ;0C
E06:	ret                           ;2E
E07:	mov R1R0, 0x37                ;5703
E09:	mov A, 0xF                    ;7F
E0A:	jmp E0D                       ;EE0D
E0C:	mov A, 0x6                    ;76
E0D:	add A, [R1R0]                 ;09
E0E:	mov [R1R0], A                 ;05
E0F:	inc R0                        ;10
E10:	jnc DF8                       ;CDF8
E12:	ret                           ;2E
E13:	mov R3R2, 0x44                ;6404
E15:	mov R1R0, 0x2C                ;5C02
E17:	mov A, 0x4                    ;74
E18:	mov R4, A                     ;28
E19:	mov A, [R1R0]                 ;04
E1A:	mov [R3R2], A                 ;07
E1B:	inc R0                        ;10
E1C:	inc R2                        ;14
E1D:	dec R4                        ;19
E1E:	jnz R4, E19                   ;DE19
E20:	ret                           ;2E
E21:	mov R1R0, 0x30                ;5003
E23:	mov R3R2, 0x36                ;6603
E25:	mov A, 0x5                    ;75
E26:	jmp E18                       ;EE18
E28:	mov R3R2, 0x44                ;6404
E2A:	jmp E2E                       ;EE2E
E2C:	mov R3R2, 0x1C                ;6C01
E2E:	stc                           ;2B
E2F:	mov R1R0, 0x2C                ;5C02
E31:	mov A, [R3R2]                 ;06
E32:	and A, [R1R0]                 ;1A
E33:	jnz A, E3A                    ;BE3A
E35:	inc R0                        ;10
E36:	inc R2                        ;14
E37:	jnz R0, E31                   ;A631
E39:	clc                           ;2A
E3A:	ret                           ;2E
E3B:	call 961                      ;F961
E3D:	jmp 2FE                       ;E2FE
E3F:	mov R1R0, 0x2E                ;5E02
E41:	mov A, [R1R0]                 ;04
E42:	mov R4, A                     ;28
E43:	dec R0                        ;11
E44:	mov A, [R1R0]                 ;04
E45:	inc R0                        ;10
E46:	mov [R1R0], A                 ;05
E47:	dec R0                        ;11
E48:	dec R0                        ;11
E49:	mov A, [R1R0]                 ;04
E4A:	inc R0                        ;10
E4B:	mov [R1R0], A                 ;05
E4C:	dec R0                        ;11
E4D:	mov A, R4                     ;29
E4E:	mov [R1R0], A                 ;05
E4F:	mov R3R2, 0xB8                ;680B
E51:	mov A, [R1R0]                 ;04
E52:	rrc A                         ;02
E53:	mov [R1R0], A                 ;05
E54:	mov A, [R3R2]                 ;06
E55:	rrc A                         ;02
E56:	mov [R3R2], A                 ;07
E57:	inc R2                        ;14
E58:	inc R2                        ;14
E59:	mov A, R2                     ;25
E5A:	jnz A, E51                    ;BE51
E5C:	inc R0                        ;10
E5D:	jnz R0, E4F                   ;A64F
E5F:	ret                           ;2E
E60:	mov A, [R1R0]                 ;04
E61:	inc R0                        ;10
E62:	or A, [R1R0]                  ;1C
E63:	ret                           ;2E
E64:	mov R1R0, 0x4B                ;5B04
E66:	mov A, 0x0                    ;70
E67:	mov R4, A                     ;28
E68:	mov A, R4                     ;29
E69:	mov [R1R0], A                 ;05
E6A:	mov A, R0                     ;21
E6B:	dec R0                        ;11
E6C:	jnz A, E68                    ;BE68
E6E:	mov A, R1                     ;23
E6F:	dec R1                        ;13
E70:	jnz A, E68                    ;BE68
E72:	ret                           ;2E
E73:	mov A, 0x2                    ;72
E74:	jmp E18                       ;EE18
E76:	mov R1R0, 0x30                ;5003
E78:	mov [R1R0], A                 ;05
E79:	mov R1R0, 0x31                ;5103
E7B:	mov A, 0x0                    ;70
E7C:	mov [R1R0], A                 ;05
E7D:	inc R0                        ;10
E7E:	mov [R1R0], A                 ;05
E7F:	ret                           ;2E
E80:	db 0xE4                       ;E4
E81:	db 0x03                       ;03
E82:	db 0xE8                       ;E8
E83:	db 0x03                       ;03
E84:	db 0xE2                       ;E2
E85:	db 0x03                       ;03
E86:	db 0x06                       ;06
E87:	db 0x60                       ;60
E88:	db 0x4C                       ;4C
E89:	db 0x81                       ;81
E8A:	db 0x8C                       ;8C
E8B:	db 0x41                       ;41
E8C:	db 0x00                       ;00
E8D:	db 0xF1                       ;F1
E8E:	db 0xE4                       ;E4
E8F:	db 0x43                       ;43
E90:	db 0x4E                       ;4E
E91:	db 0x40                       ;40
E92:	db 0xEA                       ;EA
E93:	db 0x03                       ;03
E94:	db 0x2E                       ;2E
E95:	db 0x81                       ;81
E96:	db 0x8E                       ;8E
E97:	db 0x21                       ;21
E98:	db 0x02                       ;02
E99:	db 0x63                       ;63
E9A:	db 0x04                       ;04
E9B:	db 0x41                       ;41
E9C:	mov R1R0, 0x39                ;5903
E9E:	mov A, [R1R0]                 ;04
E9F:	clc                           ;2A
EA0:	rlc A                         ;03
EA1:	mov R3R2, 0x0C                ;6C00
EA3:	mov [R3R2], A                 ;07
EA4:	inc R2                        ;14
EA5:	mov A, 0x4                    ;74
EA6:	rlc A                         ;03
EA7:	mov [R3R2], A                 ;07
EA8:	mov R1R0, 0x2C                ;5C02
EAA:	dec R2                        ;15
EAB:	mov A, [R3R2]                 ;06
EAC:	inc [R3R2]                    ;0E
EAD:	mov R4, A                     ;28
EAE:	inc R2                        ;14
EAF:	mov A, [R3R2]                 ;06
EB0:	dec R2                        ;15
EB1:	read MR0A                     ;4E
EB2:	inc R0                        ;10
EB3:	mov [R1R0], A                 ;05
EB4:	inc R0                        ;10
EB5:	jnz R0, EAB                   ;A6AB
EB7:	dec R0                        ;11
EB8:	mov A, [R1R0]                 ;04
EB9:	xor [R1R0], A                 ;1E
EBA:	mov R1R0, 0x3A                ;5A03
EBC:	and [R1R0], A                 ;1D
EBD:	mov A, [R1R0]                 ;04
EBE:	mov R4, A                     ;28
EBF:	jmp EF7                       ;EEF7
EC1:	mov R3R2, 0x0C                ;6C00
EC3:	mov R1R0, 0x2C                ;5C02
EC5:	mov A, [R1R0]                 ;04
EC6:	rrc A                         ;02
EC7:	mov [R1R0], A                 ;05
EC8:	mov A, [R3R2]                 ;06
EC9:	rlc A                         ;03
ECA:	mov [R3R2], A                 ;07
ECB:	inc R0                        ;10
ECC:	jnz R0, EC5                   ;A6C5
ECE:	inc R2                        ;14
ECF:	mov A, R2                     ;25
ED0:	jnz A, EC3                    ;BEC3
ED2:	mov R1R0, 0x39                ;5903
ED4:	mov A, 0x4                    ;74
ED5:	add A, [R1R0]                 ;09
ED6:	mov R1R0, 0x0C                ;5C00
ED8:	mov R3R2, 0x2C                ;6C02
EDA:	mov A, [R1R0]                 ;04
EDB:	mov [R3R2], A                 ;07
EDC:	inc R0                        ;10
EDD:	inc R2                        ;14
EDE:	jnz R0, EDA                   ;A6DA
EE0:	jc EF6                        ;C6F6
EE2:	dec R2                        ;15
EE3:	mov A, 0x0                    ;70
EE4:	mov [R3R2], A                 ;07
EE5:	dec R2                        ;15
EE6:	mov A, R2                     ;25
EE7:	ja2 EE3                       ;96E3
EE9:	mov R1R0, 0x0B                ;5B00
EEB:	inc R2                        ;14
EEC:	inc R0                        ;10
EED:	mov A, [R1R0]                 ;04
EEE:	jz A, EEC                     ;B6EC
EF0:	mov A, [R1R0]                 ;04
EF1:	mov [R3R2], A                 ;07
EF2:	inc R0                        ;10
EF3:	inc R2                        ;14
EF4:	jnz R0, EF0                   ;A6F0
EF6:	dec R4                        ;19
EF7:	jnz R4, EC1                   ;DEC1
EF9:	ret                           ;2E
EFA:	mov R1R0, 0x36                ;5603
EFC:	mov R3R2, 0x30                ;6003
EFE:	jmp E25                       ;EE25
F00:	db 0xFF                       ;FF
F01:	db 0xBF                       ;BF
F02:	db 0x7F                       ;7F
F03:	db 0x3F                       ;3F
F04:	db 0xFE                       ;FE
F05:	db 0xBE                       ;BE
F06:	db 0x7E                       ;7E
F07:	db 0x3E                       ;3E
F08:	db 0x97                       ;97
F09:	db 0x95                       ;95
F0A:	db 0xFD                       ;FD
F0B:	db 0xBD                       ;BD
F0C:	db 0x7D                       ;7D
F0D:	db 0x3D                       ;3D
F0E:	db 0xFC                       ;FC
F0F:	db 0xBC                       ;BC
F10:	db 0x7C                       ;7C
F11:	db 0x3C                       ;3C
F12:	db 0xD7                       ;D7
F13:	db 0xD5                       ;D5
F14:	db 0xFB                       ;FB
F15:	db 0xBB                       ;BB
F16:	db 0x7B                       ;7B
F17:	db 0x3B                       ;3B
F18:	db 0xFA                       ;FA
F19:	db 0xBA                       ;BA
F1A:	db 0x7A                       ;7A
F1B:	db 0x3A                       ;3A
F1C:	db 0x57                       ;57
F1D:	db 0x55                       ;55
F1E:	db 0xF9                       ;F9
F1F:	db 0xB9                       ;B9
F20:	db 0x79                       ;79
F21:	db 0x39                       ;39
F22:	db 0xF8                       ;F8
F23:	db 0xB8                       ;B8
F24:	db 0x78                       ;78
F25:	db 0x38                       ;38
F26:	db 0x17                       ;17
F27:	db 0x15                       ;15
F28:	db 0xF7                       ;F7
F29:	db 0xB7                       ;B7
F2A:	db 0x77                       ;77
F2B:	db 0x37                       ;37
F2C:	db 0xF6                       ;F6
F2D:	db 0xB6                       ;B6
F2E:	db 0x76                       ;76
F2F:	db 0x36                       ;36
F30:	db 0xD6                       ;D6
F31:	db 0xD4                       ;D4
F32:	db 0xF5                       ;F5
F33:	db 0xB5                       ;B5
F34:	db 0x75                       ;75
F35:	db 0x35                       ;35
F36:	db 0xF4                       ;F4
F37:	db 0xB4                       ;B4
F38:	db 0x74                       ;74
F39:	db 0x34                       ;34
F3A:	db 0x56                       ;56
F3B:	db 0x54                       ;54
F3C:	db 0xF3                       ;F3
F3D:	db 0xB3                       ;B3
F3E:	db 0x73                       ;73
F3F:	db 0x33                       ;33
F40:	db 0xF2                       ;F2
F41:	db 0xB2                       ;B2
F42:	db 0x72                       ;72
F43:	db 0x32                       ;32
F44:	db 0x16                       ;16
F45:	db 0x14                       ;14
F46:	db 0xF1                       ;F1
F47:	db 0xB1                       ;B1
F48:	db 0x71                       ;71
F49:	db 0x31                       ;31
F4A:	db 0xF0                       ;F0
F4B:	db 0xB0                       ;B0
F4C:	db 0x70                       ;70
F4D:	db 0x30                       ;30
F4E:	db 0x96                       ;96
F4F:	db 0x94                       ;94
F50:	db 0xEF                       ;EF
F51:	db 0xAF                       ;AF
F52:	db 0x6F                       ;6F
F53:	db 0x2F                       ;2F
F54:	db 0xEE                       ;EE
F55:	db 0xAE                       ;AE
F56:	db 0x6E                       ;6E
F57:	db 0x2E                       ;2E
F58:	db 0x12                       ;12
F59:	db 0x52                       ;52
F5A:	db 0xED                       ;ED
F5B:	db 0xAD                       ;AD
F5C:	db 0x6D                       ;6D
F5D:	db 0x2D                       ;2D
F5E:	db 0xEC                       ;EC
F5F:	db 0xAC                       ;AC
F60:	db 0x6C                       ;6C
F61:	db 0x2C                       ;2C
F62:	db 0x10                       ;10
F63:	db 0x50                       ;50
F64:	db 0xEB                       ;EB
F65:	db 0xAB                       ;AB
F66:	db 0x6B                       ;6B
F67:	db 0x2B                       ;2B
F68:	db 0xEA                       ;EA
F69:	db 0xAA                       ;AA
F6A:	db 0x6A                       ;6A
F6B:	db 0x2A                       ;2A
F6C:	db 0x0E                       ;0E
F6D:	db 0x4E                       ;4E
F6E:	db 0xE9                       ;E9
F6F:	db 0xA9                       ;A9
F70:	db 0x69                       ;69
F71:	db 0x29                       ;29
F72:	db 0xE8                       ;E8
F73:	db 0xA8                       ;A8
F74:	db 0x68                       ;68
F75:	db 0x28                       ;28
F76:	db 0x0C                       ;0C
F77:	db 0x4C                       ;4C
F78:	db 0xE7                       ;E7
F79:	db 0xA7                       ;A7
F7A:	db 0x67                       ;67
F7B:	db 0x27                       ;27
F7C:	db 0xE6                       ;E6
F7D:	db 0xA6                       ;A6
F7E:	db 0x66                       ;66
F7F:	db 0x26                       ;26
F80:	db 0x0A                       ;0A
F81:	db 0x4A                       ;4A
F82:	db 0xE5                       ;E5
F83:	db 0xA5                       ;A5
F84:	db 0x65                       ;65
F85:	db 0x25                       ;25
F86:	db 0xE4                       ;E4
F87:	db 0xA4                       ;A4
F88:	db 0x64                       ;64
F89:	db 0x24                       ;24
F8A:	db 0x08                       ;08
F8B:	db 0x48                       ;48
F8C:	db 0xE3                       ;E3
F8D:	db 0xA3                       ;A3
F8E:	db 0x63                       ;63
F8F:	db 0x23                       ;23
F90:	db 0xE2                       ;E2
F91:	db 0xA2                       ;A2
F92:	db 0x62                       ;62
F93:	db 0x22                       ;22
F94:	db 0x06                       ;06
F95:	db 0x46                       ;46
F96:	db 0xE1                       ;E1
F97:	db 0xA1                       ;A1
F98:	db 0x61                       ;61
F99:	db 0x21                       ;21
F9A:	db 0xE0                       ;E0
F9B:	db 0xA0                       ;A0
F9C:	db 0x60                       ;60
F9D:	db 0x20                       ;20
F9E:	db 0x04                       ;04
F9F:	db 0x44                       ;44
FA0:	db 0xDF                       ;DF
FA1:	db 0x9F                       ;9F
FA2:	db 0x5F                       ;5F
FA3:	db 0x1F                       ;1F
FA4:	db 0xDE                       ;DE
FA5:	db 0x9E                       ;9E
FA6:	db 0x5E                       ;5E
FA7:	db 0x1E                       ;1E
FA8:	db 0x42                       ;42
FA9:	db 0x40                       ;40
FAA:	db 0xDD                       ;DD
FAB:	db 0x9D                       ;9D
FAC:	db 0x5D                       ;5D
FAD:	db 0x1D                       ;1D
FAE:	db 0xDC                       ;DC
FAF:	db 0x9C                       ;9C
FB0:	db 0x5C                       ;5C
FB1:	db 0x1C                       ;1C
FB2:	db 0x82                       ;82
FB3:	db 0x80                       ;80
FB4:	db 0xDB                       ;DB
FB5:	db 0x9B                       ;9B
FB6:	db 0x5B                       ;5B
FB7:	db 0x1B                       ;1B
FB8:	db 0xDA                       ;DA
FB9:	db 0x9A                       ;9A
FBA:	db 0x5A                       ;5A
FBB:	db 0x1A                       ;1A
FBC:	db 0x02                       ;02
FBD:	db 0x00                       ;00
FBE:	db 0xD9                       ;D9
FBF:	db 0x99                       ;99
FC0:	db 0x59                       ;59
FC1:	db 0x19                       ;19
FC2:	db 0xD8                       ;D8
FC3:	db 0x98                       ;98
FC4:	db 0x58                       ;58
FC5:	db 0x18                       ;18
FC6:	db 0xC2                       ;C2
FC7:	db 0xC0                       ;C0
FC8:	db 0xD4                       ;D4
FC9:	db 0xD6                       ;D6
FCA:	db 0xD8                       ;D8
FCB:	db 0xDA                       ;DA
FCC:	db 0x98                       ;98
FCD:	db 0x94                       ;94
FCE:	db 0x96                       ;96
FCF:	db 0xDC                       ;DC
FD0:	db 0xDE                       ;DE
FD1:	db 0xE0                       ;E0
FD2:	db 0xE2                       ;E2
FD3:	db 0xA0                       ;A0
FD4:	db 0x9C                       ;9C
FD5:	db 0x9E                       ;9E
FD6:	db 0x97                       ;97
FD7:	db 0xD7                       ;D7
FD8:	db 0x57                       ;57
FD9:	db 0x03                       ;03
FDA:	db 0x43                       ;43
FDB:	db 0x83                       ;83
FDC:	db 0xC3                       ;C3
FDD:	db 0x99                       ;99
FDE:	db 0xD9                       ;D9
FDF:	db 0x59                       ;59
FE0:	db 0x09                       ;09
FE1:	db 0x49                       ;49
FE2:	db 0x89                       ;89
FE3:	db 0xC9                       ;C9
FE4:	db 0x8B                       ;8B
FE5:	db 0xCB                       ;CB
FE6:	db 0x4B                       ;4B
FE7:	db 0x0D                       ;0D
FE8:	db 0x4D                       ;4D
FE9:	db 0x8D                       ;8D
FEA:	db 0xCD                       ;CD
FEB:	db 0x9B                       ;9B
FEC:	db 0xDB                       ;DB
FED:	db 0x5B                       ;5B
FEE:	db 0x0F                       ;0F
FEF:	db 0x4F                       ;4F
FF0:	db 0x8F                       ;8F
FF1:	db 0xCF                       ;CF
FF2:	db 0x7E                       ;7E
FF3:	db 0x30                       ;30
FF4:	db 0x6D                       ;6D
FF5:	db 0x79                       ;79
FF6:	db 0x33                       ;33
FF7:	db 0x5B                       ;5B
FF8:	db 0x5F                       ;5F
FF9:	db 0x70                       ;70
FFA:	db 0x7F                       ;7F
FFB:	db 0x7B                       ;7B
FFC:	db 0x00                       ;00
FFD:	db 0x22                       ;22
FFE:	db 0x16                       ;16
FFF:	db 0x47                       ;47
