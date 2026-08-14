"""
Lima Automa - Test del Chatbot con Ollama
==========================================
Verifica que Ollama está funcionando y prueba el chatbot.
"""
import sys
sys.path.insert(0, 'src')

from chatbot_ia import ChatbotRestaurante


def test_ollama_connection():
    """Verifica que Ollama está corriendo."""
    import httpx
    
    try:
        response = httpx.get("http://localhost:11434/api/tags", timeout=5.0)
        if response.status_code == 200:
            models = response.json().get("models", [])
            print(f"Ollama OK - Modelos disponibles: {len(models)}")
            for m in models:
                print(f"  - {m['name']}")
            return True
    except Exception as e:
        print(f"Error: Ollama no está corriendo - {e}")
        print("Inicia Ollama con: ollama serve")
        return False


def test_chatbot():
    """Prueba el chatbot con una conversación simulada."""
    chatbot = ChatbotRestaurante()
    
    restaurante = {
        'nombre': 'Cafe de Lima',
        'telefono': '+5112425555',
        'distrito': 'Miraflores',
    }
    
    # Iniciar conversación
    restaurante_id, conv = chatbot.iniciar_conversacion(
        restaurante,
        'Hola, soy de Lima Automa. Vi que tienen un restaurante increíble en Miraflores.'
    )
    
    print(f"\nConversación con: {restaurante['nombre']}")
    print("-" * 50)
    
    # Probar diferentes mensajes
    test_messages = [
        "Hola, sí me interesa. ¿En qué consiste?",
        "¿Cuánto cuesta?",
        "Suena bien. ¿Cuándo podemos hablar?",
    ]
    
    for msg in test_messages:
        print(f"Cliente: {msg}")
        respuesta = chatbot.generar_respuesta(restaurante_id, msg)
        # Remove emojis for console output
        respuesta_limpia = ''.join(c for c in respuesta if ord(c) < 128)
        print(f"Claudia: {respuesta_limpia}")
        print()


if __name__ == "__main__":
    print("=" * 60)
    print("  LIMA AUTOMA - Test Chatbot Ollama")
    print("=" * 60)
    
    if test_ollama_connection():
        print()
        test_chatbot()
    else:
        print("\nNo se puede probar el chatbot sin Ollama.")
