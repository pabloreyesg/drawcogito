# 🧠 Benson Figure OCR & Cropping Tool

**Author:** Pablo Reyes  
**License:** Free for academic and personal use.

---

## 📌 Description

This Python application automates the process of detecting and extracting pages from PDF files that contain the phrase:

> **"copia de la figura compleja de benson"**

Once detected, the tool extracts the next page and allows the user to **manually review and crop** the image using an **intuitive graphical interface**.

---

## 🎯 Key Features

- ✅ OCR detection of specific phrases inside PDFs (in Spanish)
- 🖼️ Interactive image cropping with real-time preview
- 🗂️ Flexible input/output folder selection
- 🧩 Modular: run detection and cropping independently or sequentially
- 💻 Easy-to-use GUI with styled menus
- 🔁 Supports any PNG images for cropping (not just OCR output)

---

## 🛠️ Requirements

### System

- Python 3.7 or higher
- Tesseract OCR installed  
  [Download Tesseract](https://github.com/tesseract-ocr/tesseract)

- Poppler installed (for `pdf2image` to work):
  - **Windows**: [Poppler for Windows](http://blog.alivate.com.au/poppler-windows/)
  - **macOS**: `brew install poppler`
  - **Linux**: `sudo apt install poppler-utils`

### Python packages

Install dependencies using pip:

```bash
pip install pytesseract pdf2image pillow