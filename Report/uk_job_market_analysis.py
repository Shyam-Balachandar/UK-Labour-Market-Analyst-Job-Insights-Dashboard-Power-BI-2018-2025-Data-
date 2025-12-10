# Query Adzuna API
# The Adzuna API provides programmatic access to Adzuna’s job-search platform. In simple terms, 
# it lets developers pull real-time job-market data into their own apps, websites, dashboards, or research projects.
#%%
import requests
import time

APP_ID = "ca4e041d"
APP_KEY = "8247d6b4d47ae8dbbfcba18b5c4ea1e7"

roles = [
    "business analyst",
    "data analyst",
    "insight analyst",
    "junior analyst",
    "graduate analyst"
]

all_results = []

for role in roles:
    print(f"\n🔍 Fetching role: {role}")

    for page in range(1, 11):  # fetch pages 1 → 10
        url = f"https://api.adzuna.com/v1/api/jobs/gb/search/{page}"
        
        params = {
            "app_id": APP_ID,
            "app_key": APP_KEY,
            "results_per_page": 50,
            "what": role,
            "where": "UK",
            "content-type": "application/json"
        }

        response = requests.get(url, params=params)

        if response.status_code != 200:
            print("❌ Error fetching page:", page)
            break

        data = response.json()

        # If no results, stop
        if "results" not in data or len(data["results"]) == 0:
            print("No more results.")
            break

        print(f"  Page {page}: {len(data['results'])} results")

        # Flatten JSON into table rows
        for item in data["results"]:
            row = {
                "role_search": role,
                "title": item.get("title"),
                "company": item.get("company", {}).get("display_name"),
                "location": item.get("location", {}).get("display_name"),
                "area": item.get("location", {}).get("area"),
                "created": item.get("created"),
                "description": item.get("description"),
                "category": item.get("category", {}).get("label"),
                "contract_type": item.get("contract_type"),
                "contract_time": item.get("contract_time"),
                "salary_min": item.get("salary_min"),
                "salary_max": item.get("salary_max"),
                "redirect_url": item.get("redirect_url")
            }
            all_results.append(row)

        time.sleep(0.5)  # respect API rate limits

df = pd.DataFrame(all_results)
df.to_csv("uk_job_ads_raw.csv", index=False)

print("\nSaved → uk_job_ads_raw.csv")
print(df.head())

# Load the CSV
#%%
import pandas as pd
df = pd.read_csv(r"D:\BA Notes\Projects\UK Job Market Analysis\uk_job_ads_raw.csv")

# %%
# Extract region and city
import ast

import numpy as np

def parse_area(area_str):
    """
    area_str example:
    "['UK']"
    "['UK', 'North West England', 'Merseyside', 'Liverpool']"
    """
    if pd.isna(area_str):
        return np.nan, np.nan, np.nan  # country, region, city

    try:
        area_list = ast.literal_eval(area_str)  # turn string -> Python list
        if not isinstance(area_list, list) or len(area_list) == 0:
            return np.nan, np.nan, np.nan

        country = area_list[0]  # usually 'UK'

        # region: second element if it exists, else same as country
        region = area_list[1] if len(area_list) > 1 else country

        # city: last element if list length >= 2, else None
        city = area_list[-1] if len(area_list) > 1 else np.nan

        return country, region, city

    except (ValueError, SyntaxError):
        # if the text is weird and can't be parsed
        return np.nan, np.nan, np.nan


df[["country", "region", "city"]] = df["area"].apply(
    lambda x: pd.Series(parse_area(x))
)
country_counts = df["country"].value_counts()
print(country_counts)
region_counts = df["region"].value_counts()
print(region_counts)
city_counts = df["city"].value_counts()
print(city_counts)


# %%
# Extract skills
skills = ["sql", "excel", "python", "r programming", "power bi", "tableau", "azure", "aws"]

for s in skills:
    df[f"has_{s.replace(' ','_')}"] = df["description"].str.lower().str.contains(s)

# %%
# Calculate average salary
df["salary_avg"] = df[["salary_min","salary_max"]].mean(axis=1)

# %%
# Extract years of experience (regex)
import re

def get_exp(text):
    if isinstance(text, str):
        match = re.search(r'(\d+)\+?\s*years?', text.lower())
        if match:
            return int(match.group(1))
    return None

df["years_exp"] = df["description"].apply(get_exp)

# %%
# Save clean version
df.to_csv("uk_job_ads_clean.csv", index=False)

# %%
