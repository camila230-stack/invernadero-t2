# =============================================================
# MÓDULO: agente_imagenes.py
# RESPONSABLE: Integrante 3
# FUNCIÓN: Procesamiento básico de imágenes de hojas de plantas
#          usando OpenCV para detectar indicios de estrés/enfermedad.
# =============================================================

import cv2
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import urllib.request
import os


# ── Utilidad: obtener imagen (descarga si no existe) ────────
def obtener_imagen_demo(ruta: str) -> np.ndarray:
    """
    Carga una imagen desde disco. Si no existe, crea una imagen
    sintética de hoja para demostración.
    """
    if Path(ruta).exists():
        img = cv2.imread(ruta)
        if img is not None:
            return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Imagen sintética: fondo verde con manchas amarillas/marrones
    alto, ancho = 300, 400
    img = np.zeros((alto, ancho, 3), dtype=np.uint8)
    # Hoja verde
    img[:, :] = [34, 139, 34]
    # Manchas de enfermedad (amarillo-marrón)
    cv2.circle(img, (120, 100), 35, (180, 140, 20), -1)
    cv2.circle(img, (280, 200), 25, (139, 90, 43), -1)
    cv2.ellipse(img, (200, 150), (50, 30), 30, 0, 360, (160, 120, 30), -1)
    # Borde oscuro de la hoja
    cv2.rectangle(img, (10, 10), (ancho - 10, alto - 10), (20, 80, 20), 8)
    return img


# ── Paso 1: Conversión a escala de grises ───────────────────
def convertir_grises(imagen_rgb: np.ndarray) -> np.ndarray:
    """Convierte la imagen RGB a escala de grises."""
    return cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2GRAY)


# ── Paso 2: Umbralización (thresholding) ────────────────────
def aplicar_umbral(gris: np.ndarray, umbral: int = 100) -> np.ndarray:
    """
    Binariza la imagen: píxeles por debajo del umbral → negro,
    por encima → blanco. Útil para separar zonas dañadas del fondo.
    """
    _, binaria = cv2.threshold(gris, umbral, 255, cv2.THRESH_BINARY)
    return binaria


# ── Paso 3: Detección de bordes (Canny) ─────────────────────
def detectar_bordes(gris: np.ndarray) -> np.ndarray:
    """
    Aplica el algoritmo Canny para detectar bordes.
    Bordes irregulares o manchas con borde bien definido
    pueden indicar lesiones en la hoja.
    """
    return cv2.Canny(gris, threshold1=50, threshold2=150)


# ── Paso 4: Segmentación por color (HSV) ────────────────────
def segmentar_zonas_danadas(imagen_rgb: np.ndarray) -> tuple[np.ndarray, float]:
    """
    Segmenta las zonas amarillo-marrones (posible enfermedad/estrés)
    usando el espacio de color HSV.

    Returns:
        mascara: imagen binaria donde blanco = zona afectada
        porcentaje: fracción del área afectada sobre el total
    """
    hsv = cv2.cvtColor(imagen_rgb, cv2.COLOR_RGB2HSV)

    # Rango HSV para amarillo-marrón (hojas enfermas)
    bajo_amarillo = np.array([15, 50, 50])
    alto_amarillo = np.array([35, 255, 255])
    bajo_marron = np.array([5, 40, 30])
    alto_marron = np.array([15, 200, 180])

    mascara_amarillo = cv2.inRange(hsv, bajo_amarillo, alto_amarillo)
    mascara_marron = cv2.inRange(hsv, bajo_marron, alto_marron)
    mascara = cv2.bitwise_or(mascara_amarillo, mascara_marron)

    total_pixeles = imagen_rgb.shape[0] * imagen_rgb.shape[1]
    pixeles_afectados = np.count_nonzero(mascara)
    porcentaje = round((pixeles_afectados / total_pixeles) * 100, 2)

    return mascara, porcentaje


# ── Resultado principal: análisis completo ──────────────────
def analizar_hoja(ruta_imagen: str) -> dict:
    """
    Ejecuta el pipeline completo de análisis sobre una imagen de hoja.

    Returns:
        dict con imagen original, grises, bordes, segmentación
        y diagnóstico textual.
    """
    original = obtener_imagen_demo(ruta_imagen)
    gris = convertir_grises(original)
    binaria = aplicar_umbral(gris, umbral=90)
    bordes = detectar_bordes(gris)
    mascara, porcentaje_dano = segmentar_zonas_danadas(original)

    # Diagnóstico basado en porcentaje de área afectada
    if porcentaje_dano > 20:
        diagnostico = "🔴 Enfermedad probable — área afectada significativa"
        estado = "enfermedad"
    elif porcentaje_dano > 8:
        diagnostico = "🟡 Estrés moderado — revisar condiciones de riego y luz"
        estado = "estres"
    else:
        diagnostico = "🟢 Hoja en buen estado aparente"
        estado = "saludable"

    return {
        "ruta": ruta_imagen,
        "original": original,
        "grises": gris,
        "binaria": binaria,
        "bordes": bordes,
        "mascara_dano": mascara,
        "porcentaje_dano": porcentaje_dano,
        "diagnostico": diagnostico,
        "estado": estado,
    }


def graficar_procesamiento(resultado: dict) -> plt.Figure:
    """
    Muestra el pipeline de procesamiento en una figura de 5 paneles.
    """
    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    fig.suptitle(
        f"Procesamiento de hoja — Área afectada: {resultado['porcentaje_dano']}%",
        fontsize=12, fontweight="bold"
    )

    paneles = [
        (resultado["original"], "Original", "viridis"),
        (resultado["grises"], "Escala de grises", "gray"),
        (resultado["binaria"], "Umbralización", "gray"),
        (resultado["bordes"], "Detección de bordes", "gray"),
        (resultado["mascara_dano"], "Zonas dañadas", "hot"),
    ]

    for ax, (img, titulo, cmap) in zip(axes, paneles):
        if len(img.shape) == 3:
            ax.imshow(img)
        else:
            ax.imshow(img, cmap=cmap)
        ax.set_title(titulo, fontsize=9)
        ax.axis("off")

    plt.tight_layout()
    return fig


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    rutas = [
        "assets/images/hoja1.jpg",
        "assets/images/hoja2.jpg",
        "assets/images/hoja3.jpg",
    ]
    for ruta in rutas:
        resultado = analizar_hoja(ruta)
        print(f"{ruta}: {resultado['diagnostico']} ({resultado['porcentaje_dano']}%)")
        fig = graficar_procesamiento(resultado)
        plt.show()
