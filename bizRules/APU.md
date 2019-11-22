```
$4000 - $4003 Pulse 1
$4004 - $4007 Pulse 2
$4008 - $400B Triangle
$400C - $400F Noise
$4010 - $4013 DCM
$4015 Channel Enable
```

# APU Rules #

```
nes.apu.pulse1.control
$4000 DDLC VVVV
D : Duty cycle of the pulse wave 00 = 12.5% 01 = 25% 10 = 50% 11 = 75%
L : Length Counter Halt
C : Constant Volume
V : 4-bit volume
```

### ACs ###

#### Duty Cycle ####

```
WHEN address $4000 is written with $(00)(0)(1)(1111)
THEN a bit is played with duty cycle of 12.5%, counter is used, the volume is constant throughout the note and the volume is the loudest possible

```

```
WHEN address $4000 is written with $(01)(0)(1)(1111)
THEN a bit is played with duty cycle of 25%, counter is used, the volume is constant throughout the note and the volume is the loudest possible

```

```
WHEN address $4000 is written with $(10)(0)(1)(1111)
THEN a bit is played with duty cycle of 50%, counter is used, the volume is constant throughout the note and the volume is the loudest possible
```

```
WHEN address $4000 is written with $(11)(0)(1)(1111)
THEN a bit is played with duty cycle of 75%, counter is used, the volume is constant throughout the note and the volume is the loudest possible

```

```
WHEN address $4000 is written with length counter halt set to 0
THEN sound duration is controlled by length counter
```

```
WHEN address $4000 is written with length counter halt set to 0
THEN sound duration is not controlled by length counter
```

## APU Ramp Control ##

```
nes.apu.pulse1.ramp_control
$4001 EPPP NSSS
E : Enabled flag
P : Sweep Divider Period
N : Negate flag, inverts the sweep envelope
S : Shift count
``` 

```
nes.apu.pulse1.ft
$4002 TTTT TTTT
T : Low 8 bits of the timer that controls the frequency
```

```
nes.apu.pulse1.ct
$4003 LLLL LTTT
L : Length counter, if Length Counter Halt is 0, timer for note length
T : High 3 bits of timer that controls frequency
```
