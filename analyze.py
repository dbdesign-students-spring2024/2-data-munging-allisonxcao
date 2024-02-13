import csv
from collections import defaultdict

# Path to the cleaned data CSV file
clean_data_csv_path = 'data/clean_data.csv'

# Function to calculate the average of a list of numbers, excluding empty strings and missing data markers
def average(numbers):
    valid_numbers = [float(num) for num in numbers if num not in ('', '***', '****')]
    if valid_numbers:
        return sum(valid_numbers) / len(valid_numbers)
    else:
        return None

# Open the CSV file and read data
with open(clean_data_csv_path, newline='') as csvfile:
    reader = csv.DictReader(csvfile)

    # Dictionary to hold cumulative anomalies and counts for each decade
    decade_anomalies = defaultdict(list)

    for row in reader:
        year = int(row['Year'])
        decade = year - (year % 10)  # Determine the decade for the year

        # Check if J-D (annual average anomaly) is available and not missing
        if row['J-D'] not in ('', '***', '****'):
            year_average = float(row['J-D'])
        else:
            # Calculate the average anomaly for the year from monthly values, ignoring missing data
            monthly_anomalies = [row[month] for month in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] if row[month] not in ('', '***')]
            year_average = average(monthly_anomalies)

        # Only add the year's average to the decade's list if it was calculable
        if year_average is not None:
            decade_anomalies[decade].append(year_average)

# Calculate and print the average anomaly for each decade
for decade, anomalies in sorted(decade_anomalies.items()):
    avg_anomaly = average(anomalies)
    if avg_anomaly is not None:
        print(f"{decade}s: {avg_anomaly:.2f}°F")
