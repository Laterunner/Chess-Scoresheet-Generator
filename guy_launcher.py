import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from PIL import Image, ImageTk   # Pillow für Logo-Bild

def run_generator(pgn_path, outdir, jpg_enabled):
    cmd = ["python", "scoresheet_generator.py", pgn_path, "--outdir", outdir]
    if jpg_enabled:
        cmd.append("--jpg")
    subprocess.run(cmd)

'''
def show_autoclose_message(root):
    popup = tk.Toplevel(root)
    popup.title("Fertig")
    tk.Label(popup, text="Alle Scoresheets wurden erstellt!").pack(padx=20, pady=20)
    popup.after(3000, lambda: close_all(root, popup))
'''
#-------NEW---------------------------------------------------------------------------------
def show_autoclose_message(root):
    popup = tk.Toplevel(root)
    popup.title("Fertig")

    tk.Label(popup, text="Alle Scoresheets wurden erstellt!").pack(padx=20, pady=20)

    # --- Fenstergröße definieren ---
    window_width = 300
    window_height = 100

    # Bildschirmgröße abfragen
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()

    # Position berechnen (Mitte)
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))

    # Geometrie setzen
    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # Popup nach 3 Sekunden schließen
    popup.after(3000, lambda: close_all(root, popup))


#----------------------------------------------------------------------------------------
def close_all(root, popup):
    popup.destroy()
    root.destroy()
def main():
    root = tk.Tk()
    root.title("Scoresheet Generator")

    # --- Fenstergröße und Position mittig setzen ---
    window_width = 400
    window_height = 500
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # --- Logo mittig über PGN-Auswahl ---
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)  # moderne Variante
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=logo_img)
            logo_label.image = logo_img  # Referenz halten
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"⚠️ Logo konnte nicht geladen werden: {e}")

    tk.Label(root, text="PGN-Datei auswählen:").pack(pady=5)
    pgn_entry = tk.Entry(root, width=50)
    pgn_entry.pack(pady=5)

    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
        if filename:
            pgn_entry.delete(0, tk.END)
            pgn_entry.insert(0, filename)

    tk.Button(root, text="Durchsuchen", command=browse_file).pack(pady=5)

    tk.Label(root, text="Ausgabeordner:").pack(pady=5)
    outdir_entry = tk.Entry(root, width=50)
    outdir_entry.insert(0, "output")
    outdir_entry.pack(pady=5)

    jpg_var = tk.BooleanVar()
    tk.Checkbutton(root, text="JPG Export aktivieren", variable=jpg_var).pack(pady=5)

    def start_generation():
        pgn_path = pgn_entry.get()
        outdir = outdir_entry.get()
        jpg_enabled = jpg_var.get()
        if pgn_path and os.path.exists(pgn_path):
            run_generator(pgn_path, outdir, jpg_enabled)
            show_autoclose_message(root)

    tk.Button(root, text="Generieren", command=start_generation).pack(pady=20)

    root.mainloop()

'''
def main():
    root = tk.Tk()
    root.title("Scoresheet Generator")

    # --- Logo mittig über PGN-Auswahl ---
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            img = Image.open(logo_path)            
            img = img.resize((120, 120), Image.Resampling.LANCZOS)  # Größe anpassen
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=logo_img)
            logo_label.image = logo_img  # Referenz halten
            logo_label.pack(pady=10)
        except Exception as e:
            print(f"⚠️ Logo konnte nicht geladen werden: {e}")

    tk.Label(root, text="PGN-Datei auswählen:").pack(pady=5)
    pgn_entry = tk.Entry(root, width=50)
    pgn_entry.pack(pady=5)


    def browse_file():
        filename = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
        if filename:
            pgn_entry.delete(0, tk.END)
            pgn_entry.insert(0, filename)

    tk.Button(root, text="Durchsuchen", command=browse_file).pack(pady=5)

    tk.Label(root, text="Ausgabeordner:").pack(pady=5)
    outdir_entry = tk.Entry(root, width=50)
    outdir_entry.insert(0, "output")
    outdir_entry.pack(pady=5)

    jpg_var = tk.BooleanVar()
    tk.Checkbutton(root, text="JPG Export aktivieren", variable=jpg_var).pack(pady=5)

    def start_generation():
        pgn_path = pgn_entry.get()
        outdir = outdir_entry.get()
        jpg_enabled = jpg_var.get()
        if pgn_path and os.path.exists(pgn_path):
            run_generator(pgn_path, outdir, jpg_enabled)
            show_autoclose_message(root)

    tk.Button(root, text="Generieren", command=start_generation).pack(pady=20)

    root.mainloop()
'''
if __name__ == "__main__":
    main()
