#!/usr/bin/env python3
"""
Leslie / rotary loudspeaker effect.
This script implements the DAFX-style rotary speaker model: two opposite
horns are simulated by two 180-degree phase-shifted modulated delay lines.
Synchronous amplitude modulation adds the directional intensity change, and
unequal stereo mixing creates the rotating spatial impression.
"""

import argparse
import os

import numpy as np
from scipy.io import wavfile


def audio_to_float(data):
    """Convert common WAV dtypes to floating point audio in [-1, 1]."""
    if data.dtype.kind == "f":
        return data.astype(np.float64)

    if data.dtype == np.int16:
        return data.astype(np.float64) / 32768.0

    if data.dtype == np.int32:
        return data.astype(np.float64) / 2147483648.0

    if data.dtype == np.uint8:
        return (data.astype(np.float64) - 128.0) / 128.0

    raise TypeError(f"Unsupported WAV dtype: {data.dtype}")


def float_to_int16(data):
    """Convert floating point audio to int16 WAV samples (for output)."""
    clipped = np.clip(data, -1.0, 1.0)
    return np.round(clipped * 32767.0).astype(np.int16)


def mono_sum(data):
    """If the input audio is stereo -> convert it to mono, o.w do nothing"""
    if data.ndim == 1:
        return data
    return np.mean(data, axis=1)


def fractional_variable_delay(x, delay_samples):
    """Apply a time-varying fractional delay using linear interpolation.
    For each output sample n, the signal is read at n - D[n]. 
    at non-integer positions, estimating the value between samples using linear interpolation.
    """
    n = np.arange(len(x), dtype=np.float64)
    read_positions = n - delay_samples
    return np.interp(read_positions, n, x, left=0.0, right=0.0)


def leslie_effect(
    x,
    sample_rate,
    rate_hz=6.0,
    center_delay_ms=5.0,
    depth_ms=2.0,
    amp_depth=0.55,
    cross_mix=0.7,
):
    """checks that the parameters are legal"""
    if rate_hz <= 0:
        raise ValueError("rate_hz must be positive")
    if center_delay_ms <= 0:
        raise ValueError("center_delay_ms must be positive")
    if depth_ms < 0:
        raise ValueError("depth_ms must be non-negative")
    if depth_ms >= center_delay_ms:
        raise ValueError("depth_ms must be smaller than center_delay_ms")
    if not 0.0 <= amp_depth <= 1.0:
        raise ValueError("amp_depth must be between 0 and 1")
    if not 0.0 <= cross_mix <= 1.0:
        raise ValueError("cross_mix must be between 0 and 1")

    x = mono_sum(x)
    n = np.arange(len(x), dtype=np.float64)
    lfo = np.sin(2.0 * np.pi * rate_hz * n / sample_rate) 
    """creates a low freq sine wave"""

    center = center_delay_ms * 1e-3 * sample_rate
    depth = depth_ms * 1e-3 * sample_rate

    # Horn B is opposite horn A, so its delay and level modulation are inverted.
    delay_a = center + depth * lfo
    delay_b = center - depth * lfo
    horn_a = fractional_variable_delay(x, delay_a)
    horn_b = fractional_variable_delay(x, delay_b)

    amp_a = 1.0 - amp_depth * lfo
    amp_b = 1.0 + amp_depth * lfo
    horn_a *= amp_a
    horn_b *= amp_b
    """amplitude modulation"""
    
    left = horn_a + cross_mix * horn_b
    right = cross_mix * horn_a + horn_b
    y = np.column_stack((left, right))

    peak = np.max(np.abs(y))
    if peak > 0.98:
        y = y * (0.98 / peak)
    return y


def parse_args():
    parser = argparse.ArgumentParser(
        description="Apply a Leslie / rotary loudspeaker effect to a WAV file.",
    )
    parser.add_argument("input", help="Input WAV file")
    parser.add_argument("output", help="Output stereo WAV file")
    parser.add_argument("--rate", type=float, default=6.0, help="Rotation rate in Hz")
    parser.add_argument(
        "--center-delay",
        type=float,
        default=5.0,
        help="Center delay in milliseconds",
    )
    parser.add_argument(
        "--depth",
        type=float,
        default=2.0,
        help="Delay modulation depth in milliseconds",
    )
    parser.add_argument(
        "--amp-depth",
        type=float,
        default=0.55,
        help="Amplitude modulation depth from 0 to 1",
    )
    parser.add_argument(
        "--cross-mix",
        type=float,
        default=0.7,
        help="Opposite-horn stereo cross mix from 0 to 1",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    sample_rate, data = wavfile.read(args.input)
    x = audio_to_float(data)
    y = leslie_effect(
        x,
        sample_rate,
        rate_hz=args.rate,
        center_delay_ms=args.center_delay,
        depth_ms=args.depth,
        amp_depth=args.amp_depth,
        cross_mix=args.cross_mix,
    )
    output_dir = os.path.dirname(args.output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    wavfile.write(args.output, sample_rate, float_to_int16(y))
    print(f"Wrote {args.output} ({sample_rate} Hz, stereo)")


if __name__ == "__main__":
    main()
