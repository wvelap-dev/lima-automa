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
        Genera respuesta usando Ollama (local) o fallback si no está disponible.
        """
        restaurante = conversacion.get("restaurante")
        distrito = conversacion.get("distrito")

        # System prompt para el chatbot
        system_prompt = f"""Eres Claudia, una asistente de ventas de Lima Automa. Hablas con restaurantes en Lima para ofrecer nuestros servicios de marketing digital.

Tu objetivo es:
1. Presentarte como Claudia de Lima Automa
2. Explicar nuestros servicios de manera clara y atractiva
3. Responder preguntas del restaurante
4. Calificar si están interesados
5. Agendar una cita de 15 minutos por videollamada

Restaurante: {restaurante}
Distrito: {distrito}

Servicios que ofrecemos:
- Página web profesional gratis para tu restaurante
- Aparición en Google Maps mejorada
- Sistema de reseñas automáticas para mejorar tu calificación
- Campañas de marketing digital dirigidas
- **Sin costo inicial** - solo pagas por resultados

IMPORTANTE:
- Siempre preséntate como "Claudia de Lima Automa"
- Sé amigable, profesional y natural
- No hables de precios todavía, solo di que explicarás todo en la videollamada
- Enfócate en el beneficio para el restaurante específico
- Si preguntan por precios, di que explicarás los planes personalizados en la videollamada
- Si quieren agendar, pregunta qué día y hora les viene bien
- Si responden con hora como "4pm", confirma la cita
- Si dicen "sí" o "si", pregunta si quieren agendar una cita
- Varía tus respuestas, no repitas lo mismo
- Usa emojis ocasionalmente para ser más cercana

Responde en español, de manera concisa (máximo 2-3 líneas)."""

        # Construir mensajes para Ollama
        messages = [{"role": "system", "content": system_prompt}]

        # Agregar historial reciente (últimos 10 mensajes)
        historial = conversacion.get("historial", [])[-10:]
        for msg in historial:
            if msg["rol"] == "cliente":
                messages.append({"role": "user", "content": msg["mensaje"]})
            elif msg["rol"] == "sistema":
                messages.append({"role": "assistant", "content": msg["mensaje"]})

        # Intentar con Ollama primero (local, gratis)
        try:
            import httpx
            
            response = httpx.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": "qwen2.5:14b",  # Mejor para español
                    "messages": messages,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "num_predict": 200,  # Máximo tokens
                    }
                },
                timeout=30.0,  # 30 segundos timeout
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("message", {}).get("content", "")
            else:
                # Si Ollama falla, usar fallback
                return self._generar_respuesta_fallback(mensaje_cliente)
                
        except Exception as e:
            # Si Ollama no está corriendo, usar fallback
            print(f"Ollama no disponible: {e}")
            return self._generar_respuesta_fallback(mensaje_cliente)

    def _generar_respuesta_fallback(self, mensaje_cliente):
        """
        Respuesta de fallback si no hay API de OpenAI.
        """
        mensaje_lower = mensaje_cliente.lower().strip()

        # Saludos
        if any(word in mensaje_lower for word in ["hola", "buenos", "buenas", "hey"]):
            return "Hola! Soy Claudia de Lima Automa. Vi que tienen un restaurante increible. Les gustaria saber como conseguir mas clientes?"
        
        # Interés
        if any(word in mensaje_lower for word in ["interes", "interesa", "quiero", "si", "sí"]):
            return "Que bueno! Te explico: ayudamos a restaurantes a conseguir mas clientes con pagina web gratis y marketing digital. Te gustaria agendar una videollamada de 15 minutos?"
        
        # Precios
        if any(word in mensaje_lower for word in ["precio", "costo", "cuanto", "cuánto", "cuanto cuesta"]):
            return "Tenemos planes muy accesibles y personalizados para cada restaurante. En la videollamada te explico todo sin compromiso. Que dia te viene bien?"
        
        # Agendar cita
        if any(word in mensaje_lower for word in ["cita", "videollamada", "reunion", "reunión", "hablar", "cuando", "cuándo"]):
            return "Perfecto. Tenemos disponibilidad de lunes a viernes de 9am a 5pm. Que dia y hora te viene bien?"
        
        # Horas específicas
        if any(word in mensaje_lower for word in ["am", "pm", "mañana", "tarde", "hora"]):
            return "Perfecto! Anoto tu cita. Te enviare un recordatorio un dia antes. Confirmas?"
        
        # Confirmación
        if any(word in mensaje_lower for word in ["confirmo", "confirmado", "ok", "dale", "bien", "perfecto"]):
            return "Excelente! Tu cita esta confirmada. Te envio los datos por WhatsApp. Nos vemos pronto!"
        
        # Despedida
        if any(word in mensaje_lower for word in ["adios", "adiós", "bye", "chau", "hasta luego", "nos vemos"]):
            return "Hasta luego! Si cambias de opinion, aqui estamos para ayudarte. Exitos con el restaurante!"
        
        # Agradecimiento
        if any(word in mensaje_lower for word in ["gracias", "thank"]):
            return "Con gusto! Si tienes alguna otra pregunta, no dudes en preguntar. Te gustaria agendar una videollamada?"
        
        # Preguntas sobre servicios
        if any(word in mensaje_lower for word in ["servicio", "servicios", "que hacen", "qué hacen", "ayuda"]):
            return "Ofrecemos: pagina web gratis, mejoras en Google Maps, sistema de reseñas automaticas y marketing digital. Te gustaria saber mas?"
        
        # Preguntas sobre la empresa
        if any(word in mensaje_lower for word in ["empresa", "quienes son", "quién eres", "lima automa"]):
            return "Somos Lima Automa, ayudamos a restaurantes en Lima a conseguir mas clientes. Soy Claudia, tu asesora. En que te puedo ayudar?"
        
        # Respuesta genérica
        return "Hola! Soy Claudia de Lima Automa. Estoy aqui para ayudarte a conseguir mas clientes para tu restaurante. Te gustaria saber como?"

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
