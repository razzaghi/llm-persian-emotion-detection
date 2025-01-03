import openai
from openai import OpenAI
import csv
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

from prompt import prompt_template

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def initialize_openai_client(api_key):
    """
    Initializes and returns the OpenAI client.
    """
    return OpenAI(api_key=OPENAI_API_KEY)

def label_generator(client, subject, text):
    """
    Returns the emotion labels and their percentages for the given text and subject.
    """    
    prompt = prompt_template.format(subject=subject, text=text)

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": prompt}],
        temperature=0.2,  
        top_p=0.8, 
    )
    
    return response.choices[0].message.content.strip()

def process_row(client, row):
    """
    Processes a single row of the input CSV.
    """
    try:
        text = row['text']
        subject = row['subject']
        label = label_generator(client, subject, text)
    except Exception as e:
        print(f"Error processing row ID {row.get('id')}: {e}")
        label = ''
    row['label'] = label
    return row

def process_texts_multithread(input_csv, output_csv, num_threads=8):
    client = initialize_openai_client(OPENAI_API_KEY)
    processed_count = 0
    ignore_count = 370725

    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'a', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ['label']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        if outfile.tell() == 0:
            writer.writeheader()

        rows = list(reader)
        rows_to_process = rows[ignore_count:]
        
        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            futures = [
                executor.submit(process_row, client, row)
                for row in rows_to_process
            ]
            for future in futures:
                try:
                    processed_row = future.result()
                    writer.writerow(processed_row)
                    outfile.flush()
                    processed_count += 1
                    print(f"Processed {processed_count} texts")
                except Exception as e:
                    print(f"Error processing row: {e}")

    print(f"Total texts processed: {processed_count}")

process_texts_multithread('../Input_Data/input.csv', '../OutPut_Data/output.csv')

# import openai
# from openai import OpenAI
# import csv
# import os
# from dotenv import load_dotenv

# from prompt import prompt_template

# load_dotenv()

# OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# def initialize_openai_client(api_key):
#     """
#     Initializes and returns the OpenAI client.
#     """
#     return OpenAI(api_key=OPENAI_API_KEY)

# def label_generator(client, subject, text):
#     """
#     Returns the emotion labels and their percentages for the given text and subject.
#     """    
#     prompt = prompt_template.format(subject=subject, text=text)

#     response = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "system", "content": prompt}],
#         temperature=0.2,  
#         top_p=0.8, 
#     )
    
#     return response.choices[0].message.content.strip()

# def process_texts(input_csv, output_csv):
#     client = initialize_openai_client(OPENAI_API_KEY)
#     processed_count = 0
#     ignore_count = 3910

#     with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
#          open(output_csv, 'a', newline='', encoding='utf-8') as outfile:
#         reader = csv.DictReader(infile)  
#         fieldnames = reader.fieldnames + ['label']  
        
#         writer = csv.DictWriter(outfile, fieldnames=fieldnames)

#         if outfile.tell() == 0:
#             writer.writeheader()
        
#         for row in reader:
#             if processed_count > ignore_count:
#                 text = row['text']  
#                 row_id = row['id'] 
#                 subject = row['subject']  
                
#                 try:
#                     label = label_generator(client, subject, text)
#                 except Exception as e:
#                     print(f"Error processing text '{text}': {e}")
#                     label = ''
#                 row['label'] = label  
#                 writer.writerow(row) 
#                 outfile.flush()
#                 processed_count += 1 
#                 print(f"Processed {processed_count} texts")
#             else:
#                 processed_count += 1
            
#     print(f"Total texts processed: {processed_count}")

# process_texts('../Input_Data/input.csv', '../OutPut_Data/output.csv')
