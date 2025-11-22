import tkinter as tk
from tkinter import filedialog, ttk
import subprocess
import os
import chess.pgn

def run_generator(pgn_path, outdir, jpg_enabled, progress):
    # Zähle die Anzahl der Spiele im PGN
    total_games = 0
    with open(pgn_path, "r", encoding="utf-8") as f:
        while chess.pgn.read_game(f):
            total_games += 1

    progress["maximum"] = total_games
    progress["value"] = 0

    # Generator pro Spiel aufrufen (vereinfacht: hier dein Hauptskript)
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
        while game:
            # Hier würdest du dein scoresheet_generator.py aufrufen
            cmd = ["python", "scoresheet_generator.py", pgn_path, "--outdir", outdir]
            if jpg_enabled:
                cmd.append("--jpg")
            subprocess.run(cmd)

            # Fortschritt erhöhen
            progress["value"] += 1
            progress.update_idletasks()

            game = chess.pgn.read_game(f)

def show_autoclose_message(root):
    popup = tk.Toplevel(root)
    popup.title("Fertig")
    tk.Label(popup, text="Alle Scoresheets wurden erstellt!").pack(padx=20, pady=20)

    # --- Popup mittig setzen ---
    window_width = 300
    window_height = 100
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))
    popup.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    popup.after(3000, lambda: close_all(root, popup))

def close_all(root, popup):
    popup.destroy()
    root.destroy()

def main():
    root = tk.Tk()
    root.title("Scoresheet Generator")

    # --- Hauptfenster mittig setzen ---
    window_width = 400
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_position = int((screen_width / 2) - (window_width / 2))
    y_position = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

    # --- Logo optional ---
    logo_path = "logo.png"
    if os.path.exists(logo_path):
        try:
            from PIL import Image, ImageTk
            img = Image.open(logo_path)
            img = img.resize((120, 120), Image.Resampling.LANCZOS)
            logo_img = ImageTk.PhotoImage(img)
            logo_label = tk.Label(root, image=logo_img)
            logo_label.image = logo_img
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

    # --- Fortschrittsbalken ---
    progress = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress.pack(pady=10)

    def start_generation():
        pgn_path = pgn_entry.get()
        outdir = outdir_entry.get()
        jpg_enabled = jpg_var.get()
        if pgn_path and os.path.exists(pgn_path):
            run_generator(pgn_path, outdir, jpg_enabled, progress)
            show_autoclose_message(root)

    tk.Button(root, text="Generieren", command=start_generation).pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
