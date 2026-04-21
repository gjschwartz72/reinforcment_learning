
"""
golf_value_iteration.py

A tiny tabular MDP demo for Chapter 3 / 4 intuition:
- states: fairway, rough, near_green, green, hole
- actions: driver, putter
- reward = -1 per stroke until hole (0 thereafter)
- performs value iteration
- prints Bellman backups and greedy policy each iteration
- saves per-iteration values, q-values, and policies to CSV

This is meant as a teaching toy, not a realistic golf simulator.
"""

from __future__ import annotations

import csv
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple


State = str
Action = str
Transition = Tuple[float, State, float]  # (probability, next_state, reward)


@dataclass(frozen=True)
class MDP:
    states: List[State]
    actions: Dict[State, List[Action]]
    transitions: Dict[Tuple[State, Action], List[Transition]]
    gamma: float = 1.0


def build_golf_mdp() -> MDP:
    """
    A small hand-built MDP.

    Intuition:
    - Driver is strong from fairway but risky from rough / near_green.
    - Putter is weak from far away but reliable near the hole.
    - Hole is terminal.
    """
    states = ["fairway", "rough", "near_green", "green", "hole"]

    actions = {
        "fairway": ["driver", "putter"],
        "rough": ["driver", "putter"],
        "near_green": ["driver", "putter"],
        "green": ["putter"],  # keep this simple
        "hole": [],
    }

    transitions: Dict[Tuple[State, Action], List[Transition]] = {
        # From fairway
        ("fairway", "driver"): [
            (0.70, "near_green", -1.0),
            (0.20, "rough", -1.0),
            (0.10, "green", -1.0),
        ],
        ("fairway", "putter"): [
            (0.60, "fairway", -1.0),
            (0.30, "near_green", -1.0),
            (0.10, "green", -1.0),
        ],

        # From rough
        ("rough", "driver"): [
            (0.50, "near_green", -1.0),
            (0.30, "rough", -1.0),
            (0.20, "green", -1.0),
        ],
        ("rough", "putter"): [
            (0.70, "rough", -1.0),
            (0.20, "near_green", -1.0),
            (0.10, "green", -1.0),
        ],

        # From near green
        ("near_green", "driver"): [
            (0.20, "hole", -1.0),
            (0.40, "green", -1.0),
            (0.20, "rough", -1.0),
            (0.20, "near_green", -1.0),
        ],
        ("near_green", "putter"): [
            (0.70, "green", -1.0),
            (0.20, "hole", -1.0),
            (0.10, "near_green", -1.0),
        ],

        # From green
        ("green", "putter"): [
            (0.80, "hole", -1.0),
            (0.20, "green", -1.0),
        ],
    }

    return MDP(states=states, actions=actions, transitions=transitions, gamma=1.0)


def bellman_q(mdp: MDP, state: State, action: Action, v: Dict[State, float]) -> float:
    """
    One-step Bellman optimality backup for q(s,a) given current value function v.
    """
    q = 0.0
    for prob, next_state, reward in mdp.transitions[(state, action)]:
        q += prob * (reward + mdp.gamma * v[next_state])
    return q


def greedy_policy_from_q(mdp: MDP, q_values: Dict[Tuple[State, Action], float]) -> Dict[State, Action]:
    policy: Dict[State, Action] = {}
    for s in mdp.states:
        if not mdp.actions[s]:
            policy[s] = "TERMINAL"
            continue
        policy[s] = max(mdp.actions[s], key=lambda a: q_values[(s, a)])
    return policy


def value_iteration(
    mdp: MDP,
    max_iterations: int = 25,
    tolerance: float = 1e-10,
    output_dir: str | Path = "golf_vi_output",
) -> None:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    value_rows = []
    q_rows = []
    policy_rows = []

    v = {s: 0.0 for s in mdp.states}

    print("=" * 72)
    print("VALUE ITERATION START")
    print("=" * 72)

    for iteration in range(max_iterations):
        q_values: Dict[Tuple[State, Action], float] = {}
        new_v: Dict[State, float] = {}

        print(f"\nIteration {iteration}")
        print("-" * 72)

        for s in mdp.states:
            if not mdp.actions[s]:
                new_v[s] = 0.0
                value_rows.append({
                    "iteration": iteration,
                    "state": s,
                    "value": new_v[s],
                    "delta": 0.0,
                })
                print(f"state={s:12s} terminal -> V({s}) = 0.000000")
                continue

            action_values = []
            for a in mdp.actions[s]:
                q = bellman_q(mdp, s, a, v)
                q_values[(s, a)] = q
                action_values.append((a, q))

                q_rows.append({
                    "iteration": iteration,
                    "state": s,
                    "action": a,
                    "q_value": q,
                })

            best_action, best_value = max(action_values, key=lambda x: x[1])
            new_v[s] = best_value
            delta = new_v[s] - v[s]

            value_rows.append({
                "iteration": iteration,
                "state": s,
                "value": new_v[s],
                "delta": delta,
            })

            action_text = ", ".join([f"Q({s},{a})={q:.6f}" for a, q in action_values])
            print(f"state={s:12s} | {action_text} | V_new={best_value:.6f} via {best_action}")

        policy = greedy_policy_from_q(mdp, q_values)
        for s, a in policy.items():
            policy_rows.append({
                "iteration": iteration,
                "state": s,
                "greedy_action": a,
            })

        print("\nGreedy policy after this iteration:")
        for s in mdp.states:
            print(f"  {s:12s} -> {policy[s]}")

        max_change = max(abs(new_v[s] - v[s]) for s in mdp.states)
        print(f"\nMax value change this iteration: {max_change:.12f}")

        v = new_v

        if max_change < tolerance:
            print("\nConverged.")
            break

    # Save CSVs
    with (output_path / "values_by_iteration.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["iteration", "state", "value", "delta"])
        writer.writeheader()
        writer.writerows(value_rows)

    with (output_path / "qvalues_by_iteration.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["iteration", "state", "action", "q_value"])
        writer.writeheader()
        writer.writerows(q_rows)

    with (output_path / "policy_by_iteration.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["iteration", "state", "greedy_action"])
        writer.writeheader()
        writer.writerows(policy_rows)

    # Save a final summary txt
    final_policy = {}
    final_q = {}
    for s in mdp.states:
        if not mdp.actions[s]:
            final_policy[s] = "TERMINAL"
            continue
        for a in mdp.actions[s]:
            final_q[(s, a)] = bellman_q(mdp, s, a, v)
        final_policy[s] = max(mdp.actions[s], key=lambda a: final_q[(s, a)])

    with (output_path / "final_summary.txt").open("w") as f:
        f.write("Final values:\n")
        for s in mdp.states:
            f.write(f"  V*({s}) = {v[s]:.12f}\n")

        f.write("\nFinal greedy policy:\n")
        for s in mdp.states:
            f.write(f"  {s} -> {final_policy[s]}\n")

        f.write("\nFinal q-values:\n")
        for s in mdp.states:
            for a in mdp.actions[s]:
                f.write(f"  Q*({s},{a}) = {final_q[(s, a)]:.12f}\n")

    print("\n" + "=" * 72)
    print("FINAL VALUES")
    print("=" * 72)
    for s in mdp.states:
        print(f"V*({s:12s}) = {v[s]:.12f}")

    print("\nFINAL GREEDY POLICY")
    print("=" * 72)
    for s in mdp.states:
        print(f"{s:12s} -> {final_policy[s]}")

    print(f"\nSaved outputs to: {output_path.resolve()}")


if __name__ == "__main__":
    mdp = build_golf_mdp()
    value_iteration(mdp)
