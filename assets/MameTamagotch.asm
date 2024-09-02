000:	jmp 00B                       ;E00B
002:	db 0x2F                       ;2F
003:	db 0x2F                       ;2F
004:	jmp 00A                       ;E00A
006:	db 0x2F                       ;2F
007:	db 0x2F                       ;2F
008:	jmp 00A                       ;E00A
00A:	reti                          ;2F
00B:	di                            ;2D
00C:	mov R1R0, 0x00                ;5000
00E:	mov A, 0x0                    ;70
00F:	mov [R1R0], A                 ;05
010:	inc R0                        ;10
011:	jnz R0, 00E                   ;A00E
013:	inc R1                        ;12
014:	mov A, R1                     ;23
015:	sub A, 0xA                    ;410A
017:	jnz R1, 00E                   ;A80E
019:	call D45                      ;FD45
01B:	timer 0x9B                    ;47
01D:	timer on                      ;38

01E:	call sound                      ;F02E
020:	jmp 147                       ;E147
022:	call sound                      ;F02E
024:	jmp 057                       ;E057
026:	jtmr 02A                      ;D02A
028:	jmp 026                       ;E026
02A:	timer 0x9B                    ;47
02C:	jmp 01E                       ;E01E

sound:
02E:	mov R1R0, 0x1C                ;5C01
030:	in A, PP                      ;34
031:	xor A, 0xF                    ;430F
033:	and [R1R0], A                 ;1D
034:	inc R0                        ;10
035:	in A, PS                      ;33
036:	xor A, 0xF                    ;430F
038:	and [R1R0], A                 ;1D
039:	mov R1R0, 0x5F                ;5F05
03B:	mov A, 0x2                    ;72
03C:	and A, [R1R0]                 ;1A
03D:	jz A, 04B                     ;B04B
03F:	mov R1R0, 0x7C                ;5C07
041:	mov A, [R1R0]                 ;04
042:	jz A, 04C                     ;B04C
044:	sound one                     ;48
045:	mov A, [R1R0]                 ;04
046:	sound A                       ;4B
047:	mov A, 0x0                    ;70
048:	mov [R1R0], A                 ;05
049:	jmp 04C                       ;E04C
04B:	sound off                     ;4A
04C:	mov R1R0, 0x3E                ;5E03
04E:	mov A, TMRL                   ;3A
04F:	adc A, [R1R0]                 ;08
050:	mov [R1R0], A                 ;05
051:	adc A, [R1R0]                 ;08
052:	mov A, TMRL                   ;3A
053:	adc A, [R1R0]                 ;08
054:	inc R0                        ;10
055:	mov [R1R0], A                 ;05
056:	ret                           ;2E

draw:
057:	call D67                      ;FD67
059:	jz A, 026                     ;B026
05B:	inc A                         ;31
05C:	jz A, 026                     ;B026
05E:	mov R1R0, 0x5E                ;5E05
060:	mov R3R2, 0xFE                ;6E0F
062:	mov A, [R1R0]                 ;04
063:	mov [R3R2], A                 ;07
064:	inc R0                        ;10
065:	inc R2                        ;14
066:	mov A, [R1R0]                 ;04
067:	mov [R3R2], A                 ;07
068:	jmp C9C                       ;EC9C   ;draw right side
06A:	call D67                      ;FD67
06C:	dec A                         ;3F
06D:	jz A, 083                     ;B083
06F:	dec A                         ;3F
070:	jz A, 026                     ;B026
072:	dec A                         ;3F
073:	jz A, 098                     ;B098
075:	dec A                         ;3F
076:	jz A, 10F                     ;B10F
078:	dec A                         ;3F
079:	jz A, 128                     ;B128
07B:	dec A                         ;3F
07C:	jz A, 136                     ;B136
07E:	dec A                         ;3F
07F:	jz A, 138                     ;B138
081:	jmp 026                       ;E026
083:	mov R1R0, 0x94                ;5409
085:	mov [R1R0], A                 ;05
086:	mov A, 0xA                    ;7A
087:	mov R1R0, 0x90                ;5009
089:	mov [R1R0], A                 ;05
08A:	inc R0                        ;10
08B:	mov A, 0xC                    ;7C
08C:	mov [R1R0], A                 ;05
08D:	inc R0                        ;10
08E:	mov A, 0xB                    ;7B
08F:	mov [R1R0], A                 ;05
090:	inc R0                        ;10
091:	mov R3R2, 0x5B                ;6B05
093:	mov A, [R3R2]                 ;06
094:	inc A                         ;31
095:	mov [R1R0], A                 ;05
096:	jmp C2E                       ;EC2E  ;draw level select
098:	mov R3R2, 0x1A                ;6A01
09A:	mov A, [R3R2]                 ;06
09B:	jnz A, 0A0                    ;B8A0
09D:	mov A, 0x0                    ;70
09E:	jmp 0A9                       ;E0A9
0A0:	mov R1R0, 0x1B                ;5B01
0A2:	mov A, [R1R0]                 ;04
0A3:	jz A, 0B5                     ;B0B5
0A5:	rr A                          ;00
0A6:	rr A                          ;00
0A7:	and A, 0x1                    ;4201
0A9:	call EED                      ;FEED  	;!
0AB:	jmp B28                       ;EB28
0AD:	call D67                      ;FD67
0AF:	sub A, 0x3                    ;4103
0B1:	jz A, 0E7                     ;B0E7
0B3:	jmp 026                       ;E026
0B5:	mov R3R2, 0x1A                ;6A01
0B7:	mov A, [R3R2]                 ;06
0B8:	sub A, 0x5                    ;4105
0BA:	jz A, 09D                     ;B09D
0BC:	mov A, 0x1                    ;71
0BD:	mov R1R0, 0x99                ;5909
0BF:	mov [R1R0], A                 ;05
0C0:	mov R1R0, 0x2B                ;5B02
0C2:	mov A, [R1R0]                 ;04
0C3:	mov R1R0, 0x2D                ;5D02
0C5:	sub A, [R1R0]                 ;0B
0C6:	jnc 0CC                       ;C8CC
0C8:	mov R1R0, 0x2B                ;5B02
0CA:	jmp 0CE                       ;E0CE
0CC:	mov R1R0, 0x2D                ;5D02
0CE:	mov A, [R1R0]                 ;04
0CF:	mov R1R0, 0x99                ;5909
0D1:	sub A, [R1R0]                 ;0B
0D2:	mov R4, A                     ;28
0D3:	inc A                         ;31
0D4:	jz A, 0E0                     ;B0E0
0D6:	mov A, R4                     ;29
0D7:	mov R1R0, 0x91                ;5109
0D9:	mov [R1R0], A                 ;05
0DA:	mov R1R0, 0x97                ;5709
0DC:	call D52                      ;FD52
0DE:	jmp B28                       ;EB28
0E0:	mov R1R0, 0x99                ;5909
0E2:	dec [R1R0]                    ;0D
0E3:	mov A, [R1R0]                 ;04
0E4:	inc A                         ;31
0E5:	jnz A, 0C0                    ;B8C0
0E7:	mov R1R0, 0x1B                ;5B01
0E9:	mov A, [R1R0]                 ;04
0EA:	jz A, 101                     ;B101
0EC:	mov R3R2, 0x90                ;6009
0EE:	mov R1R0, 0x8C                ;5C08
0F0:	call D2E                      ;FD2E
0F2:	mov R3R2, 0x90                ;6009
0F4:	mov A, [R3R2]                 ;06
0F5:	jnz A, 107                    ;B907
0F7:	mov A, 0xA                    ;7A
0F8:	mov [R3R2], A                 ;07
0F9:	inc R2                        ;14
0FA:	mov A, R2                     ;25
0FB:	sub A, 0x4                    ;4104
0FD:	jnz A, 0F4                    ;B8F4
0FF:	jmp 107                       ;E107
101:	mov R3R2, 0x90                ;6009
103:	mov R1R0, 0x4C                ;5C04
105:	call D2E                      ;FD2E
107:	mov R3R2, 0x94                ;6409
109:	mov A, 0x1                    ;71
10A:	mov [R3R2], A                 ;07
10B:	jmp C2E                       ;EC2E
10D:	jmp 026                       ;E026
10F:	mov R1R0, 0x1B                ;5B01
111:	mov A, [R1R0]                 ;04
112:	jnz A, 0A0                    ;B8A0
114:	mov R1R0, 0x91                ;5109
116:	mov A, 0x2                    ;72
117:	mov [R1R0], A                 ;05
118:	mov R1R0, 0x97                ;5709
11A:	call D52                      ;FD52
11C:	jmp B28                       ;EB28
11E:	mov R1R0, 0x91                ;5109
120:	inc [R1R0]                    ;0C
121:	mov A, [R1R0]                 ;04
122:	sub A, 0x5                    ;4105
124:	jnz A, 11C                    ;B91C
126:	jmp 026                       ;E026
128:	mov R1R0, 0x90                ;5009
12A:	mov R4, 0x4                   ;4604
12C:	mov A, 0xA                    ;7A
12D:	mov [R1R0], A                 ;05
12E:	inc R0                        ;10
12F:	dec R4                        ;19
130:	jnz R4, 12C                   ;D92C
132:	mov A, 0x0                    ;70
133:	mov [R1R0], A                 ;05
134:	jmp 10B                       ;E10B
136:	jmp 026                       ;E026
138:	mov R1R0, 0x1E                ;5E01
13A:	mov A, [R1R0]                 ;04
13B:	ja3 143                       ;9943
13D:	mov R1R0, 0x5E                ;5E05
13F:	mov A, 0x2                    ;72
140:	or [R1R0], A                  ;1F
141:	jmp 145                       ;E145
143:	call E2A                      ;FE2A
145:	jmp 026                       ;E026

147:	mov R1R0, 0x8A                ;5A08
149:	mov R3R2, 0x8B                ;6B08
14B:	call DD6                      ;FDD6
14D:	mov R1R0, 0x1E                ;5E01
14F:	inc [R1R0]                    ;0C
150:	mov A, [R1R0]                 ;04
151:	jnz A, 155                    ;B955
153:	inc R0                        ;10
154:	inc [R1R0]                    ;0C
155:	mov R1R0, 0x1C                ;5C01
157:	mov A, [R1R0]                 ;04
158:	mov R2, A                     ;24
159:	inc R0                        ;10
15A:	mov A, [R1R0]                 ;04
15B:	mov R3, A                     ;26
15C:	mov R1R0, 0x0E                ;5E00
15E:	mov A, R2                     ;25
15F:	xor A, [R1R0]                 ;1B
160:	mov R1R0, 0x0C                ;5C00
162:	mov [R1R0], A                 ;05
163:	mov A, R2                     ;25
164:	and [R1R0], A                 ;1D
165:	mov R1R0, 0x0E                ;5E00
167:	mov [R1R0], A                 ;05
168:	inc R0                        ;10
169:	mov A, R3                     ;27
16A:	xor A, [R1R0]                 ;1B
16B:	mov R1R0, 0x0D                ;5D00
16D:	mov [R1R0], A                 ;05
16E:	mov A, R3                     ;27
16F:	and [R1R0], A                 ;1D
170:	mov R1R0, 0x0F                ;5F00
172:	mov [R1R0], A                 ;05
173:	mov R1R0, 0x1C                ;5C01
175:	in A, PP                      ;34
176:	xor A, 0xF                    ;430F
178:	mov [R1R0], A                 ;05
179:	inc R0                        ;10
17A:	in A, PS                      ;33
17B:	xor A, 0xF                    ;430F
17D:	and A, 0x7                    ;4207
17F:	mov [R1R0], A                 ;05
180:	dec R0                        ;11
181:	or A, [R1R0]                  ;1C
182:	mov R1R0, 0x7D                ;5D07
184:	jnz A, 192                    ;B992
186:	inc [R1R0]                    ;0C
187:	mov A, [R1R0]                 ;04
188:	jnz A, 190                    ;B990
18A:	inc R0                        ;10
18B:	jnz R0, 186                   ;A186
18D:	sound off                     ;4A
18E:	halt                          ;37
18F:	nop                           ;3E
190:	jmp 197                       ;E197
192:	mov A, 0x0                    ;70
193:	mov [R1R0], A                 ;05
194:	inc R0                        ;10
195:	jnz R0, 193                   ;A193
197:	call D67                      ;FD67
199:	jz A, 2B3                     ;B2B3
19B:	inc A                         ;31
19C:	jz A, 2D2                     ;B2D2
19E:	call D5B                      ;FD5B
1A0:	mov R3R2, 0x5F                ;6F05
1A2:	mov A, 0x8                    ;78
1A3:	and A, [R1R0]                 ;1A
1A4:	jz A, 1AE                     ;B1AE
1A6:	mov A, [R3R2]                 ;06
1A7:	xor A, 0x2                    ;4302
1A9:	mov [R3R2], A                 ;07
1AA:	mov A, 0x9                    ;79
1AB:	mov R3R2, 0x7C                ;6C07
1AD:	mov [R3R2], A                 ;07
1AE:	call D67                      ;FD67
1B0:	sub A, 0x3                    ;4103
1B2:	jz A, 1B8                     ;B1B8
1B4:	dec A                         ;3F
1B5:	dec A                         ;3F
1B6:	jnz A, 1C7                    ;B9C7
1B8:	call D57                      ;FD57
1BA:	and A, 0x2                    ;4202
1BC:	jz A, 1C7                     ;B1C7
1BE:	mov A, [R3R2]                 ;06
1BF:	xor A, 0x6                    ;4306
1C1:	mov [R3R2], A                 ;07
1C2:	mov A, 0x5                    ;75
1C3:	call D5F                      ;FD5F
1C5:	jmp 022                       ;E022

1C7:	mov A, [R3R2]                 ;06
1C8:	jz A, 23D                     ;B23D
1CA:	dec A                         ;3F
1CB:	jz A, 33E                     ;B33E
1CD:	dec A                         ;3F
1CE:	jz A, 38A                     ;B38A
1D0:	dec A                         ;3F
1D1:	jz A, 487                     ;B487
1D3:	dec A                         ;3F
1D4:	jz A, 6F3                     ;B6F3
1D6:	dec A                         ;3F
1D7:	jz A, 2B1                     ;B2B1
1D9:	dec A                         ;3F
1DA:	jz A, 7D3                     ;B7D3
1DC:	dec A                         ;3F
1DD:	jz A, 7F4                     ;B7F4
1DF:	dec A                         ;3F
1E0:	jz A, 217                     ;B217
1E2:	mov A, 0x1                    ;71
1E3:	call EC9                      ;FEC9
1E5:	jnz A, 215                    ;BA15
1E7:	mov A, 0x4                    ;74
1E8:	call D5F                      ;FD5F
1EA:	mov R1R0, 0x87                ;5708
1EC:	mov A, [R1R0]                 ;04
1ED:	mov R1, A                     ;22
1EE:	mov A, 0x0                    ;70
1EF:	mov R0, A                     ;20
1F0:	mov A, 0x0                    ;70
1F1:	mov [R1R0], A                 ;05
1F2:	inc R0                        ;10
1F3:	mov A, R0                     ;21
1F4:	sub A, 0x5                    ;4105
1F6:	jnz A, 1F0                    ;B9F0
1F8:	mov R1R0, 0x87                ;5708
1FA:	mov A, [R1R0]                 ;04
1FB:	mov R1R0, 0x91                ;5109
1FD:	mov [R1R0], A                 ;05
1FE:	mov R1R0, 0x97                ;5709
200:	call D52                      ;FD52
202:	jmp B28                       ;EB28
204:	mov R1R0, 0x87                ;5708
206:	dec [R1R0]                    ;0D
207:	mov A, [R1R0]                 ;04
208:	inc A                         ;31
209:	jnz A, 215                    ;BA15
20B:	mov A, 0xF                    ;7F
20C:	call D5F                      ;FD5F
20E:	mov R1R0, 0x8A                ;5A08
210:	call D52                      ;FD52
212:	mov A, 0x6                    ;76
213:	call D63                      ;FD63
215:	jmp 022                       ;E022
217:	mov R3R2, 0x2F                ;6F02
219:	mov A, [R3R2]                 ;06
21A:	jz A, 23F                     ;B23F
21C:	dec A                         ;3F
21D:	jz A, 23F                     ;B23F
21F:	dec A                         ;3F
220:	jz A, 245                     ;B245
222:	dec A                         ;3F
223:	jz A, 278                     ;B278
225:	call EE1                      ;FEE1
227:	jnc 230                       ;CA30
229:	mov A, 0x3                    ;73
22A:	call D63                      ;FD63
22C:	call E1E                      ;FE1E
22E:	jmp AB4                       ;EAB4
230:	mov R1R0, 0x1E                ;5E01
232:	mov A, [R1R0]                 ;04
233:	ja3 23B                       ;9A3B
235:	mov R1R0, 0x5E                ;5E05
237:	mov A, 0x4                    ;74
238:	or [R1R0], A                  ;1F
239:	jmp 23D                       ;E23D
23B:	call E1E                      ;FE1E
23D:	jmp 022                       ;E022
23F:	call EE1                      ;FEE1
241:	jnc 269                       ;CA69
243:	jmp 25B                       ;E25B
245:	mov R3R2, 0x8A                ;6A08
247:	mov A, [R3R2]                 ;06
248:	sub A, 0xC                    ;410C
24A:	jnc 269                       ;CA69
24C:	mov R1R0, 0x1B                ;5B01
24E:	dec [R1R0]                    ;0D
24F:	mov A, [R1R0]                 ;04
250:	jz A, 25B                     ;B25B
252:	mov A, 0x6                    ;76
253:	call D5F                      ;FD5F
255:	mov R1R0, 0x8A                ;5A08
257:	call D52                      ;FD52
259:	jmp 269                       ;E269
25B:	call ED7                      ;FED7
25D:	mov A, 0xD                    ;7D
25E:	call D5F                      ;FD5F
260:	mov R1R0, 0x8A                ;5A08
262:	call D52                      ;FD52
264:	mov A, 0x3                    ;73
265:	call D63                      ;FD63
267:	jmp 022                       ;E022
269:	mov R1R0, 0x1E                ;5E01
26B:	mov A, [R1R0]                 ;04
26C:	ja3 272                       ;9A72
26E:	call ED7                      ;FED7
270:	jmp 276                       ;E276
272:	mov A, 0x0                    ;70
273:	mov R3R2, 0x0A                ;6A00
275:	mov [R3R2], A                 ;07
276:	jmp 022                       ;E022
278:	mov R3R2, 0x8A                ;6A08
27A:	mov A, [R3R2]                 ;06
27B:	sub A, 0xA                    ;410A
27D:	jnc 2A6                       ;CAA6
27F:	mov R1R0, 0x1B                ;5B01
281:	dec [R1R0]                    ;0D
282:	mov A, [R1R0]                 ;04
283:	jz A, 28E                     ;B28E
285:	mov A, 0x2                    ;72
286:	call D5F                      ;FD5F
288:	mov R1R0, 0x8A                ;5A08
28A:	call D52                      ;FD52
28C:	jmp 2A6                       ;E2A6
28E:	mov R1R0, 0x5E                ;5E05
290:	mov A, 0x4                    ;74
291:	and A, [R1R0]                 ;1A
292:	jnz A, 2A0                    ;BAA0
294:	mov R1R0, 0x1A                ;5A01
296:	mov A, 0x0                    ;70
297:	mov [R1R0], A                 ;05
298:	call E19                      ;FE19
29A:	mov R3R2, 0x8B                ;6B08
29C:	mov A, 0x2                    ;72
29D:	mov [R3R2], A                 ;07
29E:	jmp 264                       ;E264
2A0:	mov A, 0x4                    ;74
2A1:	call D6B                      ;FD6B
2A3:	mov A, 0x1                    ;71
2A4:	jmp 3F9                       ;E3F9
2A6:	mov R1R0, 0x1E                ;5E01
2A8:	mov A, [R1R0]                 ;04
2A9:	ja3 2AF                       ;9AAF
2AB:	call E19                      ;FE19
2AD:	jmp 2B1                       ;E2B1
2AF:	call E25                      ;FE25
2B1:	jmp 022                       ;E022
2B3:	mov A, 0xC                    ;7C
2B4:	call EC9                      ;FEC9
2B6:	jz A, 022                     ;B022
2B8:	mov A, 0x2                    ;72
2B9:	mov R1R0, 0x5F                ;5F05
2BB:	or [R1R0], A                  ;1F
2BC:	mov R1R0, 0x0F                ;5F00
2BE:	mov A, [R1R0]                 ;04
2BF:	ja2 2CD                       ;92CD
2C1:	mov A, 0xB                    ;7B
2C2:	call D5F                      ;FD5F
2C4:	call D50                      ;FD50
2C6:	mov A, 0x1                    ;71
2C7:	call D63                      ;FD63
2C9:	call D45                      ;FD45
2CB:	jmp 022                       ;E022
2CD:	mov A, 0xF                    ;7F
2CE:	call D63                      ;FD63
2D0:	jmp 339                       ;E339
2D2:	call EC8                      ;FEC8
2D4:	jnz A, 30B                    ;BB0B
2D6:	mov R1R0, 0x3C                ;5C03
2D8:	mov A, [R1R0]                 ;04
2D9:	jz A, 30B                     ;B30B
2DB:	call D45                      ;FD45
2DD:	mov R1R0, 0x3A                ;5A03
2DF:	inc [R1R0]                    ;0C
2E0:	inc [R1R0]                    ;0C
2E1:	mov A, [R1R0]                 ;04
2E2:	mov R2, A                     ;24
2E3:	inc R0                        ;10
2E4:	jnz A, 2EC                    ;BAEC
2E6:	inc [R1R0]                    ;0C
2E7:	mov A, [R1R0]                 ;04
2E8:	jnz R1, 2EC                   ;AAEC
2EA:	mov A, 0xB                    ;7B
2EB:	mov [R1R0], A                 ;05
2EC:	mov A, [R1R0]                 ;04
2ED:	mov R3, A                     ;26
2EE:	mov A, 0xF                    ;7F
2EF:	mov [R3R2], A                 ;07
2F0:	inc R2                        ;14
2F1:	mov [R3R2], A                 ;07
2F2:	dec R2                        ;15
2F3:	inc R3                        ;16
2F4:	inc R3                        ;16
2F5:	mov A, R2                     ;25
2F6:	and A, 0x8                    ;4208
2F8:	jz A, 2FB                     ;B2FB
2FA:	inc R3                        ;16
2FB:	mov A, R3                     ;27
2FC:	sub A, 0x3                    ;4103
2FE:	jc 303                        ;C303
300:	sub A, 0x2                    ;4102
302:	mov R3, A                     ;26
303:	mov A, R2                     ;25
304:	add A, 0x8                    ;4008
306:	mov R2, A                     ;24
307:	mov A, 0xF                    ;7F
308:	mov [R3R2], A                 ;07
309:	inc R2                        ;14
30A:	mov [R3R2], A                 ;07
30B:	mov A, 0x0                    ;70
30C:	mov R2, A                     ;24
30D:	mov R4, 0x4                   ;4604
30F:	mov R1R0, 0x0C                ;5C00
311:	mov A, [R1R0]                 ;04
312:	rrc A                         ;02
313:	jc 327                        ;C327
315:	inc R2                        ;14
316:	dec R4                        ;19
317:	jnz R4, 312                   ;DB12
319:	inc R0                        ;10
31A:	mov A, [R1R0]                 ;04
31B:	mov R4, 0x2                   ;4602
31D:	rrc A                         ;02
31E:	rrc A                         ;02
31F:	jc 327                        ;C327
321:	inc R2                        ;14
322:	dec R4                        ;19
323:	jnz R4, 31E                   ;DB1E
325:	jmp 022                       ;E022
327:	mov A, R2                     ;25
328:	sound A                       ;4B
329:	mov R1R0, 0x3C                ;5C03
32B:	mov A, 0x1                    ;71
32C:	xor [R1R0], A                 ;1E
32D:	mov A, [R1R0]                 ;04
32E:	jz A, 339                     ;B339
330:	mov A, 0xB                    ;7B
331:	mov R1R0, 0x3B                ;5B03
333:	mov [R1R0], A                 ;05
334:	dec R0                        ;11
335:	mov A, 0x0                    ;70
336:	mov [R1R0], A                 ;05
337:	jmp 022                       ;E022
339:	mov A, 0xF                    ;7F
33A:	call D46                      ;FD46
33C:	jmp 022                       ;E022
33E:	mov A, 0x0                    ;70
33F:	mov R1R0, 0x0A                ;5A00
341:	mov [R1R0], A                 ;05
342:	call E25                      ;FE25
344:	call E2A                      ;FE2A
346:	call E1E                      ;FE1E
348:	call D57                      ;FD57
34A:	ja2 356                       ;9356
34C:	dec R0                        ;11
34D:	mov A, [R1R0]                 ;04
34E:	mov R1R0, 0x5B                ;5B05
350:	ja0 374                       ;8374
352:	ja1 377                       ;8B77
354:	jmp 388                       ;E388
356:	mov R3R2, 0x6C                ;6C06
358:	mov R1R0, 0x5B                ;5B05
35A:	mov A, [R1R0]                 ;04
35B:	call EC4                      ;FEC4
35D:	mov A, 0xC                    ;7C
35E:	sub A, [R1R0]                 ;0B
35F:	mov [R3R2], A                 ;07
360:	mov R1R0, 0x4C                ;5C04
362:	call D52                      ;FD52
364:	inc R0                        ;10
365:	call D52                      ;FD52
367:	mov R1R0, 0x4A                ;5A04
369:	call D52                      ;FD52
36B:	dec R0                        ;11
36C:	mov A, 0x1                    ;71
36D:	mov [R1R0], A                 ;05
36E:	mov A, 0x2                    ;72
36F:	call D63                      ;FD63
371:	mov A, 0x9                    ;79
372:	jmp 386                       ;E386
374:	inc [R1R0]                    ;0C
375:	jmp 378                       ;E378
377:	dec [R1R0]                    ;0D
378:	mov A, [R1R0]                 ;04
379:	inc A                         ;31
37A:	jnz A, 37F                    ;BB7F
37C:	mov A, 0x2                    ;72
37D:	jmp 384                       ;E384
37F:	sub A, 0x4                    ;4104
381:	jnz A, 385                    ;BB85
383:	mov A, 0x0                    ;70
384:	mov [R1R0], A                 ;05
385:	mov A, 0x5                    ;75
386:	call D5F                      ;FD5F
388:	jmp 022                       ;E022
38A:	call E06                      ;FE06
38C:	mov A, 0x0                    ;70
38D:	call EED                      ;FEED
38F:	jmp B28                       ;EB28
391:	mov R1R0, 0x6A                ;5A06
393:	call D52                      ;FD52
395:	mov R1R0, 0x1A                ;5A01
397:	call D52                      ;FD52
399:	mov R1R0, 0x4A                ;5A04
39B:	mov A, [R1R0]                 ;04
39C:	sub A, 0x3                    ;4103
39E:	jz A, 3A8                     ;B3A8
3A0:	sub A, 0x2                    ;4102
3A2:	jz A, 3A8                     ;B3A8
3A4:	sub A, 0x2                    ;4102
3A6:	jnz A, 3B8                    ;BBB8
3A8:	mov R1R0, 0x5B                ;5B05
3AA:	mov A, [R1R0]                 ;04
3AB:	rlc A                         ;03
3AC:	and A, 0xE                    ;420E
3AE:	call EC4                      ;FEC4
3B0:	mov A, 0x7                    ;77
3B1:	sub A, [R1R0]                 ;0B
3B2:	mov R1R0, 0x6C                ;5C06
3B4:	sub A, [R1R0]                 ;0B
3B5:	jz A, 3B8                     ;B3B8
3B7:	dec [R1R0]                    ;0D
3B8:	mov R1R0, 0x6A                ;5A06
3BA:	call D52                      ;FD52
3BC:	mov R1R0, 0x81                ;5108
3BE:	mov A, 0x0                    ;70
3BF:	mov [R1R0], A                 ;05
3C0:	call E25                      ;FE25
3C2:	mov R3R2, 0x4A                ;6A04
3C4:	mov A, [R3R2]                 ;06
3C5:	dec A                         ;3F
3C6:	jz A, 408                     ;B408
3C8:	dec A                         ;3F
3C9:	jz A, 415                     ;B415
3CB:	dec A                         ;3F
3CC:	jz A, 41A                     ;B41A
3CE:	dec A                         ;3F
3CF:	jz A, 423                     ;B423
3D1:	dec A                         ;3F
3D2:	jz A, 428                     ;B428
3D4:	dec A                         ;3F
3D5:	jz A, 406                     ;B406
3D7:	dec A                         ;3F
3D8:	jz A, 43A                     ;B43A
3DA:	mov R3R2, 0x0A                ;6A00
3DC:	mov A, [R3R2]                 ;06
3DD:	sub A, 0xA                    ;410A
3DF:	jnz A, 406                    ;BC06
3E1:	mov R1R0, 0x7A                ;5A07
3E3:	mov A, [R1R0]                 ;04
3E4:	sub A, 0xB                    ;410B
3E6:	jnz A, 406                    ;BC06
3E8:	inc R0                        ;10
3E9:	mov A, [R1R0]                 ;04
3EA:	sub A, 0x1                    ;4101
3EC:	jnz A, 406                    ;BC06
3EE:	mov A, 0xD                    ;7D
3EF:	call D6F                      ;FD6F
3F1:	mov A, 0x2                    ;72
3F2:	call D6B                      ;FD6B
3F4:	mov A, 0x4                    ;74
3F5:	mov R1R0, 0x1B                ;5B01
3F7:	mov [R1R0], A                 ;05
3F8:	mov A, 0x6                    ;76
3F9:	call D5F                      ;FD5F
3FB:	mov R1R0, 0x8A                ;5A08
3FD:	call D52                      ;FD52
3FF:	call D50                      ;FD50
401:	mov A, 0x8                    ;78
402:	call D63                      ;FD63
404:	jmp 022                       ;E022
406:	jmp 25B                       ;E25B
408:	mov R1R0, 0x7A                ;5A07
40A:	call D52                      ;FD52
40C:	mov A, 0x0                    ;70
40D:	call D6B                      ;FD6B
40F:	mov A, 0x1                    ;71
410:	call D6F                      ;FD6F
412:	mov A, 0x8                    ;78
413:	jmp 3F9                       ;E3F9
415:	mov A, 0x2                    ;72
416:	call D6F                      ;FD6F
418:	jmp 406                       ;E406
41A:	mov A, 0x3                    ;73
41B:	call D6F                      ;FD6F
41D:	mov A, 0x1                    ;71
41E:	call D6B                      ;FD6B
420:	mov A, 0x1                    ;71
421:	jmp 3F9                       ;E3F9
423:	mov A, 0x4                    ;74
424:	call D6F                      ;FD6F
426:	jmp 3F1                       ;E3F1
428:	mov R1R0, 0x0A                ;5A00
42A:	call E2F                      ;FE2F
42C:	call DE8                      ;FDE8
42E:	call EAB                      ;FEAB
430:	jz A, 435                     ;B435
432:	mov A, 0x7                    ;77
433:	jmp 436                       ;E436
435:	mov A, 0x5                    ;75
436:	call D6F                      ;FD6F
438:	jmp 3F1                       ;E3F1
43A:	mov R3R2, 0x0A                ;6A00
43C:	mov A, [R3R2]                 ;06
43D:	sub A, 0x5                    ;4105
43F:	jz A, 468                     ;B468
441:	mov R1R0, 0x1E                ;5E01
443:	call E2F                      ;FE2F
445:	call DE8                      ;FDE8
447:	call EAB                      ;FEAB
449:	jz A, 44E                     ;B44E
44B:	mov A, 0x8                    ;78
44C:	jmp 483                       ;E483
44E:	mov R1R0, 0x1A                ;5A01
450:	call E2F                      ;FE2F
452:	call DE8                      ;FDE8
454:	call EAB                      ;FEAB
456:	jz A, 45B                     ;B45B
458:	mov A, 0x9                    ;79
459:	jmp 483                       ;E483
45B:	mov R1R0, 0x15                ;5501
45D:	call E2F                      ;FE2F
45F:	call DE8                      ;FDE8
461:	call EAB                      ;FEAB
463:	jz A, 468                     ;B468
465:	mov A, 0xA                    ;7A
466:	jmp 483                       ;E483
468:	mov R1R0, 0x10                ;5001
46A:	call E2F                      ;FE2F
46C:	call DE8                      ;FDE8
46E:	call EAB                      ;FEAB
470:	jz A, 475                     ;B475
472:	mov A, 0xB                    ;7B
473:	jmp 483                       ;E483
475:	mov R1R0, 0x0C                ;5C00
477:	call E2F                      ;FE2F
479:	call DE8                      ;FDE8
47B:	call EAB                      ;FEAB
47D:	jz A, 482                     ;B482
47F:	mov A, 0x6                    ;76
480:	jmp 483                       ;E483
482:	mov A, 0xC                    ;7C
483:	call D6F                      ;FD6F
485:	jmp 3F1                       ;E3F1
487:	call EE1                      ;FEE1
489:	jnc 404                       ;CC04
48B:	mov R3R2, 0x1A                ;6A41
48D:	mov A, [R3R2]                 ;06
48E:	jz A, 4DD                     ;B4DD
490:	dec A                         ;3F
491:	jz A, 589                     ;B589
493:	dec A                         ;3F
494:	jz A, 596                     ;B596
496:	dec A                         ;3F
497:	jz A, 589                     ;B589
499:	dec A                         ;3F
49A:	jz A, 5AE                     ;B5AE
49C:	dec A                         ;3F
49D:	jz A, 5FB                     ;B5FB
49F:	jmp 825                       ;E825
4A1:	mov R1R0, 0x1B                ;5B01
4A3:	mov A, [R1R0]                 ;04
4A4:	jnz A, 4D5                    ;BCD5
4A6:	call EC3                      ;FEC3
4A8:	mov R1R0, 0x92                ;5209
4AA:	mov [R1R0], A                 ;05
4AB:	call E50                      ;FE50
4AD:	mov R3R2, 0x90                ;6009
4AF:	call D3E                      ;FD3E
4B1:	jnz A, 4CD                    ;BCCD
4B3:	mov R1R0, 0x93                ;5309
4B5:	dec [R1R0]                    ;0D
4B6:	mov A, [R1R0]                 ;04
4B7:	inc A                         ;31
4B8:	jz A, 4D1                     ;B4D1
4BA:	mov R3R2, 0x92                ;6209
4BC:	call D3E                      ;FD3E
4BE:	jz A, 4B3                     ;B4B3
4C0:	mov R3R2, 0x92                ;6209
4C2:	call D3E                      ;FD3E
4C4:	mov R4, A                     ;28
4C5:	mov A, 0x0                    ;70
4C6:	mov [R1R0], A                 ;05
4C7:	mov R3R2, 0x90                ;6009
4C9:	call D38                      ;FD38
4CB:	mov A, R4                     ;29
4CC:	mov [R1R0], A                 ;05
4CD:	call E59                      ;FE59
4CF:	jnz A, 4AD                    ;BCAD
4D1:	call E61                      ;FE61
4D3:	jnz A, 4AB                    ;BCAB
4D5:	jmp 877                       ;E877
4D7:	mov R1R0, 0x1A                ;5A01
4D9:	mov A, 0x5                    ;75
4DA:	mov [R1R0], A                 ;05
4DB:	jmp 62A                       ;E62A
4DD:	mov R1R0, 0x81                ;5108
4DF:	mov A, 0x0                    ;70
4E0:	mov [R1R0], A                 ;05
4E1:	call E54                      ;FE54
4E3:	call EC3                      ;FEC3
4E5:	mov R3R2, 0x90                ;6009
4E7:	call D38                      ;FD38
4E9:	mov A, 0x8                    ;78
4EA:	and A, [R1R0]                 ;1A
4EB:	jz A, 4F1                     ;B4F1
4ED:	mov R1R0, 0x81                ;5108
4EF:	call DD0                      ;FDD0
4F1:	mov R3R2, 0x90                ;6009
4F3:	inc [R3R2]                    ;0E
4F4:	mov A, [R3R2]                 ;06
4F5:	sub A, 0x5                    ;4105
4F7:	jnz A, 4E5                    ;BCE5
4F9:	call E8A                      ;FE8A
4FB:	jnz A, 4E3                    ;BCE3
4FD:	mov R1R0, 0x81                ;5108
4FF:	mov A, [R1R0]                 ;04
500:	sub A, 0x5                    ;4105
502:	jc 535                        ;C535
504:	inc A                         ;31
505:	jnz A, 516                    ;BD16
507:	mov R1R0, 0x5F                ;5F05
509:	mov A, [R1R0]                 ;04
50A:	ja0 518                       ;8518
50C:	mov A, 0x3                    ;73
50D:	call D6B                      ;FD6B
50F:	mov A, 0x4                    ;74
510:	mov R1R0, 0x1B                ;5B01
512:	mov [R1R0], A                 ;05
513:	mov A, 0x2                    ;72
514:	jmp 3F9                       ;E3F9
516:	call E25                      ;FE25
518:	mov R1R0, 0x6B                ;5B06
51A:	mov A, [R1R0]                 ;04
51B:	sub A, 0x1                    ;4101
51D:	jnc 52A                       ;CD2A
51F:	mov A, 0x7                    ;77
520:	mov R1R0, 0x87                ;5708
522:	mov [R1R0], A                 ;05
523:	call D50                      ;FD50
525:	mov A, 0x9                    ;79
526:	call D63                      ;FD63
528:	jmp 7F0                       ;E7F0
52A:	mov R1R0, 0x02                ;5200
52C:	mov A, 0x3                    ;73
52D:	and A, [R1R0]                 ;1A
52E:	jnz A, 535                    ;BD35
530:	inc R0                        ;10
531:	mov A, 0x3                    ;73
532:	and A, [R1R0]                 ;1A
533:	jz A, 53F                     ;B53F
535:	call D50                      ;FD50
537:	mov A, 0xE                    ;7E
538:	call D5F                      ;FD5F
53A:	mov A, 0x7                    ;77
53B:	call D63                      ;FD63
53D:	jmp 022                       ;E022
53F:	call 04C                      ;F04C
541:	mov R1R0, 0x3E                ;5E03
543:	mov A, 0x3                    ;73
544:	and A, [R1R0]                 ;1A
545:	mov R3R2, 0x02                ;6200
547:	jnz A, 559                    ;BD59
549:	mov R1R0, 0x1E                ;5E01
54B:	mov A, [R1R0]                 ;04
54C:	jz A, 53F                     ;B53F
54E:	mov R1R0, 0x3E                ;5E03
550:	mov A, 0xC                    ;7C
551:	and A, [R1R0]                 ;1A
552:	jz A, 558                     ;B558
554:	xor A, 0xC                    ;430C
556:	jnz A, 559                    ;BD59
558:	mov A, 0x4                    ;74
559:	mov [R3R2], A                 ;07
55A:	call 04C                      ;F04C
55C:	mov R1R0, 0x3F                ;5F03
55E:	mov A, 0x3                    ;73
55F:	and A, [R1R0]                 ;1A
560:	mov R3R2, 0x03                ;6300
562:	jnz A, 574                    ;BD74
564:	mov R1R0, 0x1E                ;5E01
566:	mov A, [R1R0]                 ;04
567:	jz A, 55A                     ;B55A
569:	mov R1R0, 0x3F                ;5F03
56B:	mov A, 0xC                    ;7C
56C:	and A, [R1R0]                 ;1A
56D:	jz A, 573                     ;B573
56F:	xor A, 0xC                    ;430C
571:	jnz A, 574                    ;BD74
573:	mov A, 0x4                    ;74
574:	mov [R3R2], A                 ;07
575:	mov R1R0, 0x2A                ;5A02
577:	mov A, 0x2                    ;72
578:	call EB8                      ;FEB8
57A:	inc R0                        ;10
57B:	mov A, 0x3                    ;73
57C:	call EB8                      ;FEB8
57E:	mov R1R0, 0x5C                ;5C05
580:	mov A, 0x0                    ;70
581:	mov [R1R0], A                 ;05
582:	mov R1R0, 0x1A                ;5A01
584:	inc [R1R0]                    ;0C
585:	call 8B0                      ;F8B0
587:	jmp 62A                       ;E62A
589:	mov R1R0, 0x5D                ;5D05
58B:	mov A, [R1R0]                 ;04
58C:	jz A, 591                     ;B591
58E:	dec [R1R0]                    ;0D
58F:	jmp 587                       ;E587
591:	mov R1R0, 0x1A                ;5A01
593:	inc [R1R0]                    ;0C
594:	jmp 48B                       ;E48B
596:	call 8B7                      ;F8B7
598:	jnz A, 5A5                    ;BDA5
59A:	call 8BB                      ;F8BB
59C:	jnz A, 5A5                    ;BDA5
59E:	call 8CE                      ;F8CE
5A0:	call 8D2                      ;F8D2
5A2:	mov A, 0x1                    ;71
5A3:	jmp 5A9                       ;E5A9
5A5:	mov A, 0x9                    ;79
5A6:	call D5F                      ;FD5F
5A8:	mov A, 0x4                    ;74
5A9:	mov R1R0, 0x1A                ;5A01
5AB:	mov [R1R0], A                 ;05
5AC:	jmp 585                       ;E585
5AE:	call 8B7                      ;F8B7
5B0:	jz A, 5BE                     ;B5BE
5B2:	call 8BB                      ;F8BB
5B4:	jnz A, 5F3                    ;BDF3
5B6:	call 8D2                      ;F8D2
5B8:	mov R1R0, 0x2B                ;5B02
5BA:	call E40                      ;FE40
5BC:	jmp 5C4                       ;E5C4
5BE:	call 8CE                      ;F8CE
5C0:	mov R1R0, 0x2D                ;5D02
5C2:	call E40                      ;FE40
5C4:	mov R1R0, 0x93                ;5309
5C6:	mov A, [R1R0]                 ;04
5C7:	sub A, 0x8                    ;4108
5C9:	jz A, 5EA                     ;B5EA
5CB:	mov R3R2, 0x92                ;6209
5CD:	call D3E                      ;FD3E
5CF:	and A, 0x3                    ;4203
5D1:	jz A, 5E5                     ;B5E5
5D3:	mov R3R2, 0x90                ;6009
5D5:	call D3E                      ;FD3E
5D7:	mov R4, A                     ;28
5D8:	mov A, 0x3                    ;73
5D9:	and [R1R0], A                 ;1D
5DA:	mov R3R2, 0x92                ;6209
5DC:	call D38                      ;FD38
5DE:	mov A, R4                     ;29
5DF:	and A, 0xC                    ;420C
5E1:	or A, [R1R0]                  ;1C
5E2:	mov [R1R0], A                 ;05
5E3:	jmp 5F0                       ;E5F0
5E5:	mov R1R0, 0x93                ;5309
5E7:	inc [R1R0]                    ;0C
5E8:	jmp 5C4                       ;E5C4
5EA:	mov R3R2, 0x90                ;6009
5EC:	call D3E                      ;FD3E
5EE:	mov A, 0x3                    ;73
5EF:	and [R1R0], A                 ;1D
5F0:	mov A, 0x3                    ;73
5F1:	jmp 5A9                       ;E5A9
5F3:	mov A, 0x9                    ;79
5F4:	call D5F                      ;FD5F
5F6:	jmp 825                       ;E825
5F8:	mov A, 0x5                    ;75
5F9:	jmp 5A9                       ;E5A9
5FB:	mov R1R0, 0x1B                ;5B01
5FD:	mov A, [R1R0]                 ;04
5FE:	jz A, 628                     ;B628
600:	inc [R1R0]                    ;0C
601:	mov A, [R1R0]                 ;04
602:	sub A, 0xE                    ;410E
604:	jnz A, 62A                    ;BE2A
606:	mov R1R0, 0x1B                ;5B01
608:	mov A, 0x0                    ;70
609:	mov [R1R0], A                 ;05
60A:	mov R1R0, 0x1A                ;5A01
60C:	mov A, 0x6                    ;76
60D:	mov [R1R0], A                 ;05
60E:	mov R4, 0x3                   ;4603
610:	mov R1R0, 0x8D                ;5D08
612:	mov R3R2, 0x6D                ;6D06
614:	call D30                      ;FD30
616:	mov R1R0, 0x4C                ;5C04
618:	mov R3R2, 0x8C                ;6C08
61A:	call D2E                      ;FD2E
61C:	call D73                      ;FD73
61E:	mov R1R0, 0x8C                ;5C08
620:	mov R3R2, 0x4C                ;6C04
622:	call D2E                      ;FD2E
624:	call DAF                      ;FDAF
626:	jmp 62A                       ;E62A
628:	jmp 8E2                       ;E8E2
62A:	mov R3R2, 0x1A                ;6A01
62C:	mov A, [R3R2]                 ;06
62D:	dec A                         ;3F
62E:	jz A, 634                     ;B634
630:	dec A                         ;3F
631:	dec A                         ;3F
632:	jnz A, 6F1                    ;BEF1
634:	mov R1R0, 0x88                ;5808
636:	call D52                      ;FD52
638:	mov R1R0, 0x0C                ;5C00
63A:	mov R3R2, 0x0D                ;6D00
63C:	mov A, [R3R2]                 ;06
63D:	or A, [R1R0]                  ;1C
63E:	jz A, 646                     ;B646
640:	call D50                      ;FD50
642:	mov R1R0, 0x0C                ;5C00
644:	call E9C                      ;FE9C
646:	call EC8                      ;FEC8
648:	jnz A, 64E                    ;BE4E
64A:	mov R1R0, 0x0E                ;5E00
64C:	call E9C                      ;FE9C
64E:	mov R1R0, 0x89                ;5908
650:	mov A, [R1R0]                 ;04
651:	ja2 661                       ;9661
653:	call EA7                      ;FEA7
655:	ja0 683                       ;8683
657:	call EA7                      ;FEA7
659:	ja1 6B7                       ;8EB7
65B:	call EA7                      ;FEA7
65D:	ja2 6EB                       ;96EB
65F:	jmp 6F1                       ;E6F1
661:	mov R3R2, 0x1A                ;6A01
663:	mov A, [R3R2]                 ;06
664:	dec A                         ;3F
665:	jnz A, 653                    ;BE53
667:	call 804                      ;F804
669:	mov A, [R3R2]                 ;06
66A:	call EC4                      ;FEC4
66C:	call 808                      ;F808
66E:	mov A, [R3R2]                 ;06
66F:	mov R1R0, 0x91                ;5109
671:	mov [R1R0], A                 ;05
672:	call 804                      ;F804
674:	mov R1R0, 0x91                ;5109
676:	mov A, [R1R0]                 ;04
677:	mov [R3R2], A                 ;07
678:	call 808                      ;F808
67A:	mov R1R0, 0x90                ;5009
67C:	mov A, [R1R0]                 ;04
67D:	mov [R3R2], A                 ;07
67E:	mov A, 0xB                    ;7B
67F:	call D5F                      ;FD5F
681:	jmp 653                       ;E653
683:	mov R3R2, 0x1A                ;6A01
685:	mov A, [R3R2]                 ;06
686:	dec A                         ;3F
687:	jnz A, 657                    ;BE57
689:	call 808                      ;F808
68B:	call 812                      ;F812
68D:	mov A, [R3R2]                 ;06
68E:	and A, 0x3                    ;4203
690:	jnz A, 657                    ;BE57
692:	call 808                      ;F808
694:	call 810                      ;F810
696:	mov A, R1                     ;23
697:	mov [R3R2], A                 ;07
698:	call 804                      ;F804
69A:	call 810                      ;F810
69C:	mov A, R1                     ;23
69D:	mov [R3R2], A                 ;07
69E:	call 81D                      ;F81D
6A0:	mov A, 0x0                    ;70
6A1:	mov [R3R2], A                 ;07
6A2:	mov R1R0, 0x2C                ;5C02
6A4:	mov A, [R1R0]                 ;04
6A5:	mov R2, A                     ;24
6A6:	call 812                      ;F812
6A8:	mov A, R2                     ;25
6A9:	mov [R1R0], A                 ;05
6AA:	mov R1R0, 0x2A                ;5A02
6AC:	mov A, [R1R0]                 ;04
6AD:	mov R2, A                     ;24
6AE:	call 812                      ;F812
6B0:	mov A, R2                     ;25
6B1:	mov [R1R0], A                 ;05
6B2:	mov A, 0x5                    ;75
6B3:	call D5F                      ;FD5F
6B5:	jmp 657                       ;E657
6B7:	mov R3R2, 0x1A                ;6A01
6B9:	mov A, [R3R2]                 ;06
6BA:	dec A                         ;3F
6BB:	jnz A, 65B                    ;BE5B
6BD:	call 804                      ;F804
6BF:	call 81D                      ;F81D
6C1:	mov A, [R3R2]                 ;06
6C2:	and A, 0x3                    ;4203
6C4:	jnz A, 65B                    ;BE5B
6C6:	call 804                      ;F804
6C8:	call 81B                      ;F81B
6CA:	mov A, R1                     ;23
6CB:	mov [R3R2], A                 ;07
6CC:	call 808                      ;F808
6CE:	call 81B                      ;F81B
6D0:	mov A, R1                     ;23
6D1:	mov [R3R2], A                 ;07
6D2:	call 812                      ;F812
6D4:	mov A, 0x0                    ;70
6D5:	mov [R3R2], A                 ;07
6D6:	mov R1R0, 0x2A                ;5A02
6D8:	mov A, [R1R0]                 ;04
6D9:	mov R2, A                     ;24
6DA:	call 81D                      ;F81D
6DC:	mov A, R2                     ;25
6DD:	mov [R1R0], A                 ;05
6DE:	mov R1R0, 0x2C                ;5C02
6E0:	mov A, [R1R0]                 ;04
6E1:	mov R2, A                     ;24
6E2:	call 81D                      ;F81D
6E4:	mov A, R2                     ;25
6E5:	mov [R1R0], A                 ;05
6E6:	mov A, 0x5                    ;75
6E7:	call D5F                      ;FD5F
6E9:	jmp 65B                       ;E65B
6EB:	mov R1R0, 0x5D                ;5D05
6ED:	mov A, 0x0                    ;70
6EE:	mov [R1R0], A                 ;05
6EF:	jmp 65F                       ;E65F
6F1:	jmp 022                       ;E022
6F3:	call E25                      ;FE25
6F5:	mov R3R2, 0x80                ;6008
6F7:	mov A, [R3R2]                 ;06
6F8:	jnz A, 703                    ;BF03
6FA:	call D50                      ;FD50
6FC:	mov A, 0xC                    ;7C
6FD:	call D5F                      ;FD5F
6FF:	mov R1R0, 0x8A                ;5A08
701:	call D52                      ;FD52
703:	mov R3R2, 0x80                ;6008
705:	mov A, [R3R2]                 ;06
706:	jz A, 728                     ;B728
708:	dec A                         ;3F
709:	jz A, 72D                     ;B72D
70B:	dec A                         ;3F
70C:	jz A, 730                     ;B730
70E:	dec A                         ;3F
70F:	jz A, 733                     ;B733
711:	dec A                         ;3F
712:	jz A, 7B1                     ;B7B1
714:	mov R1R0, 0x1B                ;5B01
716:	inc [R1R0]                    ;0C
717:	mov R3R2, 0x8B                ;6B08
719:	mov A, [R3R2]                 ;06
71A:	sub A, 0x2                    ;4102
71C:	jnc 72B                       ;CF2B
71E:	mov R1R0, 0x5E                ;5E05
720:	mov A, 0x6                    ;76
721:	and [R1R0], A                 ;1D
722:	mov R1R0, 0x1B                ;5B01
724:	mov A, 0x0                    ;70
725:	mov [R1R0], A                 ;05
726:	jmp 7EF                       ;E7EF
728:	mov R3R2, 0x80                ;6008
72A:	inc [R3R2]                    ;0E
72B:	jmp 022                       ;E022
72D:	mov A, 0x1                    ;71
72E:	jmp 734                       ;E734
730:	mov A, 0x2                    ;72
731:	jmp 734                       ;E734
733:	mov A, 0x3                    ;73
734:	mov R3R2, 0x90                ;6009
736:	mov [R3R2], A                 ;07
737:	call EC8                      ;FEC8
739:	jnz A, 779                    ;BF79
73B:	mov R3R2, 0x91                ;6109
73D:	mov A, 0x3                    ;73
73E:	mov [R3R2], A                 ;07
73F:	dec R2                        ;15
740:	call D38                      ;FD38
742:	call EAF                      ;FEAF
744:	dec R1                        ;13
745:	dec R1                        ;13
746:	call EAF                      ;FEAF
748:	mov R3R2, 0x92                ;6209
74A:	mov [R3R2], A                 ;07
74B:	mov R3R2, 0x90                ;6009
74D:	mov A, [R3R2]                 ;06
74E:	sub A, 0x2                    ;4102
750:	jnz A, 75A                    ;BF5A
752:	mov R3R2, 0x92                ;6209
754:	mov A, [R3R2]                 ;06
755:	dec A                         ;3F
756:	mov R4, 0x3                   ;4603
758:	jmp 76B                       ;E76B
75A:	mov R3R2, 0x90                ;6009
75C:	mov A, [R3R2]                 ;06
75D:	dec A                         ;3F
75E:	mov R4, A                     ;28
75F:	add A, 0x2                    ;4002
761:	mov R0, A                     ;20
762:	mov R2, A                     ;24
763:	mov A, 0x8                    ;78
764:	mov R1, A                     ;22
765:	mov R3, A                     ;26
766:	mov A, R4                     ;29
767:	inc A                         ;31
768:	mov R4, A                     ;28
769:	add A, [R1R0]                 ;09
76A:	mov [R3R2], A                 ;07
76B:	and A, 0x3                    ;4203
76D:	jz A, 770                     ;B770
76F:	mov R4, A                     ;28
770:	mov R3R2, 0x91                ;6109
772:	mov A, 0x2                    ;72
773:	mov [R3R2], A                 ;07
774:	dec R2                        ;15
775:	call D38                      ;FD38
777:	mov A, R4                     ;29
778:	mov [R1R0], A                 ;05
779:	mov R3R2, 0x90                ;6009
77B:	mov A, [R3R2]                 ;06
77C:	dec A                         ;3F
77D:	jz A, 730                     ;B730
77F:	dec A                         ;3F
780:	jz A, 733                     ;B733
782:	call EE1                      ;FEE1
784:	jnc 79B                       ;CF9B
786:	mov A, 0x7                    ;77
787:	call EC9                      ;FEC9
789:	jnz A, 78F                    ;BF8F
78B:	mov R1R0, 0x5E                ;5E05
78D:	mov A, 0x9                    ;79
78E:	xor [R1R0], A                 ;1E
78F:	mov A, 0x7                    ;77
790:	call EC9                      ;FEC9
792:	jnz A, 797                    ;BF97
794:	mov A, 0x4                    ;74
795:	call D5F                      ;FD5F
797:	call D57                      ;FD57
799:	ja2 79D                       ;979D
79B:	jmp 022                       ;E022
79D:	mov A, 0x5                    ;75
79E:	call D5F                      ;FD5F
7A0:	mov R3R2, 0x80                ;6008
7A2:	inc [R3R2]                    ;0E
7A3:	mov A, [R3R2]                 ;06
7A4:	sub A, 0x4                    ;4104
7A6:	jnz A, 7AF                    ;BFAF
7A8:	mov A, 0xA                    ;7A
7A9:	call D5F                      ;FD5F
7AB:	mov R1R0, 0x8A                ;5A08
7AD:	call D52                      ;FD52
7AF:	jmp 022                       ;E022
7B1:	call EE1                      ;FEE1
7B3:	jnc 7AF                       ;CFAF
7B5:	jmp 8E2                       ;E8E2
7B7:	mov R1R0, 0x3D                ;5D03
7B9:	mov A, [R1R0]                 ;04
7BA:	jz A, 7C3                     ;B7C3
7BC:	mov R1R0, 0x5E                ;5E05
7BE:	mov A, 0x4                    ;74
7BF:	or [R1R0], A                  ;1F
7C0:	mov A, 0x8                    ;78
7C1:	jmp 7C4                       ;E7C4
7C3:	mov A, 0x7                    ;77
7C4:	call D5F                      ;FD5F
7C6:	mov R1R0, 0x8A                ;5A08
7C8:	call D52                      ;FD52
7CA:	mov R1R0, 0x1B                ;5B01
7CC:	mov A, 0x2                    ;72
7CD:	mov [R1R0], A                 ;05
7CE:	mov R3R2, 0x80                ;6008
7D0:	inc [R3R2]                    ;0E
7D1:	jmp 022                       ;E022
7D3:	mov R3R2, 0x8B                ;6B08
7D5:	mov A, [R3R2]                 ;06
7D6:	sub A, 0x4                    ;4104
7D8:	jnc 7D1                       ;CFD1
7DA:	mov R1R0, 0x4A                ;5A04
7DC:	inc [R1R0]                    ;0C
7DD:	mov A, [R1R0]                 ;04
7DE:	sub A, 0x9                    ;4109
7E0:	jnz A, 7E4                    ;BFE4
7E2:	mov A, 0x1                    ;71
7E3:	mov [R1R0], A                 ;05
7E4:	mov R1R0, 0x80                ;5008
7E6:	mov A, 0x0                    ;70
7E7:	mov [R1R0], A                 ;05
7E8:	call E1E                      ;FE1E
7EA:	mov A, 0x8                    ;78
7EB:	or [R1R0], A                  ;1F
7EC:	mov A, 0x4                    ;74
7ED:	jmp 7F0                       ;E7F0
7EF:	mov A, 0x2                    ;72
7F0:	call D63                      ;FD63
7F2:	jmp 022                       ;E022
7F4:	call D57                      ;FD57
7F6:	ja2 7FA                       ;97FA
7F8:	jmp 022                       ;E022
7FA:	mov A, 0x9                    ;79
7FB:	call D5F                      ;FD5F
7FD:	call D45                      ;FD45
7FF:	mov A, 0x1                    ;71
800:	call D63                      ;FD63
802:	jmp 022                       ;E022
804:	mov R1R0, 0x2B                ;5B02
806:	jmp 80A                       ;E80A
808:	mov R1R0, 0x2D                ;5D02
80A:	mov A, [R1R0]                 ;04
80B:	mov R3, A                     ;26
80C:	dec R0                        ;11
80D:	mov A, [R1R0]                 ;04
80E:	mov R2, A                     ;24
80F:	ret                           ;2E
810:	mov A, [R3R2]                 ;06
811:	mov R1, A                     ;22
812:	inc R2                        ;14
813:	mov A, R2                     ;25
814:	sub A, 0x5                    ;4105
816:	jnz A, 81A                    ;B81A
818:	mov A, 0x0                    ;70
819:	mov R2, A                     ;24
81A:	ret                           ;2E
81B:	mov A, [R3R2]                 ;06
81C:	mov R1, A                     ;22
81D:	dec R2                        ;15
81E:	mov A, R2                     ;25
81F:	inc A                         ;31
820:	jnz A, 824                    ;B824
822:	mov A, 0x4                    ;74
823:	mov R2, A                     ;24
824:	ret                           ;2E
825:	mov R1R0, 0x8C                ;5C08
827:	call D52                      ;FD52
829:	inc R0                        ;10
82A:	call D52                      ;FD52
82C:	call EC3                      ;FEC3
82E:	mov R1R0, 0x92                ;5209
830:	mov [R1R0], A                 ;05
831:	call E50                      ;FE50
833:	mov R3R2, 0x90                ;6009
835:	call D3E                      ;FD3E
837:	and A, 0xC                    ;420C
839:	jz A, 867                     ;B067
83B:	mov R1R0, 0x93                ;5309
83D:	mov A, [R1R0]                 ;04
83E:	sub A, 0x8                    ;4108
840:	jz A, 861                     ;B061
842:	mov R3R2, 0x92                ;6209
844:	call D3E                      ;FD3E
846:	and A, 0x3                    ;4203
848:	jz A, 85C                     ;B05C
84A:	mov R3R2, 0x90                ;6009
84C:	call D3E                      ;FD3E
84E:	mov R4, A                     ;28
84F:	mov A, 0x3                    ;73
850:	and [R1R0], A                 ;1D
851:	mov R3R2, 0x92                ;6209
853:	call D38                      ;FD38
855:	mov A, R4                     ;29
856:	and A, 0xC                    ;420C
858:	or A, [R1R0]                  ;1C
859:	mov [R1R0], A                 ;05
85A:	jmp 867                       ;E867
85C:	mov R1R0, 0x93                ;5309
85E:	inc [R1R0]                    ;0C
85F:	jmp 83B                       ;E83B
861:	mov R3R2, 0x90                ;6009
863:	call D3E                      ;FD3E
865:	mov A, 0x3                    ;73
866:	and [R1R0], A                 ;1D
867:	call E59                      ;FE59
869:	inc A                         ;31
86A:	jnz A, 833                    ;B833
86C:	call E61                      ;FE61
86E:	jnz A, 831                    ;B831
870:	mov R3R2, 0x1A                ;6A01
872:	mov A, [R3R2]                 ;06
873:	sub A, 0x6                    ;4106
875:	jz A, 8AC                     ;B0AC
877:	call DAB                      ;FDAB
879:	call EC3                      ;FEC3
87B:	call E54                      ;FE54
87D:	mov R3R2, 0x90                ;6009
87F:	call D3E                      ;FD3E
881:	and A, 0xC                    ;420C
883:	xor A, 0xC                    ;430C
885:	jnz A, 89B                    ;B89B
887:	mov A, R0                     ;21
888:	add A, 0x5                    ;4005
88A:	mov R0, A                     ;20
88B:	mov A, 0x3                    ;73
88C:	and [R1R0], A                 ;1D
88D:	mov R1R0, 0x8F                ;5F08
88F:	mov A, [R1R0]                 ;04
890:	inc A                         ;31
891:	jz A, 894                     ;B094
893:	mov [R1R0], A                 ;05
894:	mov A, 0x3                    ;73
895:	call D5F                      ;FD5F
897:	mov R1R0, 0x1B                ;5B01
899:	mov A, 0x2                    ;72
89A:	mov [R1R0], A                 ;05
89B:	call E8A                      ;FE8A
89D:	jnz A, 87D                    ;B87D
89F:	call E64                      ;FE64
8A1:	jnz A, 87B                    ;B87B
8A3:	mov R3R2, 0x1A                ;6A01
8A5:	mov A, [R3R2]                 ;06
8A6:	sub A, 0x4                    ;4104
8A8:	jnz A, 8AE                    ;B8AE
8AA:	jmp 5F8                       ;E5F8
8AC:	jmp 4A1                       ;E4A1
8AE:	jmp 4D7                       ;E4D7
8B0:	mov R3R2, 0x6C                ;6C06
8B2:	mov A, [R3R2]                 ;06
8B3:	mov R1R0, 0x5D                ;5D05
8B5:	mov [R1R0], A                 ;05
8B6:	ret                           ;2E
8B7:	mov R1R0, 0x2B                ;5B02
8B9:	jmp 8BD                       ;E8BD
8BB:	mov R1R0, 0x2D                ;5D02
8BD:	mov A, [R1R0]                 ;04
8BE:	sub A, 0x7                    ;4107
8C0:	jz A, 8CC                     ;B0CC
8C2:	mov A, [R1R0]                 ;04
8C3:	inc A                         ;31
8C4:	mov R3, A                     ;26
8C5:	dec R0                        ;11
8C6:	mov A, [R1R0]                 ;04
8C7:	mov R2, A                     ;24
8C8:	mov A, [R3R2]                 ;06
8C9:	and A, 0x3                    ;4203
8CB:	ret                           ;2E
8CC:	mov A, 0x1                    ;71
8CD:	ret                           ;2E
8CE:	mov R1R0, 0x2B                ;5B02
8D0:	jmp 8D4                       ;E8D4
8D2:	mov R1R0, 0x2D                ;5D02
8D4:	mov A, [R1R0]                 ;04
8D5:	mov R3, A                     ;26
8D6:	dec R0                        ;11
8D7:	mov A, [R1R0]                 ;04
8D8:	mov R2, A                     ;24
8D9:	mov A, [R3R2]                 ;06
8DA:	inc R3                        ;16
8DB:	mov [R3R2], A                 ;07
8DC:	dec R3                        ;17
8DD:	mov A, 0x0                    ;70
8DE:	mov [R3R2], A                 ;07
8DF:	inc R0                        ;10
8E0:	inc [R1R0]                    ;0C
8E1:	ret                           ;2E
8E2:	mov R1R0, 0x3D                ;5D03
8E4:	mov A, 0x0                    ;70
8E5:	mov [R1R0], A                 ;05
8E6:	call DAB                      ;FDAB
8E8:	call E54                      ;FE54
8EA:	call EC3                      ;FEC3
8EC:	call E85                      ;FE85
8EE:	mov R3R2, 0x90                ;6009
8F0:	call D3E                      ;FD3E
8F2:	ja3 8F8                       ;98F8
8F4:	and A, 0x3                    ;4203
8F6:	jnz A, 8FE                    ;B8FE
8F8:	call E64                      ;FE64
8FA:	jz A, 92D                     ;B12D
8FC:	jmp 8EE                       ;E8EE
8FE:	call E6B                      ;FE6B
900:	call E64                      ;FE64
902:	jz A, 911                     ;B111
904:	mov R3R2, 0x90                ;6009
906:	call D3E                      ;FD3E
908:	call E96                      ;FE96
90A:	jnz A, 911                    ;B911
90C:	mov R1R0, 0x5A                ;5A05
90E:	inc [R1R0]                    ;0C
90F:	jmp 900                       ;E900
911:	mov R1R0, 0x5A                ;5A05
913:	mov A, [R1R0]                 ;04
914:	sub A, 0x3                    ;4103
916:	jnc 926                       ;C926
918:	call E79                      ;FE79
91A:	call D38                      ;FD38
91C:	call E80                      ;FE80
91E:	mov A, 0xC                    ;7C
91F:	and [R1R0], A                 ;1D
920:	inc R0                        ;10
921:	dec R4                        ;19
922:	jnz R4, 91E                   ;D91E
924:	call AA7                      ;FAA7
926:	mov R1R0, 0x90                ;5009
928:	mov A, [R1R0]                 ;04
929:	sub A, 0x5                    ;4105
92B:	jnz A, 943                    ;B943
92D:	call E8A                      ;FE8A
92F:	jnz A, 945                    ;B945
931:	call EC3                      ;FEC3
933:	call E54                      ;FE54
935:	call E85                      ;FE85
937:	mov R3R2, 0x90                ;6009
939:	call D3E                      ;FD3E
93B:	ja3 947                       ;9947
93D:	and A, 0x3                    ;4203
93F:	jz A, 97B                     ;B17B
941:	jmp 94D                       ;E94D
943:	jmp 8EC                       ;E8EC
945:	jmp 8EA                       ;E8EA
947:	call E8A                      ;FE8A
949:	jz A, 97B                     ;B17B
94B:	jmp 937                       ;E937
94D:	call E6B                      ;FE6B
94F:	call E8A                      ;FE8A
951:	jz A, 960                     ;B160
953:	mov R3R2, 0x90                ;6009
955:	call D3E                      ;FD3E
957:	call E96                      ;FE96
959:	jnz A, 960                    ;B960
95B:	mov R1R0, 0x5A                ;5A05
95D:	inc [R1R0]                    ;0C
95E:	jmp 94F                       ;E94F
960:	mov R1R0, 0x5A                ;5A05
962:	mov A, [R1R0]                 ;04
963:	sub A, 0x3                    ;4103
965:	jnc 975                       ;C975
967:	call E79                      ;FE79
969:	call D38                      ;FD38
96B:	call E80                      ;FE80
96D:	mov A, 0xC                    ;7C
96E:	and [R1R0], A                 ;1D
96F:	dec R1                        ;13
970:	dec R4                        ;19
971:	jnz R4, 96D                   ;D96D
973:	call AA7                      ;FAA7
975:	mov R1R0, 0x91                ;5109
977:	mov A, [R1R0]                 ;04
978:	inc A                         ;31
979:	jnz A, 935                    ;B935
97B:	call E64                      ;FE64
97D:	jnz A, 933                    ;B933
97F:	mov A, 0x0                    ;70
980:	jmp 983                       ;E983
982:	mov A, 0x1                    ;71
983:	mov R1R0, 0x92                ;5209
985:	mov [R1R0], A                 ;05
986:	jmp 9DF                       ;E9DF
988:	call D67                      ;FD67
98A:	sub A, 0x4                    ;4104
98C:	jnz A, 990                    ;B990
98E:	jmp 7B7                       ;E7B7
990:	mov R1R0, 0x3D                ;5D03
992:	mov A, [R1R0]                 ;04
993:	jz A, 9D9                     ;B1D9
995:	mov R1R0, 0x5C                ;5C05
997:	mov A, [R1R0]                 ;04
998:	inc A                         ;31
999:	jz A, 99C                     ;B19C
99B:	inc [R1R0]                    ;0C
99C:	mov R1R0, 0x6A                ;5A06
99E:	mov R3R2, 0x6B                ;6B06
9A0:	call DD6                      ;FDD6
9A2:	mov R1R0, 0x5C                ;5C05
9A4:	mov A, [R1R0]                 ;04
9A5:	sub A, 0x2                    ;4102
9A7:	jnc 9AF                       ;C9AF
9A9:	mov R1R0, 0x7A                ;5A07
9AB:	mov R3R2, 0x7B                ;6B07
9AD:	call DD6                      ;FDD6
9AF:	mov A, 0x0                    ;70
9B0:	mov R1R0, 0x6D                ;5D06
9B2:	mov [R1R0], A                 ;05
9B3:	call EB3                      ;FEB3
9B5:	mov R3R2, 0x3D                ;6D03
9B7:	mov A, [R3R2]                 ;06
9B8:	mov [R1R0], A                 ;05
9B9:	mov A, 0x4                    ;74
9BA:	mov R4, A                     ;28
9BB:	mov R1R0, 0x8C                ;5C08
9BD:	mov A, 0x0                    ;70
9BE:	mov [R1R0], A                 ;05
9BF:	inc R0                        ;10
9C0:	dec R4                        ;19
9C1:	jnz R4, 9BE                   ;D9BE
9C3:	mov R1R0, 0x5C                ;5C05
9C5:	mov A, [R1R0]                 ;04
9C6:	call EC4                      ;FEC4
9C8:	call D73                      ;FD73
9CA:	mov R1R0, 0x90                ;5009
9CC:	mov A, [R1R0]                 ;04
9CD:	dec A                         ;3F
9CE:	jnz A, 9C6                    ;B9C6
9D0:	mov A, 0x8                    ;78
9D1:	call D5F                      ;FD5F
9D3:	mov R1R0, 0x1B                ;5B01
9D5:	mov A, 0x2                    ;72
9D6:	mov [R1R0], A                 ;05
9D7:	jmp 9DD                       ;E9DD
9D9:	mov A, 0x0                    ;70
9DA:	mov R1R0, 0x1A                ;5A01
9DC:	mov [R1R0], A                 ;05
9DD:	jmp 62A                       ;E62A
9DF:	mov R1R0, 0x94                ;5409
9E1:	mov A, 0x0                    ;70
9E2:	mov [R1R0], A                 ;05
9E3:	mov R1R0, 0x92                ;5209
9E5:	mov A, [R1R0]                 ;04
9E6:	rl A                          ;01
9E7:	rl A                          ;01
9E8:	and A, 0x4                    ;4204
9EA:	call EC4                      ;FEC4
9EC:	inc R0                        ;10
9ED:	call EAB                      ;FEAB
9EF:	add A, 0x2                    ;4002
9F1:	mov [R1R0], A                 ;05
9F2:	call EAB                      ;FEAB
9F4:	sub A, 0x5                    ;4105
9F6:	jnc A0F                       ;CA0F
9F8:	mov R1R0, 0x93                ;5309
9FA:	mov [R1R0], A                 ;05
9FB:	dec R0                        ;11
9FC:	mov A, [R1R0]                 ;04
9FD:	jnz A, A07                    ;BA07
9FF:	inc R0                        ;10
A00:	mov R3R2, 0x90                ;6009
A02:	mov A, [R3R2]                 ;06
A03:	add A, [R1R0]                 ;09
A04:	mov [R3R2], A                 ;07
A05:	jmp A0B                       ;EA0B
A07:	mov R3R2, 0x90                ;6009
A09:	call EBD                      ;FEBD
A0B:	mov R3R2, 0x91                ;6109
A0D:	call EBD                      ;FEBD
A0F:	call E85                      ;FE85
A11:	mov R3R2, 0x90                ;6009
A13:	call D3E                      ;FD3E
A15:	ja3 A1B                       ;9A1B
A17:	and A, 0x3                    ;4203
A19:	jnz A, A34                    ;BA34
A1B:	mov R1R0, 0x92                ;5209
A1D:	mov A, [R1R0]                 ;04
A1E:	jnz A, A2A                    ;BA2A
A20:	call E8A                      ;FE8A
A22:	jz A, A94                     ;B294
A24:	call E64                      ;FE64
A26:	jz A, A94                     ;B294
A28:	jmp A11                       ;EA11
A2A:	call E8A                      ;FE8A
A2C:	jz A, A94                     ;B294
A2E:	call E90                      ;FE90
A30:	jz A, A94                     ;B294
A32:	jmp A11                       ;EA11
A34:	call E6B                      ;FE6B
A36:	mov R1R0, 0x92                ;5209
A38:	mov A, [R1R0]                 ;04
A39:	jnz A, A45                    ;BA45
A3B:	call E8A                      ;FE8A
A3D:	jz A, A5A                     ;B25A
A3F:	call E64                      ;FE64
A41:	jz A, A5A                     ;B25A
A43:	jmp A4D                       ;EA4D
A45:	call E8A                      ;FE8A
A47:	jz A, A5A                     ;B25A
A49:	call E90                      ;FE90
A4B:	jz A, A5A                     ;B25A
A4D:	mov R3R2, 0x90                ;6009
A4F:	call D3E                      ;FD3E
A51:	call E96                      ;FE96
A53:	jnz A, A5A                    ;BA5A
A55:	mov R1R0, 0x5A                ;5A05
A57:	inc [R1R0]                    ;0C
A58:	jmp A36                       ;EA36
A5A:	mov R1R0, 0x5A                ;5A05
A5C:	mov A, [R1R0]                 ;04
A5D:	sub A, 0x3                    ;4103
A5F:	jnc A79                       ;CA79
A61:	call E79                      ;FE79
A63:	call D38                      ;FD38
A65:	call E80                      ;FE80
A67:	mov A, 0xC                    ;7C
A68:	and [R1R0], A                 ;1D
A69:	mov R3R2, 0x92                ;6209
A6B:	mov A, [R3R2]                 ;06
A6C:	jnz A, A72                    ;BA72
A6E:	dec R1                        ;13
A6F:	inc R0                        ;10
A70:	jmp A74                       ;EA74
A72:	dec R1                        ;13
A73:	dec R0                        ;11
A74:	dec R4                        ;19
A75:	jnz R4, A67                   ;DA67
A77:	call AA7                      ;FAA7
A79:	mov R1R0, 0x91                ;5109
A7B:	mov A, [R1R0]                 ;04
A7C:	inc A                         ;31
A7D:	jz A, A94                     ;B294
A7F:	dec R0                        ;11
A80:	mov A, [R1R0]                 ;04
A81:	jnz A, A8C                    ;BA8C
A83:	mov R1R0, 0x90                ;5009
A85:	mov A, [R1R0]                 ;04
A86:	sub A, 0x5                    ;4105
A88:	jz A, A94                     ;B294
A8A:	jmp A0F                       ;EA0F
A8C:	mov R1R0, 0x90                ;5009
A8E:	mov A, [R1R0]                 ;04
A8F:	inc A                         ;31
A90:	jz A, A94                     ;B294
A92:	jmp A0F                       ;EA0F
A94:	mov R1R0, 0x94                ;5409
A96:	inc [R1R0]                    ;0C
A97:	mov A, [R1R0]                 ;04
A98:	sub A, 0x8                    ;4108
A9A:	jz A, A9E                     ;B29E
A9C:	jmp 9E3                       ;E9E3
A9E:	mov R1R0, 0x92                ;5209
AA0:	mov A, [R1R0]                 ;04
AA1:	jz A, AA5                     ;B2A5
AA3:	jmp 988                       ;E988
AA5:	jmp 982                       ;E982
AA7:	mov R3R2, 0x5A                ;6A05
AA9:	mov A, [R3R2]                 ;06
AAA:	sub A, 0x2                    ;4102
AAC:	mov R1R0, 0x3D                ;5D03
AAE:	add A, [R1R0]                 ;09
AAF:	jnc AB2                       ;CAB2
AB1:	mov A, 0xF                    ;7F
AB2:	mov [R1R0], A                 ;05
AB3:	ret                           ;2E
AB4:	call E1E                      ;FE1E
AB6:	mov A, 0x1                    ;71
AB7:	call D5F                      ;FD5F
AB9:	mov R1R0, 0x3D                ;5D03
ABB:	mov A, 0x0                    ;70
ABC:	mov [R1R0], A                 ;05
ABD:	call E54                      ;FE54
ABF:	call EC3                      ;FEC3
AC1:	mov R3R2, 0x90                ;6009
AC3:	call D38                      ;FD38
AC5:	mov A, 0x8                    ;78
AC6:	and A, [R1R0]                 ;1A
AC7:	jz A, ACB                     ;B2CB
AC9:	mov A, 0x4                    ;74
ACA:	or [R1R0], A                  ;1F
ACB:	mov R3R2, 0x90                ;6009
ACD:	inc [R3R2]                    ;0E
ACE:	mov A, [R3R2]                 ;06
ACF:	sub A, 0x5                    ;4105
AD1:	jnz A, AC1                    ;BAC1
AD3:	call E8A                      ;FE8A
AD5:	jnz A, ABF                    ;BABF
AD7:	jmp 877                       ;E877
AD9:	mov R3R2, 0x90                ;6009
ADB:	mov A, [R3R2]                 ;06
ADC:	mov R0, A                     ;20
ADD:	inc R2                        ;14
ADE:	mov A, [R3R2]                 ;06
ADF:	mov R1, A                     ;22
AE0:	mov A, [R1R0]                 ;04
AE1:	mov R3R2, 0x95                ;6509
AE3:	mov [R3R2], A                 ;07
AE4:	ret                           ;2E
AE5:	or [R1R0], A                  ;1F
AE6:	xor A, [R1R0]                 ;1B
AE7:	mov [R1R0], A                 ;05
AE8:	ret                           ;2E
AE9:	mov A, R3                     ;27
AEA:	rlc A                         ;03
AEB:	rlc A                         ;03
AEC:	and A, 0xC                    ;420C
AEE:	inc R0                        ;10
AEF:	mov [R1R0], A                 ;05
AF0:	ret                           ;2E
AF1:	mov A, R3                     ;27
AF2:	rrc A                         ;02
AF3:	rrc A                         ;02
AF4:	and A, 0x3                    ;4203
AF6:	dec R0                        ;11
AF7:	mov [R1R0], A                 ;05
AF8:	ret                           ;2E
AF9:	mov R4, 0x0                   ;4600
AFB:	mov A, 0xB                    ;7B
AFC:	mov R3, A                     ;26
AFD:	mov R1R0, 0x9B                ;5B09
AFF:	mov A, [R1R0]                 ;04
B00:	mov R2, A                     ;24
B01:	mov A, [R3R2]                 ;06
B02:	mov R1R0, 0x99                ;5909
B04:	and A, [R1R0]                 ;1A
B05:	inc R0                        ;10
B06:	mov [R1R0], A                 ;05
B07:	mov R1R0, 0x95                ;5509
B09:	mov A, R4                     ;29
B0A:	add A, 0x5                    ;4005
B0C:	mov R0, A                     ;20
B0D:	mov R3R2, 0x9A                ;6A09
B0F:	mov A, [R3R2]                 ;06
B10:	or A, [R1R0]                  ;1C
B11:	mov R1R0, 0x9A                ;5A09
B13:	mov [R1R0], A                 ;05
B14:	mov A, 0xB                    ;7B
B15:	mov R3, A                     ;26
B16:	inc R0                        ;10
B17:	mov A, [R1R0]                 ;04
B18:	mov R2, A                     ;24
B19:	dec R0                        ;11
B1A:	mov A, [R1R0]                 ;04
B1B:	mov [R3R2], A                 ;07
B1C:	mov A, R2                     ;25
B1D:	inc A                         ;31
B1E:	inc A                         ;31
B1F:	inc R0                        ;10
B20:	mov [R1R0], A                 ;05
B21:	inc R4                        ;18
B22:	mov A, R4                     ;29
B23:	sub A, 0x4                    ;4104
B25:	jnz A, AFB                    ;BAFB
B27:	ret                           ;2E

;draw?:
B28:	mov R1R0, 0x97                ;5709
B2A:	mov A, [R1R0]                 ;04
B2B:	jz A, B2E                     ;B32E
B2D:	mov A, 0x5                    ;75
B2E:	mov R1R0, 0x92                ;5209
B30:	mov [R1R0], A                 ;05
B31:	dec R0                        ;11
B32:	dec R0                        ;11
B33:	mov [R1R0], A                 ;05
B34:	mov R1R0, 0x93                ;5309
B36:	mov A, 0x0                    ;70
B37:	mov [R1R0], A                 ;05
B38:	inc R0                        ;10
B39:	mov A, 0x0                    ;70
B3A:	mov [R1R0], A                 ;05
B3B:	mov R1R0, 0x91                ;5109
B3D:	mov A, [R1R0]                 ;04
B3E:	mov R4, A                     ;28
B3F:	mov A, R4                     ;29
B40:	jz A, B4E                     ;B34E
B42:	mov R1R0, 0x93                ;5309
B44:	mov A, 0xE                    ;7E
B45:	add A, [R1R0]                 ;09
B46:	mov [R1R0], A                 ;05
B47:	inc R0                        ;10
B48:	mov A, 0x1                    ;71
B49:	adc A, [R1R0]                 ;08
B4A:	mov [R1R0], A                 ;05
B4B:	dec R4                        ;19
B4C:	jmp B3F                       ;EB3F


B4E:	call AD9                      ;FAD9
B50:	and A, 0x3                    ;4203
B52:	jz A, B82                     ;B382
B54:	mov A, 0x0                    ;70
B55:	call BEC                      ;FBEC
B57:	or [R1R0], A                  ;1F
B58:	call AD9                      ;FAD9
B5A:	and A, 0x3                    ;4203
B5C:	dec A                         ;3F
B5D:	jz A, B6C                     ;B36C
B5F:	dec A                         ;3F
B60:	jz A, B72                     ;B372
B62:	mov A, 0x1                    ;71
B63:	call BEC                      ;FBEC
B65:	or [R1R0], A                  ;1F
B66:	mov A, 0x2                    ;72
B67:	call BEC                      ;FBEC
B69:	or [R1R0], A                  ;1F
B6A:	jmp B91                       ;EB91
B6C:	mov A, 0x1                    ;71
B6D:	call BEC                      ;FBEC
B6F:	or [R1R0], A                  ;1F
B70:	jmp B8C                       ;EB8C
B72:	mov A, 0x1                    ;71
B73:	call BEC                      ;FBEC
B75:	call AE5                      ;FAE5
B77:	mov A, 0x2                    ;72
B78:	call BEC                      ;FBEC
B7A:	call AE5                      ;FAE5
B7C:	mov A, 0x3                    ;73
B7D:	call BEC                      ;FBEC
B7F:	or [R1R0], A                  ;1F
B80:	jmp B96                       ;EB96
B82:	mov A, 0x0                    ;70
B83:	call BEC                      ;FBEC
B85:	call AE5                      ;FAE5
B87:	mov A, 0x1                    ;71
B88:	call BEC                      ;FBEC
B8A:	call AE5                      ;FAE5
B8C:	mov A, 0x2                    ;72
B8D:	call BEC                      ;FBEC
B8F:	call AE5                      ;FAE5
B91:	mov A, 0x3                    ;73
B92:	call BEC                      ;FBEC
B94:	call AE5                      ;FAE5
B96:	call AD9                      ;FAD9
B98:	ja2 BA1                       ;93A1
B9A:	mov A, 0x4                    ;74
B9B:	call BEC                      ;FBEC
B9D:	call AE5                      ;FAE5
B9F:	jmp BA5                       ;EBA5
BA1:	mov A, 0x4                    ;74
BA2:	call BEC                      ;FBEC
BA4:	or [R1R0], A                  ;1F
BA5:	call AD9                      ;FAD9
BA7:	ja3 BB0                       ;9BB0
BA9:	mov A, 0x5                    ;75
BAA:	call BEC                      ;FBEC
BAC:	call AE5                      ;FAE5
BAE:	jmp BB4                       ;EBB4
BB0:	mov A, 0x5                    ;75
BB1:	call BEC                      ;FBEC
BB3:	or [R1R0], A                  ;1F
BB4:	mov R1R0, 0x90                ;5009
BB6:	inc [R1R0]                    ;0C
BB7:	mov A, [R1R0]                 ;04
BB8:	sub A, 0x5                    ;4105
BBA:	jz A, BC0                     ;B3C0
BBC:	sub A, 0x5                    ;4105
BBE:	jnz A, BE2                    ;BBE2
BC0:	mov R3R2, 0x98                ;6809
BC2:	mov A, [R3R2]                 ;06
BC3:	jnz A, BD7                    ;BBD7
BC5:	call D67                      ;FD67
BC7:	sub A, 0x4                    ;4104
BC9:	jz A, BD1                     ;B3D1
BCB:	sub A, 0x5                    ;4105
BCD:	jz A, BD3                     ;B3D3
BCF:	jmp 0E0                       ;E0E0
BD1:	jmp 11E                       ;E11E
BD3:	jmp 204                       ;E204
BD5:	jmp 391                       ;E391
BD7:	mov R3R2, 0x92                ;6209
BD9:	mov A, [R3R2]                 ;06
BDA:	mov [R1R0], A                 ;05
BDB:	inc R0                        ;10
BDC:	inc [R1R0]                    ;0C
BDD:	mov A, [R1R0]                 ;04
BDE:	sub A, 0x8                    ;4108
BE0:	jz A, BE4                     ;B3E4
BE2:	jmp B4E                       ;EB4E

BE4:	call D67                      ;FD67
BE6:	sub A, 0x2                    ;4102
BE8:	jz A, BD5                     ;B3D5
BEA:	jmp 0AD                       ;E0AD

BEC:	mov R1R0, 0x96                ;5609
BEE:	mov [R1R0], A                 ;05
BEF:	mov R1R0, 0x94                ;5409
BF1:	mov A, [R1R0]                 ;04
BF2:	dec R0                        ;11
BF3:	readf R4A                     ;4D
BF4:	mov R0, A                     ;20
BF5:	mov A, R4                     ;29
BF6:	mov R1, A                     ;22
BF7:	mov R3R2, 0x93                ;6309
BF9:	mov A, [R3R2]                 ;06
BFA:	inc A                         ;31
BFB:	mov [R3R2], A                 ;07
BFC:	jnz A, C00                    ;BC00
BFE:	inc R2                        ;14
BFF:	inc [R3R2]                    ;0E
C00:	mov R3R2, 0x96                ;6609
C02:	mov A, [R3R2]                 ;06
C03:	jz A, C28                     ;B428
C05:	dec A                         ;3F
C06:	jz A, C2B                     ;B42B
C08:	dec A                         ;3F
C09:	jz A, C28                     ;B428
C0B:	dec A                         ;3F
C0C:	jz A, C11                     ;B411
C0E:	dec A                         ;3F
C0F:	jz A, C2B                     ;B42B
C11:	mov A, 0x4                    ;74
C12:	mov R3R2, 0x95                ;6509
C14:	mov [R3R2], A                 ;07
C15:	mov R3R2, 0x90                ;6009
C17:	mov A, [R3R2]                 ;06
C18:	sub A, 0x5                    ;4105
C1A:	jc C1D                        ;C41D
C1C:	mov A, [R3R2]                 ;06
C1D:	inc A                         ;31
C1E:	mov R4, A                     ;28
C1F:	mov R3R2, 0x95                ;6509
C21:	mov A, [R3R2]                 ;06
C22:	clc                           ;2A
C23:	rl A                          ;01
C24:	dec R4                        ;19
C25:	jnz R4, C23                   ;DC23
C27:	ret                           ;2E

C28:	mov A, 0x2                    ;72
C29:	jmp C12                       ;EC12
C2B:	mov A, 0x1                    ;71
C2C:	jmp C12                       ;EC12
C2E:	mov R1R0, 0x9C                ;5C09
C30:	mov A, 0x0                    ;70
C31:	mov [R1R0], A                 ;05
C32:	mov R1R0, 0x9C                ;5C09
C34:	mov A, [R1R0]                 ;04
C35:	mov R2, A                     ;24
C36:	mov R1R0, 0x90                ;5009
C38:	mov A, R2                     ;25
C39:	jz A, C3D                     ;B43D
C3B:	mov R1R0, 0x92                ;5209
C3D:	mov A, 0xF                    ;7F
C3E:	readf R4A                     ;4D
C3F:	mov R3, A                     ;26
C40:	and A, 0xC                    ;420C
C42:	mov R1R0, 0x95                ;5509
C44:	mov [R1R0], A                 ;05
C45:	call AE9                      ;FAE9
C47:	mov A, R4                     ;29
C48:	mov R3, A                     ;26
C49:	and A, 0xC                    ;420C
C4B:	mov R1R0, 0x97                ;5709
C4D:	mov [R1R0], A                 ;05
C4E:	call AE9                      ;FAE9
C50:	call ECD                      ;FECD
C52:	mov A, 0x3                    ;73
C53:	mov [R1R0], A                 ;05
C54:	call AF9                      ;FAF9
C56:	mov R1R0, 0x9C                ;5C09
C58:	mov A, [R1R0]                 ;04
C59:	mov R2, A                     ;24
C5A:	mov R1R0, 0x91                ;5109
C5C:	mov A, R2                     ;25
C5D:	jz A, C61                     ;B461
C5F:	mov R1R0, 0x93                ;5309
C61:	mov A, 0xF                    ;7F
C62:	readf R4A                     ;4D
C63:	mov R3, A                     ;26
C64:	and A, 0x3                    ;4203
C66:	mov R1R0, 0x96                ;5609
C68:	mov [R1R0], A                 ;05
C69:	call AF1                      ;FAF1
C6B:	mov A, R4                     ;29
C6C:	mov R3, A                     ;26
C6D:	and A, 0x3                    ;4203
C6F:	mov R1R0, 0x98                ;5809
C71:	mov [R1R0], A                 ;05
C72:	call AF1                      ;FAF1
C74:	call ECD                      ;FECD
C76:	mov A, 0xC                    ;7C
C77:	mov [R1R0], A                 ;05
C78:	call AF9                      ;FAF9
C7A:	mov R1R0, 0x9C                ;5C09
C7C:	inc [R1R0]                    ;0C
C7D:	mov A, [R1R0]                 ;04
C7E:	sub A, 0x2                    ;4102
C80:	jnz A, C32                    ;BC32
C82:	mov R1R0, 0x94                ;5409
C84:	mov A, [R1R0]                 ;04
C85:	ja0 C8F                       ;848F
C87:	mov R1R0, 0xB6                ;560B
C89:	mov A, 0x1                    ;71
C8A:	or [R1R0], A                  ;1F
C8B:	xor A, [R1R0]                 ;1B
C8C:	mov [R1R0], A                 ;05
C8D:	jmp C93                       ;EC93
C8F:	mov R1R0, 0xB6                ;560B
C91:	mov A, 0x1                    ;71
C92:	or [R1R0], A                  ;1F
C93:	call D67                      ;FD67
C95:	dec A                         ;3F
C96:	jz A, C9A                     ;B49A
C98:	jmp 10D                       ;E10D
C9A:	jmp 10D                       ;E10D
C9C:	mov R4, 0xE                   ;460E
C9E:	mov R1R0, 0xBE                ;5E0B
CA0:	mov R3R2, 0x90                ;6009
CA2:	mov A, 0xE                    ;7E
CA3:	and A, [R1R0]                 ;1A
CA4:	mov [R3R2], A                 ;07
CA5:	dec R4                        ;19
CA6:	inc R2                        ;14
CA7:	inc R0                        ;10
CA8:	inc R0                        ;10
CA9:	mov A, R0                     ;21
CAA:	jnz A, CAD                    ;BCAD
CAC:	inc R1                        ;12
CAD:	jnz R4, CA2                   ;DCA2
CAF:	mov R1R0, 0x0A                ;5A00
CB1:	mov A, [R1R0]                 ;04
CB2:	jz A, CE5                     ;B4E5
CB4:	dec A                         ;3F
CB5:	jz A, CE7                     ;B4E7
CB7:	dec A                         ;3F
CB8:	jz A, CF5                     ;B4F5
CBA:	dec A                         ;3F
CBB:	jz A, D08                     ;B508
CBD:	dec A                         ;3F
CBE:	jz A, D10                     ;B510
CC0:	dec A                         ;3F
CC1:	jz A, D18                     ;B518
CC3:	dec A                         ;3F
CC4:	jz A, D20                     ;B520
CC6:	mov R4, A                     ;28
CC7:	mov R1R0, 0xCA                ;5A0C
CC9:	mov R3R2, 0x96                ;6609
CCB:	call EE7                      ;FEE7
CCD:	jnz A, CD0                    ;BCD0
CCF:	inc R1                        ;12
CD0:	jnz R4, CCB                   ;DCCB
CD2:	call EDD                      ;FEDD
CD4:	mov R4, 0xE                   ;460E
CD6:	mov R1R0, 0xBE                ;5E0B
CD8:	mov R3R2, 0x90                ;6009
CDA:	mov A, [R3R2]                 ;06
CDB:	mov [R1R0], A                 ;05
CDC:	call EE7                      ;FEE7
CDE:	jnz A, CE1                    ;BCE1
CE0:	inc R1                        ;12
CE1:	jnz R4, CDA                   ;DCDA
CE3:	jmp 06A                       ;E06A
CE5:	jmp CD4                       ;ECD4
CE7:	mov R1R0, 0xC0                ;500C
CE9:	mov R3R2, 0x91                ;6109
CEB:	call EDD                      ;FEDD
CED:	mov R1R0, 0xC2                ;520C
CEF:	mov R3R2, 0x92                ;6209
CF1:	call EDD                      ;FEDD
CF3:	jmp CD4                       ;ECD4
CF5:	mov R1R0, 0x1E                ;5E01
CF7:	mov A, [R1R0]                 ;04
CF8:	ja2 CE7                       ;94E7
CFA:	mov R1R0, 0xBE                ;5E0B
CFC:	mov R3R2, 0x90                ;6009
CFE:	call EDD                      ;FEDD
D00:	mov R1R0, 0xC2                ;520C
D02:	mov R3R2, 0x92                ;6209
D04:	call EDD                      ;FEDD
D06:	jmp CD4                       ;ECD4
D08:	mov R1R0, 0xC4                ;540C
D0A:	mov R3R2, 0x93                ;6309
D0C:	call EDD                      ;FEDD
D0E:	jmp CD4                       ;ECD4
D10:	mov R1R0, 0xC6                ;560C
D12:	mov R3R2, 0x94                ;6409
D14:	call EDD                      ;FEDD
D16:	jmp CD4                       ;ECD4
D18:	mov R1R0, 0xC8                ;580C
D1A:	mov R3R2, 0x95                ;6509
D1C:	call EDD                      ;FEDD
D1E:	jmp CD4                       ;ECD4
D20:	mov R1R0, 0xC8                ;580C
D22:	mov R3R2, 0x95                ;6509
D24:	call EDD                      ;FEDD
D26:	mov R1R0, 0xCA                ;5A0C
D28:	mov R3R2, 0x96                ;6609
D2A:	call EDD                      ;FEDD
D2C:	jmp CD4                       ;ECD4
D2E:	mov R4, 0x4                   ;4604
D30:	mov A, [R1R0]                 ;04
D31:	mov [R3R2], A                 ;07
D32:	inc R0                        ;10
D33:	inc R2                        ;14
D34:	dec R4                        ;19
D35:	jnz R4, D30                   ;DD30
D37:	ret                           ;2E
D38:	mov A, [R3R2]                 ;06
D39:	mov R0, A                     ;20
D3A:	inc R2                        ;14
D3B:	mov A, [R3R2]                 ;06
D3C:	mov R1, A                     ;22
D3D:	ret                           ;2E
D3E:	mov A, [R3R2]                 ;06
D3F:	mov R0, A                     ;20
D40:	inc R2                        ;14
D41:	mov A, [R3R2]                 ;06
D42:	mov R1, A                     ;22
D43:	mov A, [R1R0]                 ;04
D44:	ret                           ;2E
D45:	mov A, 0x0                    ;70
D46:	mov R1R0, 0xB4                ;540B
D48:	mov [R1R0], A                 ;05
D49:	inc R0                        ;10
D4A:	jnz R0, D48                   ;A548
D4C:	inc R1                        ;12
D4D:	jnz R1, D48                   ;AD48
D4F:	ret                           ;2E
D50:	mov R1R0, 0x1E                ;5E01
D52:	mov A, 0x0                    ;70
D53:	mov [R1R0], A                 ;05
D54:	inc R0                        ;10
D55:	mov [R1R0], A                 ;05
D56:	ret                           ;2E
D57:	mov R1R0, 0x0D                ;5D00
D59:	mov A, [R1R0]                 ;04
D5A:	ret                           ;2E
D5B:	mov R1R0, 0x0C                ;5C00
D5D:	mov A, [R1R0]                 ;04
D5E:	ret                           ;2E
D5F:	mov R1R0, 0x7C                ;5C07
D61:	mov [R1R0], A                 ;05
D62:	ret                           ;2E
D63:	mov R1R0, 0x2E                ;5E02
D65:	mov [R1R0], A                 ;05
D66:	ret                           ;2E
D67:	mov R3R2, 0x2E                ;6E02
D69:	mov A, [R3R2]                 ;06
D6A:	ret                           ;2E
D6B:	mov R3R2, 0x2F                ;6F02
D6D:	mov [R3R2], A                 ;07
D6E:	ret                           ;2E
D6F:	mov R1R0, 0x0B                ;5B00
D71:	mov [R1R0], A                 ;05
D72:	ret                           ;2E
D73:	mov R1R0, 0x8F                ;5F08
D75:	mov R3R2, 0x6F                ;6F06
D77:	clc                           ;2A
D78:	mov A, [R3R2]                 ;06
D79:	add A, [R1R0]                 ;09
D7A:	jnc D81                       ;CD81
D7C:	sub A, 0xA                    ;410A
D7E:	stc                           ;2B
D7F:	jmp D82                       ;ED82
D81:	daa                           ;36
D82:	mov [R1R0], A                 ;05
D83:	mov R4, 0x2                   ;4602
D85:	dec R0                        ;11
D86:	dec R2                        ;15
D87:	mov A, [R3R2]                 ;06
D88:	adc A, [R1R0]                 ;08
D89:	jnc D90                       ;CD90
D8B:	sub A, 0xA                    ;410A
D8D:	stc                           ;2B
D8E:	jmp D91                       ;ED91
D90:	daa                           ;36
D91:	mov [R1R0], A                 ;05
D92:	dec R4                        ;19
D93:	jnz R4, D85                   ;DD85
D95:	dec R0                        ;11
D96:	mov A, 0x0                    ;70
D97:	adc A, [R1R0]                 ;08
D98:	jnc D9F                       ;CD9F
D9A:	sub A, 0xA                    ;410A
D9C:	stc                           ;2B
D9D:	jmp DA0                       ;EDA0
D9F:	daa                           ;36
DA0:	mov [R1R0], A                 ;05
DA1:	jnc DAA                       ;CDAA
DA3:	mov R1R0, 0x8C                ;5C08
DA5:	mov A, 0x9                    ;79
DA6:	mov [R1R0], A                 ;05
DA7:	inc R0                        ;10
DA8:	jnz R0, DA6                   ;A5A6
DAA:	ret                           ;2E
DAB:	mov R4, 0x0                   ;4600
DAD:	jmp DB1                       ;EDB1
DAF:	mov R4, 0x1                   ;4601
DB1:	mov R1R0, 0x00                ;5000
DB3:	mov R3R2, 0x05                ;6500
DB5:	mov A, 0x0                    ;70
DB6:	mov R0, A                     ;20
DB7:	mov A, 0x5                    ;75
DB8:	mov R2, A                     ;24
DB9:	jnz R4, DBF                   ;DDBF
DBB:	mov A, [R1R0]                 ;04
DBC:	mov [R3R2], A                 ;07
DBD:	jmp DC1                       ;EDC1
DBF:	mov A, [R3R2]                 ;06
DC0:	mov [R1R0], A                 ;05
DC1:	inc R0                        ;10
DC2:	inc R2                        ;14
DC3:	mov A, R0                     ;21
DC4:	sub A, 0x5                    ;4105
DC6:	jnz A, DB9                    ;BDB9
DC8:	inc R1                        ;12
DC9:	inc R3                        ;16
DCA:	mov A, R1                     ;23
DCB:	sub A, 0x8                    ;4108
DCD:	jnz A, DB5                    ;BDB5
DCF:	ret                           ;2E
DD0:	mov A, [R1R0]                 ;04
DD1:	inc A                         ;31
DD2:	jz A, DD5                     ;B5D5
DD4:	inc [R1R0]                    ;0C
DD5:	ret                           ;2E
DD6:	mov A, [R1R0]                 ;04
DD7:	inc A                         ;31
DD8:	jnz A, DDE                    ;BDDE
DDA:	mov A, [R3R2]                 ;06
DDB:	inc A                         ;31
DDC:	jz A, DE7                     ;B5E7
DDE:	inc [R1R0]                    ;0C
DDF:	mov A, [R1R0]                 ;04
DE0:	jnz A, DE7                    ;BDE7
DE2:	mov A, [R3R2]                 ;06
DE3:	inc A                         ;31
DE4:	jz A, DE7                     ;B5E7
DE6:	inc [R3R2]                    ;0E
DE7:	ret                           ;2E
DE8:	mov R1R0, 0x93                ;5309
DEA:	mov R3R2, 0x91                ;6109
DEC:	mov A, [R3R2]                 ;06
DED:	sub A, [R1R0]                 ;0B
DEE:	jz A, DF4                     ;B5F4
DF0:	jc DFE                        ;C5FE
DF2:	jmp E01                       ;EE01
DF4:	dec R0                        ;11
DF5:	dec R2                        ;15
DF6:	mov A, [R3R2]                 ;06
DF7:	sub A, [R1R0]                 ;0B
DF8:	jz A, E01                     ;B601
DFA:	jc DFE                        ;C5FE
DFC:	jmp E01                       ;EE01
DFE:	mov A, 0x0                    ;70
DFF:	jmp E02                       ;EE02
E01:	mov A, 0x1                    ;71
E02:	mov R3R2, 0x94                ;6409
E04:	mov [R3R2], A                 ;07
E05:	ret                           ;2E
E06:	mov R1R0, 0x00                ;5000
E08:	mov A, 0x0                    ;70
E09:	mov [R1R0], A                 ;05
E0A:	inc R0                        ;10
E0B:	mov A, R0                     ;21
E0C:	sub A, 0xA                    ;410A
E0E:	jnz A, E08                    ;BE08
E10:	mov A, 0x0                    ;70
E11:	mov R0, A                     ;20
E12:	inc R1                        ;12
E13:	mov A, R1                     ;23
E14:	sub A, 0x8                    ;4108
E16:	jnz A, E08                    ;BE08
E18:	ret                           ;2E
E19:	mov R1R0, 0x5F                ;5F05
E1B:	mov A, 0x1                    ;71
E1C:	or [R1R0], A                  ;1F
E1D:	ret                           ;2E
E1E:	mov R1R0, 0x5E                ;5E05
E20:	mov A, 0x4                    ;74
E21:	xor A, 0xF                    ;430F
E23:	and [R1R0], A                 ;1D
E24:	ret                           ;2E
E25:	mov R1R0, 0x5F                ;5F05
E27:	mov A, 0x1                    ;71
E28:	jmp E21                       ;EE21
E2A:	mov R1R0, 0x5E                ;5E05
E2C:	mov A, 0x2                    ;72
E2D:	jmp E21                       ;EE21
E2F:	mov A, R0                     ;21
E30:	mov R3R2, 0x90                ;6009
E32:	mov [R3R2], A                 ;07
E33:	mov A, R1                     ;23
E34:	inc R2                        ;14
E35:	mov [R3R2], A                 ;07
E36:	inc R2                        ;14
E37:	mov R1R0, 0x7A                ;5A07
E39:	mov A, [R1R0]                 ;04
E3A:	mov [R3R2], A                 ;07
E3B:	inc R0                        ;10
E3C:	inc R2                        ;14
E3D:	mov A, [R1R0]                 ;04
E3E:	mov [R3R2], A                 ;07
E3F:	ret                           ;2E
E40:	mov A, [R1R0]                 ;04
E41:	mov R3R2, 0x91                ;6109
E43:	mov [R3R2], A                 ;07
E44:	mov R3R2, 0x93                ;6309
E46:	mov [R3R2], A                 ;07
E47:	dec R0                        ;11
E48:	mov A, [R1R0]                 ;04
E49:	mov R3R2, 0x90                ;6009
E4B:	mov [R3R2], A                 ;07
E4C:	mov R3R2, 0x92                ;6209
E4E:	mov [R3R2], A                 ;07
E4F:	ret                           ;2E
E50:	mov A, 0x7                    ;77
E51:	mov R1R0, 0x93                ;5309
E53:	mov [R1R0], A                 ;05
E54:	mov A, 0x7                    ;77
E55:	mov R1R0, 0x91                ;5109
E57:	mov [R1R0], A                 ;05
E58:	ret                           ;2E
E59:	mov R1R0, 0x91                ;5109
E5B:	dec [R1R0]                    ;0D
E5C:	mov A, [R1R0]                 ;04
E5D:	mov R3R2, 0x93                ;6309
E5F:	mov [R3R2], A                 ;07
E60:	ret                           ;2E
E61:	mov R1R0, 0x92                ;5209
E63:	inc [R1R0]                    ;0C
E64:	mov R1R0, 0x90                ;5009
E66:	inc [R1R0]                    ;0C
E67:	mov A, [R1R0]                 ;04
E68:	sub A, 0x5                    ;4105
E6A:	ret                           ;2E
E6B:	mov R1R0, 0x3C                ;5C03
E6D:	mov [R1R0], A                 ;05
E6E:	mov R1R0, 0x3A                ;5A03
E70:	mov R3R2, 0x90                ;6009
E72:	mov A, [R3R2]                 ;06
E73:	mov [R1R0], A                 ;05
E74:	inc R0                        ;10
E75:	inc R2                        ;14
E76:	mov A, [R3R2]                 ;06
E77:	mov [R1R0], A                 ;05
E78:	ret                           ;2E
E79:	mov R1R0, 0x5A                ;5A05
E7B:	mov A, [R1R0]                 ;04
E7C:	mov R4, A                     ;28
E7D:	mov R3R2, 0x3A                ;6A03
E7F:	ret                           ;2E
E80:	mov A, R0                     ;21
E81:	add A, 0x5                    ;4005
E83:	mov R0, A                     ;20
E84:	ret                           ;2E
E85:	mov R1R0, 0x5A                ;5A05
E87:	mov A, 0x1                    ;71
E88:	mov [R1R0], A                 ;05
E89:	ret                           ;2E
E8A:	mov R1R0, 0x91                ;5109
E8C:	dec [R1R0]                    ;0D
E8D:	mov A, [R1R0]                 ;04
E8E:	inc A                         ;31
E8F:	ret                           ;2E
E90:	mov R1R0, 0x90                ;5009
E92:	dec [R1R0]                    ;0D
E93:	mov A, [R1R0]                 ;04
E94:	inc A                         ;31
E95:	ret                           ;2E
E96:	mov R1R0, 0x3C                ;5C03
E98:	xor A, [R1R0]                 ;1B
E99:	and A, 0xB                    ;420B
E9B:	ret                           ;2E
E9C:	mov R3R2, 0x88                ;6808
E9E:	mov A, [R3R2]                 ;06
E9F:	or A, [R1R0]                  ;1C
EA0:	mov [R3R2], A                 ;07
EA1:	inc R2                        ;14
EA2:	inc R0                        ;10
EA3:	mov A, [R3R2]                 ;06
EA4:	or A, [R1R0]                  ;1C
EA5:	mov [R3R2], A                 ;07
EA6:	ret                           ;2E
EA7:	mov R1R0, 0x88                ;5808
EA9:	mov A, [R1R0]                 ;04
EAA:	ret                           ;2E
EAB:	mov R3R2, 0x94                ;6409
EAD:	mov A, [R3R2]                 ;06
EAE:	ret                           ;2E
EAF:	mov A, [R1R0]                 ;04
EB0:	inc R1                        ;12
EB1:	mov [R1R0], A                 ;05
EB2:	ret                           ;2E
EB3:	inc R0                        ;10
EB4:	mov [R1R0], A                 ;05
EB5:	inc R0                        ;10
EB6:	mov [R1R0], A                 ;05
EB7:	ret                           ;2E
EB8:	mov [R1R0], A                 ;05
EB9:	inc R0                        ;10
EBA:	mov A, 0x0                    ;70
EBB:	mov [R1R0], A                 ;05
EBC:	ret                           ;2E
EBD:	mov R1R0, 0x93                ;5309
EBF:	mov A, [R3R2]                 ;06
EC0:	sub A, [R1R0]                 ;0B
EC1:	mov [R3R2], A                 ;07
EC2:	ret                           ;2E
EC3:	mov A, 0x0                    ;70
EC4:	mov R1R0, 0x90                ;5009
EC6:	mov [R1R0], A                 ;05
EC7:	ret                           ;2E
EC8:	mov A, 0x3                    ;73
EC9:	mov R1R0, 0x1E                ;5E01
ECB:	and A, [R1R0]                 ;1A
ECC:	ret                           ;2E
ECD:	mov R1R0, 0x9C                ;5C09
ECF:	mov A, 0x7                    ;77
ED0:	sub A, [R1R0]                 ;0B
ED1:	mov R1R0, 0x9B                ;5B09
ED3:	mov [R1R0], A                 ;05
ED4:	mov R1R0, 0x99                ;5909
ED6:	ret                           ;2E
ED7:	mov R1R0, 0x0B                ;5B00
ED9:	mov A, [R1R0]                 ;04
EDA:	dec R0                        ;11
EDB:	mov [R1R0], A                 ;05
EDC:	ret                           ;2E
EDD:	mov A, 0x1                    ;71
EDE:	or A, [R1R0]                  ;1C
EDF:	mov [R3R2], A                 ;07
EE0:	ret                           ;2E
EE1:	mov R3R2, 0x8B                ;6B08
EE3:	mov A, [R3R2]                 ;06
EE4:	sub A, 0x3                    ;4103
EE6:	ret                           ;2E
EE7:	dec R4                        ;19
EE8:	inc R2                        ;14
EE9:	inc R0                        ;10
EEA:	inc R0                        ;10
EEB:	mov A, R0                     ;21
EEC:	ret                           ;2E
EED:	mov R1R0, 0x97                ;5709
EEF:	mov [R1R0], A                 ;05
EF0:	inc R0                        ;10
EF1:	mov A, 0x1                    ;71
EF2:	mov [R1R0], A                 ;05
EF3:	mov R0, A                     ;20
EF4:	mov A, 0x0                    ;70
EF5:	mov [R1R0], A                 ;05
EF6:	ret                           ;2E

EF7:	db 0x2E                       ;2E
EF8:	db 0x3E                       ;3E
EF9:	db 0x3E                       ;3E
EFA:	db 0x3E                       ;3E
EFB:	db 0x3E                       ;3E
EFC:	db 0x3E                       ;3E
EFD:	db 0x3E                       ;3E
EFE:	db 0x3E                       ;3E
EFF:	db 0x3E                       ;3E
F00:	db 0xFB                       ;FB
F01:	db 0xFB                       ;FB
F02:	db 0xFD                       ;FD
F03:	db 0xFB                       ;FB
F04:	db 0xFD                       ;FD
F05:	db 0xFD                       ;FD
F06:	db 0xFA                       ;FA
F07:	db 0xFA                       ;FA
F08:	db 0xFC                       ;FC
F09:	db 0xFB                       ;FB
F0A:	db 0xFC                       ;FC
F0B:	db 0xFD                       ;FD
F0C:	db 0xFA                       ;FA
F0D:	db 0xC1                       ;C1
F0E:	db 0xFC                       ;FC
F0F:	db 0xFA                       ;FA
F10:	db 0xBF                       ;BF
F11:	db 0xFC                       ;FC
F12:	db 0xC1                       ;C1
F13:	db 0xC1                       ;C1
F14:	db 0xBF                       ;BF
F15:	db 0xC1                       ;C1
F16:	db 0xBF                       ;BF
F17:	db 0xBF                       ;BF
F18:	db 0xC0                       ;C0
F19:	db 0xC0                       ;C0
F1A:	db 0xBE                       ;BE
F1B:	db 0xC0                       ;C0
F1C:	db 0xBE                       ;BE
F1D:	db 0xBE                       ;BE
F1E:	db 0xF7                       ;F7
F1F:	db 0xF7                       ;F7
F20:	db 0xF9                       ;F9
F21:	db 0xF7                       ;F7
F22:	db 0xF9                       ;F9
F23:	db 0xF9                       ;F9
F24:	db 0xF6                       ;F6
F25:	db 0xF6                       ;F6
F26:	db 0xF8                       ;F8
F27:	db 0xF7                       ;F7
F28:	db 0xF8                       ;F8
F29:	db 0xF9                       ;F9
F2A:	db 0xF6                       ;F6
F2B:	db 0xC5                       ;C5
F2C:	db 0xF8                       ;F8
F2D:	db 0xF6                       ;F6
F2E:	db 0xC3                       ;C3
F2F:	db 0xF8                       ;F8
F30:	db 0xC5                       ;C5
F31:	db 0xC5                       ;C5
F32:	db 0xC3                       ;C3
F33:	db 0xC5                       ;C5
F34:	db 0xC3                       ;C3
F35:	db 0xC3                       ;C3
F36:	db 0xC4                       ;C4
F37:	db 0xC4                       ;C4
F38:	db 0xC2                       ;C2
F39:	db 0xC4                       ;C4
F3A:	db 0xC2                       ;C2
F3B:	db 0xC2                       ;C2
F3C:	db 0xF3                       ;F3
F3D:	db 0xF3                       ;F3
F3E:	db 0xF5                       ;F5
F3F:	db 0xF3                       ;F3
F40:	db 0xF5                       ;F5
F41:	db 0xF5                       ;F5
F42:	db 0xF2                       ;F2
F43:	db 0xF2                       ;F2
F44:	db 0xF4                       ;F4
F45:	db 0xF3                       ;F3
F46:	db 0xF4                       ;F4
F47:	db 0xF5                       ;F5
F48:	db 0xF2                       ;F2
F49:	db 0xC9                       ;C9
F4A:	db 0xF4                       ;F4
F4B:	db 0xF2                       ;F2
F4C:	db 0xC7                       ;C7
F4D:	db 0xF4                       ;F4
F4E:	db 0xC9                       ;C9
F4F:	db 0xC9                       ;C9
F50:	db 0xC7                       ;C7
F51:	db 0xC9                       ;C9
F52:	db 0xC7                       ;C7
F53:	db 0xC7                       ;C7
F54:	db 0xC8                       ;C8
F55:	db 0xC8                       ;C8
F56:	db 0xC6                       ;C6
F57:	db 0xC8                       ;C8
F58:	db 0xC6                       ;C6
F59:	db 0xC6                       ;C6
F5A:	db 0xEF                       ;EF
F5B:	db 0xEF                       ;EF
F5C:	db 0xF1                       ;F1
F5D:	db 0xEF                       ;EF
F5E:	db 0xF1                       ;F1
F5F:	db 0xF1                       ;F1
F60:	db 0xEE                       ;EE
F61:	db 0xEE                       ;EE
F62:	db 0xF0                       ;F0
F63:	db 0xEF                       ;EF
F64:	db 0xF0                       ;F0
F65:	db 0xF1                       ;F1
F66:	db 0xEE                       ;EE
F67:	db 0xCD                       ;CD
F68:	db 0xF0                       ;F0
F69:	db 0xEE                       ;EE
F6A:	db 0xCB                       ;CB
F6B:	db 0xF0                       ;F0
F6C:	db 0xCD                       ;CD
F6D:	db 0xCD                       ;CD
F6E:	db 0xCB                       ;CB
F6F:	db 0xCD                       ;CD
F70:	db 0xCB                       ;CB
F71:	db 0xCB                       ;CB
F72:	db 0xCC                       ;CC
F73:	db 0xCC                       ;CC
F74:	db 0xCA                       ;CA
F75:	db 0xCC                       ;CC
F76:	db 0xCA                       ;CA
F77:	db 0xCA                       ;CA
F78:	db 0xEB                       ;EB
F79:	db 0xEB                       ;EB
F7A:	db 0xED                       ;ED
F7B:	db 0xEB                       ;EB
F7C:	db 0xED                       ;ED
F7D:	db 0xED                       ;ED
F7E:	db 0xEA                       ;EA
F7F:	db 0xEA                       ;EA
F80:	db 0xEC                       ;EC
F81:	db 0xEB                       ;EB
F82:	db 0xEC                       ;EC
F83:	db 0xED                       ;ED
F84:	db 0xEA                       ;EA
F85:	db 0xD1                       ;D1
F86:	db 0xEC                       ;EC
F87:	db 0xEA                       ;EA
F88:	db 0xCF                       ;CF
F89:	db 0xEC                       ;EC
F8A:	db 0xD1                       ;D1
F8B:	db 0xD1                       ;D1
F8C:	db 0xCF                       ;CF
F8D:	db 0xD1                       ;D1
F8E:	db 0xCF                       ;CF
F8F:	db 0xCF                       ;CF
F90:	db 0xD0                       ;D0
F91:	db 0xD0                       ;D0
F92:	db 0xCE                       ;CE
F93:	db 0xD0                       ;D0
F94:	db 0xCE                       ;CE
F95:	db 0xCE                       ;CE
F96:	db 0xE7                       ;E7
F97:	db 0xE7                       ;E7
F98:	db 0xE9                       ;E9
F99:	db 0xE7                       ;E7
F9A:	db 0xE9                       ;E9
F9B:	db 0xE9                       ;E9
F9C:	db 0xE6                       ;E6
F9D:	db 0xE6                       ;E6
F9E:	db 0xE8                       ;E8
F9F:	db 0xE7                       ;E7
FA0:	db 0xE8                       ;E8
FA1:	db 0xE9                       ;E9
FA2:	db 0xE6                       ;E6
FA3:	db 0xD5                       ;D5
FA4:	db 0xE8                       ;E8
FA5:	db 0xE6                       ;E6
FA6:	db 0xD3                       ;D3
FA7:	db 0xE8                       ;E8
FA8:	db 0xD5                       ;D5
FA9:	db 0xD5                       ;D5
FAA:	db 0xD3                       ;D3
FAB:	db 0xD5                       ;D5
FAC:	db 0xD3                       ;D3
FAD:	db 0xD3                       ;D3
FAE:	db 0xD4                       ;D4
FAF:	db 0xD4                       ;D4
FB0:	db 0xD2                       ;D2
FB1:	db 0xD4                       ;D4
FB2:	db 0xD2                       ;D2
FB3:	db 0xD2                       ;D2
FB4:	db 0xE3                       ;E3
FB5:	db 0xE3                       ;E3
FB6:	db 0xE5                       ;E5
FB7:	db 0xE3                       ;E3
FB8:	db 0xE5                       ;E5
FB9:	db 0xE5                       ;E5
FBA:	db 0xE2                       ;E2
FBB:	db 0xE2                       ;E2
FBC:	db 0xE4                       ;E4
FBD:	db 0xE3                       ;E3
FBE:	db 0xE4                       ;E4
FBF:	db 0xE5                       ;E5
FC0:	db 0xE2                       ;E2
FC1:	db 0xD9                       ;D9
FC2:	db 0xE4                       ;E4
FC3:	db 0xE2                       ;E2
FC4:	db 0xD7                       ;D7
FC5:	db 0xE4                       ;E4
FC6:	db 0xD9                       ;D9
FC7:	db 0xD9                       ;D9
FC8:	db 0xD7                       ;D7
FC9:	db 0xD9                       ;D9
FCA:	db 0xD7                       ;D7
FCB:	db 0xD7                       ;D7
FCC:	db 0xD8                       ;D8
FCD:	db 0xD8                       ;D8
FCE:	db 0xD6                       ;D6
FCF:	db 0xD8                       ;D8
FD0:	db 0xD6                       ;D6
FD1:	db 0xD6                       ;D6
FD2:	db 0xDF                       ;DF
FD3:	db 0xDF                       ;DF
FD4:	db 0xE1                       ;E1
FD5:	db 0xDF                       ;DF
FD6:	db 0xE1                       ;E1
FD7:	db 0xE1                       ;E1
FD8:	db 0xDE                       ;DE
FD9:	db 0xDE                       ;DE
FDA:	db 0xE0                       ;E0
FDB:	db 0xDF                       ;DF
FDC:	db 0xE0                       ;E0
FDD:	db 0xE1                       ;E1
FDE:	db 0xDE                       ;DE
FDF:	db 0xDD                       ;DD
FE0:	db 0xE0                       ;E0
FE1:	db 0xDE                       ;DE
FE2:	db 0xDB                       ;DB
FE3:	db 0xE0                       ;E0
FE4:	db 0xDD                       ;DD
FE5:	db 0xDD                       ;DD
FE6:	db 0xDB                       ;DB
FE7:	db 0xDD                       ;DD
FE8:	db 0xDB                       ;DB
FE9:	db 0xDB                       ;DB
FEA:	db 0xDC                       ;DC
FEB:	db 0xDC                       ;DC
FEC:	db 0xDA                       ;DA
FED:	db 0xDC                       ;DC
FEE:	db 0xDA                       ;DA
FEF:	db 0xDA                       ;DA
FF0:	db 0xBB                       ;BB
FF1:	db 0x11                       ;11
FF2:	db 0xE9                       ;E9
FF3:	db 0x79                       ;79
FF4:	db 0x53                       ;53
FF5:	db 0x7A                       ;7A
FF6:	db 0xFA                       ;FA
FF7:	db 0x19                       ;19
FF8:	db 0xFB                       ;FB
FF9:	db 0x7B                       ;7B
FFA:	db 0x00                       ;00
FFB:	db 0x40                       ;40
FFC:	db 0xA2                       ;A2
FFD:	db 0x00                       ;00
FFE:	db 0x00                       ;00
FFF:	db 0x00                       ;00
