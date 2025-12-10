# UK Labour Market & Analyst Job Insights  
### **A Power BI Analytics Project using ONS Data + Live Job Ads**

This project analyses **UK labour market dynamics**, **industry vacancies**, **unemployment trends**, and **real analyst job postings** to understand hiring patterns, salary expectations, and role demand.  
It combines **official ONS datasets** with a **cleaned job-ads dataset** to deliver insights through an interactive **Power BI dashboard**.

> ⚡ Built as part of my Business Analytics portfolio — designed for recruiters, hiring managers, and anyone curious about the UK job market.  
> 🤡 Includes occasional absurdity to keep analytics from becoming dangerously serious.

---

## 📊 **Project Components**
This project contains the following:

### **1. Labour Market Vacancy Trends (ONS – VACS & JOBS datasets)**
- 3-month average vacancy trends  
- Single-month vacancy breakdowns  
- Industry-wise vacancy rate  
- YoY vacancy growth/decline  
- Unemployment vs. vacancies (market tension)

### **2. Analyst Job Ads Dataset (Cleaned CSV)**
- Data Analyst  
- Business Analyst  
- Insight Analyst  
- Junior Analyst  
- Graduate Analyst  

Metrics include:
- Job count (last 30 days)
- Region-wise job distribution
- Salary benchmarking
- Experience requirement cleaning & averaging

### **3. Power BI Interactive Dashboard**
Pages included:
1. **Labour Market Overview**
2. **Industry Vacancy Deep Dive**
3. **Analyst Job Market Insights**
4. **Regional Hiring Distribution**

---

## 🧠 **Key Insights**

### 🔹 **Industry Insights**
- Human Health & Social Work has the highest 3-month vacancy volume.  
- Mining & Quarrying continues its legendary streak of being last… always.

### 🔹 **Analyst Job Insights**
- Data Analyst & Insight Analyst roles show similar demand.  
- Business Analyst roles offer slightly higher salary expectations.  
- Graduate roles pay least but require the least experience — shocker.

### 🔹 **Regional Job Demand**
> *London is not actually carrying the UK job market like a tired parent carrying a stubborn toddler — that honour goes to **South East**, which has the highest analyst job postings.*

### 🔹 **Experience Levels (Cleaned)**
- Insight Analyst → ~8.6 years  
- Data Analyst → ~6.8 years  
- Business Analyst → ~4.9 years  
- Junior Analyst → ~5.9 years  
- Graduate Analyst → ~0–1 year  

---

## 🛠️ **Data Sources**

### **ONS (Office for National Statistics)**
| File | Purpose |
|------|---------|
| **VACS01** | UK total vacancies + unemployment over time |
| **VACS02** | Vacancies by industry (SIC07) |
| **X06** | Monthly vacancies by industry *and* firm size |
| **JOBS02** | Workforce jobs by industry |
| **JOBS05** | Workforce jobs by region & industry |

### **Job Ads Dataset**
`uk_job_ads_clean.csv`  
- Contains analyst job postings scraped from multiple job boards  
- Cleaned role names, salaries, regions, and experience levels  
- Last 30-days snapshot

---

## 🧹 **Data Cleaning & Transformations**
### Done in Power Query + DAX

- Standardized role names  
- Extracted numeric years of experience (regex cleaning)  
- Removed blanks and malformed entries  
- Created a consistent **Dim_Date** table for time intelligence  
- Added calculated columns for:
  - 3-month rolling average vacancies  
  - YoY vacancy change %  
  - Latest quarter filter (`Is Latest Quarter = 1`)  
  - Salary normalization  

---

## 🔢 **DAX Highlights (Key Measures)**

```DAX
Job Ads = COUNTROWS(JobAds)

Vacancies_3M = 
AVERAGEX(
    DATESINPERIOD(Dim_Date[Date], MAX(Dim_Date[Date]), -3, MONTH),
    SUM(Vacancies[Vacancies_1M])
)

Vacancies_3M_YoY_Change% =
VAR Curr = [Vacancies_3M]
VAR Prev =
    CALCULATE(
        [Vacancies_3M],
        DATEADD(Dim_Date[Date], -1, YEAR)
    )
RETURN DIVIDE(Curr - Prev, Prev)
```
---

## ⚙️ **How to Use This Project**
> Prerequisites

> Install Power BI Desktop

> Download this repository

Steps

Open the Power BI file:
> UK_Labour_Market_Analyst_Insights.pbix

> Ensure all datasets (CSV/XLSX) are in the correct folder.

> Refresh the report to load updated data.

> Interact with slicers and visuals to explore insights.

---

## 🧩 **Data Model Overview**

> Dim_Date – full calendar table

> Dim_Industry – harmonized SIC07 industry names

> Fact_Vacancies – monthly & quarterly vacancy data

> Fact_Unemployment – labour supply

> Fact_JobAds – analyst job ads dataset

Relationships:

> Date ↔ Vacancies

> Industry ↔ Vacancies / Job Ads / Workforce Jobs

> Region ↔ Job Ads / Workforce Jobs

---

## 🚧 **Current Limitations**

> Analyst roles only — broader job families (engineering, finance, tech, etc.) not yet included.

> Job ads dataset covers only the most recent period.

> Salary & experience depend on postings that explicitly list them.

> Vacancy data is aggregated monthly or quarterly, limiting granularity.

> Demand/supply mismatch interpretations require caution.

---

## 🎯 **Who Is This For?**

> Job seekers analysing career opportunities

> Business analysts and workforce planners

> Recruiters and HR professionals

> Students building their analytics portfolio

> Anyone curious about UK labour trends

---

## 🏁 **Conclusion**

This dashboard blends official ONS data with real job market signals to help understand the UK employment landscape.
It offers both high-level trends and deep insights into Analyst-specific opportunities - with more job roles to be added soon.
