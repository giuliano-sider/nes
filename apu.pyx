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
TRIANGLE_HI_3_BIT_TIMER_MASL = 0b00000111

class Pulse:

    def __init__(self):
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

class TriangleWave:

    def __init__(self):
        self.enable_length_counter = False
        self.counter_reload_value = 0
        self.timer_low_8_bits = 0
        self.timer_hi_3_bits = 0


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


class Apu():

    natural_boolean_order = [False, True]
    inverted_boolean_order = [True, False]

    duty_values = [12.5, 25, 50, 75]

    length_counter_translation = inverted_boolean_order
    volume_constant_translation = natural_boolean_order
    sweep_flag_translation = natural_boolean_order
    negate_sweep_flag_translation = natural_boolean_order
    triangle_length_counter_translation = natural_boolean_order

    def __init__(self):
        self.pulse_1 = Pulse()
        self.pulse_2 = Pulse()
        self.triangle_wave = TriangleWave()

    def generate_square_note(self, pulse):
        print('Warning: generate_square_note not working yet')

    def write_p1_control(self, value):
        duty_bin = ( value & DUTY_MASK ) >> 6
        length_counter_halt_flag = ( value & LENGTH_COUNTER_HALT_MASK) >> 5
        is_volume_constant_flag = (value & CONSTANT_VOLUME_FLAG_MASK) >> 4
        volume = (value & VOLUME_MASK)

        self.pulse_1.duty_cycle = self.duty_values[duty_bin]
        self.pulse_1.enable_length_counter = self.length_counter_translation[length_counter_halt_flag]
        self.pulse_1.is_volume_constant = self.volume_constant_translation[is_volume_constant_flag]
        self.pulse_1.volume = volume
        self.generate_square_note(self.pulse_1)
    

    def write_p1_sweep_control(self, value):
        sweep_flag_bit = (value & PULSE_SWEEP_FLAG_MASK) >> 7
        negate_sweep_flag_bit = (value & NEGATE_SWEEP_FLAG_MASK) >> 3
        divider_value = ( value & DIVIDER_PERIOD_MASK ) >> 4
        shift_count = value & SWEEP_SHIFT_COUNT_MASK
        self.pulse_1.is_sweep_control_flag_enabled = self.sweep_flag_translation[sweep_flag_bit]
        self.pulse_1.negate_sweep_flag = self.negate_sweep_flag_translation[negate_sweep_flag_bit]
        self.pulse_1.sweep_divider_period = divider_value
        self.pulse_1.shift_count = shift_count

    def write_p1_low_bits_timer(self, value):
        self.pulse_1.low_8_bits_timer = value

    def write_p1_hi_bits_timer(self, value):
        self.pulse_1.high_3_bits_timer = value & HIGHER_BITS_PERIOD_MASK


    def write_p2_control(self, value):
        duty_bin = ( value & DUTY_MASK ) >> 6
        length_counter_halt_flag = ( value & LENGTH_COUNTER_HALT_MASK) >> 5
        is_volume_constant_flag = (value & CONSTANT_VOLUME_FLAG_MASK) >> 4
        volume = (value & VOLUME_MASK)

        self.pulse_2.duty_cycle = self.duty_values[duty_bin]
        self.pulse_2.enable_length_counter = self.length_counter_translation[length_counter_halt_flag]
        self.pulse_2.is_volume_constant = self.volume_constant_translation[is_volume_constant_flag]
        self.pulse_2.volume = volume
        self.generate_square_note(self.pulse_2)

    def write_p2_sweep_control(self, value):
        sweep_flag_bit = (value & PULSE_SWEEP_FLAG_MASK) >> 7
        negate_sweep_flag_bit = (value & NEGATE_SWEEP_FLAG_MASK) >> 3
        divider_value = ( value & DIVIDER_PERIOD_MASK ) >> 4
        shift_count = value & SWEEP_SHIFT_COUNT_MASK
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
        print('Warning: not implemented yet', file=sys.stderr)

    def write_triangle_wave_low_bits_period(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_triangle_wave_hi_bits_period(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_noise_volume_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    # write_dummy

    def write_noise_period_and_waveform_shape(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_noise_length_counter_load_and_envelope_restart(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_dmc_freq(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_raw(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_start(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_dmc_len(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_apu_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_apu_frame_counter(self, value):
        print('Warning: not implemented yet', file=sys.stderr)



    def read_p1_control(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p1_sweep_control(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p1_low_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p1_hi_bits_timer(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0


    def read_p2_control(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

    def read_p2_sweep_control(self):
        print('Warning: not implemented yet', file=sys.stderr)
        return 0

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
