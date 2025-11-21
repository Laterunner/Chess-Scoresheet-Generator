import os, time, zipfile
import chess.pgn
from tqdm import tqdm
from pdf2image import convert_from_path

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
