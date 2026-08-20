"""
Lima Automa - Scraper Completo Todos los Distritos
===================================================
Busca restaurantes en los 43 distritos de Lima
"""
import json
import requests
import time
import re
from pathlib import Path
from bs4 import BeautifulSoup


# Todos los 43 distritos de Lima
DISTRITOS_LIMA = [
    "ate", "breña", "carabayllo", "cercado-de-lima", "chaclacayo",
    "chorrillos", "cieneguilla", "comas", "el-agustino", "independencia",
    "jesus-maria", "la-molina", "la-victoria", "lima-centro", "lince",
    "los-olivos", "lurigancho", "lurin", "magdalena", "magdalena-del-mar",
    "miraflores", "pachacamac", "pueblo-libre", "puente-piedra",
    "punta-hermosa", "punta-negra", "rimac", "san-borja", "san-isidro",
    "san-juan-de-lurigancho", "san-juan-de-miraflores", "san-luis",
    "san-martin-de-porres", "san-miguel", "santa-anita", "santa-rosa",
    "santiago-de-surco", "surquillo", "villa-el-salvador",
    "villa-maria-del-triunfo"
]


def scrape_cevicherias_distrito(distrito):
    """
    Scrape restaurantes de cevicheriaslima.top para un distrito.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    restaurantes = []
    
    url = f"https://cevicheriaslima.top/{distrito}/"
    
    try:
        response = requests.get(url, headers=headers, timeout=20)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscar enlaces a restaurantes
            links = soup.find_all('a', href=True)
            
            for link in links:
                href = link.get('href', '')
                
                if f'/{distrito}/' in href and len(href) > len(f'/{distrito}/') + 3:
                    nombre = href.split('/')[-2] if href.endswith('/') else href.split('/')[-1]
                    
                    if nombre and len(nombre) > 2 and not nombre.startswith('?'):
                        nombre = nombre.replace('-', ' ').title()
                        
                        if not href.startswith('http'):
                            href = f"https://cevicheriaslima.top{href}"
                        
                        restaurante = {
                            "name": nombre,
                            "url": href,
                            "city": distrito.replace("-", " ").title(),
                            "source": "cevicheriaslima.top"
                        }
                        restaurantes.append(restaurante)
            
    except Exception:
        pass
    
    return restaurantes


def scrape_pagina_restaurante(url):
    """
    Scrape página individual para obtener teléfono.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
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
    print("  LIMA AUTOMA - Scraper Completo 43 Distritos")
    print("=" * 60)
    
    todos_los_restaurantes = []
    distritos_con_datos = 0
    
    # FASE 1: Obtener listas de todos los distritos
    print("\n  FASE 1: Obteniendo listas de restaurantes...")
    print("  " + "-" * 50)
    
    for i, distrito in enumerate(DISTRITOS_LIMA, 1):
        print(f"  {i}/43 - {distrito}...", end=" ")
        
        restaurantes = scrape_cevicherias_distrito(distrito)
        todos_los_restaurantes.extend(restaurantes)
        
        count = len(restaurantes)
        if count > 0:
            distritos_con_datos += 1
            print(f"{count} restaurantes")
        else:
            print("sin datos")
        
        time.sleep(0.3)
    
    print(f"\n  Total listados: {len(todos_los_restaurantes)}")
    print(f"  Distritos con datos: {distritos_con_datos}/43")
    
    # FASE 2: Obtener teléfonos (primeros 500)
    print("\n  FASE 2: Obteniendo teléfonos...")
    print("  (Procesando primeros 500 restaurantes)")
    print("  " + "-" * 50)
    
    enriquecidos = 0
    
    for i, restaurante in enumerate(todos_los_restaurantes[:500], 1):
        url = restaurante.get("url", "")
        
        if url:
            print(f"  {i}/500 - {restaurante['name'][:30]}...", end=" ")
            
            telefono = scrape_pagina_restaurante(url)
            
            if telefono:
                restaurante["phone"] = telefono
                enriquecidos += 1
                print(f"TEL: {telefono}")
            else:
                print("SIN TEL")
            
            time.sleep(0.2)
    
    # Guardar
    output_file = Path("data/restaurantes_43_distritos.json")
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(todos_los_restaurantes, f, ensure_ascii=False, indent=2)
    
    # Estadísticas
    con_telefono = sum(1 for r in todos_los_restaurantes if r.get("phone"))
    
    print("\n" + "=" * 60)
    print(f"  RESULTADOS FINALES:")
    print(f"  Total restaurantes: {len(todos_los_restaurantes)}")
    print(f"  Con teléfono: {con_telefono}")
    print(f"  Distritos cubiertos: {distritos_con_datos}/43")
    print(f"  Guardado en: {output_file}")
    print("=" * 60)
    
    # Top distritos
    print("\n  TOP 10 DISTRITOS:")
    print("  " + "-" * 50)
    
    from collections import Counter
    distrito_count = Counter(r["city"] for r in todos_los_restaurantes)
    
    for distrito, count in distrito_count.most_common(10):
        print(f"  {distrito}: {count} restaurantes")


if __name__ == "__main__":
    main()
