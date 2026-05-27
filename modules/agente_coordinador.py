from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

@dataclass
class MensajeAgente:
    """
    Representa un mensaje intercambiado entre agentes.
    Simula el protocolo de comunicación del sistema multiagente.
    """
    origen: str
    destino: str
    tipo: str          # "datos" | "resultado" | "alerta" | "solicitud"
    contenido: dict
    timestamp: str = field(default_factory=lambda: datetime.now().strftime("%H:%M:%S"))

class AgenteCoordinador:
    """
    Coordinador central del sistema multiagente del invernadero.

    Flujo de comunicación:
        AgenteCoordinador
            → AgenteSensor      (solicita datos)
            ← AgenteSensor      (entrega lecturas)
            → AgenteSeñales     (envía series temporales)
            ← AgenteSeñales     (entrega análisis)
            → AgenteImagenes    (envía ruta de imagen)
            ← AgenteImagenes    (entrega diagnóstico)
            → AgenteDecisor     (envía todos los hechos)
            ← AgenteDecisor     (entrega recomendaciones)
            → UI Streamlit      (publica estado consolidado)
    """

    def __init__(self):
        self.log_mensajes: list[MensajeAgente] = []
        self.estado_consolidado: dict = {}

    def _registrar(self, mensaje: MensajeAgente) -> None:
        self.log_mensajes.append(mensaje)

    def solicitar_datos_sensor(self, agente_sensor_fn) -> dict:
        """Paso 1: pide datos al AgenteSensor."""
        self._registrar(MensajeAgente(
            origen="Coordinador", destino="AgenteSensor",
            tipo="solicitud", contenido={"accion": "obtener_lecturas"},
        ))
        datos = agente_sensor_fn()
        self._registrar(MensajeAgente(
            origen="AgenteSensor", destino="Coordinador",
            tipo="datos", contenido=datos,
        ))
        return datos

    def enviar_a_agente_senales(self, agente_senales_fn, df) -> list:
        """Paso 2: pide al AgenteSeñales que analice las series temporales."""
        self._registrar(MensajeAgente(
            origen="Coordinador", destino="AgenteSeñales",
            tipo="datos", contenido={"n_registros": len(df)},
        ))
        reporte = agente_senales_fn(df)
        self._registrar(MensajeAgente(
            origen="AgenteSeñales", destino="Coordinador",
            tipo="resultado", contenido={"n_reportes": len(reporte)},
        ))
        return reporte

    def enviar_a_agente_imagenes(self, agente_imagenes_fn, ruta: str) -> dict:
        """Paso 3: pide al AgenteImagenes que procese la hoja."""
        self._registrar(MensajeAgente(
            origen="Coordinador", destino="AgenteImagenes",
            tipo="solicitud", contenido={"imagen": ruta},
        ))
        resultado = agente_imagenes_fn(ruta)
        self._registrar(MensajeAgente(
            origen="AgenteImagenes", destino="Coordinador",
            tipo="resultado",
            contenido={
                "estado": resultado["estado"],
                "porcentaje_dano": resultado["porcentaje_dano"],
            },
        ))
        return resultado

    def enviar_a_agente_decisor(self, agente_decisor_fn,
                                 datos: dict, estado_hoja: str) -> dict:
        """Paso 4: pide al AgenteDecisor que emita recomendaciones."""
        self._registrar(MensajeAgente(
            origen="Coordinador", destino="AgenteDecisor",
            tipo="datos",
            contenido={**datos, "estado_hoja": estado_hoja},
        ))
        decision = agente_decisor_fn(
            temperatura=datos["temperatura"],
            humedad_suelo=datos["humedad_suelo"],
            intensidad_luz=datos["intensidad_luz"],
            estado_hoja=estado_hoja,
        )
        self._registrar(MensajeAgente(
            origen="AgenteDecisor", destino="Coordinador",
            tipo="alerta",
            contenido={"recomendaciones": decision["recomendaciones"]},
        ))
        return decision

    def consolidar_estado(
        self,
        datos_sensor: dict,
        reporte_senales: list,
        resultado_imagen: dict,
        decision: dict,
        riesgo: dict,
    ) -> dict:
        """
        Integra todos los resultados en un único estado del sistema.
        Este objeto es el que consume la UI de Streamlit.
        """
        self._registrar(MensajeAgente(
            origen="Coordinador", destino="UI",
            tipo="resultado",
            contenido={"estado": "listo", "n_recomendaciones": len(decision["recomendaciones"])},
        ))

        self.estado_consolidado = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "sensores": datos_sensor,
            "senales": reporte_senales,
            "imagen": {
                "estado": resultado_imagen["estado"],
                "porcentaje_dano": resultado_imagen["porcentaje_dano"],
                "diagnostico": resultado_imagen["diagnostico"],
            },
            "experto": {
                "hechos": decision["hechos"],
                "recomendaciones": decision["recomendaciones"],
            },
            "riesgo": {
                "nivel": riesgo["nivel_global"],
                "probabilidad": riesgo["riesgo_global"],
            },
        }
        return self.estado_consolidado

    def obtener_log_comunicacion(self) -> list[dict]:
        """Retorna el log de mensajes para visualizar en la UI."""
        return [
            {
                "tiempo": m.timestamp,
                "de": m.origen,
                "para": m.destino,
                "tipo": m.tipo,
            }
            for m in self.log_mensajes
        ]
