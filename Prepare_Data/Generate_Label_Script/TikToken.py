import pandas as pd
import tiktoken

comments = [
    '''You are an assistant for detecting emotions and their percentages in text.#Rules:-Each input contains one or more emotions with percentages.-Exclude undetectable emotions.-Focus only on the given text and rules.-Consider idioms and Persian cultural references.-If the input is a question, add a "question": true tag.-Act only on the given subject and input.#Labels:Like, Love, Happiness, Surprise, Anger, Sadness, Fear, Anxiety, Excitement, Despair, Satisfaction, Funny, Hate, Criticism, Hope, Neutral, Worry, Trust, Regret. #just return Output in this Format: ['emo1': 0.3, 'emo2': 0.7]#Subject : {subject}#User Input: {text}'''
]


encoding_name = "o200k_base"
encoding = tiktoken.get_encoding(encoding_name)

# Function to count tokens in each comment
def count_tokens_in_comment(comment: str) -> int:
    """Count the number of tokens in a comment using tiktoken"""
    if not isinstance(comment, str):  
        return 0  
    tokens = encoding.encode(comment)
    return len(tokens)

# Convert the list of comments to a DataFrame for easier manipulation
df = pd.DataFrame(comments, columns=["comment"])

# Count tokens for each comment and add it as a new column
df['TokenCount'] = df['comment'].apply(count_tokens_in_comment)

# Display the results
print("Token count results:")
print(df)

# Calculate the total token count
total_token_count = df['TokenCount'].sum()
print(f"Total token count: {total_token_count} tokens")
