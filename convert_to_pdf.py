# Python program to convert
# text file to pdf file

from fpdf import FPDF
import os

# save FPDF() class into 
# a variable pdf

# Converts txt document to a pdf document in specified directories
# Returns relative path to file 
from fpdf import FPDF

def replace_unsupported_chars(text):
    # Replace unsupported characters with a question mark
    return text.encode('latin-1', 'replace').decode('latin-1')

def txt_to_pdf(input:str, output_dir:str, output_name:str):
    extension = input.split('.')[1]
    if extension != 'txt':
        print('Error convert_to_pdf.py: not a TXT file')
        return(None)

    # Create instance of FPDF class
    pdf = FPDF()

    # Add a page
    pdf.add_page()

    # Set font
    pdf.set_font("Arial", size=12)

    # Open the text file in utf-8 encoding
    with open(input, 'r', encoding='utf-8') as file:
        for line in file:
            # Replace unsupported characters
            line = replace_unsupported_chars(line)
            # Add the line to the PDF
            pdf.cell(200, 10, txt=line, ln=True)

    # Output the PDF to a file
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")

    output_file = f"{output_dir}/output.pdf"
    pdf.output(output_file)

    output_name = output_name + ".pdf"

    output_file = output_dir + "/" + output_name
    # output_file = output_file.replace('_', '*')
    pdf.output(output_file) 

    return output_file


