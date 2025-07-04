import os
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageTk
from tkinter import filedialog, Tk, Canvas, Button, Label, Toplevel, messagebox

# === CONFIG ===
DPI = 150
KEY_PHRASE = "copia de la figura compleja de benson".lower()
WIDTH_DISPLAY = 500

# === GLOBAL FOLDERS ===
input_pdf_dir = ""
output_dir = ""
detected_pages_dir = ""
confirmed_crops_dir = ""

def select_folders():
    global input_pdf_dir, output_dir, detected_pages_dir, confirmed_crops_dir

    input_pdf_dir = filedialog.askdirectory(title="Select Input Folder (PDFs)")
    if not input_pdf_dir:
        return False

    output_dir = filedialog.askdirectory(title="Select Output Folder")
    if not output_dir:
        return False

    detected_pages_dir = os.path.join(output_dir, "detected_pages")
    confirmed_crops_dir = os.path.join(output_dir, "confirmed_crops")
    os.makedirs(detected_pages_dir, exist_ok=True)
    os.makedirs(confirmed_crops_dir, exist_ok=True)

    return True

def run_ocr(log_to_console=True):
    log_path = os.path.join(output_dir, "results_log.txt")
    with open(log_path, "w", encoding="utf-8") as log_file:
        log_file.write("Log of Benson figure page extraction (via OCR)\n\n")
        for file in os.listdir(input_pdf_dir):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(input_pdf_dir, file)
                log_file.write(f"Processing file: {file}\n")
                if log_to_console:
                    print(f"Processing: {file}")
                pages = convert_from_path(pdf_path, dpi=DPI)
                target_index = None
                for i, page in enumerate(pages[:-1]):
                    text = pytesseract.image_to_string(page, lang="spa").lower()
                    if KEY_PHRASE in text:
                        target_index = i + 1
                        break
                if target_index is not None and target_index < len(pages):
                    output_filename = os.path.splitext(file)[0] + "_benson_page_ocr.png"
                    output_path = os.path.join(detected_pages_dir, output_filename)
                    pages[target_index].save(output_path, "PNG")
                    log_file.write(f"✔ Page detected (page {target_index + 1}): {output_filename}\n\n")
                    if log_to_console:
                        print(f"✔ Page extracted: {output_filename}")
                else:
                    log_file.write("⚠ Key phrase not found, no page extracted.\n\n")
                    if log_to_console:
                        print(f"⚠ Phrase not found in {file}")

def start_ocr():
    if not select_folders():
        return
    run_ocr()
    messagebox.showinfo("OCR Completed", "✅ OCR process completed. You can now proceed to crop the images.")

# === INTERACTIVE CROP GUI ===
class RecorteInteractivoApp:
    def __init__(self, master, input_dir, output_dir):
        self.master = master
        self.input_dir = input_dir
        self.output_dir = output_dir

        self.master.title("Validate & Crop Benson Pages")
        self.master.geometry("1100x620")
        self.master.configure(bg="#f3f4f6")

        Label(master, text="Interactive Crop Tool", font=("Segoe UI", 16, "bold"), bg="#f3f4f6", fg="#333").pack(pady=(10, 4))
        Label(master, text="Click on the left image to adjust the crop.", font=("Segoe UI", 10), bg="#f3f4f6").pack()

        self.canvas_original = Canvas(master, width=WIDTH_DISPLAY, height=500, bg="#ddd")
        self.canvas_original.pack(side="left", padx=20, pady=10)

        self.canvas_corte = Canvas(master, width=WIDTH_DISPLAY, height=500, bg="#ddd")
        self.canvas_corte.pack(side="right", padx=20, pady=10)

        Button(master, text="Next Image", command=self.cargar_siguiente, font=("Segoe UI", 10), bg="#0078D4", fg="white", width=25).pack(pady=10)

        self.lista_imagenes = sorted([
            f for f in os.listdir(self.input_dir)
            if f.lower().endswith(".png")
        ])
        self.index_actual = -1
        self.canvas_original.bind("<Button-1>", self.ajustar_corte)
        self.cargar_siguiente()

    def cargar_siguiente(self):
        self.index_actual += 1
        if self.index_actual >= len(self.lista_imagenes):
            messagebox.showinfo("Done", "✅ No more images to crop.")
            self.master.destroy()
            return

        archivo = self.lista_imagenes[self.index_actual]
        self.imagen_original_path = os.path.join(self.input_dir, archivo)
        self.imagen_original_pil = Image.open(self.imagen_original_path)

        mini = self.imagen_original_pil.resize((WIDTH_DISPLAY, int(self.imagen_original_pil.height * WIDTH_DISPLAY / self.imagen_original_pil.width)))
        self.tk_original = ImageTk.PhotoImage(mini)
        self.canvas_original.delete("all")
        self.canvas_original.create_image(0, 0, anchor="nw", image=self.tk_original)
        self.aplicar_corte(0.45)

    def ajustar_corte(self, event):
        displayed_height = self.tk_original.height()
        real_height = self.imagen_original_pil.height
        porcentaje_real = event.y / displayed_height
        self.aplicar_corte(porcentaje_real)
        self.guardar_recorte(porcentaje_real)

    def aplicar_corte(self, porcentaje):
        ancho, alto = self.imagen_original_pil.size
        inicio_y = int(alto * porcentaje)
        recorte = self.imagen_original_pil.crop((0, inicio_y, ancho, alto))
        mini_corte = recorte.resize((WIDTH_DISPLAY, int(recorte.height * WIDTH_DISPLAY / recorte.width)))
        self.tk_corte = ImageTk.PhotoImage(mini_corte)
        self.canvas_corte.delete("all")
        self.canvas_corte.create_image(0, 0, anchor="nw", image=self.tk_corte)
        self.recorte_actual = recorte

    def guardar_recorte(self, porcentaje):
        nombre_salida = os.path.basename(self.imagen_original_path).replace("benson_page_ocr", "copia_paciente_gui")
        output_path = os.path.join(self.output_dir, nombre_salida)
        self.recorte_actual.save(output_path)
        print(f"✔ Crop saved ({porcentaje:.2f}): {output_path}")

def start_gui_crop():
    global confirmed_crops_dir

    # Paso 1: seleccionar carpeta con imágenes si no hay OCR previos
    input_img_dir = detected_pages_dir
    if not os.path.exists(input_img_dir) or not os.listdir(input_img_dir):
        messagebox.showinfo("Select Folder", "No Benson pages detected. Please select a folder with PNG images.")
        input_img_dir = filedialog.askdirectory(title="Select Folder with Images to Crop")
        if not input_img_dir:
            return

    # Paso 2: carpeta de salida
    if not os.path.exists(confirmed_crops_dir) or not os.listdir(confirmed_crops_dir):
        confirmed_crops_dir = filedialog.askdirectory(title="Select Output Folder for Cropped Images")
        if not confirmed_crops_dir:
            return
        os.makedirs(confirmed_crops_dir, exist_ok=True)

    # Lanzar GUI
    win = Toplevel()
    RecorteInteractivoApp(win, input_img_dir, confirmed_crops_dir)

# === MAIN MENU ===
def main_menu():
    root = Tk()
    root.title("Benson Figure Processing Tool")
    root.geometry("400x300")
    root.configure(bg="#f9fafb")

    Label(root, text="🧠 Benson Figure OCR & Crop Tool", font=("Segoe UI", 14, "bold"), bg="#f9fafb", fg="#333").pack(pady=(30, 10))

    Button(root, text="📄 Detect Pages (OCR)", font=("Segoe UI", 11), width=30, bg="#0078D4", fg="white", command=start_ocr).pack(pady=10)
    Button(root, text="✂️ Validate & Crop Pages", font=("Segoe UI", 11), width=30, bg="#28a745", fg="white", command=start_gui_crop).pack(pady=10)
    Button(root, text="❌ Exit", font=("Segoe UI", 11), width=30, bg="#dc3545", fg="white", command=root.quit).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main_menu()
