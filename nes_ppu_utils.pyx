
PPU_IMAGE_PALETTE_BACKGROUND_OFFSET = 0x4
PPU_IMAGE_PALETTE_GENERAL_OFFSET = 0x20


def is_universal_background_palette(address):
    """Addresses divisible by 4 in the palette area of memory correspond to the universal background palette."""
    return address % 4 == 0
