# PPU Memory map# 

The PPU has its own memory, known as VRAM (Video RAM). Like the CPU, the PPU can
also address 64 KB of memory although it only has 16 KB of physical RAM. The PPU’s
memory map is shown in figure 3-1. Again, the left hand map shows a simplified version
which is elaborated on by the right hand map. Due to the difference between physical and
logical address spaces, any address above $3FFF is wrapped around, making the logical
memory locations $4000-$FFFF effectively a mirror of locations $0000-$3FFF.

![](https://gitlab.ic.unicamp.br/ra145103/mc861-nesproject/blob/ra145103-master-patch-44846/Screen%20Shot%202019-10-16%20at%2023.15.17.png

## ACs ##

### Mirroring ###

```
GIVEN address between $4000 and $FFFF
WHEN I access the content at $4000 + A inside this interval
THEN I get the same content at $0000 + A
```

## I/O ##

PPU memory uses 16-bit addresses but I/O registers are only 8-bit

```
GIVEN 16-bit address to be set to PPU and 8 bit IO registers
WHEN I write the address into $2006
THEN I need to write at $2006 twice (hi an lo bits)
```

```
WHEN I read data from $2007 once
THEN data is buffered
WHEN I read data from $2007 for the second time
THEN data is returned
```

```
GIVEN bit 2 from PPU Control ($2000)
WHEN it is set and I read data from $2007
THEN addess is incremented by 1 (which address?? :/)
```

```
GIVEN bit 2 from PPU Control ($2000)
WHEN it is not set and I read data from $2007
THEN addess is incremented by 32 (which address?? :/)
```

## PPU Registers ## 

```
GIVEN bit 5 from $2000
WHEN it is not set
THEN NES supports 8x8 sprites
```

```
GIVEN bit 5 from $2000
WHEN it is set
THEN NES suports 8x16 sprites
```

```
GIVEN bit 3 from $2001
WHEN it is not set
THEN background is cleared
```

```
GIVEN bit 3 from $2001
WHEN it is set
THEN background is rendered
```

```
GIVEN bit 4 from $2001
WHEN it is not set
THEN sprites are cleared
```

```
GIVEN bit 4 from $2001
WHEN it is set
THEN sprites are rendered
```

```
GIVEN V-Blank is ocurring
THEN PPU sets bit 7 from $2002
```

```
GIVEN bit 4 from $2002
WHEN it is not set
THEN PPU is not willing to accept writes
```

```
GIVEN bit 4 from $2002
WHEN it is set
THEN PPU is willing to accept writes
```

```
WHEN I read $2002
THEN bit 7 from $2002, the content in $2005 and $2006 are set to 0
```

## DMA ## 

```
GIVEN the DMA register ($4014) and address from the CPU memory $10000000 being the first from 256 bytes to be copied
WHEN i write into it with operand $100000
THEN the operand is multiplied by $100, resulting in the given address
```

```
GIVEN the DMA register ($4014) and address from the CPU memory $10000000 being the first from 256 bytes to be copied
WHEN i write into it with operand $100000
THEN 256 bytes are directly written in the sprite memory
```

```
WHEN DMA is occurring 
THEN CPU is prevented from using the memory
```

```
WHEN DMA occurs
THEN it take 512 cycles
```