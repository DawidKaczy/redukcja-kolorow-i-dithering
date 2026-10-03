from PIL import Image
import numpy as np
from skimage.metrics import structural_similarity as ssim

def porownaj_ssim(img_path1, img_path2):
    img1 = Image.open(img_path1).convert("L")
    img2 = Image.open(img_path2).convert("L")

    img1_np = np.array(img1)
    img2_np = np.array(img2)
    score = ssim(img1_np, img2_np, full=True)
    return score
