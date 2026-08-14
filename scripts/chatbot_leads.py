"""
Lima Automa - Integración Chatbot con Leads
============================================
Conecta el chatbot IA con los leads existentes.
"""
import sys
sys.path.insert(0, 'src')

import json
from chatbot_ia import ChatbotRestaurante
from whatsapp_automation import WhatsAppAutomation


def iniciar_chatbots_leads():
    """
    Inicia chatbots para todos los leads pendientes.
    """
    print("=" * 60)
    print("  LIMA AUTOMA - Iniciando Chatbots para Leads")
    print("=" * 60)

    # Cargar leads
    automation = WhatsAppAutomation()
    chatbot = ChatbotRestaurante()

    leads_pendientes = [
        lead for lead in automation.leads
        if lead.get("estado") == "PENDIENTE_ENVIO"
    ]

    print(f"\n  Leads pendientes: {len(leads_pendientes)}")

    for lead in leads_pendientes[:5]:  # Top 5
        restaurante = {
            "nombre": lead.get("restaurante"),
            "telefono": lead.get("telefono"),
            "distrito": lead.get("distrito", "Lima"),
        }

        # Mensaje inicial personalizado
        mensaje_inicial = lead.get("mensaje_inicial", "")

        # Iniciar conversación
        restaurante_id, conv = chatbot.iniciar_conversacion(
            restaurante,
            mensaje_inicial
        )

        print(f"\n  Chatbot iniciado para: {restaurante['nombre']}")
        print(f"  ID: {restaurante_id}")
        print(f"  Estado: {conv.get('estado')}")

    print("\n" + "=" * 60)
    print("  CHATBOTS INICIADOS")
    print("=" * 60)
    print("\n  Próximo paso: Enviar mensajes vía WhatsApp API")


def ver_estado_chatbots():
    """
    Muestra el estado de todos los chatbots activos.
    """
    chatbot = ChatbotRestaurante()

    print("=" * 60)
    print("  LIMA AUTOMA - Estado de Chatbots")
    print("=" * 60)

    pendientes = chatbot.obtener_conversaciones_pendientes()
    citas = chatbot.obtener_citas_pendientes()

    print(f"\n  Conversaciones pendientes: {len(pendientes)}")
    for p in pendientes:
        print(f"    - {p['restaurante']}: {p.get('calificacion', 'Sin calificar')}")

    print(f"\n  Citas agendadas: {len(citas)}")
    for c in citas:
        print(f"    - {c['restaurante']}: {c['cita']['fecha']} {c['cita']['hora']}")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "iniciar":
            iniciar_chatbots_leads()
        elif command == "estado":
            ver_estado_chatbots()
        else:
            print("Comandos: iniciar, estado")
    else:
        iniciar_chatbots_leads()
