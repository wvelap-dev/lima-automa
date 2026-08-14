"""
Lima Automa - Chatbot IA para Restaurantes
===========================================
Conversa automáticamente con restaurantes vía WhatsApp.
"""
import json
from datetime import datetime
from pathlib import Path


class ChatbotRestaurante:
    """
    Chatbot que habla con restaurantes interesados.
    """

    def __init__(self):
        self.conversaciones_file = Path("data/conversaciones.json")
        self.conversaciones = self._load_conversaciones()

    def _load_conversaciones(self):
        if self.conversaciones_file.exists():
            with open(self.conversaciones_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def _save_conversaciones(self):
        with open(self.conversaciones_file, "w", encoding="utf-8") as f:
            json.dump(self.conversaciones, f, ensure_ascii=False, indent=2)

    def iniciar_conversacion(self, restaurante, mensaje_inicial):
        """
        Inicia una nueva conversación con un restaurante.
        """
        restaurante_id = restaurante.get("nombre", "").lower().replace(" ", "_")

        conversacion = {
            "restaurante": restaurante.get("nombre"),
            "telefono": restaurante.get("telefono"),
            "distrito": restaurante.get("distrito"),
            "estado": "INICIADA",
            "historial": [
                {
                    "rol": "sistema",
                    "mensaje": mensaje_inicial,
                    "timestamp": datetime.now().isoformat(),
                }
            ],
            "calificacion": None,
            "cita_agendada": None,
            "notas": "",
        }

        self.conversaciones[restaurante_id] = conversacion
        self._save_conversaciones()

        return restaurante_id, conversacion

    def generar_respuesta(self, restaurante_id, mensaje_cliente):
        """
        Genera una respuesta usando IA basada en el historial.
        """
        conversacion = self.conversaciones.get(restaurante_id)
        if not conversacion:
            return None

        # Agregar mensaje del cliente al historial
        conversacion["historial"].append({
            "rol": "cliente",
            "mensaje": mensaje_cliente,
            "timestamp": datetime.now().isoformat(),
        })

        # Generar respuesta con IA
        respuesta = self._generar_respuesta_ia(conversacion, mensaje_cliente)

        # Agregar respuesta al historial
        conversacion["historial"].append({
            "rol": "sistema",
            "mensaje": respuesta,
            "timestamp": datetime.now().isoformat(),
        })

        self._save_conversaciones()

        return respuesta

    def _generar_respuesta_ia(self, conversacion, mensaje_cliente):
        """
        Genera respuesta usando OpenAI GPT-4o.
        """
        restaurante = conversacion.get("restaurante")
        distrito = conversacion.get("distrito")

        # System prompt para el chatbot
        system_prompt = f"""Eres un asistente de ventas de Lima Automa, una empresa que ayuda a restaurantes en Lima a conseguir más clientes.

Tu objetivo es:
1. Presentar nuestros servicios de manera atractiva
2. Responder preguntas del restaurante
3. Calificar si están interesados
4. Agendar una cita de 15 minutos por videollamada

Restaurante: {restaurante}
Distrito: {distrito}

Servicios que ofrecemos:
- Página web profesional gratis
- Aparición en Google Maps mejorada
- Sistema de reseñas automáticas
- Campañas de marketing digital
- **Sin costo inicial** - solo pagas por resultados

IMPORTANTE:
- Sé amigable y profesional
- No hables de precios todavía
- Enfócate en el beneficio para el restaurante
- Si preguntan por precios, di que explicamos todo en la videollamada
- Si quieren agendar, pregunta qué día les viene bien

Responde en español, de manera concisa (máximo 3-4 líneas)."""

        # Construir mensajes para OpenAI
        messages = [{"role": "system", "content": system_prompt}]

        # Agregar historial reciente (últimos 10 mensajes)
        historial = conversacion.get("historial", [])[-10:]
        for msg in historial:
            if msg["rol"] == "cliente":
                messages.append({"role": "user", "content": msg["mensaje"]})
            elif msg["rol"] == "sistema":
                messages.append({"role": "assistant", "content": msg["mensaje"]})

        # Llamar a OpenAI
        try:
            import openai
            client = openai.OpenAI()  # Usa OPENAI_API_KEY del entorno
            
            response = client.chat.completions.create(
                model="gpt-4o-mini",  # Modelo más económico
                messages=messages,
                max_tokens=200,
                temperature=0.7,
            )

            return response.choices[0].message.content

        except Exception as e:
            # Fallback si no hay API key
            return self._generar_respuesta_fallback(mensaje_cliente)

    def _generar_respuesta_fallback(self, mensaje_cliente):
        """
        Respuesta de fallback si no hay API de OpenAI.
        """
        mensaje_lower = mensaje_cliente.lower()

        if any(word in mensaje_lower for word in ["hola", "buenos", "buenas"]):
            return "¡Hola! Gracias por contactarnos. ¿En qué podemos ayudarlos?"
        
        elif any(word in mensaje_lower for word in ["precio", "costo", "cuanto"]):
            return "Tenemos planes muy accesibles. En la videollamada te explico todo personalizado. ¿Qué día te viene bien?"
        
        elif any(word in mensaje_lower for word in ["cita", "videollamada", "reunion"]):
            return "Perfecto. ¿Qué día y hora te viene bien? Tenemos disponibilidad de lunes a viernes."
        
        elif any(word in mensaje_lower for word in ["interes", "interesa", "quiero"]):
            return "¡Excelente! Vamos a agendar una cita para mostrarte todo. ¿Qué día te viene bien?"
        
        else:
            return "Gracias por tu mensaje. ¿Te gustaría que te mostremos cómo podemos ayudar a tu restaurante? Tenemos disponibilidad para una videollamada de 15 minutos."

    def calificar_interes(self, restaurante_id, calificacion):
        """
        Califica el nivel de interés del restaurante.
        """
        conversacion = self.conversaciones.get(restaurante_id)
        if conversacion:
            conversacion["calificacion"] = calificacion
            self._save_conversaciones()

    def agendar_cita(self, restaurante_id, fecha, hora):
        """
        Agenda una cita con el restaurante.
        """
        conversacion = self.conversaciones.get(restaurante_id)
        if conversacion:
            conversacion["cita_agendada"] = {
                "fecha": fecha,
                "hora": hora,
                "estado": "CONFIRMADA",
            }
            conversacion["estado"] = "CITA_AGENDADA"
            self._save_conversaciones()
            return True
        return False

    def obtener_conversaciones_pendientes(self):
        """
        Retorna conversaciones que necesitan atención.
        """
        pendientes = []
        for restaurante_id, conv in self.conversaciones.items():
            if conv.get("estado") in ["INICIADA", "EN_PROGRESO"]:
                pendientes.append({
                    "restaurante_id": restaurante_id,
                    "restaurante": conv.get("restaurante"),
                    "ultimo_mensaje": conv["historial"][-1] if conv["historial"] else None,
                    "calificacion": conv.get("calificacion"),
                })
        return pendientes

    def obtener_citas_pendientes(self):
        """
        Retorna citas agendadas que necesitan seguimiento.
        """
        citas = []
        for restaurante_id, conv in self.conversaciones.items():
            if conv.get("cita_agendada") and conv["cita_agendada"]["estado"] == "CONFIRMADA":
                citas.append({
                    "restaurante_id": restaurante_id,
                    "restaurante": conv.get("restaurante"),
                    "cita": conv.get("cita_agendada"),
                })
        return citas


# === TESTING ===
if __name__ == "__main__":
    print("=" * 60)
    print("  LIMA AUTOMA - Chatbot IA para Restaurantes")
    print("=" * 60)

    chatbot = ChatbotRestaurante()

    # Ejemplo de uso
    restaurante = {
        "nombre": "Cafe de Lima",
        "telefono": "+5112425555",
        "distrito": "Miraflores",
    }

    # Iniciar conversación
    restaurante_id, conv = chatbot.iniciar_conversacion(
        restaurante,
        "Hola, soy de Lima Automa. Vi que tienen un restaurante increíble en Miraflores. Tengo una propuesta que les puede ayudar a conseguir más clientes sin costo inicial. ¿Les gustaría escuchar?"
    )

    print(f"\n  Conversación iniciada con: {restaurante['nombre']}")
    print(f"  ID: {restaurante_id}")

    # Simular respuesta del cliente
    respuesta = chatbot.generar_respuesta(restaurante_id, "Hola, sí me interesa. ¿En qué consiste?")
    print(f"\n  Respuesta del bot: {respuesta}")

    # Simular otra respuesta
    respuesta2 = chatbot.generar_respuesta(restaurante_id, "¿Cuánto cuesta?")
    print(f"\n  Respuesta del bot: {respuesta2}")

    print("\n  Conversaciones guardadas en: data/conversaciones.json")
