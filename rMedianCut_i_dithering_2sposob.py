from PIL import Image

def zakres(value):
    return max(0, min(255, int(value)))

def najblizszy_kolor(pixel, palette):
    r, g, b = pixel
    min_dist = float('inf')
    best_color = (0, 0, 0)
    for pr, pg, pb in palette:
        dist = (r - pr) ** 2 + (g - pg) ** 2 + (b - pb) ** 2
        if dist < min_dist:
            min_dist = dist
            best_color = (pr, pg, pb)
    return best_color

def median_cut(pixels, ile_kolorow):
    if ile_kolorow <= 0:
        return [(0,0,0)]
    boxes = [pixels[:]]
    while len(boxes) < ile_kolorow:
        boxes = [b for b in boxes if len(b) > 0]
        if not boxes:
            break
        max_range = -1
        idx_to_split = None
        for i, b in enumerate(boxes):
            r_vals = [p[0] for p in b]
            g_vals = [p[1] for p in b]
            b_vals = [p[2] for p in b]
            r_range = max(r_vals) - min(r_vals)
            g_range = max(g_vals) - min(g_vals)
            b_range = max(b_vals) - min(b_vals)
            rng = max(r_range, g_range, b_range)
            if rng > max_range:
                max_range = rng
                idx_to_split = i
        box = boxes.pop(idx_to_split)
        if len(box) <= 1:
            boxes.append(box)
            break
        r_vals = [p[0] for p in box]
        g_vals = [p[1] for p in box]
        b_vals = [p[2] for p in box]
        r_range = max(r_vals) - min(r_vals)
        g_range = max(g_vals) - min(g_vals)
        b_range = max(b_vals) - min(b_vals)
        if r_range >= g_range and r_range >= b_range:
            box.sort(key=lambda x: x[0])
        elif g_range >= r_range and g_range >= b_range:
            box.sort(key=lambda x: x[1])
        else:
            box.sort(key=lambda x: x[2])
        mid = len(box)//2
        boxes.append(box[:mid])
        boxes.append(box[mid:])
    palette = []
    for b in boxes:
        if len(b) == 0:
            palette.append((0,0,0))
            continue
        r = sum(p[0] for p in b)/len(b)
        g = sum(p[1] for p in b)/len(b)
        bl = sum(p[2] for p in b)/len(b)
        palette.append((int(round(r)), int(round(g)), int(round(bl))))
    return palette

def minimalizacja_kolorow(obraz_in, ile_kolorow):
    obrazek = Image.open(obraz_in)
    obrazek = obrazek.convert("RGB")
    pixels = obrazek.load()
    width, height = obrazek.size

    all_pixels = list(obrazek.getdata())
    palette = median_cut(all_pixels, ile_kolorow)

    for y in range(height):
        for x in range(width):
            old_pixel = pixels[x, y]
            new_pixel = najblizszy_kolor(old_pixel, palette)
            pixels[x, y] = new_pixel
    return obrazek

def median_cut_dithering(obraz_in, ile_kolorow):
    obrazek = Image.open(obraz_in)
    obrazek = obrazek.convert("RGB")
    pixels = obrazek.load()
    width, height = obrazek.size

    all_pixels = list(obrazek.getdata())
    palette = median_cut(all_pixels, ile_kolorow)

    for y in range(height):
        for x in range(width):
            old_pixel = pixels[x, y]
            new_pixel = najblizszy_kolor(old_pixel, palette)
            pixels[x, y] = new_pixel

            errR = old_pixel[0] - new_pixel[0]
            errG = old_pixel[1] - new_pixel[1]
            errB = old_pixel[2] - new_pixel[2]

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
