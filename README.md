# 🧾 Chess Scoresheet Generator
A simple Python tool for generating professional multi-page DIN A5 chess scoresheets from PGN files 
— Supports CLI and GUI usage customizable branding and club-ready PDF output.

## 🔧 Features
- Processes PGN files with one or multiple games
- Creates a clean, multi-column PDF scoresheet for each game
- Optional JPG export for each page
- ZIP export of all PDFs/JPGs
- Supports very long Games (unlimited move numbers)
- Displays player names, date, event, and Elo ratings (if available)
- Includes a progress bar using `tqdm` for smooth CLI feedback
- DIN A5 layout (148 × 210 mm) for compact printing
- Optional logo/branding in the top-right corner (e.g. club logo)
- Graceful fallback for missing PGN tags or logo
- Logo top left corner (Optional)
- Footline for email and weblink
- Supports CLI and GUI usage
- Can be installed dierectly from PyPI
- included is a pgn file with 128 German Bundesliga games for testing

## 📦 The Program can be installed directly from PyPI:
	https://pypi.org/project/chess-scoresheet-generator
	pip install chess-scoresheet-generator
	you than can start from cli with scoresheet-generator or scoresheet-gui

## 📦 Alternative way to install: 
1. Install Python 3.8 or higher
2. (Windows only) Install Poppler:
   - Download from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)
   - Extract and note the path to the `poppler/bin` folder
3. Install dependencies:
   bash pip install -r requirements.txt
4. If a logo is wanted, place a file named logo.png in the same directory.
   Recommended: square, transparent PNG, approx. 100×100 px.


## 📁 Output:
	For each game in the PGN file, the tool generates:
•	White_vs_Black_GameX.pdf
•	White_vs_Black_GameX_page_1.jpg, page_2.jpg, …


## 💻Examples how to use
	python scoresheet -h for help
	python scoresheet_generator.py game1.pgn game2.pgn 
	python scoresheet_generator.py *.pgn
	pyton scoresheet_generator.py  games.pgn --jpg Enable JPG export (disabled by default)
	python scoresheet_generator.py games.pgn --outdir scoresheets

	For testing files  with single and multiple games three example.pgn files  are included. 
	JPG conversion takes some time, it must be enabled with the --jpg flag or using the GUI.

	
## 🧠 Notes
•	Elo ratings are shown only if present in the PGN headers (WhiteElo, BlackElo)
•	Layout is optimized for DIN A5 — ideal for printing or digital archiving
•	JPG export uses pdf2image and requires Poppler


## 🛠️ To-Do / Ideas
[ ] Opening detection (ECO code)
[ ] Support for landscape or DIN A4


## 📜 License
Open Source – MIT LicenseFree to use for clubs, tournaments, and personal archives.

## Example Scoresheet (JPG)

![example1_game1_Ray_vs_Xavier pdf_page1](https://github.com/user-attachments/assets/d49bc09d-d0db-4db7-ac10-f0a6b361b9e5)
