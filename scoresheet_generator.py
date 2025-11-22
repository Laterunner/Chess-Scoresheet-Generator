#Final Version 11.25
import os, time, zipfile
import argparse
import chess.pgn
from datetime import datetime
from tqdm import tqdm
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A5
from reportlab.lib.utils import ImageReader
from pdf2image import convert_from_path


def format_pgn_date(date_str):
    try:
        dt = datetime.strptime(date_str, "%Y.%m.%d")
        return dt.strftime("%#d. %B %Y")  # %-d für Linux/macOS
    except Exception:
        return date_str

def draw_metadata_header(c, headers, page_number):
    y = 570
    logo_path = "logo.png"

    try:
        if os.path.exists(logo_path):
            logo = ImageReader(logo_path)
            c.drawImage(logo, x=330, y=y - 20, width=30, height=30, preserveAspectRatio=True, mask='auto')
    except Exception as e:
        print(f"⚠️ Logo konnte nicht geladen werden: {e}")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(30, y, f"{headers['White']} vs {headers['Black']} – Seite {page_number}")

    c.setFont("Helvetica", 9)
    y -= 12
    c.drawString(30, y, f"Event:  {headers['Event']}")

    y -= 12
    c.drawString(30, y, f"Ort:    {headers['Site']}")

    y -= 12
    c.drawString(30, y, f"Datum:  {format_pgn_date(headers['Date'])}")
    c.drawString(180, y, f"Runde:  {headers['Round']}")

    y -= 12
    c.drawString(30, y, f"Weiß:   {headers['White']}")
    c.drawString(180, y, f"Schwarz:{headers['Black']}")

    y -= 12
    c.drawString(30, y, f"ELO:    {headers['WhiteElo']}")
    c.drawString(180, y, f"ELO:    {headers['BlackElo']}")
    c.drawString(320, y, f"Ergebnis:  {headers['Result']}")

    y -= 8
    c.line(30, y, 380, y)

    return y - 20  # Abstand zur Notation
   
def draw_scoresheet(c, moves, x_start=30, y_start=620, column_spacing=110, row_spacing=18, black_offset=45):
    max_full_moves_per_column = 20

    # Vertikale Linien
    c.setStrokeColorRGB(0.7, 0.7, 0.7)
    c.setLineWidth(0.5)
    for i in range(1, 3):
        x = x_start + i * column_spacing - 10
        c.line(x, y_start + 5, x, y_start - max_full_moves_per_column * row_spacing)

    # Zugnotation
    c.setFont("Helvetica", 9)
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

#NEW FOR TESTING---------------------------------------------------------------------------
def generate_single_scoresheet(moves, headers, output_pdf, jpg_enabled=True):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    c = canvas.Canvas(output_pdf, pagesize=A5)
    width, height = A5

    chunk_size = 120
    chunks = [moves[i:i + chunk_size] for i in range(0, len(moves), chunk_size)]

    for page_number, chunk in enumerate(chunks, start=1):
        # Draw header + moves
        y_start = draw_metadata_header(c, headers, page_number)
        draw_scoresheet(c, chunk, y_start=y_start)

        # --- Footer integration ---
        c.setFont("Helvetica", 7)
        footer_text = "Contact: laterunner@gmail.com.org | https://lichess.org"
        # Horizontal line above footer
        c.line(30, 50, width - 30, 50)
        # Centered footer text
        c.drawCentredString(width / 2.0, 25, footer_text)

        # Finalize this page
        c.showPage()

    c.save()

    if jpg_enabled and os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
        try:
            time.sleep(0.5)
            images = convert_from_path(output_pdf, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.splitext(output_pdf)[0] + f"_page{i+1}.jpg"
                img.save(img_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Fehler beim JPG-Export für {headers['White']} vs {headers['Black']}: {e}")


def convert_pdf_to_jpg(pdf_path, output_dir):
    """
    Convert a PDF to JPG images (one per page) with a nested progress bar.
    """
    pages = convert_from_path(pdf_path, dpi=300)
    for i, page in enumerate(tqdm(pages, desc="Converting to JPG", unit="page", leave=False)):
        jpg_path = os.path.join(output_dir, f"{os.path.basename(pdf_path)}_page{i+1}.jpg")
        page.save(jpg_path, "JPEG")

def generate_scoresheets_from_pgn_file(pgn_path, output_dir, jpg_enabled=True):
    """
    Process a PGN file and generate scoresheets (PDF and optional JPG).
    Show progress bars with average time per game.
    Finally, create a ZIP archive containing all generated files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Collect all games first
    games = []
    with open(pgn_path, "r", encoding="utf-8") as f:
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break
            games.append(game)

    total_games = len(games)
    start_time = time.time()

    # Outer progress bar for games
    with tqdm(total=total_games, desc="Processing games", unit="game") as pbar:
        for game_index, game in enumerate(games, start=1):
            game_start = time.time()

            moves = [move for move in game.mainline_moves()]
            headers = game.headers

            base_name = os.path.splitext(os.path.basename(pgn_path))[0]
            output_pdf = os.path.join(
                output_dir,
                f"{base_name}_game{game_index}_{headers.get('White','?')}_vs_{headers.get('Black','?')}.pdf"
            )

            # Generate PDF (without JPG inside)
            generate_single_scoresheet(moves, headers, output_pdf, jpg_enabled=False)

            # JPG conversion with nested bar
            if jpg_enabled:
                convert_pdf_to_jpg(output_pdf, output_dir)

            # Update outer bar after full game done
            pbar.update(1)

            # Show average time per game so far
            elapsed = time.time() - start_time
            avg_time = elapsed / game_index
            pbar.set_postfix_str(f"avg {avg_time:.1f}s/game")

            # Optional: per-game duration
            # print(f"Game {game_index} took {time.time() - game_start:.1f}s")

    # ➡️ Create ZIP archive after processing all games
    base_name = os.path.splitext(os.path.basename(pgn_path))[0]
    zip_path = os.path.join(output_dir, f"{base_name}_Scoresheets.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                # Only include files belonging to this PGN (PDF + JPG)
                if file.startswith(base_name) and (file.endswith(".pdf") or file.endswith(".jpg")):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, output_dir)
                    zipf.write(full_path, arcname)

    print(f"📦 ZIP archive created: {zip_path}")

'''
def generate_scoresheets_from_pgn_file(pgn_path, output_dir, jpg_enabled=True):
    """
    Process a PGN file and generate scoresheets (PDF and optional JPG).
    After processing, create a ZIP archive containing all generated files.
    """
    os.makedirs(output_dir, exist_ok=True)

    with open(pgn_path, "r", encoding="utf-8") as f:
        game_index = 1
        while True:
            game = chess.pgn.read_game(f)
            if game is None:
                break

            # Extract moves and headers from the game
            moves = [move for move in game.mainline_moves()]
            headers = game.headers

            # Build output filename
            base_name = os.path.splitext(os.path.basename(pgn_path))[0]
            output_pdf = os.path.join(
                output_dir,
                f"{base_name}_game{game_index}_{headers.get('White','?')}_vs_{headers.get('Black','?')}.pdf"
            )

            # Generate single scoresheet (PDF + optional JPG)
            generate_single_scoresheet(moves, headers, output_pdf, jpg_enabled)

            game_index += 1

    # ➡️ Create ZIP archive after processing all games
    base_name = os.path.splitext(os.path.basename(pgn_path))[0]
    zip_path = os.path.join(output_dir, f"{base_name}_Scoresheets.zip")

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(output_dir):
            for file in files:
                # Only include files belonging to this PGN (PDF + JPG)
                if file.startswith(base_name) and (file.endswith(".pdf") or file.endswith(".jpg")):
                    full_path = os.path.join(root, file)
                    arcname = os.path.relpath(full_path, output_dir)
                    zipf.write(full_path, arcname)

    print(f"📦 ZIP archive created: {zip_path}")
'''

def main():
    parser = argparse.ArgumentParser(description="Erzeuge Scoresheets aus PGN-Dateien.")
    parser.add_argument("pgn_files", nargs="+", help="Pfad zu einer oder mehreren PGN-Dateien")
    parser.add_argument("--jpg", action="store_true", help="Enable JPG export (disabled by default)")
    parser.add_argument("--outdir", default="output", help="Zielverzeichnis für PDF/JPG")
    args = parser.parse_args()

    for pgn_path in tqdm(args.pgn_files, desc="Verarbeite PGN-Dateien"):
        try: 
            generate_scoresheets_from_pgn_file(pgn_path, args.outdir, jpg_enabled=args.jpg)
        except Exception as e:
            print(f"⚠️ Fehler bei {pgn_path}: {e}")

if __name__ == "__main__":
    main()
