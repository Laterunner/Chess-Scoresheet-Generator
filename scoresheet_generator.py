import os
import argparse
import chess.pgn
from tqdm import tqdm
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
import time

def extract_moves_from_pgn(pgn_path):
    with open(pgn_path, "r", encoding="utf-8") as f:
        game = chess.pgn.read_game(f)
        board = game.board()
        moves = []
        for move in game.mainline_moves():
            san = board.san(move)
            moves.append(san)
            board.push(move)
    return moves

def draw_scoresheet(c, moves, x_start=50, y_start=750, column_spacing=180, row_spacing=20):
    max_full_moves_per_column = 20  # 20 Züge = 40 Halbzüge
    for i, move in enumerate(moves):
        move_number = i // 2 + 1
        is_white = i % 2 == 0
        col = (move_number - 1) // max_full_moves_per_column
        row = (move_number - 1) % max_full_moves_per_column
        x = x_start + col * column_spacing
        y = y_start - row * row_spacing
        label = f"{move_number}." if is_white else ""
        c.drawString(x, y, f"{label} {move}")

def generate_pdf(moves, output_pdf):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    c = canvas.Canvas(output_pdf)
    draw_scoresheet(c, moves)
    c.save()

def convert_pdf_to_jpg(pdf_path, output_dir):
    time.sleep(0.5)  # Warten, bis PDF sicher geschrieben ist
    if os.path.exists(pdf_path) and os.path.getsize(pdf_path) > 0:
        try:
            images = convert_from_path(pdf_path, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.join(output_dir, f"{os.path.splitext(os.path.basename(pdf_path))[0]}_page{i+1}.jpg")
                img.save(img_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Fehler beim Konvertieren von {pdf_path}: {e}")
    else:
        print(f"⚠️ PDF {pdf_path} existiert nicht oder ist leer.")

def main():
    parser = argparse.ArgumentParser(description="Erzeuge Scoresheets aus PGN-Dateien.")
    parser.add_argument("pgn_files", nargs="+", help="Pfad zu einer oder mehreren PGN-Dateien")
    parser.add_argument("--no-jpg", action="store_true", help="JPG-Export deaktivieren")
    parser.add_argument("--outdir", default="output", help="Zielverzeichnis für PDF/JPG")
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    for pgn_path in tqdm(args.pgn_files, desc="Verarbeite PGNs"):
        try:
            moves = extract_moves_from_pgn(pgn_path)
            base_name = os.path.splitext(os.path.basename(pgn_path))[0]
            pdf_path = os.path.join(args.outdir, f"{base_name}.pdf")
            generate_pdf(moves, pdf_path)

            if not args.no_jpg:
                convert_pdf_to_jpg(pdf_path, args.outdir)

        except Exception as e:
            print(f"⚠️ Fehler bei {pgn_path}: {e}")

if __name__ == "__main__":
    main()
