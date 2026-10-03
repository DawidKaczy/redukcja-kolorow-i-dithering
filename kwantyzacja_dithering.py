from PIL import Image

def zakres(value):
    return max(0, min(255, int(value)))

def kwantyzacja(obraz_in, ile_kolorow):
    ile_kolorow = ile_kolorow - 1
    obrazek = Image.open(obraz_in)
    obrazek = obrazek.convert("RGB")
    pixels = obrazek.load()
    szerokosc, wysokosc = obrazek.size

    for y in range(wysokosc):
        for x in range(szerokosc):
            oldR, oldG, oldB = pixels[x, y]

            if ile_kolorow > 0:
                nowy_r = round(ile_kolorow * oldR / 255) * (255 / ile_kolorow)
                nowy_g = round(ile_kolorow * oldG / 255) * (255 / ile_kolorow)
                nowy_b = round(ile_kolorow * oldB / 255) * (255 / ile_kolorow)
            else:
                nowy_r, nowy_g, nowy_b = 0, 0, 0

            pixels[x, y] = (
                zakres(nowy_r),
                zakres(nowy_g),
                zakres(nowy_b)
            )
    return obrazek

def dithering(obraz_in, ile_kolorow):
    ile_kolorow = ile_kolorow - 1
    obrazek = Image.open(obraz_in)
    obrazek = obrazek.convert("RGB")
    pixels = obrazek.load()
    width, height = obrazek.size

    for y in range(height):
        for x in range(width):
            oldR, oldG, oldB = pixels[x, y]

            newR = round(ile_kolorow * oldR / 255) * (255 / ile_kolorow)
            newG = round(ile_kolorow * oldG / 255) * (255 / ile_kolorow)
            newB = round(ile_kolorow * oldB / 255) * (255 / ile_kolorow)

            pixels[x, y] = (
                zakres(newR),
                zakres(newG),
                zakres(newB)
            )

            errR = oldR - newR
            errG = oldG - newG
            errB = oldB - newB

            if x + 1 < width:
                r, g, b = pixels[x + 1, y]
                pixels[x + 1, y] = (
                    zakres(r + errR * 7 / 16.0),
                    zakres(g + errG * 7 / 16.0),
                    zakres(b + errB * 7 / 16.0)
                )

            if x - 1 >= 0 and y + 1 < height:
                r, g, b = pixels[x - 1, y + 1]
                pixels[x - 1, y + 1] = (
                    zakres(r + errR * 3 / 16.0),
                    zakres(g + errG * 3 / 16.0),
                    zakres(b + errB * 3 / 16.0)
                )

            if y + 1 < height:
                r, g, b = pixels[x, y + 1]
                pixels[x, y + 1] = (
                    zakres(r + errR * 5 / 16.0),
                    zakres(g + errG * 5 / 16.0),
                    zakres(b + errB * 5 / 16.0)
                )

            if x + 1 < width and y + 1 < height:
                r, g, b = pixels[x + 1, y + 1]
                pixels[x + 1, y + 1] = (
                    zakres(r + errR * 1 / 16.0),
                    zakres(g + errG * 1 / 16.0),
                    zakres(b + errB * 1 / 16.0)
                )
    return obrazek


