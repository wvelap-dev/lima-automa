"""
Lima Automa - Buscar Más Restaurantes (Respetando Rate Limits)
==============================================================
Geoapify Free: 3,000 créditos/día, 5 req/seg
"""
import json
import requests
import time
from pathlib import Path


API_KEY = "9f42bcf9bd064b4d9365ef9ff6604e76"


def buscar_restaurantes(distrito, lat, lon, radio=1500, offset=0):
    """Busca restaurantes con offset para paginación."""
    url = "https://api.geoapify.com/v2/places"
    
    params = {
        "categories": "catering.restaurant",
        "filter": f"circle:{lon},{lat},{radio}",
        "limit": 50,
        "offset": offset,
        "lang": "es",
        "apiKey": API_KEY
    }
    
    try:
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            restaurantes = []
            
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                
                categories = props.get("categories", [])
                cuisine = ""
                for cat in categories:
                    if "catering" in cat:
                        cuisine = cat.split(".")[-1]
                        break
                
                restaurante = {
                    "name": props.get("name", "Sin nombre"),
                    "phone": props.get("phone", ""),
                    "website": props.get("website", ""),
                    "address": props.get("formatted", ""),
                    "city": distrito,
                    "cuisine": cuisine,
                    "lat": props.get("lat"),
                    "lon": props.get("lon"),
                    "source": "Geoapify"
                }
                restaurantes.append(restaurante)
            
            return restaurantes
        else:
            print(f"    Error HTTP: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"    Error: {e}")
        return []


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Buscar Más Restaurantes")
    print("  Geoapify Free: 3,000 créditos/día, 5 req/seg")
    print("=" * 60)
    
    # Distritos principales
    distritos = {
        "Miraflores": (-12.1191, -77.0299),
        "San Isidro": (-12.0981, -77.0361),
        "Barranco": (-12.1464, -77.0217),
        "Santiago de Surco": (-12.1358, -76.9931),
        "San Borja": (-12.0961, -76.9991),
        "Jesús María": (-12.0764, -77.0461),
        "La Molina": (-12.0833, -76.9333),
        "Lima Centro": (-12.0464, -77.0461),
    }
    
    todos_los_restaurantes = []
    creditos_usados = 0
    
    for distrito, (lat, lon) in distritos.items():
        print(f"\n  Buscando en {distrito}...")
        
        # Buscar hasta 100 restaurantes por distrito (2 páginas)
        for offset in [0, 50]:
            restaurantes = buscar_restaurantes(distrito, lat, lon, offset=offset)
            todos_los_restaurantes.extend(restaurantes)
            creditos_usados += 1
            
            print(f"    Offset {offset}: {len(restaurantes)} restaurantes")
            
            # Rate limiting: 5 req/seg = 200ms entre requests
            time.sleep(0.25)
    
    # Guardar todos
    output_file = Path("data/clientes_geoapify_completo.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(todos_los_restaurantes, f, ensure_ascii=False, indent=2)
    
    print("\n" + "=" * 60)
    print(f"  TOTAL: {len(todos_los_restaurantes)} restaurantes")
    print(f"  Créditos usados: {creditos_usados}")
    print(f"  Créditos restantes: {3000 - creditos_usados}")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)


if __name__ == "__main__":
    main()
