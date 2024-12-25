import pandas as pd

# File paths and corresponding subject values
files = [
    ('achareh_cleaned.csv', 'نظرات ارائه دهندگان خدمات'),
    ('ecommers_cleaned.csv', 'نظرات محصول فروشگاهی'),
    ('education_cleaned.csv', 'نظرات دوره های آموزشی'),
    ('food_cleaned.csv', 'نظرات در مورد غذا ها'),
    ('jabama_cleaned.csv', 'نظرات برای اجاره مکان گردشی'),
    ('Legal_cleaned.csv', 'نظرات خدمات حقوقی'),
    ('medical_cleaned.csv', 'نظرات در مورد پزشک ها')
]

# Initialize an empty DataFrame to store combined data
all_data = pd.DataFrame()

# Loop through files, read them, and add the subject column
for file_path, subject_value in files:
    df = pd.read_csv(file_path)  # Read the CSV file
    df['subject'] = subject_value  # Add the subject column
    all_data = pd.concat([all_data, df], ignore_index=True)  # Append to the combined DataFrame

# Add an 'id' column with values ranging from 1 to the number of rows
all_data['id'] = range(1, len(all_data) + 1)

# Save the combined data to a new CSV file
all_data.to_csv('all_data.csv', index=False)

print("Combined data saved to 'all_data.csv' with an 'id' column.")
