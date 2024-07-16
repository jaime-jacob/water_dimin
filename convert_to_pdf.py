# Python program to convert
# text file to pdf file

from fpdf import FPDF
import os

# save FPDF() class into 
# a variable pdf

# Converts txt document to a pdf document in specified directories
# Returns relative path to file 
def txt_to_pdf(input, output_dir="data/water_pdfs"):
    pdf = FPDF() 

    # Add a page
    pdf.add_page()

    # set style and size of font 
    # that you want in the pdf
    pdf.set_font("Arial", size = 10)

    # open the text file in read mode
    f = open(input, "r")

    # insert the texts in pdf
    for x in f:
        pdf.cell(200, 10, txt = x, ln = 1, align = 'L')

    # save the pdf with name .pdf
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"Directory '{output_dir}' created.")
    # else:
    #     print(f"Directory '{output_dir}' already exists.")
    
    output = input.split('/')
    output = output[2].split('.')
    output = output[0] + ".pdf"
    output_file = output_dir + "/" + output
    print("Output file name:", output_file)
    pdf.output(output_file) 


    return(output_file)

#txt_to_pdf("data/water_docs/adams_county.txt", "data/water_pdfs")
