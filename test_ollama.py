import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot_ia import ChatbotRestaurante

chatbot = ChatbotRestaurante()

# Test restaurant
restaurante = {
    'nombre': 'Cafe de Lima',
    'telefono': '+5112425555',
    'distrito': 'Miraflores',
}

# Start conversation
restaurante_id, conv = chatbot.iniciar_conversacion(
    restaurante,
    'Hola, soy de Lima Automa. Vi que tienen un restaurante increible en Miraflores.'
)

print('Conversacion iniciada con:', restaurante['nombre'])
print('ID:', restaurante_id)
print()

# Test first response
respuesta = chatbot.generar_respuesta(restaurante_id, 'Hola, si me interesa. En que consiste?')
print('Respuesta 1:', respuesta)
print()

# Test second response
respuesta2 = chatbot.generar_respuesta(restaurante_id, 'Cuanto cuesta?')
print('Respuesta 2:', respuesta2)
