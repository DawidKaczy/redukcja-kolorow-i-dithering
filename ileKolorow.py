from PIL import Image


def policz_kolory(obraz_input):
    if isinstance(obraz_input, str):
        img = Image.open(obraz_input)
    else:
        img = obraz_input

    img = img.convert("RGB")

    unikalne_kolory = set(img.getdata())

    return len(unikalne_kolory)