#!/usr/bin/env python3
"""
Generate CSV for MTurk user study: hi-res videos.

Methods: f2v, f2v_sl, demofusion, dynamicscaler, wan_md
Indices: 001, 014, 018, 025, 038, 040, 043, 044
"""

import csv
import random
from itertools import combinations

METHODS = ["f2v", "f2v_sl", "demofusion", "dynamicscaler", "wan_md"]
OUR_METHODS = {"f2v", "f2v_sl"}
INDICES = ["001", "014", "018", "025", "038", "040", "043", "044"]

QUESTIONS = [
    "Which video provides the most convincing motion animation of the input image, with enough perceptible motion? Reward the quantity of coherent movement. More movement is better, but the movement has to be realistic.",
    "Which video most closely resembles a coherently animated fresco artwork? Reward the abscence of wobblyness.",
]

GITHUB_USERNAME = "Caselles"
BASE_URL = f"https://raw.githubusercontent.com/{GITHUB_USERNAME}/fresco2video-study/main/videos4/"


def generate_csv(output_file="user_study_hires.csv", seed=42):
    random.seed(seed)

    rows = []

    method_pairs = [
        (a, b) for a, b in combinations(METHODS, 2)
        if a in OUR_METHODS or b in OUR_METHODS
    ]

    print(f"Comparison pairs ({len(method_pairs)}):")
    for a, b in method_pairs:
        print(f"  {a} vs {b}")
    print()

    for idx in INDICES:
        for method_a, method_b in method_pairs:
            if random.random() < 0.5:
                method_a, method_b = method_b, method_a

            video_a_url = f"{BASE_URL}{method_a}_{idx}.mp4"
            video_b_url = f"{BASE_URL}{method_b}_{idx}.mp4"

            for question in QUESTIONS:
                rows.append({
                    "question": question,
                    "prompt": f"Video {idx}",
                    "video_input_url": "",
                    "video_a_url": video_a_url,
                    "video_b_url": video_b_url,
                    "method_a": method_a,
                    "method_b": method_b,
                    "fresco": idx,
                })

    random.shuffle(rows)

    with open(output_file, "w", newline="") as f:
        fieldnames = ["question", "prompt", "video_input_url", "video_a_url", "video_b_url",
                      "method_a", "method_b", "fresco"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Generated {len(rows)} rows in {output_file}")

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
