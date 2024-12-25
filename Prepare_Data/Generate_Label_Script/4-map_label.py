import csv
import ast

mapping = {
    "Like": ["Dislike"],
    "Embarrassment": [],
    "Guilt": [],
    "Love": [],
    "Happiness": [],
    "Surprise": [],
    "Anger": ["Frustration"],
    "Sadness": ["Disappointment", "Nostalgia"],
    "Fear": ["Warning"],
    "Anxiety": [],
    "Excitement": [],
    "Despair": [],
    "Satisfaction": ["Pride", "Relief"],
    "Funny": [],
    "Hate": ["Disgust", "Dislike"],
    "Gratitude": ["Thankfulness"],
    "Criticism": ["Suggestion"],
    "Hope": ["Curiosity", "Expectation"],
    "Neutral": ["Confusion"],
    "Worry": ["Concern"],
    "Trust": [],
    "Regret": []
}

reverse_mapping = {v: k for k, values in mapping.items() for v in values}

input_csv_path = "output_with_vibe_error_wrong_label.csv"
output_csv_path = "final_output_gpt_v.csv"

with open(input_csv_path, "r", encoding="utf-8") as csvfile, open(output_csv_path, "w", encoding="utf-8", newline="") as outfile:
    reader = csv.DictReader(csvfile)
    fieldnames = reader.fieldnames
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()

    for row in reader:
        try:
            labels = ast.literal_eval(row["label"])
            mapped_labels = {}
            for label, value in labels.items():
                if label in reverse_mapping:
                    new_label = reverse_mapping[label]
                    mapped_labels[new_label] = value
                else:
                    mapped_labels[label] = value
            row["label"] = str(mapped_labels)
            writer.writerow(row)
        except Exception as e:
            print(f"Error processing row: {row}, Error: {e}")

print(f"Mapped labels saved to {output_csv_path}")
