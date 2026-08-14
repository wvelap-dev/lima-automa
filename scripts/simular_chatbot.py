"""
Lima Automa - Simulación de Chatbot con Audio
==============================================
Simula una conversación de WhatsApp con el chatbot.
"""
import sys
sys.path.insert(0, 'src')

import json
import time
from datetime import datetime
from chatbot_ia import ChatbotRestaurante


def simular_conversacion():
    """
    Simula una conversación completa con un restaurante.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Simulación de Chatbot con Audio")
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
    print(f"  Simulando conversación de WhatsApp...\n")

    # Iniciar conversación
    restaurante_id, conv = chatbot.iniciar_conversacion(
        restaurante,
        "¡Hola! Soy Claudia de Lima Automa 👋 Vi que tienen un restaurante increíble en Miraflores. Tengo una propuesta que les puede ayudar a conseguir más clientes sin costo inicial. ¿Les gustaría escuchar?"
    )

    # Mensajes de la conversación
    mensajes = [
        ("cliente", "Hola, sí me interesa. ¿En qué consiste?"),
        ("cliente", "¿Cuánto cuesta?"),
        ("cliente", "Suena bien. ¿Cuándo podemos hablar?"),
        ("cliente", "El viernes a las 10am me viene bien"),
    ]

    print("  [CONVERSACIÓN INICIADA]")
    print("  " + "-" * 40)

    for rol, mensaje in mensajes:
        # Mostrar mensaje del cliente
        print(f"\n  [CLIENTE] {mensaje}")
        
        # Generar respuesta del bot
        respuesta = chatbot.generar_respuesta(restaurante_id, mensaje)
        print(f"  [CLAUDIA] {respuesta}")
        
        # Simular delay de audio
        time.sleep(1)

    # Agendar cita
    chatbot.agendar_cita(restaurante_id, "2026-08-22", "10:00")
    print(f"\n  [SISTEMA] Cita agendada: viernes 22 agosto a las 10:00")

    # Mostrar resumen
    print("\n" + "=" * 60)
    print("  RESUMEN DE LA SIMULACIÓN")
    print("=" * 60)
    print(f"\n  Restaurante: {restaurante['nombre']}")
    print(f"  Distrito: {restaurante['distrito']}")
    print(f"  Estado: {conv.get('estado')}")
    print(f"  Citas agendadas: 1")
    print(f"  Conversación guardada en: data/conversaciones.json")

    return conv


def simular_varios_restaurantes():
    """
    Simula conversaciones con varios restaurantes.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Simulación con Varios Restaurantes")
    print("=" * 60)

    chatbot = ChatbotRestaurante()

    restaurantes = [
        {"nombre": "Cafe de Lima", "telefono": "+5112425555", "distrito": "Miraflores"},
        {"nombre": "La Panka", "telefono": "+5114474646", "distrito": "Miraflores"},
        {"nombre": "Victoria", "telefono": "+5112472404", "distrito": "Barranco"},
    ]

    for restaurante in restaurantes:
        print(f"\n  Simulando: {restaurante['nombre']}")
        print("  " + "-" * 40)

        # Iniciar conversación
        restaurante_id, conv = chatbot.iniciar_conversacion(
            restaurante,
            f"Hola, soy de Lima Automa. Vi que tienen {restaurante['nombre']} en {restaurante['distrito']}. Tengo una propuesta que les puede ayudar a conseguir más clientes sin costo inicial. ¿Les gustaría escuchar?"
        )

        # Mensaje del cliente
        respuesta = chatbot.generar_respuesta(restaurante_id, "Hola, sí me interesa")
        print(f"  [BOT] {respuesta}")

        # Respuesta del bot
        respuesta2 = chatbot.generar_respuesta(restaurante_id, "¿Cuándo podemos hablar?")
        print(f"  [BOT] {respuesta2}")

    # Mostrar resumen
    pendientes = chatbot.obtener_conversaciones_pendientes()
    print(f"\n  Conversaciones activas: {len(pendientes)}")
    print("  Simulación completada.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "varios":
            simular_varios_restaurantes()
        else:
            print("Comandos: (sin args) o 'varios'")
    else:
        simular_conversacion()
