from PIL import Image, ImageDraw, ImageFont

RUGGINE = (143, 67, 42)        # --ruggine
RUGGINE_SCURA = (110, 50, 32)  # --ruggine-scura
TELA = (239, 231, 214)         # --tela
CARTA = (247, 242, 230)        # --carta
ORO = (185, 138, 61)           # --oro

FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"

def rounded(draw, box, r, fill):
    draw.rounded_rectangle(box, radius=r, fill=fill)

def make_icon(size, maskable=False, out="icon.png"):
    img = Image.new("RGB", (size, size), RUGGINE)
    d = ImageDraw.Draw(img)

    # cornice "da stampa" in oro (doppio filetto), come una vecchia edizione tipografica
    # zona sicura maskable = 80% centrale -> margini piu' ampi
    m = int(size * (0.16 if maskable else 0.075))
    w1 = max(2, size // 90)
    d.rectangle([m, m, size - m, size - m], outline=ORO, width=w1)
    m2 = m + max(3, size // 45)
    d.rectangle([m2, m2, size - m2, size - m2], outline=ORO, width=max(1, w1 // 2))

    # lettera "D" (Dizionèri) in tela, serif
    fsize = int(size * (0.42 if maskable else 0.52))
    font = ImageFont.truetype(FONT, fsize)
    text = "D"
    bbox = d.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    x = (size - tw) / 2 - bbox[0]
    y = (size - th) / 2 - bbox[1] - size * 0.015
    # leggera ombra tipografica
    d.text((x + size*0.008, y + size*0.008), text, font=font, fill=RUGGINE_SCURA)
    d.text((x, y), text, font=font, fill=CARTA)

    # sottotitolo: due frecce (italiano <-> romagnolo)
    fsize2 = int(size * (0.10 if maskable else 0.13))
    font2 = ImageFont.truetype(FONT, fsize2)
    t2 = "\u21c4"  # ⇄ (fallback: se il glifo manca, usare "IT-RO")
    b2 = d.textbbox((0, 0), t2, font=font2)
    if b2[2] - b2[0] <= 1:
        t2 = "IT\u00b7RO"
        b2 = d.textbbox((0, 0), t2, font=font2)
    x2 = (size - (b2[2] - b2[0])) / 2 - b2[0]
    y2 = size - m2 - (b2[3] - b2[1]) - size * (0.05 if maskable else 0.045) - b2[1]
    d.text((x2, y2), t2, font=font2, fill=ORO)

    img.save(out, "PNG")
    print(out, img.size)

make_icon(192, False, "icon-192.png")
make_icon(512, False, "icon-512.png")
make_icon(512, True,  "icon-maskable-512.png")
make_icon(180, False, "apple-touch-icon.png")
