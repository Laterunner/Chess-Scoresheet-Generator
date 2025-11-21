
import tkinter as tk
from tkinter import filedialog
import subprocess

def run_generator():
    # PGN-Datei auswählen
    pgn_file = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
    if not pgn_file:
        return

    # Output-Verzeichnis
    outdir = outdir_entry.get().strip() or "output"

    # JPG-Option
    jpg_enabled = jpg_var.get()

    # Kommando zusammenbauen
    cmd = ["python", "scoresheet_generator.py", pgn_file, "--outdir", outdir]
    if jpg_enabled:
        cmd.append("--jpg")

    # Starten
    subprocess.run(cmd)

# Fenster
root = tk.Tk()
root.title("Chess Scoresheet Generator")

# Output-Verzeichnis
tk.Label(root, text="Output directory:").pack(pady=5)
outdir_entry = tk.Entry(root, width=40)
outdir_entry.insert(0, "output")
outdir_entry.pack(pady=5)

# JPG-Export Checkbox
jpg_var = tk.BooleanVar(value=False)
tk.Checkbutton(root, text="Enable JPG export", variable=jpg_var).pack(pady=5)

# Start-Button
tk.Button(root, text="Select PGN & Start", command=run_generator).pack(pady=10)

root.mainloop()
