"""
Lima Automa - Script de prueba del Chatbot IA
==============================================
Simula una conversación con un restaurante.
"""
import sys
sys.path.insert(0, 'src')

from chatbot_ia import ChatbotRestaurante


def main():
    print("=" * 60)
    print("  LIMA AUTOMA - Prueba del Chatbot IA")
    print("=" * 60)

    chatbot = ChatbotRestaurante()

    # Restaurante de prueba
    restaurante = {
        "nombre": "Cafe de Lima",
        "telefono": "+5112425555",
        "distrito": "Miraflores",
    }

    print(f"\n  Restaurante: {restaurante['nombre']}")
    print(f"  Distrito: {restaurante['distrito']}")

    # Iniciar conversación
    restaurante_id, conv = chatbot.iniciar_conversacion(
        restaurante,
        "¡Hola! Soy Claudia de Lima Automa 👋 Vi que tienen un restaurante increíble en Miraflores. Tengo una propuesta que les puede ayudar a conseguir más clientes sin costo inicial. ¿Les gustaría escuchar?"
    )

    print(f"\n  [CLAUDIA] Hola! Soy Claudia de Lima Automa. Vi que tienen un restaurante increible en Miraflores. Tengo una propuesta que les puede ayudar a conseguir mas clientes sin costo inicial. Les gustaria escuchar?")

    # Simular conversación
    mensajes_cliente = [
        "Hola, sí me interesa. ¿En qué consiste?",
        "¿Cuánto cuesta?",
        "Suena bien. ¿Cuándo podemos hablar?",
        "El viernes a las 10am me viene bien",
    ]

    for mensaje in mensajes_cliente:
        print(f"\n  [CLIENTE] {mensaje}")
        respuesta = chatbot.generar_respuesta(restaurante_id, mensaje)
        print(f"  [CLAUDIA] {respuesta}")

    # Agendar cita
    chatbot.agendar_cita(restaurante_id, "2026-08-22", "10:00")
    print(f"\n  [SISTEMA] Cita agendada: viernes 22 agosto a las 10:00")

    # Ver conversaciones pendientes
    pendientes = chatbot.obtener_conversaciones_pendientes()
    print(f"\n  Conversaciones pendientes: {len(pendientes)}")

    # Ver citas pendientes
    citas = chatbot.obtener_citas_pendientes()
    print(f"  Citas pendientes: {len(citas)}")

    print("\n" + "=" * 60)
    print("  PRUEBA COMPLETADA")
    print("=" * 60)
    print("\n  Archivos generados:")
    print("  - data/conversaciones.json")


if __name__ == "__main__":
    main()
