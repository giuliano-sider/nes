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
        .dsb 16
    ZeroPageAddressWithOffset:
        .dsb 1

   .ende

   ;NOTE: you can also split the variable declarations into individual pages, like this:

   .enum $0100
   Page1Address:
     .dsb 16
   Page1AddressWithOffset:
     .dsb 1
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
    ; Accumulator addressing mode
    LDA #$AE                        ; PC = c002, A = $AE, N = 1, Z = 0

    ASL A                           ; PC = c003, A = $5C, N = 0, Z = 0, C = 1
    ROL A                           ; PC = c004, A = $B9, N = 1, Z = 0, C = 0
    ROL A                           ; PC = c005, A = $72, N = 0, Z = 0, C = 1
    ROR A                           ; PC = c006, A = $B9, N = 1, Z = 0, C = 0
    LSR A                           ; PC = c007, A = $5C, N = 0, Z = 0, C = 1


    ; Zero page addressing mode
    LDA #$AE                        ; PC = c009, A = $AE, N = 1, Z = 0
    STA ZeroPageAddress             ; PC = c00b                                addr = $0000, data = $AE

    ASL ZeroPageAddress             ; PC = c00c, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $5C
    ROL ZeroPageAddress             ; PC = c00d, A = $AE, N = 1, Z = 0, C = 0, addr = $0000, data = $B9
    ROL ZeroPageAddress             ; PC = c00e, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $72
    ROR ZeroPageAddress             ; PC = c00f, A = $AE, N = 1, Z = 0, C = 0, addr = $0000, data = $B9
    LSR ZeroPageAddress             ; PC = c010, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $5C


    ; Zero page with X offset addressing mode
    LDX #$10                        ; PC = c012, X = $10
    LDA #$AE                        ; PC = c014, A = $AE, N = 1, Z = 0
    STA ZeroPageAddress, X          ; PC = c016                                addr = $0010, data = $AE

    ASL ZeroPageAddress, X          ; PC = c018, A = $AE, N = 0, Z = 0, C = 1, addr = $0010, data = $5C
    ROL ZeroPageAddress, X          ; PC = c01a, A = $AE, N = 1, Z = 0, C = 0, addr = $0010, data = $B9
    ROL ZeroPageAddress, X          ; PC = c01c, A = $AE, N = 0, Z = 0, C = 1, addr = $0010, data = $72
    ROR ZeroPageAddress, X          ; PC = c01e, A = $AE, N = 1, Z = 0, C = 0, addr = $0010, data = $B9
    LSR ZeroPageAddress, X          ; PC = c020, A = $AE, N = 0, Z = 0, C = 1, addr = $0010, data = $5C


    ; Absolute addressing mode
    LDA #$AE                        ; PC = c022, A = $AE, N = 1, Z = 0
    STA Page1Address                ; PC = c025                                addr = $0000, data = $AE

    ASL Page1Address                ; PC = c028, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $5C
    ROL Page1Address                ; PC = c02b, A = $AE, N = 1, Z = 0, C = 0, addr = $0000, data = $B9
    ROL Page1Address                ; PC = c02e, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $72
    ROR Page1Address                ; PC = c031, A = $AE, N = 1, Z = 0, C = 0, addr = $0000, data = $B9
    LSR Page1Address                ; PC = c034, A = $AE, N = 0, Z = 0, C = 1, addr = $0000, data = $5C


    ; Absolute with X offset addressing mode
    LDX #$10                        ; PC = c036, X = $10
    LDA #$AE                        ; PC = c038, A = $AE, N = 1, Z = 0
    STA Page1Address, X             ; PC = c03b                                addr = $0010, data = $AE
    
    ASL Page1Address, X             ; PC = c03e, A = $AE, N = 1, Z = 0, C = 1, addr = $0010, data = $5C
    ROL Page1Address, X             ; PC = c041, A = $AE, N = 1, Z = 0, C = 0, addr = $0010, data = $B9
    ROL Page1Address, X             ; PC = c044, A = $AE, N = 0, Z = 0, C = 1, addr = $0010, data = $72
    ROR Page1Address, X             ; PC = c047, A = $AE, N = 1, Z = 0, C = 0, addr = $0010, data = $B9
    LSR Page1Address, X             ; PC = c04a, A = $AE, N = 0, Z = 0, C = 1, addr = $0010, data = $5C

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
