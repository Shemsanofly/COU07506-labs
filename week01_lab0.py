"""COU07506 Week 01 / Lab 0: signals and audio.

SHEMSA NASSOR AMIN | 240242454734 | BEng24COE | Group 16
Standalone version of the notebook's Python computations.

Run: python week01_lab0.py
Show plot windows: python week01_lab0.py --show
Outputs are saved in outputs/ beside this script. An optional my_voice.wav
in the same directory replaces the manual's fallback test tone.
AI assistance and verification are documented in the accompanying notebook.
"""
import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--show', action='store_true', help='Display plot windows.')
    args = parser.parse_args()
    base_dir = Path(__file__).resolve().parent

    import matplotlib
    if not args.show:
        matplotlib.use('Agg')

    # Task 1.1 - Elementary sequences

    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.io import wavfile

    plt.rcParams['figure.figsize'] = (9, 3.5)
    output_dir = base_dir / 'outputs'
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
    if args.show:
        plt.show()
    else:
        plt.close(fig)

    assert delta.sum() == 1 and delta[n == 0].item() == 1
    assert np.all(step[n < 0] == 0) and np.all(step[n >= 0] == 1)
    assert ramp[n == 10].item() == 10
    assert np.isclose(expo[n == 1].item(), 0.8)
    print('Known-value checks passed for all four sequences.')

    # Task 1.2 - Changing the parameters

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
    if args.show:
        plt.show()
    else:
        plt.close(fig)

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
    if args.show:
        plt.show()
    else:
        plt.close(fig)

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

    # Task 1.3 - Working with audio

    def mono_normalize(raw):
        raw = np.asarray(raw)
        if raw.ndim not in (1, 2) or raw.size == 0:
            raise ValueError('Expected a nonempty mono or multichannel WAV.')
        mono = raw.astype(np.float64)
        if raw.dtype == np.uint8:
            mono -= 128.0
        if mono.ndim == 2:
            mono = mono.mean(axis=1)
        if not np.all(np.isfinite(mono)):
            raise ValueError('The WAV contains nonfinite sample values.')
        peak = np.max(np.abs(mono))
        return mono / peak if peak > 0 else mono


    fname = base_dir / 'my_voice.wav'
    using_recording = fname.is_file()
    if using_recording:
        fs, raw = wavfile.read(fname)
        x = mono_normalize(raw)
        audio_source = f'Phone/user WAV: {fname.name}'
    else:
        fs = 16000
        t_fallback = np.arange(0, 2, 1 / fs)
        x = 0.5 * np.sin(2 * np.pi * 440 * t_fallback) * np.exp(-t_fallback)
        audio_source = 'Synthetic fallback: 440 Hz decaying sine (not a voice recording)'

    t = np.arange(len(x)) / fs
    duration = len(x) / fs
    print(audio_source)
    print(f'fs = {fs} Hz, duration = {duration:.2f} s, samples = {len(x)}')
    print(f'Peak absolute amplitude = {np.max(np.abs(x)):.6f}')
    if using_recording and not 3 <= duration <= 5:
        print('The supplied recording is outside the requested 3-5 second range.')

    fig, ax = plt.subplots(figsize=(10, 3.8))
    ax.plot(t, x, linewidth=0.6)
    ax.set_xlabel('Time (s)')
    ax.set_ylabel('Amplitude (relative full scale)')
    ax.set_title('My voice recording' if using_recording else 'Fallback: 440 Hz decaying sine')
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(output_dir / 'task_1_3_audio.png', dpi=160)
    if args.show:
        plt.show()
    else:
        plt.close(fig)

    # The WAV saved below can be played in any audio player.

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

    # Known-answer checks for normalization and the permitted fallback.
    assert np.array_equal(mono_normalize(np.zeros(8, dtype=np.int16)), np.zeros(8))
    assert np.array_equal(mono_normalize(np.array([128, 128], dtype=np.uint8)), [0, 0])
    assert np.allclose(mono_normalize(np.array([-32768, 0, 32767], dtype=np.int16)),
                       [-1, 0, 32767 / 32768])
    assert np.array_equal(mono_normalize(np.array([[1000, -1000]], dtype=np.int16)), [0])
    if not using_recording:
        assert fs == 16000 and len(x) == 32000 and duration == 2.0
        peak_bin = np.argmax(np.abs(np.fft.rfft(x)))
        measured_frequency = np.fft.rfftfreq(len(x), d=1 / fs)[peak_bin]
        assert np.isclose(measured_frequency, 440.0)
        print(f'Fallback frequency check: FFT peak = {measured_frequency:.1f} Hz.')
    print('Audio normalization and WAV read/write checks passed.')

    # Analysis question 1 - Storage for one minute of mono audio

    one_minute_samples = 60 * int(fs)
    one_minute_pcm_bytes = 2 * one_minute_samples
    print(f'Audio source: {audio_source}')
    print(f'Sampling rate: {fs:,} Hz')
    print(f'One minute in mono: {one_minute_samples:,} sample values')
    print(f'At 16-bit PCM: {one_minute_pcm_bytes:,} bytes of sample data (without WAV header)')


if __name__ == "__main__":
    main()
