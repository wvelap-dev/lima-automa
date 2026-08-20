"""
Lima Automa - Scraper CeVicheriasLima Top
==========================================
Extrae teléfonos de páginas individuales
"""
import json
import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup


def scrape_lista_restaurantes():
    """
    Obtiene lista de restaurantes desde la página principal.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    restaurantes = []
    
    # Páginas de distritos
    distritos = [
        "miraflores", "san-isidro", "barranco", "santiago-de-surco",
        "san-borja", "jesus-maria", "la-molina", "lima-centro",
        "pueblo-libre", "surquillo", "breña", "lince", "magdalena"
    ]
    
    for distrito in distritos:
        url = f"https://cevicheriaslima.top/{distrito}/"
        
        try:
            print(f"  Buscando en {distrito}...")
            
            response = requests.get(url, headers=headers, timeout=20)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Buscar todos los enlaces a páginas de restaurantes
                links = soup.find_all('a', href=True)
                
                for link in links:
                    href = link.get('href', '')
                    
                    # Filtrar enlaces de restaurantes
                    if f'/{distrito}/' in href and href != f'/{distrito}/':
                        # Obtener nombre del restaurante
                        nombre = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                        nombre = nombre.replace('-', ' ').title()
                        
                        # Construir URL completa
                        if not href.startswith('http'):
                            href = f"https://cevicheriaslima.top{href}"
                        
                        restaurante = {
                            "name": nombre,
                            "url": href,
                            "city": distrito.replace("-", " ").title(),
                            "source": "cevicheriaslima.top"
                        }
                        restaurantes.append(restaurante)
                
                print(f"    {distrito}: {len([r for r in restaurantes if r['city'] == distrito.replace('-', ' ').title()])} restaurantes")
                
                time.sleep(0.5)
                
        except Exception as e:
            print(f"    Error: {e}")
    
    return restaurantes


def scrape_pagina_restaurante(url):
    """
    Scrape una página individual de restaurante para obtener teléfono.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar teléfono
            phone_elem = soup.find('a', href=re.compile(r'tel:'))
            if phone_elem:
                return phone_elem['href'].replace('tel:', '').strip()
            
            # Buscar en texto
            text = soup.get_text()
            phone_match = re.search(r'\+51\s*\d{3}\s*\d{3}\s*\d{4}', text)
            if phone_match:
                return phone_match.group(0)
            
        return ""
        
    except Exception:
        return ""


def main():
    """Función principal."""
    print("=" * 60)
    print("  LIMA AUTOMA - Scraper CeVicheriasLima Top")
    print("=" * 60)
    
    # Paso 1: Obtener lista de restaurantes
    print("\n  PASO 1: Obteniendo lista de restaurantes...")
    restaurantes = scrape_lista_restaurantes()
    
    print(f"\n  Total restaurantes encontrados: {len(restaurantes)}")
    
    # Paso 2: Scrapear páginas individuales (primeros 100)
    print("\n  PASO 2: Obteniendo teléfonos...")
    print("  (Procesando primeros 100 restaurantes)")
    
    enriquecidos = 0
    
    for i, restaurante in enumerate(restaurantes[:100], 1):
        url = restaurante.get("url", "")
        
        if url:
            print(f"  {i}/100 - {restaurante['name'][:30]}...", end=" ")
            
            telefono = scrape_pagina_restaurante(url)
            
            if telefono:
                restaurante["phone"] = telefono
                enriquecidos += 1
                print(f"TEL: {telefono}")
            else:
                print("SIN TEL")
            
            time.sleep(0.3)
    
    # Guardar
    output_file = Path("data/restaurantes_cevicherias.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(restaurantes, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    con_telefono = sum(1 for r in restaurantes if r.get("phone"))
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS:")
    print(f"  Total restaurantes: {len(restaurantes)}")
    print(f"  Con teléfono: {con_telefono}")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)
    
    # Mostrar ejemplos
    print("\n  EJEMPLOS CON TELÉFONO:")
    print("  " + "-" * 50)
    
    ejemplos = [r for r in restaurantes if r.get("phone")][:10]
    
    for i, r in enumerate(ejemplos, 1):
        print(f"  {i}. {r['name'][:40]} - TEL: {r['phone']}")


if __name__ == "__main__":
    main()
