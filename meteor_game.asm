; This is a simple game burned to an NROM-256 NES cartridge game using asm6f
; syntax. TODO: what does it do.

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

; PPU

PPUCTRL = $2000
ENABLE_VBLANK_NMI = %10000000
USE_PATTERN_TABLE_1_FOR_SPRITES = %00001000

PPUMASK = $2001
ENABLE_SPRITE_RENDERING = %00010000
ENABLE_BACKGROUND_RENDERING = %00001000

PPUSTATUS = $2002
OAMADDR = $2003
OAMDATA = $2004
PPUSCROLL = $2005
PPUADDR = $2006
PPUDATA = $2007

OAMDMA = $4014


; APU

DMC_0 = $4010

APU_FRAME_COUNTER = $4017
APU_FRAME_IRQ_DISABLE = %01000000

; I/O

JOYPAD_1 = $4016
JOYPAD_2 = $4017

; Bits in the order they are read from the joypad port
JOYPAD_A_PRESSED      = %10000000
JOYPAD_B_PRESSED      = %01000000
JOYPAD_SELECT_PRESSED = %00100000
JOYPAD_START_PRESSED  = %00010000
JOYPAD_UP_PRESSED     = %00001000
JOYPAD_DOWN_PRESSED   = %00000100
JOYPAD_LEFT_PRESSED   = %00000010
JOYPAD_RIGHT_PRESSED  = %00000001


; PPU RAM regions:

PATTERN_TABLE_0 = $0000
PATTERN_TABLE_1 = $1000

NAMETABLE_0 = $2000
ATTRIBUTE_TABLE_0 = $23C0
NAMETABLE_1 = $2400
ATTRIBUTE_TABLE_1 = $27C0
NAMETABLE_2 = $2800
ATTRIBUTE_TABLE_2 = $2BC0
NAMETABLE_3 = $2C00
ATTRIBUTE_TABLE_3 = $2FC0

BACKGROUND_PALETTE_0 = $3F00
BACKGROUND_PALETTE_1 = $3F04
BACKGROUND_PALETTE_2 = $3F08
BACKGROUND_PALETTE_3 = $3F0C
SPRITE_PALETTE_0 = $3F10
SPRITE_PALETTE_1 = $3F14
SPRITE_PALETTE_2 = $3F18
SPRITE_PALETTE_3 = $3F1C


; NES colors

NES_GRAY = $00
NES_BLUE = $02
NES_RED = $05
NES_GREEN = $1A
NES_YELLOW = $28
NES_WHITE = $30
NES_BLACK = $0D


; Game parameters

; initial position
MAIN_CHARACTER_Y_0 = 240/2
MAIN_CHARACTER_X_0 = 256/2

; pixel increment per frame when the directional buttons are pressed
MAIN_CHARACTER_DELTA_Y = 1
MAIN_CHARACTER_DELTA_X = 1
.IF MAIN_CHARACTER_DELTA_X > 128 || MAIN_CHARACTER_DELTA_Y > 128
    .ERROR "Setting the main character step to bigger than 128 will cause overflow"
.ENDIF

MIN_X_COORD = 10
MIN_Y_COORD = 10
MAX_X_COORD = 240
MAX_Y_COORD = 230

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

    ; TODO: Declare variables:

    ; workspace variables

    ; global variables

    joypad_1_keypress_flags: ; written by the NMI polling code
        .DSB 1

.ENDE

; Stack page
.ENUM $0100
    ; TODO: (optionally) Declare variables for background tile attributes to be copied to
    ; the nametable/attribute table during Vblank using "pop slide".
.ENDE

; OAM DMA transfer page: sprite attributes to be copied to OAM during Vblank.
.ENUM $0200
    ; y - 1, tile index, sprite flags, x - 1
    main_character_sprite_y:
        .DSB 1
    main_character_sprite_tile:
        .DSB 1
    main_character_sprite_attributes:
        .DSB 1
    main_character_sprite_x:
        .DSB 1

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

.INCLUDE "lib/macro_library.asm"


Reset:

    ; Disable various features:
    SEI ; disable IRQs
    CLD ; disable decimal mode

    LDX #0
    STX PPUCTRL ; disable Vblank NMI
    STX PPUMASK ; disable PPU rendering
    STX DMC_0 ; disable DMC IRQs

    LDX #APU_FRAME_IRQ_DISABLE
    STX APU_FRAME_COUNTER

    ; Set up stack
    LDX #$FF
    TXS

; NOTE: according to https://wiki.nesdev.com/w/index.php/PPU_power_up_state
; polling the PPUSTATUS in this Reset scenario is safe, and might only
; delay bootup by a few frames.
    BIT PPUSTATUS ; Read PPUSTATUS to clear Vblank flag for safety

    ; First wait for Vblank to make sure PPU is ready.
    @VBlankWait1:        ; do ...
        BIT PPUSTATUS
        BPL @VBlankWait1 ; ... while (PPUSTATUS.IsVblank == false)

    ; Second wait for Vblank; PPU should be ready after this.
    @VBlankWait2:        ; do ...
        BIT PPUSTATUS
        BPL @VBlankWait2 ; ... while (PPUSTATUS.IsVblank == false)

    ; fill palette

    PpuMemcpy BACKGROUND_PALETTE_0, PlainBackgroundPalette, 4
    PpuMemcpy SPRITE_PALETTE_0, MainCharacterRegularPalette, 4

    ; Load background tile in nametables
    ; and plain background palette in attribute tables

    PpuMemset NAMETABLE_0 + 0*256, PLAIN_BACKGROUND_TILE, 256
    PpuMemset NAMETABLE_0 + 1*256, PLAIN_BACKGROUND_TILE, 256
    PpuMemset NAMETABLE_0 + 2*256, PLAIN_BACKGROUND_TILE, 256
    PpuMemset NAMETABLE_0 + 3*256, PLAIN_BACKGROUND_TILE, 192
    PpuMemset ATTRIBUTE_TABLE_0, PLAIN_BACKGROUND_PALETTE, 64

    ; fill OAM DMA transfer page and transfer to OAM

    Memset main_character_sprite_y, MAIN_CHARACTER_Y_0 - 1, 1
    Memset main_character_sprite_tile, MAIN_CHARACTER_TILE, 1
    Memset main_character_sprite_attributes, MAIN_CHARACTER_REGULAR_PALETTE, 1
    Memset main_character_sprite_x, MAIN_CHARACTER_X_0, 1

    Memset $200 + 4, $FF, 256 - 4 ; fill the rest of the OAM with invisible sprites

    LDA #0
    STA OAMADDR
    LDA #$02 ; transfer contents of page 2 to OAM
    STA OAMDMA ; begin transfer to OAM

    ; begin rendering by setting the registers

    LDA PPUSTATUS ; clear Vblank flag
    LDA #(ENABLE_VBLANK_NMI | USE_PATTERN_TABLE_1_FOR_SPRITES)
    STA PPUCTRL
    LDA #(ENABLE_SPRITE_RENDERING | ENABLE_BACKGROUND_RENDERING)
    STA PPUMASK

Main:

    ; TODO: consider updating Sprite OAM here based on input polled from NMI.

WaitForFrameNMI:
    JMP WaitForFrameNMI

Handle_A_keypress:
    RTS
Handle_B_keypress:
    RTS
Handle_Select_keypress:
    RTS
Handle_Start_keypress:
    RTS

Handle_Up_keypress:
    PHP
    PHA
    ; sprite_y -= DELTA_Y
    LDA main_character_sprite_y
    SEC
    SBC #MAIN_CHARACTER_DELTA_Y
    ; if (sprite_y < MIN_Y_COORD) sprite_y += DELTA_Y
    BCC @HitBorder ; in case we went 0
    CMP #MIN_Y_COORD
    BCC @HitBorder ; in case we went under min y coord
    JMP @Done
@HitBorder: ; from this border ye shall not pass
    ADC #MAIN_CHARACTER_DELTA_Y
@Done:
    STA main_character_sprite_y
    PLA
    PLP
    RTS

Handle_Down_keypress:
    PHP
    PHA
    ; sprite_y += DELTA_Y
    LDA main_character_sprite_y
    CLC
    ADC #MAIN_CHARACTER_DELTA_Y
    ; if (sprite_y >= MAX_Y_COORD) sprite_y -= DELTA_Y
    BCS @HitBorder ; in case we went over 255
    CMP #MAX_Y_COORD
    BCS @HitBorder ; in case we reached or went past MAX_Y
    JMP @Done
@HitBorder: ; from this border ye shall not pass
    SBC #MAIN_CHARACTER_DELTA_Y
    JSR Start_Beep
@Done:
    STA main_character_sprite_y
    PLA
    PLP
    RTS

Handle_Left_keypress:
    PHP
    PHA
    ; sprite_x -= DELTA_X
    LDA main_character_sprite_x
    SEC
    SBC #MAIN_CHARACTER_DELTA_X
    ; if (sprite_x < MIN_X_COORD) sprite_x += DELTA_X
    BCC @HitBorder ; in case we went under 0
    CMP #MIN_X_COORD
    BCC @HitBorder ; in case we went under min x
    JMP @Done
@HitBorder: ; from this border ye shall not pass
    ADC #MAIN_CHARACTER_DELTA_X
@Done:
    STA main_character_sprite_x
    PLA
    PLP
    RTS

Handle_Right_keypress:
    PHP
    PHA
    ; sprite_x += DELTA_X
    LDA main_character_sprite_x
    CLC
    ADC #MAIN_CHARACTER_DELTA_X
    ; if (sprite_x >= MAX_X_COORD) sprite_x -= DELTA_X
    BCS @HitBorder ; in case we went over 255
    CMP #MAX_X_COORD
    BCS @HitBorder ; in case we reached or went past MAX_X
    JMP @Done
@HitBorder: ; from this border ye shall not pass
    SBC #MAIN_CHARACTER_DELTA_X
@Done:
    STA main_character_sprite_x
    PLA
    PLP
    RTS

;;;;;;;;;;;;;;;;;;; Beep Engine ;;;;;;;;;;;;;;;;;;;;;;;;;;;;
Start_Beep:
    PHP
    PHA

    LDA #%00000001  ;enable Sq1, Sq2 and Tri channels
    STA $4015
    LDA #%00011000  ;Duty 00, Allow Length Counter, Volume 8 (half volume)
    STA $4000
    LDA #$C9        ;$0C9 is a C# in NTSC mode
    STA $4002       ;low 8 bits of period
    LDA #$20
    STA $4003       ;high 3 bits of period
    LDY #$00
Start_Tick:
    LDX #$00
Resume_Tick:
    INX
    CPX #$ff
    BNE Resume_Tick
Increment_Y:
    INY
    CPY #$10
    BNE Start_Tick
Stop_Beep:
    LDA #%00000000  ;enable Sq1, Sq2 and Tri channels
    STA $4015
    JMP Done_Beep
Done_Beep:
    PLA
    PLP
    RTS
;;;;;;;;;;;;;;;;;;; End Beep Engine ;;;;;;;;;;;;;;;;;;;;;;;;;;;;

NMI:

    ; TODO: NMI code goes here.

    LDA #0
    STA OAMADDR
    LDA #$02 ; OAM DMA transfer page number
    STA OAMDMA ; begin transfer to OAM

    ; poll controller and set flags
    PollJoypad_1 joypad_1_keypress_flags

    ; Update sprite based on the joypad input
    HandleControllerInput joypad_1_keypress_flags, Handle_A_keypress, Handle_B_keypress, Handle_Select_keypress, Handle_Start_keypress, Handle_Up_keypress, Handle_Down_keypress, Handle_Left_keypress, Handle_Right_keypress


    RTI

IRQ:

    ; TODO: IRQ code goes here.
    RTI


; Static data:

; Palette colors
BACKGROUND_COLOR = NES_WHITE

; Palette indices
PLAIN_BACKGROUND_PALETTE = 0
MAIN_CHARACTER_REGULAR_PALETTE = 0

InitialPaletteData:

InitialBackgroundPalettes:
    PlainBackgroundPalette:
        .DSB 4, BACKGROUND_COLOR ; uniform background color

    .DSB 4, BACKGROUND_COLOR ; unused
    .DSB 4, BACKGROUND_COLOR ; unused
    .DSB 4, BACKGROUND_COLOR ; unused

InitialSpritePalettes:
    MainCharacterRegularPalette:
        ;                     eyes,    nose/neck,  mouth
        .DB BACKGROUND_COLOR, NES_RED, NES_YELLOW, NES_GREEN

    .DSB 4, BACKGROUND_COLOR ; unused
    .DSB 4, BACKGROUND_COLOR ; unused
    .DSB 4, BACKGROUND_COLOR ; unused

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
CHR_ROM:
; TODO: specify the tiles manually using byte/word directives or include an external
; binary file (perhaps the output of a tile editor).
; .INCBIN "tiles.chr"

PLAIN_BACKGROUND_TILE = 0
; plane 0
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
; plane 1
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00000000

.PAD (CHR_ROM + 4096), 0

MAIN_CHARACTER_TILE = 0
; Protagonist sprite (test_sprite.xcf)
; plane 0
.DB %00000000
.DB %00100100
.DB %00000000
.DB %00000000
.DB %10000001
.DB %01111110
.DB %00000000
.DB %00000000
; plane 1
.DB %00000000
.DB %00000000
.DB %00000000
.DB %00011000
.DB %10000001
.DB %01111110
.DB %00011000
.DB %00011000

; Everything else is background color.
.PAD (CHR_ROM + NUM_CHR_ROM_BANKS*8192), 0

;----------------------------------------------------------------
