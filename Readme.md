HOME LOAN ADVISOR
=================

Project Overview
----------------
This project is a console-based Python program that estimates a user's loan eligibility and provides a basic home-loan recommendation.  
The program takes user inputs such as CIBIL score, income, debt, employment history, age, and loan details, and then generates a heuristic score to predict approval chances.

It also calculates an approximate EMI using standard loan math and displays a possible interest rate range along with repayment tips.

Features
--------
- Menu-less interactive questionnaire  
- Heuristic scoring model based on:
  - CIBIL score
  - Debt-to-income ratio
  - Income trend
  - Employment years
  - Age category
  - Urban/rural residence
- Loan recommendation (Government Bank, Private Bank, NBFC, etc.)
- Estimated interest rate range
- EMI calculation using amortization formula
- Summary report showing score, approval chance, EMI, and total payable amount
- General repayment suggestions

Technologies / Tools Used
-------------------------
- Python 3  
- math module  
- Console interface (no external libraries)

Steps to Install and Run
------------------------
1. Install Python 3 if it is not already installed.  
2. Download the project folder or clone the repository.  
3. Open a terminal inside the folder.  
4. Run the file using:5. Enter the requested details when prompted.

Instructions for Testing
------------------------
- Test different CIBIL scores to observe how the score changes.  
- Try varying income, debt levels, and loan amounts.  
- Enter incorrect or empty values to check default handling.  
- Compare EMI output for different tenures and interest rates.  
- Try urban vs rural residence to observe the rate adjustments.
