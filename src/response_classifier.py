"""
Lima Automa - Clasificador de Respuestas con IA
================================================
Usa GPT para clasificar respuestas de restaurantes.
"""
import json
import os


# Prompts para clasificacion
SYSTEM_PROMPT = """Eres un clasificador de respuestas de ventas B2B para un mercado 
de restaurantes en Lima, Peru. Tu trabajo es clasificar las respuestas de los 
duenos de restaurantes cuando reciben un mensaje de prospeccion.

Clasifica cada respuesta en UNA de estas categorias:

1. CALIENTE (score 80-100): La persona esta interesada y quiere avanzar.
   Ejemplos: "si me interesa", "cuando podemos hablar", "envieme info", 
   "dale", "ok", "perfecto", "cuando quedamos"

2. TIBIO (score 40-70): Muestra interes pero no esta listo para decidir.
   Ejemplos: "despues", "piensalo", "mandame info", "interesante", 
   "voy a ver", "no ahora pero tal vez"

3. FRIO (score 10-30): Rechazo suave o no interesado.
   Ejemplos: "no gracias", "no me interesa", "ya tengo", "estoy ocupado"

4. NO_RESPONDE (score 0): No hubo respuesta o respuesta vacia.

5. INDEFINIDO (score 30-50): Respuesta ambigua que requiere revision humana.

Responde UNICAMENTE con un JSON valido con esta estructura:
{
    "tipo": "CALIENTE|TIBIO|FRIO|NO_RESPONDE|INDEFINIDO",
    "score": 0-100,
    "razon": "Breve explicacion de por que clasificaste asi",
    "accion": "Que hacer a continuacion",
    "confianza": 0.0-1.0
}"""


def clasificar_respuesta_ia(respuesta_texto, api_key=None):
    """
    Clasifica una respuesta usando GPT.
    """
    if not api_key:
        api_key = os.environ.get("OPENAI_API_KEY")

    if not api_key:
        # Fallback: clasificacion por palabras clave
        return clasificar_respuesta_basica(respuesta_texto)

    try:
        import openai
        client = openai.OpenAI(api_key=api_key)

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Clasifica esta respuesta: '{respuesta_texto}'"}
            ],
            temperature=0.3,
            max_tokens=200,
        )

        resultado = response.choices[0].message.content
        return json.loads(resultado)

    except Exception as e:
        print(f"Error con IA: {e}")
        return clasificar_respuesta_basica(respuesta_texto)


def clasificar_respuesta_basica(texto):
    """
    Clasificacion por palabras clave (sin IA).
    """
    texto_lower = texto.lower()

    calientes = [
        "si", "claro", "cuando", "como", "quiero", "me interesa",
        "envieme", "mandame", "dame info", "cuanto cuesta",
        "videollamada", "reunion", "hablamos", "dale", "ok",
        "perfecto", "genial", "excelente", "estoy interesado",
        "contactame", "llamame", "escribeme",
    ]

    tibios = [
        "despues", "luego", "piensalo", "no se", "tal vez",
        "quizas", "mandame info", "que mas", "cuentame",
        "interesante", "voy a ver", "no ahora",
    ]

    frios = [
        "no gracias", "no me interesa", "ya tengo", "no necesito",
        "no puedo", "estoy ocupado", "no es momento",
        "no tengo tiempo", "no",
    ]

    for palabra in calientes:
        if palabra in texto_lower:
            return {
                "tipo": "CALIENTE",
                "score": 90,
                "razon": f"Palabra clave positiva: '{palabra}'",
                "accion": "Agendar videollamada inmediatamente",
                "confianza": 0.8,
            }

    for palabra in tibios:
        if palabra in texto_lower:
            return {
                "tipo": "TIBIO",
                "score": 50,
                "razon": f"Interes moderado: '{palabra}'",
                "accion": "Enviar caso de exito y reintentar en 3 dias",
                "confianza": 0.7,
            }

    for palabra in frios:
        if palabra in texto_lower:
            return {
                "tipo": "FRIO",
                "score": 20,
                "razon": f"Rechazo: '{palabra}'",
                "accion": "Seguimiento suave en 30 dias",
                "confianza": 0.8,
            }

    return {
        "tipo": "INDEFINIDO",
        "score": 40,
        "razon": "Sin palabra clave clara",
        "accion": "Revisar manualmente",
        "confianza": 0.5,
    }


# === TESTING ===
if __name__ == "__main__":
    test_responses = [
        "Si, me interesa. Cuando podemos hablar?",
        "Despues le escribo",
        "No gracias",
        "Que onda, cuento mas?",
        "Ok perfecto",
        "Estoy ocupado ahora",
        "jajaja",
    ]

    print("=" * 60)
    print("  Clasificador de Respuestas - Test")
    print("=" * 60)

    for resp in test_responses:
        resultado = clasificar_respuesta_basica(resp)
        print(f"\n  Respuesta: '{resp}'")
        print(f"  Tipo: {resultado['tipo']} (Score: {resultado['score']})")
        print(f"  Razon: {resultado['razon']}")
        print(f"  Accion: {resultado['accion']}")
