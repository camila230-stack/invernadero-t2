# =============================================================
# MÓDULO: agente_senales.py
# RESPONSABLE: Integrante 2
# FUNCIÓN: Analiza señales temporales, detecta tendencias,
#          picos, caídas y anomalías en los datos del sensor.
# =============================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks


def analizar_senal(serie: pd.Series, nombre: str, umbral_anomalia: float = 2.0) -> dict:
    """
    Analiza una señal temporal e identifica estadísticas y anomalías.

    Args:
        serie: Serie de Pandas con los valores de la variable.
        nombre: Nombre de la variable para mostrar en reportes.
        umbral_anomalia: Desviaciones estándar para considerar un punto anómalo.

    Returns:
        dict con media, std, min, max, anomalías y tendencia.
    """
    media = serie.mean()
    std = serie.std()
    minimo = serie.min()
    maximo = serie.max()

    # Anomalías: puntos fuera de media ± umbral*std
    anomalias_idx = serie[np.abs(serie - media) > umbral_anomalia * std].index.tolist()

    # Tendencia lineal simple (pendiente de regresión)
    x = np.arange(len(serie))
    pendiente = np.polyfit(x, serie.values, 1)[0]
    if pendiente > 0.05:
        tendencia = "ascendente 📈"
    elif pendiente < -0.05:
        tendencia = "descendente 📉"
    else:
        tendencia = "estable ➡️"

    # Picos positivos
    picos, _ = find_peaks(serie.values, prominence=std * 0.8)

    return {
        "variable": nombre,
        "media": round(media, 2),
        "std": round(std, 2),
        "min": round(minimo, 2),
        "max": round(maximo, 2),
        "tendencia": tendencia,
        "n_anomalias": len(anomalias_idx),
        "indices_anomalias": anomalias_idx[:5],  # máx 5 para mostrar
        "n_picos": len(picos),
        "pendiente": round(pendiente, 4),
    }


def graficar_senal_con_anomalias(df: pd.DataFrame, col: str, nombre: str) -> plt.Figure:
    """
    Grafica la señal y marca visualmente las anomalías detectadas.
    """
    serie = df[col]
    media = serie.mean()
    std = serie.std()
    anomalias = serie[np.abs(serie - media) > 2 * std]

    fig, ax = plt.subplots(figsize=(12, 4))
    ax.plot(df["timestamp"], serie, label=nombre, color="#2980b9", linewidth=1.3)
    ax.axhline(media, color="gray", linestyle="--", linewidth=0.8, label="Media")
    ax.axhline(media + 2 * std, color="#e74c3c", linestyle=":", linewidth=0.8, label="+2σ")
    ax.axhline(media - 2 * std, color="#e74c3c", linestyle=":", linewidth=0.8, label="-2σ")

    if not anomalias.empty:
        ax.scatter(
            df.loc[anomalias.index, "timestamp"],
            anomalias.values,
            color="red", zorder=5, label="Anomalía", s=40
        )

    ax.set_title(f"Análisis de señal: {nombre}", fontsize=12, fontweight="bold")
    ax.set_xlabel("Tiempo")
    ax.set_ylabel(nombre)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    plt.xticks(rotation=30, fontsize=7)
    plt.tight_layout()
    return fig


def interpretar_anomalia(variable: str, valor: float) -> str:
    """
    Retorna una explicación textual de qué significa una anomalía
    para esa variable dentro del contexto del invernadero.
    """
    interpretaciones = {
        "temperatura": (
            f"⚠️ Temperatura anómala ({valor:.1f}°C): puede indicar fallo en ventilación "
            "o exposición directa al sol sin control térmico."
        ),
        "humedad_suelo": (
            f"⚠️ Humedad del suelo anómala ({valor:.1f}%): puede indicar riego excesivo "
            "o fuga en el sistema, o sequía severa si el valor es muy bajo."
        ),
        "humedad_ambiental": (
            f"⚠️ Humedad ambiental anómala ({valor:.1f}%): valores extremos favorecen "
            "el desarrollo de hongos (alta) o estrés hídrico foliar (baja)."
        ),
        "intensidad_luz": (
            f"⚠️ Luz anómala ({valor:.1f} lux): puede indicar obstrucción del techo, "
            "sensor sucio, o exposición extrema que queme las hojas."
        ),
    }
    return interpretaciones.get(variable, f"Anomalía detectada en {variable}: {valor:.2f}")


def generar_reporte_senales(df: pd.DataFrame) -> list[dict]:
    """
    Analiza temperatura y humedad del suelo como señales principales.
    Retorna lista de resultados para mostrar en la UI.
    """
    variables = [
        ("temperatura", "Temperatura (°C)"),
        ("humedad_suelo", "Humedad del suelo (%)"),
    ]
    reportes = []
    for col, nombre in variables:
        resultado = analizar_senal(df[col], nombre)
        reportes.append(resultado)
    return reportes


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    from agente_sensor import simular_datos_invernadero
    df = simular_datos_invernadero()
    reportes = generar_reporte_senales(df)
    for r in reportes:
        print(r)
    fig = graficar_senal_con_anomalias(df, "temperatura", "Temperatura (°C)")
    plt.show()
