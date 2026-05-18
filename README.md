
# Leslie Effect 

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
python3 leslie.py dry/input.wav wet/output_fast.wav --rate 6 --center-delay 5 --depth 2
python3 leslie.py dry/input.wav wet/output_slow.wav --rate 1.2 --center-delay 5 --depth 2
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

Place the dry sample in `dry/`, then write the processed file to `wet/`.

## Example Audio

Dry input sample:

[dry/test_chord.wav](dry/test_chord.wav)

Processed Leslie output:

[wet/test_chord_leslie.wav](wet/test_chord_leslie.wav)

## Files

- `leslie.py`: runnable Leslie effect implementation.
- `dry/`: dry input samples.
- `wet/`: processed wet output samples.
