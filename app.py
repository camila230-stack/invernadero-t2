import streamlit as st
import streamlit.components.v1 as components
import sys, os, json, base64

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "modules"))

from agente_sensor import simular_datos_invernadero, obtener_estado_actual
from agente_imagenes import analizar_hoja
from agente_coordinador import AgenteCoordinador
from paralelismo import ejecutar_agentes_en_paralelo

try:
    from agente_decisor import ejecutar_sistema_experto
    PYDATALOG_OK = True
except Exception:
    PYDATALOG_OK = False

try:
    from razonamiento_probabilistico import calcular_riesgo
    PROB_OK = True
except Exception:
    PROB_OK = False

st.set_page_config(page_title="Invernadero Inteligente", page_icon="🌿", layout="wide")

st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container { padding: 0 !important; max-width: 100% !important; }
    section[data-testid="stSidebar"] { background: #0D0D0D; }
    section[data-testid="stSidebar"] * { color: #F0EEE8 !important; }
    .hoja-preview { border-radius: 10px; margin-top: 8px; border: 1px solid rgba(255,255,255,0.1); }
    .badge-estado {
        padding: 5px 10px; border-radius: 6px;
        font-size: 12px; font-weight: 600;
        margin-top: 6px; display: inline-block;
    }
</style>
""", unsafe_allow_html=True)

def decision_manual(temperatura, humedad_suelo, intensidad_luz, estado_hoja):
    hechos = []
    recomendaciones = []
    if temperatura > 32:
        hechos.append("temperatura_alta")
        recomendaciones.append("Alerta por temperatura elevada")
    else:
        hechos.append("temperatura_normal")
    if humedad_suelo < 30:
        hechos.append("humedad_baja")
        hechos.append("suelo_seco")
        if temperatura > 32:
            recomendaciones.append("Regar ahora - humedad critica")
        else:
            recomendaciones.append("Riego recomendado - humedad baja")
    else:
        hechos.append("humedad_adecuada")
    if intensidad_luz < 200:
        hechos.append("luz_insuficiente")
        recomendaciones.append("Esperar y monitorear - luz baja")
    else:
        hechos.append("luz_adecuada")
    if estado_hoja == "enfermedad":
        hechos += ["manchas_en_hoja", "hoja_amarilla", "condicion_enfermedad"]
        recomendaciones.append("Posible enfermedad en hojas")
        if humedad_suelo < 30:
            recomendaciones.append("Revision urgente del cultivo")
    elif estado_hoja == "estres":
        hechos += ["manchas_en_hoja", "borde_oscuro"]
        recomendaciones.append("Estres moderado en hoja")
    else:
        hechos.append("hoja_sana")
    if "humedad_adecuada" in hechos and "temperatura_normal" in hechos and "hoja_sana" in hechos:
        recomendaciones.append("Cultivo en estado normal")
    if not recomendaciones:
        recomendaciones.append("Sin alertas activas")
    return {"hechos": hechos, "recomendaciones": recomendaciones}

def riesgo_manual(temperatura, humedad_suelo, estado_hoja):
    if temperatura > 32 and humedad_suelo < 30:
        return {"nivel_global": "CRITICO", "riesgo_global": 0.85}
    elif estado_hoja in ("enfermedad", "estres"):
        return {"nivel_global": "ALTO", "riesgo_global": 0.72}
    elif temperatura > 32 or humedad_suelo < 30:
        return {"nivel_global": "MEDIO", "riesgo_global": 0.55}
    else:
        return {"nivel_global": "BAJO", "riesgo_global": 0.08}

with st.sidebar:
    st.markdown("### Configuracion")
    n_registros = st.slider("Registros simulados", 50, 200, 120, step=10)
    imagen_sel = st.selectbox("Imagen de hoja", [
        "assets/images/hoja1.jpg",
        "assets/images/hoja2.jpg",
        "assets/images/hoja3.jpg",
    ])

    # Preview de la imagen seleccionada
    if os.path.exists(imagen_sel):
        st.image(imagen_sel, use_container_width=True, caption="Vista previa")

    ejecutar = st.button("Ejecutar analisis", type="primary", use_container_width=True)
    st.markdown("---")

    # Mostrar resultado del análisis si ya se ejecutó
    if "res_img" in st.session_state:
        img = st.session_state["res_img"]
        estado = img["estado"]
        dano = img["porcentaje_dano"]
        if estado == "enfermedad":
            color = "#E24B4A"
            texto = "Enfermedad probable"
        elif estado == "estres":
            color = "#EF9F27"
            texto = "Estres moderado"
        else:
            color = "#1D9E75"
            texto = "Hoja saludable"
        st.markdown(
            f'<div style="background:{color}20;border:1px solid {color};border-radius:8px;'
            f'padding:8px 12px;text-align:center;">'
            f'<div style="color:{color};font-weight:700;font-size:13px;">{texto}</div>'
            f'<div style="color:{color}99;font-size:11px;">{dano}% area afectada</div>'
            f'</div>',
            unsafe_allow_html=True
        )

    st.markdown("---")
    st.caption("T2 - Sistemas Inteligentes y ML")
    st.caption("camila230-stack")

if ejecutar:
    with st.spinner("Analizando invernadero..."):
        df = simular_datos_invernadero(n_registros)
        datos = obtener_estado_actual(df)
        res_img = analizar_hoja(imagen_sel)
        if PYDATALOG_OK:
            try:
                decision = ejecutar_sistema_experto(
                    datos["temperatura"], datos["humedad_suelo"],
                    datos["intensidad_luz"], res_img["estado"])
            except Exception:
                decision = decision_manual(
                    datos["temperatura"], datos["humedad_suelo"],
                    datos["intensidad_luz"], res_img["estado"])
        else:
            decision = decision_manual(
                datos["temperatura"], datos["humedad_suelo"],
                datos["intensidad_luz"], res_img["estado"])
        if PROB_OK:
            try:
                riesgo = calcular_riesgo(
                    datos["temperatura"], datos["humedad_suelo"],
                    datos["humedad_ambiental"], datos["intensidad_luz"],
                    res_img["estado"])
            except Exception:
                riesgo = riesgo_manual(datos["temperatura"], datos["humedad_suelo"], res_img["estado"])
        else:
            riesgo = riesgo_manual(datos["temperatura"], datos["humedad_suelo"], res_img["estado"])
        res_paralelo = ejecutar_agentes_en_paralelo(datos, imagen_sel)
    st.session_state["datos"] = datos
    st.session_state["decision"] = decision
    st.session_state["riesgo"] = riesgo
    st.session_state["res_img"] = res_img
    st.session_state["imagen_sel"] = imagen_sel
    st.rerun()

html_path = os.path.join(os.path.dirname(__file__), "assets", "templates", "dashboard.html")
if not os.path.exists(html_path):
    st.error("No se encuentra assets/templates/dashboard.html")
    st.stop()

with open(html_path, "r", encoding="utf-8") as f:
    html_content = f.read()

if "datos" in st.session_state:
    d = st.session_state["datos"]
    dec = st.session_state["decision"]
    r = st.session_state["riesgo"]
    img = st.session_state["res_img"]
    imagen_path = st.session_state["imagen_sel"]
    nivel_map = {"CRITICO": 95, "ALTO": 78, "MEDIO": 55, "BAJO": 15}
    recomendaciones_js = []
    for rec in dec["recomendaciones"]:
        recomendaciones_js.append({"icon": "ti-bell", "text": rec, "color": "#1D9E75", "bg": "#1D9E7515"})
    imagen_b64 = ""
    imagen_ext = "jpeg"
    if os.path.exists(imagen_path):
        ext = imagen_path.split(".")[-1].lower()
        imagen_ext = "jpeg" if ext == "jpg" else ext
        with open(imagen_path, "rb") as img_file:
            imagen_b64 = base64.b64encode(img_file.read()).decode("utf-8")
    data_obj = {
        "temperatura": round(float(d["temperatura"]), 1),
        "humedad_suelo": round(float(d["humedad_suelo"]), 1),
        "humedad_ambiental": round(float(d["humedad_ambiental"]), 1),
        "intensidad_luz": round(float(d["intensidad_luz"]), 0),
        "estado_hoja": img["estado"],
        "porcentaje_dano": float(img["porcentaje_dano"]),
        "riesgo_nivel": r["nivel_global"],
        "riesgo_pct": nivel_map.get(r["nivel_global"], 50),
        "hechos": dec["hechos"],
        "recomendaciones": recomendaciones_js,
        "imagen_base64": imagen_b64,
        "imagen_ext": imagen_ext,
    }
    data_js = "const DATA = " + json.dumps(data_obj, ensure_ascii=False) + ";"
    html_content = html_content.replace("const DATA = {", data_js + "\nconst DATA_UNUSED = {", 1)

components.html(html_content, height=1180, scrolling=True)