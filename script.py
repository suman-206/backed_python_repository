import pandas as pd

# Replace 'your_file.csv' with the actual path to your CSV file
csv_file_path = "/home/ttluser/Desktop/input_file.csv"

#import pandas as pd

# Define the Gear 2 lookup table
# gear_2_lookup = {
#     700: 8, 1000: 9.6, 1250: 10, 1500: 10, 1750: 9.8,
#     2000: 9.2, 2250: 8.2, 2500: 7.2, 3000: 5.9,
#     3500: 4.5, 4000: 4, 6000: 4
# }
#
# # Load CSV file (replace 'your_file.csv' with actual file path)
# df = pd.read_csv(csv_file_path, usecols=["eventDateTime", "engineRpm", "gearInfo"])
#
# # Function to get Gear 2 value based on engine RPM
# def get_gear_2_value(rpm):
#     # Find the closest matching RPM in the lookup table
#     closest_rpm = min(gear_2_lookup.keys(), key=lambda x: abs(x - rpm))
#     return gear_2_lookup[closest_rpm]
#
# # Apply the function to get Gear 2 values
# df["Gear 2 Value"] = df["engineRpm"].apply(get_gear_2_value)
#
# # Save to a new Excel file
# output_file_path = "/home/ttluser/Desktop/output.xlsx"
# df.to_excel(output_file_path, index=False)
#
# print(f"New Excel file saved: {output_file_path}")


import pandas as pd

# Define lookup table for all gears
gear_lookup = {
    1: {700: 10, 1000: 10, 1250: 10, 1500: 10, 1750: 10, 2000: 9.5, 2250: 8.6, 2500: 7.7, 3000: 6.4, 3500: 5.2, 4000: 4, 6000: 4},
    2: {700: 8, 1000: 9.6, 1250: 10, 1500: 10, 1750: 9.8, 2000: 9.2, 2250: 8.2, 2500: 7.2, 3000: 5.9, 3500: 4.5, 4000: 4, 6000: 4},
    3: {700: 8, 1000: 9.6, 1250: 10, 1500: 10, 1750: 9.8, 2000: 9.2, 2250: 8.2, 2500: 7, 3000: 5.5, 3500: 4.5, 4000: 4, 6000: 4},
    4: {700: 8, 1000: 9.6, 1250: 10, 1500: 10, 1750: 9.9, 2000: 9.6, 2250: 8.4, 2500: 7.2, 3000: 5.8, 3500: 5, 4000: 4, 6000: 4},
    5: {700: 7.5, 1000: 9.6, 1250: 10, 1500: 10, 1750: 10, 2000: 9.8, 2250: 8.8, 2500: 7.6, 3000: 6.6, 3500: 5.3, 4000: 4, 6000: 4},
    6: {700: 7.5, 1000: 9.6, 1250: 10, 1500: 10, 1750: 10, 2000: 10, 2250: 9.3, 2500: 8.7, 3000: 7.5, 3500: 5.5, 4000: 4, 6000: 4},
}

# Load CSV file
# csv_file_path = "your_file.csv"
df = pd.read_csv(csv_file_path, usecols=["eventDateTime", "engineRpm", "gearInfo"])

# Function to get gear value based on engine RPM and gear
def get_gear_value(rpm, gear):
    if gear in gear_lookup:
        closest_rpm = min(gear_lookup[gear].keys(), key=lambda x: abs(x - rpm))
        return gear_lookup[gear][closest_rpm]
    return None  # If gear not found

# Apply function for all gears
for gear in range(1, 7):
    df[f"Gear {gear} Value"] = df.apply(lambda row: get_gear_value(row["engineRpm"], gear), axis=1)

# Save to a new Excel file
output_file_path = "/home/ttluser/Desktop/all_gear_values.xlsx"
df.to_excel(output_file_path, index=False)

print(f"New Excel file saved: {output_file_path}")
