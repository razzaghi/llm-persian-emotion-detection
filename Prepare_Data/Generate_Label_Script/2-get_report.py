import pandas as pd
import ast

# Load the CSV file
file_path = "/Users/borhandarvishi/Desktop/llm-persian-emotion-detection/Prepare_Data/Generate_Label_Script/output_with_vibe_error_wrong_label.csv"
df = pd.read_csv(file_path)

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

# Clean labels
df['label'] = df['label'].apply(clean_label_format)

# Define label categories
positive_labels = {'Like', 'Love', 'Happiness', 'Excitement', 'Gratitude', 'Satisfaction', 'Hope', 'Trust', 'Funny','Advice'}
negative_labels = {'Embarrassment', 'Guilt', 'Anger', 'Sadness', 'Fear', 'Anxiety', 'Despair', 'Hate', 'Criticism', 'Regret', 'Worry'}
neutral_labels = {'Surprise', 'Neutral','Request','Question'}

all_labels = positive_labels | negative_labels | neutral_labels

# Function to calculate vibe
def calculate_vibe(labels):
    positive_score = sum(value for key, value in labels.items() if key in positive_labels)
    negative_score = sum(value for key, value in labels.items() if key in negative_labels)
    neutral_score = sum(value for key, value in labels.items() if key in neutral_labels)
    if positive_score == 0 and negative_score == 0 and neutral_score > 0:
        return 2
    score = positive_score - negative_score
    return 0 if score > 0 else 1

# Function to check for errors
def check_error(labels):
    total_score = sum(labels.values())
    return 1 if total_score > 1 else 0

# Function to check for wrong labels
def check_wrong_label(labels):
    for key in labels.keys():
        if key not in all_labels:
            return 1
    return 0

# Apply calculations
df['vibe'] = df['label'].apply(calculate_vibe)
df['error'] = df['label'].apply(check_error)
df['wrong_label'] = df['label'].apply(check_wrong_label)

# Filter data for each category
positive_vibes = df[df['vibe'] == 0]
negative_vibes = df[df['vibe'] == 1]
neutral_vibes = df[df['vibe'] == 2]
errors = df[df['error'] == 1]
wrong_labels = df[df['wrong_label'] == 1]

# Save each category to separate CSV files
positive_vibes.to_csv("REPORT/positive_vibes.csv", index=False)
negative_vibes.to_csv("REPORT/negative_vibes.csv", index=False)
neutral_vibes.to_csv("REPORT/neutral_vibes.csv", index=False)
errors.to_csv("REPORT/error.csv", index=False)
wrong_labels.to_csv("REPORT/wrong_labels.csv", index=False)

# Summary report
positive_count = len(positive_vibes)
negative_count = len(negative_vibes)
neutral_count = len(neutral_vibes)
error_count = len(errors)
wrong_label_count = len(wrong_labels)

print("Summary:")
print(f"Positive Vibes: {positive_count}")
print(f"Negative Vibes: {negative_count}")
print(f"Neutral Vibes: {neutral_count}")
print(f"Errors: {error_count}")
print(f"Wrong Labels: {wrong_label_count}")
