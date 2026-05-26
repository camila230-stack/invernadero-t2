# 📋 GUÍA PARA CADA INTEGRANTE — T2 Invernadero Inteligente

## ✅ INTEGRANTE 1 — Tú (Streamlit + Coordinador)

**Archivos a subir:**
- `app.py`
- `modules/agente_coordinador.py`
- `requirements.txt`
- `README.md`
- `GUIA_INTEGRANTES.md`

**Tu parte cubre:**
- Interfaz web completa (Streamlit)
- Coordinación entre todos los agentes
- Parte I: comunicación entre agentes
- Parte K: optimización (el dashboard prioriza alertas por nivel de riesgo)

**Rama:** `main` (tú haces los merges de todos)

**Comandos:**
```bash
git init
git add .
git commit -m "feat: estructura inicial + app Streamlit + coordinador"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/invernadero-t2.git
git push -u origin main
```

---

## ✅ INTEGRANTE 2 — Simulación + Señales + Paralelismo

**Archivos a trabajar:**
- `modules/agente_sensor.py`
- `modules/agente_senales.py`
- `modules/paralelismo.py`

**Tu parte cubre:**
- Parte A: simulación de datos (120 registros, 4 variables, 2 gráficos)
- Parte B: análisis de señales (anomalías, tendencias, picos)
- Parte J: programación paralela (threading con 3 hilos)

**Comandos para subir tu parte:**
```bash
git clone https://github.com/TU_USUARIO/invernadero-t2.git
cd invernadero-t2
git checkout -b feature/simulacion-datos
# [modifica tus archivos si quieres personalizarlos]
git add modules/agente_sensor.py modules/agente_senales.py modules/paralelismo.py
git commit -m "feat: simulación de datos, análisis de señales y paralelismo"
git push origin feature/simulacion-datos
# → Crea un Pull Request en GitHub hacia main
```

**Cosas que puedes personalizar:**
- Cambiar los rangos de temperatura/humedad en `agente_sensor.py`
- Ajustar el umbral de anomalía en `agente_senales.py`
- Agregar un 4to hilo en `paralelismo.py`

---

## ✅ INTEGRANTE 3 — OpenCV (Procesamiento de imágenes)

**Archivos a trabajar:**
- `modules/agente_imagenes.py`
- `assets/images/hoja1.jpg` (puedes agregar imágenes reales)
- `assets/images/hoja2.jpg`
- `assets/images/hoja3.jpg`

**Tu parte cubre:**
- Parte C: procesamiento de imágenes (carga, grises, umbral, bordes, segmentación)

**Comandos para subir tu parte:**
```bash
git clone https://github.com/TU_USUARIO/invernadero-t2.git
cd invernadero-t2
git checkout -b feature/procesamiento-imagenes
# [agrega imágenes reales en assets/images/ si tienes]
git add modules/agente_imagenes.py assets/images/
git commit -m "feat: procesamiento de imágenes con OpenCV"
git push origin feature/procesamiento-imagenes
# → Crea un Pull Request en GitHub hacia main
```

**Cosas que puedes personalizar:**
- Reemplazar las imágenes sintéticas con fotos reales de hojas
- Ajustar los rangos HSV para tu tipo de planta
- Agregar más operaciones de procesamiento (morfología, filtros)

---

## ✅ INTEGRANTE 4 — pyDatalog + Lógica + Probabilidad

**Archivos a trabajar:**
- `modules/agente_decisor.py`
- `modules/logica_proposicional.py`
- `modules/razonamiento_probabilistico.py`

**Tu parte cubre:**
- Parte D: sistema experto (8 hechos, 6 reglas, pyDatalog)
- Parte E: representación del conocimiento
- Parte G: lógica proposicional (5 proposiciones, 4 expresiones)
- Parte H: razonamiento probabilístico (5 situaciones justificadas)

**Comandos para subir tu parte:**
```bash
git clone https://github.com/TU_USUARIO/invernadero-t2.git
cd invernadero-t2
git checkout -b feature/sistema-experto
git add modules/agente_decisor.py modules/logica_proposicional.py modules/razonamiento_probabilistico.py
git commit -m "feat: sistema experto pyDatalog + lógica proposicional + probabilidad"
git push origin feature/sistema-experto
# → Crea un Pull Request en GitHub hacia main
```

**Cosas que puedes personalizar:**
- Agregar más reglas en `agente_decisor.py` (mínimo 6, puedes poner más)
- Cambiar las probabilidades en `razonamiento_probabilistico.py` con justificación
- Ampliar las proposiciones lógicas

---

## 🔀 Proceso de merge (Integrante 1)

1. Cada integrante crea su Pull Request en GitHub
2. Tú revisas que el código no rompa `app.py`
3. Haces merge de cada rama hacia `main`
4. Pruebas locales: `streamlit run app.py`
5. Capturas de pantalla para el informe (Entregable 4)
