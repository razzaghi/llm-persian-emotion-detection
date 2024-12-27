import csv
import ast


mapping = {
    "Like": ["Admiration", "Respect", "Care", "Acceptance", "Humility"],
    "Embarrassment": [],
    "Guilt": ["Regret", "Forgiveness"],
    "Love": ["Admiration", "Care", "Empathy", "Sympathy"],
    "Happiness": ["Satisfaction", "Pride"],
    "Surprise": ["Anticipation"],
    "Anger": ["Annoyance", "Frustration"],
    "Sadness": ["Disappointment", "Nostalgia", "Weakness"],
    "Fear": ["Warning", "Nervousness", "Urgency"],
    "Anxiety": ["Nervousness", "Stress", "Impatience", "Hurry"],
    "Excitement": ["Anticipation"],
    "Despair": ["Pain", "Fatigue", "Discomfort", "Cold"],
    "Satisfaction": ["Pride", "Relief", "Understanding"],
    "Funny": [],
    "Hate": ["Disgust", "Dislike", "Distrust"],
    "Gratitude": ["Thankfulness", "Empathy"],
    "Criticism": ["Suggestion", "Dissatisfaction"],
    "Hope": ["Curiosity", "Expectation", "Expectations", "Encouragement"],
    "Neutral": ["Confusion", "Calm", "Calmness", "Patience"],
    "Worry": ["Concern", "Uncertainty"],
    "Trust": ["Confidence", "Responsibility", "Effort"],
    "Regret": ["Guilt", "Forgiveness"],
    "Request": ["Need", "Help", "Hunger", "Impatience"],
    "Advice": ["Suggestion", "Encouragement"]
}



reverse_mapping = {v: k for k, values in mapping.items() for v in values}

input_csv_path = "/Users/borhandarvishi/Desktop/llm-persian-emotion-detection/Prepare_Data/Generate_Label_Script/output_with_vibe_error_wrong_label.csv"
output_csv_path = "maped_label.csv"

with open(input_csv_path, "r", encoding="utf-8-sig") as csvfile, open(output_csv_path, "w", encoding="utf-8-sig", newline="") as outfile:
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
