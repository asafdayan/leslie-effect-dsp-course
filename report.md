# Leslie / Rotary Loudspeaker Effect

## What the Effect Does

The Leslie effect, also called the rotary loudspeaker effect, simulates the
sound of a loudspeaker cabinet whose horn rotates while playing. The result is
a lively moving sound: the signal seems to swirl across the stereo image, while
its loudness and pitch change periodically. At moderate rotation speeds the
effect adds motion and depth, especially to organ-like sustained sounds. At
higher speeds it becomes more dramatic, with a clear tremolo-like amplitude
variation and a vibrato-like Doppler shimmer.

The effect is strongly associated with electric organs, but it can also be used
on guitar, voice, synthesizers, and other sustained sounds. The important
audible ingredients are not only a left-right stereo movement, but also small
periodic pitch and intensity changes. These changes make the sound feel as if
it is physically moving relative to the listener.

Artistically, the Leslie speaker became important because it made electric
organs sound less static and more expressive, closer in spirit to the moving
air and spatial depth of a pipe organ. In the 1960s musicians also began using
it as a studio effect beyond organ sounds. The Beatles, for example, used
Leslie processing on guitar and vocals, including George Harrison's guitar
parts.

## How the Effect Works

The implementation follows the rotary loudspeaker model described in DAFX,
Section 3.4.3. A Leslie cabinet can be approximated by two opposite rotating
horns. As the horn moves toward the listener, the perceived pitch is slightly
raised and the level increases. As it moves away, the perceived pitch is lowered
and the level decreases. The opposite horn performs the complementary motion,
so the two horn signals are modulated with a phase difference of $180^\circ$.

The pitch variation is implemented with a modulated delay line. This follows
the same principle as vibrato: if the delay changes over time, the spacing
between output samples is locally compressed or expanded, which produces a
Doppler-like frequency change. DAFX Chapter 2 describes fractional delay lines
and vibrato using a low-frequency oscillator to control the delay time. Since
the desired delay is not generally an integer number of samples, this
implementation uses linear interpolation between neighboring samples.

The signal flow used in this implementation is:
![](pictures/Pasted%20image%2020260518220246.png)

Let the low-frequency oscillator be

$$
m[n]=\sin\left( 2\pi f_{\mathrm{rot}}\frac{n}{f_{s}} \right)
$$

where $f_{\mathrm{rot}}$ is the rotation frequency and $f_{s}$ is the sampling frequency. The
two opposite horn delays are

$$
\begin{aligned}
D_{A}[n]&=D_{0}+\Delta D\cdot m[n] \\
D_{B}[n]&=D_{0}-\Delta D\cdot m[n]
\end{aligned}
$$

where $D_{0}$ is the center delay and $\Delta D$ is the delay modulation depth, both
measured in samples. The two horn signals are read from the input using these
time-varying fractional delays:

$$
\begin{aligned}
h_{A}[n]&=x\left[n-D_{A}[n]\right] \\
h_{B}[n]&=x\left[n-D_{B}[n]\right]
\end{aligned}
$$

To model the directional loudness change of the rotating horn, the delayed
signals are amplitude modulated synchronously:

$$
\begin{aligned}
a_{A}[n]&=1+\alpha\cdot m[n] \\
a_{B}[n]&=1-\alpha\cdot m[n]
\end{aligned}
$$

The modulated horn signals are then

$$
\begin{aligned}
s_{A}[n]&=a_{A}[n]\cdot h_{A}[n] \\
s_{B}[n]&=a_{B}[n]\cdot h_{B}[n]
\end{aligned}
$$

Finally, the output is made stereo using unequal mixing of the two horn signals,
similar to the DAFX block diagram:

$$
\begin{aligned}
y_{L}[n]&=s_{A}[n]+\beta\cdot s_{B}[n] \\
y_{R}[n]&=\beta\cdot s_{A}[n]+s_{B}[n]
\end{aligned}
$$

The parameter $\beta$ controls the amount of cross-mixing between the two horns.
When $\beta$ is less than one, the left and right channels receive different
combinations of the rotating horn signals, so the listener perceives spatial
motion.

The key parameters are the rotation frequency $f_{\mathrm{rot}}$, the center
delay $D_{0}$, the delay modulation depth $\Delta D$, the amplitude modulation
depth $\alpha$, and the stereo cross-mix coefficient $\beta$.

The complete signal flow is therefore as follows. First, the input signal is
sent into two delay lines, representing the two opposite horns of the rotating
speaker. The two delay lines are controlled by sinusoidal signals with a
$180^\circ$ phase difference. This time-varying delay creates the Doppler-like
pitch modulation: when a horn moves toward the listener, the effective delay is
changing in a way that raises the perceived pitch; when it moves away, the
perceived pitch is lowered. Second, the outputs of the delay lines are
amplitude modulated using the same low-frequency oscillator. This models the
directional intensity change of the rotating horn. The horn moving toward the
listener has increasing amplitude, while the horn moving away has decreasing
amplitude. Third, the two processed horn signals are mixed unequally into the
left and right output channels. This unequal mixing is what turns the pitch and
amplitude modulation into a stereo rotary-speaker impression.

## Implementation Choices

The program is written in Python using NumPy and SciPy. It accepts an input WAV
file and writes a stereo processed WAV file:

```bash
python3 leslie.py dry/input.wav wet/output_leslie.wav
```

The default settings are chosen to make the effect clear on a short
demonstration sample:

- rotation rate: $6\ \mathrm{Hz}$
- center delay: $5\ \mathrm{ms}$
- delay depth: $2\ \mathrm{ms}$
- amplitude depth: $0.55$
- stereo cross-mix: $0.7$

The code is sample-rate independent: millisecond parameters are converted to
samples using the input file's sampling rate. The input is summed to mono before
processing, because the model represents one source being played through a
virtual rotating cabinet. The output is stereo. After processing, the signal is
normalized if necessary to avoid clipping.

A more detailed Leslie model could split the signal into high-frequency horn and low-frequency drum bands, use separate rotation speeds, add acceleration between slow and fast modes, or model cabinet coloration and room reflections. Here, the main goal is to demonstrate the core DSP ideas from
DAFX: delay-line modulation, amplitude modulation, opposite-phase horn motion,
and stereo mixing.

## References

U. Zolzer, ed., *DAFX: Digital Audio Effects*, 2nd edition. See Section 3.4.3
for the rotary loudspeaker effect, and Chapter 2 for fractional delay lines and
vibrato based on modulated delay.
