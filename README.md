# COU07506 laboratory work

Week 1 / Lab 0 follows printed pages 5-7 (PDF pages 6-8) of
`COU07506_DSP_Laboratory_Manual_2026-27.pdf` supplied in the parent folder.

Open `COU07506_Week01_YOUR_REGNO.ipynb` in Jupyter, VS Code, or Google Colab.
It includes Tasks 1.1-1.5, plots, audio playback, pre-lab examples, analysis
answers, and an AI-use statement. The saved notebook includes executed outputs.

For local use, install `requirements.txt` in a Python 3.11+ environment. This
workspace also has a prepared environment at `../.venv`. Select its Python
interpreter as the notebook kernel, then restart the kernel and run all cells.
The notebook builder can recreate the unexecuted notebook:

```powershell
..\.venv\Scripts\python.exe build_lab0.py
```

To execute all cells and save their outputs again:

```powershell
..\.venv\Scripts\python.exe execute_lab0.py
```

Task 1.3 uses the manual's 2-second, 16 kHz, 440 Hz fallback test signal because
no personal voice recording was supplied. To use your voice, put a 3-5 second
WAV file named `my_voice.wav` beside the notebook (or upload it to Colab's
Files panel) and run all cells. The notebook reads its actual sampling rate,
converts stereo to mono, normalizes safely, plots, plays, and writes audio.
The exported `outputs/lab0_processed.wav` is generated audio, not a voice
recording. Do not rename it to `my_voice.wav`.

`week01_lab0.m` implements optional Task 1.4. Run it in GNU Octave or MATLAB.
No Octave/MATLAB executable was available here, so that script has not been
executed in either application.

Task 1.5 uses the permitted local repository option: this folder is the
`COU07506-labs` Git repository. The notebook is committed locally. No remote
repository or eLMS upload is claimed.

Before submitting:

1. Fill in your name, registration number, class, and group in the title cell.
   Rename the notebook to `COU07506_Week01_<RegNo>.ipynb`.
2. Personalize the pre-lab device examples to devices you actually used.
3. Add your phone recording if required by your instructor; rerun all cells
   and check the updated audio and analysis outputs. The manual permits the
   supplied fallback.
4. Review every cell and complete the student understanding declaration.
5. Show the plots and audio measurements to your instructor for Checkpoint 1.
6. Commit your personalized notebook (`git add` then `git commit`). A web
   repository link can be added if you later push to GitHub/GitLab; currently
   the notebook records the local repository path allowed by Task 1.5.
7. Upload the final notebook to DIT-eLMS yourself; no connected eLMS session
   was available to perform or confirm the upload.
8. Form your group of 3-5 students and post two topics to the eLMS forum. Two
   suggested topics are included in the notebook for discussion.
