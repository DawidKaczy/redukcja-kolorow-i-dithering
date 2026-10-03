from PIL import Image
import random


def zakres(value):
    return max(0, min(255, int(value)))

def kwantyzacja(obraz_in, ile_kolorow, seed=None):
    if seed is not None:
        random.seed(seed)

    ile_kolorow = ile_kolorow - 1
    obrazek = Image.open(obraz_in)
    obrazek = obrazek.convert("RGB")
    pixels = obrazek.load()
    szerokosc, wysokosc = obrazek.size

    for y in range(wysokosc):
        for x in range(szerokosc):
            oldR, oldG, oldB = pixels[x, y]

            noiseR = random.randint(-64, 64)
            noiseG = random.randint(-64, 64)
            noiseB = random.randint(-64, 64)

            tempR = zakres(oldR + noiseR)
            tempG = zakres(oldG + noiseG)
            tempB = zakres(oldB + noiseB)

            newR = round(ile_kolorow * tempR / 255) * (255 / ile_kolorow)
            newG = round(ile_kolorow * tempG / 255) * (255 / ile_kolorow)
            newB = round(ile_kolorow * tempB / 255) * (255 / ile_kolorow)

            pixels[x, y] = (
                zakres(newR),
                zakres(newG),
                zakres(newB)
            )

    return obrazek


def dithering(obraz_in, ile_kolorow, seed=None):
    if seed is not None:
        random.seed(seed)

    ile_kolorow = ile_kolorow - 1
    obrazek = Image.open(obraz_in).convert("RGB")
    pixels = obrazek.load()

    szerokosc, wysokosc = obrazek.size

    for y in range(wysokosc):
        for x in range(szerokosc):
            oldR, oldG, oldB = pixels[x, y]

            noiseR = random.randint(-64, 64)
            noiseG = random.randint(-64, 64)
            noiseB = random.randint(-64, 64)

            inputR = zakres(oldR + noiseR)
            inputG = zakres(oldG + noiseG)
            inputB = zakres(oldB + noiseB)

            newR = round(ile_kolorow * inputR / 255) * (255 / ile_kolorow)
            newG = round(ile_kolorow * inputG / 255) * (255 / ile_kolorow)
            newB = round(ile_kolorow * inputB / 255) * (255 / ile_kolorow)

            pixels[x, y] = (
                zakres(newR),
                zakres(newG),
                zakres(newB)
            )

            errR = inputR - newR
            errG = inputG - newG
            errB = inputB - newB

            if x + 1 < szerokosc:
                r, g, b = pixels[x + 1, y]
                pixels[x + 1, y] = (
                    zakres(r + errR * 7 / 16),
                    zakres(g + errG * 7 / 16),
                    zakres(b + errB * 7 / 16)
                )

            if x - 1 >= 0 and y + 1 < wysokosc:
                r, g, b = pixels[x - 1, y + 1]
                pixels[x - 1, y + 1] = (
                    zakres(r + errR * 3 / 16),
                    zakres(g + errG * 3 / 16),
                    zakres(b + errB * 3 / 16)
                )

            if y + 1 < wysokosc:
                r, g, b = pixels[x, y + 1]
                pixels[x, y + 1] = (
                    zakres(r + errR * 5 / 16),
                    zakres(g + errG * 5 / 16),
                    zakres(b + errB * 5 / 16)
                )

            if x + 1 < szerokosc and y + 1 < wysokosc:
                r, g, b = pixels[x + 1, y + 1]
                pixels[x + 1, y + 1] = (
                    zakres(r + errR * 1 / 16),
                    zakres(g + errG * 1 / 16),
                    zakres(b + errB * 1 / 16)
                )

    return obrazek