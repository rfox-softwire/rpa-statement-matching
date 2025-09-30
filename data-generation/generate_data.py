import uuid
import random
import os
from datetime import datetime, timedelta
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_data(rows=10000, output_file='internal_data.csv', sample_size=1000):
    """
    Generate a CSV file with randomized data and create two sample files.
    
    Args:
        rows (int): Number of rows to generate
        output_file (str): Name of the main output CSV file
        sample_size (int): Number of rows to include in each sample
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
    
    # Create two sample datasets from the generated data
    if os.path.exists(output_file):
        # Read the generated data
        with open(output_file, 'r') as f:
            reader = csv.DictReader(f)
            data = list(reader)
        
        # Ensure sample size is not larger than the dataset
        sample_size = min(sample_size, len(data) // 2)  # Half the sample size for each file
        
        def modify_sample(sample_data, changes=20):
            # Make a deep copy to avoid modifying the original data
            modified = [row.copy() for row in sample_data]
            
            # Ensure we have enough rows to modify
            changes = min(changes, len(modified) // 2)
            
            # Select unique rows for price and volume changes
            all_indices = list(range(len(modified)))
            price_indices = random.sample(all_indices, changes)
            volume_indices = random.sample([i for i in all_indices if i not in price_indices], changes)
            
            # Modify prices
            for idx in price_indices:
                price = int(modified[idx]['price'])
                modified[idx]['price'] = str(int(price * random.uniform(0.9, 1.1)))  # ±10%
            
            # Modify volumes
            for idx in volume_indices:
                volume = int(modified[idx]['volume'])
                modified[idx]['volume'] = str(int(volume * random.uniform(0.5, 1.5)))  # ±50%
            
            return modified
        
        # Create and modify first sample (broker_1_data.csv)
        sample_1_data = random.sample(data, sample_size)
        modified_sample_1 = modify_sample(sample_1_data)
        with open('broker_1_data.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(modified_sample_1)
        
        # Remove selected samples from the data to ensure no overlap
        remaining_data = [row for row in data if row not in sample_1_data]
        
        # Create and modify second sample and save as PDF
        sample_2_data = random.sample(remaining_data, min(sample_size, len(remaining_data)))
        modified_sample_2 = modify_sample(sample_2_data)
        
        # Save as CSV (commented out, uncomment if you want both CSV and PDF)
        # with open('broker_2_data.csv', 'w', newline='') as f:
        #     writer = csv.DictWriter(f, fieldnames=data[0].keys())
        #     writer.writeheader()
        #     writer.writerows(modified_sample_2)
        
        # Save as PDF
        def create_pdf(data, filename):
            doc = SimpleDocTemplate(filename, pagesize=letter)
            elements = []
            
            # Get headers from the first row
            headers = list(data[0].keys())
            
            # Prepare data for the table
            table_data = [headers]
            for row in data:
                table_data.append([str(row[header]) for header in headers])
            
            # Create the table
            table = Table(table_data)
            
            # Add style to the table
            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, 0), 10),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.white),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('FONTSIZE', (0, 1), (-1, -1), 8),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
            ])
            
            # Apply the style
            table.setStyle(style)
            
            # Add the table to the elements
            elements.append(table)
            
            # Build the PDF
            doc.build(elements)
        
        # Create PDF for broker 2 data
        create_pdf(modified_sample_2, 'broker_2_data.pdf')
        
        print(f"Successfully created sample files:")
        print(f"- broker_1_data.csv (CSV)")
        print(f"- broker_2_data.pdf (PDF with table)")
    else:
        print(f"Error: {output_file} not found. Cannot create sample files.")

if __name__ == "__main__":
    generate_data()
