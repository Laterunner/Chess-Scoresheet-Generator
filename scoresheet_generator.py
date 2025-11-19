import argparse
import os
import chess.pgn
from reportlab.lib.pagesizes import A5
from reportlab.pdfgen import canvas
from pdf2image import convert_from_path
from tqdm import tqdm

def pgn_to_scoresheet_unlimited(game, output_pdf, export_jpg=True, dpi=300, poppler_path=None):
    """
    Erstellt ein mehrseitiges DIN A5 Scoresheet für eine einzelne Partie.
    Optional: Export jeder Seite als JPG.
    """
    moves = []
    node = game
    while node.variations:
        node = node.variations[0]
        moves.append(node.san())

    c = canvas.Canvas(output_pdf, pagesize=A5)
    width, height = A5
    x_positions = [40, 150, 260]
    lines_per_page = 20
    total_pairs = (len(moves) + 1) // 2
    move_number = 1
    i = 0
    page = 1

    while move_number <= total_pairs:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, height - 40, f"Schach Scoresheet – Seite {page}")
        c.setFont("Helvetica", 9)
        if page == 1:
            c.drawString(40, height - 60, f"Event: {game.headers.get('Event', '')}")
            c.drawString(40, height - 75, f"Date: {game.headers.get('Date', '')}")
            c.drawString(40, height - 90, f"White: {game.headers.get('White', '')}")
            c.drawString(40, height - 105, f"Black: {game.headers.get('Black', '')}")
            white_elo = game.headers.get("WhiteElo")
            black_elo = game.headers.get("BlackElo")
            if white_elo:
                c.drawString(250, height - 90, f"Elo: {white_elo}")
            if black_elo:
                c.drawString(250, height - 105, f"Elo: {black_elo}")

        y = height - 130
        for line in range(lines_per_page):
            for col in range(3):
                if move_number > total_pairs:
                    break
                if i + 1 < len(moves):
                    white = moves[i]
                    black = moves[i + 1]
                    i += 2
                elif i < len(moves):
                    white = moves[i]
                    black = "____"
                    i += 1
                else:
                    white = "____"
                    black = "____"
                text = f"{move_number}. {white} {black}"
                c.drawString(x_positions[col], y, text)
                move_number += 1
            y -= 12
        c.showPage()
        page += 1

    c.save()

    if export_jpg:
        pages = convert_from_path(output_pdf, dpi=dpi, poppler_path=poppler_path)
        for i, page_img in enumerate(pages):
            page_img.save(f"{output_pdf.replace('.pdf', '')}_page_{i+1}.jpg", "JPEG")

def generate_all_scoresheets(pgn_path, output_dir, export_jpg=True, dpi=300, poppler_path=None):
    os.makedirs(output_dir, exist_ok=True)
    with open(pgn_path, "r", encoding="utf-8") as f:
        games = list(iter(lambda: chess.pgn.read_game(f), None))

    for i, game in enumerate(tqdm(games, desc="Erzeuge Scoresheets", unit="Partie")):
        white = game.headers.get("White", f"White{i+1}")
        black = game.headers.get("Black", f"Black{i+1}")
        filename_base = f"{white}_vs_{black}_Game{i+1}".replace(" ", "_")
        output_pdf = os.path.join(output_dir, f"{filename_base}.pdf")
        pgn_to_scoresheet_unlimited(game, output_pdf, export_jpg, dpi, poppler_path)

def main():
    parser = argparse.ArgumentParser(description="Erzeuge Scoresheets aus einer PGN-Datei.")
    parser.add_argument("pgn", help="Pfad zur PGN-Datei mit einer oder mehreren Partien")
    parser.add_argument("-o", "--output", default="scoresheets", help="Ausgabeordner für PDF/JPG")
    parser.add_argument("--no-jpg", action="store_true", help="Nur PDF erzeugen, keine JPGs")
    parser.add_argument("--dpi", type=int, default=300, help="DPI für JPG-Export (Standard: 300)")
    parser.add_argument("--poppler", help="Pfad zu Poppler (nur unter Windows nötig)")

    args = parser.parse_args()
    generate_all_scoresheets(
        pgn_path=args.pgn,
        output_dir=args.output,
        export_jpg=not args.no_jpg,
        dpi=args.dpi,
        poppler_path=args.poppler
    )

if __name__ == "__main__":
    main()
