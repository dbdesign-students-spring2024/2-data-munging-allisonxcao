def convert_to_fahrenheit(celsius_anomaly):
    #Convert temperature anomaly from 0.01 degrees Celsius to Fahrenheit."""
    celsius = celsius_anomaly / 100.0  
    fahrenheit = celsius * 1.8  
    return format(fahrenheit, '.1f')  

def is_data_line(line):
    #Check if the line is a data line.
    return line.strip() and not line.startswith(' ') and line[0].isdigit()

original_file_path = 'data/nasa.txt'
clean_file_path = 'data/clean_data.csv'

first_column_heading_encountered = False

with open(original_file_path, 'r') as infile, open(clean_file_path, 'w') as outfile:
    for line in infile:
        if not line.strip() or "GLOBAL Land-Ocean" in line or "Divide by 100" in line:
            continue

        if "Year" in line and "Jan" in line:
            if not first_column_heading_encountered:
                outfile.write(','.join(line.split()[:-2]) + '\n')
                first_column_heading_encountered = True
            continue  

        if is_data_line(line):
            parts = line.split()
            new_parts = [parts[0]]
            
            for part in parts[1:-2]:
                if part == '***': 
                    new_parts.append('')
                elif part.replace('-', '').isdigit(): 
                    new_parts.append(convert_to_fahrenheit(int(part)))
                else:
                    new_parts.append(part)
            outfile.write(','.join(new_parts) + '\n')
