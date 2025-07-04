"""
=======================================================================
Extract Specific Page from PDFs Using OCR - Benson Figure Detection
Author: Pablo Reyes
=======================================================================

📌 Description:
This script scans multiple PDF files in a selected folder and uses OCR 
(Optical Character Recognition) to detect a specific Spanish phrase: 
"copia de la figura compleja de benson". When found, it extracts the 
following page (i+1) where the phrase was detected and saves it as a 
PNG image.

The process includes logging results in a text file for reference.

🎯 Key Features:
- Supports batch processing of PDFs.
- Uses Tesseract OCR to read text from PDF pages.
- Graphical interface to choose both input and output folders.
- Automatically saves detected pages in PNG format.
- Generates a log file detailing results for each file.

🛠 Requirements:
- Python 3.x
- Installed Packages:
    - pytesseract
    - pdf2image
    - Pillow (PIL)
    - tkinter (comes with standard Python installation)
- Tesseract OCR installed on your system.
  Download from: https://github.com/tesseract-ocr/tesseract

🔧 Optional:
If Tesseract is not in your PATH, set its full path in:
    pytesseract.pytesseract.tesseract_cmd

=======================================================================
"""

import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image
from tkinter import filedialog, Tk
from tkinter.messagebox import showinfo

# === CONFIGURATION ===
DPI = 150
KEY_PHRASE = "copia de la figura compleja de benson".lower()  # Use lowercase for OCR matching

# Optional: Set path to tesseract.exe if not in PATH
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# === GRAPHICAL INTERFACE TO SELECT FOLDERS ===
root = Tk()
root.withdraw()  # Hide main window

pdf_dir = filedialog.askdirectory(title="Select Folder Containing PDFs")
if not pdf_dir:
    print("❌ No input folder selected. Exiting.")
    exit()

output_dir = filedialog.askdirectory(title="Select Output Folder for Images and Logs")
if not output_dir:
    print("❌ No output folder selected. Exiting.")
    exit()

log_path = os.path.join(output_dir, "results_log.txt")

# === CREATE OUTPUT DIRECTORY IF IT DOESN'T EXIST ===
os.makedirs(output_dir, exist_ok=True)

# === LOG FILE ===
with open(log_path, "w", encoding="utf-8") as log_file:
    log_file.write("Log of Benson figure page extraction (via OCR)\n\n")

    # === PROCESS EACH PDF ===
    for file in os.listdir(pdf_dir):
        if file.lower().endswith(".pdf"):
            pdf_path = os.path.join(pdf_dir, file)
            log_file.write(f"Processing file: {file}\n")
            print(f"Processing: {file}")

            pages = convert_from_path(pdf_path, dpi=DPI)
            target_index = None

            for i, page in enumerate(pages[:-1]):  # skip last page
                text = pytesseract.image_to_string(page, lang="spa").lower()
                if KEY_PHRASE in text:
                    target_index = i + 1
                    break

            if target_index is not None and target_index < len(pages):
                output_filename = os.path.splitext(file)[0] + "_benson_page_ocr.png"
                output_path = os.path.join(output_dir, output_filename)
                pages[target_index].save(output_path, "PNG")
                log_file.write(f"✔ Page detected (page {target_index + 1}): {output_filename}\n\n")
                print(f"✔ Page extracted: {output_filename}")
            else:
                log_file.write("⚠ Key phrase not found, no page extracted.\n\n")
                print(f"⚠ Phrase not found in {file}")

showinfo("Completed", "✅ OCR process and logging complete.")
