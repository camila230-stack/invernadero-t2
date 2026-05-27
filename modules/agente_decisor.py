def ejecutar_sistema_experto(
    temperatura: float,
    humedad_suelo: float,
    intensidad_luz: float,
    estado_hoja: str = "saludable",
) -> dict:
    hechos = []
    recomendaciones = []

    # Regla 1 y 2: temperatura
    if temperatura > 32:
        hechos.append("temperatura_alta")
        recomendaciones.append("🌡️ Alerta por temperatura elevada")
    elif temperatura < 15:
        hechos.append("temperatura_baja")
    else:
        hechos.append("temperatura_normal")

    # Regla 3 y 4: humedad del suelo
    if humedad_suelo < 30:
        hechos.append("humedad_baja")
        hechos.append("suelo_seco")
        if temperatura > 32:
            recomendaciones.append("💧 Regar ahora — humedad crítica")
        else:
            recomendaciones.append("💧 Riego recomendado — humedad baja")
    elif humedad_suelo > 70:
        hechos.append("humedad_alta")
        hechos.append("suelo_humedo")
    else:
        hechos.append("humedad_adecuada")

    # Regla 5: luz
    if intensidad_luz < 200:
        hechos.append("luz_insuficiente")
        recomendaciones.append("⏳ Esperar y monitorear — luz insuficiente")
    elif intensidad_luz > 1000:
        hechos.append("luz_excesiva")
    else:
        hechos.append("luz_adecuada")

    # Regla 6 y 7: estado de hoja (viene de OpenCV)
    if estado_hoja == "enfermedad":
        hechos += ["manchas_en_hoja", "hoja_amarilla", "condicion_enfermedad"]
        recomendaciones.append("🍂 Posible enfermedad en hojas")
        if humedad_suelo < 30:
            recomendaciones.append("🚨 Revisión urgente del cultivo")
    elif estado_hoja == "estres":
        hechos += ["manchas_en_hoja", "borde_oscuro"]
        recomendaciones.append("🍂 Estrés moderado en hoja — revisar riego")
    else:
        hechos.append("hoja_sana")

    # Regla 8: cultivo normal si todo está bien
    if ("humedad_adecuada" in hechos and
        "temperatura_normal" in hechos and
        "hoja_sana" in hechos):
        recomendaciones.append("✅ Cultivo en estado normal")

    if not recomendaciones:
        recomendaciones.append("ℹ️ Sin alertas activas")

    return {"hechos": hechos, "recomendaciones": recomendaciones}