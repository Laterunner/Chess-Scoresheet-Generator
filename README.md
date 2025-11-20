# 🧾 Chess Scoresheet Generator

A practical Python tool for generating multi-page DIN A5 chess scoresheets from PGN files — perfect for tournaments, clubs, or personal archives.
![example_game2_Testperson_vs_Marius_page1](https://github.com/user-attachments/assets/2367cc7e-899d-44af-8a95-18d1b595e0f1)



## 🔧 Features

- Processes PGN files with one or multiple games
- Creates a clean, multi-column PDF scoresheet for each game
- Optional JPG export for each page
- Displays player names, date, event, and Elo ratings (if available)
- Includes a progress bar using `tqdm` for smooth CLI feedback
- DIN A5 layout (148 × 210 mm) for compact printing
- Optional logo in the top-right corner (e.g. club logo)
- Graceful fallback for missing PGN tags or logo
🖼️ Logo Support (Optional)

Place a file named logo.png in the same directory.Recommended: square, transparent PNG, approx. 100×100 px.


## 📦 Installation

1. Install Python 3.8 or higher
2. (Windows only) Install Poppler:
   - Download from [Poppler for Windows](https://github.com/oschwartz10612/poppler-windows/releases)
   - Extract and note the path to the `poppler/bin` folder
3. Install dependencies:
   bash pip install -r requirements.txt

## 📁 Output
For each game in the PGN file, the tool generates:
•	White_vs_Black_GameX.pdf
•	White_vs_Black_GameX_page_1.jpg, page_2.jpg, …

## 💻Examples how to use
	python scoresheet_generator.py game1.pgn game2.pgn
	python scoresheet_generator.py *.pgn --no-jpg
	python scoresheet_generator.py game.pgn --outdir scoresheets

	
## 🧠 Notes
•	Elo ratings are shown only if present in the PGN headers (WhiteElo, BlackElo)
•	Layout is optimized for DIN A5 — ideal for printing or digital archiving
•	JPG export uses pdf2image and requires Poppler

## 🛠️ To-Do / Ideas

[ ] ZIP export of all PDFs/JPGs

[ ] GUI or web frontend

[ ] Opening detection (ECO code)

[ ] Support for landscape or DIN A4

[ ] Footer with club name or website



## 📜 License
Open Source – MIT LicenseFree to use for clubs, tournaments, and personal archives.

