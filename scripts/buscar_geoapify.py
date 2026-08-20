"""
Lima Automa - Buscador de Restaurantes con Geoapify
====================================================
GRATIS: 3,000 requests/día
"""
import json
import requests
from pathlib import Path


API_KEY = "9f42bcf9bd064b4d9365ef9ff6604e76"


def buscar_restaurantes_geoapify(distrito="Miraflores", radio=1000):
    """
    Busca restaurantes usando Geoapify API.
    """
    distritos = {
        "Miraflores": (-12.1191, -77.0299),
        "San Isidro": (-12.0981, -77.0361),
        "Barranco": (-12.1464, -77.0217),
        "Santiago de Surco": (-12.1358, -76.9931),
        "San Borja": (-12.0961, -76.9991),
        "Jesús María": (-12.0764, -77.0461),
        "La Molina": (-12.0833, -76.9333),
        "San Martín de Porres": (-12.0061, -77.0361),
        "Lima Centro": (-12.0464, -77.0461),
        "Pueblo Libre": (-12.0731, -77.0581),
    }
    
    if distrito not in distritos:
        print(f"  Distrito no encontrado: {distrito}")
        return []
    
    lat, lon = distritos[distrito]
    
    url = "https://api.geoapify.com/v2/places"
    
    params = {
        "categories": "catering.restaurant",
        "filter": f"circle:{lon},{lat},{radio}",
        "limit": 50,
        "lang": "es",
        "apiKey": API_KEY,
        "fields": "name,formatted,phone,website,rating,review_count,opening_hours,categories"
    }
    
    try:
        print(f"  Buscando restaurantes en {distrito}...")
        
        response = requests.get(url, params=params, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            restaurantes = []
            
            for feature in data.get("features", []):
                props = feature.get("properties", {})
                
                # Obtener cuisine de categorías
                categories = props.get("categories", [])
                cuisine = ""
                for cat in categories:
                    if "catering" in cat:
                        cuisine = cat.split(".")[-1]
                        break
                
                restaurante = {
                    "geoapify_id": props.get("place_id"),
                    "name": props.get("name", "Sin nombre"),
                    "phone": props.get("phone", ""),
                    "website": props.get("website", ""),
                    "address": props.get("formatted", ""),
                    "city": distrito,
                    "cuisine": cuisine,
                    "rating": props.get("rating", 0),
                    "reviews": props.get("review_count", 0),
                    "lat": props.get("lat"),
                    "lon": props.get("lon"),
                    "source": "Geoapify"
                }
                restaurantes.append(restaurante)
            
            print(f"  Encontrados: {len(restaurantes)} restaurantes")
            return restaurantes
        else:
            print(f"  Error HTTP: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"  Error: {e}")
        return []


def guardar_resultados(restaurantes, filename="data/clientes_geoapify.json"):
    """Guarda los resultados en un archivo JSON."""
    output_file = Path(filename)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(restaurantes, f, ensure_ascii=False, indent=2)
    
    print(f"  Guardados: {len(restaurantes)} restaurantes en {output_file}")
    return output_file


def mostrar_restaurantes(restaurantes, limite=15):
    """Muestra los restaurantes encontrados."""
    print("\n  RESTAURANTES ENCONTRADOS:")
    print("  " + "-" * 60)
    
    for i, r in enumerate(restaurantes[:limite], 1):
        nombre = r.get("name", "Sin nombre")
        cuisine = r.get("cuisine", "No especificado")
        phone = r.get("phone", "Sin teléfono")
        website = r.get("website", "Sin web")
        rating = r.get("rating", 0)
        address = r.get("address", "")[:50]
        
        print(f"\n  {i}. {nombre}")
        print(f"     Tipo: {cuisine} | Rating: {rating}")
        print(f"     Dirección: {address}")
        print(f"     Tel: {phone} | Web: {website[:30] if website else 'N/A'}")
    
    if len(restaurantes) > limite:
        print(f"\n  ... y {len(restaurantes) - limite} más")


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Buscador Geoapify (GRATIS)")
    print("=" * 60)
    
    # Buscar en Miraflores
    distrito = "Miraflores"
    radio = 2000  # 2 km
    
    restaurantes = buscar_restaurantes_geoapify(distrito, radio)
    
    if restaurantes:
        guardar_resultados(restaurantes)
        mostrar_restaurantes(restaurantes)
        
        print("\n  ¡Búsqueda completada!")
        print("  Guardado en: data/clientes_geoapify.json")
    else:
        print("\n  No se encontraron restaurantes.")


if __name__ == "__main__":
    main()
