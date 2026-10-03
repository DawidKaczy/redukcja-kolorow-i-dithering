from flask import Flask, render_template, request, redirect, url_for

from rRedukcja_i_dithering_1sposob import kwantyzacja as kwantyzacja_baza, dithering as dithering_baza
from rRedukcja_i_dithering_1sposob_i_szum import kwantyzacja as kwantyzacja_szum, dithering as dithering_szum

from rMedianCut_i_dithering_2sposob import minimalizacja_kolorow, median_cut_dithering
from aPrownanie import porownaj_ssim

from ileKolorow import policz_kolory

import os
import random
import sys
app = Flask(__name__)
UPLOADS_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
os.makedirs(UPLOADS_FOLDER, exist_ok=True)

obrazy_do_analizy = {
    "oryginalny": os.path.join("static", "uploads", "oryginalny_obraz.png"),
    "kwantyzacja": os.path.join("static", "uploads", "kwantyzacja_obraz.png"),
    "median_cut": os.path.join("static", "uploads", "minimalizacja_kolorow_obraz.png"),
    "dithering": os.path.join("static", "uploads", "dithering_obraz.png"),
    "median_cut_dithering": os.path.join("static", "uploads", "median_cut_dithering_obraz.png"),
}


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("obraz")
        slider_value = request.form.get("slider_value")
        czy_dodac_szum = request.form.get("dodaj_szum")

        if file and file.filename:
            obraz_path = os.path.join(UPLOADS_FOLDER, "oryginalny_obraz.png")
            file.save(obraz_path)

            try:
                slider_value = int(slider_value)
            except (TypeError, ValueError):
                slider_value = 128

            slider_wynik = slider_value * slider_value * slider_value

            if czy_dodac_szum:
                moj_seed = random.randrange(sys.maxsize)
                obraz_kwantyzacja = kwantyzacja_szum(obraz_path, slider_value, seed=moj_seed)
                obraz_dithering = dithering_szum(obraz_path, slider_value, seed=moj_seed)
            else:
                obraz_kwantyzacja = kwantyzacja_baza(obraz_path, slider_value)
                obraz_dithering = dithering_baza(obraz_path, slider_value)

            kwantyzacja_path = os.path.join(UPLOADS_FOLDER, "kwantyzacja_obraz.png")
            obraz_kwantyzacja.save(kwantyzacja_path)

            prownanie_kwantyzacja = porownaj_ssim(obraz_path, kwantyzacja_path)

            dithering_path = os.path.join(UPLOADS_FOLDER, "dithering_obraz.png")
            obraz_dithering.save(dithering_path)

            prownanie_dithering = porownaj_ssim(obraz_path, dithering_path)

            obraz_median_cut = minimalizacja_kolorow(obraz_path, slider_value)
            minimalizacja_kolorow_path = os.path.join(UPLOADS_FOLDER, "minimalizacja_kolorow_obraz.png")
            obraz_median_cut.save(minimalizacja_kolorow_path)

            prownanie_minimalizacja = porownaj_ssim(obraz_path, minimalizacja_kolorow_path)

            obraz_median_cut_dithering = median_cut_dithering(obraz_path, slider_value)
            median_cut_dithering_path = os.path.join(UPLOADS_FOLDER, "median_cut_dithering_obraz.png")
            obraz_median_cut_dithering.save(median_cut_dithering_path)

            prownanie_median_cut_dithering = porownaj_ssim(obraz_path, median_cut_dithering_path)


            kolory_org = policz_kolory(obraz_path)
            kolory_kwant = policz_kolory(obraz_kwantyzacja)
            kolory_dith = policz_kolory(obraz_dithering)
            kolory_median = policz_kolory(obraz_median_cut)
            kolory_median_dith = policz_kolory(obraz_median_cut_dithering)

            return redirect(url_for(
                "indexv2",
                filename="oryginalny_obraz.png",
                filename2="kwantyzacja_obraz.png",
                filename3="dithering_obraz.png",
                filename4="minimalizacja_kolorow_obraz.png",
                filename5="median_cut_dithering_obraz.png",
                slider=slider_value,
                slider_wynik=slider_wynik,
                kwantyzacja_wynik=prownanie_kwantyzacja,
                dithering_wynik=prownanie_dithering,
                minimalizacja_wynik=prownanie_minimalizacja,
                median_cut_dithering_wynik=prownanie_median_cut_dithering,

                k_org = kolory_org,
                k_kwant = kolory_kwant,
                k_dith = kolory_dith,
                k_median = kolory_median,
                k_median_dith = kolory_median_dith,
            ))

    return render_template("index.html")

@app.route("/indexv2")
def indexv2():
    filename = request.args.get("filename")
    filename2 = request.args.get("filename2")
    filename3 = request.args.get("filename3")
    filename4 = request.args.get("filename4")
    filename5 = request.args.get("filename5")

    slider = request.args.get("slider")
    slider_wynik = int(request.args.get("slider_wynik"))
    kwantyzacja_wynik = float(request.args.get("kwantyzacja_wynik"))
    dithering_wynik = float(request.args.get("dithering_wynik"))
    minimalizacja_wynik = float(request.args.get("minimalizacja_wynik"))
    median_cut_dithering_wynik = float(request.args.get("median_cut_dithering_wynik"))

    k_org = request.args.get("k_org")
    k_kwant = request.args.get("k_kwant")
    k_dith = request.args.get("k_dith")
    k_median = request.args.get("k_median")
    k_median_dith = request.args.get("k_median_dith")

    return render_template(
        "indexv2.html",
        obraz_oryginalny=f"uploads/{filename}",
        obraz_kwantyzacja=f"uploads/{filename2}",
        obraz_dithering=f"uploads/{filename3}",
        obraz_median_cut=f"uploads/{filename4}",
        obraz_median_cut_dithering=f"uploads/{filename5}",
        slider=slider,
        slider_wynik=slider_wynik,
        kwantyzacja_wynik=kwantyzacja_wynik,
        dithering_wynik=dithering_wynik,
        minimalizacja_wynik=minimalizacja_wynik,
        median_cut_dithering_wynik=median_cut_dithering_wynik,

        c_org=k_org,
        c_kwant=k_kwant,
        c_dith=k_dith,
        c_median=k_median,
        c_median_dith=k_median_dith,
    )


@app.route("/indexv3")
def indexv3():
    filename5 = request.args.get("filename5")
    filename3 = request.args.get("filename3")

    c_dith = request.args.get("c_dith")
    c_median_dith = request.args.get("c_median_dith")

    return render_template(
        "indexv3.html",
        obraz_dithering=f"uploads/{filename3}",
        c_dith=c_dith,
        obraz_median_cut_dithering=f"uploads/{filename5}",
        c_median_dith=c_median_dith
    )


if __name__ == "__main__":
    app.run(debug=True)