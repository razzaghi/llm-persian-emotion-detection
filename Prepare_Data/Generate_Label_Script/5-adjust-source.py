# This script processes emotion labels by mapping them using predefined mappings,
# adjusting their values to ensure the sum equals 1, and saving the cleaned output
# to a CSV file with only necessary columns retained.

import pandas as pd
import ast
import csv

# Load the CSV file
input_csv_path = "/Users/borhandarvishi/Desktop/llm-persian-emotion-detection/SentimentData/Train_Data/all_output.csv"
output_csv_path = "maped_and_adjusted_labels.csv"

# Mapping for emotion labels
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

# Function to clean label format
def clean_label_format(label):
    try:
        if isinstance(label, str):
            label = label.replace("[", "{").replace("]", "}")   
            label = label.replace("'", '"') 
            return ast.literal_eval(label)  
        return label
    except (ValueError, SyntaxError):
        return {}

# Function to map labels using reverse mapping
def map_labels(labels):
    mapped_labels = {}
    for label, value in labels.items():
        if label in reverse_mapping:
            new_label = reverse_mapping[label]
            if new_label in mapped_labels:
                mapped_labels[new_label] += value  # Add to existing value
            else:
                mapped_labels[new_label] = value
        else:
            if label in mapped_labels:
                mapped_labels[label] += value  # Add to existing value
            else:
                mapped_labels[label] = value
    return mapped_labels

# Function to clean and adjust label format
def clean_and_adjust_label(label):
    if not label:  # Check if the label is empty
        return label  # Return as is if no labels are present

    total = sum(label.values())
    if total > 1:
        # If total exceeds 1, subtract the excess from the largest label
        excess = total - 1
        max_label = max(label, key=label.get)
        label[max_label] -= excess
    elif total < 1:
        # If total is less than 1, add the deficit to the largest label
        deficit = 1 - total
        max_label = max(label, key=label.get)
        label[max_label] += deficit

    return {key: max(value, 0) for key, value in label.items()}  # Ensure no negative values

# Read input CSV
df = pd.read_csv(input_csv_path)

# Process each row to map and adjust labels
def process_row(row):
    try:
        labels = clean_label_format(row["label"])
        mapped_labels = map_labels(labels)
        adjusted_labels = clean_and_adjust_label(mapped_labels)
        return adjusted_labels
    except Exception as e:
        print(f"Error processing row ID {row['id']}: {e}")
        return {}

df['label'] = df.apply(process_row, axis=1)

# Keep only necessary columns
df = df[["id", "text", "label", "subject"]]

# Save the final output to CSV
df.to_csv(output_csv_path, index=False)

print(f"Mapped and adjusted labels saved to {output_csv_path}")
