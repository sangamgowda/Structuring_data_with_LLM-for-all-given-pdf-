Project: PDF Table Extractor

Description:
This project extracts tables from PDF files and processes them into structured JSON format. The final output is a JSON file containing all the structured data for each PDF.

Dependencies:
- Python 3.x
- pdfplumber
- pandas

Installation:
1. Install the required Python packages using pip:

Usage:
1. Place the PDF files in the Data/Pricelist folder.
2. Run the script 1.py to extract and process the tables from the PDFs:
The script will perform the following steps:
- Extract tables from PDFs and process them into structured data.
- Save the structured data as JSON files in the Data/Extracted_Data folder.

Script Breakdown:
- extract_tables_from_pdf(pdf_path): Extracts tables from a PDF file and processes them into structured data.
- process_all_pdfs(input_folder, output_folder): Processes all PDFs in the input folder and saves the structured data for each PDF as a JSON file in the output folder.

Folder Structure:
- Data/
  - Pricelist/ (Folder containing PDFs)
  - Extracted_Data/ (Folder to save structured JSON data)
