import os
import pdfplumber
import pandas as pd
import json
from transformers import pipeline

# Initialize Hugging Face pipeline for LLM processing
generator = pipeline("text-generation", model="gpt2")

# Define column mappings
COLUMN_MAPPINGS = {
    "id_columns": ['Cat. NO', 'Order no', 'Diamond Chain Part No','Part No.', 'Catalog No.', 'Cat.Nos', 'IDH No.'],
    "title_columns": ['type', 'electrical product names','Carding Machine', ''],
    "description_columns": ['description', 'Type and frame size', 'Product Description','in mm','in inches', ''],
    "price_columns": ['M.R.P.', 'LP in INR', 'PRICE IN RS', 'MRP Per Metre',' Rs.   P.','MRP Per Metre Rs.   P.', 'Price', 'MRP*  / Unit', 'MRP', 'price']
}

def identify_column(column_name, mapping_type):
    """Identify the standardized column type."""
    if column_name is None:  # Skip None column names
        return False
    for keyword in COLUMN_MAPPINGS[mapping_type]:
        if keyword.lower() in column_name.lower():
            return True
    return False


def process_table(df):
    """Process the table to extract structured data."""
    structured_data = []
    for _, row in df.iterrows():
        # Map columns to standardized names
        sku_id = next((row[col] for col in df.columns if identify_column(col, "id_columns")), None)
        
        # Check for title, description, and price; handle Series objects correctly
        title = next((row[col] for col in df.columns if identify_column(col, "title_columns")), None)
        title = title if isinstance(title, str) else ""

        description = next((row[col] for col in df.columns if identify_column(col, "description_columns")), None)
        description = description if isinstance(description, str) else ""

        # Check if price is valid and convert to float, else set to None
        price = next((row[col] for col in df.columns if identify_column(col, "price_columns")), None)
        
        # Ensure that price is a valid value and convert to float if necessary
        if price is not None:
            try:
                # If price is a Series, we take the first value
                price = float(price) if isinstance(price, (str, int, float)) else None
            except ValueError:
                price = None

        # Collect additional attributes and ensure they're serializable
        attributes = {
            col: str(row[col]) if isinstance(row[col], pd.Series) else row[col]  # Convert Series to string
            for col in df.columns
            if col not in COLUMN_MAPPINGS["id_columns"]
            and col not in COLUMN_MAPPINGS["title_columns"]
            and col not in COLUMN_MAPPINGS["description_columns"]
            and col not in COLUMN_MAPPINGS["price_columns"]
        }

        # Add structured entry
        structured_data.append({
            "ID": sku_id,
            "title": title,
            "description": description,
            "price": price,
            "attributes": attributes
        })
    return structured_data



def extract_tables_from_pdf(pdf_path):
    """Extract tables from PDF using pdfplumber."""
    all_data = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            table = page.extract_table()
            if table:
                df = pd.DataFrame(table[1:], columns=table[0])  # First row as header
                if df.shape[1] > 2:  # Only process tables with > 2 columns
                    structured_data = process_table(df)
                    all_data.extend(structured_data)
    return all_data

def process_all_pdfs(input_folder, output_folder):
    """Process all PDFs in a folder and save structured data for each."""
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    for file_name in os.listdir(input_folder):
        if file_name.endswith(".pdf"):  # Process only PDF files
            pdf_path = os.path.join(input_folder, file_name)
            output_path = os.path.join(output_folder, f"{os.path.splitext(file_name)[0]}_data.json")
            
            print(f"Processing {pdf_path}...")
            all_data = extract_tables_from_pdf(pdf_path)
            with open(output_path, "w") as f:
                json.dump(all_data, f, indent=4)
            print(f"Data saved to {output_path}")

# Folder paths
input_folder = "Data\Pricelist"
output_folder = "Data\Extracted_Data"

# Run the process
process_all_pdfs(input_folder,output_folder)