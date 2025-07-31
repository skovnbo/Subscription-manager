"""
This script matches farms from farms.csv to agreements in Dynamics 365 by correlating:
    - farmId (from farms.csv)
    - skov_farmid (from msdyn_agreements in Dynamics)
The script outputs a report with farmId, farmName, agreement status, and agreement number.
If multiple agreements exist for a skov_farmid, only the first agreement number is shown.
"""
import os
import csv
 
# Read agreements from all_agreements.csv
def read_agreements(filename="all_agreements.csv"):
    agreements = []
    with open(filename, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            agreements.append(row)
    return agreements

# Read farms from CSV
def read_farms(filename="farms.csv"):
    farms = []
    with open(filename, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            farms.append(row)
    return farms

# Match farms to agreements
def match_farms_to_agreements(farms, agreements):
    # Correlate farmId (from farms.csv) to FarmID (from all_agreements.csv)
    farmid_to_agreement = {}
    for ag in agreements:
        raw_farmid = str(ag.get("FarmID", "")).strip().lower()
        agreement_number = ag.get("AgreementNumber", "")
        if raw_farmid:
            if raw_farmid not in farmid_to_agreement:
                farmid_to_agreement[raw_farmid] = agreement_number
    report = []
    for farm in farms:
        lic_farm_id = str(farm.get("farmId", "")).strip().lower()
        lic_farm_name = farm.get("farmName", "")
        agreement_number = farmid_to_agreement.get(lic_farm_id, "")
        has_agreement = bool(agreement_number)
        report.append({
            "LIC_farmId": lic_farm_id,
            "LIC_farmName": lic_farm_name,
            "DYN_agreementNumber": agreement_number,
            "hasAgreement": has_agreement
        })
    return report

# Write report to CSV
def write_report(report, filename="farm_agreement_report.csv"):
    with open(filename, "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["LIC_farmId", "LIC_farmName", "DYN_agreementNumber", "hasAgreement"])
        writer.writeheader()
        writer.writerows(report)
    print(f"Report written to {filename}")

if __name__ == "__main__":
    try:
        agreements = read_agreements()
        farms = read_farms()
        report = match_farms_to_agreements(farms, agreements)
        write_report(report)
        # Output counts
        total_farms = len(farms)
        total_agreements = len(agreements)
        matching = sum(1 for row in report if row["hasAgreement"])
        print(f"Total farms (LIC): {total_farms}")
        print(f"Total agreements (DYN): {total_agreements}")
        print(f"Matching rows: {matching}")
        # Print sample farmIds and FarmIDs for debugging
        print("Sample LIC_farmIds (from farms.csv):")
        print([str(f.get("farmId", "")).strip().lower() for f in farms[:10]])
        print("Sample DYN_FarmIDs (from all_agreements.csv):")
        print([str(a.get("FarmID", "")).strip().lower() for a in agreements[:10]])
        # Print all keys from the first 3 agreement records for inspection
        print("\nKeys in first 3 agreement records:")
        for i, a in enumerate(agreements[:3]):
            print(f"Agreement {i+1} keys: {list(a.keys())}")
        # Print all non-empty FarmID values from agreements
        non_empty_farmids = [str(a.get("FarmID", "")).strip().lower() for a in agreements if str(a.get("FarmID", "")).strip()]
        print(f"\nNon-empty FarmID values in agreements (count: {len(non_empty_farmids)}):")
        print(non_empty_farmids[:20])
    except Exception as e:
        print(f"Error: {e}")
