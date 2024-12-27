import pandas as pd
import glob

# مسیر فایل‌های CSV
path = '*.csv'  # اینجا مسیر فایل‌ها را تنظیم کنید

# خواندن تمام فایل‌های CSV در پوشه
all_files = glob.glob(path)

# لیستی برای ذخیره داده‌ها
data_frames = []

# خواندن هر فایل CSV و اضافه کردن به لیست
for file in all_files:
    df = pd.read_csv(file)  # فرض بر این است که فایل UTF-8 است
    data_frames.append(df)

# ترکیب تمام فایل‌ها در یک DataFrame
combined_data = pd.concat(data_frames, ignore_index=True)

# حذف ردیف‌های تکراری بر اساس ستون 'id'
combined_data = combined_data.drop_duplicates(subset='id')

# مرتب‌سازی بر اساس ستون 'id'
combined_data = combined_data.sort_values(by='id')

# ذخیره داده‌ها در فایل خروجی
combined_data.to_csv('all_output.csv', index=False, encoding='utf-8-sig')

print("ترکیب فایل‌ها با موفقیت انجام شد و فایل خروجی به نام all_data.csv ذخیره شد.")
