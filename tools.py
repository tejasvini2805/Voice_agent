from langchain_core.tools import tool
import os
import csv

# 1. Mock Database (Telangana Schemes)
SCHEMES = [
    {
        "name": "Rythu Bandhu",
        "min_age": 18,
        "occupation": "farmer",
        "benefit": "Rs 5000 per acre"
    },
    {
        "name": "Kalyana Lakshmi",
        "min_age": 18,
        "gender": "female",
        "max_income": 200000,
        "benefit": "Financial assistance for marriage"
    },
    {
        "name": "Aarogyasri",
        "max_income": 500000,
        "benefit": "Free health coverage up to 5 Lakhs"
    }
]

# 2. Define the Tool function
@tool
def check_eligibility(age: int, income: int, occupation: str, gender: str) -> str:
    """
    Checks eligibility for government schemes.
    Args:
        age: User's age in years.
        income: User's annual family income in Rupees.
        occupation: User's job (e.g., farmer, student, unemployed).
        gender: male or female.
    """
    eligible_schemes = []
    
    # Logic to filter schemes
    for scheme in SCHEMES:
        if age < scheme.get("min_age", 0):
            continue
        if income > scheme.get("max_income", float('inf')):
            continue
        if "occupation" in scheme and scheme["occupation"] != occupation:
            continue
        if "gender" in scheme and scheme["gender"] != gender:
            continue
            
        eligible_schemes.append(f"{scheme['name']} ({scheme['benefit']})")
    
    if not eligible_schemes:
        return "No schemes found matching these criteria."
    
    return f"Eligible Schemes found: {', '.join(eligible_schemes)}"
from langchain_core.tools import tool
import random

# Existing tool...
# (Keep your existing SCHEMES list and check_eligibility function here exactly as they are)

# --- NEW TOOL ---
@tool
def apply_for_scheme(scheme_name: str, applicant_name: str, age: int) -> str:
    """
    Applies for a scheme and SAVES it to a file.
    Args:
        scheme_name: Name of the scheme (e.g., Rythu Bandhu)
        applicant_name: Name of the user (e.g., 'Farmer')
        age: Age of the applicant
    """
    # 1. Generate Fake ID
    app_id = f"TS-{random.randint(1000, 9999)}-2025"
    
    # 2. SAVE to a real file (The "Proof")
    file_exists = os.path.isfile("applications.csv")
    
    with open("applications.csv", mode="a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        # Write header if new file
        if not file_exists:
            writer.writerow(["App_ID", "Scheme", "Applicant_Name", "Age", "Status"])
        
        # Write the Data
        writer.writerow([app_id, scheme_name, applicant_name, age, "Submitted"])
    
    return f"SUCCESS: Application {app_id} saved to database. SMS sent."