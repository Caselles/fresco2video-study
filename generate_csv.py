#!/usr/bin/env python3
"""
Generate CSV for MTurk user study - pairwise video comparisons.

Methods: f2v, wan_md, wan_vsr, demofusion, dynamicscaler
Frescos: 00031686, 00151595, 00361771, 00371667
Questions: overall preference, motion plausibility, fine-detail preservation, global coherence
"""

import csv
import random
from itertools import combinations

# Configuration
METHODS = ["f2v", "wan_md", "wan_vsr", "demofusion", "dynamicscaler"]
FRESCOS = ["00031686", "00151595", "00361771", "00371667"]

QUESTIONS = [
    "Which video do you prefer overall?",
    "Which video exhibits more natural and stable motion?",
    "Which video better preserves fine details and textures over time?",
    "Which video better maintains global visual consistency across the entire fresco?",
]

# GitHub raw URL - REPLACE 'YOUR_GITHUB_USERNAME' with your actual username
# After creating repo 'fresco2video-study' on GitHub
GITHUB_USERNAME = "Caselles"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/fresco2video-study/main/videos/"


def generate_csv(output_file="user_study.csv", seed=42):
    """Generate the MTurk CSV with randomized A/B ordering."""
    random.seed(seed)

    rows = []

    # Generate all pairwise comparisons
    method_pairs = list(combinations(METHODS, 2))

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

    # Write full CSV (with tracking columns for your analysis)
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
