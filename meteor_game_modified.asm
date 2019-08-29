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
NES_BLUE = $01
NES_DARK_BLUE = $02
NES_RED = $05
NES_BROWN = $16
NES_GREEN = $1A
NES_YELLOW = $28
NES_LIME_GREEN = $29
NES_WHITE = $30
NES_BLACK = $0D


; Game parameters


; initial position
MAIN_CHARACTER_X_0 = 256/2
MAIN_CHARACTER_Y_0 = 240/2

; pixel increment per frame when the directional buttons are pressed
MAIN_CHARACTER_DELTA_X = 1
MAIN_CHARACTER_DELTA_Y = 1

; limits of main character movement
MAIN_CHARACTER_MIN_X = 10
MAIN_CHARACTER_MAX_X = 245 - MAIN_CHARACTER_X_LENGTH
MAIN_CHARACTER_MIN_Y = 10
MAIN_CHARACTER_MAX_Y = 230 - MAIN_CHARACTER_Y_LENGTH

MAIN_CHARACTER_MAX_LIFE = 8
MAIN_CHARACTER_INITIAL_LIFE = MAIN_CHARACTER_MAX_LIFE


; TODO: consider varying this by difficulty level.
FRAMES_PER_FLYING_OBJECT_SPAWNED = 30

; Spawn sequence contains 5 * 2048 = 10KiB of static data 
; generated by the code in meteor_generator.ipynb,
; which should be enough for a long play sequence until it wraps around.
NUM_FLYING_OBJECTS_IN_SPAWN_SEQUENCE =  2048

STATIC_FLYING_OBJECT_DATA_ADDR = $C000

; Keep in mind that only 64 sprites can be displayed on screen.
MAX_METEORS_ON_SCREEN = 8

MAX_POWERUPS_ON_SCREEN = 4

MAX_FLYING_OBJECTS_ON_SCREEN = MAX_METEORS_ON_SCREEN + MAX_POWERUPS_ON_SCREEN

SIZEOF_FLYING_OBJECT = 5
SIZEOF_FLYING_OBJECTS_ON_SCREEN = SIZEOF_FLYING_OBJECT * MAX_FLYING_OBJECTS_ON_SCREEN

; typedef enum flying_object_type {
;     METEOR = 0,
;     POWERUP = 1,
;     NONE = 0xFF
; } FlyingObjectType;

IS_METEOR = 0
IS_POWERUP = 1
NONE = $FF

; typedef struct flying_object {
;     uint8_t x;
;     uint8_t y;
;     int8_t delta_x;
;     int8_t delta_y;
;     FlyingObjectType type;
; } FlyingObject;


; upper left corner of lifebar
LIFEBAR_X_COORD = 16
LIFEBAR_Y_COORD = 16

LIFEBAR_NAMETABLE_ADDR = (NAMETABLE_0 + $20 * (LIFEBAR_Y_COORD / 8) + (LIFEBAR_X_COORD / 8))


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

    ; workspace/scratch variables and static frames

    WriteSprite_param_x:
        .DSB 1
    WriteSprite_param_y:
        .DSB 1
    WriteSprite_param_tile_info_addr:
        .DSW 1
    WriteSprite_non_const_param_write_offset:
        .DSB 1
    WriteSprite_local_var_i:
        .DSB 1
    WriteSprite_local_var_j:
        .DSB 1
    WriteSprite_local_var_x:
        .DSB 1
    WriteSprite_local_var_y:
        .DSB 1
    WriteSprite_local_var_num_tiles_x:
        .DSB 1
    WriteSprite_local_var_num_tiles_y:
        .DSB 1

    ; global variables

    ; produced by NMI joypad polling code, consumed by UpdateGameState.
    ; 7 6 5      4     3  2    1    0
    ; A B Select Start Up Down Left Right
    joypad_1_keypress_flags:
        .DSB 1

    ; cleared after reset and after UpdateGameState finishes its work. 
    ; Main waits for NMI frame handler to set it again.
    time_to_update_game_state:
        .DSB 1

    ; cleared after NMI frame handler finishes its work.
    ; NMI will not run again until Main finishes its work by setting it.
    time_to_render:
        .DSB 1 

    ; game model variables

    main_character_x:
        .DSB 1
    main_character_y:
        .DSB 1

    main_character_life:
        .DSB 1

    num_meteors_on_screen:
        .DSB 1
    num_powerups_on_screen:
        .DSB 1
    ; num_flying_objects_on_screen = num_meteors_on_screen + num_powerups_on_screen
    num_flying_objects_on_screen:
        .DSB 1

    flying_objects_on_screen:
        .DSB SIZEOF_FLYING_OBJECTS_ON_SCREEN

    ; points to the next flying object in the spawn sequence
    next_flying_object_addr:
        .DSW 1

    frames_until_next_flying_object_spawn:
        .DSB 1

    .IF $ >= $0100
        .ERROR "Too many variables packed into page zero"
    .ENDIF
.ENDE

; Stack page
.ENUM $0100 

.ENDE

; OAM DMA transfer page: sprite attributes to be copied to OAM during Vblank.
; produced by PopulateShadowOAMWithSpriteData, consumed by NMI frame handler.
.ENUM $0200
OAM_DMA_TransferPage:
    ; y - 1, tile index, sprite attribute flags, x - 1
    main_character_sprite_attributes:
        .DSB NUM_MAIN_CHARACTER_TILES * 4

    flying_object_sprite_attributes:
        ; y - 1, tile index, sprite attribute flags, x - 1
        .DSB (NUM_POWERUP_TILES*MAX_POWERUPS_ON_SCREEN + NUM_METEOR_TILES*MAX_METEORS_ON_SCREEN) * 4
    
    .IF $ >= $0300
        .ERROR "sprite attributes must fit on page 2 for DMA transfer to OAM"
    .ENDIF
.ENDE

; Rest of RAM: [$0300, $0800)
.ENUM $0300

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

    JSR InitGameState

    WaitForPpuToStabilizeAfterReset

    ; fill all the palettes
    PpuMemcpy BACKGROUND_PALETTE_0, InitialPaletteData, 32

    ; Load background tile in nametables 
    ; and plain background palette in attribute tables
    
    PpuMemset NAMETABLE_0 + 0*256, PLAIN_BACKGROUND_PATTERN_TABLE_INDEX, 256
    PpuMemset NAMETABLE_0 + 1*256, PLAIN_BACKGROUND_PATTERN_TABLE_INDEX, 256
    PpuMemset NAMETABLE_0 + 2*256, PLAIN_BACKGROUND_PATTERN_TABLE_INDEX, 256
    PpuMemset NAMETABLE_0 + 3*256, PLAIN_BACKGROUND_PATTERN_TABLE_INDEX, 192
    PpuMemset ATTRIBUTE_TABLE_0, PLAIN_BACKGROUND_PALETTE_INDEX, 64

    ; fill OAM DMA transfer page with invisible sprites for now and transfer to OAM.
    
    Memset OAM_DMA_TransferPage, $FF, 256
    TransferPageToOamSpriteMemory OAM_DMA_TransferPage

    ; begin rendering by setting the registers

    LDA PPUSTATUS ; clear Vblank flag
    LDA #(ENABLE_VBLANK_NMI)
    STA PPUCTRL
    LDA #(ENABLE_SPRITE_RENDERING | ENABLE_BACKGROUND_RENDERING)
    STA PPUMASK

    LDA #1
    STA time_to_render ; Reset's work is finished: NMI frame renderer may now proceed.

Main:
    
    LDA time_to_update_game_state
    BEQ Main ; while (time_to_update_game_state == false), Main has nothing to do.

    JSR UpdateGameState

    LDA #1
    STA time_to_render ; Main's work is finished: NMI frame renderer may now proceed.
    
    JMP Main

InitGameState:
    SaveRegisters

    LDA #(MAIN_CHARACTER_X_0)
    STA main_character_x

    LDA #(MAIN_CHARACTER_Y_0)
    STA main_character_y

    LDA #(MAIN_CHARACTER_INITIAL_LIFE)
    STA main_character_life

    LDA #0
    STA num_meteors_on_screen
    STA num_powerups_on_screen
    STA num_flying_objects_on_screen

    Memset flying_objects_on_screen, NONE, SIZEOF_FLYING_OBJECTS_ON_SCREEN

    ; next_flying_object_addr = &FlyingObjectData[0]
    StoreAddress next_flying_object_addr, STATIC_FLYING_OBJECT_DATA_ADDR

    LDA #(FRAMES_PER_FLYING_OBJECT_SPAWNED)
    STA frames_until_next_flying_object_spawn

    LDA #0
    STA time_to_update_game_state

    RestoreRegisters
    RTS

UpdateGameState:
    SaveRegisters

    ; Update main character sprite based on the joypad input
    HandleControllerInput joypad_1_keypress_flags, Handle_A_keypress, Handle_B_keypress, Handle_Select_keypress, Handle_Start_keypress, Handle_Up_keypress, Handle_Down_keypress, Handle_Left_keypress, Handle_Right_keypress

    JSR UpdateFlyingObjects
    JSR CheckCollisions
    JSR PopulateShadowOAMWithSpriteData

    LDA #0
    STA time_to_update_game_state

    RestoreRegisters
    RTS

UpdateFlyingObjects:

    RTS

CheckCollisions:

    RTS

; initializes the "shadow OAM" page based on game state since 
; we don't have time for that during Vblank.
PopulateShadowOAMWithSpriteData:
    SaveRegisters

    ; fill shadow OAM with invisible sprites
    Memset OAM_DMA_TransferPage, $FF, 256

    LDA main_character_x
    STA WriteSprite_param_x
    LDA main_character_y
    STA WriteSprite_param_y
    StoreAddress WriteSprite_param_tile_info_addr, MainCharacterTileInfo
    LDA #0
    STA WriteSprite_non_const_param_write_offset
    JSR WriteSprite ; WriteSprite(main_character_x, main_character_y, MainCharacterTileInfo, &write_addr)

    ; loop over all the flying objects on screen and write them to shadow OAM
    LDY #0 ; flying_object_addr = &flying_objects_on_screen[0]
@ForEachFlyingObjectOnScreen:
    CPY #(SIZEOF_FLYING_OBJECTS_ON_SCREEN)
    BEQ @Done

    ; WriteSprite_non_const_param_write_offset already has the right shadow OAM page offset
    LDA flying_objects_on_screen + 0, y ; load x coord
    STA WriteSprite_param_x
    LDA flying_objects_on_screen + 1, y ; load y coord
    STA WriteSprite_param_y
    LDA flying_objects_on_screen + 4, y ; load type
    CMP #(IS_METEOR)
    BEQ @HandleMeteor
    CMP #(IS_POWERUP)
    BNE @HandleNextObject ; must be NONE in this case
; handle powerup
    StoreAddress WriteSprite_param_tile_info_addr, PowerupTileInfo
    JSR WriteSprite ; WriteSprite(x, y, PowerupTileInfo, &write_addr)
    JMP @HandleNextObject
@HandleMeteor:
    StoreAddress WriteSprite_param_tile_info_addr, MeteorTileInfo
    JSR WriteSprite ; WriteSprite(x, y, MeteorTileInfo, &write_addr)

@HandleNextObject:
    TYA
    CLC
    ADC #(SIZEOF_FLYING_OBJECT)
    TAY ; point to next object
    JMP @ForEachFlyingObjectOnScreen
@Done:
    RestoreRegisters
    RTS

; @param x has the x coordinate of the upper right corner of the sprite to be rendered.
; @param y has they coordinate of the upper right corner of the sprite to be rendered.
; @param tile_info has the address of the TileInfo structure containing the x and y dimensions
; of the sprite, followed by an array of the tile indices that compose it.
; @param write_addr is an output param with the offset of the address where the sprite
; will be written into the shadow OAM page. it is incremented by the number of the 
; bytes written.
; this function uses a static frame for parameters and local variables and is therefore
; not reentrant.
WriteSprite:
    SaveRegisters
    
    LDY #0
    LDA (WriteSprite_param_tile_info_addr), Y ; load num_tiles_x
    STA WriteSprite_local_var_num_tiles_x
    INY
    LDA (WriteSprite_param_tile_info_addr), Y ; load num_tiles_y
    STA WriteSprite_local_var_num_tiles_y
    INY ; offset where the first tile index is stored

    LDA #0
    STA WriteSprite_local_var_i ; i = 0
    STA WriteSprite_local_var_j ; j = 0

    LDA WriteSprite_param_y
    STA WriteSprite_local_var_y
    DEC WriteSprite_local_var_y ; y coordinate of first row of tiles

@ForEachTileRow: ; while (i < num_tiles_y)
    LDA WriteSprite_local_var_i
    CMP WriteSprite_local_var_num_tiles_y
    BEQ @Done

    LDA WriteSprite_param_x
    STA WriteSprite_local_var_x
    DEC WriteSprite_local_var_x ; x coordinate of first tile in row
@ForEachTile: ; while (j < num_tiles_x)
    LDA WriteSprite_local_var_j
    CMP WriteSprite_local_var_num_tiles_x
    BEQ @NextTileRow

    ; write tile in row i, col j of sprite to shadow OAM page
    LDX WriteSprite_non_const_param_write_offset
    LDA WriteSprite_local_var_y
    SEC
    SBC #1
    STA OAM_DMA_TransferPage, X
    INX
    LDA (WriteSprite_param_tile_info_addr), Y
    INY
    STA OAM_DMA_TransferPage, X
    INX
    LDA #(PLAIN_SPRITE_PALETTE_INDEX) ; Attributes: no flip, in foreground
    STA OAM_DMA_TransferPage, X
    INX
    LDA WriteSprite_local_var_x
    SEC 
    SBC #1
    STA OAM_DMA_TransferPage, X
    INX
    STX WriteSprite_non_const_param_write_offset

    LDA #8 ; pixels per tile
    ADC WriteSprite_local_var_x
    STA WriteSprite_local_var_x ; next x coordinate of tile
    INC WriteSprite_local_var_j
    JMP @ForEachTile
@NextTileRow:
    LDA #8 ; pixels per tile
    ADC WriteSprite_local_var_y
    STA WriteSprite_local_var_y ; next y coordinate of tile
    INC WriteSprite_local_var_i
    JMP @ForEachTileRow

@Done:
    RestoreRegisters
    RTS


Handle_A_keypress:
    RTS
Handle_B_keypress:
    RTS
Handle_Select_keypress:
    RTS
Handle_Start_keypress:
    RTS

Handle_Up_keypress:
    SaveRegisters

    Uint8_SubtractWithSaturation main_character_y, #(MAIN_CHARACTER_DELTA_Y), #(MAIN_CHARACTER_MIN_Y)
    STA main_character_y

    RestoreRegisters
    RTS

Handle_Down_keypress:
    SaveRegisters

    Uint8_AddWithSaturation main_character_y, #(MAIN_CHARACTER_DELTA_Y), #(MAIN_CHARACTER_MAX_Y)
    STA main_character_y

    RestoreRegisters
    RTS

Handle_Left_keypress:
    SaveRegisters

    Uint8_SubtractWithSaturation main_character_x, #(MAIN_CHARACTER_DELTA_X), #(MAIN_CHARACTER_MIN_X)
    STA main_character_x

    RestoreRegisters
    RTS

Handle_Right_keypress:
    SaveRegisters

    Uint8_AddWithSaturation main_character_x, #(MAIN_CHARACTER_DELTA_X), #(MAIN_CHARACTER_MAX_X)
    STA main_character_x

    RestoreRegisters
    RTS

; sets background tiles related to the life bar
RenderLifeBar:
    SaveRegisters

    LDA #>LIFEBAR_NAMETABLE_ADDR
    STA PPUADDR
    LDA #<LIFEBAR_NAMETABLE_ADDR
    STA PPUADDR
    LDX #0

    LDA #(REMAINING_LIFEBAR_PATTERN_TABLE_INDEX)
@RenderRemainingLifeBarTile:
    CPX main_character_life
    BEQ @RenderDepletedLifeBarTile
    STA PPUDATA
    INX
    JMP @RenderRemainingLifeBarTile

    LDA #(DEPLETED_LIFEBAR_PATTERN_TABLE_INDEX)
@RenderDepletedLifeBarTile:
    CPX #(MAIN_CHARACTER_MAX_LIFE)
    BEQ @Done
    STA PPUDATA
    INX
    JMP @RenderDepletedLifeBarTile

@Done:
    RestoreRegisters
    RTS

NMI:
    SaveRegisters

    ; TODO: consider putting a frame counter here.

    LDA time_to_render
    BEQ @Done ; if Main hasn't finished working, we must skip this frame / Vblank period.

    LDA #0
    STA time_to_render

    TransferPageToOamSpriteMemory OAM_DMA_TransferPage

    JSR RenderLifeBar

    ; the code up to here must execute during the Vblank period

    ; poll controller and set flags
    PollJoypad_1 joypad_1_keypress_flags

    LDA #1
    STA time_to_update_game_state 

@Done:
    RestoreRegisters
    RTI

IRQ:
    ; TODO: IRQ code goes here.
    RTI


; Static data:

; Palette colors
BG_COLOR = NES_BLACK

; all the tiles are using this palette
UNIVERSAL_PALETTE .EQU BG_COLOR, NES_RED, NES_LIME_GREEN, NES_BLUE

PLAIN_BACKGROUND_PALETTE_INDEX = 0
PLAIN_SPRITE_PALETTE_INDEX = 0

InitialPaletteData:

InitialBackgroundPalettes:
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE

InitialSpritePalettes:
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE
    .DB UNIVERSAL_PALETTE

; sprite pattern table indices

; main character is 3x2 tiles (24x16 pixels)
NUM_MAIN_CHARACTER_X_TILES = 3
MAIN_CHARACTER_X_LENGTH = (NUM_MAIN_CHARACTER_X_TILES * 8)
NUM_MAIN_CHARACTER_Y_TILES = 2
MAIN_CHARACTER_Y_LENGTH = (NUM_MAIN_CHARACTER_Y_TILES * 8)
NUM_MAIN_CHARACTER_TILES = NUM_MAIN_CHARACTER_X_TILES * NUM_MAIN_CHARACTER_Y_TILES
MainCharacterTileInfo:
MainCharacterSpriteDimensions: 
    .DB NUM_MAIN_CHARACTER_X_TILES, NUM_MAIN_CHARACTER_Y_TILES
MainCharacterTileIndices:
    .DB $00, $01, $02
    .DB $10, $11, $12

; meteor is 2x2 tiles (16x16 pixels)
NUM_METEOR_X_TILES = 2
METEOR_X_LENGTH = NUM_METEOR_X_TILES * 8
NUM_METEOR_Y_TILES = 2
METEOR_Y_LENGTH = (NUM_METEOR_Y_TILES * 8)
NUM_METEOR_TILES = NUM_METEOR_X_TILES * NUM_METEOR_Y_TILES
MeteorTileInfo:
MeteorSpriteDimensions:
    .DB NUM_METEOR_X_TILES, NUM_METEOR_Y_TILES
MeteorTileIndices:
    .DB $04, $05
    .DB $14, $15

; powerup is 1x1 tiles (8x8 pixels)
NUM_POWERUP_X_TILES = 1
POWERUP_X_LENGTH = (NUM_POWERUP_X_TILES * 8)
NUM_POWERUP_Y_TILES = 1
POWERUP_Y_LENGTH = (NUM_POWERUP_Y_TILES * 8)
NUM_POWERUP_TILES = NUM_POWERUP_X_TILES * NUM_POWERUP_Y_TILES
PowerupTileInfo:
PowerupSpriteDimensions:
    .DB NUM_POWERUP_X_TILES, NUM_POWERUP_Y_TILES
PowerupTileIndices:
    .DB REMAINING_LIFEBAR_PATTERN_TABLE_INDEX

; background pattern table indices

PLAIN_BACKGROUND_PATTERN_TABLE_INDEX = $FF

REMAINING_LIFEBAR_PATTERN_TABLE_INDEX = $33

DEPLETED_LIFEBAR_PATTERN_TABLE_INDEX = $45


.ORG STATIC_FLYING_OBJECT_DATA_ADDR
FlyingObjectData:
    ; x, y, delta_x, delta_y, flying_object_type
    .INCBIN "data/flying_objects.bin"

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

; generated using https://erikonarheim.com/NES-Sprite-Editor/
    .INCBIN "cockroachGame.chr"

;----------------------------------------------------------------
