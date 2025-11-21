import tkinter as tk
from tkinter import messagebox
import subprocess
import sys

def run_test():
    # Run a simple Python one-liner
    cmd = [sys.executable, "-c", "print('hello from subprocess')"]

    result = subprocess.run(cmd, capture_output=True, text=True)

    # Show whatever came back
    messagebox.showinfo("Result", f"Return code: {result.returncode}\n\nOutput:\n{result.stdout}\n\nErrors:\n{result.stderr}")

# Create window
app = tk.Tk()
app.title("Hello Test")

tk.Button(app, text="Run Hello", command=run_test).pack(pady=20)

app.mainloop()
