import csv
import uuid
import random
from datetime import datetime, timedelta

def generate_data(rows=10000, output_file='random_data.csv'):
    """
    Generate a CSV file with randomized data.
    
    Args:
        rows (int): Number of rows to generate
        output_file (str): Name of the output CSV file
    """
    # Generate a random date within the past month
    def random_date():
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        random_days = random.randint(0, (end_date - start_date).days)
        return (start_date + timedelta(days=random_days)).strftime('%Y-%m-%d')
    
    # Generate data rows
    data = []
    for _ in range(rows):
        row = {
            'id': str(uuid.uuid4())[:8],  # First 8 chars of UUID for a shorter ID
            'price': random.randint(10000, 99999),  # 5-digit price
            'volume': random.randint(1, 1000),        # Volume between 1 and 1,000
            'date': random_date()                     # Random date in the past month
        }
        data.append(row)
    
    # Write to CSV
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['id', 'price', 'volume', 'date']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        writer.writerows(data)
    
    print(f"Successfully generated {rows} rows in {output_file}")

if __name__ == "__main__":
    generate_data()
