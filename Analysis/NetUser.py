import pandas as pd
import numpy as np
from scipy.stats import spearmanr
import seaborn as sns
import matplotlib.pyplot as plt
import os
from datetime import datetime

# 参数设置
missing_threshold = 0.2  # 允许的最大缺失值比例
years = list(range(2000, 2024))
analysis_years = (2010, 2022)

def process_internet_data():
    df_internet = pd.read_excel('DATA/API_IT.NET.USER.ZS_DS2_zh_excel_v2_94.xls', header=None)
    df_internet.columns = ['Country Code'] + years

    # Reshape to long format and filter years
    df_internet_long = pd.melt(
        df_internet,
        id_vars=['Country Code'],
        value_vars=years,
        var_name='Year',
        value_name='Internet Users (%)'
    ).query(f'{analysis_years[0]} <= Year <= {analysis_years[1]}')

    # Clean and interpolate
    df_internet_cleaned = (
        df_internet_long.groupby('Country Code')
        .filter(lambda x: x['Internet Users (%)'].isnull().mean() <= missing_threshold)
        .assign(
            Year=lambda x: x['Year'].astype(int),
            Internet=lambda x: x.groupby('Country Code')['Internet Users (%)']
            .transform(lambda s: s.astype(float).interpolate(method='linear'))
        )
        .dropna(subset=['Internet Users (%)'])
    )
    return df_internet_cleaned

def process_crime_data():
    df_crime = pd.read_excel('DATA/country_yearly_incident_counts.xlsx', header=None)
    df_crime.columns = ['Country Code'] + years

    # Reshape to long format and filter years 
    df_crime_long = pd.melt(
        df_crime,
        id_vars=['Country Code'],
        value_vars=years,
        var_name='Year',
        value_name='Cyber_Crime_Count'
    ).query(f'{analysis_years[0]} <= Year <= {analysis_years[1]}')

    # Clean and interpolate
    df_crime_cleaned = (
        df_crime_long.groupby('Country Code')
        .filter(lambda x: x['Cyber_Crime_Count'].isnull().mean() <= missing_threshold)
        .assign(
            Year=lambda x: x['Year'].astype(int),
            Cyber_Crime_Count=lambda x: x.groupby('Country Code')['Cyber_Crime_Count']
            .transform(lambda s: s.astype(float).interpolate(method='linear'))
        )
        .dropna(subset=['Cyber_Crime_Count'])
    )
    return df_crime_cleaned

def analyze_data(df_internet, df_crime):
    # Merge datasets
    df_merged = pd.merge(
        df_internet,
        df_crime,
        on=['Country Code', 'Year'],
        how='inner'
    )
    
    # Calculate log transformation for crime count
    df_merged['log_crime'] = np.log1p(df_merged['Cyber_Crime_Count'])
    
    try:
        # Calculate correlation with scientific notation for p-value
        rho, p = spearmanr(df_merged['Internet'], df_merged['Cyber_Crime_Count'])
        print(f"Spearman Correlation: {rho:.6f}, p-value: {p:.2e}")
        
        if p < 1e-10:
            print("Note: p-value is extremely small (p < 1e-10), indicating strong statistical significance")
            
    except Exception as e:
        print(f"Error calculating correlation: {e}")
        return df_merged, None, None
    
    return df_merged, rho, p

def visualize_data(df, rho, p):
    # Create output directory and timestamp
    output_dir = 'output/plots'
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Create single figure with 1x3 layout
    plt.figure(figsize=(20, 6), dpi=120)

    # 1. Internet Users vs Crime Scatter Plot
    plt.subplot(131)
    sns.regplot(
        data=df,
        x='Internet',
        y='log_crime',
        scatter_kws={'alpha': 0.6, 's': 40, 'color': '#2c7bb6'},
        line_kws={'color': '#d7191c', 'lw': 2}
    )
    plt.title(f'Internet Users vs Cyber Crime (ρ={rho:.2f}, p={p:.2e})', fontsize=12)
    plt.xlabel('Internet Users (%)')
    plt.ylabel('Log Cyber Crime Count (log(1+x))')

    # 2. Time Series Plot
    plt.subplot(132)
    yearly_crimes = df.groupby('Year')['log_crime'].mean()
    plt.plot(yearly_crimes.index, yearly_crimes.values, 'o-', color='#2c7bb6')
    plt.title('Average Log Cyber Crimes by Year', fontsize=12)
    plt.xlabel('Year')
    plt.ylabel('Log Average Crime Count')

    # 3. Internet Users Distribution
    plt.subplot(133)
    sns.histplot(data=df, x='Internet', kde=True)
    plt.title('Internet Users Distribution', fontsize=12)
    plt.xlabel('Internet Users (%)')

    # Save and display
    plt.tight_layout()
    plt.savefig(
        f'{output_dir}/internet_crime_analysis_{timestamp}.png',
        dpi=300,
        bbox_inches='tight',
        facecolor='white',
        edgecolor='none'
    )
    plt.show()

if __name__ == "__main__":
    df_internet = process_internet_data()
    df_crime = process_crime_data()
    df_merged, rho, p = analyze_data(df_internet, df_crime)
    visualize_data(df_merged, rho, p)