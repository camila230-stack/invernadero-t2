# =============================================================
# MÓDULO: razonamiento_probabilistico.py
# RESPONSABLE: Integrante 4
# FUNCIÓN: Estima el nivel de riesgo del cultivo mediante
#          probabilidades simples y niveles de confianza.
# =============================================================

from dataclasses import dataclass


@dataclass
class SituacionRiesgo:
    """Representa una situación con su probabilidad asignada."""
    nombre: str
    condicion: str
    probabilidad: float      # 0.0 a 1.0
    justificacion: str
    nivel: str               # "BAJO" | "MEDIO" | "ALTO" | "CRITICO"
    recomendacion: str


# ── Tabla de situaciones probabilísticas ────────────────────
# Cada situación tiene su probabilidad de ocurrencia de riesgo
# y una justificación académica del valor asignado.
SITUACIONES = [
    SituacionRiesgo(
        nombre="Estrés hídrico severo",
        condicion="temperatura_alta AND humedad_suelo_baja",
        probabilidad=0.85,
        justificacion=(
            "Combinación crítica: alta temperatura acelera la transpiración "
            "mientras la baja humedad impide la absorción de agua. "
            "Estudios agronómicos reportan 80-90% de daño en estas condiciones."
        ),
        nivel="CRITICO",
        recomendacion="Riego inmediato + activar ventilación",
    ),
    SituacionRiesgo(
        nombre="Posible enfermedad fúngica",
        condicion="manchas_en_hoja AND humedad_ambiental_alta",
        probabilidad=0.72,
        justificacion=(
            "La presencia de manchas junto con alta humedad ambiental favorece "
            "el desarrollo de hongos (Botrytis, Phytophthora). "
            "Se asigna 72% porque las manchas también pueden ser por quemaduras de sol."
        ),
        nivel="ALTO",
        recomendacion="Aplicar fungicida preventivo y reducir humedad ambiental",
    ),
    SituacionRiesgo(
        nombre="Estado estable del cultivo",
        condicion="temperatura_normal AND humedad_adecuada AND hoja_sana",
        probabilidad=0.92,
        justificacion=(
            "Cuando temperatura, humedad y aspecto foliar son normales, "
            "la probabilidad de que el cultivo esté saludable es muy alta. "
            "El 8% restante contempla factores no medidos (pH, nutrientes)."
        ),
        nivel="BAJO",
        recomendacion="Continuar monitoreo rutinario",
    ),
    SituacionRiesgo(
        nombre="Estrés por luz insuficiente",
        condicion="luz_insuficiente AND temperatura_normal",
        probabilidad=0.55,
        justificacion=(
            "Luz baja reduce la fotosíntesis, pero la planta puede adaptarse "
            "en el corto plazo. Probabilidad media porque depende de la duración."
        ),
        nivel="MEDIO",
        recomendacion="Revisar sistema de iluminación artificial",
    ),
    SituacionRiesgo(
        nombre="Riesgo combinado moderado",
        condicion="humedad_suelo_baja AND hoja_con_estres",
        probabilidad=0.68,
        justificacion=(
            "Combinación de estrés hídrico y foliar sin temperatura extrema. "
            "Riesgo moderado-alto que requiere atención pronta pero no inmediata."
        ),
        nivel="ALTO",
        recomendacion="Programar riego y evaluar hojas manualmente",
    ),
]


def calcular_riesgo(
    temperatura: float,
    humedad_suelo: float,
    humedad_ambiental: float,
    intensidad_luz: float,
    estado_hoja: str,
) -> dict:
    """
    Evalúa qué situaciones de riesgo están activas y calcula
    una probabilidad de riesgo global compuesta.

    Returns:
        dict con situaciones activas, riesgo global y nivel de alerta.
    """
    situaciones_activas = []

    # Evaluar cada situación según las condiciones actuales
    if temperatura > 32 and humedad_suelo < 30:
        situaciones_activas.append(SITUACIONES[0])  # Estrés hídrico severo

    if estado_hoja in ("enfermedad", "estres") and humedad_ambiental > 70:
        situaciones_activas.append(SITUACIONES[1])  # Posible enfermedad

    if (15 <= temperatura <= 32) and (30 <= humedad_suelo <= 70) and estado_hoja == "saludable":
        situaciones_activas.append(SITUACIONES[2])  # Estado estable

    if intensidad_luz < 200 and (15 <= temperatura <= 32):
        situaciones_activas.append(SITUACIONES[3])  # Estrés por luz

    if humedad_suelo < 30 and estado_hoja in ("enfermedad", "estres"):
        situaciones_activas.append(SITUACIONES[4])  # Riesgo combinado

    # Riesgo global: si hay estado estable, es bajo; si hay critico, es alto
    niveles_activos = [s.nivel for s in situaciones_activas]

    if "CRITICO" in niveles_activos:
        riesgo_global = max(s.probabilidad for s in situaciones_activas)
        nivel_global = "CRITICO"
        color = "#e74c3c"
    elif "ALTO" in niveles_activos:
        riesgo_global = max(s.probabilidad for s in situaciones_activas if s.nivel in ("ALTO", "CRITICO"))
        nivel_global = "ALTO"
        color = "#e67e22"
    elif "MEDIO" in niveles_activos:
        riesgo_global = 0.55
        nivel_global = "MEDIO"
        color = "#f1c40f"
    elif "BAJO" in niveles_activos:
        riesgo_global = 0.08
        nivel_global = "BAJO"
        color = "#2ecc71"
    else:
        riesgo_global = 0.30
        nivel_global = "INDETERMINADO"
        color = "#95a5a6"

    return {
        "situaciones_activas": situaciones_activas,
        "riesgo_global": round(riesgo_global, 2),
        "nivel_global": nivel_global,
        "color": color,
        "n_situaciones": len(situaciones_activas),
    }


def resumen_probabilistico(resultado: dict) -> str:
    """Genera un texto resumen del análisis probabilístico."""
    lineas = [
        f"📊 **Riesgo global: {resultado['riesgo_global']*100:.0f}% — Nivel {resultado['nivel_global']}**",
        f"Se identificaron {resultado['n_situaciones']} situación(es) de riesgo activas:\n",
    ]
    for s in resultado["situaciones_activas"]:
        lineas.append(
            f"• **{s.nombre}** ({s.probabilidad*100:.0f}% probabilidad): {s.recomendacion}"
        )
    return "\n".join(lineas)


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    resultado = calcular_riesgo(
        temperatura=35.0,
        humedad_suelo=22.0,
        humedad_ambiental=75.0,
        intensidad_luz=600.0,
        estado_hoja="enfermedad",
    )
    print(resumen_probabilistico(resultado))
