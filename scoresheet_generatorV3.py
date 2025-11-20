def generate_single_scoresheet(moves, title, output_pdf, jpg_enabled=True):
    os.makedirs(os.path.dirname(output_pdf), exist_ok=True)
    c = canvas.Canvas(output_pdf)

    # Split into chunks of 120 halfmoves (60 full moves)
    chunk_size = 120
    chunks = [moves[i:i + chunk_size] for i in range(0, len(moves), chunk_size)]

    for page_number, chunk in enumerate(chunks, start=1):
        draw_header(c, title=title, page_number=page_number)
        draw_scoresheet(c, chunk)
        c.showPage()

    c.save()

    # JPG export
    if jpg_enabled and os.path.exists(output_pdf) and os.path.getsize(output_pdf) > 0:
        try:
            time.sleep(0.5)
            images = convert_from_path(output_pdf, dpi=300)
            for i, img in enumerate(images):
                img_path = os.path.splitext(output_pdf)[0] + f"_page{i+1}.jpg"
                img.save(img_path, "JPEG")
        except Exception as e:
            print(f"⚠️ Fehler beim JPG-Export für {title}: {e}")
