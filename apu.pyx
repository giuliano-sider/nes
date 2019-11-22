import sys
from scipy import signal
import numpy as np
# from pygame.mixer import Sound, get_init, pre_init

import contextlib
with contextlib.redirect_stdout(None):
    import pygame
    from pygame.mixer import Sound, get_init, pre_init


DUTY_MASK = 0b11000000
LENGTH_COUNTER_HALT_MASK = 0b00100000
CONSTANT_VOLUME_FLAG_MASK = 0b00010000
VOLUME_MASK = 0b00001111
HIGHER_BITS_PERIOD_MASK = 0b00000111
PULSE_SWEEP_FLAG_MASK = 0b10000000
DIVIDER_PERIOD_MASK = 0b01110000
NEGATE_SWEEP_FLAG_MASK = 0b00001000
SWEEP_SHIFT_COUNT_MASK = 0b00000111
TRIANGLE_LENGTH_COUNTER_FLAG_MASK = 0b10000000
TRIANGLE_COUNTER_RELOAD_MASK = 0b01111111
TRIANGLE_HI_3_BIT_TIMER_MASK = 0b00000111
TRIANGLE_LENGTH_COUNTER_VALUE_MASK = 0b11111000
NOISE_LENGTH_COUNTER_HALT_FLAG_MASK = 0b00100000
NOISE_CONSTANT_VOLUME_FLAG_MASK = 0b00010000
NOISE_VOLUME_MASK = 0b00001111
NOISE_MODE_FLAG_MASK = 0b10000000
NOISE_PERIOD_MASK = 0b00001111
NOISE_LENGTH_COUNTER_LOAD_MASK = 0b11111000

APU_CONTROL_PULSE_1_MASK = 0b00000001
APU_CONTROL_PULSE_2_MASK = 0b00000010
APU_CONTROL_TRIANGLE_MASK = 0b00000100
APU_CONTROL_NOISE_MASK = 0b00001000
APU_CONTROL_DMC_MASK = 0b00010000

NTSC_CPU_FREQUENCY = 1789773.0

def createPyGameForTesting():
    frequency = 44100
    size = -16
    channels = 1
    buffer = 1024

    pre_init(frequency, size, channels, buffer)
    pygame.init()
    return pygame

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


class ApuControlRegister():

    def __init__(self):
        self.is_pulse_1_enabled = False
        self.is_pulse_2_enabled = False
        self.is_triangle_notes_enabled = False
        self.is_noise_enabled = False


class Apu():

    natural_boolean_order = [False, True]
    inverted_boolean_order = [True, False]

    duty_values = [12.5, 25, 50, 75]

    length_counter_translation = inverted_boolean_order
    volume_constant_translation = natural_boolean_order
    sweep_flag_translation = natural_boolean_order
    negate_sweep_flag_translation = natural_boolean_order
    triangle_length_counter_translation = natural_boolean_order
    apu_control_enable_translation = natural_boolean_order

    def __init__(self, squareNote=SquareNote):
        self.control = ApuControlRegister()
        self.pulse_1 = Pulse(squareNote)
        self.pulse_2 = Pulse(squareNote)
        self.triangle_wave = TriangleWave()
        self.noise_wave = NoiseWave()

    def write_p1_control(self, value):
        duty_bin = ( value & DUTY_MASK ) >> 6
        length_counter_halt_flag = ( value & LENGTH_COUNTER_HALT_MASK) >> 5
        is_volume_constant_flag = (value & CONSTANT_VOLUME_FLAG_MASK) >> 4
        volume = (value & VOLUME_MASK)

        self.pulse_1.raw_control_value = value
        self.pulse_1.duty_cycle = self.duty_values[duty_bin]
        self.pulse_1.enable_length_counter = self.length_counter_translation[length_counter_halt_flag]
        self.pulse_1.is_volume_constant = self.volume_constant_translation[is_volume_constant_flag]
        self.pulse_1.volume = volume
    

    def write_p1_sweep_control(self, value):
        sweep_flag_bit = (value & PULSE_SWEEP_FLAG_MASK) >> 7
        negate_sweep_flag_bit = (value & NEGATE_SWEEP_FLAG_MASK) >> 3
        divider_value = ( value & DIVIDER_PERIOD_MASK ) >> 4
        shift_count = value & SWEEP_SHIFT_COUNT_MASK

        self.pulse_1.raw_sweep_control = value
        self.pulse_1.is_sweep_control_flag_enabled = self.sweep_flag_translation[sweep_flag_bit]
        self.pulse_1.negate_sweep_flag = self.negate_sweep_flag_translation[negate_sweep_flag_bit]
        self.pulse_1.sweep_divider_period = divider_value
        self.pulse_1.shift_count = shift_count

    def write_p1_low_bits_timer(self, value):
        self.pulse_1.low_8_bits_timer = value

    def write_p1_hi_bits_timer(self, value):
        self.pulse_1.high_3_bits_timer = value & HIGHER_BITS_PERIOD_MASK
        self.pulse_1.generate_square_note()


    def write_p2_control(self, value):
        duty_bin = ( value & DUTY_MASK ) >> 6
        length_counter_halt_flag = ( value & LENGTH_COUNTER_HALT_MASK) >> 5
        is_volume_constant_flag = (value & CONSTANT_VOLUME_FLAG_MASK) >> 4
        volume = (value & VOLUME_MASK)

        self.pulse_2.raw_control_value = value
        self.pulse_2.duty_cycle = self.duty_values[duty_bin]
        self.pulse_2.enable_length_counter = self.length_counter_translation[length_counter_halt_flag]
        self.pulse_2.is_volume_constant = self.volume_constant_translation[is_volume_constant_flag]
        self.pulse_2.volume = volume
        self.pulse_2.generate_square_note()

    def write_p2_sweep_control(self, value):
        sweep_flag_bit = (value & PULSE_SWEEP_FLAG_MASK) >> 7
        negate_sweep_flag_bit = (value & NEGATE_SWEEP_FLAG_MASK) >> 3
        divider_value = ( value & DIVIDER_PERIOD_MASK ) >> 4
        shift_count = value & SWEEP_SHIFT_COUNT_MASK

        self.pulse_2.raw_sweep_control = value
        self.pulse_2.is_sweep_control_flag_enabled = self.sweep_flag_translation[sweep_flag_bit]
        self.pulse_2.negate_sweep_flag = self.negate_sweep_flag_translation[negate_sweep_flag_bit]
        self.pulse_2.sweep_divider_period = divider_value
        self.pulse_2.shift_count = shift_count


    def write_p2_low_bits_timer(self, value):
        self.pulse_2.low_8_bits_timer = value

    def write_p2_hi_bits_timer(self, value):
        self.pulse_2.high_3_bits_timer = value & HIGHER_BITS_PERIOD_MASK


    def write_triangle_wave_linear_counter(self, value):
        enable_length_counter_bit = ( value & TRIANGLE_LENGTH_COUNTER_FLAG_MASK ) >> 7
        self.triangle_wave.enable_length_counter = self.triangle_length_counter_translation[enable_length_counter_bit]
        self.triangle_wave.counter_reload_value = value & TRIANGLE_COUNTER_RELOAD_MASK

    def write_dummy(self, value):
        pass

    def write_triangle_wave_low_bits_period(self, value):
        self.triangle_wave.timer_low_8_bits = value

    def write_triangle_wave_hi_bits_period(self, value):
        self.triangle_wave.timer_hi_3_bits = value & TRIANGLE_HI_3_BIT_TIMER_MASK
        self.triangle_wave.length_counter_load = ( value & TRIANGLE_LENGTH_COUNTER_VALUE_MASK ) >> 3


    def write_noise_volume_control(self, value):
        enable_length_counter_bit = (value & NOISE_LENGTH_COUNTER_HALT_FLAG_MASK) >> 5
        constant_volume_bit = (value & NOISE_CONSTANT_VOLUME_FLAG_MASK) >> 4
        volume = value & NOISE_VOLUME_MASK

        self.noise_wave.enable_length_counter = self.length_counter_translation[enable_length_counter_bit]
        self.noise_wave.is_volume_constant = self.volume_constant_translation[constant_volume_bit]
        self.noise_wave.volume = volume

    # write_dummy

    def write_noise_period_and_waveform_shape(self, value):
        self.noise_wave.mode_flag = ( value & NOISE_MODE_FLAG_MASK ) >> 7
        self.noise_wave.period = ( value & NOISE_PERIOD_MASK )

    def write_noise_length_counter_load_and_envelope_restart(self, value):
        self.noise_wave.length_counter_load = (value & NOISE_LENGTH_COUNTER_LOAD_MASK) >> 3


    def write_dmc_freq(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_raw(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_start(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_len(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_apu_control(self, value):
        is_pulse_1_enabled_bit = value & APU_CONTROL_PULSE_1_MASK
        is_pulse_2_enabled_bit = value & APU_CONTROL_PULSE_2_MASK >> 1
        is_triangle_notes_enabled_bit = value & APU_CONTROL_TRIANGLE_MASK >> 2
        is_noise_enabled_bit = value & APU_CONTROL_NOISE_MASK >> 3
        is_dmc_enabled_bit = value & APU_CONTROL_DMC_MASK >> 4

        self.control.is_pulse_1_enabled = self.apu_control_enable_translation[is_pulse_1_enabled_bit]
        self.control.is_pulse_2_enabled = self.apu_control_enable_translation[is_pulse_2_enabled_bit]
        self.control.is_triangle_notes_enabled = self.apu_control_enable_translation[is_triangle_notes_enabled_bit]
        self.control.is_noise_enabled = self.apu_control_enable_translation[is_noise_enabled_bit]
        self.control.is_dmc_enabled = self.apu_control_enable_translation[is_dmc_enabled_bit]


    def write_apu_frame_counter(self, value):
        print('Warning: not implemented yet', file=sys.stderr)



    def read_p1_control(self):
        return self.pulse_1.raw_control_value

    def read_p1_sweep_control(self):
        return self.pulse_1.raw_sweep_control

    def read_p1_low_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p1_hi_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0


    def read_p2_control(self):
        return self.pulse_2.raw_control_value

    def read_p2_sweep_control(self):
        return self.pulse_2.raw_sweep_control

    def read_p2_low_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p2_hi_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0


    def read_triangle_wave_linear_counter(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_dummy(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_triangle_wave_low_bits_period(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_triangle_wave_hi_bits_period(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0


    def read_noise_volume_control(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    # read_dummy

    def read_noise_period_and_waveform_shape(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_noise_length_counter_load_and_envelope_restart(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0


    def read_dmc_freq(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_dmc_raw(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_dmc_start(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_dmc_len(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def read_apu_status(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0
