#!/usr/bin/env python3
"""
Generate CSV for MTurk user study (new) - pairwise video comparisons.

Methods: f2v, f2v_sl, demofusion, dynamicscaler, wan_md
Frescos: 00030143, 00061004, 00071379, 00181317, 00231100
Comparisons: only pairs involving f2v or f2v_sl (no inter-baseline comparisons)
Questions: animation quality, fresco-style fidelity
"""

import csv
import random
from itertools import combinations

# Configuration
METHODS = ["f2v", "f2v_sl", "demofusion", "dynamicscaler", "wan_md"]
OUR_METHODS = {"f2v", "f2v_sl"}
FRESCOS = ["00030143", "00061004", "00071379", "00181317", "00231100"]

QUESTIONS = [
    "Which video provides the most convincing animation of the input image, with appropriate and perceptible motion?",
    "Which video most closely resembles a fresco artwork that has been smoothly and naturally animated?",
]

GITHUB_USERNAME = "Caselles"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/fresco2video-study/main/videos2/"


def generate_csv(output_file="user_study_new.csv", seed=42):
    """Generate the MTurk CSV with randomized A/B ordering."""
    random.seed(seed)

    rows = []

    # Only pairs where at least one method is ours (f2v or f2v_sl)
    method_pairs = [
        (a, b) for a, b in combinations(METHODS, 2)
        if a in OUR_METHODS or b in OUR_METHODS
    ]

    print(f"Comparison pairs ({len(method_pairs)}):")
    for a, b in method_pairs:
        print(f"  {a} vs {b}")
    print()

    for fresco in FRESCOS:
        for method_a, method_b in method_pairs:
            # Randomize which method is shown as A vs B
            if random.random() < 0.5:
                method_a, method_b = method_b, method_a

            video_a_url = f"{BASE_URL}{method_a}_{fresco}.mp4"
            video_b_url = f"{BASE_URL}{method_b}_{fresco}.mp4"

            for question in QUESTIONS:
                rows.append({
                    "question": question,
                    "prompt": f"Fresco {fresco}",
                    "video_input_url": "",
                    "video_a_url": video_a_url,
                    "video_b_url": video_b_url,
                    "method_a": method_a,
                    "method_b": method_b,
                    "fresco": fresco,
                })

    # Shuffle all rows
    random.shuffle(rows)

    # Write full CSV (with tracking columns for analysis)
    with open(output_file, "w", newline="") as f:
        fieldnames = ["question", "prompt", "video_input_url", "video_a_url", "video_b_url",
                      "method_a", "method_b", "fresco"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows in {output_file}")

    # Write clean MTurk CSV
    mturk_file = output_file.replace(".csv", "_mturk.csv")
    with open(mturk_file, "w", newline="") as f:
        fieldnames = ["question", "prompt", "video_input_url", "video_a_url", "video_b_url"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({k: row[k] for k in fieldnames})
    print(f"Generated MTurk-ready file: {mturk_file}")


if __name__ == "__main__":
    generate_csv()
