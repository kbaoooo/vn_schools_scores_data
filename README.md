# 📚 Vietnam University Admission Scores Data (2021-2025)

A robust Python-based crawler designed to systematically extract and organize historical university admission scores from the Tuyensinh247 platform.

## 🌟 Features

- **Consolidated Logic**: A single entry point (`craw.py`) for all operations.
- **API-Driven**: Uses internal search and score APIs for maximum reliability and clean data.
- **Historical Depth**: Supports full data extraction for years **2021, 2022, 2023, 2024, and 2025**.
- **Organized Storage**: Data is automatically siloed into school-specific folders for easy browsing and analysis.
- **Smart Skipping**: Automatically detects existing files and only crawls missing data, making it safe to resume.

## 📂 Project Structure

```text
.
├── craw.py                 # Main crawler script
├── README.md               # Project documentation
└── craw-data/
    ├── schools_with_ids.json # Master school list with IDs
    └── scores/             # Historical admission scores
        └── [SCHOOL_CODE]/  # e.g., BKA, KHA, NTH
            ├── 2021.json
            ├── 2022.json
            └── ...
```

## 🚀 Getting Started

### 1. Installation

Ensure you have Python 3 installed. This project uses the `requests` library.

```bash
pip install requests
```

### 2. Update School Metadata

To refresh the list of schools and their unique IDs from the API:

```bash
python3 craw.py --schools
```

### 3. Crawl Admission Scores

To crawl all missing scores for the default range (2021-2025):

```bash
python3 craw.py --scores
```

**Advanced Options:**

- **Crawl specific years:**
  ```bash
  python3 craw.py --scores --years 2024 2025
  ```
- **Limit the number of schools (for testing):**
  ```bash
  python3 craw.py --scores --limit 10
  ```
- **Adjust delay to prevent rate-limiting:**
  ```bash
  python3 craw.py --scores --delay 2.0
  ```

## 📊 Data Format

The scores are saved as JSON files following this structure:

```json
{
  "success": true,
  "data": [
    {
      "school_id": 357,
      "code": "7220201",
      "name": "Ngôn ngữ Anh",
      "block": "A01;D01;D09;D10",
      "mark": 37.3,
      "year": 2021,
      "admission_name": "Điểm thi THPT"
    },
    ...
  ]
}
```

## ⚖️ License
This project is for educational and research purposes.
