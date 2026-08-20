"""
Lima Automa - Scraper Múltiples Fuentes
========================================
Extrae teléfonos de cevicheriaslima.top y otros directorios
"""
import json
import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup


def scrape_cevicherias_lima(distrito="miraflores"):
    """
    Scraping de cevicheriaslima.top - Tiene teléfonos reales.
    """
    restaurantes = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-PE,es;q=0.9"
    }
    
    # URL base
    base_url = f"https://cevicheriaslima.top/{distrito}/"
    
    try:
        print(f"  Buscando en {distrito}...")
        
        response = requests.get(base_url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar cards de restaurantes
            cards = soup.find_all('div', class_='card') or \
                    soup.find_all('article') or \
                    soup.find_all('div', class_='listing')
            
            if not cards:
                # Buscar por patrones de enlaces
                cards = soup.find_all('a', href=re.compile(r'/' + distrito + r'/'))
            
            print(f"    Encontrados: {len(cards)} elementos")
            
            for card in cards:
                try:
                    # Extraer nombre
                    name_elem = card.find('h2') or card.find('h3') or card.find('a')
                    name = name_elem.text.strip() if name_elem else ""
                    
                    # Extraer teléfono
                    phone_elem = card.find('a', href=re.compile(r'tel:'))
                    if phone_elem:
                        phone = phone_elem['href'].replace('tel:', '').strip()
                    else:
                        phone = ""
                    
                    # Extraer dirección
                    addr_elem = card.find('p') or card.find('span', class_='address')
                    address = addr_elem.text.strip() if addr_elem else ""
                    
                    # Extraer rating
                    rating_elem = card.find('span', class_='rating') or \
                                 card.find('div', class_='stars')
                    rating = rating_elem.text.strip() if rating_elem else ""
                    
                    if name and len(name) > 2:
                        restaurante = {
                            "name": name[:100],
                            "phone": phone,
                            "address": address[:200],
                            "rating": rating,
                            "city": distrito.replace("-", " ").title(),
                            "source": "cevicheriaslima.top"
                        }
                        restaurantes.append(restaurante)
                        
                except Exception as e:
                    continue
            
            time.sleep(1)
            
        else:
            print(f"    Error HTTP: {response.status_code}")
            
    except Exception as e:
        print(f"    Error: {e}")
    
    return restaurantes


def scrape_eldirectorio(distrito="lima"):
    """
    Scraping de pe.eldirectorio.co
    """
    restaurantes = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    url = f"https://pe.eldirectorio.co/empresas/{distrito}/restaurantes"
    
    try:
        print(f"  Buscando en eldirectorio.co/{distrito}...")
        
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar listings
            listings = soup.find_all('div', class_='listing') or \
                      soup.find_all('div', class_='business')
            
            print(f"    Encontrados: {len(listings)} listings")
            
            for listing in listings:
                try:
                    name_elem = listing.find('h2') or listing.find('h3')
                    name = name_elem.text.strip() if name_elem else ""
                    
                    phone_elem = listing.find('a', href=re.compile(r'tel:'))
                    phone = phone_elem['href'].replace('tel:', '').strip() if phone_elem else ""
                    
                    addr_elem = listing.find('p', class_='address')
                    address = addr_elem.text.strip() if addr_elem else ""
                    
                    if name:
                        restaurante = {
                            "name": name[:100],
                            "phone": phone,
                            "address": address[:200],
                            "city": distrito.title(),
                            "source": "eldirectorio.co"
                        }
                        restaurantes.append(restaurante)
                        
                except Exception:
                    continue
            
            time.sleep(1)
            
    except Exception as e:
        print(f"    Error: {e}")
    
    return restaurantes


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Scraper Múltiples Fuentes")
    print("=" * 60)
    
    # Distritos de Lima
    distritos = [
        "miraflores",
        "san-isidro",
        "barranco",
        "santiago-de-surco",
        "san-borja",
        "jesus-maria",
        "la-molina",
        "lima-centro",
        "pueblo-libre",
        "surquillo"
    ]
    
    todos_los_restaurantes = []
    
    # Scraping de cevicheriaslima.top
    print("\n  FUENTE 1: cevicheriaslima.top (1134+ restaurantes)")
    print("  " + "-" * 50)
    
    for distrito in distritos:
        restaurantes = scrape_cevicherias_lima(distrito)
        todos_los_restaurantes.extend(restaurantes)
        print(f"    {distrito}: {len(restaurantes)} restaurantes")
    
    # Scraping de eldirectorio.co
    print("\n  FUENTE 2: pe.eldirectorio.co")
    print("  " + "-" * 50)
    
    for distrito in ["lima", "miraflores", "san-isidro"]:
        restaurantes = scrape_eldirectorio(distrito)
        todos_los_restaurantes.extend(restaurantes)
        print(f"    {distrito}: {len(restaurantes)} restaurantes")
    
    # Guardar
    output_file = Path("data/restaurantes_directorio.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(todos_los_restaurantes, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    con_telefono = sum(1 for r in todos_los_restaurantes if r.get("phone"))
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS:")
    print(f"  Total restaurantes: {len(todos_los_restaurantes)}")
    print(f"  Con teléfono: {con_telefono}")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)
    
    # Mostrar ejemplos
    print("\n  EJEMPLOS CON TELÉFONO:")
    print("  " + "-" * 50)
    
    ejemplos = [r for r in todos_los_restaurantes if r.get("phone")][:15]
    
    for i, r in enumerate(ejemplos, 1):
        print(f"  {i}. {r['name'][:40]}")
        print(f"     TEL: {r['phone']} | {r['city']}")


if __name__ == "__main__":
    main()
