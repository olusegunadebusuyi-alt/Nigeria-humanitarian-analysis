
# Nigeria Humanitarian Needs Analysis 2017–2026
**Author:** Segun Adebusuyi  
**Data source:** UN OCHA Humanitarian Needs Overview (HNO) via HDX  
**Tools:** Python, pandas, matplotlib

## What this project does
Analyses 10 years of UN humanitarian data covering Northeast Nigeria — 
Adamawa, Borno and Yobe states — to quantify the scale, geography and 
trend of humanitarian need from 2017 to 2026.

## Key findings
- **2024 was the worst year on record** — 16M people in need, nearly 
  double 2023's 8.3M, driven by the Alau Dam collapse in October 2024
- **Borno State** consistently accounts for over 50% of total need
- **Fufore LGA** (Adamawa) had 197,634 people in need in 2023 alone
- By 2026 numbers have fallen to 5.9M — improving but still critical

## Files
| File | Description |
|------|-------------|
| `nigeria_humanitarian_analysis.py` | Full analysis code |
| `nigeria_humanitarian_lga_2019_2024.csv` | Clean LGA-level dataset |
| `nigeria_humanitarian_national_trend.csv` | National totals 2018–2026 |
| `chart1_national_trend.png` | Annotated trend chart |

## Data limitations
- 2025–2026 files still under development; only national totals used
- Gender disaggregation inconsistent across years
- 2017 data excluded from LGA analysis due to sector double-counting
