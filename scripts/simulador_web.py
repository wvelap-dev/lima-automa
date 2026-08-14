"""
Lima Automa - Simulación Interactiva del Chatbot
=================================================
Interfaz web para simular conversaciones con el chatbot.
"""
import sys
sys.path.insert(0, 'src')

import json
from datetime import datetime
from pathlib import Path


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simulación Chatbot - Lima Automa</title>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Poppins', sans-serif;
            background: #0a0a0a;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            padding: 20px;
        }
        .container {
            max-width: 400px;
            width: 100%;
        }
        .phone {
            background: #1a1a1a;
            border-radius: 30px;
            padding: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        .header {
            background: #075e54;
            padding: 15px;
            border-radius: 20px 20px 0 0;
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .avatar {
            width: 40px;
            height: 40px;
            background: #25d366;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 18px;
            font-weight: bold;
            color: white;
        }
        .header-info {
            flex: 1;
        }
        .header-name {
            color: white;
            font-weight: 600;
            font-size: 14px;
        }
        .header-status {
            color: #8696a0;
            font-size: 12px;
        }
        .chat {
            background: #0b141a;
            padding: 20px;
            height: 400px;
            overflow-y: auto;
        }
        .message {
            max-width: 80%;
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 10px;
            font-size: 14px;
            line-height: 1.4;
        }
        .bot {
            background: #1f2c34;
            color: white;
            margin-right: auto;
            border-bottom-left-radius: 0;
        }
        .cliente {
            background: #005c4b;
            color: white;
            margin-left: auto;
            border-bottom-right-radius: 0;
        }
        .time {
            font-size: 10px;
            color: #8696a0;
            margin-top: 5px;
            text-align: right;
        }
        .input-area {
            background: #1f2c34;
            padding: 15px;
            border-radius: 0 0 20px 20px;
            display: flex;
            gap: 10px;
        }
        .input {
            flex: 1;
            background: #2a3942;
            border: none;
            border-radius: 20px;
            padding: 12px 15px;
            color: white;
            font-size: 14px;
        }
        .input::placeholder { color: #8696a0; }
        .send-btn {
            background: #00a884;
            border: none;
            border-radius: 50%;
            width: 45px;
            height: 45px;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .send-btn:hover { background: #00c49a; }
        .send-icon {
            width: 20px;
            height: 20px;
            fill: white;
        }
        .controls {
            margin-top: 20px;
            display: flex;
            gap: 10px;
        }
        .ctrl-btn {
            flex: 1;
            background: #25d366;
            border: none;
            border-radius: 10px;
            padding: 12px;
            color: white;
            font-weight: 600;
            cursor: pointer;
        }
        .ctrl-btn:hover { background: #20bd5a; }
        .ctrl-btn.secondary { background: #6b7b8d; }
    </style>
</head>
<body>
    <div class="container">
        <div class="phone">
            <div class="header">
                <div class="avatar">CL</div>
                <div class="header-info">
                    <div class="header-name">Claudia - Lima Automa</div>
                    <div class="header-status">online</div>
                </div>
            </div>
            <div class="chat" id="chat">
                <div class="message bot">
                    ¡Hola! Soy Claudia de Lima Automa 👋 Vi que tienen un restaurante increíble en Miraflores. Tengo una propuesta que les puede ayudar a conseguir más clientes sin costo inicial. ¿Les gustaría escuchar?
                    <div class="time">10:00</div>
                </div>
            </div>
            <div class="input-area">
                <input type="text" class="input" id="input" placeholder="Escribe un mensaje...">
                <button class="send-btn" onclick="enviarMensaje()">
                    <svg class="send-icon" viewBox="0 0 24 24">
                        <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
                    </svg>
                </button>
            </div>
        </div>
        <div class="controls">
            <button class="ctrl-btn" onclick="respuestaRapida('interes')">Me interesa</button>
            <button class="ctrl-btn secondary" onclick="respuestaRapida('precio')">¿Precio?</button>
        </div>
        <div class="controls">
            <button class="ctrl-btn" onclick="respuestaRapida('cita')">Agendar cita</button>
            <button class="ctrl-btn secondary" onclick="respuestaRapida('adios')">Adiós</button>
        </div>
    </div>

    <script>
        const chat = document.getElementById('chat');
        const input = document.getElementById('input');
        
        const respuestas = {
            'interes': 'Hola, sí me interesa. ¿En qué consiste?',
            'precio': '¿Cuánto cuesta?',
            'cita': 'Suena bien. ¿Cuándo podemos hablar?',
            'adios': 'Gracias, bye!'
        };
        
        const respuestasBot = {
            'interes': '¡Qué bueno! 😊 Te explico: ayudamos a restaurantes a conseguir más clientes con página web gratis y marketing digital. ¿Te gustaría agendar una videollamada de 15 minutos?',
            'precio': 'Tenemos planes muy accesibles y personalizados para cada restaurante. En la videollamada te explico todo sin compromiso. ¿Qué día te viene bien?',
            'cita': 'Perfecto 📅 Tenemos disponibilidad de lunes a viernes de 9am a 5pm. ¿Qué día y hora te viene bien?',
            'adios': '¡Hasta luego! 👋 Si cambias de opinión, aquí estamos para ayudarte. ¡Éxitos con el restaurante!'
        };
        
        function agregarMensaje(texto, esBot) {
            const now = new Date();
            const time = now.getHours().toString().padStart(2, '0') + ':' + 
                        now.getMinutes().toString().padStart(2, '0');
            
            const msg = document.createElement('div');
            msg.className = `message ${esBot ? 'bot' : 'cliente'}`;
            msg.innerHTML = `${texto}<div class="time">${time}</div>`;
            chat.appendChild(msg);
            chat.scrollTop = chat.scrollHeight;
        }
        
        function enviarMensaje() {
            const texto = input.value.trim();
            if (!texto) return;
            
            agregarMensaje(texto, false);
            input.value = '';
            
            setTimeout(() => {
                const respuesta = respuestasBot[texto.toLowerCase()] || 
                    '¡Hola! Soy Claudia de Lima Automa. Estoy aquí para ayudarte a conseguir más clientes para tu restaurante. ¿Te gustaría saber cómo?';
                agregarMensaje(respuesta, true);
            }, 1000);
        }
        
        function respuestaRapida(tipo) {
            const texto = respuestas[tipo];
            agregarMensaje(texto, false);
            
            setTimeout(() => {
                agregarMensaje(respuestasBot[tipo], true);
            }, 1000);
        }
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') enviarMensaje();
        });
    </script>
</body>
</html>"""


def crear_simulador_web():
    """
    Crea un archivo HTML para simular el chatbot.
    """
    output_file = Path("simulador_chatbot.html")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(HTML_TEMPLATE)
    
    print(f"Simulador creado: {output_file}")
    print("Abre el archivo en tu navegador para probarlo.")
    
    return output_file


if __name__ == "__main__":
    print("=" * 60)
    print("  LIMA AUTOMA - Simulador Web del Chatbot")
    print("=" * 60)
    
    archivo = crear_simulador_web()
    
    print("\n  Instrucciones:")
    print(f"  1. Abre {archivo} en tu navegador")
    print("  2. Escribe mensajes o usa los botones rápidos")
    print("  3. El chatbot responderá automáticamente")
