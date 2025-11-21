import sys

def run_generator():
    pgn_file = filedialog.askopenfilename(filetypes=[("PGN files", "*.pgn")])
    if not pgn_file:
        return

    outdir = outdir_entry.get().strip() or "output"
    jpg_enabled = jpg_var.get()

    # Use the same Python interpreter running the GUI
    cmd = [sys.executable, "scoresheet_generator.py", pgn_file, "--outdir", outdir]
    if not jpg_enabled:
        cmd.append("--no-jpg")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            messagebox.showinfo("Done", f"Finished!\n\nOutput:\n{result.stdout}")
        else:
            messagebox.showerror("Error", f"Generator failed:\n{result.stderr}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to run generator:\n{e}")

    app.destroy()
