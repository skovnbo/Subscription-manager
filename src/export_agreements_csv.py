def write_agreements_csv(agreements, filename="all_agreements.csv"):
    rows = []
    for ag in agreements:
        rows.append({
            "AgreementGuid": ag.get("msdyn_agreementid", ""),
            "AgreementNumber": ag.get("msdyn_agreementnumber", ""),
            "AgreementName": ag.get("msdyn_name", ""),
            "AgreementType": ag.get("_skov_agreementtype_value", ""),
            "FarmID": ag.get("skov_farmid", "")
        })
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["AgreementGuid", "AgreementNumber", "AgreementName", "AgreementType", "FarmID"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"All agreements written to {filename}")


import os
import requests
import csv
from dotenv import load_dotenv
from pathlib import Path
dotenv_path = Path(__file__).resolve().parents[2] / '.env'
load_dotenv(dotenv_path=dotenv_path)

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
TENANT_ID = os.getenv("TENANT_ID")
RESOURCEPROD = os.getenv("RESOURCEPROD")

# OAuth2 token endpoint for Azure AD
TOKEN_URL = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
# Agreements API endpoint
AGREEMENTS_API = f"{RESOURCEPROD}/api/data/v9.2/msdyn_agreements"

def get_access_token():
    data = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials',
        'scope': f'{RESOURCEPROD}/.default'
    }
    response = requests.post(TOKEN_URL, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def fetch_agreements(token):
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    response = requests.get(AGREEMENTS_API, headers=headers)
    response.raise_for_status()
    return response.json().get('value', [])

if __name__ == "__main__":
    token = get_access_token()
    agreements = fetch_agreements(token)
    write_agreements_csv(agreements)
