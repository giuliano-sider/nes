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

    ZeroPageAddress:
        .dsb 1

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
                                    ; PC = c000, A = 0
    LDA #$AE                        ; PC = c002, A = $AE, N = 1, Z = 0
    STA ZeroPageAddress             ; PC = c004, A = $AE, N = 1, Z = 0, addr = $0000, data = $AE
    LDA #$AF                        ; PC = c006, A = $AF, N = 1, Z = 0
    LDA ZeroPageAddress             ; PC = c008, A = $AE, N = 1, Z = 0, addr = $0000, data = $AE
    BRK

   .org $E000

data_2:
	.db $AE

NMI:

   ;NOTE: NMI code goes here

IRQ:
    JMP IRQ
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
