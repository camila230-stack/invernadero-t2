# =============================================================
# MÓDULO: agente_decisor.py
# RESPONSABLE: Integrante 4
# FUNCIÓN: Sistema experto basado en reglas usando pyDatalog.
#          Emite recomendaciones a partir de hechos del entorno.
# =============================================================

from pyDatalog import pyDatalog

# ── Declaración de términos lógicos ─────────────────────────
pyDatalog.create_terms(
    # Hechos de entrada (sensores)
    "humedad_baja, humedad_adecuada, humedad_alta",
    "temperatura_alta, temperatura_normal, temperatura_baja",
    "luz_insuficiente, luz_adecuada, luz_excesiva",
    # Hechos derivados de imágenes
    "manchas_en_hoja, borde_oscuro, hoja_amarilla, hoja_sana",
    # Estados intermedios inferidos
    "suelo_seco, suelo_humedo, planta_con_estres, planta_sana",
    "condicion_enfermedad",
    # Recomendaciones finales
    "recomendar_riego_urgente, recomendar_esperar",
    "alerta_temperatura, alerta_enfermedad, revision_urgente",
    "cultivo_normal",
    # Variables
    "X",
)


def cargar_reglas() -> None:
    """
    Define todas las reglas del sistema experto.
    Se llama UNA sola vez al iniciar el módulo.
    """

    # ── REGLA 1: suelo seco si humedad es baja
    suelo_seco() <= humedad_baja()

    # ── REGLA 2: riego urgente si suelo seco y temperatura alta
    recomendar_riego_urgente() <= (suelo_seco() & temperatura_alta())

    # ── REGLA 3: riego urgente si solo humedad muy baja (sin temp alta)
    recomendar_riego_urgente() <= (humedad_baja() & temperatura_normal())

    # ── REGLA 4: alerta de temperatura si temperatura alta
    alerta_temperatura() <= temperatura_alta()

    # ── REGLA 5: posible enfermedad si manchas + coloración
    condicion_enfermedad() <= (manchas_en_hoja() & hoja_amarilla())
    condicion_enfermedad() <= (manchas_en_hoja() & borde_oscuro())
    alerta_enfermedad() <= condicion_enfermedad()

    # ── REGLA 6: revisión urgente si enfermedad + estrés hídrico
    revision_urgente() <= (condicion_enfermedad() & suelo_seco())

    # ── REGLA 7: planta sana si todo está en rango normal
    planta_sana() <= (humedad_adecuada() & temperatura_normal() & luz_adecuada())
    cultivo_normal() <= (planta_sana() & hoja_sana())

    # ── REGLA 8: esperar y monitorear si humedad adecuada pero luz baja
    recomendar_esperar() <= (humedad_adecuada() & luz_insuficiente())


# Cargar las reglas al importar el módulo
cargar_reglas()


def _limpiar_hechos() -> None:
    """Retracta todos los hechos dinámicos para evitar conflictos."""
    for hecho in [
        humedad_baja, humedad_adecuada, humedad_alta,
        temperatura_alta, temperatura_normal, temperatura_baja,
        luz_insuficiente, luz_adecuada, luz_excesiva,
        manchas_en_hoja, borde_oscuro, hoja_amarilla, hoja_sana,
    ]:
        try:
            -hecho()
        except Exception:
            pass


def _asignar_hechos_sensores(temperatura: float, humedad_suelo: float,
                              intensidad_luz: float) -> list[str]:
    """
    Convierte valores numéricos en hechos lógicos del sistema experto.
    Retorna lista de hechos añadidos para mostrar en la UI.
    """
    hechos = []

    # Temperatura
    if temperatura > 32:
        +temperatura_alta()
        hechos.append("temperatura_alta")
    elif temperatura < 15:
        +temperatura_baja()
        hechos.append("temperatura_baja")
    else:
        +temperatura_normal()
        hechos.append("temperatura_normal")

    # Humedad del suelo
    if humedad_suelo < 30:
        +humedad_baja()
        hechos.append("humedad_baja")
    elif humedad_suelo > 70:
        +humedad_alta()
        hechos.append("humedad_alta")
    else:
        +humedad_adecuada()
        hechos.append("humedad_adecuada")

    # Luz
    if intensidad_luz < 200:
        +luz_insuficiente()
        hechos.append("luz_insuficiente")
    elif intensidad_luz > 1000:
        +luz_excesiva()
        hechos.append("luz_excesiva")
    else:
        +luz_adecuada()
        hechos.append("luz_adecuada")

    return hechos


def _asignar_hechos_imagen(estado_hoja: str) -> list[str]:
    """Convierte el resultado del AgenteImagenes en hechos lógicos."""
    hechos = []
    if estado_hoja == "enfermedad":
        +manchas_en_hoja()
        +hoja_amarilla()
        hechos += ["manchas_en_hoja", "hoja_amarilla"]
    elif estado_hoja == "estres":
        +manchas_en_hoja()
        +borde_oscuro()
        hechos += ["manchas_en_hoja", "borde_oscuro"]
    else:
        +hoja_sana()
        hechos.append("hoja_sana")
    return hechos


def consultar_recomendaciones() -> list[str]:
    """Ejecuta las consultas y retorna lista de recomendaciones activas."""
    recomendaciones = []
    if recomendar_riego_urgente():
        recomendaciones.append("💧 Regar ahora — humedad crítica")
    if alerta_temperatura():
        recomendaciones.append("🌡️ Alerta por temperatura elevada")
    if alerta_enfermedad():
        recomendaciones.append("🍂 Posible enfermedad en hojas")
    if revision_urgente():
        recomendaciones.append("🚨 Revisión urgente del cultivo")
    if cultivo_normal():
        recomendaciones.append("✅ Cultivo en estado normal")
    if recomendar_esperar():
        recomendaciones.append("⏳ Esperar y seguir monitoreando")
    return recomendaciones if recomendaciones else ["ℹ️ Sin alertas activas"]


def ejecutar_sistema_experto(
    temperatura: float,
    humedad_suelo: float,
    intensidad_luz: float,
    estado_hoja: str = "saludable",
) -> dict:
    """
    Punto de entrada principal del sistema experto.

    Args:
        temperatura: °C del sensor
        humedad_suelo: % del sensor
        intensidad_luz: lux del sensor
        estado_hoja: 'saludable' | 'estres' | 'enfermedad' (del AgenteImagenes)

    Returns:
        dict con hechos cargados y recomendaciones inferidas
    """
    _limpiar_hechos()
    hechos_sensores = _asignar_hechos_sensores(temperatura, humedad_suelo, intensidad_luz)
    hechos_imagen = _asignar_hechos_imagen(estado_hoja)
    recomendaciones = consultar_recomendaciones()

    return {
        "hechos": hechos_sensores + hechos_imagen,
        "recomendaciones": recomendaciones,
    }


# ── Ejecución directa para pruebas ──────────────────────────
if __name__ == "__main__":
    resultado = ejecutar_sistema_experto(
        temperatura=35.0,
        humedad_suelo=22.0,
        intensidad_luz=600.0,
        estado_hoja="enfermedad",
    )
    print("Hechos:", resultado["hechos"])
    print("Recomendaciones:")
    for r in resultado["recomendaciones"]:
        print(" -", r)
