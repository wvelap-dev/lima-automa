"""
Lima Automa - Enriquecer Restaurantes con Teléfonos
====================================================
Busca teléfonos individuales de cada restaurante
"""
import json
import requests
import time
import re
from pathlib import Path


def buscar_telefono_google(nombre_restaurante, distrito="Miraflores"):
    """
    Busca teléfono usando Google Search (sin API key).
    """
    query = f'"{nombre_restaurante}" "{distrito}" Lima telefono'
    
    url = "https://www.google.com/search"
    
    params = {
        "q": query,
        "hl": "es"
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "es-PE,es;q=0.9"
    }
    
    try:
        response = requests.get(url, params=params, headers=headers, timeout=15)
        
        if response.status_code == 200:
            # Buscar teléfonos en el HTML
            phone_patterns = [
                r'\(\d{3}\)\s*\d{3}-\d{4}',  # (01) 234-5678
                r'\d{3}-\d{3}-\d{4}',  # 012-345-6789
                r'\+51\s*\d{3}\s*\d{3}\s*\d{4}',  # +51 999 888 777
                r'9\d{8}',  # 999888777
                r'01\d{7}',  # 012345678
            ]
            
            phones_found = []
            for pattern in phone_patterns:
                matches = re.findall(pattern, response.text)
                phones_found.extend(matches)
            
            # Filtrar teléphonos válidos (no genéricos)
            valid_phones = []
            for phone in phones_found:
                phone_clean = phone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                # Teléfonos válidos de Perú: 9 dígitos (celular) o 7-8 dígitos (fijo)
                if len(phone_clean) >= 7 and phone_clean not in ["929705612", "012345678"]:
                    valid_phones.append(phone)
            
            if valid_phones:
                return valid_phones[0]
        
        return ""
        
    except Exception as e:
        return ""


def buscar_telefono_directorio(nombre_restaurante, distrito="Miraflores"):
    """
    Busca teléfono en directorios web peruanos.
    """
    # Directorios peruanos con scraping simple
    directorios = [
        {
            "name": "DirectedPeru",
            "url": f"https://www.directedperu.com/search?q={nombre_restaurante.replace(' ', '+')}"
        },
        {
            "name": "GuiaPe", 
            "url": f"https://www.guiape.com.pe/buscar?q={nombre_restaurante.replace(' ', '+')}"
        }
    ]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept-Language": "es-PE,es;q=0.9"
    }
    
    for directorio in directorios:
        try:
            response = requests.get(directorio["url"], headers=headers, timeout=10)
            
            if response.status_code == 200:
                phone_patterns = [
                    r'\(\d{3}\)\s*\d{3}-\d{4}',
                    r'\d{3}-\d{3}-\d{4}',
                    r'\+51\s*\d{3}\s*\d{3}\s*\d{4}',
                    r'9\d{8}',
                    r'01\d{7}',
                ]
                
                phones_found = []
                for pattern in phone_patterns:
                    matches = re.findall(pattern, response.text)
                    phones_found.extend(matches)
                
                # Filtrar genéricos
                valid_phones = [p for p in phones_found if p not in ["929705612", "012345678"]]
                
                if valid_phones:
                    return valid_phones[0]
                    
        except Exception:
            continue
    
    return ""


def enrich_restaurantes():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Enriqueciendo Restaurantes")
    print("=" * 60)
    
    # Cargar restaurantes
    input_file = Path("data/clientes_geoapify_completo.json")
    
    if not input_file.exists():
        print("\n  No hay archivo de restaurantes.")
        return
    
    with open(input_file, "r", encoding="utf-8") as f:
        restaurantes = json.load(f)
    
    print(f"\n  Restaurantes cargados: {len(restaurantes)}")
    
    # Buscar teléfonos (solo primeros 100)
    print("\n  Buscando teléfonos...")
    print("  (Procesando primeros 100 restaurantes)")
    
    enriquecidos = 0
    
    for i, restaurante in enumerate(restaurantes[:100], 1):
        nombre = restaurante.get("name", "")
        distrito = restaurante.get("city", "Miraflores")
        
        if nombre and nombre != "Sin nombre":
            print(f"  {i}/100 - {nombre}...", end=" ")
            
            # Intentar con Google
            telefono = buscar_telefono_google(nombre, distrito)
            
            # Si no funciona, intentar con directorios
            if not telefono:
                telefono = buscar_telefono_directorio(nombre, distrito)
            
            if telefono:
                restaurante["phone"] = telefono
                enriquecidos += 1
                print(f"TEL: {telefono}")
            else:
                print("SIN TEL")
            
            # Rate limiting
            time.sleep(0.5)
    
    # Guardar
    output_file = Path("data/clientes_enriquecidos.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(restaurantes, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS:")
    print(f"  Total: {len(restaurantes)}")
    print(f"  Con teléfono: {enriquecidos}")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    enrich_restaurantes()
