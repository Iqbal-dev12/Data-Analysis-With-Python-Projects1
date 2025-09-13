import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import linregress
import numpy as np
from google.colab import files

# Step 1: Upload file
print("📂 Please upload epa-sea-level.csv from your computer...")
uploaded = files.upload()
file_name = list(uploaded.keys())[0]

# Step 2: Read CSV with auto delimiter detection
df = pd.read_csv(file_name, sep=None, engine='python')
print("📑 Detected Columns:", df.columns.tolist())
print(df.head())

# If there's only one column, try splitting manually
if len(df.columns) == 1:
    print("⚠️ Detected single column — trying to split manually...")
    df = pd.read_csv(file_name, sep=',', engine='python')  # Force comma split
    print("✅ After re-read, columns are:", df.columns.tolist())
    print(df.head())

# Normalize column names
df.columns = df.columns.str.strip().str.lower()

# Find year & sea level columns dynamically
year_candidates = [col for col in df.columns if "year" in col]
sea_candidates = [col for col in df.columns if "adjusted" in col]

if not year_candidates or not sea_candidates:
    raise ValueError("❌ Could not detect year or sea level column automatically. "
                     "Please check your CSV file format.")

year_col = year_candidates[0]
sea_col = sea_candidates[0]

# Step 3: Scatter plot
plt.figure(figsize=(12, 6))
plt.scatter(df[year_col], df[sea_col], alpha=0.7, label="Data points")

# Step 4: First line of best fit (all data)
slope_all, intercept_all, *_ = linregress(df[year_col], df[sea_col])
x_pred_all = np.arange(int(df[year_col].min()), 2051)
y_pred_all = intercept_all + slope_all * x_pred_all
plt.plot(x_pred_all, y_pred_all, 'r', label='Best fit line (1880–Present)')

# Step 5: Second line of best fit (since 2000)
df_recent = df[df[year_col] >= 2000]
slope_recent, intercept_recent, *_ = linregress(df_recent[year_col], df_recent[sea_col])
x_pred_recent = np.arange(2000, 2051)
y_pred_recent = intercept_recent + slope_recent * x_pred_recent
plt.plot(x_pred_recent, y_pred_recent, 'g', label='Best fit line (2000–Present)')

# Step 6: Labels and title
plt.xlabel('Year')
plt.ylabel('Sea Level (inches)')
plt.title('Rise in Sea Level')
plt.legend()
plt.grid(alpha=0.3)

# Step 7: Save & download
plt.savefig('sea_level_plot.png')
files.download('sea_level_plot.png')
plt.show()
