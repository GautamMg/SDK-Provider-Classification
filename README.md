# SDK Provider Classification

## Overview
This project focuses on classifying SDK providers into three distinct types:
1. **Platform Providers** (e.g., Apple).
2. **Developers** (SDKs created by app developers).
3. **Non-Developers** (SDKs not provided by developers).

Using two data files, the script performs string matching and cross-referencing to determine the appropriate classification for each SDK.

---

## Features
- Encodes SDK providers as either **Platform**, **Developer**, or **Non-Developer**.
- Uses string matching between the `sdk_overview` and `ios_developers_apps` datasets to identify developer-associated SDKs.
- Handles case normalization and exact string comparisons for robust matching.

---

## Input Data
1. **`sdk_overview_20241020.csv`**
   - Contains SDK metadata, including `company` and `description` fields.
   - Used to identify whether the provider is **Apple** or associated with developers.

2. **`ios_developers_apps_20241029.csv`**
   - Contains app and developer data, including `developer` and `title` fields.
   - Cross-referenced with the `sdk_overview` file for matching.

---

## Output
- A CSV file with an added column, `sdk_provider`, indicating one of the following values:
  1. `Platform` (e.g., Apple).
  2. `Developer`.
  3. `Non-Developer`.

---

## Steps Followed
### 1. Identify Platform Providers
- Extract SDKs with `company` containing **"Apple"**.
- Encode these rows as `sdk_provider = "Platform"`.

### 2. Developer vs. Non-Developer Classification
- For SDKs not provided by Apple:
  - Perform case-normalized string matching between:
    - `developer` (`ios_developers_apps.csv`) and `company` (`sdk_overview.csv`).
    - `developer` (`ios_developers_apps.csv`) and `description` (`sdk_overview.csv`).
    - `title` (`ios_developers_apps.csv`) and `description` (`sdk_overview.csv`).
  - If any match is found, encode `sdk_provider = "Developer"`.
  - If no match is found, encode `sdk_provider = "Non-Developer"`.

---

## Requirements
- **Python Version**: 3.8 or higher
- **Libraries**:
  - `pandas`: For data manipulation and analysis.
  - Additional dependencies can be listed in `requirements.txt`.

---

## How to Run
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/sdk-provider-classification.git
