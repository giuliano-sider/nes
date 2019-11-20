import os
import sys
import unittest

sys.path += os.pardir
from nes_cpu_test_utils import CreateTestCpu, execute_instruction
from Instructions.arithmetics_instructions import *
from cpu cimport Cpu
from apu import Apu, Pulse

class TestArithmetic(unittest.TestCase):

	def test_apu_sets_pulse_1_as_square_wave_pulse(self):
		apu = Apu()

		self.assertIs(type(apu.pulse_1), Pulse)

	def test_if_duty_is_set_to_12p5_when_value_starts_with_0b00(self):
		apu = Apu()
		value = 0b00111111
		apu.write_p1_control(value)

		self.assertEqual(apu.pulse_1.duty_cycle, 12.5)

	def test_if_duty_is_set_to_25_when_value_starts_with_0b01(self):
		apu = Apu()
		value = 0b01111111
		apu.write_p1_control(value)

		self.assertEqual(apu.pulse_1.duty_cycle, 25)

	def test_if_duty_is_set_to_25_when_value_starts_with_0b10(self):
		apu = Apu()
		value = 0b10111111
		apu.write_p1_control(value)

		self.assertEqual(apu.pulse_1.duty_cycle, 50)

	def test_if_duty_is_set_to_25_when_value_starts_with_0b11(self):
		apu = Apu()
		value = 0b11111111
		apu.write_p1_control(value)

		self.assertEqual(apu.pulse_1.duty_cycle, 75)

	def test_if_length_counter_is_enabled_when_value_has_bit_set(self):
		apu = Apu()
		value = 0b00111111
		apu.write_p1_control(value)

		self.assertFalse(apu.pulse_1.enable_length_counter)

	def test_if_length_counter_is_enabled_when_value_has_bit_unset(self):
		apu = Apu()
		value = 0b00011111
		apu.write_p1_control(value)

		self.assertTrue(apu.pulse_1.enable_length_counter)

	def test_if_volume_is_set_to_be_constant_when_bit_is_set(self):
		apu = Apu()
		value = 0b00111111
		apu.write_p1_control(value)

		self.assertTrue(apu.pulse_1.is_volume_constant)

	def test_if_volume_is_set_to_be_constant_when_bit_is_unset(self):
		apu = Apu()
		value = 0b00101111
		apu.write_p1_control(value)

		self.assertFalse(apu.pulse_1.is_volume_constant)

	def test_if_volume_value_is_set_correctly(self):
		apu = Apu()
		value = 0b00101110
		apu.write_p1_control(value)

		self.assertEqual(apu.pulse_1.volume, 14)

if __name__ == '__main__':
	unittest.main()
