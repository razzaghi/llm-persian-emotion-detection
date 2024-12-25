import csv
import ast

specified_labels = set([
    "Like", "Embarrassment", "Guilt", "Love", "Happiness", "Surprise", "Anger", "Sadness", "Fear", "Anxiety",
    "Excitement", "Despair", "Satisfaction", "Funny", "Hate", "Gratitude", "Criticism", "Hope", "Neutral", "Worry",
    "Trust", "Regret","Question"
])

input_csv_path = "llm-persian-emotion-detection/Prepare_Data/Generate_Label_Script/final_output_gpt_v1.csv"
output_txt_path = "unknown_labels.txt"

unknown_labels = set()

with open(input_csv_path, "r", encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        try:
            labels = ast.literal_eval(row["label"])
            for label in labels.keys():
                if label not in specified_labels:
                    unknown_labels.add(label)
        except Exception as e:
            print(f"Error processing row: {row}, Error: {e}")

with open(output_txt_path, "w", encoding="utf-8") as txtfile:
    for label in sorted(unknown_labels):
        txtfile.write(f"{label}\n")

print(f"Unknown labels saved to {output_txt_path}")
