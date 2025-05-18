from turtle import color
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from windrose import WindroseAxes

def prepare_time_series(df):
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], format='%Y-%m-%d %H:%M')
    df.set_index('Timestamp', inplace=True)
    return df

def plot_time_series(df, columns):
    sampled_df = df.resample('D').mean().ffill()
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    fig, axs = plt.subplots(2, 2, figsize=(16, 10))
    axs = axs.flatten()
    for i, col in enumerate(columns):
        axs[i].plot(sampled_df.index, sampled_df[col], color=colors[i], label=col)
        axs[i].set_title(f"Time Series of {col}")
        axs[i].set_xlabel("Timestamp")
        axs[i].set_ylabel(col)
        axs[i].grid(True)
        axs[i].legend()
    plt.tight_layout()
    plt.show()

def plot_period(df, columns, start_date, end_date, title_suffix=""):
    period_df = df.loc[start_date:end_date]
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    fig, axs = plt.subplots(4, 1, figsize=(16, 20))
    axs = axs.flatten()
    for i, col in enumerate(columns):
        axs[i].plot(period_df.index, period_df[col], label=col, color=colors[columns.index(col)])
        axs[i].set_title(f"{col} ({title_suffix}) {start_date} to {end_date}")
        axs[i].set_xlabel("Timestamp")
        axs[i].set_ylabel(col)
        axs[i].grid(True)
        axs[i].legend()
    plt.tight_layout()
    plt.show()

def plot_cleaning_effect(df):
    mod_means = df.groupby('Cleaning')[['ModA', 'ModB']].mean()
    mod_means.plot(kind='bar', figsize=(8, 6), color=['#1f77b4', '#ff7f0e'])
    plt.title('Average ModA and ModB by Cleaning Status')
    plt.xlabel('Cleaning (0 = Before, 1 = After)')
    plt.ylabel('Average Irradiance (W/m²)')
    plt.xticks(ticks=[0, 1], labels=['Before Cleaning', 'After Cleaning'], rotation=0)
    plt.grid(axis='y')
    plt.legend(title='Sensor')
    plt.tight_layout()
    plt.show()

def plot_correlation_heatmap(df, columns):
    corr_matrix = df[columns].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    plt.show()

def plot_scatter_pairs(df, pairs):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    for i, (x, y) in enumerate(pairs):
        sns.scatterplot(data=df, x=x, y=y, ax=axes[i], alpha=0.6)
        axes[i].set_title(f'{y} vs. {x}')
    if len(pairs) < 6:
        fig.delaxes(axes[-1])
    plt.tight_layout()
    plt.show()

def plot_histograms(df):
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    curated_ghi = df['GHI'].replace(0, np.nan).dropna()
    sns.histplot(curated_ghi, bins=40, kde=True, ax=axes[0], color='orange')
    axes[0].set_title("Histogram of GHI")
    sns.histplot(df['WS'], bins=40, kde=True, ax=axes[1], color='blue')
    axes[1].set_title("Histogram of Wind Speed")
    plt.tight_layout()
    plt.show()

def plot_wind_rose(df):
    ax = WindroseAxes.from_ax()
    ax.bar(df["WD"], df["WS"], normed=True, opening=0.8, edgecolor='white')
    ax.set_legend(title="Wind Speed (m/s)")
    plt.title("Wind Rose")
    plt.show()

def plot_rh_effect(df):
    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.scatterplot(x='RH', y='Tamb', data=df, ax=axs[0])
    sns.scatterplot(x='RH', y='GHI', data=df, ax=axs[1])
    axs[0].set_title('RH vs. Tamb')
    axs[1].set_title('RH vs. GHI')
    plt.tight_layout()
    plt.show()

    fig, axs = plt.subplots(1, 2, figsize=(12, 5))
    sns.regplot(x='RH', y='Tamb', data=df, ax=axs[0], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    sns.regplot(x='RH', y='GHI', data=df, ax=axs[1], scatter_kws={'alpha':0.5}, line_kws={'color':'red'})
    axs[0].set_title('RH vs. Tamb with Trendline')
    axs[1].set_title('RH vs. GHI with Trendline')
    plt.tight_layout()
    plt.show()

def plot_bubble_chart(df, size='RH'):
    plt.figure(figsize=(8,6))
    sizes = df[size] / df[size].max() * 30
    plt.scatter(df["GHI"], df["Tamb"], s=sizes, alpha=0.5, c='blue', edgecolors='w', linewidth=0.5)
    plt.xlabel("GHI")
    plt.ylabel("Tamb")
    plt.title(f'Bubble Chart: {"Tamb"} vs. {"GHI"} with bubble size = {size}')
    plt.grid(True)
    plt.show()