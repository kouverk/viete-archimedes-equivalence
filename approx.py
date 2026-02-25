"""
Approximate pi using Viète's formula:
  pi ~ 2 * (2/sqrt(2)) * (2/sqrt(2+sqrt(2))) * (2/sqrt(2+sqrt(2+sqrt(2)))) * ...

Convergence metric: correct decimal places = -log10(|approx - pi|)
  This is more informative than percent error — it tells you exactly how many
  digits of pi you've nailed. Python's math.pi is a float64, so the hard ceiling
  is ~15.65 correct decimal places (52-bit mantissa → log10(2^52) ≈ 15.65).
"""
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

PI = math.pi
FLOAT64_DIGIT_LIMIT = math.log10(2**52)  # ≈ 15.65

dem = math.sqrt(2)
approx = 2 * (2 / dem)

iterations = []
approximations = []
correct_digits_list = []

for i in range(100):
    dem = math.sqrt(2 + dem)
    approx *= 2 / dem

    error = abs(approx - PI)
    correct_digits = -math.log10(error) if error > 0 else FLOAT64_DIGIT_LIMIT

    iterations.append(i)
    approximations.append(approx)
    correct_digits_list.append(correct_digits)

    print(f"iter {i:3d}:  {approx:.16f}   correct digits: {correct_digits:.2f}   abs error: {error:.2e}")

# --- Plotting ---
ZOOM = 30  # iterations where all the action happens

BLACK      = "#000000"
HOT_PINK   = "#FF2D78"
ELECTRIC   = "#00F5FF"
GOLD       = "#FFD700"
WHITE      = "#FFFFFF"
GRID_GRAY  = "#333333"

plt.rcParams.update({
    "figure.facecolor":  BLACK,
    "axes.facecolor":    BLACK,
    "axes.edgecolor":    WHITE,
    "axes.labelcolor":   WHITE,
    "xtick.color":       WHITE,
    "ytick.color":       WHITE,
    "text.color":        WHITE,
    "legend.facecolor":  "#111111",
    "legend.edgecolor":  WHITE,
    "grid.color":        GRID_GRAY,
})

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
fig.patch.set_facecolor(BLACK)
fig.suptitle("Viète's Formula — Pi Approximation Convergence", fontsize=14, fontweight="bold", color=WHITE)

# --- Left: approximation value converging to pi ---
ax1.plot(iterations[:ZOOM], approximations[:ZOOM], color=HOT_PINK, marker="o", markersize=4,
         linewidth=2, label="Viète approximation")
ax1.axhline(y=PI, color=GOLD, linestyle="--", linewidth=1.5, label=f"π ≈ {PI:.10f}…")
ax1.set_xlabel("Iteration")
ax1.set_ylabel("Value")
ax1.set_title("Approximation Converging to π", color=WHITE)
ax1.legend()
ax1.grid(True, alpha=0.4)

# --- Right: correct decimal places per iteration ---
ax2.plot(iterations[:ZOOM], correct_digits_list[:ZOOM], color=ELECTRIC, marker="o", markersize=4,
         linewidth=2, label="Correct decimal places")
ax2.axhline(
    y=FLOAT64_DIGIT_LIMIT,
    color=GOLD,
    linestyle="--",
    linewidth=1.2,
    label=f"float64 ceiling ≈ {FLOAT64_DIGIT_LIMIT:.1f} digits",
)
ax2.set_xlabel("Iteration")
ax2.set_ylabel("Correct Decimal Places")
ax2.set_title("Convergence Rate: Decimal Places of Accuracy", color=WHITE)
ax2.yaxis.set_major_locator(ticker.MultipleLocator(1))
ax2.grid(True, alpha=0.4)
ax2.legend()

plt.tight_layout()
plt.savefig("pi_convergence.png", dpi=150, bbox_inches="tight", facecolor=BLACK)
print("\nPlot saved to pi_convergence.png")
plt.show()
