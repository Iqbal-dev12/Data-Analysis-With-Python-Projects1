# ================================
# 📊 Page View Time Series Visualizer
# Colab-ready version (uses file upload)
# ================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.colab import files

# Step 1: Ask user to upload the CSV
print("📂 Please upload fcc-forum-pageviews.csv from your computer...")
uploaded = files.upload()
file_name = list(uploaded.keys())[0]  # get the first uploaded file

# Step 2: Read and clean the data
df = pd.read_csv(file_name, parse_dates=["date"], index_col="date")

# Clean data by removing top and bottom 2.5%
low = df["value"].quantile(0.025)
high = df["value"].quantile(0.975)
df = df[(df["value"] >= low) & (df["value"] <= high)]

# Step 3: Define plotting functions
def draw_line_plot():
    fig, ax = plt.subplots(figsize=(15, 5))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")
    plt.tight_layout()
    fig.savefig("line_plot.png")
    files.download("line_plot.png")
    return fig

def draw_bar_plot():
    df_bar = df.copy()
    df_bar["year"] = df_bar.index.year
    df_bar["month"] = df_bar.index.month
    df_grouped = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    fig = df_grouped.plot(kind="bar", figsize=(10, 7)).figure
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(
        title="Months",
        labels=[
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
    )
    plt.tight_layout()
    fig.savefig("bar_plot.png")
    files.download("bar_plot.png")
    return fig

def draw_box_plot():
    df_box = df.copy()
    df_box.reset_index(inplace=True)
    df_box["year"] = [d.year for d in df_box.date]
    df_box["month"] = [d.strftime("%b") for d in df_box.date]

    month_order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

    fig, axes = plt.subplots(1, 2, figsize=(15, 5))

    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    sns.boxplot(x="month", y="value", data=df_box, order=month_order, ax=axes[1])
    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    plt.tight_layout()
    fig.savefig("box_plot.png")
    files.download("box_plot.png")
    return fig

# Step 4: Call functions to generate and download plots
print("✅ File loaded and cleaned. Generating plots...")
draw_line_plot()
draw_bar_plot()
draw_box_plot()
print("✅ All plots generated and downloaded!")
