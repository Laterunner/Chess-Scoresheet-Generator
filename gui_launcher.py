import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess

def run_generator():
    # Select PGN file
    pgn_file = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
    if not pgn_file:
        return

    # Output directory
    outdir = outdir_entry.get().strip() or "output"

    # JPG option
    jpg_enabled = jpg_var.get()

    # Build command
    cmd = ["python", "scoresheet_generator.py", pgn_file, "--outdir", outdir]
    if not jpg_enabled:
        cmd.append("--no-jpg")

    # Run generator
    subprocess.run(cmd)

    # Show confirmation popup
    messagebox.showinfo("Done", "Scoresheet generation finished successfully!")

    # Close GUI after confirmation
    app.destroy()
