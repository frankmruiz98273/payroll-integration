import os
import requests
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

# ===================== AXISCARE =====================
def fetch_axiscare_visits():
    url = "https://14165.axiscare.com/api/visits"
    headers = {
        "Accept": "application/json",
        "Authorization": f"Bearer {os.getenv('AXISCARE_API_KEY')}",
        "X-AxisCare-Api-Version": "2023-10-01"
    }
    
    params = {
        "caregiverId": 12345,           # change as needed
        "startDate": os.getenv("START_DATE"),
        "endDate": os.getenv("END_DATE")
    }
    
    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()
    return response.json()

# ===================== CONNECTTEAM =====================
def fetch_connectteam_timeclocks():
    base_url = "https://api.connecteam.com/time-clock/v1/time-clocks"
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {os.getenv('CONNECTTEAM_API_KEY')}"
    }
    
    timeclock_ids = [205, 5937081, 206, 6318023, 204, 5717312, 5609070]  # your IDs
    
    all_data = []
    for tc_id in timeclock_ids:
        url = f"{base_url}/{tc_id}/time-activities"
        params = {
            "startDate": os.getenv("START_DATE"),
            "endDate": os.getenv("END_DATE")
        }
        resp = requests.get(url, headers=headers, params=params)
        if resp.status_code == 200:
            all_data.extend(resp.json())
    
    return all_data

# ===================== MAIN =====================
if __name__ == "__main__":
    print("Fetching data...")
    
    axiscare_data = fetch_axiscare_visits()
    connectteam_data = fetch_connectteam_timeclocks()
    
    # Save to CSV for now
    pd.DataFrame(axiscare_data).to_csv("axiscare_visits.csv", index=False)
    pd.DataFrame(connectteam_data).to_csv("connectteam_time.csv", index=False)
    
    print("✅ Data pulled and saved to CSV files!")