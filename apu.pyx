import sys

class Pulse:

    def __init__(self):
        self.duty_cycle = 0
        self.enable_length_counter = 0
        self.is_volume_constant = 0
        self.volume = 0
        self.is_ramp_control_flag_enabled = 0
        self.sweep_divider_period = 0
        self.negate_ramp_flag = 0
        self.shift_count = 0
        self.low_8_bits_timer = 0
        self.high_3_bits_timer = 0
        self.length_counter = 0


class Apu:

    def __init__(self):
        self.pulse_1 = Pulse()
        self.pulse_2 = Pulse()


    def write_p1_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p1_sweep_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p1_low_bits_timer(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p1_hi_bits_timer(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_p2_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p2_sweep_control(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p2_low_bits_timer(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

    def write_p2_hi_bits_timer(self, value):
        print('Warning: not implemented yet', file=sys.stderr)


    def write_triangle_wave_linear_counter(self, value):
        print('Warning: not implemented yet', file=sys.stderr)

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
