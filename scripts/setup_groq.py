"""
Lima Automa - Configuración de Groq (Gratis)
=============================================
Groq ofrece inference ultrarrápida con modelos open-source gratis.
"""
import os
from pathlib import Path


def setup_groq():
    """Configura Groq para Lima Automa."""
    print("=" * 60)
    print("  LIMA AUTOMA - Configuración de Groq")
    print("=" * 60)
    
    print("""
    Groq es una API de IA GRATUITA que ofrece:
    - Velocidad: 300-800 tokens/segundo
    - Modelos: Llama 3.3 70B, Llama 3.1 8B, Mixtral, etc.
    - Límites: 30 requests/minuto, 14,400 requests/día
    - Sin tarjeta de crédito requerida
    """)
    
    # Verificar si ya tiene la API key
    existing_key = os.environ.get("GROQ_API_KEY")
    if existing_key:
        print(f"  ✅ GROQ_API_KEY ya configurada: {existing_key[:10]}...")
        return existing_key
    
    # Pedir API key
    print("  Para obtener tu API key gratis:")
    print("  1. Ve a https://console.groq.com")
    print("  2. Crea una cuenta (gratis)")
    print("  3. Ve a API Keys")
    print("  4. Crea una nueva API key")
    print()
    
    api_key = input("  Ingresa tu GROQ_API_KEY (o presiona Enter para usar Ollama): ").strip()
    
    if not api_key:
        print("\n  Usando Ollama como fallback.")
        return None
    
    # Guardar en archivo .env
    env_file = Path(".env")
    env_content = ""
    if env_file.exists():
        with open(env_file, "r") as f:
            env_content = f.read()
    
    # Agregar o actualizar GROQ_API_KEY
    if "GROQ_API_KEY" in env_content:
        lines = env_content.split("\n")
        for i, line in enumerate(lines):
            if line.startswith("GROQ_API_KEY="):
                lines[i] = f"GROQ_API_KEY={api_key}"
                break
        env_content = "\n".join(lines)
    else:
        env_content += f"\nGROQ_API_KEY={api_key}"
    
    with open(env_file, "w") as f:
        f.write(env_content.strip())
    
    print(f"\n  ✅ API key guardada en .env")
    return api_key


def test_groq(api_key):
    """Prueba la conexión con Groq."""
    try:
        from openai import OpenAI
        
        client = OpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1"
        )
        
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "user", "content": "Hola, responde en español con una frase corta."}
            ],
            max_tokens=50
        )
        
        print(f"\n  ✅ Groq funcionando!")
        print(f"  Respuesta: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"\n  ❌ Error: {e}")
        return False


if __name__ == "__main__":
    api_key = setup_groq()
    if api_key:
        test_groq(api_key)
