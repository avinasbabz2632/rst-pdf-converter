import os
import pdf2image
import pytesseract
from pdf2image.exceptions import PDFPageCountError, PDFSyntaxError
from PIL import Image
from docutils.core import publish_file

def pdf_to_rst(pdf_path, rst_path):
    try:
        # Convert PDF pages to images
        images = pdf2image.convert_from_path(pdf_path)
    except (PDFPageCountError, PDFSyntaxError) as e:
        print("Failed to process PDF:", e)
        return

    # Initialize an empty string to store the extracted text
    extracted_text = ""

    # Directory to store extracted images
    img_dir = os.path.join(os.path.dirname(rst_path), "images")
    os.makedirs(img_dir, exist_ok=True)

    # Extract text from each image using pytesseract
    for i, image in enumerate(images):
        # Save the image and add a reference to it in the RST file
        img_path = os.path.join(img_dir, f"image{i}.png")
        image.save(img_path)

        # Add image reference to the RST document
        extracted_text += f".. image:: ./images/image{i}.png\n\n"

        # Add the OCR text below the image
        extracted_text += pytesseract.image_to_string(image) + "\n\n"

    # Write the extracted text to the RST file
    with open(rst_path, "w", encoding="utf-8") as file:
        file.write(extracted_text)

    # Convert RST to HTML
    html_path = os.path.splitext(rst_path)[0] + ".html"
    publish_file(source_path=rst_path, destination_path=html_path, writer_name="html")

# Specify the path to your PDF file and the desired RST output file
pdf_file = "samplefile.pdf"
rst_file = "samplefile.rst"

# Convert the PDF to RST
pdf_to_rst(pdf_file, rst_file)

