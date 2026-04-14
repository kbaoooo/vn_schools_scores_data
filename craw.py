import requests
import json
import time
import os
import argparse
from pathlib import Path

# Configuration
BASE_URL = "https://diemthi.tuyensinh247.com"
SCHOOL_LIST_FILE = "craw-data/schools_with_ids.json"
SCORES_DIR = Path("craw-data/scores")

def crawl_school_list():
    """
    Crawls the school list with IDs from the internal search API.
    """
    url = f"{BASE_URL}/api/school/search?q="
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    print(f"Fetching school list from API: {url}")
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        api_data = response.json()
        
        if not api_data.get("success") or "data" not in api_data:
            print("Error: API response unsuccessful.")
            return

        raw_schools = api_data["data"]
        schools = []

        for item in raw_schools:
            schools.append({
                "school_id": item.get("id"),
                "school_code": item.get("code"),
                "school_name": item.get("name"),
                "school_alias": item.get("alias")
            })

        # Sort schools by name for convenience
        schools.sort(key=lambda x: x['school_name'] if x['school_name'] else "")

        output_dir = Path("craw-data")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Save to the main file used by scores crawler
        with open(SCHOOL_LIST_FILE, "w", encoding="utf-8") as f:
            json.dump({"data": schools}, f, ensure_ascii=False, indent=2)
            
        print(f"Successfully crawled {len(schools)} schools to {SCHOOL_LIST_FILE}")

    except Exception as e:
        print(f"Error fetching school list: {e}")

def crawl_scores(years=None, delay=1.0, subset=None):
    """
    Crawls admission scores using IDs from the internal API.
    """
    if years is None:
        years = [2021, 2022, 2023, 2024, 2025]
    
    method_id = 1  # Điểm thi THPT
    SCORES_DIR.mkdir(parents=True, exist_ok=True)
    
    if not os.path.exists(SCHOOL_LIST_FILE):
        print(f"Error: {SCHOOL_LIST_FILE} not found. Please run --schools first.")
        return
        
    with open(SCHOOL_LIST_FILE, 'r', encoding='utf-8') as f:
        schools_data = json.load(f)
        schools = schools_data.get('data', [])
        
    if subset:
        schools = schools[:subset]
        
    print(f"Processing {len(schools)} schools for years {years}...")
    
    for i, school in enumerate(schools):
        school_id = school.get('school_id')
        school_code = school.get('school_code')
        school_name = school.get('school_name')
        
        if not school_id or not school_code:
            continue
            
        print(f"[{i+1}/{len(schools)}] {school_code} - {school_name}")
        
        for year in years:
            school_dir = SCORES_DIR / school_code
            school_dir.mkdir(parents=True, exist_ok=True)
            output_file = school_dir / f"{year}.json"
            
            if output_file.exists():
                continue
                
            url = f"{BASE_URL}/api/common/cutoff-score?school_id={school_id}&method_id={method_id}&year={year}"
            
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('success') and data.get('data'):
                        with open(output_file, 'w', encoding='utf-8') as out_f:
                            json.dump(data, out_f, indent=2, ensure_ascii=False)
                        print(f"  Year {year}: Success")
                    else:
                        # No data found
                        pass
                else:
                    print(f"  Year {year}: Error {response.status_code}")
                    
            except Exception as e:
                print(f"  Year {year}: Exception {e}")
                
            time.sleep(0.1)
            
        time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description="Data Crawler")
    parser.add_argument("--schools", action="store_true", help="Crawl the school list with IDs from API")
    parser.add_argument("--scores", action="store_true", help="Crawl admission scores from API")
    parser.add_argument("--years", nargs="+", type=int, help="Years to crawl (default: 2021-2025)")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between schools (default: 1.0s)")
    parser.add_argument("--limit", type=int, help="Limit the number of schools to process (for testing)")
    
    args = parser.parse_args()

    if args.schools:
        crawl_school_list()
    
    if args.scores:
        crawl_scores(years=args.years, delay=args.delay, subset=args.limit)
        
    if not args.schools and not args.scores:
        parser.print_help()

if __name__ == "__main__":
    main()
