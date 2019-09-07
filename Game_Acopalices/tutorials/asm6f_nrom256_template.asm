; This is a fully functional template for an NROM-256 NES cartridge game using asm6f
; syntax. To prove that it works, it paints the screen blue using the PPUMASK 
; emphasis bits and then does nothing, forever.

; Note that the file iNES output file size for this NROM-256 cartridge is
; 16 + 16384*NUM_PRG_ROM_BANKS + 8192*NUM_CHR_ROM_BANKS
; since the iNES header is 16 bytes long.

; ------------------------------------------------------------------------------
; Constants
; ------------------------------------------------------------------------------

; iNES header constants:

; Number of 16KiB PRG ROM banks to use. Since we don't use bank switching in this
; template, you must specify only 1 or 2 banks. 3 is right out. 1 or 2 is the number of
; banks thou shalt specify, and the number of the banking shall be 1 or 2. :)
NUM_PRG_ROM_BANKS = 2

; Number of 8KiB CHR ROM banks to use.
NUM_CHR_ROM_BANKS = 1

; Use horizontal nametable mirroring, in which [$2000, $2400) == [$2800, $2C00)
; and [$2400, $2800) == [$2C00, $3000) in the PPU address space.
HORIZONTAL_MIRRORING = %0000

; Use vertical nametable mirroring, in which [$2000, $2800) == [$2800, $3000)
; in the PPU address space.
VERTICAL_MIRRORING = %0001

; The NROM mapper is the simplest one that could possibly work :)
NROM_MAPPER = 0

; Registers:

PPUCTRL = $2000
PPUMASK = $2001
PPUSTATUS = $2002

APU_FRAME_COUNTER = $4017
APU_FRAME_IRQ_DISABLE = %01000000

DMC_0 = $4010

; ------------------------------------------------------------------------------


; ------------------------------------------------------------------------------
; iNES header
; ------------------------------------------------------------------------------
.INESPRG NUM_PRG_ROM_BANKS 

.INESCHR NUM_CHR_ROM_BANKS

.INESMAP NROM_MAPPER

.INESMIR VERTICAL_MIRRORING 
; ------------------------------------------------------------------------------


;----------------------------------------------------------------
; Variables
;----------------------------------------------------------------

; Zero-page workspace variables
.ENUM $0000 

; TODO: Declare variables using the DSB and DSW directives, like this:

; workspace variables

; my_variable0: .dsb 1
; my_variable1: .dsb 3

; global variables

.ENDE

; Stack page
.ENUM $0100 
; TODO: (optionally) Declare variables for background tile attributes to be copied to 
; the nametable/attribute table during Vblank using "pop slide".
.ENDE

; OAM DMA transfer page
.ENUM $0200 
; TODO: Declare variables for sprite tile attributes to be copied to OAM during Vblank.
.ENDE

; Rest of RAM: [$0300, $0800)
.ENUM $0300
; TODO: Declare additional variables.
.ENDE

;----------------------------------------------------------------


;----------------------------------------------------------------
; PRG ROM (program bank(s))
;----------------------------------------------------------------

.BASE $10000 - (NUM_PRG_ROM_BANKS*$4000)

; Wait for the PPU to become ready, set the PPU mask emphasis bits, and then NOP forever.
Reset:

    ; TODO: actual initialization code goes here.

    ; Disable various features:
    SEI ; disable IRQs
    CLD ; disable decimal mode
    LDX #APU_FRAME_IRQ_DISABLE
    STX APU_FRAME_COUNTER
    LDX #0
    STX PPUCTRL ; disable Vblank NMI
    STX PPUMASK ; disable PPU rendering
    STX DMC_0 ; disable DMC IRQs
    
    ; Set up stack
    DECX ; X = $FF
    TXS

; TODO: consider not polling the Vblank flag, and using the Vblank NMI instead. 
; Because of a race condition, it doesn't look like polling the Vblank flag is a 
; good idea at all. Actually it might be a very bad idea.
    ; First wait for Vblank to make sure PPU is ready.
    @VBlankWait1:
        BIT PPUSTATUS 
        BPL @VBlankWait1 ; poll the Vblank flag

    ; TODO: determine what the point of this is.
    INX ; X = 0
    @ClearMemory:
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
        BNE @ClearMemory

    ; Second wait for Vblank; PPU should be ready after this.
    @VBlankWait2:
        BIT PPUSTATUS
        BPL @VBlankWait2 ; poll the Vblank flag

    ; TODO: the takahirox js emulator is painting red instead of blue. 
    ; they have rgb instead of bgr in PPUSTATUS
    ; mednafen paints blue correctly. report this bug on github.
    LDA #%10000000 ; emphasize blue 
    STA PPUMASK

    @NopForever:
        JMP @NopForever

NMI:

    ; TODO: NMI code goes here.
    RTI

IRQ:

    ; TODO: IRQ code goes here.
    RTI

;----------------------------------------------------------------


;----------------------------------------------------------------
; Interrupt vector
;----------------------------------------------------------------

.ORG $FFFA

.DW NMI
.DW Reset
.DW IRQ

;----------------------------------------------------------------


;----------------------------------------------------------------
; CHR-ROM bank(s)
;----------------------------------------------------------------

; TODO: specify the tiles manually using byte/word directives or include an external
; binary file (perhaps the output of a tile editor).
; .INCBIN "tiles.chr"
.DSB (NUM_CHR_ROM_BANKS*8192), 0 ; Pattern tables on the CHR ROM are all zero.