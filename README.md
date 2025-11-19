# 🧾 Chess Scoresheet Generator

A practical Python tool for generating multi-page DIN A5 chess scoresheets from PGN files — perfect for tournaments, clubs, or personal archives.

## 🔧 Features

- Processes PGN files with one or multiple games
- Creates a clean, multi-column PDF scoresheet for each game
- Displays player names, date, event, and Elo ratings (if available)
- Optional: exports each PDF page as a high-resolution JPG
- Includes a progress bar using `tqdm` for smooth CLI feedback

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

## 🧠 Notes
•	Elo ratings are shown only if present in the PGN headers (WhiteElo, BlackElo)
•	Layout is optimized for DIN A5 — ideal for printing or digital archiving
•	JPG export uses pdf2image and requires Poppler

## 📜 License
This tool is free to use and can be adapted for club, tournament, or personal use.

