import json
import sys
import llm
from prompts import CATEGORIES, get_prompt

DATASET_PATH = "evals/dataset.jsonl"
MIN_SCORE = 0.85  


def main():
    total = 0
    correct = 0

    with open(DATASET_PATH, "r") as f:
        for line in f:
            row = json.loads(line)
            email_text = row["email"]
            expected = row["expected_category"]


            prompt = get_prompt(email_text)
            predicted = llm.complete(prompt).lower().strip()

            total += 1
            if predicted == expected:
                correct += 1
            else:
                print(
                    f"[MISS] #{row['id']}: expected='{expected}', got='{predicted}' | {email_text}"
                )

    accuracy = correct / total
    print(f"\nEval Score: {correct}/{total} ({accuracy:.1%})")

    if accuracy < MIN_SCORE:
        print(f"FAILED: Score {accuracy:.1%} is below threshold {MIN_SCORE:.1%}")
        sys.exit(1)

    print("PASSED!")


if __name__ == "__main__":
    main()