

def printLog(regPC, regA, regX, regY, regSP,  regP):
	print("| pc = 0x%04x | a = 0x%04x  | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = 10101010 |" % (regPC 
	,regA, regX, regY, regSP ))
	
def printLogs(regPC, regA, regX, regY, regSP,  regP, memAddr, data):
	print("| pc = 0x%04x | a = 0x%04x  | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = 10101010 | MEM[0x%04x] = 0x99 |" % (regPC 
	,regA, regX, regY, regSP ))

printLog(1,1,1,1,0xFFC,0);
