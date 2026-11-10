import cmath
import math
import random
import time

import matplotlib.pyplot as plt

STUDENT_NUMBER = 17

ops = {"mul": 0, "add": 0}

def dft_term(f, k, i):
    N = len(f)
    angle = 2 * math.pi * k * i / N
    a = f[i] * math.cos(angle)
    b = -f[i] * math.sin(angle)
    ops["mul"] += 5
    return a, b


def dft_coefficient(f, k):
    A, B = 0.0, 0.0
    for i in range(len(f)):
        a, b = dft_term(f, k, i)
        A += a
        B += b
        ops["add"] += 2
    return complex(round(A, 10) + 0.0, round(B, 10) + 0.0)


def dft(f):
    return [dft_coefficient(f, k) for k in range(len(f))]


def idft(C):
    N = len(C)
    s = []
    for n in range(N):
        total = 0
        for k in range(N):
            total += C[k] * cmath.exp(2j * math.pi * k * n / N)
        s.append(round((total / N).real, 10) + 0.0)
    return s


def plot_spectrum(C, title, filename):
    k = range(len(C))
    amplitudes = [abs(c) for c in C]
    phases = [cmath.phase(c) for c in C]

    plt.figure(figsize=(12, 4))
    plt.subplot(1, 2, 1)
    plt.stem(k, amplitudes)
    plt.title(f"{title}: amplitude spectrum |C_k|")
    plt.xlabel("k")
    plt.grid(True)

    plt.subplot(1, 2, 2)
    plt.stem(k, phases)
    plt.title(f"{title}: phase spectrum arg C_k")
    plt.xlabel("k")
    plt.ylabel("rad")
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(filename)
    plt.show()


def print_coefficients(C):
    for k, c in enumerate(C):
        print(f"C_{k:<2} = {c.real:9.4f} {c.imag:+9.4f}j   "
              f"|C| = {abs(c):8.4f}   arg = {cmath.phase(c):7.4f} rad")


def part1():
    print("===== PART I =====")
    N = 10 + STUDENT_NUMBER
    random.seed(STUDENT_NUMBER)
    f = [round(random.uniform(-10, 10), 2) for _ in range(N)]
    print(f"N = {N}")
    print(f"f = {f}")

    start = time.perf_counter()
    C = dft(f)
    elapsed = time.perf_counter() - start

    print_coefficients(C)
    print(f"Time: {elapsed * 1000:.3f} ms")
    print(f"Multiplications: {ops['mul']}, additions: {ops['add']}")
    plot_spectrum(C, f"Part I (N={N})", "part1_spectrum.png")


def make_samples(n):
    bits = format(96 + n, "b").zfill(7)
    bits = ("1" if n % 2 else "0") + bits
    return [int(b) for b in bits]


def analog_signal(C, t, T):
    N = len(C)
    s = C[0].real
    for k in range(1, N // 2):
        s += 2 * abs(C[k]) * math.cos(2 * math.pi * k * t / T + cmath.phase(C[k]))
    s += C[N // 2].real * math.cos(math.pi * N * t / T)
    return s / N


def part2():
    print("\n===== PART II =====")
    s = make_samples(STUDENT_NUMBER)
    N = len(s)
    print(f"96 + {STUDENT_NUMBER} = {96 + STUDENT_NUMBER} = {format(96 + STUDENT_NUMBER, 'b')} (bin)")
    print(f"s(nT) = {s}")

    C = dft(s)
    print_coefficients(C)

    print("s(t) = 1/8 * [", end="")
    print(f"{C[0].real:.4f}", end="")
    for k in range(1, N // 2):
        print(f" + {2 * abs(C[k]):.4f}*cos({2 * k}*pi*t/T {cmath.phase(C[k]):+.4f})", end="")
    print(f" + ({C[N // 2].real:.4f})*cos(8*pi*t/T) ]")

    T = 1.0
    t = [i * T / 500 for i in range(501)]
    plt.figure(figsize=(10, 4))
    plt.plot(t, [analog_signal(C, x, T) for x in t], label="s(t)")
    plt.stem([i * T / N for i in range(N)], s, linefmt="r-", markerfmt="ro", label="s(nT)")
    plt.title("Reconstructed analog signal")
    plt.xlabel("t / T")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("part2_signal.png")
    plt.show()

    plot_spectrum(C, "Part II (N=8)", "part2_spectrum.png")
    return C


def part3(C):
    print("\n===== PART III =====")
    s = idft(C)
    for n, value in enumerate(s):
        print(f"s({n}T) = {value:.4f}")

    print("s(0) = 1/8 * (C_0 + C_1 + ... + C_7) = "
          f"1/8 * ({sum(C).real:.4f}) = {sum(C).real / 8:.4f}")
    terms = [C[k] * cmath.exp(1j * math.pi * k / 4) for k in range(8)]
    print("s(1T) = 1/8 * sum C_k * exp(j*pi*k/4) = "
          f"1/8 * ({sum(terms).real:.4f}) = {sum(terms).real / 8:.4f}")


if __name__ == "__main__":
    part1()
    C2 = part2()
    part3(C2)
