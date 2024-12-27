import pandas as pd

# فایل ورودی
input_file = "final_output_gpt_v.csv"
# فایل خروجی
output_file = "output.csv"

# ستون‌هایی که می‌خواهید نگه دارید
columns_to_keep = ["id", "text", "label","subject"]

# خواندن فایل CSV
df = pd.read_csv(input_file)

# فیلتر کردن ستون‌ها
df_filtered = df[columns_to_keep]

# ذخیره فایل خروجی
df_filtered.to_csv(output_file, index=False, encoding="utf-8-sig")

print("فایل خروجی با موفقیت ذخیره شد.")
