import pandas as pd

df = pd.read_csv('llm-persian-emotion-detection/SentimentData/UnCleaned/jabama.csv')

df_filtered = df[['comment']]

df_filtered.to_csv('filtered_file.csv', index=False)
