import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# ── Configuración base del invernadero ──────────────────────
SEMILLA = 42
np.random.seed(SEMILLA)
N_REGISTROS = 120  # mínimo 100 según rúbrica


def simular_datos_invernadero(n: int = N_REGISTROS) -> pd.DataFrame:
    """
    Genera un DataFrame con datos simulados de sensores del invernadero.
    Cada variable sigue un comportamiento realista con tendencias y ruido.

    Returns:
        pd.DataFrame con columnas:
            timestamp, temperatura, humedad_ambiental,
            intensidad_luz, humedad_suelo
    """
    # Marcas de tiempo cada 15 minutos durante 30 horas
    inicio = datetime(2024, 6, 1, 6, 0, 0)
    timestamps = [inicio + timedelta(minutes=15 * i) for i in range(n)]

    # Ciclo diario para temperatura (sube al mediodía, baja de noche)
    ciclo_dia = np.sin(np.linspace(0, 4 * np.pi, n))
    temperatura = 22 + 8 * ciclo_dia + np.random.normal(0, 1.2, n)

    # Humedad ambiental: inversa a la temperatura + ruido
    humedad_ambiental = 65 - 10 * ciclo_dia + np.random.normal(0, 3, n)
    humedad_ambiental = np.clip(humedad_ambiental, 30, 95)

    # Luz: solo hay durante el día (horas 6-18)
    horas = np.array([t.hour + t.minute / 60 for t in timestamps])
    es_dia = ((horas >= 6) & (horas <= 18)).astype(float)
    intensidad_luz = es_dia * (800 + 300 * np.sin(np.pi * (horas - 6) / 12))
    intensidad_luz += np.random.normal(0, 40, n)
    intensidad_luz = np.clip(intensidad_luz, 0, 1200)

    # Humedad del suelo: decrece con el tiempo salvo eventos de riego
    humedad_suelo = np.zeros(n)
    nivel = 70.0
    for i in range(n):
        # Simulamos 3 eventos de riego automático
        if i in [20, 60, 95]:
            nivel = min(nivel + 30, 90)
        nivel -= np.random.uniform(0.2, 0.6)   # evaporación gradual
        nivel = max(nivel, 10)
        humedad_suelo[i] = nivel + np.random.normal(0, 1)

    df = pd.DataFrame({
        "timestamp": timestamps,
        "temperatura": np.round(temperatura, 2),
        "humedad_ambiental": np.round(humedad_ambiental, 2),
        "intensidad_luz": np.round(intensidad_luz, 2),
        "humedad_suelo": np.round(humedad_suelo, 2),
    })
    return df


def graficar_variables(df: pd.DataFrame) -> plt.Figure:
    """
    Genera una figura con 4 subgráficos, uno por variable.
    Retorna la figura para usarla en Streamlit con st.pyplot().
    """
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)
    fig.suptitle("Datos simulados del invernadero", fontsize=14, fontweight="bold")

    variables = [
        ("temperatura", "Temperatura (°C)", "#e74c3c"),
        ("humedad_ambiental", "Humedad ambiental (%)", "#3498db"),
        ("intensidad_luz", "Intensidad de luz (lux)", "#f1c40f"),
        ("humedad_suelo", "Humedad del suelo (%)", "#2ecc71"),
    ]

    for ax, (col, label, color) in zip(axes, variables):
        ax.plot(df["timestamp"], df[col], color=color, linewidth=1.2)
        ax.set_ylabel(label, fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=30, labelsize=7)

    plt.tight_layout()
    return fig


def obtener_estado_actual(df: pd.DataFrame) -> dict:
    """
    Devuelve el último registro del DataFrame como diccionario.
    Lo usa el AgenteCoordinador para tomar decisiones.
    """
    ultimo = df.iloc[-1]
    return {
        "temperatura": float(ultimo["temperatura"]),
        "humedad_ambiental": float(ultimo["humedad_ambiental"]),
        "intensidad_luz": float(ultimo["intensidad_luz"]),
        "humedad_suelo": float(ultimo["humedad_suelo"]),
    }


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    df = simular_datos_invernadero()
    print(f"✅ Datos generados: {len(df)} registros")
    print(df.head(10).to_string(index=False))
    fig = graficar_variables(df)
    plt.show()
