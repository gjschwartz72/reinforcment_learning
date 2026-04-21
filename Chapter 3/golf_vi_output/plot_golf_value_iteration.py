
"""
plot_golf_value_iteration.py

Reads CSV outputs from golf_value_iteration.py and makes a few simple plots.
"""

from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

OUTPUT_DIR = Path("golf_vi_output")

values = pd.read_csv(OUTPUT_DIR / "values_by_iteration.csv")
qvalues = pd.read_csv(OUTPUT_DIR / "qvalues_by_iteration.csv")
policy = pd.read_csv(OUTPUT_DIR / "policy_by_iteration.csv")

# Plot values by state over iterations
for state in values["state"].unique():
    subset = values[values["state"] == state]
    plt.figure()
    plt.plot(subset["iteration"], subset["value"], marker="o")
    plt.xlabel("Iteration")
    plt.ylabel("Value")
    plt.title(f"Value Iteration: V({state}) over iterations")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"value_{state}.png")
    plt.close()

# Plot q-values by state-action over iterations
for state in qvalues["state"].unique():
    subset = qvalues[qvalues["state"] == state]
    plt.figure()
    for action in subset["action"].unique():
        sa = subset[subset["action"] == action]
        plt.plot(sa["iteration"], sa["q_value"], marker="o", label=action)
    plt.xlabel("Iteration")
    plt.ylabel("Q-value")
    plt.title(f"Value Iteration: Q({state}, a) over iterations")
    plt.legend()
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / f"qvalues_{state}.png")
    plt.close()

print(f"Plots saved into {OUTPUT_DIR.resolve()}")
