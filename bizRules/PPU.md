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

```
```