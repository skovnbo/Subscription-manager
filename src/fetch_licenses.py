import os
import csv
import requests
from dotenv import load_dotenv

# Load environment variables from .env file in the workspace root
from pathlib import Path
dotenv_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=dotenv_path)

LICENSEAPI = os.getenv("LICENSEAPI")
LICENSEAPIUSE = os.getenv("LICENSEAPIUSE")

LICENSEAPIKEY = os.getenv("LICENSEAPIKEY")

def fetch_licenses():
    response = requests.get(LICENSEAPI, auth=(LICENSEAPIUSE, LICENSEAPIKEY))
    response.raise_for_status()
    return response.json()


def write_to_csv(data, filename="licenses.csv"):
    if not data:
        print("No data to write.")
        return
    # If data is a dict with a key containing the list, extract it
    if isinstance(data, dict):
        # Try to find the first list in the dict
        for v in data.values():
            if isinstance(v, list):
                data = v
                break
    keys = data[0].keys() if data else []
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)
    print(f"Data written to {filename}")

# New function to write only farm names to a separate CSV
def write_farms_to_csv(data, filename="farms.csv"):
    if not data:
        print("No data to write for farms.")
        return
    # If data is a dict with a key containing the list, extract it
    if isinstance(data, dict):
        for v in data.values():
            if isinstance(v, list):
                data = v
                break
    # Try to get the farm id and name from each item
    farms = []
    for item in data:
        farm_id = None
        farm_name = None
        for id_key in ["farmId", "FarmId", "id", "Id"]:
            if id_key in item:
                farm_id = item[id_key]
                break
        for name_key in ["farmName", "FarmName", "name", "Name"]:
            if name_key in item:
                farm_name = item[name_key]
                break
        if farm_id is not None or farm_name is not None:
            farms.append({"farmId": farm_id, "farmName": farm_name})
    if not farms:
        print("No farm ids or names found in data.")
        return
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["farmId", "farmName"])
        writer.writeheader()
        writer.writerows(farms)
    print(f"Farm ids and names written to {filename}")

if __name__ == "__main__":
    print(f"LICENSEAPI: {LICENSEAPI}")
    print(f"LICENSEAPIUSE: {LICENSEAPIUSE}")
    print(f"LICENSEAPIKEY: {LICENSEAPIKEY}")
    try:
        licenses = fetch_licenses()
        write_to_csv(licenses)
        write_farms_to_csv(licenses)
    except Exception as e:
        print(f"Error: {e}")
