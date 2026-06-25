# ══════════════════════════════════════════════════
# Northeast Nigeria Humanitarian Needs Analysis
# 2018 – 2026
# ══════════════════════════════════════════════════
# Author:  Segun Adebusuyi
# Date:    June 2026
# Purpose: Research — quantifying the scale and
#          geography of humanitarian need in NE Nigeria
#          using UN OCHA HNO data (HDX)
# Data:    Adamawa, Borno, Yobe — LGA level 2019–2024
#          National totals 2018–2026
# ══════════════════════════════════════════════════
"""
Nigeria Northeast Humanitarian Needs Analysis — 2018 to 2026
Data source: UN OCHA Humanitarian Needs Overview (HNO) via HDX
Covers: Adamawa, Borno, Yobe states (LGA level 2019–2024 + national totals)

HOW TO USE:
  Run this in Google Colab. Upload both CSV files when prompted.
  Or paste file paths if running locally.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

plt.style.use('seaborn-v0_8-whitegrid')

# ─────────────────────────────────────────────
# LOAD THE TWO CLEAN FILES YOU DOWNLOADED
# ─────────────────────────────────────────────
lga_df      = pd.read_csv('nigeria_humanitarian_lga_2019_2024.csv')
national_df = pd.read_csv('nigeria_humanitarian_national_trend.csv')

print("LGA dataset shape:", lga_df.shape)
print("Years covered:", sorted(lga_df['year'].unique()))
print("States:", sorted(lga_df['state'].unique()))
print("\nNational trend:\n", national_df.to_string(index=False))


# ─────────────────────────────────────────────
# EDA — always first
# ─────────────────────────────────────────────
print("\n--- Missing values ---")
print(lga_df.isnull().sum())

print("\n--- People in Need summary stats ---")
print(lga_df.groupby('year')['pin_total'].describe())


# ─────────────────────────────────────────────
# QUESTION 1: How has the overall crisis changed 2018–2026?
# ─────────────────────────────────────────────
fig, ax = plt.subplots(figsize=(10, 4))

colors = ['#f38ba8' if y == 2024 else '#89b4fa' for y in national_df['year']]
bars = ax.bar(national_df['year'], national_df['pin_total'] / 1e6, color=colors, width=0.7)

# Annotate the dam collapse
ax.annotate('Alau Dam collapse\nOct 2024',
            xy=(2024, 16), xytext=(2022.2, 14.5),
            arrowprops=dict(arrowstyle='->', color='#f38ba8'),
            fontsize=9, color='#f38ba8')

# Annotate each bar
for bar, val in zip(bars, national_df['pin_total']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1,
            f'{val/1e6:.1f}M', ha='center', va='bottom', fontsize=9, fontweight='bold')

ax.set_title(
    'Northeast Nigeria: 16M people in need in 2024\n'
    'Analysis by Segun Adebusuyi | Source: UN OCHA HNO via HDX',
    fontsize=11, fontweight='bold', pad=12
)
ax.set_xlabel('Year')
ax.set_ylabel('People in Need (millions)')
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f'{x:.0f}M'))
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart1_national_trend.png', dpi=150, bbox_inches='tight')
plt.show()
print("Finding Q1: 2024 had 16M people in need — nearly double 2023's 8.3M")


# ─────────────────────────────────────────────
# QUESTION 2: Which state drives the crisis?
# ─────────────────────────────────────────────
state_trend = lga_df.groupby(['year','state'])['pin_total'].sum().reset_index()

fig, ax = plt.subplots(figsize=(10, 4))
colors_state = {'Borno': '#f38ba8', 'Adamawa': '#89b4fa', 'Yobe': '#a6e3a1'}
for state, grp in state_trend.groupby('state'):
    ax.plot(grp['year'], grp['pin_total']/1e6,
            marker='o', linewidth=2.5, label=state, color=colors_state[state])

ax.set_title('Borno consistently accounts for over 50% of NorthEast Nigeria humanitarian needs',
             fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('Year')
ax.set_ylabel('People in Need (millions)')
ax.legend(loc='upper left')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart2_state_trend.png', dpi=150, bbox_inches='tight')
plt.show()

borno_share = state_trend[state_trend['state']=='Borno']['pin_total'].mean() / \
              state_trend.groupby('year')['pin_total'].sum().mean() * 100
print(f"Finding Q2: Borno averages {borno_share:.0f}% of total NorthEast Nigeria people in need")


# ─────────────────────────────────────────────
# QUESTION 3: Which LGAs are the most crisis-affected?
# ─────────────────────────────────────────────
# Use 2023 as most recent complete LGA data
lga_2023 = lga_df[lga_df['year']==2023].sort_values('pin_total', ascending=False)
top10 = lga_2023.head(10)

fig, ax = plt.subplots(figsize=(10, 5))
bar_colors = ['#f38ba8' if s == 'Borno' else '#89b4fa' if s == 'Adamawa' else '#a6e3a1'
              for s in top10['state']]
bars = ax.barh(top10['lga'] + ' (' + top10['state'] + ')',
               top10['pin_total'] / 1e6,
               color=bar_colors, height=0.7)

for bar, val in zip(bars, top10['pin_total']):
    ax.text(bar.get_width() + 0.01, bar.get_y() + bar.get_height()/2,
            f'{val/1e3:.0f}k', va='center', fontsize=9)

ax.set_title('Maiduguri and Jere (Borno) have the most people in need — 2023',
             fontsize=12, fontweight='bold', pad=12)
ax.set_xlabel('People in Need (millions)')
ax.invert_yaxis()
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('chart3_top_lgas.png', dpi=150, bbox_inches='tight')
plt.show()
print(f"Finding Q3: Top LGA is {top10.iloc[0]['lga']} ({top10.iloc[0]['state']}) "
      f"with {top10.iloc[0]['pin_total']:,.0f} people in need in 2023")


# ─────────────────────────────────────────────
# QUESTION 4: LGA-level change 2019 → 2023
# ─────────────────────────────────────────────
pivot = lga_df[lga_df['year'].isin([2019,2023])].pivot_table(
    index=['state','lga'], columns='year', values='pin_total').reset_index()
pivot.columns = ['state','lga','pin_2019','pin_2023']
pivot = pivot.dropna()
pivot['pct_change'] = ((pivot['pin_2023'] - pivot['pin_2019']) / pivot['pin_2019'] * 100).round(1)

print("\nFinding Q4: Biggest increases 2019 → 2023")
print(pivot.sort_values('pct_change', ascending=False).head(5)[
    ['state','lga','pin_2019','pin_2023','pct_change']].to_string(index=False))

print("\nFinding Q4: Biggest decreases 2019 → 2023")
print(pivot.sort_values('pct_change').head(5)[
    ['state','lga','pin_2019','pin_2023','pct_change']].to_string(index=False))


# ─────────────────────────────────────────────
# SUMMARY
# ─────────────────────────────────────────────
print("""
══════════════════════════════════════════════════
KEY FINDINGS — Nigeria NE Humanitarian Crisis
══════════════════════════════════════════════════
1. SCALE:  2024 saw 16M people in need — nearly 2× the 8.3M in 2023.
           By 2025 this fell to 7.8M and 5.9M in 2026 (improving).
2. STATE:  Borno drives the crisis — consistently 50%+ of total PiN.
3. LGA:    Maiduguri and Jere LGAs alone account for hundreds of thousands.
4. TREND:  Most LGAs saw increases 2019→2023, with IDPs and returnees
           swelling host community pressure.
5. 2026:   The reduction to 5.9M nationally suggests some recovery,
           but this remains one of Africa's largest humanitarian crises.

RECOMMENDATION:
Resource allocation should prioritise Borno (especially Maiduguri/Jere),
where absolute numbers are highest and historical need most persistent.
══════════════════════════════════════════════════
""")
