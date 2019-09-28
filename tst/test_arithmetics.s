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

   zero_page_var: 
      .DSB 1
   

   ;NOTE: declare variables using the DSB and DSW directives, like this:

   ;MyVariable0 .dsb 1
   ;MyVariable1 .dsb 3

   .ende

   ;NOTE: you can also split the variable declarations into individual pages, like this:

   .enum $0100
      absolute_value_1:
      .DSB 1
      absolute_value_2:
      .DSB 1
   .ende

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
   LDA #$02                ; pc = 0xc002
   STA absolute_value_1    ; pc = 0xc005
   LDA #$08                ; pc = 0xc007
   ADC $0100               ; pc = 0xc00a
   CMP #$0a                ; pc = 0xc00c
   LDA #$02                ; pc = 0xc00e
   STA absolute_value_2    ; pc = 0xc011
   LDX #$00                ; pc = 0xc013
   INX                     ; pc = 0xc014
   LDA #$00
   CLC
   ADC $0100,X
   CMP #$02
   BRK ; Abort execution

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
