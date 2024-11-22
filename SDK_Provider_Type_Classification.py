import pandas as pd
import re
from tqdm import tqdm

# Add relevant input path name
sdk_overview = pd.read_csv('input/sdk_overview_20241020.csv')
ios_developers_apps = pd.read_csv('input/ios_developers_apps_20241029.csv')

# Function to extract the 'name' field from the 'company' column
def extract_company_name(company_str):
    match = re.search(r"name=['\"]([^'\"]*)['\"]", company_str)
    return match.group(1).lower() if match else 'unknown'

sdk_overview['company_name'] = sdk_overview['company'].astype(str).apply(extract_company_name)

# Converting 'description' to lowercase for classification only
sdk_overview['temp_description'] = sdk_overview['description'].astype(str).str.lower()

# Converting relevant columns in ios_developers_apps to lowercase
ios_developers_apps['developer'] = ios_developers_apps['developer'].astype(str).str.lower()
ios_developers_apps['title'] = ios_developers_apps['title'].astype(str).str.lower()

developer_id_map = ios_developers_apps.set_index('developer')['developer_id'].to_dict()
title_to_developer_id_map = ios_developers_apps.set_index('title')['developer_id'].to_dict()

# Initialising 'sdk_provider' with 'Non-Developer' as default and adding 'developer_id' column
sdk_overview['sdk_provider'] = 'Non-Developer'
sdk_overview['developer_id'] = None
sdk_overview.loc[sdk_overview['company_name'] == 'apple', 'sdk_provider'] = 'Apple'

# Function to determine if an SDK is provided by a Developer with exact word matching
def classify_sdk_provider(row):
    if row['sdk_provider'] == 'Apple':
        return 'Apple', None
    
    company_name = row['company_name']
    description_words = set(row['temp_description'].split())
    
    # Primary Matching: Exact match for developer names in company_name
    if company_name in developer_id_map:
        return 'Developer', developer_id_map[company_name]
    
    # Secondary Matching: Check if any developer name or app title matches exactly as a word in description
    for dev in developer_id_map:
        if dev in description_words:
            return 'Developer', developer_id_map[dev]
    
    for title in title_to_developer_id_map:
        if title in description_words: 
            return 'Developer', title_to_developer_id_map[title]
    
    return 'Non-Developer', None

tqdm.pandas(desc="Classifying SDK providers")
sdk_overview[['sdk_provider', 'developer_id']] = sdk_overview.progress_apply(
    lambda row: pd.Series(classify_sdk_provider(row)), axis=1
)

# Removing the temporary columns, keeping only sdk_provider and developer_id as the new additions
sdk_overview = sdk_overview.drop(columns=['company_name', 'temp_description'])

sdk_overview.to_csv('[relevant output path]', index=False)

provider_counts = sdk_overview['sdk_provider'].value_counts()
print("SDK Provider Counts:")
print(f"Developer: {provider_counts.get('Developer', 0)}")
print(f"Non-Developer: {provider_counts.get('Non-Developer', 0)}")
print(f"Apple: {provider_counts.get('Apple', 0)}")