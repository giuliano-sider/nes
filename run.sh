GAME=${1:-game.asm}
asm6f "$GAME" game.bin && mednafen game.bin
