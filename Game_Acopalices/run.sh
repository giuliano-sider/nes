GAME=${1:-game.asm}
asm6f -L "$GAME" game.bin && mednafen game.bin
