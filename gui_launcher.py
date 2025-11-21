
import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess, sys, os

def run_generator():
    pgn_file = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
    if not pgn_file:
        return

    outdir = outdir_entry.get().strip() or "output"
    jpg_enabled = jpg_var.get()

    script_path = os.path.join(os.path.dirname(__file__), "scoresheet_generator.py")
    cmd = [sys.executable, script_path, pgn_file, "--outdir", outdir]
    if jpg_enabled:
        cmd.append("--jpg")

    # Run generator, let output flow to terminal
    result = subprocess.run(cmd)

    if result.returncode == 0:
        messagebox.showinfo("Done", "Scoresheet generation finished successfully!")
    else:
        messagebox.showerror("Error", f"Generator failed with code {result.returncode}")

    app.destroy()


# GUI setup
app = tk.Tk()
app.title("Chess Scoresheet Generator")

# Center window
window_width, window_height = 400, 150
screen_width, screen_height = app.winfo_screenwidth(), app.winfo_screenheight()
x_position = int((screen_width/2) - (window_width/2))
y_position = int((screen_height/2) - (window_height/2))
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

# Keep on top
app.attributes("-topmost", True)

# Output directory field
tk.Label(app, text="Output directory:").pack(pady=5)
outdir_entry = tk.Entry(app, width=40)
outdir_entry.insert(0, "output")
outdir_entry.pack(pady=5)

# JPG export checkbox
jpg_var = tk.BooleanVar(value=True)  # default: JPG enabled
tk.Checkbutton(app, text="Enable JPG export", variable=jpg_var).pack(pady=5)

# Start button
tk.Button(app, text="Select PGN & Start", command=run_generator).pack(pady=10)

app.mainloop()
