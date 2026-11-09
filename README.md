# Lab 2 — Discrete Fourier Transform (DFT)

Course: "Mathematical foundations of digital signal processing", variant n = 17.

- **Part I** — DFT of a random vector of N = 10 + 17 = 27 values, amplitude/phase spectra,
  execution time and number of operations.
- **Part II** — 8 samples from 96 + 17 = 113 in binary (8th digit = 1, odd variant),
  DFT coefficients and the reconstructed analog signal s(t).
- **Part III** — inverse DFT, recovered samples s(nT).

## Run

```
pip install -r requirements.txt
python main.py
```

Console output is in `output.txt`, plots are saved as `part1_spectrum.png`,
`part2_signal.png`, `part2_spectrum.png`.
