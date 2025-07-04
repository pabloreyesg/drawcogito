# Benson Figure Page Extractor (OCR)

**Author**: Pablo Reyes  
**Description**: Automatically scans PDF files for a specific Spanish phrase using OCR and extracts the following page as an image.

---

## What This Script Does

This Python script searches through all PDF files in a selected input folder, looking for the phrase:

> **"copia de la figura compleja de benson"**

When the phrase is found in any page (except the last), it extracts the **next page** (i+1) and saves it as a PNG image. A detailed log file is also generated in the output folder.

---

## Features

- Batch processing of PDFs.
- OCR-based phrase detection using Tesseract.
- GUI prompts for selecting input and output folders.
- Saves extracted pages as high-quality PNG files.
- Creates a log file summarizing results for each PDF.

---

## Requirements

- **Python 3.6 or higher**
- **Tesseract OCR**  
  Install from: [https://github.com/tesseract-ocr/tesseract](https://github.com/tesseract-ocr/tesseract)

- **Python packages**:
  ```bash
  pip install pytesseract pdf2image pillow ```

Poppler (for pdf2image)
Windows: Download from Poppler for Windows
macOS: brew install poppler
Linux: sudo apt install poppler-utils

If Tesseract is not in your system PATH, you must set its path manually in the script:

```python

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
```
