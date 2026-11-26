# COU07506 laboratory work

Week 1 / Lab 0: Setting Up the DSP Laboratory.

SHEMSA NASSOR AMIN | 240242454734 | BEng24COE | Group 16

Open [the Week 1 notebook](COU07506_Week01_240242454734.ipynb) in Jupyter, VS Code, or Google Colab. It includes executed plots, the audio player, pre-lab and analysis answers, two proposed mini-project topics, the repository link, and a ChatGPT (OpenAI) AI-use statement.

The female synthetic voice in [my_voice.wav](my_voice.wav) says **“Hello, I'm Shemsa Amin.”** It uses Microsoft Zira Desktop and is supplied as a 4-second, 48,000 Hz, mono, 16-bit PCM WAV. It is synthesized speech rather than a phone recording of the student. See [voice_source.txt](voice_source.txt). Keep it beside the notebook; upload it to the Colab Files panel before running. `outputs/lab0_processed.wav` contains the processed voice.

One minute at this sampling rate requires 2,880,000 mono sample values or 5,760,000 bytes of 16-bit sample data, excluding the header.

Install and run:

```powershell
python -m pip install -r requirements.txt
python execute_lab0.py
```

`week01_lab0.py` runs the same Python calculations and saves the plots and processed WAV. Add `--show` for plot windows. `build_lab0.py` renders the existing personalized notebook to HTML. Neither silently substitutes the previous 440 Hz fallback tone.

`week01_lab0.m` is the optional Octave/MATLAB Task 1.4 script; it has not been executed in Octave/MATLAB. Student review and instructor checkpoint boxes remain unsigned.

[Download the Week 1 submission ZIP](submission/COU07506_Week01_240242454734_Submission.zip).

Repository: [Shemsanofly/COU07506-labs](https://github.com/Shemsanofly/COU07506-labs).
