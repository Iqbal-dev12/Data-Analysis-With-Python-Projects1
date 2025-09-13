
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import os
from io import StringIO

# ------------------------
# CSV filename
csv_file = "medical_examination.csv"

# Check if CSV exists locally
if not os.path.exists(csv_file):
    # If not, use Colab file upload
    try:
        from google.colab import files
        print("CSV file not found locally. Please upload your CSV file.")
        uploaded = files.upload()  # upload your CSV
        csv_file = list(uploaded.keys())[0]
    except ImportError:
        # If not in Colab, create a sample CSV as fallback
        print("CSV file not found. Creating a small sample CSV.")
        sample_data = """height,weight,cholesterol,gluc,smoke,alco,active,cardio,ap_lo,ap_hi
170,70,1,1,0,0,1,0,80,120
180,90,2,1,1,0,1,1,90,140
160,50,1,2,0,1,0,0,70,110
"""
        csv_file = "medical_examination.csv"
        with open(csv_file, "w") as f:
            f.write(sample_data)

# Load the CSV
df = pd.read_csv(csv_file)

# Add 'overweight' column
df['BMI'] = df['weight'] / ((df['height']/100) ** 2)
df['overweight'] = (df['BMI'] > 25).astype(int)
df.drop('BMI', axis=1, inplace=True)

# Normalize data: 0 = good, 1 = bad
df['cholesterol'] = (df['cholesterol'] > 1).astype(int)
df['gluc'] = (df['gluc'] > 1).astype(int)

def draw_cat_plot():
    df_cat = pd.melt(df,
                     id_vars=['cardio'],
                     value_vars=['cholesterol', 'gluc', 'smoke', 'alco', 'active', 'overweight'])
    df_cat = df_cat.groupby(['cardio', 'variable', 'value']).size().reset_index(name='total')

    fig = sns.catplot(
        data=df_cat,
        x='variable',
        y='total',
        hue='value',
        col='cardio',
        kind='bar'
    ).fig

    return fig

def draw_heat_map():
    df_heat = df[
        (df['ap_lo'] <= df['ap_hi']) &
        (df['height'] >= df['height'].quantile(0.025)) &
        (df['height'] <= df['height'].quantile(0.975)) &
        (df['weight'] >= df['weight'].quantile(0.025)) &
        (df['weight'] <= df['weight'].quantile(0.975))
    ]

    corr = df_heat.corr()
    mask = np.triu(np.ones_like(corr, dtype=bool))

    fig, ax = plt.subplots(figsize=(12, 10))
    sns.heatmap(corr, mask=mask, annot=True, fmt=".1f", cmap='coolwarm', square=True, linewidths=0.5)

    return fig

# Draw and save plots
cat_fig = draw_cat_plot()
cat_fig.savefig("catplot.png")
print("Categorical plot saved as catplot.png")

heat_fig = draw_heat_map()
heat_fig.savefig("heatmap.png")
print("Heatmap saved as heatmap.png")
