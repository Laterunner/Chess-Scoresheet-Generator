import tkinter as tk
from tkinter import filedialog
import subprocess
import os

def run_generator(pgn_path, outdir, jpg_enabled):
    # Hier rufst du dein Hauptskript auf
    cmd = ["python", "scoresheet_generator.py", pgn_path, "--outdir", outdir]
    if jpg_enabled:
        cmd.append("--jpg")
    subprocess.run(cmd)

def show_autoclose_message(root):
    popup = tk.Toplevel(root)
    popup.title("Fertig")
    tk.Label(popup, text="Alle Scoresheets wurden erstellt!").pack(padx=20, pady=20)

    # Popup nach 3 Sekunden schließen
    popup.after(3000, lambda: close_all(root, popup))

def close_all(root, popup):
    popup.destroy()
    root.destroy()   # schließt auch das Hauptfenster

def main():
    root = tk.Tk()
    root.title("Scoresheet Generator")

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

if __name__ == "__main__":
    main()
