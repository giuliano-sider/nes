
def printLog(regPC, regA, regX, regY, regSP,  regP):
	print("| pc = 0x%04x | a = 0x%04x  | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %s |" % (regPC 
	,regA, regX, regY, regSP, format(14, regP)))

def printLogs(regPC, regA, regX, regY, regSP,  regP, memAddr, data):
	print("| pc = 0x%04x | a = 0x%04x  | x = 0x%04x | y = 0x%04x | sp = 0x%04x | p[NV-BDIZC] = %d | MEM[0x%04x] = 0x%04x |" % (regPC 
	,regA, regX, regY, regSP, regP, memAddr, data))

printLog(1,1,1,1,0xFFC,'08b');
