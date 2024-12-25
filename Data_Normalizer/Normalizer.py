# just need text column

import pandas as pd
import re
import unicodedata
import emoji

# Convert non-breaking spaces to regular spaces
def normalize_non_breaking_space(text):
    if isinstance(text, str):  # Ensure that the text is a string
        return text.replace('\u200C', ' ')
    return text  # Return as is if it's not a string

# Remove emojis from text
def remove_emojis(text):
    if isinstance(text, str):
        return emoji.replace_emoji(text, replace='')
    return text

# Convert Persian numbers to English numbers
def persian_to_english_numbers(text):
    if isinstance(text, str):
        persian_digits = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹']
        english_digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        table = str.maketrans(''.join(persian_digits), ''.join(english_digits))
        return text.translate(table)
    return text

# Convert Arabic characters to Persian characters
def arabic_to_persian(text):
    if isinstance(text, str):
        arabic_letters = {'ي': 'ی', 'ك': 'ک'}
        for arabic, persian in arabic_letters.items():
            text = text.replace(arabic, persian)
        return text
    return text

# Replace special characters with spaces
def replace_special_chars(text):
    if isinstance(text, str):
        chars_to_replace = ['@', '#', '*', '_', "'", '"', '""', "''", '&', '^']
        for char in chars_to_replace:
            text = text.replace(char, ' ')
        return text
    return text


# Remove extra spaces and newline characters
def remove_extra_spaces_and_newlines(text):
    if isinstance(text, str):
        # Replace multiple spaces with a single space
        text = re.sub(r'\s+', ' ', text)
        # Remove newline characters
        text = re.sub(r'\n+', ' ', text)
        return text
    return text

# Remove exact duplicates
def remove_exact_duplicates(df):
    return df.drop_duplicates(subset='text')

# Main function to clean the dataset
def clean_dataset(input_file, output_file):
    # Load dataset
    df = pd.read_csv(input_file)

    # Apply preprocessing steps
    df['text'] = df['text'].apply(normalize_non_breaking_space)
    df['text'] = df['text'].apply(remove_emojis)
    df['text'] = df['text'].apply(persian_to_english_numbers)
    df['text'] = df['text'].apply(arabic_to_persian)
    df['text'] = df['text'].apply(replace_special_chars)
    df['text'] = df['text'].apply(remove_extra_spaces_and_newlines)

    # Remove exact duplicates
    df = remove_exact_duplicates(df)

    # Save the cleaned dataset
    df.to_csv(output_file, index=False)

# Usage
input_file = 'llm-persian-emotion-detection/SentimentData/Cleaned/medical_cleaned.csv'
output_file = 'x_cleaned.csv'
clean_dataset(input_file, output_file)
