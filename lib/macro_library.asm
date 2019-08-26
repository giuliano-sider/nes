
; macro internal variables (removing this breaks asm6f because of some bug)
_i = 0

; Copy [src_addr, src_addr + byte_count) to [dest_addr, dest_addr + byte_count).
; The ranges must not overlap.
; Clobbers A.
.MACRO UnrolledMemcpy dest_addr, src_addr, byte_count
    .IF (byte_count) > 256
        .ERROR "Are you sure you want to use an UnrolledMemcpy with more than 256 LDA/STA pairs expanded inline?"
    .ENDIF
    _i=0
    .REPT (byte_count)
        LDA (src_addr) + _i
        STA (dest_addr) + _i
        _i=_i+1
    .ENDR
.ENDM

; Copy [src_addr, src_addr + byte_count) 
; in the CPU address space to 
; [dest_addr, dest_addr + byte_count)
; in the PPU address space,
; 1 <= byte_count <= 256.
; Clobbers A, X, Y.
.MACRO PpuMemcpy dest_addr, src_addr, byte_count
    .IF (byte_count) < 1 || (byte_count) > 256
        .ERROR "PpuMemcpy: byte_count should be in the [1, 256] range"
    .ENDIF
    LDA #>(dest_addr) ; PPUADDR takes most significant byte first
    STA PPUADDR
    LDA #<(dest_addr)
    STA PPUADDR
    LDX #0
    LDY #((byte_count)%256) ; y = number of remaining bytes to copy (note that the y = 256 == 0 (mod 256) case still works)
    @CopyLoop:
        LDA src_addr, X
        STA PPUDATA
        INX
        DEY
        BNE @CopyLoop
.ENDM

; Fill [dest_addr, dest_addr + byte_count) in the PPU address space
; with the byte given by fill_value,
; 1 <= byte_count <= 256.
; Clobbers A, Y.
.MACRO PpuMemset dest_addr, fill_value, byte_count
    .IF (byte_count) < 1 || (byte_count) > 256
        .ERROR "PpuMemset: byte_count should be in the [1, 256] range"
    .ENDIF
    LDA #>(dest_addr) ; PPUADDR takes most significant byte first
    STA PPUADDR
    LDA #<(dest_addr)
    STA PPUADDR
    LDY #((byte_count)%256) ; y = number of remaining bytes to fill (note that the y = 256 == 0 (mod 256) case still works)
    LDA #(fill_value)
    @FillLoop:
        STA PPUDATA
        DEY
        BNE @FillLoop
.ENDM

; Fill [dest_addr, dest_addr + byte_count) in the CPU address space
; with the byte given by fill_value,
; 1 <= byte_count <= 256.
; Clobbers A, X, Y.
.MACRO Memset dest_addr, fill_value, byte_count
    .IF (byte_count) < 1 || (byte_count) > 256
        .ERROR "Memset: byte_count should be in the [1, 256] range"
    .ENDIF
    LDX #0
    LDY #((byte_count)%256) ; y = number of remaining bytes to fill (note that the y = 256 == 0 (mod 256) case still works)
    LDA #(fill_value)
    @FillLoop:
        STA dest_addr, X
        INX
        DEY
        BNE @FillLoop
.ENDM

; Copy [src_addr, src_addr + byte_count) 
; in the CPU address space to 
; [dest_addr, dest_addr + byte_count)
; in the CPU address space,
; 1 <= byte_count <= 256.
; The memory regions should not overlap.
; Clobbers A, X, Y.
.MACRO Memcpy dest_addr, src_addr, byte_count
    .IF (byte_count) < 1 || (byte_count) > 256
        .ERROR "MEMCPY: byte_count should be in the [1, 256] range"
    .ENDIF
    .IF (dest_addr) <= (src_addr) && (src_addr) < (dest_addr) + (byte_count) ||
        (src_addr) <= (dest_addr) && (dest_addr) < (src_addr) + (byte_count)
        .ERROR "MEMCPY: The regions starting at dest_addr and src_addr must not overlap"
    .ENDIF
    LDX #0
    LDY #((byte_count)%256) ; y = number of remaining bytes to copy (note that the y = 256 == 0 case still works)
    @CopyLoop:
        LDA src_addr, X
        STA dest_addr, X
        INX
        DEY
        BNE @CopyLoop
.ENDM

; Stores 8 IsButtonPressed flags in the byte stored at result_addr, where the bits are:
; 7 6 5      4     3  2    1    0
; A B Select Start Up Down Left Right
.MACRO PollJoypad_1 result_addr
    ; strobe joypad 1 to begin the read process
    LDA #1
    STA JOYPAD_1
    LDA #0
    STA JOYPAD_1
    STA result_addr ; result = 0

    LDA JOYPAD_1 ; read A
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read B
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Select
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Start
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Up
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Down
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Left
    LSR A
    ROL result_addr
    LDA JOYPAD_1 ; read Right
    LSR A
    ROL result_addr
.ENDM

.MACRO HandleControllerInput joypad_keypress_flags, A_handler, B_handler, Select_handler, Start_handler, Up_handler, Down_handler, Left_handler, Right_handler

    @Check_A:
        LDA #JOYPAD_A_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_B
        JSR A_handler
    @Check_B:
        LDA #JOYPAD_B_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Select
        JSR B_handler
    @Check_Select:
        LDA #JOYPAD_SELECT_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Start
        JSR Select_handler
    @Check_Start:
        LDA #JOYPAD_START_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Up
        JSR Start_handler
    @Check_Up:
        LDA #JOYPAD_UP_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Down
        JSR Up_handler
    @Check_Down:
        LDA #JOYPAD_DOWN_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Left
        JSR Down_handler
    @Check_Left:
        LDA #JOYPAD_LEFT_PRESSED
        BIT joypad_keypress_flags
        BEQ @Check_Right
        JSR Left_handler
    @Check_Right:
        LDA #JOYPAD_RIGHT_PRESSED
        BIT joypad_keypress_flags
        BEQ @DoneChecking
        JSR Right_handler
    @DoneChecking:
.ENDM
