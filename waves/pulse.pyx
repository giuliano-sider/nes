
class Pulse:

    def __init__(self, squareNote):
        self.raw_control_value = 0
        self.raw_sweep_control = 0

        self.duty_cycle = 0
        self.enable_length_counter = False
        self.is_volume_constant = False
        self.volume = 0
        self.is_sweep_control_flag_enabled = False
        self.sweep_divider_period = 0
        self.negate_sweep_flag = False
        self.shift_count = 0
        self.low_8_bits_timer = 0
        self.high_3_bits_timer = 0
        self.length_counter = 0
        self._SquareNote = squareNote

    def generate_square_note(self):
        # generate frequency
        period = (self.high_3_bits_timer << 7) + self.low_8_bits_timer
        frequency_pulse = round(NTSC_CPU_FREQUENCY / (16 * (period + 1) ))
        note = self._SquareNote(frequency_pulse)
        note.play()



class TriangleWave:

    def __init__(self):
        self.enable_length_counter = False
        self.counter_reload_value = 0
        self.timer_low_8_bits = 0
        self.timer_hi_3_bits = 0
        self.length_counter_load = 0

    def generate_trinagle_note(self):
        # generate frequency
        period = (self.high_3_bits_timer << 7) + self.low_8_bits_timer
        frequency_pulse = round(NTSC_CPU_FREQUENCY / (32 * (period + 1)))
        note = self._TriangleNote(frequency_pulse)
        note.play()

class TrianguleNote(Sound):

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

class NoiseWave:

    def __init__(self):
        self.enable_length_counter = False
        self.is_volume_constant = False
        self.volume = 0
        self.mode_flag = 0


class SquareNote(Sound):

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

