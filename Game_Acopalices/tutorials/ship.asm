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

	SEI          ; disable IRQs
	CLD          ; disable decimal mode
	LDX #$40
	STX $4017    ; disable APU frame IRQ
	LDX #$FF
	TXS          ; Set up stack
	INX          ; now X = 0
	STX $2000    ; disable NMI
	STX $2001    ; disable rendering
	STX $4010    ; disable DMC IRQs

vblankwait1:       ; First wait for vblank to make sure PPU is ready
	BIT $2002
	BPL vblankwait1

clrmem:
	LDA #$00
	STA $0000, x
	STA $0100, x
	STA $0200, x
	STA $0400, x
	STA $0500, x
	STA $0600, x
	STA $0700, x
	LDA #$FE
	STA $0300, x
	INX
	BNE clrmem
   
vblankwait2:      ; Second wait for vblank, PPU is ready after this
	BIT $2002
	BPL vblankwait2


LoadPalettes:
	LDA $2002             ; read PPU status to reset the high/low latch
	LDA #$3F
	STA $2006             ; write the high byte of $3F00 address
	LDA #$00
	STA $2006             ; write the low byte of $3F00 address
	LDX #$00              ; start out at 0
LoadPalettesLoop:
	LDA palette, x        ; load data from address (palette + the value in x)
		                  ; 1st time through loop it will load palette+0
		                  ; 2nd time through loop it will load palette+1
		                  ; 3rd time through loop it will load palette+2
		                  ; etc
	STA $2007             ; write to PPU
	INX                   ; X = X + 1
	CPX #$20              ; Compare X to hex $10, decimal 16 - copying 16 bytes = 4 sprites
	BNE LoadPalettesLoop  ; Branch to LoadPalettesLoop if compare was Not Equal to zero
		                ; if compare was equal to 32, keep going down



LoadSprites:
	LDX #$00              ; start at 0
LoadSpritesLoop:
	LDA sprites, x        ; load data from address (sprites +  x)
	STA $0200, x          ; store into RAM address ($0200 + x)
	INX                   ; X = X + 1
	CPX #$20              ; Compare X to hex $20, decimal 32
	BNE LoadSpritesLoop   ; Branch to LoadSpritesLoop if compare was Not Equal to zero
		                ; if compare was equal to 32, keep going down
		      
		      

	LDA #%10000000   ; enable NMI, sprites from Pattern Table 1
	STA $2000

	LDA #%00010000   ; enable sprites
	STA $2001

Forever:
	JMP Forever     ;jump back to Forever, infinite loop

NMI:

	LDA #$00
	STA $2003       ; set the low byte (00) of the RAM address
	LDA #$02
	STA $4014       ; set the high byte (02) of the RAM address, start the transfer


LatchController:
	LDA #$01
	STA $4016
	LDA #$00
	STA $4016       ; tell both the controllers to latch buttons


ReadA: 
	LDA $4016       ; player 1 - A
	AND #%00000001  ; only look at bit 0
	BEQ ReadADone   ; branch to ReadADone if button is NOT pressed (0)
		          ; add instructions here to do something when button IS pressed (1)

	; sprite 1
	LDA $0200       ; load sprite Y-1 position
	CLC             ; make sure the carry flag is clear
	ADC #$04        ; A = A + 1
	STA $0200       ; save sprite Y-1 position
	
	; sprite 2
	LDA $0204       ; load sprite Y-1 position
	CLC             ; make sure the carry flag is clear
	ADC #$04        ; A = A + 1
	STA $0204       ; save sprite Y-1 position
ReadADone:        ; handling this button is done
  

ReadB: 
	LDA $4016       ; player 1 - B
	AND #%00000001  ; only look at bit 0
	BEQ ReadBDone   ; branch to ReadBDone if button is NOT pressed (0)
		          ; add instructions here to do something when button IS pressed (1)
	
	; sprite 1
	LDA $0200       ; load sprite Y-1 position
	SEC             ; make sure carry flag is set
	SBC #$04        ; A = A - 1
	STA $0200       ; save sprite Y-1 position
	
	; sprite 2
	LDA $0204       ; load sprite 2 Y-1 position
	SEC             ; make sure carry flag is set
	SBC #$04        ; A = A - 1
	STA $0204       ; save sprite 2 Y-1 position
	
ReadBDone:        ; handling this button is done


  
	RTI             ; return from interrupt
 
;;;;;;;;;;;;;;  
  
  
  
	;.bank 1
	.org $E000
palette:
	.db $0F,$31,$32,$33,$34,$35,$36,$37,$38,$39,$3A,$3B,$3C,$3D,$3E,$0F
	.db $0F,$20,$0C,$07,$31,$02,$38,$3C,$0F,$1C,$15,$14,$31,$02,$38,$3C

sprites:
	; big ship
		;vert tile attr horiz
	;.db $6C, $00, $00, $70   ;sprite 0
	;.db $6C, $01, $00, $78   ;sprite 1
	;.db $6C, $02, $00, $80   ;sprite 2
	;.db $6C, $03, $00, $88   ;sprite 3
	;.db $70, $10, $00, $70   ;sprite 4
	;.db $70, $11, $00, $78   ;sprite 5
	;.db $70, $12, $00, $80   ;sprite 6
	;.db $70, $13, $00, $88   ;sprite 7
	;.db $78, $20, $00, $70   ;sprite 8
	;.db $78, $21, $00, $78   ;sprite 9
	;.db $78, $22, $00, $80   ;sprite 10
	;.db $78, $23, $00, $88   ;sprite 11
	
	; little ship
	.db $70, $04, $00, $70   ;sprite 12
	.db $70, $05, $00, $78   ;sprite 13
	

	.org $FFFA     ;first of the three vectors starts here
	.dw NMI        ;when an NMI happens (once per frame if enabled) the 
		           ;processor will jump to the label NMI:
	.dw Reset      ;when the processor first turns on or is reset, it will jump
		           ;to the label RESET:
	.dw 0          ;external interrupt IRQ is not used in this tutorial
  
  
;;;;;;;;;;;;;;  
  
  
	;.bank 2
	;.org $0000
	.incbin "tiles.chr"   ;includes 8KB graphics file from SMB1

IRQ:

	;NOTE: IRQ code goes here

;----------------------------------------------------------------
; interrupt vectors
;----------------------------------------------------------------

   ;.org $fffa

   ;.dw NMI
   ;.dw Reset
   ;.dw IRQ

;----------------------------------------------------------------
; CHR-ROM bank
;----------------------------------------------------------------

   ;.incbin "tiles.chr"
