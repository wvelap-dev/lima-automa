"""
Lima Automa - Scraper Páginas Amarillas Perú
=============================================
Extrae teléfonos de restaurantes desde paginasamarillas.com.pe
"""
import json
import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup


def scrape_paginas_amarillas(distrito="miraflores", paginas=3):
    """
    Scraping de Páginas Amarillas Perú.
    
    Args:
        distrito: Nombre del distrito
        paginas: Número de páginas a scrapear
    
    Returns:
        Lista de restaurantes con teléfonos
    """
    restaurantes = []
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-PE,es;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive"
    }
    
    for pagina in range(1, paginas + 1):
        # URL de búsqueda de Páginas Amarillas Perú
        url = f"https://www.paginasamarillas.com.pe/search/restaurantes/{distrito}/pagina-{pagina}"
        
        print(f"  Página {pagina}: {url}")
        
        try:
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar cards de negocios
                cards = soup.find_all('div', class_='business-card') or \
                        soup.find_all('div', class_='result-item') or \
                        soup.find_all('li', class_='result')
                
                if not cards:
                    # Intentar otros selectores
                    cards = soup.find_all('div', {'data-business': True})
                
                print(f"    Encontrados: {len(cards)} cards")
                
                for card in cards:
                    try:
                        # Extraer nombre
                        name_elem = card.find('h2') or card.find('a', class_='business-name')
                        name = name_elem.text.strip() if name_elem else "Sin nombre"
                        
                        # Extraer teléfono
                        phone_elem = card.find('a', href=re.compile(r'tel:')) or \
                                    card.find('span', class_='phone')
                        
                        if phone_elem:
                            phone = phone_elem.text.strip()
                            if not phone and phone_elem.get('href'):
                                phone = phone_elem['href'].replace('tel:', '')
                        else:
                            phone = ""
                        
                        # Extraer dirección
                        addr_elem = card.find('p', class_='address') or \
                                   card.find('span', class_='address')
                        address = addr_elem.text.strip() if addr_elem else ""
                        
                        # Extraer website
                        web_elem = card.find('a', href=re.compile(r'http'))
                        website = web_elem['href'] if web_elem else ""
                        
                        if name != "Sin nombre":
                            restaurante = {
                                "name": name,
                                "phone": phone,
                                "address": address,
                                "website": website,
                                "city": distrito.title(),
                                "source": "Páginas Amarillas"
                            }
                            restaurantes.append(restaurante)
                            
                    except Exception as e:
                        continue
                
                # Rate limiting
                time.sleep(2)
                
            else:
                print(f"    Error HTTP: {response.status_code}")
                
        except Exception as e:
            print(f"    Error: {e}")
    
    return restaurantes


def buscar_por_distrito(distrito):
    """Busca restaurantes en un distrito específico."""
    print(f"\n  Buscando restaurantes en {distrito}...")
    
    restaurantes = scrape_paginas_amarillas(distrito, paginas=2)
    
    print(f"  Encontrados: {len(restaurantes)}")
    
    return restaurantes


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Scraper Páginas Amarillas Perú")
    print("=" * 60)
    
    # Distritos principales
    distritos = [
        "miraflores",
        "san-isidro",
        "barranco",
        "santiago-de-surco",
        "san-borja",
        "jesus-maria",
        "la-molina",
        "lima"
    ]
    
    todos_los_restaurantes = []
    
    for distrito in distritos:
        restaurantes = buscar_por_distrito(distrito)
        todos_los_restaurantes.extend(restaurantes)
    
    # Guardar
    output_file = Path("data/restaurantes_telefonos.json")
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
    
    ejemplos = [r for r in todos_los_restaurantes if r.get("phone")][:10]
    
    for i, r in enumerate(ejemplos, 1):
        print(f"  {i}. {r['name']} - TEL: {r['phone']}")


if __name__ == "__main__":
    main()
