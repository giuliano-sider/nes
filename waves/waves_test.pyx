from array import array
from time import sleep
from scipy import signal
import numpy as np

import pygame
from pygame.mixer import Sound, get_init, pre_init

class SquareNotes(Sound):

    def __init__(self, frequency, duty=0.5, volume=.1, duration=.1):
        self.frequency = frequency
        self.duty = duty
        self.duration = duration
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        init_frequency = get_init()[0]
        init_size = get_init()[1]
        period = int(round(init_frequency / self.frequency))
        t = np.linspace(0, 1, period, endpoint=False)
        amplitude = 2 ** (abs(init_size) - 1) - 1
        samples = amplitude * signal.square(2 * np.pi * t, duty=self.duty)
        return np.tile(np.array(samples, dtype='int16'), round(self.duration * self.frequency))


class TriangleNotes(Sound):

    def __init__(self, frequency, volume=.1, duration=.1):
        self.frequency = frequency
        self.duration = duration
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        init_frequency = get_init()[0]
        init_size = get_init()[1]
        period = int(round(init_frequency / self.frequency))
        t = np.linspace(0, 1, period, endpoint=False)
        amplitude = 2 ** (abs(init_size) - 1) - 1
        samples = amplitude * signal.sawtooth(2 * np.pi * t, 0.5)
        return np.tile(np.array(samples, dtype='int16'), round(self.duration * self.frequency))

if __name__ == "__main__":
    frequency = 44100
    size = -16
    channels = 1
    buffer = 1024

    pre_init(frequency, size, channels, buffer)
    pygame.init()
    note_1 = SquareNotes(400, duration=0.1)
    note_1.play()
    sleep(1.1)
    note_1.stop()

    note_2 = TriangleNotes(600, duration=0.1, volume=0.2)
    note_2.play()
    sleep(1.1)
    note_2.stop()

