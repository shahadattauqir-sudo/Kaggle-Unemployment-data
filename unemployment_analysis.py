"""
TASK 2: Unemployment Analysis with Python
Author: Antigravity AI Data Science Team
Description:
    Comprehensive analysis of unemployment rate data in India representing unemployed people percentage.
    - Data cleaning and preprocessing for both Kaggle datasets
    - Exploratory Data Analysis (EDA) and trend visualization
    - Investigation into the impact of COVID-19 lockdowns on unemployment
    - Rural vs. Urban comparative dynamics
    - Regional (Zone) and geographic disparity analysis
    - Seasonal and temporal pattern identification
    - Economic and social policy recommendations
"""

import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Set style for publication-ready visual aesthetics
sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({
    'font.size': 11,
    'axes.labelsize': 12,
    'axes.titlesize': 14,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11,
    'figure.titlesize': 16,
    'figure.autolayout': True,
    'font.family': 'sans-serif'
})

# Create visualizations output directory
OUTPUT_DIR = "visualizations"
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("=" * 80)
print("             UNEMPLOYMENT ANALYSIS WITH PYTHON - TASK 2")
print("=" * 80)

# ==============================================================================
# 1. DATA LOADING AND CLEANING
# ==============================================================================
print("\n[Step 1] Loading and Cleaning Datasets...")

file1 = "Unemployment in India.csv"
file2 = "Unemployment_Rate_upto_11_2020.csv"

# --- Dataset 1: Unemployment in India.csv (Rural & Urban breakdown: May 2019 - Jun 2020) ---
df_detailed = pd.read_csv(file1)
print(f"Raw shape of '{file1}': {df_detailed.shape}")

# Drop rows where all elements are NaN (trailing empty rows)
df_detailed.dropna(how='all', inplace=True)

# Clean column headers: strip whitespace
df_detailed.columns = df_detailed.columns.str.strip()

# Standardize column names
rename_dict1 = {
    'Region': 'State',
    'Date': 'Date',
    'Frequency': 'Frequency',
    'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
    'Estimated Employed': 'Employed',
    'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
    'Area': 'Area_Type'
}
df_detailed.rename(columns=rename_dict1, inplace=True)

# Clean string columns
df_detailed['State'] = df_detailed['State'].str.strip()
df_detailed['Area_Type'] = df_detailed['Area_Type'].str.strip()
df_detailed['Frequency'] = df_detailed['Frequency'].str.strip()

# Parse Dates
df_detailed['Date'] = pd.to_datetime(df_detailed['Date'].str.strip(), format='%d-%m-%Y')
df_detailed['Year'] = df_detailed['Date'].dt.year
df_detailed['Month'] = df_detailed['Date'].dt.month
df_detailed['Month_Name'] = df_detailed['Date'].dt.strftime('%b %Y')
df_detailed['Year_Month'] = df_detailed['Date'].dt.to_period('M')

# Define COVID-19 pandemic phases for detailed dataset
# Pre-COVID: May 2019 - Feb 2020
# Lockdown Shock: Mar 2020 - May 2020
# Post-Lockdown: Jun 2020 onwards
def categorize_phase(dt):
    if dt < pd.Timestamp('2020-03-01'):
        return 'Pre-Lockdown (May 2019 - Feb 2020)'
    elif dt <= pd.Timestamp('2020-05-31'):
        return 'Lockdown Shock (Mar 2020 - May 2020)'
    else:
        return 'Post-Lockdown Recovery (Jun 2020+)'

df_detailed['Pandemic_Phase'] = df_detailed['Date'].apply(categorize_phase)

print(f"Cleaned shape of '{file1}': {df_detailed.shape}")
print(f"Missing values after cleaning:\n{df_detailed.isnull().sum()}")

# --- Dataset 2: Unemployment_Rate_upto_11_2020.csv (Zone & Coordinates: Jan 2020 - Oct 2020) ---
df_regional = pd.read_csv(file2)
print(f"\nRaw shape of '{file2}': {df_regional.shape}")
df_regional.dropna(how='all', inplace=True)
df_regional.columns = df_regional.columns.str.strip()

rename_dict2 = {
    'Region': 'State',
    'Date': 'Date',
    'Frequency': 'Frequency',
    'Estimated Unemployment Rate (%)': 'Unemployment_Rate',
    'Estimated Employed': 'Employed',
    'Estimated Labour Participation Rate (%)': 'Labour_Participation_Rate',
    'Region.1': 'Zone',
    'longitude': 'Longitude',
    'latitude': 'Latitude'
}
df_regional.rename(columns=rename_dict2, inplace=True)

# Clean string columns
df_regional['State'] = df_regional['State'].str.strip()
df_regional['Zone'] = df_regional['Zone'].str.strip()
df_regional['Frequency'] = df_regional['Frequency'].str.strip()

# Parse Dates
df_regional['Date'] = pd.to_datetime(df_regional['Date'].str.strip(), format='%d-%m-%Y')
df_regional['Year'] = df_regional['Date'].dt.year
df_regional['Month'] = df_regional['Date'].dt.month
df_regional['Month_Name'] = df_regional['Date'].dt.strftime('%b %Y')
df_regional['Year_Month'] = df_regional['Date'].dt.to_period('M')

df_regional['Pandemic_Phase'] = df_regional['Date'].apply(categorize_phase)

print(f"Cleaned shape of '{file2}': {df_regional.shape}")
print(f"Missing values after cleaning:\n{df_regional.isnull().sum()}")

# Save cleaned files for downstream usage
df_detailed.to_csv("cleaned_unemployment_india.csv", index=False)
df_regional.to_csv("cleaned_unemployment_2020.csv", index=False)
print("Saved 'cleaned_unemployment_india.csv' and 'cleaned_unemployment_2020.csv'")

# ==============================================================================
# 2. STATISTICAL SUMMARY & EXPLORATORY METRICS
# ==============================================================================
print("\n" + "=" * 80)
print("[Step 2] Statistical Summary and Baseline Metrics")
print("=" * 80)

print("\n--- Summary Statistics: Unemployment in India (Rural & Urban) ---")
print(df_detailed[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].describe().round(2))

print("\n--- Summary Statistics by Area Type (Rural vs Urban) ---")
area_summary = df_detailed.groupby('Area_Type').agg(
    Avg_Unemployment=('Unemployment_Rate', 'mean'),
    Median_Unemployment=('Unemployment_Rate', 'median'),
    Std_Unemployment=('Unemployment_Rate', 'std'),
    Avg_Employed=('Employed', 'mean'),
    Avg_LPR=('Labour_Participation_Rate', 'mean')
).round(2)
print(area_summary)

print("\n--- Summary Statistics by Pandemic Phase ---")
phase_summary = df_detailed.groupby('Pandemic_Phase').agg(
    Avg_Unemployment=('Unemployment_Rate', 'mean'),
    Max_Unemployment=('Unemployment_Rate', 'max'),
    Avg_Employed=('Employed', 'mean'),
    Avg_LPR=('Labour_Participation_Rate', 'mean')
).round(2)
print(phase_summary)

# ==============================================================================
# 3. COVID-19 IMPACT INVESTIGATION
# ==============================================================================
print("\n" + "=" * 80)
print("[Step 3] COVID-19 Lockdown Shock Investigation")
print("=" * 80)

# Pre-lockdown vs Lockdown comparison per state in df_detailed
pre_covid = df_detailed[df_detailed['Date'] < '2020-03-01'].groupby('State')['Unemployment_Rate'].mean().reset_index()
pre_covid.rename(columns={'Unemployment_Rate': 'Pre_Lockdown_Avg'}, inplace=True)

lockdown = df_detailed[(df_detailed['Date'] >= '2020-03-01') & (df_detailed['Date'] <= '2020-05-31')].groupby('State')['Unemployment_Rate'].mean().reset_index()
lockdown.rename(columns={'Unemployment_Rate': 'Lockdown_Avg'}, inplace=True)

impact_df = pd.merge(pre_covid, lockdown, on='State')
impact_df['Absolute_Increase'] = (impact_df['Lockdown_Avg'] - impact_df['Pre_Lockdown_Avg']).round(2)
impact_df['Percentage_Spike'] = (((impact_df['Lockdown_Avg'] - impact_df['Pre_Lockdown_Avg']) / impact_df['Pre_Lockdown_Avg']) * 100).round(2)
impact_df.sort_values(by='Absolute_Increase', ascending=False, inplace=True)

print("\nTop 10 States with Highest Absolute Increase in Unemployment Rate during Lockdown:")
print(impact_df.head(10).to_string(index=False))

# National employment loss during lockdown shock
pre_emp = df_detailed[df_detailed['Date'] == '2020-02-29']['Employed'].sum()
peak_lockdown_emp = df_detailed[df_detailed['Date'] == '2020-04-30']['Employed'].sum()
emp_drop = pre_emp - peak_lockdown_emp
pct_emp_drop = (emp_drop / pre_emp) * 100
print(f"\nNational Employment Impact (Feb 2020 vs Apr 2020):")
print(f"Total Employed (Feb 2020): {pre_emp:,.0f}")
print(f"Total Employed (Apr 2020 peak shock): {peak_lockdown_emp:,.0f}")
print(f"Estimated Net Jobs Displaced: {emp_drop:,.0f} ({pct_emp_drop:.2f}% contraction)")

# ==============================================================================
# 4. GENERATING PUBLICATION-GRADE VISUALIZATIONS
# ==============================================================================
print("\n" + "=" * 80)
print("[Step 4] Generating Publication-Grade Visualizations...")
print("=" * 80)

# Chart 1: National Unemployment Timeline (May 2019 - Jun 2020)
plt.figure(figsize=(12, 6))
monthly_nat = df_detailed.groupby('Date')['Unemployment_Rate'].mean().reset_index()
plt.plot(monthly_nat['Date'], monthly_nat['Unemployment_Rate'], marker='o', color='#d62728', linewidth=2.5, label='National Average')
plt.axvspan(pd.Timestamp('2020-03-24'), pd.Timestamp('2020-05-31'), color='#ff9896', alpha=0.35, label='National Lockdown Period')
plt.annotate(
    f"April 2020 Peak: {monthly_nat[monthly_nat['Date']=='2020-04-30']['Unemployment_Rate'].values[0]:.2f}%",
    xy=(pd.Timestamp('2020-04-30'), monthly_nat[monthly_nat['Date']=='2020-04-30']['Unemployment_Rate'].values[0]),
    xytext=(pd.Timestamp('2019-10-01'), 22),
    arrowprops=dict(facecolor='black', shrink=0.08, width=1.5, headwidth=8),
    fontsize=11, fontweight='bold', bbox=dict(boxstyle="round,pad=0.4", fc="yellow", alpha=0.6)
)
plt.title("National Unemployment Rate Timeline in India (2019 - 2020)\nHighlighting the Acute COVID-19 Lockdown Shock", fontsize=15, pad=15)
plt.xlabel("Timeline", fontsize=12)
plt.ylabel("Unemployment Rate (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(loc='upper left')
plt.tight_layout()
p1 = os.path.join(OUTPUT_DIR, "01_national_unemployment_trend.png")
plt.savefig(p1, dpi=300)
plt.close()
print(f"-> Generated: {p1}")

# Chart 2: Rural vs Urban Trends Over Time
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=df_detailed,
    x='Date',
    y='Unemployment_Rate',
    hue='Area_Type',
    style='Area_Type',
    markers=True,
    dashes=False,
    palette={'Rural': '#2ca02c', 'Urban': '#1f77b4'},
    linewidth=2.5
)
plt.axvspan(pd.Timestamp('2020-03-24'), pd.Timestamp('2020-05-31'), color='#ff9896', alpha=0.3, label='Lockdown Period')
plt.title("Rural vs. Urban Unemployment Dynamics (May 2019 – June 2020)", fontsize=15, pad=15)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Unemployment Rate (%)", fontsize=12)
plt.legend(title="Sector", loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
p2 = os.path.join(OUTPUT_DIR, "02_rural_vs_urban_trends.png")
plt.savefig(p2, dpi=300)
plt.close()
print(f"-> Generated: {p2}")

# Chart 3: Distribution Boxplot and Violin of Rural vs Urban Rates
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.boxplot(
    data=df_detailed,
    x='Area_Type',
    y='Unemployment_Rate',
    palette={'Rural': '#a1d99b', 'Urban': '#9ecae1'},
    ax=axes[0],
    boxprops=dict(alpha=0.8)
)
axes[0].set_title("Unemployment Rate Distribution: Rural vs. Urban", fontsize=13)
axes[0].set_xlabel("Area Sector")
axes[0].set_ylabel("Unemployment Rate (%)")

sns.violinplot(
    data=df_detailed,
    x='Pandemic_Phase',
    y='Unemployment_Rate',
    hue='Area_Type',
    split=True,
    palette={'Rural': '#2ca02c', 'Urban': '#1f77b4'},
    ax=axes[1],
    inner='quartile'
)
axes[1].set_title("Phase-wise Unemployment Distribution Across Sectors", fontsize=13)
axes[1].set_xlabel("Pandemic Phase")
axes[1].set_ylabel("Unemployment Rate (%)")
axes[1].tick_params(axis='x', rotation=15)
plt.tight_layout()
p3 = os.path.join(OUTPUT_DIR, "03_rural_vs_urban_distribution.png")
plt.savefig(p3, dpi=300)
plt.close()
print(f"-> Generated: {p3}")

# Chart 4: Top 10 Most Affected States (Pre vs Lockdown)
plt.figure(figsize=(12, 7))
top10_impact = impact_df.head(10).sort_values(by='Absolute_Increase', ascending=True)
y_pos = np.arange(len(top10_impact))
bar_width = 0.38

plt.barh(y_pos + bar_width/2, top10_impact['Lockdown_Avg'], height=bar_width, color='#d62728', label='Lockdown Shock (Mar-May 2020)', alpha=0.9)
plt.barh(y_pos - bar_width/2, top10_impact['Pre_Lockdown_Avg'], height=bar_width, color='#1f77b4', label='Pre-Lockdown Baseline (May 2019 - Feb 2020)', alpha=0.85)

for i in range(len(top10_impact)):
    plt.text(top10_impact['Lockdown_Avg'].iloc[i] + 0.8, y_pos[i] + bar_width/2 - 0.1,
             f"+{top10_impact['Absolute_Increase'].iloc[i]:.1f}%", color='#8b0000', fontweight='bold', fontsize=9.5)

plt.yticks(y_pos, top10_impact['State'])
plt.xlabel("Unemployment Rate (%)", fontsize=12)
plt.title("Top 10 Most Impacted States: Baseline vs. Peak Lockdown Unemployment Rate", fontsize=15, pad=15)
plt.legend(loc='lower right')
plt.grid(True, linestyle='--', alpha=0.5, axis='x')
plt.tight_layout()
p4 = os.path.join(OUTPUT_DIR, "04_covid_impact_top_states.png")
plt.savefig(p4, dpi=300)
plt.close()
print(f"-> Generated: {p4}")

# Chart 5: Heatmap of State Unemployment Across 2020 (using df_regional)
plt.figure(figsize=(14, 10))
pivot_state = df_regional.pivot_table(
    index='State',
    columns='Month_Name',
    values='Unemployment_Rate',
    aggfunc='mean'
)
# Order columns chronologically
months_order = [m.strftime('%b %Y') for m in pd.date_range(start='2020-01-01', end='2020-10-31', freq='MS')]
pivot_state = pivot_state.reindex(columns=[m for m in months_order if m in pivot_state.columns])

sns.heatmap(pivot_state, cmap='YlOrRd', annot=True, fmt=".1f", linewidths=0.5, cbar_kws={'label': 'Unemployment Rate (%)'})
plt.title("State-wise Monthly Unemployment Rate Trajectory in 2020\n(Showing Acute Surge in April-May 2020)", fontsize=15, pad=15)
plt.xlabel("Month", fontsize=12)
plt.ylabel("State / Union Territory", fontsize=12)
plt.tight_layout()
p5 = os.path.join(OUTPUT_DIR, "05_state_unemployment_heatmap.png")
plt.savefig(p5, dpi=300)
plt.close()
print(f"-> Generated: {p5}")

# Chart 6: Zone-wise Comparison (North, South, East, West, Northeast)
plt.figure(figsize=(12, 6))
zone_monthly = df_regional.groupby(['Date', 'Zone'])['Unemployment_Rate'].mean().reset_index()
sns.lineplot(data=zone_monthly, x='Date', y='Unemployment_Rate', hue='Zone', marker='o', linewidth=2.5)
plt.axvspan(pd.Timestamp('2020-03-24'), pd.Timestamp('2020-05-31'), color='#ff9896', alpha=0.3, label='Lockdown Shock')
plt.title("Regional Zone Unemployment Trajectories Across 2020", fontsize=15, pad=15)
plt.xlabel("Date", fontsize=12)
plt.ylabel("Average Unemployment Rate (%)", fontsize=12)
plt.legend(title="Zone", loc='upper left')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
p6 = os.path.join(OUTPUT_DIR, "06_zone_wise_comparison.png")
plt.savefig(p6, dpi=300)
plt.close()
print(f"-> Generated: {p6}")

# Chart 7: Labour Participation Rate vs Unemployment Rate
plt.figure(figsize=(10, 6))
sns.scatterplot(
    data=df_detailed,
    x='Labour_Participation_Rate',
    y='Unemployment_Rate',
    hue='Area_Type',
    size='Employed',
    sizes=(30, 250),
    alpha=0.7,
    palette={'Rural': '#2ca02c', 'Urban': '#1f77b4'}
)
# Trendline
sns.regplot(
    data=df_detailed,
    x='Labour_Participation_Rate',
    y='Unemployment_Rate',
    scatter=False,
    color='black',
    line_kws={'linestyle': '--', 'linewidth': 1.8}
)
plt.title("Labour Participation Rate (LPR) vs. Unemployment Rate", fontsize=15, pad=15)
plt.xlabel("Estimated Labour Participation Rate (%)", fontsize=12)
plt.ylabel("Estimated Unemployment Rate (%)", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.5)
plt.tight_layout()
p7 = os.path.join(OUTPUT_DIR, "07_labour_participation_vs_unemployment.png")
plt.savefig(p7, dpi=300)
plt.close()
print(f"-> Generated: {p7}")

# Chart 8: Correlation Heatmap
plt.figure(figsize=(8, 6))
corr = df_detailed[['Unemployment_Rate', 'Employed', 'Labour_Participation_Rate']].corr()
sns.heatmap(corr, annot=True, cmap='coolwarm', vmin=-1, vmax=1, fmt=".3f", linewidths=1.0)
plt.title("Correlation Matrix: Labor Market Metrics", fontsize=14, pad=15)
plt.tight_layout()
p8 = os.path.join(OUTPUT_DIR, "08_correlation_matrix.png")
plt.savefig(p8, dpi=300)
plt.close()
print(f"-> Generated: {p8}")

# Chart 9: Absolute Employment Contraction During Lockdown
plt.figure(figsize=(11, 5.5))
emp_trend = df_detailed.groupby(['Date', 'Area_Type'])['Employed'].sum().reset_index()
# Convert to millions for readability
emp_trend['Employed_Millions'] = emp_trend['Employed'] / 1e6
sns.barplot(data=emp_trend, x='Date', y='Employed_Millions', hue='Area_Type', palette={'Rural': '#74c476', 'Urban': '#6baed6'})
plt.title("Total Employed Population Trend (Millions) - Sector Breakdown", fontsize=15, pad=15)
plt.xlabel("Month", fontsize=12)
plt.ylabel("Employed Population (Millions)", fontsize=12)
plt.xticks(rotation=45, ha='right', ticks=range(len(emp_trend['Date'].unique())), labels=[d.strftime('%b %Y') for d in sorted(emp_trend['Date'].unique())])
plt.legend(title="Sector", loc='lower left')
plt.grid(True, linestyle='--', alpha=0.5, axis='y')
plt.tight_layout()
p9 = os.path.join(OUTPUT_DIR, "09_lockdown_employment_loss.png")
plt.savefig(p9, dpi=300)
plt.close()
print(f"-> Generated: {p9}")

# Chart 10: Geographic Bubble Plot (using Latitude & Longitude from df_regional)
plt.figure(figsize=(10, 8))
lockdown_geo = df_regional[df_regional['Date'] == '2020-04-30'].copy()
plt.scatter(
    lockdown_geo['Longitude'],
    lockdown_geo['Latitude'],
    s=lockdown_geo['Unemployment_Rate'] * 25,
    c=lockdown_geo['Unemployment_Rate'],
    cmap='YlOrRd',
    edgecolors='black',
    alpha=0.8,
    linewidth=1.2
)
cbar = plt.colorbar()
cbar.set_label('Peak Unemployment Rate (%) in April 2020', fontsize=11)

for _, row in lockdown_geo.iterrows():
    if row['Unemployment_Rate'] > 20:
        plt.annotate(
            f"{row['State']}\n({row['Unemployment_Rate']:.1f}%)",
            xy=(row['Longitude'], row['Latitude']),
            xytext=(row['Longitude'] + 0.6, row['Latitude'] + 0.4),
            fontsize=8.5,
            fontweight='semibold',
            bbox=dict(boxstyle="round,pad=0.2", fc="white", alpha=0.7, edgecolor='gray')
        )

plt.title("Geographic Severity of Peak COVID-19 Unemployment (April 2020)\nBubble Size & Color Proportional to Unemployment Rate", fontsize=14, pad=15)
plt.xlabel("Longitude", fontsize=12)
plt.ylabel("Latitude", fontsize=12)
plt.grid(True, linestyle='--', alpha=0.4)
plt.tight_layout()
p10 = os.path.join(OUTPUT_DIR, "10_geospatial_bubble_map.png")
plt.savefig(p10, dpi=300)
plt.close()
print(f"-> Generated: {p10}")

print("\n" + "=" * 80)
print("All 10 Visualizations successfully generated in 'visualizations/' folder.")
print("=" * 80)
