import os
import argparse
from tqdm import tqdm
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
import chess.pgn
import time

def extract_moves(pgn_path):
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
        board = game.board()
        moves = []
        for move in game.mainline_moves():
            san = board.san(move)
            moves.append(san)
            board.push(move)
    return moves

def draw_header(c, title, page_number, x=50, y=800):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"{title} – Seite {page_number}")
    c.setFont("Helvetica", 10)

def draw_scoresheet(c, moves, x_start=50, y_start=750, column_spacing=180, row_spacing=20, black_offset=60):
    max_full_moves_per_column = 20  # 20 Züge = 40 Halbzüge
    for i, move in enumerate(moves):
        move_number = i // 2 + 1
        is_white = i % 2 == 0
        col = (move_number - 1) // max_full_moves_per_column
        row = (move_number - 1) % max_full_moves_per_column
        x = x_start + col * column_spacing
        if not is_white:
            x += black_offset
        y = y_start - row * row_spacing
        label = f"{move_number}." if is_white else ""
        c.drawString(x, y, f"{label} {move}")

def generate_single_scoresheet(pgn_path, output_dir, jpg_enabled=True):
    os.makedirs(output_dir, exist_ok=True)
    base_name = os.path.splitext(os.path.basename(pgn_path))[0]
    pdf_path = os.path.join(output_dir, f"{base_name}.pdf")

    # Züge extrahieren
    moves = extract_moves(pgn_path)

    # PDF erzeugen
    c = canvas.Canvas(pdf_path)
    draw_header(c, title=base_name, page_number=1)
    draw_scoresheet(c, moves)
    c.save()

    # JPG-Export (optional)
    if jpg_enabled and os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        try:
            time.sleep(0.5)
            images = convert_from_path(pdf_path, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.join(output_dir, f"{base_name}_page{i+1}.jpg")
                img.save(img_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Fehler beim JPG-Export für {base_name}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Erzeuge Scoresheets aus PGN-Dateien.")
    parser.add_argument("pgn_files", nargs="+", help="Pfad zu einer oder mehreren PGN-Dateien")
    parser.add_argument("--no-jpg", action="store_true", help="JPG-Export deaktivieren")
    parser.add_argument("--outdir", default="output", help="Zielverzeichnis für PDF/JPG")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    for pgn_path in tqdm(args.pgn_files, desc="Verarbeite PGNs"):
        try:
            generate_single_scoresheet(pgn_path, args.outdir, jpg_enabled=not args.no_jpg)
        except Exception as e:
            print(f"⚠️ Fehler bei {pgn_path}: {e}")

if __name__ == "__main__":
    main()
