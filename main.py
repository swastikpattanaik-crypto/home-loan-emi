# homeloan_suggestions
# Simple Home Loan Advisor

import math

def approximate_emi(principal, annual_rate_pct, years):
    if principal <= 0 or years <= 0:
        return 0.0
    r = annual_rate_pct / 100.0 / 12.0
    n = int(years * 12)
    emi = (principal * r * (1 + r) ** n) / ((1 + r) ** n - 1)
    return emi

def compute_simple_score(data):
    score = 100.0
    c = data['cibil']

    if c >= 800: score += 75
    elif c >= 750: score += 65
    elif c >= 700: score += 55
    elif c >= 650: score += 30
    elif c >= 600: score += 20
    elif c >=550 :  score += 10
    elif c >=500 :  score += 0
    elif c >=400 :  score -= 15
    elif c >=300 :  score -= 35
    else: score -= 70

    monthly_income = data['income']
    existing = data['existing_debt']
    loan_emi_est = approximate_emi(data['loan_amount'], 9.5, data['tenure_years'])
    projected = existing + loan_emi_est
    dti = (projected / monthly_income) if monthly_income > 0 else 10.0

    if dti <= 0.15: score += 50
    elif dti <= 0.25: score += 35
    elif dti <= 0.30: score += 25
    elif dti <= 0.45: score += 10
    elif dti <= 0.60: score += 5
    elif dti <= 0.75: score -= 50
    else: score -= 200

    yrs = data['employment_years']
    if yrs >= 25: score += 75
    elif yrs >= 20: score += 70
    elif yrs >= 15: score += 60
    elif yrs >= 10: score += 25
    elif yrs >= 5: score += 10
    elif yrs >= 3: score -=5
    else: score -= 30

    t = data['income_trend']
    if t == 'increasing': score += 10
    elif t == 'stable': score += 0
    elif t == 'decreasing': score -= 15

    if data['residence'] == 'urban': score += 10
    else: score += 5

    age = data['age']
    if age < 21: score -= 50
    elif age >= 61: score += 60
    elif age >= 51: score += 50
    elif age >= 41: score += 45
    elif age >= 31: score += 35
    elif age >= 21: score += 30

    score = max(0, min(score, 270))
    return round(score, 1)

def recommend(score, data):
    loan = data['loan_amount']
    residence = data['residence']
    if score >= 210:
        lender = "Government Bank"
        base = 7.5; spread = 1.0
    elif score >= 175:
        lender = "Private Bank"
        base = 8.5; spread = 1.5
    elif score >= 150:
        lender = "Private Bank / Good NBFC"
        base = 9.5; spread = 2.0
    elif score >= 125:
        lender = "NBFC/good NBFC"
        base = 10.0; spread = 2.5
    elif score >= 100:
        lender = "NBFC"
        base = 11.5; spread = 3.0
    elif score >= 75:
        lender = "NBFC"
        base = 13.0; spread = 2.5
    else:
        return "Rejected", (0.0, 0.0)

    if residence != 'urban': base += 0.3
    if loan >= 10_000_000: base += 0.5
    elif loan >= 5_000_000: base += 0.25

    low = round(base, 2); high = round(base + spread, 2)
    return lender, (low, high)

def format_currency(x):
    try:
        return "₹" + f"{int(round(x)):,}"
    except:
        return str(x)

def get_int(prompt, default):
    try:
        s = input(prompt).strip()
        return int(s) if s != "" else default
    except:
        return default

def get_float(prompt, default):
    try:
        s = input(prompt).strip()
        return float(s) if s != "" else default
    except:
        return default

def main():
    print("==< Home Loan Advisor >==")
    name = input("Name: ").strip() or "Applicant"

    cibil = get_int("CIBIL score (300-900): ", 700)
    residence = input("Residence (urban/rural): ").strip().lower() or "urban"
    income = get_float("Monthly net income (INR): ", 30000.0)
    income_trend = input("Income trend (increasing/stable/decreasing): ").strip().lower() or "stable"
    employment_years = get_float("Years in current job/business: ", 1.0)
    existing_debt = get_float("Existing monthly EMI / debt (INR): ", 0.0)
    loan_amount = get_float("Desired loan amount (INR): ", 2000000.0)
    tenure_years = get_float("Tenure in years: ", 20.0)
    property_type = input("Property type (new/resale): ").strip().lower() or "new"
    age = get_int("Age: ", 30)

    data = {
        'name': name, 'cibil': cibil, 'residence': residence, 'income': income,
        'income_trend': income_trend, 'employment_years': employment_years,
        'existing_debt': existing_debt, 'loan_amount': loan_amount,
        'tenure_years': tenure_years, 'property_type': property_type, 'age': age
    }

    score = compute_simple_score(data)
    lender, (r_low, r_high) = recommend(score, data)
    rep_rate = (r_low + r_high) / 2.0
    emi = approximate_emi(loan_amount, rep_rate, tenure_years)
    total_paid = emi * tenure_years * 12
    total_interest = total_paid - loan_amount

    if score >= 210: chance = "Very High"
    elif score >= 150: chance = "High"
    elif score >= 110: chance = "Moderate"
    elif score >= 75: chance = "Low"
    else: chance = "Very Low"

    print("\n--- Recommendation ---")
    print(f"Applicant: {name}")
    print(f"Heuristic score: {score} / 380")
    print(f"Approval chance: {chance}")
    print(f"Recommended lender type: {lender}")
    print(f"Estimated interest rate: {r_low}% - {r_high}% (representative used: {rep_rate:.2f}%))")
    print(f"Loan amount: {format_currency(loan_amount)} | Tenure: {tenure_years} years")
    print(f"Estimated EMI: {format_currency(emi)} per month")
    print(f"Total repayable: {format_currency(total_paid)} (Interest ≈ {format_currency(total_interest)})\n")

    print("Simple repayment tips:")
    print("1> Shorter tenure reduces total interest but increases EMI.")
    print("2> If your lender allows prepayment without big penalty, prepay when you have extra money.")
    print("3> Normally if you pay 1-2 months extra EMI per year i.e 13-14 emis instead of 12 total interest drops a lot.")
    print("4> Increase EMI by 5% yearly if possible,it will significantly decrease your total intrest")
    print("5> Improve CIBIL and reduce debts for lower interest.")
    print("6> Consider co-applicant or guarantor if score is low.")
    print("\nNote: This is just a prediction. Actual lenders/financial institutions follow detailed rules.")

if _name== 'main_':
    main()
