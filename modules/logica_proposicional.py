# =============================================================
# MÓDULO: logica_proposicional.py
# RESPONSABLE: Integrante 4
# FUNCIÓN: Representa el conocimiento del sistema mediante
#          lógica proposicional formal (Parte G del T2).
# =============================================================


# ── Definición de proposiciones ─────────────────────────────
PROPOSICIONES = {
    "P": "La humedad del suelo es baja (< 30%)",
    "Q": "La temperatura es alta (> 32 °C)",
    "R": "Se requiere riego urgente",
    "S": "La hoja presenta manchas o coloración anómala",
    "T": "Hay posible enfermedad en la planta",
    "U": "La luz es insuficiente (< 200 lux)",
    "V": "El cultivo está en estado normal",
    "W": "Se recomienda revisión urgente",
}

# ── Definición de expresiones lógicas (reglas formales) ─────
EXPRESIONES_LOGICAS = [
    {
        "id": 1,
        "expresion": "(P ∧ Q) → R",
        "significado": (
            "Si la humedad del suelo es baja Y la temperatura es alta, "
            "entonces se requiere riego urgente. "
            "La conjunción de ambos factores estresa gravemente la planta."
        ),
        "vars": ["P", "Q"],
        "conclusion": "R",
    },
    {
        "id": 2,
        "expresion": "S → T",
        "significado": (
            "Si la hoja presenta manchas o coloración anómala, "
            "entonces hay posible enfermedad. "
            "Es una regla de inferencia directa basada en síntomas visuales."
        ),
        "vars": ["S"],
        "conclusion": "T",
    },
    {
        "id": 3,
        "expresion": "(T ∧ P) → W",
        "significado": (
            "Si hay posible enfermedad Y la humedad es baja, "
            "entonces se requiere revisión urgente. "
            "La combinación de enfermedad y estrés hídrico es crítica."
        ),
        "vars": ["T", "P"],
        "conclusion": "W",
    },
    {
        "id": 4,
        "expresion": "(¬P ∧ ¬Q ∧ ¬S) → V",
        "significado": (
            "Si NO hay humedad baja, NO hay temperatura alta, y NO hay manchas, "
            "entonces el cultivo está en estado normal. "
            "Solo cuando todas las condiciones son aceptables el sistema concluye normalidad."
        ),
        "vars": ["P", "Q", "S"],
        "conclusion": "V",
        "negados": True,
    },
    {
        "id": 5,
        "expresion": "Q → alerta_temperatura",
        "significado": (
            "Si la temperatura es alta, se activa la alerta de temperatura. "
            "Esta es una regla simple de monitoreo preventivo."
        ),
        "vars": ["Q"],
        "conclusion": "alerta_temperatura",
    },
]


def evaluar_expresion(expresion_id: int, valores: dict) -> dict:
    """
    Evalúa una expresión lógica dado un conjunto de valores de verdad.

    Args:
        expresion_id: ID de la expresión (1–5)
        valores: dict {letra: bool} con el valor de cada proposición,
                 ej: {"P": True, "Q": False, "S": True}

    Returns:
        dict con la expresión, los valores y el resultado (True/False)
    """
    expr = next((e for e in EXPRESIONES_LOGICAS if e["id"] == expresion_id), None)
    if not expr:
        return {"error": f"Expresión {expresion_id} no encontrada"}

    # Evaluación manual según la forma de la expresión
    if expresion_id == 1:   # (P ∧ Q) → R
        antecedente = valores.get("P", False) and valores.get("Q", False)
        resultado = (not antecedente) or valores.get("R", True)
        activa = antecedente  # si el antecedente es verdadero, se dispara

    elif expresion_id == 2:  # S → T
        antecedente = valores.get("S", False)
        resultado = (not antecedente) or valores.get("T", True)
        activa = antecedente

    elif expresion_id == 3:  # (T ∧ P) → W
        antecedente = valores.get("T", False) and valores.get("P", False)
        resultado = (not antecedente) or valores.get("W", True)
        activa = antecedente

    elif expresion_id == 4:  # (¬P ∧ ¬Q ∧ ¬S) → V
        antecedente = (
            not valores.get("P", True)
            and not valores.get("Q", True)
            and not valores.get("S", True)
        )
        resultado = (not antecedente) or valores.get("V", True)
        activa = antecedente

    elif expresion_id == 5:  # Q → alerta
        antecedente = valores.get("Q", False)
        resultado = (not antecedente) or True
        activa = antecedente

    else:
        return {"error": "Forma de expresión desconocida"}

    return {
        "expresion": expr["expresion"],
        "significado": expr["significado"],
        "valores": valores,
        "antecedente_verdadero": activa,
        "conclusion_activa": activa,
        "expresion_valida": resultado,
    }


def evaluar_todas(temperatura: float, humedad_suelo: float,
                  estado_hoja: str) -> list[dict]:
    """
    Evalúa las 5 expresiones lógicas con los valores del sistema.
    Retorna una lista de evaluaciones para mostrar en la UI.
    """
    valores = {
        "P": humedad_suelo < 30,
        "Q": temperatura > 32,
        "R": (humedad_suelo < 30) and (temperatura > 32),
        "S": estado_hoja in ("enfermedad", "estres"),
        "T": estado_hoja == "enfermedad",
        "V": (humedad_suelo >= 30) and (temperatura <= 32) and (estado_hoja == "saludable"),
        "W": (estado_hoja == "enfermedad") and (humedad_suelo < 30),
    }
    return [evaluar_expresion(i, valores) for i in range(1, 6)]


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    print("=== PROPOSICIONES ===")
    for clave, desc in PROPOSICIONES.items():
        print(f"  {clave}: {desc}")

    print("\n=== EVALUACIÓN (temp=35, humedad=22, hoja=enfermedad) ===")
    resultados = evaluar_todas(35.0, 22.0, "enfermedad")
    for r in resultados:
        activa = "✅ ACTIVA" if r.get("conclusion_activa") else "⬜ inactiva"
        print(f"  {r['expresion']} — {activa}")
