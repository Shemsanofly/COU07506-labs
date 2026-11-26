"""COU07506 Week 1: calculations exported from the revised notebook.
Female synthetic voice: Hello, I'm Shemsa Amin. See voice_source.txt.
Run with python week01_lab0.py; add --show to display plot windows.
AI assistance: ChatGPT (OpenAI). Optional Octave script not executed.
"""
import os
import sys
from pathlib import Path
os.chdir(Path(__file__).resolve().parent)
import matplotlib
if '--show' not in sys.argv:
    matplotlib.use('Agg')


import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.io import wavfile
from pathlib import Path
from IPython.display import Audio, display

plt.rcParams['figure.figsize'] = (9, 3.5)
output_dir = Path('outputs')
output_dir.mkdir(exist_ok=True)

n = np.arange(-5, 11)
delta = (n == 0).astype(float)       # 1 only at n = 0
step = (n >= 0).astype(float)        # 1 for every n >= 0
ramp = n * step                     # n for n >= 0, otherwise 0
expo = 0.8**n * step                # causal, decaying exponential

fig, axes = plt.subplots(1, 4, figsize=(14, 3.5))
for ax, x_sequence, title in zip(
    axes,
    [delta, step, ramp, expo],
    [r'Unit impulse: $\delta(n)$', r'Unit step: $u(n)$',
     r'Unit ramp: $n u(n)$', r'Exponential: $(0.8)^n u(n)$'],
):
    ax.stem(n, x_sequence, basefmt='k-')
    ax.set_title(title)
    ax.set_xlabel('Sample index n (samples)')
    ax.set_ylabel('Amplitude (dimensionless)')
    ax.set_xlim(-5.5, 10.5)
    ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / 'task_1_1_sequences.png', dpi=160)
plt.show()

assert delta.sum() == 1 and delta[n == 0].item() == 1
assert np.all(step[n < 0] == 0) and np.all(step[n >= 0] == 1)
assert ramp[n == 10].item() == 10
assert np.isclose(expo[n == 1].item(), 0.8)
print('Known-value checks passed for all four sequences.')

fig, axes = plt.subplots(1, 3, figsize=(12, 3.5))
for ax, a in zip(axes, [0.5, -0.8, 1.1]):
    xa = a**n * step
    ax.stem(n, xa, basefmt='k-')
    ax.set_title(fr'$a^n u(n)$, $a={a}$')
    ax.set_xlabel('Sample index n (samples)')
    ax.set_ylabel('Amplitude (dimensionless)')
    ax.set_xlim(-5.5, 10.5)
    ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / 'task_1_2_exponentials.png', dpi=160)
plt.show()

for a in [0.5, -0.8, 1.1]:
    print(f'a = {a:4.1f}: x(0) = 1, x(1) = {a:.1f}, x(10) = {a**10:.6f}')

n_cos = np.arange(41)
cos8 = np.cos(2 * np.pi * n_cos / 8)
cos75 = np.cos(2 * np.pi * n_cos / 7.5)

fig, axes = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
for ax, values, title in zip(
    axes, [cos8, cos75],
    [r'$\cos(2\pi n/8)$: fundamental period 8 samples',
     r'$\cos(2\pi n/7.5)$: fundamental period 15 samples'],
):
    ax.stem(n_cos, values, basefmt='k-')
    ax.set_title(title)
    ax.set_xlabel('Sample index n (samples)')
    ax.set_ylabel('Amplitude (dimensionless)')
    ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / 'task_1_2_cosines.png', dpi=160)
plt.show()

# Compare all overlapping samples separated by each proposed period.
assert np.allclose(cos8[8:], cos8[:-8], rtol=0, atol=1e-12)
assert np.allclose(cos75[15:], cos75[:-15], rtol=0, atol=1e-12)
assert not np.allclose(cos75[8:], cos75[:-8], rtol=0, atol=1e-12)
for samples, period in [(cos8, 8), (cos75, 15)]:
    assert not any(
        np.allclose(samples[k:], samples[:-k], rtol=0, atol=1e-12)
        for k in range(1, period)
    )
print('Verified fundamental periods: 8 samples and 15 samples.')

def mono_normalize(raw):
    raw = np.asarray(raw)
    values = raw.astype(np.float64)
    if raw.dtype == np.uint8:
        values -= 128
    if values.ndim == 2:
        values = values.mean(axis=1)
    if values.ndim != 1 or not values.size or not np.all(np.isfinite(values)):
        raise ValueError('Expected a nonempty, finite audio signal.')
    peak = np.max(np.abs(values))
    return values / peak if peak else values

fname = Path('my_voice.wav')
if not fname.is_file():
    raise FileNotFoundError('Place the supplied my_voice.wav beside this notebook (upload it in Colab).')
fs, raw = wavfile.read(fname)
x = mono_normalize(raw)
audio_source = "Female synthetic voice: Hello, I'm Shemsa Amin. (Microsoft Zira Desktop)"
t = np.arange(len(x)) / fs
duration = len(x) / fs
assert fs == 48000 and 3 <= duration <= 5
print(audio_source)
print(f'fs = {fs:,} Hz, duration = {duration:.2f} s, samples = {len(x):,}')
fig, ax = plt.subplots(figsize=(10, 3.8))
ax.plot(t, x, linewidth=0.6)
ax.set(title='Female synthetic voice: Shemsa Amin', xlabel='Time (s)', ylabel='Amplitude (relative full scale)')
ax.grid(True, alpha=0.3)
fig.tight_layout()
fig.savefig(output_dir / 'task_1_3_audio.png', dpi=160)
plt.show()
print('Audio saved in outputs/lab0_processed.wav.')

audio_out = output_dir / 'lab0_processed.wav'
pcm = np.rint(np.clip(x, -1, 1) * 32767).astype(np.int16)
wavfile.write(audio_out, fs, pcm)
fs_readback, pcm_readback = wavfile.read(audio_out)
assert fs_readback == fs
assert pcm_readback.shape == x.shape
assert np.array_equal(pcm_readback, pcm)
max_error = np.max(np.abs(x - pcm_readback.astype(float) / 32767))
assert max_error <= 0.5 / 32767 + 1e-12
print(f'Wrote {audio_out}: {fs_readback} Hz, mono, signed 16-bit PCM.')
print(f'Maximum write/read error = {max_error:.8f} (relative amplitude).')


assert np.array_equal(mono_normalize(np.zeros(8, dtype=np.int16)), np.zeros(8))
assert np.array_equal(mono_normalize(np.array([128, 128], dtype=np.uint8)), [0, 0])
assert np.allclose(mono_normalize(np.array([-32768, 0, 32767], dtype=np.int16)), [-1, 0, 32767/32768])
print('Normalization and WAV write/read checks passed.')

one_minute_samples = 60 * int(fs)
one_minute_pcm_bytes = 2 * one_minute_samples
print(f'Audio source: {audio_source}')
print(f'Sampling rate: {fs:,} Hz')
print(f'One minute in mono: {one_minute_samples:,} sample values')
print(f'At 16-bit PCM: {one_minute_pcm_bytes:,} bytes of sample data (without WAV header)')
