PPU_IMAGE_PALETTE_BACKGROUND_OFFSET = 0x4
PPU_IMAGE_PALETTE_GENERAL_OFFSET = 0x20


def is_background_palette(address):
    return address % 4 == 0
