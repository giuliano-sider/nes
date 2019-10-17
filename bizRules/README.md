# Project Title

Development rules for PPU

## Write on PPU

```
WHEN I write in $2000

THEN I can access the content also in the following addresses: [$2000, $2008, ... $3FF8]`
```

```
WHEN I write in $2001
THEN I can access the content also in the following addresses: [$2001, $2009, ... $3ff9]
```

```
WHEN I write in $2002
THEN I can access the content also in the following addresses: [$2002, $200A, ... $3ffA]
```

```
WHEN I write in $2003
THEN I can access the content also in the following addresses: [$2003, $200B, ... $3ffB]
```

```
WHEN I write in $2004
THEN I can access the content also in the following addresses: [$2004, $200C, ... $3ffC]
```

```
WHEN I write in $2005
THEN I can access the content also in the following addresses: [$2005, $200D, ... $3ffD]
```

```
WHEN I write in $2006
THEN I can access the content also in the following addresses: [$2006, $200E, ... $3ffE]
```

```
WHEN I write in $2007
THEN I can access the content also in the following addresses: [$2007, $200F, ... $3ffF]
```

(This feature is apparently done already, but not tested ;) )

## 16-bit shift register behavior

### Context ###

There are 2 register of this type in PPU. These contain the pattern table data for two tiles. 

### ACs ###

```
WHEN 8 cycles of processing happens
THEN the data for the next tile is loaded into the upper 8 bits of this shift register
```

```
WHEN 8 cycles of processing happens
THEN the pixel to render is fetched from one of the lower 8 bits
```

## 8-bit shift register ##

### Context ###

There are 2 register of this type in PPU. These contain the palette attributes for the lower 8 pixels of the 16-bit shift register. These registers are fed by a latch which contains the palette attribute for the next tile

### ACs ###

```
WHEN 8 cycles of processing happens
THEN the latch is loaded with the paletter attribute for the next tile
```

## Paint one tile in background ##

### Context ### 

GIVEN a CHR with one tile stored on 3 column and 2 row of the first section of patter tablr
WHEN I set PPUCTRL ($2000) with 0
THEN I

## Interrupts ##

GIVEN an interrupt request ocurred
THEN I should complete the execution of the current instruction

GIVEN an interrupt request ocurred and current instruction finished
THEN I push the program counter and status register into the stack

GIVEN an interrupt request ocurred and current instruction finished
THEN Interruption should be disabled on the status register

GIVEN an interrupt 
THEN PC should load the respective address from the vector table (this AC needs more details)


