# =============================================================
# app.py — App principal Streamlit
# RESPONSABLE: Integrante 1
# FUNCIÓN: Interfaz web completa del Sistema Inteligente
#          de Monitoreo de Invernadero.
# Ejecutar con: streamlit run app.py
# =============================================================

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import sys
import os

# Asegurar que los módulos se encuentren
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agente_sensor import simular_datos_invernadero, graficar_variables, obtener_estado_actual
from agente_senales import generar_reporte_senales, graficar_senal_con_anomalias
from agente_imagenes import analizar_hoja, graficar_procesamiento
from agente_decisor import ejecutar_sistema_experto
from logica_proposicional import PROPOSICIONES, EXPRESIONES_LOGICAS, evaluar_todas
from razonamiento_probabilistico import calcular_riesgo, resumen_probabilistico
from agente_coordinador import AgenteCoordinador
from paralelismo import ejecutar_agentes_en_paralelo


# ── Configuración de página ──────────────────────────────────
st.set_page_config(
    page_title="🌱 Invernadero Inteligente",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Estilos personalizados ───────────────────────────────────
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem; font-weight: 800;
        color: #2ecc71; margin-bottom: 0;
    }
    .subtitle {
        color: #7f8c8d; font-size: 1rem; margin-bottom: 1.5rem;
    }
    .metric-card {
        background: #1a2a1a; border-radius: 10px;
        padding: 1rem; border-left: 4px solid #2ecc71;
    }
    .alert-critico { color: #e74c3c; font-weight: bold; font-size: 1.1rem; }
    .alert-alto    { color: #e67e22; font-weight: bold; }
    .alert-medio   { color: #f1c40f; font-weight: bold; }
    .alert-bajo    { color: #2ecc71; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


# ── Sidebar: controles de simulación ────────────────────────
with st.sidebar:
    st.header("⚙️ Configuración")
    n_registros = st.slider("Registros simulados", 50, 200, 120, step=10)
    umbral_anomalia = st.slider("Umbral anomalía (σ)", 1.5, 3.0, 2.0, step=0.1)
    imagen_seleccionada = st.selectbox(
        "Imagen de hoja",
        ["assets/images/hoja1.jpg",
         "assets/images/hoja2.jpg",
         "assets/images/hoja3.jpg"],
    )
    st.markdown("---")
    ejecutar = st.button("🚀 Ejecutar análisis completo", type="primary", use_container_width=True)

    st.markdown("---")
    st.caption("T2 — Sistemas Inteligentes y ML")
    st.caption("Integrantes: [Pon sus nombres aquí]")


# ── Encabezado principal ─────────────────────────────────────
st.markdown('<p class="main-title">🌿 Sistema Inteligente de Invernadero</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Monitoreo multiagente • Análisis de señales • Visión computacional • Sistema experto</p>', unsafe_allow_html=True)

if not ejecutar:
    st.info("👈 Ajusta los parámetros en el panel izquierdo y pulsa **Ejecutar análisis completo**.")
    st.stop()


# ══════════════════════════════════════════════════════════════
# EJECUCIÓN DEL SISTEMA
# ══════════════════════════════════════════════════════════════

coordinador = AgenteCoordinador()

with st.spinner("Generando datos del invernadero..."):
    df = simular_datos_invernadero(n_registros)
    datos_actuales = obtener_estado_actual(df)

with st.spinner("Analizando señales..."):
    reporte_senales = generar_reporte_senales(df)

with st.spinner("Procesando imagen de hoja..."):
    resultado_imagen = analizar_hoja(imagen_seleccionada)

with st.spinner("Consultando sistema experto..."):
    decision = ejecutar_sistema_experto(
        temperatura=datos_actuales["temperatura"],
        humedad_suelo=datos_actuales["humedad_suelo"],
        intensidad_luz=datos_actuales["intensidad_luz"],
        estado_hoja=resultado_imagen["estado"],
    )

with st.spinner("Calculando riesgo..."):
    riesgo = calcular_riesgo(
        temperatura=datos_actuales["temperatura"],
        humedad_suelo=datos_actuales["humedad_suelo"],
        humedad_ambiental=datos_actuales["humedad_ambiental"],
        intensidad_luz=datos_actuales["intensidad_luz"],
        estado_hoja=resultado_imagen["estado"],
    )

with st.spinner("Ejecutando agentes en paralelo..."):
    resultado_paralelo = ejecutar_agentes_en_paralelo(datos_actuales, imagen_seleccionada)

estado = coordinador.consolidar_estado(
    datos_actuales, reporte_senales, resultado_imagen, decision, riesgo
)


# ══════════════════════════════════════════════════════════════
# PANEL SUPERIOR: MÉTRICAS EN TIEMPO REAL
# ══════════════════════════════════════════════════════════════

st.subheader("📡 Lecturas actuales del invernadero")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("🌡️ Temperatura", f"{datos_actuales['temperatura']:.1f} °C",
            delta="Alta" if datos_actuales["temperatura"] > 32 else "Normal")
col2.metric("💧 Humedad suelo", f"{datos_actuales['humedad_suelo']:.1f} %",
            delta="Baja" if datos_actuales["humedad_suelo"] < 30 else "OK")
col3.metric("🌫️ Humedad ambiental", f"{datos_actuales['humedad_ambiental']:.1f} %")
col4.metric("☀️ Luz", f"{datos_actuales['intensidad_luz']:.0f} lux")
col5.metric(
    f"⚠️ Riesgo global",
    f"{riesgo['riesgo_global']*100:.0f}%",
    delta=riesgo["nivel_global"],
    delta_color="inverse",
)


# ══════════════════════════════════════════════════════════════
# PESTAÑAS DE CONTENIDO
# ══════════════════════════════════════════════════════════════

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Datos y Señales",
    "🍃 Imágenes",
    "🧠 Sistema Experto",
    "📐 Lógica",
    "📈 Probabilidad",
    "🤖 Agentes",
    "⚡ Paralelismo",
])


# ── TAB 1: Datos y señales ───────────────────────────────────
with tab1:
    st.subheader("Parte A — Datos simulados del invernadero")
    st.write(f"**{len(df)} registros** generados con comportamiento realista.")
    with st.expander("Ver tabla de datos"):
        st.dataframe(df.head(20), use_container_width=True)

    st.pyplot(graficar_variables(df))

    st.subheader("Parte B — Análisis de señales temporales")
    for reporte in reporte_senales:
        with st.expander(f"📉 {reporte['variable']}"):
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Media", reporte["media"])
            c2.metric("Mín", reporte["min"])
            c3.metric("Máx", reporte["max"])
            c4.metric("Tendencia", reporte["tendencia"])
            st.info(f"Anomalías detectadas: **{reporte['n_anomalias']}** — Picos: **{reporte['n_picos']}**")

    col = "temperatura" if reporte_senales[0]["variable"].startswith("Temp") else "humedad_suelo"
    st.pyplot(graficar_senal_con_anomalias(df, "temperatura", "Temperatura (°C)"))
    st.pyplot(graficar_senal_con_anomalias(df, "humedad_suelo", "Humedad del suelo (%)"))


# ── TAB 2: Imágenes ─────────────────────────────────────────
with tab2:
    st.subheader("Parte C — Procesamiento de imágenes con OpenCV")
    st.write("**Pipeline aplicado:** carga → escala de grises → umbralización → detección de bordes → segmentación HSV")

    col_a, col_b = st.columns([2, 1])
    with col_a:
        st.pyplot(graficar_procesamiento(resultado_imagen))
    with col_b:
        st.markdown("### Diagnóstico")
        st.markdown(f"**{resultado_imagen['diagnostico']}**")
        st.metric("Área afectada", f"{resultado_imagen['porcentaje_dano']} %")
        st.markdown("""
**¿Qué se observó?**
- Zonas con cambio de coloración (amarillo/marrón) segmentadas
- Bordes irregulares que pueden indicar lesiones
- Umbralización revela textura interna de la hoja

**Utilidad en el sistema:**
El porcentaje de área afectada alimenta directamente
al AgenteDecisor como hecho lógico `manchas_en_hoja`.
        """)


# ── TAB 3: Sistema experto ───────────────────────────────────
with tab3:
    st.subheader("Parte D & E — Sistema experto con pyDatalog")

    col_h, col_r = st.columns(2)

    with col_h:
        st.markdown("#### 📌 Hechos cargados")
        for hecho in decision["hechos"]:
            st.markdown(f"- `{hecho}`")

    with col_r:
        st.markdown("#### 💡 Recomendaciones inferidas")
        for rec in decision["recomendaciones"]:
            st.markdown(f"**{rec}**")

    st.markdown("---")
    st.markdown("#### 📋 Tabla de conocimiento")
    reglas = [
        {"Condición (Antecedente)", "Consecuencia (Conclusión)"},
    ]
    st.table({
        "Antecedente": [
            "humedad_baja",
            "suelo_seco ∧ temperatura_alta",
            "manchas_en_hoja ∧ hoja_amarilla",
            "manchas_en_hoja ∧ borde_oscuro",
            "condicion_enfermedad ∧ suelo_seco",
            "humedad_adecuada ∧ temperatura_normal ∧ luz_adecuada",
        ],
        "Consecuencia": [
            "suelo_seco",
            "recomendar_riego_urgente",
            "condicion_enfermedad",
            "condicion_enfermedad",
            "revision_urgente",
            "planta_sana",
        ],
    })


# ── TAB 4: Lógica proposicional ─────────────────────────────
with tab4:
    st.subheader("Parte G — Lógica proposicional")

    st.markdown("#### Proposiciones del sistema")
    for clave, desc in PROPOSICIONES.items():
        st.markdown(f"- **{clave}**: {desc}")

    st.markdown("---")
    st.markdown("#### Evaluación de expresiones lógicas")

    evaluaciones = evaluar_todas(
        datos_actuales["temperatura"],
        datos_actuales["humedad_suelo"],
        resultado_imagen["estado"],
    )

    for ev in evaluaciones:
        estado_expr = "🔴 **ACTIVA**" if ev.get("conclusion_activa") else "⬜ inactiva"
        with st.expander(f"`{ev['expresion']}` — {estado_expr}"):
            st.write(ev["significado"])


# ── TAB 5: Probabilidad ─────────────────────────────────────
with tab5:
    st.subheader("Parte H — Razonamiento probabilístico")
    st.markdown(resumen_probabilistico(riesgo))

    st.markdown("---")
    if riesgo["situaciones_activas"]:
        for s in riesgo["situaciones_activas"]:
            with st.expander(f"{s.nombre} — {s.probabilidad*100:.0f}% probabilidad"):
                st.write(f"**Condición:** `{s.condicion}`")
                st.write(f"**Justificación:** {s.justificacion}")
                st.write(f"**Recomendación:** {s.recomendacion}")
                st.progress(s.probabilidad)
    else:
        st.success("No se detectaron situaciones de riesgo activas.")


# ── TAB 6: Comunicación entre agentes ───────────────────────
with tab6:
    st.subheader("Parte F & I — Diseño y comunicación entre agentes")

    st.markdown("""
| Agente | Conocimiento | Recibe | Entrega |
|---|---|---|---|
| **AgenteSensor** | Parámetros de simulación | Solicitud del coordinador | DataFrame con 120+ registros |
| **AgenteSeñales** | Estadística de señales temporales | DataFrame | Reporte de tendencias y anomalías |
| **AgenteImagenes** | OpenCV: HSV, Canny, umbralización | Ruta de imagen | Diagnóstico y % área afectada |
| **AgenteDecisor** | Reglas pyDatalog (8 hechos, 6 reglas) | Hechos numéricos y de imagen | Lista de recomendaciones |
| **AgenteCoordinador** | Protocolo de mensajes entre agentes | Todo | Estado consolidado a la UI |
    """)

    st.markdown("#### 📨 Log de mensajes entre agentes")
    log_df = pd.DataFrame(coordinador.obtener_log_comunicacion())
    st.dataframe(log_df, use_container_width=True)


# ── TAB 7: Paralelismo ───────────────────────────────────────
with tab7:
    st.subheader("Parte J — Programación paralela con threading")

    st.markdown("""
**Implementación:** se lanzaron **3 hilos** simultáneamente con `threading.Thread`:
- 🔵 Hilo 1: análisis de señales
- 🟢 Hilo 2: procesamiento de imágenes
- 🟠 Hilo 3: emisión de decisión

Los resultados se depositaron en una `queue.Queue` compartida y se recuperaron al finalizar todos.
    """)

    st.markdown("#### 🕐 Log de ejecución paralela")
    for linea in resultado_paralelo["log"]:
        st.text(linea)

    st.metric("⏱️ Tiempo total (paralelo)", f"{resultado_paralelo['duracion_total']} s",
              help="Si fuera secuencial habría tomado ~5 s; en paralelo ~2.1 s")

    st.markdown("#### Resultados por hilo")
    for r in resultado_paralelo["resultados"]:
        st.json(r)
