
BRK = 0x00

def brk(cpu, logger):
    if not cpu.is_test_mode:
        raise NotImplementedError()
    else:
        cpu.set_break()
        logger.printLog(cpu.PC, cpu.A, cpu.X, cpu.Y, cpu.SP, cpu.P)

handlers = {
    BRK: brk
}