import os
import argparse
from tqdm import tqdm
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
import chess.pgn
import time

def draw_header(c, title, page_number, x=50, y=800):
    c.setFont("Helvetica-Bold", 12)
    c.drawString(x, y, f"{title} – Seite {page_number}")
    c.setFont("Helvetica", 10)

def draw_scoresheet(c, moves, x_start=50, y_start=750, column_spacing=180, row_spacing=20, black_offset=60):
    max_full_moves_per_column = 20
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

def generate_single_scoresheet(moves, title, output_pdf, jpg_enabled=True):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    c = canvas.Canvas(output_pdf)
    draw_header(c, title=title, page_number=1)
    draw_scoresheet(c, moves)
    c.save()

    if jpg_enabled and os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
        try:
            time.sleep(0.5)
            images = convert_from_path(output_pdf, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.splitext(output_pdf)[0] + f"_page{i+1}.jpg"
                img.save(img_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Fehler beim JPG-Export für {title}: {e}")

def generate_scoresheets_from_pgn_file(pgn_path, output_dir, jpg_enabled=True):
    os.makedirs(output_dir, exist_ok=True)
    with open(pgn_path, "r", encoding="utf-8") as f:
        game_index = 1
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            board = game.board()
            moves = []
            for move in game.mainline_moves():
                san = board.san(move)
                moves.append(san)
                board.push(move)

            white = game.headers.get("White", "White")
            black = game.headers.get("Black", "Black")
            title = f"{white} vs {black}"
            base_name = os.path.splitext(os.path.basename(pgn_path))[0]
            pdf_name = f"{base_name}_game{game_index}_{white}_vs_{black}.pdf"
            output_pdf = os.path.join(output_dir, pdf_name)

            generate_single_scoresheet(moves, title, output_pdf, jpg_enabled)
            game_index += 1

def main():
    parser = argparse.ArgumentParser(description="Erzeuge Scoresheets aus PGN-Dateien.")
    parser.add_argument("pgn_files", nargs="+", help="Pfad zu einer oder mehreren PGN-Dateien")
    parser.add_argument("--no-jpg", action="store_true", help="JPG-Export deaktivieren")
    parser.add_argument("--outdir", default="output", help="Zielverzeichnis für PDF/JPG")
    args = parser.parse_args()

    for pgn_path in tqdm(args.pgn_files, desc="Verarbeite PGN-Dateien"):
        try:
            generate_scoresheets_from_pgn_file(pgn_path, args.outdir, jpg_enabled=not args.no_jpg)
        except Exception as e:
            print(f"⚠️ Fehler bei {pgn_path}: {e}")

if __name__ == "__main__":
    main()
