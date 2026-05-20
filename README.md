# Leslie Effect Special Assignment

Python implementation of a Leslie / rotary loudspeaker effect for the DSP
special assignment. The implementation follows the DAFX rotary-speaker idea:
two opposite modulated delay lines, synchronous amplitude modulation, and
unequal stereo mixing.

## Requirements

Python 3 with NumPy and SciPy:

```bash
python3 -m pip install numpy scipy
```

## Usage

```bash
python3 leslie.py dry/input.wav wet/output_leslie.wav
```

Useful optional controls:

```bash
python3 leslie.py dry/input.wav wet/output_fast.wav --rate 6.5 --center-delay 6 --depth 3 --amp-depth 0.85 --cross-mix 0.4
python3 leslie.py dry/input.wav wet/output_slow.wav --rate 2 --center-delay 6 --depth 1 --amp-depth 0.35 --cross-mix 0.6
```

## Options

- `input`: input WAV file.
- `output`: output stereo WAV file.
- `--rate`: rotation rate in Hz. Default: `6.0`.
- `--center-delay`: center delay in milliseconds. Default: `5.0`.
- `--depth`: delay modulation depth in milliseconds. Default: `2.0`.
- `--amp-depth`: amplitude modulation depth from `0` to `1`. Default: `0.55`.
- `--cross-mix`: opposite-horn stereo cross mix from `0` to `1`. Default: `0.7`.
- `-h`, `--help`: show the command-line help.

Place dry samples in `dry/`, then write processed files to `wet/`.

## Demo Commands

The submitted demo files were produced with three intentionally different
styles:

```bash
python3 leslie.py dry/casta.wav wet/casta_slow_wide.wav --rate 2.0 --center-delay 6 --depth 1.0 --amp-depth 0.35 --cross-mix 0.6
python3 leslie.py dry/casta.wav wet/casta_classic_fast.wav --rate 6.5 --center-delay 6 --depth 3.0 --amp-depth 0.85 --cross-mix 0.4
python3 leslie.py dry/casta.wav wet/casta_dramatic.wav --rate 8.5 --center-delay 9 --depth 5.0 --amp-depth 0.95 --cross-mix 0.2

python3 leslie.py dry/speechshort.wav wet/speechshort_slow_wide.wav --rate 2.0 --center-delay 6 --depth 1.0 --amp-depth 0.35 --cross-mix 0.6
python3 leslie.py dry/speechshort.wav wet/speechshort_classic_fast.wav --rate 6.5 --center-delay 6 --depth 3.0 --amp-depth 0.85 --cross-mix 0.4
python3 leslie.py dry/speechshort.wav wet/speechshort_dramatic.wav --rate 8.5 --center-delay 9 --depth 5.0 --amp-depth 0.95 --cross-mix 0.2
```

