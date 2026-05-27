# =============================================================
# MÓDULO: paralelismo.py
# RESPONSABLE: Integrante 2
# FUNCIÓN: Ejecuta múltiples agentes de forma concurrente
#          usando threading para simular trabajo paralelo.
# =============================================================

import threading
import time
import queue
from datetime import datetime


# Cola compartida donde los agentes depositan sus resultados
cola_resultados = queue.Queue()


def tarea_analizar_senales(datos: dict, log: list) -> None:
    """
    Hilo 1: Simula el análisis de señales temporales.
    Escribe su resultado en la cola compartida.
    """
    inicio = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{inicio}] 🔵 Hilo Señales — iniciado")
    time.sleep(1.2)  # simula tiempo de procesamiento

    resultado = {
        "agente": "AgenteSeñales",
        "estado": "temperatura_alta" if datos.get("temperatura", 0) > 30 else "temperatura_normal",
        "alertas": [],
    }
    if datos.get("humedad_suelo", 50) < 35:
        resultado["alertas"].append("humedad_suelo_baja")

    fin = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{fin}] 🔵 Hilo Señales — completado: {resultado['estado']}")
    cola_resultados.put(resultado)


def tarea_procesar_imagenes(ruta_imagen: str, log: list) -> None:
    """
    Hilo 2: Simula el procesamiento de imágenes con OpenCV.
    En producción llama a agente_imagenes; aquí simula el tiempo.
    """
    inicio = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{inicio}] 🟢 Hilo Imágenes — iniciado ({ruta_imagen})")
    time.sleep(1.8)  # OpenCV tarda un poco más

    resultado = {
        "agente": "AgenteImagenes",
        "imagen": ruta_imagen,
        "estado_hoja": "posible_enfermedad" if "enferma" in ruta_imagen else "saludable",
        "confianza": 0.73,
    }

    fin = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{fin}] 🟢 Hilo Imágenes — completado: {resultado['estado_hoja']}")
    cola_resultados.put(resultado)


def tarea_emitir_decision(esperar_segundos: float, log: list) -> None:
    """
    Hilo 3: Agente decisor. Espera a que los otros terminen
    (simulado) y luego emite la recomendación final.
    """
    inicio = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{inicio}] 🟠 Hilo Decisor — esperando resultados...")
    time.sleep(esperar_segundos)

    resultado = {
        "agente": "AgenteDecisor",
        "recomendacion": "Regar ahora — humedad crítica detectada",
        "nivel_riesgo": "ALTO",
    }

    fin = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    log.append(f"[{fin}] 🟠 Hilo Decisor — decisión emitida: {resultado['recomendacion']}")
    cola_resultados.put(resultado)


def ejecutar_agentes_en_paralelo(datos_sensor: dict, ruta_imagen: str) -> dict:
    """
    Lanza los 3 agentes como hilos independientes y espera
    a que todos terminen. Retorna un resumen de resultados.

    Args:
        datos_sensor: dict con lecturas actuales del invernadero.
        ruta_imagen: ruta de la imagen de hoja a procesar.

    Returns:
        dict con log de ejecución y resultados de cada agente.
    """
    log = []
    inicio_global = time.time()

    # Crear los tres hilos
    hilo_senales = threading.Thread(
        target=tarea_analizar_senales,
        args=(datos_sensor, log),
        name="HiloSeñales",
        daemon=True,
    )
    hilo_imagenes = threading.Thread(
        target=tarea_procesar_imagenes,
        args=(ruta_imagen, log),
        name="HiloImagenes",
        daemon=True,
    )
    hilo_decisor = threading.Thread(
        target=tarea_emitir_decision,
        args=(2.1, log),
        name="HiloDecisor",
        daemon=True,
    )

    # Lanzar todos al mismo tiempo
    log.append("🚀 Iniciando ejecución paralela de agentes...")
    hilo_senales.start()
    hilo_imagenes.start()
    hilo_decisor.start()

    # Esperar a que los tres terminen
    hilo_senales.join()
    hilo_imagenes.join()
    hilo_decisor.join()

    duracion = round(time.time() - inicio_global, 2)
    log.append(f"✅ Todos los agentes finalizaron en {duracion}s (paralelo)")

    # Recoger resultados de la cola
    resultados = []
    while not cola_resultados.empty():
        resultados.append(cola_resultados.get())

    return {
        "log": log,
        "resultados": resultados,
        "duracion_total": duracion,
    }


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    datos = {"temperatura": 34.5, "humedad_suelo": 28.0}
    resumen = ejecutar_agentes_en_paralelo(datos, "assets/images/hoja1.jpg")
    print("\n".join(resumen["log"]))
    print(f"\nResultados: {resumen['resultados']}")
