from pdf2image import convert_from_path
import os

# Specify folder path containing PDF files
folder_path = os.path.dirname(__file__)

# Loop through each PDF file in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".pdf"):
        pdf_path = os.path.join(folder_path, filename)

        # Convert all pages to PNG images
        images = convert_from_path(pdf_path, dpi=200)

        # Save each image with individual page number and PDF filename
        for i, image in enumerate(images):
            image.save(os.path.join(os.path.dirname(__file__),
                       f"{filename}_page_{i+1}.png"), "PNG")

print("All PDF files converted to images!")
