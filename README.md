# 🌱 Sistema Inteligente Multiagente para Invernadero
**Evaluación T2 — Sistemas Inteligentes y Machine Learning**

## 👥 Integrantes y Módulos

| Integrante | Módulo | Archivos |
|---|---|---|
| **Integrante 1 (tú)** | Streamlit UI + Coordinador | `app.py`, `modules/agente_coordinador.py` |
| **Integrante 2** | Simulación de datos + Señales + Paralelismo | `modules/agente_sensor.py`, `modules/agente_senales.py`, `modules/paralelismo.py` |
| **Integrante 3** | OpenCV — Procesamiento de imágenes | `modules/agente_imagenes.py` |
| **Integrante 4** | pyDatalog — Sistema experto + Lógica + Probabilidad | `modules/agente_decisor.py`, `modules/logica_proposicional.py`, `modules/razonamiento_probabilistico.py` |

---

## 📁 Estructura del Proyecto

```
invernadero/
├── app.py                          # [INT. 1] App principal Streamlit
├── requirements.txt                # Dependencias
├── README.md
├── assets/
│   └── images/                     # [INT. 3] Imágenes de hojas para procesar
│       ├── hoja1.jpg
│       ├── hoja2.jpg
│       └── hoja3.jpg
└── modules/
    ├── agente_sensor.py            # [INT. 2] Simulación de datos del entorno
    ├── agente_senales.py           # [INT. 2] Análisis de señales temporales
    ├── paralelismo.py              # [INT. 2] Threading/asyncio concurrente
    ├── agente_imagenes.py          # [INT. 3] OpenCV — procesamiento de hojas
    ├── agente_decisor.py           # [INT. 4] pyDatalog — sistema experto
    ├── logica_proposicional.py     # [INT. 4] Lógica proposicional
    ├── razonamiento_probabilistico.py # [INT. 4] Probabilidades de riesgo
    └── agente_coordinador.py       # [INT. 1] Orquesta todos los agentes
```

---

## 🚀 Cómo ejecutar

```bash
# 1. Clonar el repositorio
git clone https://github.com/TU_USUARIO/invernadero-t2.git
cd invernadero-t2

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py
```

---

## 🔀 Flujo de trabajo GitHub (para el equipo)

```bash
# Cada integrante trabaja en su rama
git checkout -b feature/tu-modulo

# Subir cambios
git add .
git commit -m "feat: descripcion de tu cambio"
git push origin feature/tu-modulo

# Crear Pull Request en GitHub hacia main
# El integrante 1 revisa y hace merge
```

### Ramas sugeridas
- `feature/simulacion-datos` → Integrante 2
- `feature/procesamiento-imagenes` → Integrante 3
- `feature/sistema-experto` → Integrante 4
- `main` → Integrante 1 (coordina merges)

---

## ⚙️ Dependencias principales

- `streamlit` — Interfaz web
- `numpy`, `pandas`, `matplotlib` — Datos y gráficos
- `opencv-python` — Procesamiento de imágenes
- `pyDatalog` — Sistema experto
- `Pillow` — Manejo de imágenes

---

## 📊 Rúbrica de evaluación (20 pts)

| Criterio | Pts | Módulo responsable |
|---|---|---|
| Simulación de datos y análisis de señales | 3 | Integrante 2 |
| Procesamiento básico de imágenes | 3 | Integrante 3 |
| Sistema experto y representación del conocimiento | 4 | Integrante 4 |
| Diseño de agentes basados en conocimiento | 3 | Todos |
| Lógica proposicional y razonamiento probabilístico | 2 | Integrante 4 |
| Comunicación entre agentes y programación paralela | 3 | Integrantes 1 y 2 |
| Optimización, claridad técnica y presentación | 2 | Integrante 1 |
