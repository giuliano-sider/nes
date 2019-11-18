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

        self.write_registers_ = {
            FIRST_PULSE_CONTROL: self.write_p1_control,
            FIRST_PULSE_SWEEP_CONTROL: self.write_p1_sweep_control,
            FIRST_PULSE_LOW_BITS_TIMER: self.write_p1_low_bits_timer,
            FIRST_PULSE_HI_BITS_TIMER: self.write_p1_hi_bits_timer,
            SECOND_PULSE_CONTROL: self.write_p2_control,
            SECOND_PULSE_SWEEP_CONTROL: self.write_p2_sweep_control,
            SECOND_PULSE_LOW_BITS_TIMER: self.write_p2_low_bits_timer,
            SECOND_PULSE_HI_BITS_TIMER: self.write_p2_hi_bits_timer,
            TRIANGLE_WAVE_MUTE_CONTROL: self.write_triangle_wave_mute_control,
            TRIANGLE_WAVE_DUMMY: self.write_dummy,
            TRIANGLE_WAVE_LOW_BITS_PERIOD: self.write_triangle_wave_low_bits_period,
            TRIANGLE_WAVE_HI_BITS_PERIOD: self.write_triangle_wave_hi_bits_period,
            NOISE_VOLUME_CONTROL: self.write_noise_volume_control,
            NOISE_TONE_CONTROL: self.write_noise_tone_control
        }

        self.read_registers_ = {
            FIRST_PULSE_CONTROL: self.read_p1_control,
            FIRST_PULSE_SWEEP_CONTROL: self.read_p1_sweep_control,
            FIRST_PULSE_LOW_BITS_TIMER: self.read_p1_low_bits_timer,
            FIRST_PULSE_HI_BITS_TIMER: self.read_p1_hi_bits_timer,
            SECOND_PULSE_CONTROL: self.read_p1_control,
            SECOND_PULSE_SWEEP_CONTROL: self.read_p2_sweep_control,
            SECOND_PULSE_LOW_BITS_TIMER: self.read_p2_low_bits_timer,
            SECOND_PULSE_HI_BITS_TIMER: self.read_p2_hi_bits_timer,
            TRIANGLE_WAVE_MUTE_CONTROL: self.read_triangle_wave_mute_control,
            TRIANGLE_WAVE_DUMMY: self.read_dummy,
            TRIANGLE_WAVE_LOW_BITS_PERIOD: self.read_triangle_wave_low_bits_period,
            TRIANGLE_WAVE_HI_BITS_PERIOD: self.read_triangle_wave_hi_bits_period,
            NOISE_VOLUME_CONTROL: self.read_noise_volume_control,
            NOISE_TONE_CONTROL: self.read_noise_tone_control
        }

    def write_p1_control(self, value):
        console.log('Warning: not implemented yet')

    def write_p1_sweep_control(self, value):
        console.log('Warning: not implemented yet')

    def write_p1_low_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def write_p1_hi_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def write_p2_control(self, value):
        console.log('Warning: not implemented yet')

    def write_p2_sweep_control(self, value):
        console.log('Warning: not implemented yet')

    def write_p2_low_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def write_p2_hi_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def write_triangle_wave_mute_control(self, value):
        console.log('Warning: not implemented yet')

    def write_dummy(self, value):
        console.log('Warning: not implemented yet')

    def write_triangle_wave_low_bits_period(self, value):
        console.log('Warning: not implemented yet')

    def write_triangle_wave_hi_bits_period(self, value):
        console.log('Warning: not implemented yet')

    def write_noise_volume_control(self, value):
        console.log('Warning: not implemented yet')

    def write_noise_tone_control(self, value):
        console.log('Warning: not implemented yet')

    def read_p1_control(self, value):
        console.log('Warning: not implemented yet')

    def read_p1_sweep_control(self, value):
        console.log('Warning: not implemented yet')

    def read_p1_low_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def read_p1_hi_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def read_p2_control(self, value):
        console.log('Warning: not implemented yet')

    def read_p2_sweep_control(self, value):
        console.log('Warning: not implemented yet')

    def read_p2_low_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def read_p2_hi_bits_timer(self, value):
        console.log('Warning: not implemented yet')

    def read_triangle_wave_mute_control(self, value):
        console.log('Warning: not implemented yet')

    def read_dummy(self, value):
        console.log('Warning: not implemented yet')

    def read_triangle_wave_low_bits_period(self, value):
        console.log('Warning: not implemented yet')

    def read_triangle_wave_hi_bits_period(self, value):
        console.log('Warning: not implemented yet')

    def read_noise_volume_control(self, value):
        console.log('Warning: not implemented yet')

    def read_noise_tone_control(self, value):
        console.log('Warning: not implemented yet')