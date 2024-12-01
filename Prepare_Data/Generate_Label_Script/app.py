
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

# def process_texts(input_csv, output_csv, subject):
#     client = initialize_openai_client(OPENAI_API_KEY)
#     processed_count = 0  

#     with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
#          open(output_csv, 'a', newline='', encoding='utf-8') as outfile:
#         reader = csv.reader(infile)
#         writer = csv.writer(outfile)

#         if outfile.tell() == 0:
#             writer.writerow(['text', 'label'])
        
#         for row in reader:
#             text = row[0]
#             try:
#                 label = label_generator(client, subject, text)
#             except Exception as e:
#                 print(f"Error processing text '{text}': {e}")
#                 label = ''
#             writer.writerow([text, label])
#             outfile.flush()
#             processed_count += 1 
#             print(f"Processed {processed_count} texts")
            
#     print(f"Total texts processed: {processed_count}")

# subject = "E-commerce comments"  
# process_texts('/Users/borhandarvishi/Desktop/PROJECTS/llm-persian-emotion-detection/Prepare_Data/Generate_Label_Script/input.csv', 'output.csv', subject)

import openai
from openai import OpenAI
import csv
import os
from dotenv import load_dotenv

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

def process_texts(input_csv, output_csv, subject):
    client = initialize_openai_client(OPENAI_API_KEY)
    processed_count = 0

    with open(input_csv, 'r', newline='', encoding='utf-8') as infile, \
         open(output_csv, 'a', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile)  
        fieldnames = reader.fieldnames + ['label']  
        
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)

        if outfile.tell() == 0:
            writer.writeheader()
        
        for row in reader:
            text = row['text']  
            row_id = row['id'] 
            try:
                label = label_generator(client, subject, text)
            except Exception as e:
                print(f"Error processing text '{text}': {e}")
                label = ''
            row['label'] = label  
            writer.writerow(row) 
            outfile.flush()
            processed_count += 1 
            print(f"Processed {processed_count} texts")
            
    print(f"Total texts processed: {processed_count}")

subject = "E-commerce comments"  
process_texts('../Input_Data/input.csv', '../OutPut_Data/output.csv', subject)


