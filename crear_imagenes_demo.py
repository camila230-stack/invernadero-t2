"""Script para generar imágenes de demo si no hay imágenes reales."""
import numpy as np
import cv2
import os

os.makedirs("assets/images", exist_ok=True)

def crear_hoja(nombre, tipo):
    h, w = 300, 400
    img = np.zeros((h, w, 3), dtype=np.uint8)

    if tipo == "sana":
        img[:] = [34, 139, 34]
        cv2.ellipse(img, (200, 150), (160, 120), 0, 0, 360, [45, 160, 45], -1)
    elif tipo == "enferma":
        img[:] = [34, 100, 34]
        cv2.ellipse(img, (200, 150), (160, 120), 0, 0, 360, [40, 130, 40], -1)
        cv2.circle(img, (120, 100), 40, [180, 140, 20], -1)
        cv2.circle(img, (280, 180), 30, [139, 90, 43], -1)
        cv2.ellipse(img, (190, 200), (55, 35), 30, 0, 360, [160, 120, 30], -1)
    elif tipo == "estres":
        img[:] = [50, 120, 50]
        cv2.ellipse(img, (200, 150), (160, 120), 0, 0, 360, [60, 140, 60], -1)
        cv2.circle(img, (150, 130), 20, [160, 140, 40], -1)
        cv2.circle(img, (240, 160), 15, [150, 130, 50], -1)

    cv2.imwrite(f"assets/images/{nombre}.jpg", img)
    print(f"✅ Creada: assets/images/{nombre}.jpg")

crear_hoja("hoja1", "sana")
crear_hoja("hoja2", "enferma")
crear_hoja("hoja3", "estres")
print("Imágenes de demo creadas.")
