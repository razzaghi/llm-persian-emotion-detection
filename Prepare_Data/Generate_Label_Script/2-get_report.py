import pandas as pd
import ast

file_path = "llm-persian-emotion-detection/Prepare_Data/OutPut_Data/output.csv"
df = pd.read_csv(file_path)

def clean_label_format(label):
    try:
        if isinstance(label, str):
            label = label.replace("[", "{").replace("]", "}") 
            label = label.replace("'", '"')  
            return ast.literal_eval(label) 
        return label
    except (ValueError, SyntaxError):
        return {}

df['label'] = df['label'].apply(clean_label_format)

positive_labels = {'Like', 'Love', 'Happiness', 'Excitement', 'Gratitude', 'Satisfaction', 'Hope', 'Trust', 'Funny'}
negative_labels = {'Embarrassment', 'Guilt', 'Anger', 'Sadness', 'Fear', 'Anxiety', 'Despair', 'Hate', 'Criticism', 'Regret', 'Worry'}
neutral_labels = {'Surprise', 'Neutral'}

all_labels = positive_labels | negative_labels | neutral_labels

def calculate_vibe(labels):
    positive_score = sum(value for key, value in labels.items() if key in positive_labels)
    negative_score = sum(value for key, value in labels.items() if key in negative_labels)
    neutral_score = sum(value for key, value in labels.items() if key in neutral_labels)
    if positive_score == 0 and negative_score == 0 and neutral_score > 0:
        return 2
    score = positive_score - negative_score
    return 0 if score > 0 else 1

def check_error(labels):
    total_score = sum(labels.values())
    return 1 if total_score > 1 else 0

def check_wrong_label(labels):
    for key in labels.keys():
        if key not in all_labels:
            return 1
    return 0

df['vibe'] = df['label'].apply(calculate_vibe)
df['error'] = df['label'].apply(check_error)
df['wrong_label'] = df['label'].apply(check_wrong_label)

positive_count = (df['vibe'] == 0).sum()
negative_count = (df['vibe'] == 1).sum()
neutral_count = (df['vibe'] == 2).sum()
error_count = df['error'].sum()
wrong_label_count = df['wrong_label'].sum()

print("Summary:")
print(f"Positive Vibes: {positive_count}")
print(f"Negative Vibes: {negative_count}")
print(f"Neutral Vibes: {neutral_count}")
print(f"Errors: {error_count}")
print(f"Wrong Labels: {wrong_label_count}")
