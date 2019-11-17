import unittest
import numpy as np
import scipy.signal

sample_rate = 44100


class TestLoad(unittest.TestCase):

    def test_scipy_wave(self):
        play_for(sine_wave(440, 4096), 1000)
        play_for(square_wave(440, 4096), 1000)

    def sine_wave(hz, peak, n_samples=sample_rate):
        """Compute N samples of a sine wave with given frequency and peak amplitude.
           Defaults to one second.
        """
        length = sample_rate / float(hz)
        omega = numpy.pi * 2 / length
        xvalues = numpy.arange(int(length)) * omega
        onecycle = peak * numpy.sin(xvalues)
        return numpy.resize(onecycle, (n_samples,)).astype(numpy.int16)

    def square_wave(hz, peak, duty_cycle=.5, n_samples=sample_rate):
        """Compute N samples of a sine wave with given frequency and peak amplitude.
           Defaults to one second.
        """
        t = numpy.linspace(0, 1, 500 * 440 / hz, endpoint=False)
        wave = scipy.signal.square(2 * numpy.pi * 5 * t, duty=duty_cycle)
        wave = numpy.resize(wave, (n_samples,))
        return (peak / 2 * wave.astype(numpy.int16)
