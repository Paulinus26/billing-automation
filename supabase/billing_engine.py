# The "Accountant" Script
def calculate_bill(usage, limit):
    price_per_gb = 0.50
    if usage > limit:
        overage = usage - limit
        return round(overage * price_per_gb, 2)
    return 0.0

# Example: User used 150GB with a 100GB limit
bill_total = calculate_bill(150, 100)
print(f"Final Charge: ${bill_total}") # Result: $25.0