; Author: tokumaru
; http://forums.nesdev.com/viewtopic.php?%20p=58138#58138
;----------------------------------------------------------------
; constants
;----------------------------------------------------------------
PRG_COUNT = 1 ;1 = 16KB, 2 = 32KB
MIRRORING = %0001 ;%0000 = horizontal, %0001 = vertical, %1000 = four-screen

;----------------------------------------------------------------
; variables
;----------------------------------------------------------------

   .enum $0000

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

   .ende

   ;NOTE: you can also split the variable declarations into individual pages, like this:

   ;.enum $0100
   ;.ende

   ;.enum $0200
   ;.ende

;----------------------------------------------------------------
; iNES header
;----------------------------------------------------------------

   .db "NES", $1a ;identification of the iNES header
   .db PRG_COUNT ;number of 16KB PRG-ROM pages
   .db $01 ;number of 8KB CHR-ROM pages
   .db $00|MIRRORING ;mapper 0 and mirroring
   .dsb 9, $00 ;clear the remaining bytes

;----------------------------------------------------------------
; program bank(s)
;----------------------------------------------------------------

   .base $10000-(PRG_COUNT*$4000)

Reset:
                        ; PC = c000, V = 0, mem = c000
    JMP address_3       ; PC = c00d, V = 0, mem = c000
address_0:
    ADC #$FF            ; PC = c004, V = 0, mem = c003
    ADC #$80            ; PC = c006, V = 1, mem = c005
    JMP $c00c           ; PC = c00c, V = 1, mem = c007
    ADC #$00            ; PC = c00a, V = 1, mem = c00a
    JMP $c00f           ; PC = c00f, V = 1, mem = c00c
address_1:
    BRK                 ; Abort execution, mem = c00f

address_2:
    JMP address_1       ; PC = c002, V = 0, mem = c010
address_3:
    JMP address_2       ; PC = c00c, V = 1, mem = c013


   .org $E000
data_1:
	.db $c0, $13        ; mem = e000, e001
data_2:
	.db $c0, $0f        ; mem = e002, e003

NMI:

   ;NOTE: NMI code goes here

IRQ:

   ;NOTE: IRQ code goes here

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   .org $fffa

   .dw NMI
   .dw Reset
   .dw IRQ

;----------------------------------------------------------------
; CHR ROM bank(s)
;----------------------------------------------------------------

   .dsb 8192 ; one CHR ROM bank
