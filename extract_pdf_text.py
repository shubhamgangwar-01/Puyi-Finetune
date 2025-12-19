"""
Extract text from PDF file
"""

import PyPDF2
import os

def extract_text_from_pdf(pdf_path, output_path):
    """Extract all text from PDF and save to text file"""
    
    print(f"Opening PDF: {pdf_path}")
    
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at {pdf_path}")
        return False
    
    try:
        # Open the PDF file
        with open(pdf_path, 'rb') as pdf_file:
            # Create PDF reader object
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            
            # Get number of pages
            num_pages = len(pdf_reader.pages)
            print(f"Total pages: {num_pages}")
            
            # Extract text from all pages
            full_text = []
            
            for page_num in range(num_pages):
                print(f"Extracting page {page_num + 1}/{num_pages}...", end='\r')
                page = pdf_reader.pages[page_num]
                text = page.extract_text()
                full_text.append(text)
            
            print(f"\nExtraction complete!")
            
            # Combine all text
            combined_text = '\n\n--- Page Break ---\n\n'.join(full_text)
            
            # Save to text file
            with open(output_path, 'w', encoding='utf-8') as text_file:
                text_file.write(combined_text)
            
            print(f"✓ Text saved to: {output_path}")
            print(f"✓ Total characters: {len(combined_text):,}")
            print(f"✓ Total pages: {num_pages}")
            
            return True
            
    except Exception as e:
        print(f"Error: {e}")
        return False


if __name__ == "__main__":
    # PDF file path
    pdf_file = r"C:\Users\amrit\Desktop\ernie-memories-project\From Emperor to Citizen_ The Autobiography of Aisin-Gioro Pu -- ____ -- 401643b625aea088e5002d3c35e6d7.pdf"
    
    # Output text file
    output_file = r"C:\Users\amrit\Desktop\ernie-memories-project\emperor_to_citizen_text.txt"
    
    # Extract text
    extract_text_from_pdf(pdf_file, output_file)
